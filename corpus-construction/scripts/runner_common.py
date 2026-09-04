#!/usr/bin/env python3
"""
runner_common.py -- plumbing shared by the teacher runners.

Everything in here is provider-agnostic: key loading, the pricing table, cost maths,
JSON salvage, the run-directory layout, checkpoint/resume, and the run manifest. The
provider-specific parts (how a call is built, how usage is reported, how web search
works) stay in the runner that owns them.

The one rule worth stating: a run is identified by (model, reasoning_effort, prompt),
not by a timestamp. That triple is what an ablation varies, so it is what the output
tree is keyed on, and it is what makes a run resumable -- a timestamped directory is
unfindable by definition on the next invocation.

    outputs/runs/<model>/<effort>/<prompt_stem>/
        <tag>_responses.jsonl    raw text + parsed JSON, one line per review
        <tag>_meta.jsonl         usage, cost, latency, status, contract errors
        <tag>_summary.json       scoreboard row + the run manifest
        checkpoint.json          progress counters, for --resume
"""

from __future__ import annotations

import json
import os
import random
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------- pricing
# USD per million tokens. Check the pricing page on the day you run and record the
# date; these move, and the paper needs the rates that were live for the run.
#
# Keyed by model id. The runner looks the model up here instead of you editing a
# constant -- swapping --model luna/terra used to mean remembering to swap a pricing
# block by hand, and a forgotten swap silently produces a 10x-wrong cost projection.

PRICING_TABLE: dict[str, dict] = {
    "gpt-5.6-luna": {
        "model": "gpt-5.6-luna",
        "as_of": "2026-08-21",
        "input": 0.20,
        "cached_input": 0.02,      # 0.1x input
        "cache_write": 0.25,       # 1.25x input
        "output": 1.20,
    },
    "gpt-5.6-sol": {
        "model": "gpt-5.6-sol",
        "as_of": "2026-08-22",
        "input": 4.00,
        "cached_input": 0.40,      # 0.1x input
        "cache_write": 5.00,       # 1.25x input
        "output": 20.00,
    },
    "gpt-5.6-terra": {
        "model": "gpt-5.6-terra",
        "as_of": "2026-08-21",
        "input": 2.00,
        "cached_input": 0.20,      # 0.1x input
        "cache_write": 2.50,       # 1.25x input
        "output": 12.00,
    },
    "kimi-k3": {
        "model": "kimi-k3",
        "as_of": "2026-08-21",
        "input": 3.00,             # cache miss
        "cached_input": 0.30,      # cache hit, 0.1x
        "cache_write": 0.0,        # automatic caching: no write charge
        "output": 15.00,
        # $0.005 is Moonshot's confirmed fee for the $web_search BUILTIN's trigger
        # (platform.kimi.ai/docs/pricing/tools). The k3 path uses the Formula channel
        # instead (moonshot/web-search:latest); its fiber-execution fee was NOT
        # separately confirmed at write time -- check before trusting spend totals.
        "search_per_call": 0.005,
    },

    # ---- Anthropic ----------------------------------------------------------
    # Cache read is 0.1x input, cache write 1.25x input (5-minute ephemeral TTL).
    # The web_search server tool is billed per search on top of tokens.
    "claude-opus-5": {
        "model": "claude-opus-5",
        "as_of": "2026-08-22",
        "input": 5.00,
        "cached_input": 0.50,      # 0.1x input
        "cache_write": 6.25,       # 1.25x input
        "output": 25.00,
        "search_per_call": 0.010,  # $10 / 1000 searches
        "search_backend": "anthropic_builtin",
    },
    "claude-sonnet-5": {
        "model": "claude-sonnet-5",
        "as_of": "2026-08-22",
        # INTRO PRICING, and it expires. List is 3.00/15.00; the promotional rate
        # below is what is live through 2026-08-31. Both are carried so a re-run in
        # September is caught by the preflight check rather than silently mispriced.
        "input": 2.00,
        "cached_input": 0.20,
        "cache_write": 2.50,
        "output": 10.00,
        "search_per_call": 0.010,
        "search_backend": "anthropic_builtin",
        "intro_until": "2026-08-31",
        "list_input": 3.00,
        "list_cached_input": 0.30,
        "list_cache_write": 3.75,
        "list_output": 15.00,
    },
    "claude-haiku-4-5": {
        "model": "claude-haiku-4-5",
        "as_of": "2026-08-22",
        # INTRO PRICING, and it expires. List is 3.00/15.00; the promotional rate
        # below is what is live through 2026-08-31. Both are carried so a re-run in
        # September is caught by the preflight check rather than silently mispriced.
        "input": 1.00,
        "cached_input": 0.10,
        "cache_write": 1.25,
        "output": 5.00,
        "search_per_call": 0.010,
        "search_backend": "anthropic_builtin",
        "intro_until": "2026-08-31",
        "list_input": 3.00,
        "list_cached_input": 0.30,
        "list_cache_write": 3.75,
        "list_output": 15.00,
    },

    # ---- DeepSeek -----------------------------------------------------------
    # DEEPSEEK: the rate depends on the UTC clock. Peak is 01:00-04:00 and
    # 06:00-10:00 UTC and costs exactly double; every other hour is off-peak. The
    # top level below IS the off-peak table, so a caller that forgets `when=` still
    # gets a complete, correctly-labelled dict rather than a KeyError. Pass
    # `when=` to pricing_for() to have the window resolved for you.
    #
    # search_per_call is TAVILY's list price, not DeepSeek's -- DeepSeek has no
    # search product. It lives here so cost_usd() needs no special-casing and the
    # run's total bill is honest. web_search_tool.py asserts the two agree.
    "deepseek-v4-pro": {
        "model": "deepseek-v4-pro",
        "as_of": "2026-08-22",
        "input": 0.66,             # cache miss, off-peak
        "cached_input": 0.022,     # cache hit, off-peak
        "cache_write": 0.0,        # automatic caching: no write charge
        "output": 1.98,
        "window": "off_peak",
        "search_per_call": 0.008,
        "search_backend": "tavily",
        "peak_hours_utc": [[1, 4], [6, 10]],
        "windows": {
            "off_peak": {"input": 0.66, "cached_input": 0.022,
                         "cache_write": 0.0, "output": 1.98},
            "peak":     {"input": 1.32, "cached_input": 0.044,
                         "cache_write": 0.0, "output": 3.96},
        },
    },
    "deepseek-v4-flash": {
        "model": "deepseek-v4-flash",
        "as_of": "2026-08-22",
        "input": 0.22,
        "cached_input": 0.007,
        "cache_write": 0.0,
        "output": 0.66,
        "window": "off_peak",
        "search_per_call": 0.008,
        "search_backend": "tavily",
        "peak_hours_utc": [[1, 4], [6, 10]],
        "windows": {
            "off_peak": {"input": 0.22, "cached_input": 0.007,
                         "cache_write": 0.0, "output": 0.66},
            "peak":     {"input": 0.44, "cached_input": 0.014,
                         "cache_write": 0.0, "output": 1.32},
        },
    },
}


