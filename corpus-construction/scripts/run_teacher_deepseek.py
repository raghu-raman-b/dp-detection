#!/usr/bin/env python3
"""
run_teacher_deepseek.py -- run a teacher prompt over the tuning 50 on DeepSeek V4.

    python run_teacher_deepseek.py --check                offline: config, prompt, paths
    python run_teacher_deepseek.py --dry                  one live call + a caching probe
    python run_teacher_deepseek.py --actual               labels the 50
    python run_teacher_deepseek.py --actual --resume      picks up where a killed run stopped

Needs:  pip install openai requests   (DeepSeek's chat surface is OpenAI-compatible; the
                                       web-search tool in web_search_tool.py is plain REST)

Same command-line surface, same output tree, same resume semantics as
run_teacher_openai.py and run_teacher_kimi.py -- the shared half lives in
runner_common.py, so a prompt ablation is driven identically whichever provider is under
test:

    python run_teacher_deepseek.py --actual --prompt ../outputs/prompts/teacher_v2_bare.txt

Sequential within a run, same as the other two: DeepSeek's automatic context caching
rewards a stable prefix sent repeatedly, so cold parallel workers would all miss.

Six ways DeepSeek differs. Each is marked DEEPSEEK DIFF below.
  1. THERE IS NO WEB SEARCH. DeepSeek ships no search product at any tier, and R10 of
     the prompt grants every provider one search per review. So the search is ours:
     web_search_tool.py is declared as an ordinary function tool and executed here in a
     client-side loop, exactly the shape run_teacher_kimi.py uses for the Formula API.
     Two consequences worth stating plainly: (a) there is no once-per-run tool-declaration
     fetch, because the declaration is a local constant -- which also means the tool
     bytes are stable across calls, which prefix caching requires; (b) the search bill is
     Tavily's, not DeepSeek's, and it is carried in PRICING_TABLE's search_per_call so
     rc.cost_usd needs no special-casing. preflight asserts the two agree.
  2. PRICING DEPENDS ON THE UTC CLOCK. Peak is 01:00-04:00 and 06:00-10:00 UTC and costs
     exactly double; every other hour is half. No other provider in the bake-off does
     this. The rate is therefore resolved PER CALL from the hour the call started, and
     every row records its window and utc_hour. See the block comment above actual_run.
  3. reasoning_content MUST BE ECHOED BACK across tool rounds. When `tools` is passed,
     DeepSeek requires the intermediate assistant reasoning_content in every subsequent
     turn -- omitting it is a 400, not a quality regression, and it applies even on turns
     where the model did not call a tool. This is the same trap k3 has for the same
     reason, and the same fix: echo the model's own message dump back unfiltered.
  4. THE EFFORT AXIS HAS TWO RUNGS. On the OpenAI-compatible surface, thinking is a
     boolean: extra_body={"thinking": {"type": "enabled"|"disabled"}}. The finer
     none|low|high|max ladder exists only on DeepSeek's Anthropic-format surface, which
     is a different base_url, different usage field names and a different tool-call
     shape -- a third architecture for one extra axis point. So --effort here is
     none|high and DeepSeek contributes a thinking-on/off contrast to the sweep, not an
     effort curve. --effort-surface reasoning is wired up for anyone who wants to probe
     the other surface; --dry will tell you whether it 400s.
  5. Caching is automatic prefix caching -- no breakpoint, no write charge. Stable
     prefix first, per-review text last, which the prompt already does.
  6. 1M context and a 384K output ceiling, so MAX_OUTPUT_CAP is nowhere near the model's
     limit. MAX_OUTPUT stays at the same 8192 the other runners use, for comparability.

Output tree, one directory per (model, effort, prompt):

    ../outputs/runs/<model>/<effort>/<prompt_stem>/
        <tag>_responses.jsonl   raw text + parsed JSON (+ every re-attempt)
        <tag>_meta.jsonl        usage, cost, latency, status, price window, contract
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
from datetime import datetime, timezone
from pathlib import Path

from openai import OpenAI

sys.path.insert(0, str(Path(__file__).parent))
import runner_common as rc
import web_search_tool as wst
from build_prompt import load_prompt

SCRIPT_DIR = Path(__file__).resolve().parent
resolve, show, payload_for = rc.resolve, rc.show, rc.payload_for

# ============================== DEFAULTS ==============================
DEFAULT_MODEL   = "deepseek-v4-pro"
DEFAULT_EFFORT  = "high"            # none | high   (DEEPSEEK DIFF 4; no ladder)
DEFAULT_PROMPT  = "../outputs/prompts/teacher_v2_full.txt"
# The review set and the run tree both come from --eval-set
# (runner_common.EVAL_SETS), asked interactively when the flag is omitted:
#   tuning      ../tuning/tuning_set_50_blind.jsonl      -> ../outputs/runs
#   validation  ../validation/validation_set_blind.jsonl -> ../outputs/validation/runs
# Both are blind files: no gold ever enters this process. --reviews and
# --out-root still override, for a one-off against some other file.
BASE_URL        = "https://api.deepseek.com"

MAX_OUTPUT      = 8192      # reasoning counts against this; too low = truncated JSON
MAX_OUTPUT_CAP  = 32768     # ceiling for the truncation bump (DEEPSEEK DIFF 6: the
                            # model would allow 384K; this cap is for comparability)
TRUNCATION_BUMP = 2.0

RETRIES         = 3         # transport-level attempts per call
PARSE_RETRIES   = 2         # extra attempts when the response is not parseable JSON
SEND_TEMPERATURE = False    # V4 reasons; leave off unless you decide otherwise
TEMPERATURE     = 0.0
PROJECT_TO      = 200_000
RNG_SEED        = 20260822  # only seeds retry jitter; no effect on model sampling

# DEEPSEEK DIFF 1: the frozen policy is one search per review. The loop enforces it:
# after MAX_TOOL_ROUNDS the next call goes out with tool_choice="none" so the model
# must answer from what it has.
MAX_TOOL_ROUNDS = 1
SEARCH_BACKEND  = "tavily"
SEARCH_CACHE    = "../outputs/web-search-cache"

# DEEPSEEK DIFF 4: what each --effort actually puts on the wire. One dict, so the
# question "does this axis change the request at all?" has exactly one answer to read.
EFFORT_SURFACE  = "thinking"        # thinking | reasoning
EFFORT_BODY = {
    "thinking": {                                   # OpenAI-compatible surface
        "none": {"thinking": {"type": "disabled"}},
        "high": {"thinking": {"type": "enabled"}},
    },
    "reasoning": {                                  # unverified; --dry probes it
        "none": {"reasoning": {"effort": "none"}},
        "low":  {"reasoning": {"effort": "low"}},
        "high": {"reasoning": {"effort": "high"}},
        "max":  {"reasoning": {"effort": "max"}},
    },
}

API_KEY_ENV     = "DEEPSEEK_API_KEY"
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
    eval_set: str
    web_search: bool
    max_output: int
    parse_retries: int
    retries: int
    max_tool_rounds: int
    limit: int
    only: set
    max_spend: float
    effort_surface: str = EFFORT_SURFACE
    pin_window: str = "auto"           # auto | peak | off_peak  (DEEPSEEK DIFF 2)
    search_backend: str = SEARCH_BACKEND
    search_cache: str = SEARCH_CACHE
    prompt: str = ""
    prompt_sha: str = ""
    legal_codes: set = field(default_factory=set)
    pricing: dict = field(default_factory=dict)
    paths: rc.RunPaths | None = None

    def pricing_now(self, when: datetime | None = None) -> dict:
        """DEEPSEEK DIFF 2. Pinned runs freeze one rate card; otherwise the window is
        resolved from the hour this call started. Either way a FLAT dict comes back,
        so rc.cost_usd and compute_run_stats.py see the shape they always see."""
        if self.pin_window != "auto":
            return self.pricing
        return rc.pricing_for(self.model, when=when or datetime.now(timezone.utc))


def build_config(a: argparse.Namespace) -> RunConfig:
    cfg = RunConfig(
        model=a.model, effort=a.effort,
        prompt_file=resolve(a.prompt), reviews_file=resolve(a.reviews),
        eval_set=a.eval_set,
        out_root=resolve(a.out_root), web_search=not a.no_web_search,
        max_output=a.max_output, parse_retries=a.parse_retries, retries=a.retries,
        max_tool_rounds=a.max_tool_rounds, limit=a.limit,
        only={s.strip() for s in a.only.split(",") if s.strip()} if a.only else set(),
        max_spend=a.max_spend, effort_surface=a.effort_surface,
        pin_window=a.pin_window, search_backend=a.search_backend,
        search_cache="" if a.no_search_cache else a.search_cache,
    )
    if not cfg.prompt_file.exists():
        sys.exit(f"prompt not found: {cfg.prompt_file}\n"
                 f"  build one:  python build_prompt.py")
    if cfg.effort not in EFFORT_BODY[cfg.effort_surface]:
        sys.exit(f"--effort {cfg.effort!r} is not available on the "
                 f"{cfg.effort_surface!r} surface.\n"
                 f"  available: {', '.join(EFFORT_BODY[cfg.effort_surface])}")
    cfg.prompt = load_prompt(cfg.prompt_file)
    cfg.prompt_sha = hashlib.sha256(cfg.prompt.encode()).hexdigest()
    cfg.legal_codes = rc.legal_codes_from_prompt(cfg.prompt)
    cfg.pricing = rc.pricing_for(
        cfg.model, window=None if cfg.pin_window == "auto" else cfg.pin_window)
    cfg.paths = rc.RunPaths(cfg.out_root, cfg.model, cfg.effort, cfg.prompt_file)
    return cfg


def get_client() -> "OpenAI":
    """max_retries=0 hands the retry policy back to rc.call_with_retries. The SDK
    retries twice of its own accord by default, which would silently nest two
    uncoordinated backoff schedules inside one rc attempt and under-report
    counters['retried']."""
    return OpenAI(api_key=rc.load_api_key(API_KEY_ENV, SCRIPT_DIR, ENV_FILE),
                  base_url=BASE_URL, max_retries=0, timeout=600.0)


def get_search_tool(cfg: RunConfig) -> "wst.WebSearchTool | None":
    if not cfg.web_search:
        return None
    return wst.WebSearchTool(cfg.search_backend,
                             cache_dir=cfg.search_cache or None,
                             rng=random.Random(RNG_SEED))


# --------------------------------------------------------------------- the call

def effort_body(cfg: RunConfig) -> dict:
    """DEEPSEEK DIFF 4: the single place that answers 'what does --effort send?'."""
    return dict(EFFORT_BODY[cfg.effort_surface][cfg.effort])


def build_kwargs(cfg: RunConfig, messages: list, use_tools: bool,
                 tools_list: list | None, max_output: int) -> dict:
    kw = {
        "model": cfg.model,
        "messages": messages,
        "max_tokens": max_output,          # chat-completions name, not max_output_tokens
        "extra_body": effort_body(cfg),    # DEEPSEEK DIFF 4: not a top-level param
    }
    if cfg.web_search and tools_list:
        kw["tools"] = tools_list                    # resent on every call in the loop
        if not use_tools:
            kw["tool_choice"] = "none"              # forces a final answer at the cap
    if SEND_TEMPERATURE:
        kw["temperature"] = TEMPERATURE
    return kw


def usage_of(resp) -> dict:
    """One API call's usage. Field names match the OpenAI runner so the shared cost
    maths and compute_run_stats.py need no special-casing.

    DeepSeek reports prompt_cache_hit_tokens / prompt_cache_miss_tokens, but the
    OpenAI-compatible shim has moved cached_tokens around between versions, so probe
    both. hit + miss should equal prompt_tokens; if it ever does not, flag it rather
    than crash -- a silent disagreement here is a wrong bill, and --dry prints it."""
    u = resp.usage
    hit = getattr(u, "prompt_cache_hit_tokens", None)
    miss = getattr(u, "prompt_cache_miss_tokens", None)
    if hit is None:
        d = getattr(u, "prompt_tokens_details", None)
        hit = getattr(d, "cached_tokens", 0) if d else 0
    hit = hit or 0
    plain = miss if miss is not None else (u.prompt_tokens - hit)
    reasoning = 0
    cd = getattr(u, "completion_tokens_details", None)
    if cd:
        reasoning = getattr(cd, "reasoning_tokens", 0) or 0
    out = {
        "input_tokens": u.prompt_tokens,               # inclusive of the cache hit
        "cached_tokens": hit,
        "cache_write_tokens": 0,                       # DEEPSEEK DIFF 5: no such charge
        "uncached_input_tokens": plain,
        "output_tokens": u.completion_tokens,
        "reasoning_tokens": reasoning,
        "total_tokens": getattr(u, "total_tokens", None),
    }
    if hit + plain != u.prompt_tokens:
        out["usage_mismatch"] = {"hit": hit, "miss": plain,
                                 "prompt_tokens": u.prompt_tokens}
    return out


# compute_run_stats.py counts a review as truncated when status == "incomplete", and
# compare_runs.py gates a run out of the ranking on truncated > 0. chat-completions
# reports finish_reason instead, so the raw value is normalised into that vocabulary
# here -- left raw, a truncated run reports zero truncations and sails through the gate.
STATUS_OF = {"stop": "completed", "length": "incomplete", "tool_calls": "tool_use",
             "content_filter": "refusal", "insufficient_system_resource": "incomplete"}


def status_of(finish_reason: str | None) -> str:
    return STATUS_OF.get(finish_reason or "", finish_reason or "completed")


def one_call(client, cfg: RunConfig, messages: list, use_tools: bool,
             tools_list: list | None, max_output: int, rng: random.Random):
    """A single API call with retries. Returns (response, latency, etype, emsg)."""
    return rc.call_with_retries(
        lambda: client.chat.completions.create(
            **build_kwargs(cfg, messages, use_tools, tools_list, max_output)),
        cfg.retries, rng)


def run_review(client, cfg: RunConfig, tool, tools_list: list | None,
               system_prompt: str, user_input: str, max_output: int,
               rng: random.Random, review_id: str = ""):
    """DEEPSEEK DIFF 1: the whole tool loop for ONE review, against our own search tool.

    Returns (text, usage, latency, n_calls, searches, finish_reason, served, etype,
    emsg) -- `served` is resp.model, the dated build that actually answered, which the
    paper needs and which the request's alias does not give you.
    `searches` holds the query, whether it was a cache hit, and its cost, which is
    where the invoked_web_search / search_query audit fields and the search half of the
    bill both come from. `usage`/`latency` cover only the chat calls; the search call is
    separate and billed by the backend (see PRICING_TABLE's search_per_call).
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
            return None, usage, total_latency, n_calls, searches, None, None, etype, emsg

        usage = rc.add_usage(usage, usage_of(resp))
        choice = resp.choices[0]
        served = getattr(resp, "model", None)

        if choice.finish_reason != "tool_calls":
            return (choice.message.content, usage, total_latency, n_calls,
                    searches, choice.finish_reason, served, None, None)

        # DEEPSEEK DIFF 3: echo the assistant message back verbatim and unfiltered.
        # With `tools` in play DeepSeek REQUIRES the intermediate reasoning_content in
        # every later turn -- dropping it is a 400, not a degradation. model_dump keeps
        # everything the SDK parsed, which is exactly what the API wants back. (k3 has
        # the same requirement for its own reasons; see run_teacher_kimi.py.)
        messages.append(choice.message.model_dump(exclude_none=True))
        for tc in choice.message.tool_calls or []:
            if tc.function.name == wst.TOOL_NAME and tool is not None:
                res = tool.execute(tc.function.arguments, review_id=review_id,
                                   caller="deepseek")
                content = res.as_tool_content()
                searches.append({"query": res.query, "result_chars": len(content),
                                 "cached": res.cached, "cost_usd": res.cost_usd,
                                 "backend": res.backend, "error": res.error,
                                 "n_results": res.n_results})
            else:
                content = f"Error: unable to find tool by name '{tc.function.name}'"
            messages.append({"role": "tool", "tool_call_id": tc.id,
                             "name": tc.function.name, "content": content})
        rounds += 1


def label_review(client, cfg: RunConfig, tool, tools_list: list | None,
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
    review_id = row.get("review_id", "")
    attempts: list = []
    usage_total: dict = {}
    latency_total = 0.0
    n_calls = 0
    all_searches: list = []
    max_out = cfg.max_output
    fin = None
    served_model = None

    for k in range(cfg.parse_retries + 1):
        text, u, lat, calls, searches, fin, served, etype, emsg = run_review(
            client, cfg, tool, tools_list, cfg.prompt, payload, max_out, rng, review_id)
        served_model = served or served_model
        latency_total += lat
        n_calls += calls
        all_searches += searches
        if etype:
            return {"api_error_type": etype, "api_error_message": emsg,
                    "attempts": attempts,
                    "usage": rc.add_usage(usage_total, u) if u else usage_total,
                    "latency_s": latency_total, "n_calls": n_calls,
                    "n_searches": len(all_searches), "searches": all_searches,
                    "finish_reason": None, "served_model": served_model,
                    "parsed": None, "raw": None,
                    "parse_note": None, "contract": None}

        usage_total = rc.add_usage(usage_total, u)
        watch.observe(u)
        parsed, note = rc.parse_json(text)
        attempts.append({"n": k + 1, "max_output": max_out, "status": fin,
                         "parse_note": note, "latency_s": round(lat, 2),
                         "n_api_calls": calls, "usage": u, "raw": text,
                         "search_queries": [s["query"] for s in searches]})

        if parsed is not None:
            return {"api_error_type": None, "api_error_message": None,
                    "attempts": attempts, "usage": usage_total,
                    "latency_s": latency_total, "n_calls": n_calls,
                    "n_searches": len(all_searches), "searches": all_searches,
                    "finish_reason": fin, "served_model": served_model,
                    "parsed": parsed, "raw": text, "parse_note": note,
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
            "n_searches": len(all_searches), "searches": all_searches,
            "finish_reason": fin, "served_model": served_model,
            "parsed": None, "raw": attempts[-1]["raw"],
            "parse_note": "parse_failed", "contract": None}


# ---------------------------------------------------------------------- preflight

def window_report(cfg: RunConfig, n_todo: int) -> None:
    """DEEPSEEK DIFF 2. The cheapest fix for peak pricing is to not start a run at
    09:50 UTC, so say so before the run rather than in the summary afterwards."""
    now = datetime.now(timezone.utc)
    win = rc.pricing_window(now)
    mins_left = min(((lo - now.hour - 1) % 24) * 60 + (60 - now.minute)
                    for lo, hi in ((a, b) for a, b in rc.PEAK_WINDOWS_UTC)) \
        if win == "off_peak" else \
        min(((hi - now.hour - 1) % 24) * 60 + (60 - now.minute)
            for lo, hi in rc.PEAK_WINDOWS_UTC if lo <= now.hour < hi)
    est_min = n_todo * 25 / 60          # ~25s/review, the observed rate on the others
    print(f"price window   {win} at {now.strftime('%H:%M')} UTC   "
          f"(peak = 01:00-04:00 and 06:00-10:00 UTC, 2x)")
    if cfg.pin_window != "auto":
        print(f"               PINNED to {cfg.pin_window}: every row is billed at that "
              f"card regardless of the clock, and says so in its meta.")
    elif est_min > mins_left:
        print(f"               !! PRICING BOUNDARY in ~{mins_left:.0f} min but this run "
              f"needs ~{est_min:.0f} min.")
        print(f"               Rows either side are priced differently (correctly, per "
              f"call). To keep one window, start after 10:00 UTC.")
    else:
        print(f"               ~{est_min:.0f} min needed, ~{mins_left:.0f} min left in "
              f"this window -- the run should stay in it.")


def preflight(cfg: RunConfig, rows: list, done: set) -> None:
    man = rc.prompt_manifest(cfg.prompt_file)
    p = cfg.pricing
    print("=" * 72)
    print(f"model          {cfg.model}   effort={cfg.effort or 'none'}   "
          f"web_search={cfg.web_search}   max_tool_rounds={cfg.max_tool_rounds}")
    print(f"effort sends   {json.dumps(effort_body(cfg))}   "
          f"(surface={cfg.effort_surface}; DEEPSEEK DIFF 4)")
    print(f"pricing        in ${p['input']} / cached ${p['cached_input']} / "
          f"out ${p['output']} per MTok + ${p.get('search_per_call', 0)}/search"
          f"   (as of {p['as_of']})")
    window_report(cfg, len(rows) - len(done))
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
    print(f"cache          automatic prefix caching (DEEPSEEK DIFF 5: no breakpoint, "
          f"no write fee)")
    if cfg.web_search:
        print(f"search         {cfg.search_backend} via web_search_tool.py "
              f"(DEEPSEEK DIFF 1: client-side loop)")
        print(f"               cache {show(resolve(cfg.search_cache)) if cfg.search_cache else 'OFF'}")
    else:
        print(f"search         off")
    print(f"budget         max_tokens={cfg.max_output:,} (bump to {MAX_OUTPUT_CAP:,} on "
          f"truncation)  parse_retries={cfg.parse_retries}")
    if cfg.max_spend:
        print(f"spend guard    stop above ${cfg.max_spend:g}")
    print(f"output         {show(cfg.paths.dir)}/")
    print("=" * 72)


def check_search_pricing(cfg: RunConfig, tool) -> None:
    """The search fee in PRICING_TABLE is the BACKEND's list price, not DeepSeek's. If
    the two ever drift the run's bill is quietly wrong, so fail loudly at preflight."""
    if tool is None:
        return
    listed = cfg.pricing.get("search_per_call", 0.0)
    if abs(tool.cost_per_search - listed) > 1e-9:
        sys.exit(f"search pricing disagreement:\n"
                 f"  {tool.name} backend charges ${tool.cost_per_search}/search\n"
                 f"  PRICING_TABLE['{cfg.model}']['search_per_call'] = ${listed}\n"
                 f"  update runner_common.py (and record the date you read it).")


# --------------------------------------------------------------- dry run

def dry_run(cfg: RunConfig) -> None:
    rng = random.Random(RNG_SEED)
    client = get_client()
    rows = rc.select_reviews(cfg.reviews_file, cfg.only, cfg.limit)
    preflight(cfg, rows, set())

    tool = get_search_tool(cfg)
    check_search_pricing(cfg, tool)
    tools_list = wst.openai_tools() if tool else None
    if tools_list:
        print(f"\ntool declared locally: {tools_list[0]['function']['name']} "
              f"(no per-run fetch; DEEPSEEK DIFF 1)")

    # --- stage 1: does the API work, and does the tool loop actually complete? ---
    print("\n[1/2] throwaway call with search (short prompt, below the cache floor)...")
    probe_cfg = RunConfig(**{**cfg.__dict__,
                             "prompt": "You are a helpful assistant. Answer in one sentence."})
    text, u, lat, n_calls, searches, fin, served, etype, emsg = run_review(
        client, probe_cfg, tool, tools_list, probe_cfg.prompt,
        "What is a welkin pass in Genshin Impact? Search before answering.",
        cfg.max_output, rng, review_id="dry-probe")
    if etype:
        print(f"\nFAILED: {etype}: {emsg}")
        if "reasoning" in str(emsg).lower() or "400" in str(etype):
            print("  If this is a 400 mentioning reasoning_content, DEEPSEEK DIFF 3 is")
            print("  the culprit: the assistant echo is being filtered somewhere.")
        sys.exit(1)
    print(f"  api calls    {n_calls}  (2 means the search loop ran)")
    print(f"  finish       {fin} -> status={status_of(fin)}   served={served}")
    print(f"  text         {(text or '')[:200]!r}")
    print(f"  searches     {[s['query'] for s in searches] or 'none'}")
    for s in searches:
        print(f"  search       {s['result_chars']} chars, cached={s['cached']}, "
              f"${s['cost_usd']:.4f}, {s['n_results']} results"
              + (f", ERROR {s['error']}" if s["error"] else ""))
    rc.print_stats("  stage1", u, lat, show_write=False)
    if "usage_mismatch" in u:
        print(f"  !! usage mismatch {u['usage_mismatch']} -- hit+miss != prompt_tokens.")
        print(f"     Check usage_of() against DeepSeek's current field names.")

    # --- stage 2: does the real prompt cache? two identical-prefix calls. ---
    print("\n[2/2] automatic caching check: two calls with the real prompt...")
    for n in (1, 2):
        text2, u2, lat2, nc2, s2, fin2, served2, etype2, emsg2 = run_review(
            client, cfg, tool, tools_list, cfg.prompt, payload_for(rows[0]),
            cfg.max_output, rng, review_id=rows[0].get("review_id", "dry"))
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
                    rc.check_contract(parsed, rows[0].get("review_text", ""),
                                      cfg.legal_codes))
                print(f"  contract: {'OK' if not errs else '; '.join(errs)}")
            pr = cfg.pricing_now()
            per = rc.cost_usd(u2, pr, len(s2))["total"]
            print(f"  output tokens {u2['output_tokens']:,} "
                  f"(reasoning {u2['reasoning_tokens']:,}) <- this sets the bill")
            print(f"  ~${per:.6f}/review at the {pr['window']} rate"
                  f"  ->  ~${per * len(rows):.4f} for {len(rows)} reviews"
                  f"  ->  ~${per * PROJECT_TO:,.0f} at {PROJECT_TO:,}")
    if tool:
        print(f"\n  search tool: {tool.stats()}")

    print(f"\nIf caching is OK and the JSON parsed, run:\n"
          f"  python run_teacher_deepseek.py --actual --model {cfg.model} "
          f"--effort {cfg.effort} --prompt {show(cfg.prompt_file)}")


# ------------------------------------------------------------------ actual run

def actual_run(cfg: RunConfig, a: argparse.Namespace) -> None:
    rng = random.Random(RNG_SEED)
    client = get_client()
    rows = rc.select_reviews(cfg.reviews_file, cfg.only, cfg.limit)
    paths = cfg.paths
    paths.mkdir()

    done = rc.resume_gate(paths, cfg.prompt_sha, a.resume, a.overwrite)
    todo = [r for r in rows if r.get("review_id") not in done]

    preflight(cfg, rows, done)
    if not todo:
        print("nothing to do: every selected review is already labelled.")
        return

    tool = get_search_tool(cfg)
    check_search_pricing(cfg, tool)
    tools_list = wst.openai_tools() if tool else None

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
    search_spend = float(state.get("search_spend_usd", 0.0))
    windows_seen = set(state.get("pricing_windows_seen") or [])

    def save(complete: bool) -> None:
        rc.write_checkpoint(paths, {
            "tag": paths.tag, "model": cfg.model, "reasoning_effort": cfg.effort,
            "prompt_file": str(cfg.prompt_file), "prompt_sha256": cfg.prompt_sha,
            "eval_set": cfg.eval_set, "reviews_file": str(cfg.reviews_file), "n_selected": len(rows),
            "started": started, "complete": complete, "spend_usd": round(spend, 6),
            "extra_tool_loop_calls": n_extra_calls,
            "search_spend_usd": round(search_spend, 6),
            "pricing_windows_seen": sorted(windows_seen), **counters})

    print(f"\n{len(todo)} reviews to label -> {show(paths.responses)}\n")
    stopped = None
    try:
        for i, row in enumerate(todo, 1):
            rid = str(uuid.uuid4())
            started_utc = datetime.now(timezone.utc)
            # DEEPSEEK DIFF 2: the rate card is resolved HERE, from the hour this call
            # starts, and stored on the row. compute_run_stats.py reads the first row's
            # `pricing` and prints it as the run's rate card -- true when the run sits
            # in one window, and the summary's pricing_windows_seen says when it did not.
            pricing_now = cfg.pricing_now(started_utc)
            windows_seen.add(pricing_now["window"])

            res = label_review(client, cfg, tool, tools_list, row, rng, watch)

            u = res["usage"]
            n_billable = sum(1 for s in res["searches"]
                             if not s["cached"] and not s["error"])
            cost = rc.cost_usd(u, pricing_now, n_billable) if u else {"total": 0.0}
            spend += cost["total"]
            search_spend += sum(s["cost_usd"] for s in res["searches"])
            n_att = len(res["attempts"])
            counters["extra_attempts"] += max(n_att - 1, 0)
            counters["retried"] += n_att > 1
            n_extra_calls += max(res["n_calls"] - n_att, 0)
            truncated = res["finish_reason"] == "length"
            failed_parse = res["parsed"] is None and not res["api_error_type"]

            meta = {"request_id": rid, "review_id": row.get("review_id"),
                    "ts": datetime.now().isoformat(timespec="seconds"),
                    "provider": "deepseek", "model": cfg.model,
                    "reasoning_effort": cfg.effort,
                    "effort_surface": cfg.effort_surface,
                    "effort_body": effort_body(cfg),
                    "prompt_file": str(cfg.prompt_file), "prompt_sha256": cfg.prompt_sha,
                    "cache_mode": "automatic", "base_url": BASE_URL,
                    "temperature": TEMPERATURE if SEND_TEMPERATURE else "default",
                    "web_search": cfg.web_search,
                    "web_search_channel": (f"{cfg.search_backend}:web_search_tool"
                                           if cfg.web_search else None),
                    "max_tool_rounds": cfg.max_tool_rounds,
                    # DEEPSEEK DIFF 2: this row's own rate card, not the run's.
                    "pricing": pricing_now,
                    "pricing_window": pricing_now["window"],
                    "pricing_pinned": cfg.pin_window != "auto",
                    "utc_hour": started_utc.hour,
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
                meta |= {"status": status_of(res["finish_reason"]),
                         "finish_reason": res["finish_reason"],   # raw, kept alongside
                         "model_version": res["served_model"],
                         "incomplete_reason": "max_tokens" if truncated else None,
                         # total the teacher SAW; billable excludes cache hits
                         "n_web_searches": res["n_searches"],
                         "n_web_searches_billable": n_billable,
                         "n_web_searches_cached": sum(1 for s in res["searches"]
                                                      if s["cached"]),
                         "search_queries": [s["query"] for s in res["searches"]],
                         "search_result_chars": [s["result_chars"]
                                                 for s in res["searches"]],
                         "search_errors": [s["error"] for s in res["searches"]
                                           if s["error"]],
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
                          f"labels={meta['n_labels']}  searches={res['n_searches']}"
                          f"  calls={res['n_calls']}  [{pricing_now['window']}]{flag}")
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
    if len(windows_seen) > 1:
        print(f"\n!! this run straddled a pricing boundary: {sorted(windows_seen)}.")
        print(f"   Each row was billed at its own window (see meta.pricing_window), but")
        print(f"   the report's single rate card is the FIRST row's. Say so in the paper.")
    rc.summarize(paths, counters, spend, all_usage, cfg.pricing, PROJECT_TO, extra={
        "complete": stopped is None, "stopped_because": stopped,
        "started": started, "provider": "deepseek",
        "model": cfg.model, "reasoning_effort": cfg.effort,
        "effort_surface": cfg.effort_surface, "effort_body": effort_body(cfg),
        "web_search": cfg.web_search,
        "web_search_channel": (f"{cfg.search_backend}:web_search_tool"
                               if cfg.web_search else None),
        "cache_mode": "automatic", "max_tool_rounds": cfg.max_tool_rounds,
        "temperature": TEMPERATURE if SEND_TEMPERATURE else "default",
        "prompt_file": str(cfg.prompt_file), "prompt_sha256": cfg.prompt_sha,
        "eval_set": cfg.eval_set, "reviews_file": str(cfg.reviews_file),
        "max_output": cfg.max_output, "parse_retries": cfg.parse_retries,
        "extra_tool_loop_calls": n_extra_calls,
        "pricing_windows_seen": sorted(windows_seen),
        "pricing_pinned": cfg.pin_window != "auto",
        "search_spend_usd": round(search_spend, 6),
        "search_stats": tool.stats() if tool else None,
        "manifest": rc.run_manifest(cfg.prompt_file, __file__),
    })

    if stopped:
        print(f"\nSTOPPED: {stopped}")
        print(f"  resume with:  python run_teacher_deepseek.py --actual --resume "
              f"--model {cfg.model} --effort {cfg.effort} --prompt {show(cfg.prompt_file)}")
        sys.exit(2)
    print(f"\nnext: python compute_run_stats.py --run-dir {show(paths.dir)}")


# --------------------------------------------------------------------------- cli

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Run a teacher prompt over a review set on DeepSeek V4.",
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
                    help="DEEPSEEK DIFF 4: none|high on the default 'thinking' surface; "
                         "none|low|high|max on the 'reasoning' surface")
    ap.add_argument("--effort-surface", default=EFFORT_SURFACE,
                    choices=sorted(EFFORT_BODY),
                    help="which API surface carries the effort setting")
    ap.add_argument("--prompt", default=DEFAULT_PROMPT,
                    help="built prompt file; its stem names the output directory")
    ap.add_argument("--eval-set", choices=sorted(rc.EVAL_SETS), default=None,
                    help="tuning (the 50, burned on selection) or validation "
                         "(the 75, reported); asked interactively when omitted")
    ap.add_argument("--reviews", default=None,
                    help="override the review file --eval-set would pick")
    ap.add_argument("--out-root", default=None,
                    help="override the run tree --eval-set would pick")

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

    ap.add_argument("--pin-window", default="auto", choices=("auto", "peak", "off_peak"),
                    help="DEEPSEEK DIFF 2: 'auto' prices each call by the hour it "
                         "started (exact). Pinning declares one window for the whole "
                         "run and records that it is an assumption.")
    ap.add_argument("--search-backend", default=SEARCH_BACKEND,
                    choices=sorted(wst.BACKENDS),
                    help="which engine web_search_tool.py calls")
    ap.add_argument("--search-cache", default=SEARCH_CACHE,
                    help="disk cache so repeat queries are free and replayable")
    ap.add_argument("--no-search-cache", action="store_true",
                    help="search live every time (loses replayability; costs more)")

    a = ap.parse_args()
    if a.resume and a.overwrite:
        ap.error("--resume and --overwrite are opposites; pick one")

    # --eval-set picks the review file and the run tree together. Keeping them
    # in one switch is what stops a validation run landing in the tuning tree.
    a.eval_set = rc.resolve_eval_set(a.eval_set, what="label")
    _sel = rc.EVAL_SETS[a.eval_set]
    a.reviews = a.reviews or _sel["reviews"]
    a.out_root = a.out_root or _sel["runs"]
    # NB: unlike the OpenAI runner, "none" is NOT normalised to "". Here it is a real
    # rung (thinking disabled) and it keys into EFFORT_BODY. RunPaths renders "" and
    # "none" to the same directory name, so the output tree stays consistent anyway.
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
