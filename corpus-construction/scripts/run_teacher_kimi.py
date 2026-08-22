#!/usr/bin/env python3
"""
run_teacher_kimi.py -- run a teacher prompt over the tuning 50 on Kimi K3.

    python run_teacher_kimi.py --check                   offline: config, prompt, paths
    python run_teacher_kimi.py --dry                     one live call + a caching probe
    python run_teacher_kimi.py --actual                  labels the 50
    python run_teacher_kimi.py --actual --resume         picks up where a killed run stopped

Needs:  pip install openai requests   (Moonshot's chat surface is OpenAI-compatible;
                                        the Formula API used below for k3 web search is
                                        a separate plain-REST surface, hence requests)

Same command-line surface, same output tree, same resume semantics as
run_teacher_openai.py -- the shared half of both runners lives in runner_common.py, so a
prompt ablation is driven the same way whichever provider is under test:

    python run_teacher_kimi.py --actual --prompt ../outputs/prompts/teacher_v2_bare.txt

Sequential within a run, same as the OpenAI runner: Moonshot's automatic prefix caching
rewards a stable prefix sent repeatedly, so cold parallel workers would all miss.

Four ways Kimi differs from OpenAI. Each is marked KIMI DIFF below.
  1. Web search is a CLIENT-SIDE TOOL LOOP -- and on kimi-k3 specifically it goes through
     the FORMULA API (moonshot/web-search:latest), not the older $web_search builtin.
     $web_search's round-2 echo (send the model's own generated arguments back verbatim)
     currently returns 400 "tokenization failed" on every attempt on k3 -- confirmed
     against Moonshot's own k3 bug tracker (reported 2026-07-23, still open at last
     check); it works fine on k2.6, which is why it's easy to miss if you tested there
     first. The Formula channel instead: (a) fetches the real "web_search" function
     declaration from GET /formulas/{uri}/tools once per run, (b) on a tool_calls
     response, actually EXECUTES the search yourself via POST /formulas/{uri}/fibers
     using the model's generated arguments, and (c) feeds the real fiber output back as
     the tool message content. That's three network calls for a searched review
     (chat -> fiber -> chat) instead of two, and the fiber call is billed separately
     from the search's trigger fee -- see the PRICING note in runner_common.py.
  2. reasoning_effort is low | high | max, default max. There is no "medium", so this is
     not directly comparable to the Luna sweep. Defaulted to "high".
  3. Caching is automatic prefix caching -- no breakpoint to set, no write charge.
     Stable prefix first, per-review text last, which the prompt already does.
  4. K3 always reasons; thinking cannot be turned off, only turned down. Multi-turn tool
     loops on k3 need the assistant's reasoning_content preserved across rounds, not
     just role/content/tool_calls -- run_review() echoes the full message dump (not a
     filtered subset) for that reason; see the comment at the echo line below.

Output tree, one directory per (model, effort, prompt):

    ../outputs/runs/<model>/<effort>/<prompt_stem>/
        <tag>_responses.jsonl   raw text + parsed JSON (+ every re-attempt)
        <tag>_meta.jsonl        usage, cost, latency, status, contract errors
        <tag>_summary.json      scoreboard row + run manifest
        checkpoint.json         progress, for --resume
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import requests
from openai import OpenAI

sys.path.insert(0, str(Path(__file__).parent))
import runner_common as rc
from build_prompt import load_prompt

SCRIPT_DIR = Path(__file__).resolve().parent
resolve, show, payload_for = rc.resolve, rc.show, rc.payload_for

# ============================== DEFAULTS ==============================
DEFAULT_MODEL   = "kimi-k3"
DEFAULT_EFFORT  = "high"            # low | high | max   (KIMI DIFF 2; no "medium")
DEFAULT_PROMPT  = "../outputs/prompts/teacher_v2_full.txt"
DEFAULT_REVIEWS = "../tuning/tuning_set_50_blind.jsonl"   # blind: no gold in this process
OUT_ROOT        = "../outputs/runs"
BASE_URL        = "https://api.moonshot.ai/v1"

MAX_OUTPUT      = 8192      # reasoning counts against this; too low = truncated JSON
MAX_OUTPUT_CAP  = 32768     # ceiling for the truncation bump
TRUNCATION_BUMP = 2.0

RETRIES         = 3         # transport-level attempts per call
PARSE_RETRIES   = 2         # extra attempts when the response is not parseable JSON
SEND_TEMPERATURE = False    # K3 is a reasoning model; leave off unless you decide
TEMPERATURE     = 0.0
PROJECT_TO      = 200_000
RNG_SEED        = 20260822  # only seeds retry jitter; no effect on model sampling

# KIMI DIFF 1: your frozen policy is one search per review. The loop enforces it: after
# MAX_TOOL_ROUNDS the next call goes out with tool_choice="none" so the model must answer.
MAX_TOOL_ROUNDS = 1

# KIMI DIFF 1 (k3 path): the web-search tool for k3 lives behind the Formula API, not
# the $web_search builtin -- see the module docstring. The declaration is static, so
# it's fetched once per run (get_web_search_tools) and reused for every call in the loop.
FORMULA_URI     = "moonshot/web-search:latest"

API_KEY_ENV     = "MOONSHOT_API_KEY"
ENV_FILE        = ".env"           # optional: KEY=value lines, gitignored
# ======================================================================


# ------------------------------------------------------------------ run config

@dataclass
class RunConfig:
    """One run, fully resolved. See the note in run_teacher_openai.py: the axes come
    from argparse, so they travel in an object rather than in module globals."""
    model: str
    effort: str
    prompt_file: Path
    reviews_file: Path
    out_root: Path
    web_search: bool
    max_output: int
    parse_retries: int
    retries: int
    max_tool_rounds: int
    limit: int
    only: set[str]
    max_spend: float
    prompt: str = ""
    prompt_sha: str = ""
    legal_codes: set[str] = field(default_factory=set)
    pricing: dict = field(default_factory=dict)
    paths: rc.RunPaths | None = None


def build_config(a: argparse.Namespace) -> RunConfig:
    cfg = RunConfig(
        model=a.model, effort=a.effort,
        prompt_file=resolve(a.prompt), reviews_file=resolve(a.reviews),
        out_root=resolve(a.out_root), web_search=not a.no_web_search,
        max_output=a.max_output, parse_retries=a.parse_retries, retries=a.retries,
        max_tool_rounds=a.max_tool_rounds, limit=a.limit,
        only={s.strip() for s in a.only.split(",") if s.strip()} if a.only else set(),
        max_spend=a.max_spend,
    )
    if not cfg.prompt_file.exists():
        sys.exit(f"prompt not found: {cfg.prompt_file}\n"
                 f"  build one:  python build_prompt.py")
    cfg.prompt = load_prompt(cfg.prompt_file)
    cfg.prompt_sha = hashlib.sha256(cfg.prompt.encode()).hexdigest()
    cfg.legal_codes = rc.legal_codes_from_prompt(cfg.prompt)
    cfg.pricing = rc.pricing_for(cfg.model)
    cfg.paths = rc.RunPaths(cfg.out_root, cfg.model, cfg.effort, cfg.prompt_file)
    return cfg


def get_client() -> tuple["OpenAI", str]:
    """Returns (client, key) -- the raw key is also needed for the Formula API's plain
    HTTP endpoints below, which sit outside the openai SDK's chat-completions surface."""
    key = rc.load_api_key(API_KEY_ENV, SCRIPT_DIR, ENV_FILE)
    return OpenAI(api_key=key, base_url=BASE_URL), key