# DeepSeek's peak windows, as half-open [start, end) UTC hours. Half-open matters at
# the edges: 04:00 and 10:00 are the first off-peak hours, not the last peak ones.
PEAK_WINDOWS_UTC = ((1, 4), (6, 10))


def pricing_window(when: datetime | None = None, windows=PEAK_WINDOWS_UTC) -> str:
    """Which price window a call made at `when` falls in. Keyed on the hour the call
    STARTS, in UTC. A review that straddles a boundary is billed at the window it
    began in -- which is an assumption, so the runner records utc_hour on every row."""
    when = when or datetime.now(timezone.utc)
    if when.tzinfo is not None:
        when = when.astimezone(timezone.utc)
    return "peak" if any(lo <= when.hour < hi for lo, hi in windows) else "off_peak"


def pricing_for(model: str, when: datetime | None = None,
                window: str | None = None) -> dict:
    """Exact match first, then the longest prefix. The prefix fallback exists because
    the served model_version is often the dated build (gpt-5.6-luna-2026-08-01) while
    the request names the alias.

    `when` only matters for providers whose rate depends on the clock (DeepSeek). For
    everyone else the entry carries no "windows" key and the dict comes back untouched,
    so every existing one-argument call site keeps exactly the behaviour it had. When
    there IS a window, the returned dict is still FLAT -- same keys, same shape -- so
    cost_usd() and compute_run_stats.py keep consuming it as a plain rate card."""
    entry = None
    if model in PRICING_TABLE:
        entry = PRICING_TABLE[model]
    else:
        hits = sorted((k for k in PRICING_TABLE if model.startswith(k)), key=len)
        if hits:
            entry = PRICING_TABLE[hits[-1]]
    if entry is None:
        sys.exit(
            f"no pricing for model {model!r}.\n"
            f"  known: {', '.join(sorted(PRICING_TABLE))}\n"
            f"  add it to PRICING_TABLE in runner_common.py, with the date you read it."
        )

    if "windows" not in entry:
        return entry

    when = when or datetime.now(timezone.utc)
    # An explicit `window` pins the whole run to one declared rate card instead of
    # resolving per call. That is an ASSUMPTION, so it is recorded as one: the caller
    # writes pricing_pinned into the meta rows and the summary.
    win = window or pricing_window(
        when, tuple(tuple(w) for w in entry.get("peak_hours_utc", PEAK_WINDOWS_UTC)))
    if win not in entry["windows"]:
        sys.exit(f"unknown price window {win!r} for {model}: "
                 f"known {', '.join(sorted(entry['windows']))}")
    out = {k: v for k, v in entry.items() if k != "windows"}
    out |= entry["windows"][win]
    out["window"] = win
    out["window_pinned"] = window is not None
    out["window_resolved_at"] = when.astimezone(timezone.utc).isoformat(timespec="seconds")
    return out


