#!/usr/bin/env python3
"""
run_teacher_openai.py -- run a teacher prompt over the tuning 50 on an OpenAI model.

    python run_teacher_openai.py --check                     offline: config, prompt, cost estimate
    python run_teacher_openai.py --dry                       one live call + a caching probe
    python run_teacher_openai.py --actual                    labels the 50
    python run_teacher_openai.py --actual --resume           picks up where a killed run stopped

The three axes of the ablation are command-line arguments, not constants, so the same
checkout can run three prompts at once in three terminals:

    python run_teacher_openai.py --actual --prompt ../outputs/prompts/teacher_v2_bare.txt
    python run_teacher_openai.py --actual --prompt ../outputs/prompts/teacher_v2_boundary.txt
    python run_teacher_openai.py --actual --prompt ../outputs/prompts/teacher_v2_full.txt

Those three do not fight over the cache: the cache key is derived from the prompt SHA,
so each process warms and reads its own prefix.

Sequential within a run, on purpose: the first call writes the cached prefix and every
later call reads it. Parallel workers launched cold would all miss at once and each pay
a cache write.

Output tree, one directory per (model, effort, prompt):

    ../outputs/runs/<model>/<effort>/<prompt_stem>/
        <tag>_responses.jsonl   raw text + parsed JSON (+ every re-attempt)
        <tag>_meta.jsonl        usage, cost, latency, status, contract errors
        <tag>_summary.json      scoreboard row + run manifest
        checkpoint.json         progress, for --resume

Re-running a config OVERWRITES it. An interrupted run is the exception: its checkpoint
is detected and the run refuses to start until you pick --resume or --overwrite, so a
half-finished 50 is never silently thrown away.
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

from openai import OpenAI

sys.path.insert(0, str(Path(__file__).parent))
import runner_common as rc
from build_prompt import load_prompt

SCRIPT_DIR = Path(__file__).resolve().parent

# ============================== DEFAULTS ==============================
# All of these are argparse defaults now. Edit for a new standing default; override on
# the command line for one run.
DEFAULT_MODEL   = "gpt-5.6-luna"    # see runner_common.PRICING_TABLE for what is priced
DEFAULT_EFFORT  = "high"            # none | low | medium | high | xhigh | max
DEFAULT_PROMPT  = "../outputs/prompts/teacher_v2_full.txt"
DEFAULT_REVIEWS = "../tuning/tuning_set_50_blind.jsonl"   # blind: no gold in this process
OUT_ROOT        = "../outputs/runs"

MAX_OUTPUT      = 8192      # reasoning tokens count against this; too low = empty output
MAX_OUTPUT_CAP  = 32768     # ceiling for the truncation bump below
TRUNCATION_BUMP = 2.0       # multiplier applied when a parse failure was a truncation

RETRIES         = 3         # transport-level attempts per call
PARSE_RETRIES   = 2         # extra attempts when the response is not parseable JSON
SEND_TEMPERATURE = False    # True only if the model accepts it
TEMPERATURE     = 0.0
PROJECT_TO      = 200_000   # for the end-of-run projection
RNG_SEED        = 20260822  # only seeds retry jitter; no effect on model sampling

WEB_SEARCH_TOOL = {"type": "web_search"}

# GPT-5.6 caching: the implicit breakpoint sits on the LATEST USER MESSAGE, which is a
# different review every call. Without an explicit breakpoint the prefix never matches and
# every request pays a 1.25x cache write. So: prompt goes in a developer message with an
# explicit breakpoint, explicit-only mode stops the review suffix being cached, and a
# stable prompt_cache_key routes requests to the same cache.
CACHE_MODE       = "explicit"      # "explicit" | "implicit"
CACHE_KEY_PREFIX = "dp-teacher"    # prompt sha is appended automatically

API_KEY_ENV      = "OPENAI_API_KEY"
ENV_FILE         = ".env"          # optional: KEY=value lines, gitignored
# ======================================================================


resolve, show = rc.resolve, rc.show


# ------------------------------------------------------------------ run config

@dataclass
class RunConfig:
    """One run, fully resolved. Passed explicitly everywhere instead of living in module
    globals -- once the axes come from argparse, mutating globals is how a run ends up
    reporting one model's name against another model's pricing."""
    model: str
    effort: str
    prompt_file: Path
    reviews_file: Path
    out_root: Path
    web_search: bool
    max_output: int
    parse_retries: int
    retries: int
    limit: int
    only: set[str]
    max_spend: float
    prompt: str = ""
    prompt_sha: str = ""
    legal_codes: set[str] = field(default_factory=set)
    pricing: dict = field(default_factory=dict)
    paths: rc.RunPaths | None = None

    @property
    def cache_key(self) -> str:
        return f"{CACHE_KEY_PREFIX}-{self.prompt_sha[:12]}"


def build_config(a: argparse.Namespace) -> RunConfig:
    cfg = RunConfig(
        model=a.model,
        effort=a.effort,
        prompt_file=resolve(a.prompt),
        reviews_file=resolve(a.reviews),
        out_root=resolve(a.out_root),
        web_search=not a.no_web_search,
        max_output=a.max_output,
        parse_retries=a.parse_retries,
        retries=a.retries,
        limit=a.limit,
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


def load_reviews(cfg: RunConfig) -> list[dict]:
    return rc.select_reviews(cfg.reviews_file, cfg.only, cfg.limit)


payload_for = rc.payload_for


# --------------------------------------------------------------------- the call

def build_kwargs(cfg: RunConfig, user_input: str, max_output: int,
                 cached: bool = True) -> dict:
    """cached=True puts the prompt in a developer message with an explicit breakpoint.
    cached=False is for the throwaway dry-run call (too short to cache anyway)."""
    if not cached:
        return {"model": cfg.model, "instructions": cfg.prompt, "input": user_input,
                "max_output_tokens": max_output,
                **({"reasoning": {"effort": cfg.effort}} if cfg.effort else {}),
                **({"tools": [WEB_SEARCH_TOOL]} if cfg.web_search else {})}

    kw = {
        "model": cfg.model,
        "max_output_tokens": max_output,
        "prompt_cache_key": cfg.cache_key,
        "prompt_cache_options": {"mode": CACHE_MODE},
        "input": [
            {"type": "message", "role": "developer", "content": [
                {"type": "input_text", "text": cfg.prompt,
                 "prompt_cache_breakpoint": {"mode": "explicit"}}]},
            {"type": "message", "role": "user", "content": [
                {"type": "input_text", "text": user_input}]},
        ],
    }
    if cfg.effort:
        kw["reasoning"] = {"effort": cfg.effort}
    if cfg.web_search:
        kw["tools"] = [WEB_SEARCH_TOOL]      # tools render before the prefix: keep identical
    if SEND_TEMPERATURE:
        kw["temperature"] = TEMPERATURE
    return kw


def usage_dict(resp) -> dict:
    u = resp.usage
    d = getattr(u, "input_tokens_details", None)
    cached = getattr(d, "cached_tokens", 0) or 0
    written = getattr(d, "cache_write_tokens", 0) or 0
    reasoning = getattr(getattr(u, "output_tokens_details", None), "reasoning_tokens", 0) or 0
    return {
        "input_tokens": u.input_tokens,
        "cached_tokens": cached,
        "cache_write_tokens": written,           # 1.25x rate on 5.6+; should be ~0 after call 1
        "uncached_input_tokens": u.input_tokens - cached - written,
        "output_tokens": u.output_tokens,
        "reasoning_tokens": reasoning,
        "total_tokens": getattr(u, "total_tokens", None),
    }


def response_meta(resp) -> dict:
    """Fields worth keeping beyond usage. `status` matters most: if reasoning eats
    max_output_tokens the response comes back incomplete with truncated JSON."""
    inc = getattr(resp, "incomplete_details", None)
    return {
        "response_id": resp.id,
        "model_version": resp.model,
        "created_at": getattr(resp, "created_at", None),
        "status": getattr(resp, "status", None),
        "incomplete_reason": getattr(inc, "reason", None) if inc else None,
        "service_tier": getattr(resp, "service_tier", None),
        "tool_calls": [it.type for it in resp.output if getattr(it, "type", "") != "message"],
        "n_web_searches": sum(1 for it in resp.output
                              if getattr(it, "type", "") == "web_search_call"),
    }


def call(client, cfg: RunConfig, user_input: str, rng: random.Random,
         max_output: int | None = None, cached: bool = True):
    """One API call with transport retries. Returns (response, latency, etype, emsg)."""
    mo = max_output or cfg.max_output
    return rc.call_with_retries(
        lambda: client.responses.create(**build_kwargs(cfg, user_input, mo, cached)),
        cfg.retries, rng)


def label_review(client, cfg: RunConfig, row: dict, rng: random.Random,
                 watch: rc.CacheWatch) -> dict:
    """Label one review, re-attempting while the response will not parse as JSON.

    Two distinct failure modes hide behind "unparseable", and they need different
    answers. A response that got cut off mid-object (status=incomplete) will be cut off
    again at the same budget no matter how many times it is resampled -- that one gets a
    bigger max_output. A response that merely wrapped the object in prose is a sampling
    accident, and an identical resample usually clears it.

    Every attempt is kept, and every attempt's usage is summed into the returned total:
    a re-attempt costs real money, and a per-review cost that ignores it understates the
    projection at 200k."""
    review_text = row.get("review_text", "")
    payload = payload_for(row)
    attempts: list[dict] = []
    usage_total: dict = {}
    latency_total = 0.0
    n_searches = 0
    max_out = cfg.max_output

    for k in range(cfg.parse_retries + 1):
        resp, lat, etype, emsg = call(client, cfg, payload, rng, max_output=max_out)
        latency_total += lat
        if etype:
            return {"api_error_type": etype, "api_error_message": emsg,
                    "attempts": attempts, "usage": usage_total,
                    "latency_s": latency_total, "n_searches": n_searches,
                    "parsed": None, "raw": None, "parse_note": None,
                    "rmeta": {}, "contract": None}

        u = usage_dict(resp)
        usage_total = rc.add_usage(usage_total, u)
        watch.observe(u)
        rmeta = response_meta(resp)
        n_searches += rmeta["n_web_searches"]
        text = resp.output_text
        parsed, note = rc.parse_json(text)
        attempts.append({"n": k + 1, "max_output": max_out, "status": rmeta["status"],
                         "incomplete_reason": rmeta["incomplete_reason"],
                         "parse_note": note, "latency_s": round(lat, 2),
                         "usage": u, "raw": text})

        if parsed is not None:
            return {"api_error_type": None, "api_error_message": None,
                    "attempts": attempts, "usage": usage_total,
                    "latency_s": latency_total, "n_searches": n_searches,
                    "parsed": parsed, "raw": text, "parse_note": note, "rmeta": rmeta,
                    "contract": rc.check_contract(parsed, review_text, cfg.legal_codes)}

        if k < cfg.parse_retries:
            if rmeta["status"] == "incomplete" and max_out < MAX_OUTPUT_CAP:
                bumped = min(int(max_out * TRUNCATION_BUMP), MAX_OUTPUT_CAP)
                print(f"       truncated at max_output={max_out:,} "
                      f"({rmeta['incomplete_reason']}) -> retrying at {bumped:,}")
                max_out = bumped
            else:
                print(f"       unparseable JSON -> resample "
                      f"{k + 2}/{cfg.parse_retries + 1}")

    # Out of attempts. This is NOT an api error: the call succeeded and was billed, the
    # model just would not emit JSON. Downstream gating counts the two separately.
    return {"api_error_type": None, "api_error_message": None,
            "attempts": attempts, "usage": usage_total, "latency_s": latency_total,
            "n_searches": n_searches, "parsed": None, "raw": attempts[-1]["raw"],
            "parse_note": "parse_failed", "rmeta": rmeta, "contract": None}


# ---------------------------------------------------------------------- preflight

def preflight(cfg: RunConfig, rows: list[dict], done: set[str]) -> None:
    man = rc.prompt_manifest(cfg.prompt_file)
    print("=" * 72)
    print(f"model          {cfg.model}   effort={cfg.effort or 'none'}   "
          f"web_search={cfg.web_search}")
    print(f"pricing        in ${cfg.pricing['input']} / cached ${cfg.pricing['cached_input']}"
          f" / write ${cfg.pricing['cache_write']} / out ${cfg.pricing['output']} per MTok"
          f"   (as of {cfg.pricing['as_of']})")
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
    print(f"cache          key={cfg.cache_key}  mode={CACHE_MODE}")
    print(f"budget         max_output={cfg.max_output:,} (bump to {MAX_OUTPUT_CAP:,} on "
          f"truncation)  parse_retries={cfg.parse_retries}")
    if cfg.max_spend:
        print(f"spend guard    stop above ${cfg.max_spend:g}")
    print(f"output         {show(cfg.paths.dir)}/")
    print("=" * 72)


# --------------------------------------------------------------------- dry run

def dry_run(cfg: RunConfig) -> None:
    rng = random.Random(RNG_SEED)
    client = OpenAI(api_key=rc.load_api_key(API_KEY_ENV, SCRIPT_DIR, ENV_FILE))
    rows = load_reviews(cfg)
    preflight(cfg, rows, set())

    # --- stage 1: does the API work at all, and does web search fire? ---
    print("\n[1/2] throwaway call with web search (short prompt, not cacheable)...")
    probe_cfg = RunConfig(**{**cfg.__dict__, "prompt": "You are a helpful assistant. "
                                                       "Answer in one sentence."})
    resp, latency, etype, emsg = call(client, probe_cfg,
                                      "What is today's weather in Guwahati, India?",
                                      rng, cached=False)
    if etype:
        print(f"\nFAILED: {etype}: {emsg}\nFix the arguments and rerun --dry.")
        sys.exit(1)

    u = usage_dict(resp)
    print(f"  response.id  {resp.id}")
    print(f"  model        {resp.model}")
    print(f"  text         {resp.output_text!r}")
    print(f"  tool calls   {[i.type for i in resp.output if getattr(i,'type','')!='message'] or 'none'}")
    rc.print_stats("  stage1", u, latency)

    # --- stage 2: does the real prompt actually cache? two identical-prefix calls. ---
    print(f"\n[2/2] caching check: two calls with the real prompt (key={cfg.cache_key})...")
    for n in (1, 2):
        r2, lat2, etype2, emsg2 = call(client, cfg, payload_for(rows[0]), rng)
        if etype2:
            print(f"\nFAILED on cache probe: {etype2}: {emsg2}")
            print("If this is a 400 on prompt_cache_breakpoint, check the block type and mode.")
            sys.exit(1)
        u2 = usage_dict(r2)
        rc.print_stats(f"  call {n}", u2, lat2)
        if n == 2:
            hit = u2["cached_tokens"] / max(u2["input_tokens"], 1)
            parsed, note = rc.parse_json(r2.output_text)
            print()
            if hit > 0.8:
                print(f"  CACHING OK: {hit:.0%} of input read from cache on the second call.")
            else:
                print(f"  CACHING BROKEN: only {hit:.0%} cached on call 2.")
                print("  Check: is the prefix >= 1024 tokens, is the breakpoint on the developer")
                print("  input_text block, is prompt_cache_key identical, did tools change?")
            print(f"  parsed JSON on probe: {note}")
            if parsed is not None:
                errs = rc.contract_errors(
                    rc.check_contract(parsed, rows[0].get("review_text", ""), cfg.legal_codes))
                print(f"  contract: {'OK' if not errs else '; '.join(errs)}")
            per = rc.cost_usd(u2, cfg.pricing)["total"]
            print(f"  output tokens {u2['output_tokens']:,} "
                  f"(reasoning {u2['reasoning_tokens']:,}) <- this sets the bill")
            print(f"  ~${per:.6f}/review  ->  ~${per * len(rows):.4f} for {len(rows)} reviews"
                  f"  ->  ~${per * PROJECT_TO:,.0f} at {PROJECT_TO:,}")

    print(f"\nIf caching is OK and the JSON parsed, run:\n"
          f"  python run_teacher_openai.py --actual --model {cfg.model} "
          f"--effort {cfg.effort} --prompt {show(cfg.prompt_file)}")


# ------------------------------------------------------------------ actual run

def actual_run(cfg: RunConfig, a: argparse.Namespace) -> None:
    rng = random.Random(RNG_SEED)
    client = OpenAI(api_key=rc.load_api_key(API_KEY_ENV, SCRIPT_DIR, ENV_FILE))
    rows = load_reviews(cfg)
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

    def save(complete: bool) -> None:
        rc.write_checkpoint(paths, {
            "tag": paths.tag, "model": cfg.model, "reasoning_effort": cfg.effort,
            "prompt_file": str(cfg.prompt_file), "prompt_sha256": cfg.prompt_sha,
            "reviews_file": str(cfg.reviews_file), "n_selected": len(rows),
            "started": started, "complete": complete, "spend_usd": round(spend, 6),
            **counters})

    print(f"\n{len(todo)} reviews to label -> {show(paths.responses)}\n")
    stopped = None
    try:
        for i, row in enumerate(todo, 1):
            rid = str(uuid.uuid4())
            res = label_review(client, cfg, row, rng, watch)

            u = res["usage"]
            cost = rc.cost_usd(u, cfg.pricing) if u else {"total": 0.0}
            spend += cost["total"]
            n_att = len(res["attempts"])
            counters["extra_attempts"] += max(n_att - 1, 0)
            counters["retried"] += n_att > 1
            rmeta = res["rmeta"] or {}

            failed_parse = res["parsed"] is None and not res["api_error_type"]
            meta = {"request_id": rid, "review_id": row.get("review_id"),
                    "ts": datetime.now().isoformat(timespec="seconds"),
                    "model": cfg.model, "reasoning_effort": cfg.effort,
                    "prompt_file": str(cfg.prompt_file), "prompt_sha256": cfg.prompt_sha,
                    "cache_key": cfg.cache_key, "cache_mode": CACHE_MODE,
                    "web_search": cfg.web_search, "pricing": cfg.pricing,
                    "latency_s": round(res["latency_s"], 2),
                    # error_type is API failure only. A response that arrived and would
                    # not parse is a different animal and gets its own flag: the call
                    # was billed, and the compliance gate scores the two separately.
                    "error_type": res["api_error_type"],
                    "error_message": res["api_error_message"],
                    "parse_failed": failed_parse,
                    "n_attempts": n_att,
                    "n_truncated_attempts": sum(a_["status"] == "incomplete"
                                                for a_ in res["attempts"]),
                    "attempt_parse_notes": [a_["parse_note"] for a_ in res["attempts"]]}

            rec = {"request_id": rid, "review_id": row.get("review_id"),
                   "raw": res["raw"], "parsed": res["parsed"],
                   "parse_note": res["parse_note"],
                   "error_type": res["api_error_type"] or ("parse_failed" if failed_parse
                                                           else None)}
            if n_att > 1:
                rec["attempts"] = res["attempts"]      # audit trail for the paper

            # Usage is recorded whichever way the row went. An API error on attempt 2
            # still leaves attempt 1 on the bill, and a cost that only lands in meta on
            # the happy path is a cost that vanishes when the run is resumed.
            if u:
                all_usage.append(u)
                meta |= {"usage": u, "cost_usd": cost}

            if res["api_error_type"]:
                counters["api_errors"] += 1
                print(f"  [{i:>2}/{len(todo)}] API ERROR {res['api_error_type']}: "
                      f"{(res['api_error_message'] or '')[:60]}")
            else:
                meta |= {k: v for k, v in rmeta.items() if k != "n_web_searches"}
                meta["n_web_searches"] = res["n_searches"]
                meta["parse_note"] = res["parse_note"]

                if res["parsed"] is None:
                    counters["parse_failures"] += 1
                    rc.print_stats(f"[{i:>2}/{len(todo)}] {'PARSE FAILED':<16}", u, res["latency_s"])
                    print(f"       gave up after {n_att} attempts  ${cost['total']:.6f}  "
                          f"running ${spend:.4f}")
                else:
                    counters["ok"] += 1
                    counters["parsed"] += 1
                    counters["truncated"] += rmeta.get("status") == "incomplete"
                    counters["searched"] += res["n_searches"] > 0
                    v = res["contract"] or {}
                    errs = rc.contract_errors(v) if v else []
                    counters["contract_bad"] += bool(errs)
                    meta |= {"n_labels": len(v.get("labels", [])),
                             "contract": {k: v[k] for k in
                                          ("bad_codes", "dup_codes", "missing_span",
                                           "span_bad", "span_loose")} if v else None}
                    flag = " TRUNCATED" if rmeta.get("status") == "incomplete" else ""
                    note = res["parse_note"] + (f" x{n_att}" if n_att > 1 else "")
                    rc.print_stats(f"[{i:>2}/{len(todo)}] {note:<16}", u, res["latency_s"])
                    print(f"       ${cost['total']:.6f}  running ${spend:.4f}  "
                          f"labels={meta['n_labels']}  searches={res['n_searches']}{flag}")
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
        "started": started, "provider": "openai",
        "model": cfg.model, "reasoning_effort": cfg.effort, "web_search": cfg.web_search,
        "prompt_file": str(cfg.prompt_file), "prompt_sha256": cfg.prompt_sha,
        "reviews_file": str(cfg.reviews_file), "cache_mode": CACHE_MODE,
        "max_output": cfg.max_output, "parse_retries": cfg.parse_retries,
        "manifest": rc.run_manifest(cfg.prompt_file, __file__),
    })

    if stopped:
        print(f"\nSTOPPED: {stopped}")
        print(f"  resume with:  python run_teacher_openai.py --actual --resume "
              f"--model {cfg.model} --effort {cfg.effort} --prompt {show(cfg.prompt_file)}")
        sys.exit(2)
    print(f"\nnext: python compute_run_stats.py --run-dir {show(paths.dir)}")


# --------------------------------------------------------------------------- cli

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Run a teacher prompt over a review set on an OpenAI model.",
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
                    choices=["none", "low", "medium", "high", "xhigh", "max"])
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
    ap.add_argument("--parse-retries", type=int, default=PARSE_RETRIES,
                    help="extra attempts when the response will not parse as JSON")
    ap.add_argument("--retries", type=int, default=RETRIES,
                    help="transport-level attempts per call")
    ap.add_argument("--no-web-search", action="store_true")

    a = ap.parse_args()
    if a.effort == "none":
        a.effort = ""
    if a.resume and a.overwrite:
        ap.error("--resume and --overwrite are opposites; pick one")
    return a


def main() -> None:
    a = parse_args()
    cfg = build_config(a)
    if a.check:
        rows = load_reviews(cfg)
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