# ------------------------------------------------------------------ formula api

def formula_call(key: str, method: str, path: str, body: dict | None,
                 retries: int, rng: random.Random) -> dict:
    """Raw HTTP call to a Formula API endpoint (GET .../tools, POST .../fibers). These
    are separate REST endpoints alongside /chat/completions, not part of the OpenAI-
    compatible chat surface, so the openai SDK client doesn't reach them -- plain
    requests, same bearer auth as everything else."""
    url = BASE_URL + path

    def once():
        resp = requests.request(method, url, headers={"Authorization": f"Bearer {key}"},
                                json=body, timeout=30)
        resp.raise_for_status()
        return resp.json()

    data, _, etype, emsg = rc.call_with_retries(once, retries, rng, label="formula")
    if etype:
        raise RuntimeError(f"formula {method} {path} failed: {etype}: {emsg}")
    return data


def get_web_search_tools(key: str, retries: int, rng: random.Random) -> list:
    """Fetch the 'web_search' function declaration for the Formula channel. Static per
    run -- callers fetch this once and pass it into every run_review() call."""
    return formula_call(key, "GET", f"/formulas/{FORMULA_URI}/tools", None, retries, rng)["tools"]


def run_formula_search(key: str, tool_call, retries: int, rng: random.Random) -> str:
    """Execute one web_search tool call server-side via the Formula API and return the
    real result content as a string, ready to drop straight into a role=tool message.
    This is the step the old $web_search builtin used to do for you automatically on
    the round-2 /chat/completions call; on k3 that automatic path 400s, so you run it
    yourself here (this call is where the fiber-execution fee is billed)."""
    fiber = formula_call(key, "POST", f"/formulas/{FORMULA_URI}/fibers",
                         {"name": tool_call.function.name,
                          "arguments": tool_call.function.arguments}, retries, rng)
    ctx = fiber.get("context", {})
    return ctx.get("output") or ctx.get("encrypted_output") or ""