def cost_usd(u: dict, pricing: dict, n_searches: int = 0) -> dict:
    """Cost of one review from exact token counts. The three input buckets are
    disjoint. n_searches is billed on top where the provider charges per search."""
    c_cached = (u.get("cached_tokens") or 0)         * pricing["cached_input"] / 1e6
    c_write  = (u.get("cache_write_tokens") or 0)    * pricing.get("cache_write", 0.0) / 1e6
    c_plain  = (u.get("uncached_input_tokens") or 0) * pricing["input"] / 1e6
    c_out    = (u.get("output_tokens") or 0)         * pricing["output"] / 1e6
    c_search = n_searches * pricing.get("search_per_call", 0.0)
    out = {"cached": round(c_cached, 8), "cache_write": round(c_write, 8),
           "uncached_input": round(c_plain, 8), "output": round(c_out, 8),
           "total": round(c_cached + c_write + c_plain + c_out + c_search, 8)}
    if c_search:
        out["search"] = round(c_search, 8)
    return out


# ------------------------------------------------------------------------- keys

def load_api_key(env_var: str, script_dir: Path, env_file: str = ".env") -> str:
    """Real environment first, then a KEY=value file next to the script.
    Never hardcode the key in a script -- it goes to git and into the paper repo."""
    key = os.environ.get(env_var)
    if not key:
        envfile = script_dir / env_file
        if envfile.exists():
            for line in envfile.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == env_var:
                    key = v.strip().strip("\"'")
                    break
    if not key:
        sys.exit(
            f"No API key found.\n"
            f"  export {env_var}=sk-...\n"
            f"or put a line in {script_dir / env_file}:\n"
            f"  {env_var}=sk-...\n"
            f"(add {env_file} to .gitignore)"
        )
    print(f"key loaded ({key[:7]}...{key[-4:]})", file=sys.stderr)
    return key


# ------------------------------------------------------------------------ retry
# Two failure families, and they want opposite handling. A 429 or a 5xx or a dropped
# socket is transient: back off and try again. A 400 is a malformed request -- a bad
# cache breakpoint, an unsupported parameter -- and will fail identically forever, so
# retrying it three times with backoff just wastes wall clock before the same death.

NON_RETRYABLE_STATUS = {400, 401, 403, 404, 409, 422}


def status_code_of(exc: Exception) -> int | None:
    for attr in ("status_code", "http_status"):
        code = getattr(exc, attr, None)
        if isinstance(code, int):
            return code
    resp = getattr(exc, "response", None)
    code = getattr(resp, "status_code", None)
    return code if isinstance(code, int) else None


def is_retryable(exc: Exception) -> bool:
    code = status_code_of(exc)
    if code is None:
        return True                      # timeouts, connection resets, unknown shapes
    if code in (408, 409, 425, 429):
        return True
    return not (code in NON_RETRYABLE_STATUS or 400 <= code < 500)


def backoff_seconds(attempt: int, exc: Exception, rng: random.Random) -> float:
    """Exponential with jitter. Jitter matters even single-threaded: a rate limit you
    hit at a fixed cadence you keep hitting at a fixed cadence."""
    code = status_code_of(exc)
    retry_after = getattr(exc, "retry_after", None)
    if isinstance(retry_after, (int, float)) and retry_after > 0:
        return float(retry_after)
    base = 10.0 * (attempt + 1) if code == 429 else 2.0 ** attempt
    return base * (1.0 + rng.random() * 0.25)


def call_with_retries(fn, retries: int, rng: random.Random, label: str = ""):
    """Run fn() with the retry policy above.
    Returns (result, latency, error_type, error_message) -- error_type is the
    exception class name alone, kept separate from the message so downstream
    gating can count error kinds without substring surgery."""
    for attempt in range(retries):
        t0 = time.time()
        try:
            return fn(), time.time() - t0, None, None
        except Exception as e:
            etype = type(e).__name__
            last = attempt == retries - 1
            if last or not is_retryable(e):
                why = "" if last else " (not retryable)"
                return None, time.time() - t0, etype, f"{e}{why}"
            wait = backoff_seconds(attempt, e, rng)
            print(f"    retry {attempt+1}/{retries-1} after {etype} "
                  f"(sleep {wait:.1f}s){' ' + label if label else ''}", file=sys.stderr)
            time.sleep(wait)


# -------------------------------------------------------------------- json parse

