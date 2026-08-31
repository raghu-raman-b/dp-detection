#!/usr/bin/env python3
"""
run_teacher_anthropic.py -- run a teacher prompt over the tuning 50 on Claude.

    python run_teacher_anthropic.py --check                offline: config, prompt, paths
    python run_teacher_anthropic.py --dry                  one live call + a caching probe
    python run_teacher_anthropic.py --actual               labels the 50
    python run_teacher_anthropic.py --actual --resume      picks up where a killed run stopped

Needs:  pip install anthropic

Same command-line surface, same output tree, same resume semantics as
run_teacher_openai.py and run_teacher_kimi.py -- the shared half lives in
runner_common.py, so a prompt ablation is driven identically whichever provider is
under test:

    python run_teacher_anthropic.py --actual --prompt ../outputs/prompts/teacher_v2_bare.txt

Sequential within a run, same as the others: the cached prefix has to be written once
before it can be read 49 times, and cold parallel workers would each pay the write.

Nine ways Claude differs. Each is marked CLAUDE DIFF below.
  1. USAGE IS CACHE-EXCLUSIVE, and this is the one that will silently corrupt a run.
     usage.input_tokens counts ONLY tokens that were neither read from nor written to
     cache -- every other provider in the bake-off reports a cache-INCLUSIVE prompt
     count. compute_run_stats.py computes cache_hit_rate as cached/input, and
     rc.print_stats and rc.CacheWatch do the same, so usage_of() below re-derives an
     inclusive input_tokens. Copy the obvious mapping instead and you get a hit rate
     around 25x too high and an understated bill, with nothing in the output looking
     wrong.
  2. THERE IS NO REASONING-TOKEN COUNT. Thinking tokens are billed inside
     output_tokens and are not broken out. reasoning_tokens is therefore hard 0, and
     meta carries reasoning_tokens_reported=false to say why. The report's
     "reasoning % of output" line reads 0% for Claude: that means NOT REPORTED, not
     "did not think", and the column must not be compared across providers.
  3. Caching is an EXPLICIT breakpoint on the system block -- no cache key, not
     automatic: system=[{type:text, text:PROMPT, cache_control:{type:ephemeral}}] with
     the review in the user message. Default TTL is 5 minutes, which is ample between
     consecutive sequential calls; --cache-ttl 1h exists for an interrupted run, but a
     1h write costs 2x a 5m write, so it is not the default.
  4. WEB SEARCH IS SERVER-SIDE with max_uses, so there is no client tool loop: the
     one-search-per-review policy is enforced by the API. The count comes from
     usage.server_tool_use.web_search_requests -- ground truth -- and NOT from the
     model's own invoked_web_search field, which is self-report on every provider.
     Server-tool errors arrive at HTTP 200, not as exceptions: on success a
     web_search_tool_result block's .content is a LIST of results, on failure it is an
     OBJECT with error_code. Branch on that before indexing it.
  5. SAMPLING PARAMETERS AND PREFILL ARE GONE. temperature, top_p, top_k and assistant
     prefill all return 400 on these models. SEND_TEMPERATURE is not an escape hatch
     here; it does not exist.
  6. Effort is output_config={"effort": ...} -- NESTED, not a top-level parameter --
     and thinking is {"type": "adaptive"}. budget_tokens is removed and 400s. The
     ladder is low|medium|high|xhigh|max, which is five of the OpenAI runner's six
     rungs, so this is the provider most directly comparable to the Luna sweep.
     thinking is deliberately never disabled: it is legal only at effort <= high, and
     with thinking off the model sometimes writes a tool call into visible text instead
     of emitting a tool_use block, which would look like a search that never happened.
  7. stop_reason HAS FIVE VALUES and three need real handling. max_tokens is normalised
     to status="incomplete" so compute_run_stats.py counts it as truncated. pause_turn
     is resumed by echoing the assistant content back UNCHANGED -- thinking blocks and
     all -- which is the same shape of trap as k3's reasoning_content echo, from the
     opposite direction. refusal is recorded with its stop_details category and NOT
     resampled: a refusal is a finding, and burning three parse-retries on one just
     buys three refusals at three prices.
  8. SERVER-SIDE REFUSAL FALLBACKS ARE OFF, deliberately. Turning them on would let a
     refused request be silently re-run on a different model inside the same call --
     meta["model"] would then name a model that did not answer the review. In a
     provider bake-off that is fatal, so USE_FALLBACKS stays False.
  9. Responses are streamed and collected with get_final_message(). Once the truncation
     bump reaches 32k a non-streaming request risks the SDK's HTTP timeout. latency_s
     therefore measures time-to-final-message, the same wall-clock quantity the other
     runners record.
  10. HAIKU 4.5 DOES NOT HAVE ADAPTIVE THINKING OR THE EFFORT PARAMETER -- both 400,
      verified live against /v1/models and a direct probe on 2026-08-22
      ('adaptive thinking is not supported on this model' / 'This model does not
      support the effort parameter'). It also can't take the dynamic-filtering search
      tool (web_search_20260209 400s with a programmatic-tool-calling error), so it
      falls back to the basic web_search_20250305 variant instead. supports_effort()
      and search_tool_type() below branch every call on the model string; a Haiku run
      thinks with an explicit token budget (thinking={"enabled", budget_tokens=N})
      instead of adaptive thinking, and sends no output_config at all. --effort is
      therefore rejected on Haiku (use --thinking-budget instead), and cfg.effort
      reads "none" in the output tree and the meta rows for those runs.

Output tree, one directory per (model, effort, prompt):

    ../outputs/runs/<model>/<effort>/<prompt_stem>/
        <tag>_responses.jsonl   raw text + parsed JSON (+ every re-attempt)
        <tag>_meta.jsonl        usage, cost, latency, status, searches, contract
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
from datetime import date, datetime
from pathlib import Path

import anthropic

sys.path.insert(0, str(Path(__file__).parent))
import runner_common as rc
from build_prompt import load_prompt

SCRIPT_DIR = Path(__file__).resolve().parent
resolve, show, payload_for = rc.resolve, rc.show, rc.payload_for

# ============================== DEFAULTS ==============================
DEFAULT_MODEL   = "claude-haiku-4-5"
DEFAULT_EFFORT  = "high"            # low | medium | high | xhigh | max  (CLAUDE DIFF 6)
                                     # -- ignored on models without effort (CLAUDE DIFF 10)
EFFORT_CHOICES  = ("low", "medium", "high", "xhigh", "max")
DEFAULT_PROMPT  = "../outputs/prompts/teacher_v2_full.txt"
# The review set and the run tree both come from --eval-set
# (runner_common.EVAL_SETS), asked interactively when the flag is omitted:
#   tuning      ../tuning/tuning_set_50_blind.jsonl      -> ../outputs/runs
#   validation  ../validation/validation_set_blind.jsonl -> ../outputs/validation/runs
# Both are blind files: no gold ever enters this process. --reviews and
# --out-root still override, for a one-off against some other file.

MAX_OUTPUT      = 8192      # thinking counts against this; too low = truncated JSON
MAX_OUTPUT_CAP  = 32768     # ceiling for the truncation bump
TRUNCATION_BUMP = 2.0

RETRIES         = 3         # transport-level attempts per call
PARSE_RETRIES   = 2         # extra attempts when the response is not parseable JSON
PROJECT_TO      = 200_000
RNG_SEED        = 20260822  # only seeds retry jitter; no effect on model sampling

# CLAUDE DIFF 4 / 10: max_uses enforces the frozen one-search-per-review policy
# server-side, so there is no client loop to cap. The tool dict must be
# BYTE-IDENTICAL on every call within a run: tools render before the cached prefix,
# so a tool list that varies kills caching for the whole run. search_tool_type() is a
# pure function of the model string, so every call in a run gets the same dict even
# though it is rebuilt each time rather than shared as a single object.
SEARCH_TOOL_TYPE_CURRENT = "web_search_20260209"   # dynamic-filtering, current-gen
SEARCH_TOOL_TYPE_BASIC   = "web_search_20250305"   # Haiku 4.5: 20260209 400s on it

# CLAUDE DIFF 10: no adaptive thinking, no effort parameter, no 20260209 search tool.
# Prefix-matched like rc.pricing_for(), so a dated build (…-20251001) still matches.
NO_EFFORT_MODELS = ("claude-haiku-4-5",)


def supports_effort(model: str) -> bool:
    return not model.startswith(NO_EFFORT_MODELS)


def search_tool_type(model: str) -> str:
    return SEARCH_TOOL_TYPE_BASIC if not supports_effort(model) else SEARCH_TOOL_TYPE_CURRENT


def web_search_tool_for(model: str) -> dict:
    return {"type": search_tool_type(model), "name": "web_search", "max_uses": 1}


# CLAUDE DIFF 3
CACHE_TTL       = "5m"      # 5m | 1h. A 1h write costs 2x a 5m write.
CACHE_MODE      = "explicit_system_block"
# The cacheable-prefix floor is 4096 tokens on Haiku 4.5 (vs 1024/512 on current-gen
# Opus/Sonnet) -- moot here since teacher_v2_full.txt runs ~24k tokens either way, but
# worth knowing before trusting a cache-hit read on a much shorter prompt.

# CLAUDE DIFF 6 / 7 / 8 / 10
MAX_PAUSE_RESUMES   = 2
USE_FALLBACKS       = False     # see CLAUDE DIFF 8. Do not turn this on for a bake-off.
STREAM              = True      # CLAUDE DIFF 9
THINKING_BUDGET_DEFAULT = 4096  # budget_tokens for NO_EFFORT_MODELS; must be < max_tokens


def thinking_kwargs_for(model: str, thinking_budget: int, max_output: int) -> dict:
    """CLAUDE DIFF 6 / 10: adaptive thinking + effort on current-gen models; Haiku 4.5
    thinks the older way, with an explicit budget that must stay under max_tokens."""
    if supports_effort(model):
        return {"type": "adaptive"}
    budget = max(1024, min(thinking_budget, max_output - 1))
    return {"type": "enabled", "budget_tokens": budget}

API_KEY_ENV     = "ANTHROPIC_API_KEY"
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
    limit: int
    only: set
    max_spend: float
    cache_ttl: str = CACHE_TTL
    max_pause_resumes: int = MAX_PAUSE_RESUMES
    thinking_budget: int = THINKING_BUDGET_DEFAULT   # CLAUDE DIFF 10: NO_EFFORT_MODELS only
    prompt: str = ""
    prompt_sha: str = ""
    legal_codes: set = field(default_factory=set)
    pricing: dict = field(default_factory=dict)
    paths: rc.RunPaths | None = None

    @property
    def cache_control(self) -> dict:
        cc = {"type": "ephemeral"}
        if self.cache_ttl != "5m":
            cc["ttl"] = self.cache_ttl
        return cc


def build_config(a: argparse.Namespace) -> RunConfig:
    # CLAUDE DIFF 10: --effort has no target on a NO_EFFORT_MODELS model -- resolve it
    # here rather than in argparse, since the right default depends on --model.
    if a.effort is None:
        effort = DEFAULT_EFFORT if supports_effort(a.model) else "none"
    elif not supports_effort(a.model):
        sys.exit(f"--effort has no effect on {a.model}: it has no effort parameter "
                 f"(CLAUDE DIFF 10). Drop --effort and use --thinking-budget instead.")
    else:
        effort = a.effort

    cfg = RunConfig(
        model=a.model, effort=effort,
        prompt_file=resolve(a.prompt), reviews_file=resolve(a.reviews),
        eval_set=a.eval_set,
        out_root=resolve(a.out_root), web_search=not a.no_web_search,
        max_output=a.max_output, parse_retries=a.parse_retries, retries=a.retries,
        limit=a.limit,
        only={s.strip() for s in a.only.split(",") if s.strip()} if a.only else set(),
        max_spend=a.max_spend, cache_ttl=a.cache_ttl,
        max_pause_resumes=a.max_pause_resumes, thinking_budget=a.thinking_budget,
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


def get_client() -> "anthropic.Anthropic":
    """max_retries=0 hands the retry policy back to rc.call_with_retries. The SDK
    retries twice of its own accord by default, which would nest two uncoordinated
    backoff schedules inside one rc attempt and under-report counters['retried']."""
    return anthropic.Anthropic(
        api_key=rc.load_api_key(API_KEY_ENV, SCRIPT_DIR, ENV_FILE),
        max_retries=0, timeout=600.0)


def check_pricing_freshness(cfg: RunConfig) -> None:
    """A promotional rate with an expiry in the table is a trap for a re-run: the code
    keeps quoting it long after it stopped being true."""
    until = cfg.pricing.get("intro_until")
    if until and date.today().isoformat() > until:
        print(f"!! PRICING: {cfg.model}'s promotional rate expired on {until}, but "
              f"PRICING_TABLE still carries it.")
        print(f"   list rates are in/out ${cfg.pricing.get('list_input')} / "
              f"${cfg.pricing.get('list_output')} per MTok.")
        print(f"   Update runner_common.py before trusting this run's cost numbers.")


# --------------------------------------------------------------------- the call

def build_kwargs(cfg: RunConfig, user_input: str, max_output: int,
                 cached: bool = True, assistant: list | None = None) -> dict:
    """CLAUDE DIFF 3/5/6/10. Note what is NOT here: no temperature, no top_p, no
    prefill -- all 400s on these models regardless of which one. budget_tokens IS
    sent, but only on NO_EFFORT_MODELS (Haiku 4.5); output_config is the opposite --
    sent only on models that support effort. Sending both on the same call, or either
    on the wrong model family, 400s."""
    system = [{"type": "text", "text": cfg.prompt}]
    if cached:
        system[0]["cache_control"] = cfg.cache_control

    messages = [{"role": "user", "content": user_input}]
    if assistant:
        # CLAUDE DIFF 7: a pause_turn resume echoes the assistant content back
        # UNCHANGED -- thinking blocks, server_tool_use blocks and all. Filtering it
        # down to the text blocks loses the model's own state and the turn restarts
        # rather than continuing.
        messages.append({"role": "assistant", "content": assistant})

    kw = {
        "model": cfg.model,
        "max_tokens": max_output,
        "system": system,
        "messages": messages,
        "thinking": thinking_kwargs_for(cfg.model, cfg.thinking_budget, max_output),
    }
    if supports_effort(cfg.model):
        kw["output_config"] = {"effort": cfg.effort}   # CLAUDE DIFF 6: nested
    if cfg.web_search:
        kw["tools"] = [web_search_tool_for(cfg.model)]  # byte-identical every call
    return kw


def usage_of(resp) -> dict:
    """CLAUDE DIFF 1 -- the load-bearing function in this file.

    Anthropic's usage.input_tokens EXCLUDES both cache reads and cache writes. Every
    other runner reports a cache-inclusive prompt count, and cached/input is computed
    downstream in three places, so input_tokens is re-derived as the sum here. The
    three buckets stay disjoint, which is what rc.cost_usd bills on."""
    u = resp.usage
    cr = getattr(u, "cache_read_input_tokens", 0) or 0
    cw = getattr(u, "cache_creation_input_tokens", None)
    if cw is None:
        # newer builds break the write out by TTL instead of totalling it
        cc = getattr(u, "cache_creation", None)
        cw = ((getattr(cc, "ephemeral_5m_input_tokens", 0) or 0) +
              (getattr(cc, "ephemeral_1h_input_tokens", 0) or 0)) if cc else 0
    cw = cw or 0
    plain = u.input_tokens or 0                  # EXCLUSIVE of cr and cw
    out = u.output_tokens or 0
    return {
        "input_tokens": plain + cr + cw,         # inclusive, for the /input divides
        "cached_tokens": cr,
        "cache_write_tokens": cw,
        "uncached_input_tokens": plain,          # cr + cw + plain == input_tokens
        "output_tokens": out,
        "reasoning_tokens": 0,                   # CLAUDE DIFF 2: not reported
        "total_tokens": plain + cr + cw + out,
    }


def text_of(resp) -> str:
    """Text blocks ONLY. A response can also carry thinking blocks and server-tool
    blocks; concatenating those into the JSON payload would guarantee a parse failure."""
    return "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")


def searches_of(resp) -> list:
    """CLAUDE DIFF 4. Queries come from the server_tool_use blocks; the authoritative
    COUNT comes from usage (see response_meta). Errors arrive at HTTP 200 inside the
    result block, so success and failure are told apart by the shape of .content:
    a list of results on success, an object with error_code on failure."""
    out = []
    for b in resp.content:
        t = getattr(b, "type", "")
        if t == "server_tool_use" and getattr(b, "name", "") == "web_search":
            inp = getattr(b, "input", None) or {}
            if not isinstance(inp, dict):
                inp = {}
            out.append({"query": inp.get("query"), "error": None, "n_results": None})
        elif t == "web_search_tool_result":
            content = getattr(b, "content", None)
            if isinstance(content, list):
                if out:
                    out[-1]["n_results"] = len(content)
            else:
                code = getattr(content, "error_code", None) or "unknown_error"
                if out:
                    out[-1]["error"] = code
                else:
                    out.append({"query": None, "error": code, "n_results": None})
    return out


def response_meta(resp, n_pause_resumes: int = 0) -> dict:
    """CLAUDE DIFF 7: normalise stop_reason into the `status` vocabulary the scorer
    speaks. compute_run_stats.py counts status=="incomplete" as truncated; leaving raw
    stop reasons in that field silently reports zero truncations forever."""
    stop = getattr(resp, "stop_reason", None)
    status = {"max_tokens": "incomplete", "refusal": "refusal",
              "pause_turn": "paused", "tool_use": "tool_use"}.get(stop, "completed")
    stu = getattr(resp.usage, "server_tool_use", None)
    n_search = getattr(stu, "web_search_requests", 0) if stu else 0
    det = getattr(resp, "stop_details", None)      # populated ONLY on refusal
    return {
        "response_id": getattr(resp, "id", None),
        "model_version": getattr(resp, "model", None),
        "status": status,
        "stop_reason": stop,
        "incomplete_reason": "max_tokens" if status == "incomplete" else None,
        "refusal_category": getattr(det, "category", None) if det else None,
        "refusal_explanation": getattr(det, "explanation", None) if det else None,
        "n_web_searches": n_search or 0,
        "n_pause_resumes": n_pause_resumes,
        "reasoning_tokens_reported": False,        # CLAUDE DIFF 2
        "cache_mode": CACHE_MODE,
    }


def one_call(client, cfg: RunConfig, user_input: str, max_output: int,
             rng: random.Random, cached: bool = True, assistant: list | None = None):
    """A single API call with retries. Returns (response, latency, etype, emsg).
    CLAUDE DIFF 9: streamed, then collected."""
    def fire():
        kw = build_kwargs(cfg, user_input, max_output, cached, assistant)
        if not STREAM:
            return client.messages.create(**kw)
        with client.messages.stream(**kw) as stream:
            return stream.get_final_message()

    return rc.call_with_retries(fire, cfg.retries, rng)


def run_review(client, cfg: RunConfig, user_input: str, max_output: int,
               rng: random.Random, cached: bool = True):
    """One review, including any pause_turn resumes.

    Returns (text, usage, latency, n_calls, searches, status, resp, etype, emsg).
    There is no tool loop here -- CLAUDE DIFF 4, web search runs server-side -- so the
    only reason this makes more than one call is a paused turn."""
    usage: dict = {}
    searches: list = []
    total_latency = 0.0
    n_calls = 0
    assistant = None
    resp = None

    for resumes in range(cfg.max_pause_resumes + 1):
        resp, lat, etype, emsg = one_call(client, cfg, user_input, max_output, rng,
                                          cached, assistant)
        total_latency += lat
        n_calls += 1
        if etype:
            return None, usage, total_latency, n_calls, searches, None, None, etype, emsg

        usage = rc.add_usage(usage, usage_of(resp))
        searches += searches_of(resp)

        if getattr(resp, "stop_reason", None) != "pause_turn":
            break
        # CLAUDE DIFF 7: hand the model's own content back verbatim and let it continue.
        assistant = resp.content
        if resumes == cfg.max_pause_resumes:
            print(f"       still paused after {resumes + 1} resumes -- taking what we have")

    meta = response_meta(resp, n_pause_resumes=n_calls - 1)
    # usage is summed across resumes, but server_tool_use on the last response only
    # covers that response, so recount searches from the blocks we actually collected.
    meta["n_web_searches"] = max(meta["n_web_searches"], len(searches))
    return (text_of(resp), usage, total_latency, n_calls, searches,
            meta["status"], meta, None, None)


def label_review(client, cfg: RunConfig, row: dict, rng: random.Random,
                 watch: rc.CacheWatch) -> dict:
    """Label one review, re-attempting while the response will not parse as JSON.

    Two distinct failure modes hide behind "unparseable", and they need different
    answers. A response that got cut off mid-object (status="incomplete") will be cut
    off again at the same budget no matter how many times it is resampled -- that one
    gets a bigger max_tokens. A response that merely wrapped the object in prose is a
    sampling accident, and an identical resample usually clears it.

    A REFUSAL is a third thing and is not retried at all (CLAUDE DIFF 7): the model
    declined, and resampling only buys the same decline at three times the price.

    Every attempt is kept, and every attempt's usage is summed into the returned total:
    a re-attempt costs real money, and a per-review cost that ignores it understates the
    projection at 200k."""
    review_text = row.get("review_text", "")
    payload = payload_for(row)
    attempts: list = []
    usage_total: dict = {}
    latency_total = 0.0
    n_calls = 0
    all_searches: list = []
    max_out = cfg.max_output
    rmeta = None
    status = None

    def result(**kw) -> dict:
        base = {"api_error_type": None, "api_error_message": None,
                "attempts": attempts, "usage": usage_total,
                "latency_s": latency_total, "n_calls": n_calls,
                "n_searches": len(all_searches), "searches": all_searches,
                "status": status, "rmeta": rmeta, "parsed": None, "raw": None,
                "parse_note": None, "contract": None}
        return base | kw

    for k in range(cfg.parse_retries + 1):
        text, u, lat, calls, searches, status, rmeta, etype, emsg = run_review(
            client, cfg, payload, max_out, rng)
        latency_total += lat
        n_calls += calls
        all_searches += searches
        if etype:
            return result(api_error_type=etype, api_error_message=emsg,
                          usage=rc.add_usage(usage_total, u) if u else usage_total,
                          status=None)

        usage_total = rc.add_usage(usage_total, u)
        watch.observe(u)
        parsed, note = rc.parse_json(text)
        attempts.append({"n": k + 1, "max_output": max_out, "status": status,
                         "parse_note": note, "latency_s": round(lat, 2),
                         "n_api_calls": calls, "usage": u, "raw": text,
                         "search_queries": [s["query"] for s in searches]})

        if parsed is not None:
            return result(parsed=parsed, raw=text, parse_note=note,
                          contract=rc.check_contract(parsed, review_text,
                                                     cfg.legal_codes))

        if status == "refusal":
            # CLAUDE DIFF 7: a decision, not a transport failure. Stop here.
            print(f"       REFUSAL ({rmeta.get('refusal_category')}) -- not resampling")
            return result(raw=text, parse_note="refusal")

        if k < cfg.parse_retries:
            if status == "incomplete" and max_out < MAX_OUTPUT_CAP:
                bumped = min(int(max_out * TRUNCATION_BUMP), MAX_OUTPUT_CAP)
                print(f"       truncated at max_tokens={max_out:,} -> retrying at {bumped:,}")
                max_out = bumped
            else:
                print(f"       unparseable JSON -> resample {k + 2}/{cfg.parse_retries + 1}")

    # Out of attempts. This is NOT an api error: the calls succeeded and were billed,
    # the model just would not emit JSON.
    return result(raw=attempts[-1]["raw"], parse_note="parse_failed")


# ---------------------------------------------------------------------- preflight

def preflight(cfg: RunConfig, rows: list, done: set) -> None:
    man = rc.prompt_manifest(cfg.prompt_file)
    p = cfg.pricing
    think = thinking_kwargs_for(cfg.model, cfg.thinking_budget, cfg.max_output)
    think_str = (think["type"] if think["type"] == "adaptive"
                 else f"{think['type']} (budget={think['budget_tokens']:,})")
    print("=" * 72)
    print(f"model          {cfg.model}   "
          f"effort={cfg.effort if supports_effort(cfg.model) else 'n/a (CLAUDE DIFF 10)'}   "
          f"web_search={cfg.web_search}   thinking={think_str}")
    print(f"pricing        in ${p['input']} / cached ${p['cached_input']} / "
          f"write ${p['cache_write']} / out ${p['output']} per MTok "
          f"+ ${p.get('search_per_call', 0)}/search   (as of {p['as_of']})")
    check_pricing_freshness(cfg)
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
    print(f"cache          {CACHE_MODE}, ttl={cfg.cache_ttl} "
          f"(CLAUDE DIFF 3: breakpoint on the system block)")
    print(f"search         {search_tool_type(cfg.model)} max_uses="
          f"{web_search_tool_for(cfg.model)['max_uses']}"
          if cfg.web_search else "search         off")
    print(f"budget         max_tokens={cfg.max_output:,} (bump to {MAX_OUTPUT_CAP:,} on "
          f"truncation)  parse_retries={cfg.parse_retries}")
    print(f"               fallbacks={USE_FALLBACKS} (CLAUDE DIFF 8), "
          f"pause_resumes<={cfg.max_pause_resumes}, stream={STREAM}")
    if cfg.max_spend:
        print(f"spend guard    stop above ${cfg.max_spend:g}")
    print(f"output         {show(cfg.paths.dir)}/")
    print("=" * 72)


# --------------------------------------------------------------- dry run

def dry_run(cfg: RunConfig) -> None:
    rng = random.Random(RNG_SEED)
    client = get_client()
    rows = rc.select_reviews(cfg.reviews_file, cfg.only, cfg.limit)
    preflight(cfg, rows, set())

    # --- stage 1: does the API work, and does the server-side tool fire? ---
    print("\n[1/2] throwaway call with search (short prompt, below the cache floor)...")
    probe_cfg = RunConfig(**{**cfg.__dict__,
                             "prompt": "You are a helpful assistant. Answer in one sentence."})
    text, u, lat, n_calls, searches, status, rmeta, etype, emsg = run_review(
        client, probe_cfg, "What is a welkin pass in Genshin Impact? Search first.",
        cfg.max_output, rng, cached=False)
    if etype:
        print(f"\nFAILED: {etype}: {emsg}\nFix the arguments and rerun --dry.")
        sys.exit(1)
    print(f"  api calls    {n_calls}  (>1 means a paused turn was resumed)")
    print(f"  status       {status}  (stop_reason={rmeta['stop_reason']})")
    print(f"  text         {(text or '')[:200]!r}")
    print(f"  searches     {rmeta['n_web_searches']} per usage; "
          f"queries {[s['query'] for s in searches] or 'none'}")
    for s in searches:
        if s["error"]:
            print(f"  !! search error at HTTP 200: {s['error']} (CLAUDE DIFF 4)")
    rc.print_stats("  stage1", u, lat)

    # --- stage 2: does the explicit breakpoint cache? two identical-prefix calls. ---
    print("\n[2/2] explicit-cache check: two calls with the real prompt...")
    for n in (1, 2):
        text2, u2, lat2, nc2, s2, st2, rm2, e2, m2 = run_review(
            client, cfg, payload_for(rows[0]), cfg.max_output, rng)
        if e2:
            print(f"\nFAILED on cache probe: {e2}: {m2}")
            sys.exit(1)
        rc.print_stats(f"  call {n}", u2, lat2)
        # CLAUDE DIFF 1 made visible before 50 reviews are paid for.
        print(f"           reconcile: plain {u2['uncached_input_tokens']:,} "
              f"+ read {u2['cached_tokens']:,} + write {u2['cache_write_tokens']:,} "
              f"= {u2['input_tokens']:,}  "
              f"{'OK' if u2['uncached_input_tokens'] + u2['cached_tokens'] + u2['cache_write_tokens'] == u2['input_tokens'] else '!! MISMATCH'}")
        if n == 2:
            hit = u2["cached_tokens"] / max(u2["input_tokens"], 1)
            parsed, note = rc.parse_json(text2)
            print()
            if hit > 0.8:
                print(f"  CACHING OK: {hit:.0%} of input read from cache on the second call.")
            elif hit > 0.3:
                print(f"  CACHING PARTIAL: {hit:.0%}. Check the tool list and the system")
                print("  block are byte-identical between the two calls.")
            else:
                print(f"  CACHING BROKEN: only {hit:.0%} cached on call 2. Check:")
                print("   - the prompt body only (load_prompt strips the build-log header)")
                print("   - cache_control is on the system block, not the user message")
                print("   - the tools list is the module constant, not rebuilt per call")
                print("   - the prefix is over ~1024 tokens (it is, at ~24k)")
            print(f"  parsed JSON on probe: {note}")
            if parsed is not None:
                errs = rc.contract_errors(
                    rc.check_contract(parsed, rows[0].get("review_text", ""),
                                      cfg.legal_codes))
                print(f"  contract: {'OK' if not errs else '; '.join(errs)}")
            per = rc.cost_usd(u2, cfg.pricing, rm2["n_web_searches"])["total"]
            print(f"  output tokens {u2['output_tokens']:,} "
                  f"(thinking is inside this; CLAUDE DIFF 2) <- this sets the bill")
            print(f"  ~${per:.6f}/review  ->  ~${per * len(rows):.4f} for {len(rows)} "
                  f"reviews  ->  ~${per * PROJECT_TO:,.0f} at {PROJECT_TO:,}")

    print(f"\nIf caching is OK and the JSON parsed, run:\n"
          f"  python run_teacher_anthropic.py --actual --model {cfg.model} "
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

    n_super = rc.supersede(paths, {r.get("review_id") for r in todo})
    if n_super:
        print(f"superseding {n_super} failed row(s) from the previous pass")
    counters, spend, all_usage = rc.prior_state(paths)
    _, state = rc.load_progress(paths)
    started = state.get("started") or datetime.now().isoformat(timespec="seconds")
    watch = rc.CacheWatch()
    f_resp = open(paths.responses, "a", encoding="utf-8")
    f_meta = open(paths.meta, "a", encoding="utf-8")
    n_extra_calls = int(state.get("extra_pause_calls", 0))

    def save(complete: bool) -> None:
        rc.write_checkpoint(paths, {
            "tag": paths.tag, "model": cfg.model, "reasoning_effort": cfg.effort,
            "prompt_file": str(cfg.prompt_file), "prompt_sha256": cfg.prompt_sha,
            "eval_set": cfg.eval_set, "reviews_file": str(cfg.reviews_file), "n_selected": len(rows),
            "started": started, "complete": complete, "spend_usd": round(spend, 6),
            "extra_pause_calls": n_extra_calls, **counters})

    print(f"\n{len(todo)} reviews to label -> {show(paths.responses)}\n")
    stopped = None
    try:
        for i, row in enumerate(todo, 1):
            rid = str(uuid.uuid4())
            res = label_review(client, cfg, row, rng, watch)

            u = res["usage"]
            rmeta = res["rmeta"] or {}
            n_search = rmeta.get("n_web_searches", res["n_searches"])
            cost = rc.cost_usd(u, cfg.pricing, n_search) if u else {"total": 0.0}
            spend += cost["total"]
            n_att = len(res["attempts"])
            counters["extra_attempts"] += max(n_att - 1, 0)
            counters["retried"] += n_att > 1
            n_extra_calls += max(res["n_calls"] - n_att, 0)
            truncated = res["status"] == "incomplete"
            refused = res["status"] == "refusal"
            failed_parse = res["parsed"] is None and not res["api_error_type"]

            meta = {"request_id": rid, "review_id": row.get("review_id"),
                    "ts": datetime.now().isoformat(timespec="seconds"),
                    "provider": "anthropic", "model": cfg.model,
                    "reasoning_effort": cfg.effort,
                    "thinking": ("adaptive" if supports_effort(cfg.model) else "enabled"),
                    # CLAUDE DIFF 10: only meaningful (non-None) on NO_EFFORT_MODELS.
                    "thinking_budget": (None if supports_effort(cfg.model)
                                        else cfg.thinking_budget),
                    "prompt_file": str(cfg.prompt_file), "prompt_sha256": cfg.prompt_sha,
                    "cache_mode": CACHE_MODE, "cache_ttl": cfg.cache_ttl,
                    # CLAUDE DIFF 5: there is no temperature to record. Saying so is
                    # better than an absent key that reads as "forgot to log it".
                    "temperature": "unsupported",
                    "fallbacks": USE_FALLBACKS,
                    "web_search": cfg.web_search,
                    "web_search_channel": search_tool_type(cfg.model) if cfg.web_search else None,
                    "max_uses": web_search_tool_for(cfg.model)["max_uses"],
                    "pricing": cfg.pricing,
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
                meta |= dict(rmeta)
                meta |= {"search_queries": [s["query"] for s in res["searches"]],
                         "search_errors": [s["error"] for s in res["searches"]
                                           if s["error"]],
                         "parse_note": res["parse_note"]}

                if refused:
                    counters["refusals"] += 1
                    counters["parse_failures"] += 1
                    rc.print_stats(f"[{i:>2}/{len(todo)}] {'REFUSAL':<16}", u,
                                   res["latency_s"])
                    print(f"       category={rmeta.get('refusal_category')}  "
                          f"${cost['total']:.6f}  running ${spend:.4f}")
                elif res["parsed"] is None:
                    counters["parse_failures"] += 1
                    rc.print_stats(f"[{i:>2}/{len(todo)}] {'PARSE FAILED':<16}", u,
                                   res["latency_s"])
                    print(f"       gave up after {n_att} attempts  ${cost['total']:.6f}  "
                          f"running ${spend:.4f}")
                else:
                    counters["ok"] += 1
                    counters["parsed"] += 1
                    counters["truncated"] += truncated
                    counters["searched"] += n_search > 0
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
                                   res["latency_s"])
                    print(f"       ${cost['total']:.6f}  running ${spend:.4f}  "
                          f"labels={meta['n_labels']}  searches={n_search}  "
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
    if counters["refusals"]:
        print(f"\n!! {counters['refusals']} refusal(s). compare_runs.py gates on a parse")
        print(f"   rate of 1.00, so this run will not be ranked. That is a finding about")
        print(f"   the teacher, not a bug -- report it rather than resampling it away.")
    rc.summarize(paths, counters, spend, all_usage, cfg.pricing, PROJECT_TO, extra={
        "complete": stopped is None, "stopped_because": stopped,
        "started": started, "provider": "anthropic",
        "model": cfg.model, "reasoning_effort": cfg.effort,
        "thinking": ("adaptive" if supports_effort(cfg.model) else "enabled"),
        "thinking_budget": None if supports_effort(cfg.model) else cfg.thinking_budget,
        "web_search": cfg.web_search,
        "web_search_channel": search_tool_type(cfg.model) if cfg.web_search else None,
        "cache_mode": CACHE_MODE, "cache_ttl": cfg.cache_ttl,
        "temperature": "unsupported", "fallbacks": USE_FALLBACKS,
        "reasoning_tokens_reported": False,        # CLAUDE DIFF 2
        "prompt_file": str(cfg.prompt_file), "prompt_sha256": cfg.prompt_sha,
        "eval_set": cfg.eval_set, "reviews_file": str(cfg.reviews_file),
        "max_output": cfg.max_output, "parse_retries": cfg.parse_retries,
        "extra_pause_calls": n_extra_calls,
        "manifest": rc.run_manifest(cfg.prompt_file, __file__),
    })

    if stopped:
        print(f"\nSTOPPED: {stopped}")
        print(f"  resume with:  python run_teacher_anthropic.py --actual --resume "
              f"--model {cfg.model} --effort {cfg.effort} --prompt {show(cfg.prompt_file)}")
        sys.exit(2)
    print(f"\nnext: python compute_run_stats.py --run-dir {show(paths.dir)}")


# --------------------------------------------------------------------------- cli

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Run a teacher prompt over a review set on Claude.",
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
    ap.add_argument("--effort", default=None, choices=list(EFFORT_CHOICES),
                    help=f"CLAUDE DIFF 6: nested in output_config; defaults to "
                         f"{DEFAULT_EFFORT!r} on models that support it. CLAUDE DIFF "
                         f"10: rejected on Haiku 4.5 -- it has no effort parameter, "
                         f"use --thinking-budget there instead")
    ap.add_argument("--thinking-budget", type=int, default=THINKING_BUDGET_DEFAULT,
                    help="CLAUDE DIFF 10: budget_tokens for models with no adaptive "
                         "thinking/effort (Haiku 4.5) -- ignored on every other "
                         "model. Must be < max_tokens, min 1024")
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
    ap.add_argument("--parse-retries", type=int, default=PARSE_RETRIES,
                    help="extra attempts when the response will not parse as JSON")
    ap.add_argument("--retries", type=int, default=RETRIES,
                    help="transport-level attempts per call")
    ap.add_argument("--no-web-search", action="store_true")
    ap.add_argument("--cache-ttl", default=CACHE_TTL, choices=("5m", "1h"),
                    help="CLAUDE DIFF 3: a 1h write costs 2x a 5m write")
    ap.add_argument("--max-pause-resumes", type=int, default=MAX_PAUSE_RESUMES,
                    help="how many times a pause_turn is resumed before giving up")

    a = ap.parse_args()
    if a.resume and a.overwrite:
        ap.error("--resume and --overwrite are opposites; pick one")

    # --eval-set picks the review file and the run tree together. Keeping them
    # in one switch is what stops a validation run landing in the tuning tree.
    a.eval_set = rc.resolve_eval_set(a.eval_set, what="label")
    _sel = rc.EVAL_SETS[a.eval_set]
    a.reviews = a.reviews or _sel["reviews"]
    a.out_root = a.out_root or _sel["runs"]
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