# --------------------------------------------------------------------- the call

def build_kwargs(cfg: RunConfig, messages: list, use_tools: bool,
                 tools_list: list | None, max_output: int) -> dict:
    kw = {
        "model": cfg.model,
        "messages": messages,
        "max_tokens": max_output,          # chat-completions name, not max_output_tokens
    }
    if cfg.effort:
        kw["reasoning_effort"] = cfg.effort         # top-level on K3, not nested
    if cfg.web_search and tools_list:
        kw["tools"] = tools_list                    # resent on every call in the loop
        if not use_tools:
            kw["tool_choice"] = "none"              # forces a final answer at the cap
    if SEND_TEMPERATURE:
        kw["temperature"] = TEMPERATURE
    return kw


def usage_of(resp) -> dict:
    """One API call's usage. Field names match the OpenAI runner so the shared cost
    maths and compute_run_stats.py need no special-casing. Moonshot has moved
    cached_tokens around between versions, so probe both the flat field and
    prompt_tokens_details."""
    u = resp.usage
    cached = getattr(u, "cached_tokens", None)
    if cached is None:
        d = getattr(u, "prompt_tokens_details", None)
        cached = getattr(d, "cached_tokens", 0) if d else 0
    cached = cached or 0
    reasoning = 0
    cd = getattr(u, "completion_tokens_details", None)
    if cd:
        reasoning = getattr(cd, "reasoning_tokens", 0) or 0
    return {
        "input_tokens": u.prompt_tokens,
        "cached_tokens": cached,
        "cache_write_tokens": 0,                       # no such charge here
        "uncached_input_tokens": u.prompt_tokens - cached,
        "output_tokens": u.completion_tokens,
        "reasoning_tokens": reasoning,
        "total_tokens": getattr(u, "total_tokens", None),
    }


def one_call(client, cfg: RunConfig, messages: list, use_tools: bool,
             tools_list: list | None, max_output: int, rng: random.Random):
    """A single API call with retries. Returns (response, latency, etype, emsg)."""
    return rc.call_with_retries(
        lambda: client.chat.completions.create(
            **build_kwargs(cfg, messages, use_tools, tools_list, max_output)),
        cfg.retries, rng)


def run_review(client, key: str, cfg: RunConfig, tools_list: list | None,
               system_prompt: str, user_input: str, max_output: int,
               rng: random.Random):
    """KIMI DIFF 1 (k3 path): the whole tool loop for ONE review, via the Formula API.

    Returns (text, usage, latency, n_calls, searches, finish_reason, etype, emsg).
    `searches` holds the query and result length, which is where your
    invoked_web_search / search_query audit fields come from. `usage`/`latency` cover
    only the /chat/completions calls; the fiber execution call is separate and billed
    separately (see run_formula_search / PRICING["search_per_call"]).
    """
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}]
    usage: dict = {}
    searches: list = []
    total_latency = 0.0
    n_calls = 0
    rounds = 0

    while True:
        at_cap = rounds >= cfg.max_tool_rounds
        resp, lat, etype, emsg = one_call(client, cfg, messages, not at_cap,
                                          tools_list, max_output, rng)
        total_latency += lat
        n_calls += 1
        if etype:
            return None, usage, total_latency, n_calls, searches, None, etype, emsg

        usage = rc.add_usage(usage, usage_of(resp))
        choice = resp.choices[0]

        if choice.finish_reason != "tool_calls":
            return (choice.message.content, usage, total_latency, n_calls,
                    searches, choice.finish_reason, None, None)

        # Echo the assistant message back verbatim, unfiltered. K3 requires its own
        # reasoning_content to be replayed across tool rounds (unlike the trimmed
        # role/content/tool_calls-only example in Moonshot's docs, which is not enough
        # for k3's always-on reasoning) -- model_dump keeps everything the SDK parsed.
        messages.append(choice.message.model_dump(exclude_none=True))
        for tc in choice.message.tool_calls or []:
            if tc.function.name == "web_search":
                args = json.loads(tc.function.arguments)
                content = run_formula_search(key, tc, cfg.retries, rng)
                searches.append({"query": args.get("query"),
                                 "result_chars": len(content),
                                 "raw_arguments": args})
            else:
                content = f"Error: unable to find tool by name '{tc.function.name}'"
            messages.append({"role": "tool", "tool_call_id": tc.id,
                             "name": tc.function.name, "content": content})
        rounds += 1