def parse_json(text: str) -> tuple[dict | None, str]:
    """Salvage a JSON object from a model response. The note records what had to be
    done to get there, which is itself a compliance signal worth scoring."""
    raw = (text or "").strip()
    note = "clean"
    if raw.startswith("```"):
        raw, note = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw).strip(), "stripped_fence"
    try:
        return json.loads(raw), note
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", raw, re.S)
        if m:
            try:
                return json.loads(m.group(0)), "extracted_braces"
            except json.JSONDecodeError:
                pass
    return None, "parse_failed"


# ------------------------------------------------------------- contract checking
# The prompt's own output spec lists the legal codes. Reading them back out of the
# rendered prompt (rather than out of the codebook) means the check is always against
# what this run actually asked for, even if the codebook has moved on since the build.

_CODE_BLOCK = re.compile(r"spelled exactly:\s*\n\n(.*?)\n\s*\n", re.S)


def legal_codes_from_prompt(prompt: str) -> set[str]:
    m = _CODE_BLOCK.search(prompt)
    if not m:
        return set()
    return {ln.strip() for ln in m.group(1).splitlines() if ln.strip()}


def check_contract(parsed: dict | None, review_text: str, legal: set[str]) -> dict:
    """The codebook rules that can be checked mechanically, checked at run time
    instead of an hour later in compute_run_stats.py. A prompt that emits illegal
    codes is worth killing at review 3, not at review 50."""
    v = {"bad_codes": [], "dup_codes": [], "missing_span": [],
         "span_bad": [], "span_loose": [], "labels": []}
    if not parsed:
        return v
    seen: list[str] = []
    for item in parsed.get("labels") or []:
        if not isinstance(item, dict):
            v["bad_codes"].append(str(item)[:40])
            continue
        code, span = item.get("label"), item.get("span")
        if legal and code not in legal:
            v["bad_codes"].append(str(code))
            continue
        if code in seen:
            v["dup_codes"].append(code)                      # R1
        seen.append(code)
        v["labels"].append(code)
        if not span:
            v["missing_span"].append(code)                   # R3
        elif span not in review_text:
            norm = lambda s: " ".join(s.split()).lower()
            bucket = "span_loose" if norm(span) in norm(review_text) else "span_bad"
            v[bucket].append(code)
    return v


def contract_errors(v: dict) -> list[str]:
    """Compact one-line rendering for the live log; empty means the row is clean."""
    out = []
    for key, msg in (("bad_codes", "illegal code"), ("dup_codes", "dup (R1)"),
                     ("missing_span", "no span (R3)"), ("span_bad", "span not verbatim")):
        if v[key]:
            out.append(f"{msg}: {','.join(str(c) for c in v[key])}")
    return out


# ------------------------------------------------------------------ usage maths

def add_usage(a: dict, b: dict) -> dict:
    """Sum usage across the calls that make up one review -- tool-loop rounds, and
    re-attempts after an unparseable response. Every attempt was billed, so every
    attempt has to land in the total or the cost projection is a fiction."""
    if not a:
        return dict(b)
    out = {k: (a.get(k) or 0) + (b.get(k) or 0) for k in b if k != "total_tokens"}
    out["total_tokens"] = (a.get("total_tokens") or 0) + (b.get("total_tokens") or 0)
    return out


def print_stats(tag: str, u: dict, latency: float, show_write: bool = True) -> None:
    hit = (u.get("cached_tokens") or 0) / u["input_tokens"] if u.get("input_tokens") else 0
    written = (f"written={u.get('cache_write_tokens', 0):,} " if show_write else "")
    print(f"[{datetime.now():%H:%M:%S}] {tag}  "
          f"input={u['input_tokens']:,} cached={u.get('cached_tokens', 0):,} ({hit:.0%}) "
          f"{written}"
          f"output={u['output_tokens']:,} (reasoning={u.get('reasoning_tokens', 0):,}) "
          f"{latency:.1f}s")


class CacheWatch:
    """A cold prefix costs 1.25x on call 1 and 0.1x forever after. If calls 3+ are
    still missing, the prefix is not matching and the run is quietly costing 10x --
    which --dry checks for and the actual run never used to. Warn once, loudly."""

    def __init__(self, floor: float = 0.5, warm_after: int = 2):
        self.floor, self.warm_after, self.n, self.warned = floor, warm_after, 0, False

    def observe(self, u: dict) -> None:
        self.n += 1
        if self.warned or self.n <= self.warm_after or not u.get("input_tokens"):
            return
        hit = (u.get("cached_tokens") or 0) / u["input_tokens"]
        if hit < self.floor:
            self.warned = True
            print(f"\n  !! CACHE MISS on call {self.n}: only {hit:.0%} of input read from "
                  f"cache.\n     Every later call pays full input rate. Check the prefix is "
                  f">= 1024 tokens,\n     the breakpoint placement, prompt_cache_key, and "
                  f"that tools did not change.\n     Ctrl-C now if the bill matters.\n",
                  file=sys.stderr)


# -------------------------------------------------------------- run tree + state

SCRIPT_DIR = Path(__file__).resolve().parent