def label_review(client, key: str, cfg: RunConfig, tools_list: list | None,
                 row: dict, rng: random.Random, watch: rc.CacheWatch) -> dict:
    """Label one review, re-attempting while the response will not parse as JSON.

    Two distinct failure modes hide behind "unparseable", and they need different
    answers. A response that got cut off mid-object (finish_reason="length") will be cut
    off again at the same budget no matter how many times it is resampled -- that one
    gets a bigger max_tokens. A response that merely wrapped the object in prose is a
    sampling accident, and an identical resample usually clears it.

    Every attempt is kept, and every attempt's usage is summed into the returned total:
    a re-attempt costs real money, and a per-review cost that ignores it understates the
    projection at 200k."""
    review_text = row.get("review_text", "")
    payload = payload_for(row)
    attempts: list[dict] = []
    usage_total: dict = {}
    latency_total = 0.0
    n_calls = n_searches = 0
    max_out = cfg.max_output
    fin = None

    for k in range(cfg.parse_retries + 1):
        text, u, lat, calls, searches, fin, etype, emsg = run_review(
            client, key, cfg, tools_list, cfg.prompt, payload, max_out, rng)
        latency_total += lat
        n_calls += calls
        if etype:
            return {"api_error_type": etype, "api_error_message": emsg,
                    "attempts": attempts, "usage": rc.add_usage(usage_total, u) if u else usage_total,
                    "latency_s": latency_total, "n_calls": n_calls,
                    "n_searches": n_searches, "searches": [], "finish_reason": None,
                    "parsed": None, "raw": None, "parse_note": None, "contract": None}

        usage_total = rc.add_usage(usage_total, u)
        watch.observe(u)
        n_searches += len(searches)
        parsed, note = rc.parse_json(text)
        attempts.append({"n": k + 1, "max_output": max_out, "status": fin,
                         "parse_note": note, "latency_s": round(lat, 2),
                         "n_api_calls": calls, "usage": u, "raw": text,
                         "search_queries": [s["query"] for s in searches]})

        if parsed is not None:
            return {"api_error_type": None, "api_error_message": None,
                    "attempts": attempts, "usage": usage_total,
                    "latency_s": latency_total, "n_calls": n_calls,
                    "n_searches": n_searches, "searches": searches,
                    "finish_reason": fin, "parsed": parsed, "raw": text,
                    "parse_note": note,
                    "contract": rc.check_contract(parsed, review_text, cfg.legal_codes)}

        if k < cfg.parse_retries:
            if fin == "length" and max_out < MAX_OUTPUT_CAP:
                bumped = min(int(max_out * TRUNCATION_BUMP), MAX_OUTPUT_CAP)
                print(f"       truncated at max_tokens={max_out:,} -> retrying at {bumped:,}")
                max_out = bumped
            else:
                print(f"       unparseable JSON -> resample {k + 2}/{cfg.parse_retries + 1}")

    # Out of attempts. This is NOT an api error: the calls succeeded and were billed,
    # the model just would not emit JSON.
    return {"api_error_type": None, "api_error_message": None, "attempts": attempts,
            "usage": usage_total, "latency_s": latency_total, "n_calls": n_calls,
            "n_searches": n_searches, "searches": [], "finish_reason": fin,
            "parsed": None, "raw": attempts[-1]["raw"], "parse_note": "parse_failed",
            "contract": None}


# ---------------------------------------------------------------------- preflight

def preflight(cfg: RunConfig, rows: list[dict], done: set[str]) -> None:
    man = rc.prompt_manifest(cfg.prompt_file)
    p = cfg.pricing
    print("=" * 72)
    print(f"model          {cfg.model}   effort={cfg.effort or 'none'}   "
          f"web_search={cfg.web_search}   max_tool_rounds={cfg.max_tool_rounds}")
    print(f"pricing        in ${p['input']} / cached ${p['cached_input']} / "
          f"out ${p['output']} per MTok + ${p.get('search_per_call', 0)}/search"
          f"   (as of {p['as_of']})")
    print(f"prompt         {show(cfg.prompt_file)}")
    print(f"               {len(cfg.prompt):,} chars, ~{len(cfg.prompt)//4:,} tokens, "
          f"sha {cfg.prompt_sha[:12]}")
    if man:
        print(f"               mode={man.get('mode')}  codebook={man.get('codebook_version')}"
              f"  n_labels={man.get('n_labels')}")
    print(f"legal codes    {len(cfg.legal_codes)} parsed from the prompt's output spec"
          + ("   !! NONE FOUND - contract checks disabled" if not cfg.legal_codes else ""))
    print(f"reviews        {show(cfg.reviews_file)}  ({len(rows)} selected"
          + (f", {len(done)} already done" if done else "") + ")")
    print(f"cache          automatic prefix caching (KIMI DIFF 3: no breakpoint, no write fee)")
    print(f"search channel {'formula:' + FORMULA_URI if cfg.web_search else 'off'}")
    print(f"budget         max_tokens={cfg.max_output:,} (bump to {MAX_OUTPUT_CAP:,} on "
          f"truncation)  parse_retries={cfg.parse_retries}")
    if cfg.max_spend:
        print(f"spend guard    stop above ${cfg.max_spend:g}")
    print(f"output         {show(cfg.paths.dir)}/")
    print("=" * 72)


# --------------------------------------------------------------- dry run

def dry_run(cfg: RunConfig) -> None:
    rng = random.Random(RNG_SEED)
    client, key = get_client()
    rows = rc.select_reviews(cfg.reviews_file, cfg.only, cfg.limit)
    preflight(cfg, rows, set())

    tools_list = None
    if cfg.web_search:
        print(f"\nfetching web-search tool declaration from formula {FORMULA_URI}...")
        tools_list = get_web_search_tools(key, cfg.retries, rng)
        print(f"  got {len(tools_list)} tool(s): "
              f"{[t['function']['name'] for t in tools_list]}")

    # --- stage 1: does the API work, and does the tool loop actually complete? ---
    print("\n[1/2] throwaway call with search (short prompt, below the cache floor)...")
    probe_cfg = RunConfig(**{**cfg.__dict__,
                             "prompt": "You are a helpful assistant. Answer in one sentence."})
    text, u, lat, n_calls, searches, fin, etype, emsg = run_review(
        client, key, probe_cfg, tools_list, probe_cfg.prompt,
        "Search for today's weather in Guwahati, India.", cfg.max_output, rng)
    if etype:
        print(f"\nFAILED: {etype}: {emsg}\nFix the arguments and rerun --dry.")
        sys.exit(1)
    print(f"  api calls    {n_calls}  (2 means the search loop ran)")
    print(f"  finish       {fin}")
    print(f"  text         {text!r}")
    print(f"  searches     {[s['query'] for s in searches] or 'none'}")
    if searches and searches[0]["result_chars"]:
        print(f"  search result {searches[0]['result_chars']:,} chars fetched via the fiber call")
    rc.print_stats("  stage1", u, lat, show_write=False)

    # --- stage 2: does the real prompt cache? two identical-prefix calls. ---
    print("\n[2/2] automatic caching check: two calls with the real prompt...")
    for n in (1, 2):
        text2, u2, lat2, nc2, s2, fin2, etype2, emsg2 = run_review(
            client, key, cfg, tools_list, cfg.prompt, payload_for(rows[0]),
            cfg.max_output, rng)
        if etype2:
            print(f"\nFAILED on cache probe: {etype2}: {emsg2}")
            sys.exit(1)
        rc.print_stats(f"  call {n}", u2, lat2, show_write=False)
        if n == 2:
            hit = u2["cached_tokens"] / max(u2["input_tokens"], 1)
            parsed, note = rc.parse_json(text2)
            print()
            if hit > 0.8:
                print(f"  CACHING OK: {hit:.0%} of input read from cache on the second call.")
            elif hit > 0.3:
                print(f"  CACHING PARTIAL: {hit:.0%}. Expected if the search loop fired -- the")
                print("  second call in the loop carries uncached search results.")
            else:
                print(f"  CACHING WEAK: only {hit:.0%} cached on call 2.")
                print("  Automatic caching is best-effort. Check nothing dynamic precedes")
                print("  the prompt and that the system message is byte-identical.")
                print("  The run is still valid if this stays low -- just costlier. Report it.")
            print(f"  parsed JSON on probe: {note}")
            if parsed is not None:
                errs = rc.contract_errors(
                    rc.check_contract(parsed, rows[0].get("review_text", ""), cfg.legal_codes))
                print(f"  contract: {'OK' if not errs else '; '.join(errs)}")
            per = rc.cost_usd(u2, cfg.pricing, len(s2))["total"]
            print(f"  output tokens {u2['output_tokens']:,} "
                  f"(reasoning {u2['reasoning_tokens']:,}) <- this sets the bill")
            print(f"  ~${per:.6f}/review  ->  ~${per * len(rows):.4f} for {len(rows)} reviews"
                  f"  ->  ~${per * PROJECT_TO:,.0f} at {PROJECT_TO:,}")

    print(f"\nIf caching is OK and the JSON parsed, run:\n"
          f"  python run_teacher_kimi.py --actual --model {cfg.model} "
          f"--effort {cfg.effort} --prompt {show(cfg.prompt_file)}")