def resolve(p: str | Path) -> Path:
    """Relative paths are relative to the scripts directory, not to the shell's cwd.
    The repo's conventional paths all start ../, and a run launched from the repo root
    should not silently write its outputs somewhere else."""
    p = Path(p)
    return p if p.is_absolute() else (SCRIPT_DIR / p).resolve()


# ------------------------------------------------------------- evaluation sets

# Two review sets, two output trees, one switch. The separation is not cosmetic:
# master_flow's standing rule is that nothing which touched prompt tuning or
# provider selection may appear in a reported evaluation, and the surest way to
# honour that is for the two to never share a directory.
#
#   tuning      the 50. Burned. Drove prompt and provider choice, so every number
#               on it is a max-over-configs statistic and is never reported.
#   validation  the 75. The reporting set, scored once against adjudicated gold.
#   prompt-eval the 30 of those 75 that prompt v3 does NOT contain. Once a prompt
#               quotes gold reviews as worked examples it cannot be scored on them,
#               so this is the only clean arm for v3. Small and thin -- 13 of the 29
#               labels have no support -- hence meso_macro: False.
#
# `gold` is a candidate list: the first file that exists wins. Validation prefers
# the adjudicated panel gold and falls back to the author's single-coder labels so
# the plumbing is usable before the adjudication meeting -- resolve_gold() says so
# loudly when that happens.
EVAL_SETS = {
    "tuning": {
        "n": 50,
        "blurb": "selection only. Burned: these numbers drove prompt and provider\n"
                 "choice and never appear in the paper.",
        "reviews": "../tuning/tuning_set_50_blind.jsonl",
        "gold":    ["../tuning/tuning_set_50.jsonl"],
        "runs":    "../outputs/runs",
        "stats":   "../outputs/run-stats",
        "compare": "../outputs/comparison",
    },
    "validation": {
        "n": 75,
        "blurb": "the reporting set. Scored once, against the adjudicated gold.",
        "reviews": "../validation/validation_set_blind.jsonl",
        "gold":    ["../validation/gold_set.jsonl",
                    "../validation/validation_set.jsonl"],
        "runs":    "../outputs/validation/runs",
        "stats":   "../outputs/validation/run-stats",
        "compare": "../outputs/validation/comparison",
    },
    "prompt-eval": {
        "n": 30,
        "blurb": "the 30 gold reviews prompt v3 does NOT quote. The only arm a\n"
                 "prompt built from gold examples can honestly be scored on.\n"
                 "Thin: 13 of 29 labels have no support -- micro and example-F1\n"
                 "only, meso macro-F1 is suppressed. See prompt_eval_report.md.",
        "reviews": "../prompt_eval/prompt_eval_set_blind.jsonl",
        "gold":    ["../prompt_eval/gold_set.jsonl"],
        "runs":    "../outputs/prompt-eval/runs",
        "stats":   "../outputs/prompt-eval/run-stats",
        "compare": "../outputs/prompt-eval/comparison",
        # Averaging F1 over the 5 labels that clear the support floor produces a number
        # that reads as comparable to the validation figure over 19. It is not.
        "meso_macro": False,
    },
}
DEFAULT_EVAL_SET = "tuning"


def _count_lines(p: Path) -> int | None:
    try:
        with open(p, encoding="utf-8") as fh:
            return sum(1 for line in fh if line.strip())
    except OSError:
        return None


def resolve_eval_set(explicit: str | None = None, *, what: str = "label") -> str:
    """Which review set this invocation is about.

    An explicit --eval-set always wins. Otherwise ask, when there is a human to
    ask; a non-interactive caller keeps the historical default so existing
    scripts and cron jobs do not silently change which set they touch."""
    if explicit:
        if explicit not in EVAL_SETS:
            sys.exit(f"unknown --eval-set {explicit!r}; choose from {', '.join(EVAL_SETS)}")
        return explicit
    if not sys.stdin.isatty():
        print(f"--eval-set not given and no tty; defaulting to {DEFAULT_EVAL_SET}",
              file=sys.stderr)
        return DEFAULT_EVAL_SET

    names = list(EVAL_SETS)
    print(f"\nWhich review set to {what}?\n")
    for i, name in enumerate(names, 1):
        s = EVAL_SETS[name]
        n = _count_lines(resolve(s["reviews"]))
        have = f"{n} reviews" if n is not None else "FILE NOT FOUND"
        print(f"  {i}) {name:<11} {have:<18} {s['reviews']}")
        print(f"     {'':<11} {'-> ' + s['runs']}")
        for line in s["blurb"].split("\n"):
            print(f"     {'':<11} {line}")
        print()
    while True:
        try:
            raw = input(f"set [1-{len(names)}, or a name]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            sys.exit("\naborted")
        if raw in EVAL_SETS:
            return raw
        if raw.isdigit() and 1 <= int(raw) <= len(names):
            return names[int(raw) - 1]
        print(f"  pick 1-{len(names)} or one of: {', '.join(names)}")


def resolve_gold(eval_set: str, explicit: str | None = None) -> Path:
    """The gold file for a set: an explicit --gold, else the first candidate that
    exists. Falling back to the author's single-coder labels on the validation set
    is legitimate for a smoke test and illegitimate as a reported number, so it is
    never silent."""
    if explicit:
        return resolve(explicit)
    cands = EVAL_SETS[eval_set]["gold"]
    for i, c in enumerate(cands):
        p = resolve(c)
        if p.exists():
            if i > 0:
                print(f"\n  !! {Path(cands[0]).name} not found -- scoring against "
                      f"{p.name} instead.\n"
                      f"     Those are the author's single-coder labels, not the "
                      f"adjudicated panel gold.\n"
                      f"     Usable as a smoke test. Not reportable as agreement.\n",
                      file=sys.stderr)
            return p
    sys.exit(f"no gold file for '{eval_set}'; looked for: "
             + ", ".join(cands))


def show(p: Path) -> str:
    """Paths in the log are for copy-pasting into the next command, so prefer a short
    relative one -- but a chain of ../.. climbing out of the repo is worse than absolute."""
    try:
        rel = os.path.relpath(p, Path.cwd())
    except ValueError:
        return str(p)
    return str(p) if rel.startswith("../..") else rel


def prompt_stem(prompt_file: str | Path) -> str:
    """teacher_v2_bare.txt -> teacher_v2_bare. The prompt is a run axis, so it names
    a directory; the ablation modes then sit side by side under one model/effort."""
    return Path(prompt_file).name.rsplit(".txt", 1)[0]


class RunPaths:
    """outputs/runs/<model>/<effort>/<prompt_stem>/ and the files inside it.

    Filenames keep the <tag>_ prefix even though the directory already says it: the
    files get copied around and attached to things, and a bare responses.jsonl on its
    own tells you nothing about which run produced it."""

    def __init__(self, root: str | Path, model: str, effort: str, prompt_file: str | Path):
        self.stem = prompt_stem(prompt_file)
        self.effort = effort or "none"
        self.dir = Path(root) / model / self.effort / self.stem
        self.tag = f"{model}_{self.effort}_{self.stem}"
        self.responses = self.dir / f"{self.tag}_responses.jsonl"
        self.meta = self.dir / f"{self.tag}_meta.jsonl"
        self.summary = self.dir / f"{self.tag}_summary.json"
        self.checkpoint = self.dir / "checkpoint.json"

    def exists(self) -> bool:
        return self.responses.exists()

    def wipe(self) -> None:
        for p in (self.responses, self.meta, self.summary, self.checkpoint):
            p.unlink(missing_ok=True)

    def mkdir(self) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)


def discover_runs(root: Path) -> list[Path]:
    """Every run directory under outputs/runs, newest first. The tree is
    <model>/<effort>/<prompt_stem>/, so a sweep leaves several and both the scorer (score
    all of them) and the comparison (list what exists) need to enumerate them."""
    if not root.exists():
        return []
    dirs = {p.parent for p in root.rglob("*_responses.jsonl")}
    return sorted(dirs, key=lambda d: max(f.stat().st_mtime
                                          for f in d.glob("*_responses.jsonl")),
                  reverse=True)


def run_tags(run_dir: Path) -> list[str]:
    """Every run tag present in a directory, oldest first."""
    return [f.name.replace("_responses.jsonl", "")
            for f in sorted(run_dir.glob("*_responses.jsonl"),
                            key=lambda f: f.stat().st_mtime)]


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue                     # a half-written last line from a hard kill
    return out