# ------------------------------------------------------------------ actual run

def actual_run(cfg: RunConfig, a: argparse.Namespace) -> None:
    rng = random.Random(RNG_SEED)
    client, key = get_client()
    rows = rc.select_reviews(cfg.reviews_file, cfg.only, cfg.limit)
    paths = cfg.paths
    paths.mkdir()

    done = rc.resume_gate(paths, cfg.prompt_sha, a.resume, a.overwrite)
    todo = [r for r in rows if r.get("review_id") not in done]

    preflight(cfg, rows, done)
    if not todo:
        print("nothing to do: every selected review is already labelled.")
        return

    tools_list = get_web_search_tools(key, cfg.retries, rng) if cfg.web_search else None

    n_super = rc.supersede(paths, {r.get("review_id") for r in todo})
    if n_super:
        print(f"superseding {n_super} failed row(s) from the previous pass")
    counters, spend, all_usage = rc.prior_state(paths)
    _, state = rc.load_progress(paths)
    started = state.get("started") or datetime.now().isoformat(timespec="seconds")
    watch = rc.CacheWatch()
    f_resp = open(paths.responses, "a", encoding="utf-8")
    f_meta = open(paths.meta, "a", encoding="utf-8")
    n_extra_calls = int(state.get("extra_tool_loop_calls", 0))

    def save(complete: bool) -> None:
        rc.write_checkpoint(paths, {
            "tag": paths.tag, "model": cfg.model, "reasoning_effort": cfg.effort,
            "prompt_file": str(cfg.prompt_file), "prompt_sha256": cfg.prompt_sha,
            "reviews_file": str(cfg.reviews_file), "n_selected": len(rows),
            "started": started, "complete": complete, "spend_usd": round(spend, 6),
            "extra_tool_loop_calls": n_extra_calls, **counters})

    print(f"\n{len(todo)} reviews to label -> {show(paths.responses)}\n")
    stopped = None
    try:
        for i, row in enumerate(todo, 1):
            rid = str(uuid.uuid4())
            res = label_review(client, key, cfg, tools_list, row, rng, watch)

            u = res["usage"]
            cost = rc.cost_usd(u, cfg.pricing, res["n_searches"]) if u else {"total": 0.0}
            spend += cost["total"]
            n_att = len(res["attempts"])
            counters["extra_attempts"] += max(n_att - 1, 0)
            counters["retried"] += n_att > 1
            n_extra_calls += max(res["n_calls"] - n_att, 0)
            truncated = res["finish_reason"] == "length"
            failed_parse = res["parsed"] is None and not res["api_error_type"]

            meta = {"request_id": rid, "review_id": row.get("review_id"),
                    "ts": datetime.now().isoformat(timespec="seconds"),
                    "provider": "moonshot", "model": cfg.model,
                    "reasoning_effort": cfg.effort,
                    "prompt_file": str(cfg.prompt_file), "prompt_sha256": cfg.prompt_sha,
                    "cache_mode": "automatic", "base_url": BASE_URL,
                    "temperature": TEMPERATURE if SEND_TEMPERATURE else "default",
                    "web_search": cfg.web_search,
                    "web_search_channel": f"formula:{FORMULA_URI}",
                    "max_tool_rounds": cfg.max_tool_rounds, "pricing": cfg.pricing,
                    "latency_s": round(res["latency_s"], 2),
                    # error_type is API failure only; a response that arrived and would
                    # not parse gets its own flag. The call was billed either way.
                    "error_type": res["api_error_type"],
                    "error_message": res["api_error_message"],
                    "parse_failed": failed_parse,
                    "n_attempts": n_att, "n_api_calls": res["n_calls"],
                    "attempt_parse_notes": [x["parse_note"] for x in res["attempts"]]}

            rec = {"request_id": rid, "review_id": row.get("review_id"),
                   "raw": res["raw"], "parsed": res["parsed"],
                   "parse_note": res["parse_note"],
                   "error_type": res["api_error_type"] or ("parse_failed" if failed_parse
                                                           else None)}
            if n_att > 1:
                rec["attempts"] = res["attempts"]      # audit trail for the paper

            if u:
                all_usage.append(u)
                meta |= {"usage": u, "cost_usd": cost}

            if res["api_error_type"]:
                counters["api_errors"] += 1
                print(f"  [{i:>2}/{len(todo)}] API ERROR {res['api_error_type']}: "
                      f"{(res['api_error_message'] or '')[:60]}")
            else:
                meta |= {"status": res["finish_reason"],
                         "incomplete_reason": "max_tokens" if truncated else None,
                         "n_web_searches": res["n_searches"],
                         "search_queries": [s["query"] for s in res["searches"]],
                         "search_result_chars": [s["result_chars"] for s in res["searches"]],
                         "parse_note": res["parse_note"]}

                if res["parsed"] is None:
                    counters["parse_failures"] += 1
                    rc.print_stats(f"[{i:>2}/{len(todo)}] {'PARSE FAILED':<16}", u,
                                   res["latency_s"], show_write=False)
                    print(f"       gave up after {n_att} attempts  ${cost['total']:.6f}  "
                          f"running ${spend:.4f}")
                else:
                    counters["ok"] += 1
                    counters["parsed"] += 1
                    counters["truncated"] += truncated
                    counters["searched"] += res["n_searches"] > 0
                    v = res["contract"] or {}
                    errs = rc.contract_errors(v) if v else []
                    counters["contract_bad"] += bool(errs)
                    meta |= {"n_labels": len(v.get("labels", [])),
                             "contract": {k: v[k] for k in
                                          ("bad_codes", "dup_codes", "missing_span",
                                           "span_bad", "span_loose")} if v else None}
                    flag = " TRUNCATED" if truncated else ""
                    note = res["parse_note"] + (f" x{n_att}" if n_att > 1 else "")
                    rc.print_stats(f"[{i:>2}/{len(todo)}] {note:<16}", u,
                                   res["latency_s"], show_write=False)
                    print(f"       ${cost['total']:.6f}  running ${spend:.4f}  "
                          f"labels={meta['n_labels']}  searches={res['n_searches']}  "
                          f"calls={res['n_calls']}{flag}")
                    if errs:
                        print(f"       CONTRACT: {'; '.join(errs)}")

            f_resp.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f_meta.write(json.dumps(meta, ensure_ascii=False) + "\n")
            f_resp.flush(); f_meta.flush()
            save(complete=False)

            if cfg.max_spend and spend > cfg.max_spend:
                stopped = f"spend guard: ${spend:.4f} over the ${cfg.max_spend:g} ceiling"
                break
    except KeyboardInterrupt:
        stopped = "interrupted (Ctrl-C)"
    finally:
        f_resp.close(); f_meta.close()

    save(complete=stopped is None)
    rc.summarize(paths, counters, spend, all_usage, cfg.pricing, PROJECT_TO, extra={
        "complete": stopped is None, "stopped_because": stopped,
        "started": started, "provider": "moonshot",
        "model": cfg.model, "reasoning_effort": cfg.effort, "web_search": cfg.web_search,
        "web_search_channel": f"formula:{FORMULA_URI}", "cache_mode": "automatic",
        "max_tool_rounds": cfg.max_tool_rounds,
        "temperature": TEMPERATURE if SEND_TEMPERATURE else "default",
        "prompt_file": str(cfg.prompt_file), "prompt_sha256": cfg.prompt_sha,
        "reviews_file": str(cfg.reviews_file),
        "max_output": cfg.max_output, "parse_retries": cfg.parse_retries,
        "extra_tool_loop_calls": n_extra_calls,
        "manifest": rc.run_manifest(cfg.prompt_file, __file__),
    })

    if stopped:
        print(f"\nSTOPPED: {stopped}")
        print(f"  resume with:  python run_teacher_kimi.py --actual --resume "
              f"--model {cfg.model} --effort {cfg.effort} --prompt {show(cfg.prompt_file)}")
        sys.exit(2)
    print(f"\nnext: python compute_run_stats.py --run-dir {show(paths.dir)}")