def load_progress(paths: RunPaths, id_key: str = "review_id") -> tuple[set[str], dict]:
    """What a resumed run has already paid for.

    The done-set is derived from responses.jsonl rather than from the checkpoint,
    because that file IS the deliverable: if a line is in it, the work exists on disk,
    and the two can never drift. checkpoint.json only carries the running aggregates
    a resumed run needs in order to report a correct total at the end.

    A row that errored or failed to parse is NOT done -- it gets retried next pass."""
    done = set()
    for rec in read_jsonl(paths.responses):
        if rec.get(id_key) and not rec.get("error_type"):
            done.add(rec[id_key])
    counters = {}
    if paths.checkpoint.exists():
        try:
            counters = json.loads(paths.checkpoint.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            counters = {}
    return done, counters


def select_reviews(reviews_file: Path, only: set[str], limit: int) -> list[dict]:
    rows = read_jsonl(reviews_file)
    if not rows:
        sys.exit(f"no reviews in {reviews_file}")
    if only:
        rows = [r for r in rows if r.get("review_id") in only]
        missing = only - {r.get("review_id") for r in rows}
        if missing:
            sys.exit(f"--only ids not in {show(reviews_file)}: {sorted(missing)}")
    if limit:
        rows = rows[:limit]
    return rows


def payload_for(row: dict) -> str:
    """What the model sees of a review. Deliberately just these two fields: the gold
    labels live in the same source file for some sets, and they must not leak."""
    return json.dumps({"game_name": row.get("game_name", ""),
                       "review_text": row.get("review_text", "")}, ensure_ascii=False)


COUNTER_KEYS = ("ok", "parsed", "truncated", "searched", "contract_bad",
                "api_errors", "parse_failures", "retried", "extra_attempts",
                "superseded", "refusals")


def supersede(paths: RunPaths, retry_ids: set[str]) -> int:
    """A resumed run re-labels every review that failed last pass. The old rows stay on
    disk -- a paid-for failure is evidence, and the paper wants it -- but they are
    flagged so the scorer skips them. Without the flag one review contributes two rows
    and its failure is counted twice."""
    if not retry_ids:
        return 0
    n = 0
    for path in (paths.responses, paths.meta):
        rows = read_jsonl(path)
        if not rows:
            continue
        with open(path, "w", encoding="utf-8") as f:
            for r in rows:
                if r.get("review_id") in retry_ids and not r.get("superseded"):
                    r["superseded"] = True
                    n += path == paths.responses
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return n


def prior_state(paths: RunPaths) -> tuple[dict, float, list[dict]]:
    """Rebuild the running totals from meta.jsonl rather than from the checkpoint.

    meta.jsonl is the file that records what was actually billed; if a run dies between
    writing a row and writing the checkpoint, the derived totals are still right. The
    checkpoint only has to carry the run's identity and whether it finished.

    Superseded rows keep their cost in `spend` -- that money was spent -- but stay out
    of the usage rows, so mean-tokens-per-review describes the reviews that survived."""
    counters = dict.fromkeys(COUNTER_KEYS, 0)
    spend, usage = 0.0, []
    for m in read_jsonl(paths.meta):
        spend += (m.get("cost_usd") or {}).get("total", 0.0)
        n_att = m.get("n_attempts", 1)
        counters["extra_attempts"] += max(n_att - 1, 0)
        counters["retried"] += n_att > 1
        if m.get("superseded"):
            counters["superseded"] += 1
            continue
        if m.get("usage"):
            usage.append(m["usage"])
        if m.get("error_type"):
            counters["api_errors"] += 1
        elif m.get("parse_failed"):
            counters["parse_failures"] += 1
        else:
            counters["ok"] += 1
            counters["parsed"] += 1
            counters["truncated"] += m.get("status") in ("incomplete", "length")
            counters["searched"] += bool(m.get("n_web_searches"))
            counters["refusals"] += m.get("status") == "refusal"
            c = m.get("contract") or {}
            counters["contract_bad"] += any(
                c.get(k) for k in ("bad_codes", "dup_codes", "missing_span", "span_bad"))
    return counters, spend, usage


def resume_gate(paths: RunPaths, prompt_sha: str, resume: bool, overwrite: bool) -> set[str]:
    """Decide what a re-invocation does with the output already sitting in the run
    directory, and return the set of review_ids that do not need doing again.

    Default is overwrite: a run is named by its configuration, so re-running one means
    replacing it. The exception is a run that was interrupted -- its checkpoint says
    complete=false, and silently wiping that throws away calls that were already paid
    for -- so that one case stops and makes you choose."""
    done, state = load_progress(paths)
    incomplete = paths.exists() and not state.get("complete", False)

    if resume:
        n_rows = len(read_jsonl(paths.responses))
        if not n_rows:
            print("--resume: nothing on disk yet, starting fresh.")
            return set()
        if not done:
            print(f"--resume: {n_rows} row(s) on disk, none of them usable "
                  f"-- retrying all of them.")
        if state.get("prompt_sha256") and state["prompt_sha256"] != prompt_sha:
            sys.exit(
                f"refusing to resume: the prompt changed since this run started.\n"
                f"  checkpoint: {state['prompt_sha256'][:12]}\n"
                f"  now:        {prompt_sha[:12]}\n"
                f"  half the rows would be labelled by a different prompt. Rerun with "
                f"--overwrite to start clean.")
        return done

    if incomplete and not overwrite:
        sys.exit(
            f"an interrupted run is sitting in {show(paths.dir)}\n"
            f"  {len(done)} review(s) already labelled and paid for.\n"
            f"  --resume     finish it\n"
            f"  --overwrite  discard it and start again")

    if paths.exists():
        print(f"overwriting the completed run in {show(paths.dir)}")
    paths.wipe()
    return set()


def summarize(paths: RunPaths, counters: dict, spend: float, all_usage: list[dict],
              pricing: dict, project_to: int, extra: dict) -> dict:
    """Print the end-of-run scoreboard and write <tag>_summary.json."""
    n = max(len(all_usage), 1)
    tot = {k: sum(x.get(k, 0) or 0 for x in all_usage) for k in
           ("input_tokens", "cached_tokens", "cache_write_tokens",
            "uncached_input_tokens", "output_tokens", "reasoning_tokens")}
    per = spend / n
    n_done = counters["parsed"] + counters["parse_failures"] + counters["api_errors"]

    print(f"\ndone. ok {counters['ok']}/{n_done}  parsed {counters['parsed']}/{n_done}  "
          f"truncated {counters['truncated']}  searched {counters['searched']}")
    print(f"  api errors      {counters['api_errors']}   "
          f"parse failures {counters['parse_failures']}   "
          f"contract issues {counters['contract_bad']}")
    if counters["extra_attempts"]:
        print(f"  re-attempts     {counters['extra_attempts']} extra call(s) on "
              f"{counters['retried']} review(s), billed into the totals below")
    if counters["superseded"]:
        print(f"  superseded      {counters['superseded']} row(s) from an earlier pass: "
              f"kept on disk and still on the bill, excluded from scoring")
    if all_usage:
        print(f"  cache hit rate  {tot['cached_tokens']/max(tot['input_tokens'],1):.3f}")
        print(f"  mean output     {tot['output_tokens']/n:.0f} tokens "
              f"(reasoning {tot['reasoning_tokens']/n:.0f}, "
              f"{100*tot['reasoning_tokens']/max(tot['output_tokens'],1):.0f}% of output)")
        print(f"  spend           ${spend:.4f}   ${per:.6f}/review")
        print(f"  projected {project_to:,}: ${per*project_to:,.0f} "
              f"(rates as of {pricing['as_of']})")

    summary = {
        "tag": paths.tag, "n": len(all_usage), "prompt_stem": paths.stem,
        "finished": datetime.now().isoformat(timespec="seconds"),
        **extra, "pricing": pricing, **counters,
        "cache_hit_rate": round(tot["cached_tokens"]/max(tot["input_tokens"], 1), 4),
        "mean_output_tokens": round(tot["output_tokens"]/n, 1),
        "mean_reasoning_tokens": round(tot["reasoning_tokens"]/n, 1),
        "spend_usd": round(spend, 6), "usd_per_review": round(per, 8),
        f"projected_usd_at_{project_to}": round(per*project_to, 2),
    }
    paths.summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def write_checkpoint(paths: RunPaths, state: dict) -> None:
    state = dict(state)
    state["updated"] = datetime.now().isoformat(timespec="seconds")
    tmp = paths.checkpoint.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    tmp.replace(paths.checkpoint)        # atomic: a kill mid-write leaves the old one


# --------------------------------------------------------------------- manifest

def git_commit(repo_dir: Path) -> str | None:
    try:
        out = subprocess.run(["git", "-C", str(repo_dir), "rev-parse", "HEAD"],
                             capture_output=True, text=True, timeout=5)
        return out.stdout.strip() or None if out.returncode == 0 else None
    except Exception:
        return None


def git_dirty(repo_dir: Path) -> bool | None:
    try:
        out = subprocess.run(["git", "-C", str(repo_dir), "status", "--porcelain"],
                             capture_output=True, text=True, timeout=10)
        return bool(out.stdout.strip()) if out.returncode == 0 else None
    except Exception:
        return None


def prompt_manifest(prompt_file: str | Path) -> dict:
    """build_prompt.py writes <prompt>.manifest.json beside every prompt it renders.
    It carries the codebook version and the ablation flags -- exactly what a run needs
    to record about the prompt it used, already computed."""
    p = Path(str(prompt_file) + ".manifest.json")
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


SDK_MODULES = ("openai", "anthropic", "requests", "httpx2", "tavily")


def lib_versions(modules=SDK_MODULES) -> dict:
    """Versions of every SDK a runner might have used. importlib.metadata reads the
    installed distribution's metadata rather than importing the package, so recording
    the anthropic version costs a Kimi run nothing and a missing SDK is None, not a
    crash."""
    import importlib.metadata as md
    out = {}
    for name in modules:
        try:
            out[name] = md.version(name)
        except Exception:
            out[name] = None
    return out


def run_manifest(prompt_file: str | Path, script_file: str | Path) -> dict:
    """Everything needed to reconstruct this run months later, when the working tree
    has moved on and the paper is asking which codebook produced which number."""
    repo = Path(script_file).resolve().parent
    libs = lib_versions()
    return {
        "argv": sys.argv,
        "script": Path(script_file).name,
        "python": sys.version.split()[0],
        "libs": libs,
        "openai_lib": libs.get("openai"),     # kept: earlier summaries carry this key
        "git_commit": git_commit(repo),
        "git_dirty": git_dirty(repo),
        "prompt_manifest": prompt_manifest(prompt_file),
    }