# --------------------------------------------------------------------------- cli

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Run a teacher prompt over a review set on Kimi K3.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true",
                      help="offline preflight: config, prompt, paths. No API calls.")
    mode.add_argument("--dry", action="store_true",
                      help="one live call plus a caching probe")
    mode.add_argument("--actual", action="store_true", help="label the review set")

    ap.add_argument("--model", default=DEFAULT_MODEL,
                    help=f"one of: {', '.join(sorted(rc.PRICING_TABLE))} "
                         f"(pricing is looked up, not configured)")
    ap.add_argument("--effort", default=DEFAULT_EFFORT,
                    choices=["low", "high", "max"],
                    help="KIMI DIFF 2: no 'medium', so not comparable to the Luna sweep")
    ap.add_argument("--prompt", default=DEFAULT_PROMPT,
                    help="built prompt file; its stem names the output directory")
    ap.add_argument("--reviews", default=DEFAULT_REVIEWS)
    ap.add_argument("--out-root", default=OUT_ROOT)

    ap.add_argument("--resume", action="store_true",
                    help="continue an interrupted run, skipping reviews already done")
    ap.add_argument("--overwrite", action="store_true",
                    help="discard an interrupted run and start clean")

    ap.add_argument("--limit", type=int, default=0, help="0 = all")
    ap.add_argument("--only", default="",
                    help="comma-separated review_ids; re-run just the ones a prompt got wrong")
    ap.add_argument("--max-spend", type=float, default=0.0,
                    help="stop the run once spend passes this many USD (0 = no ceiling)")
    ap.add_argument("--max-output", type=int, default=MAX_OUTPUT)
    ap.add_argument("--max-tool-rounds", type=int, default=MAX_TOOL_ROUNDS,
                    help="searches allowed per review before tool_choice=none")
    ap.add_argument("--parse-retries", type=int, default=PARSE_RETRIES,
                    help="extra attempts when the response will not parse as JSON")
    ap.add_argument("--retries", type=int, default=RETRIES,
                    help="transport-level attempts per call")
    ap.add_argument("--no-web-search", action="store_true")

    a = ap.parse_args()
    if a.resume and a.overwrite:
        ap.error("--resume and --overwrite are opposites; pick one")
    return a


def main() -> None:
    a = parse_args()
    cfg = build_config(a)
    if a.check:
        rows = rc.select_reviews(cfg.reviews_file, cfg.only, cfg.limit)
        done, state = rc.load_progress(cfg.paths)
        preflight(cfg, rows, done)
        if done:
            print(f"on disk: {len(done)} labelled, "
                  f"complete={state.get('complete')}, spend=${state.get('spend_usd', 0):.4f}")
        print("\nno API calls made. --dry to check the connection and caching.")
    elif a.dry:
        dry_run(cfg)
    else:
        actual_run(cfg, a)


if __name__ == "__main__":
    main()
