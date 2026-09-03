#!/usr/bin/env python3
"""
annotate_corpus.py -- label the whole corpus with the frozen teacher configuration.

This is the production sibling of run_teacher_openai.py. That script exists to compare
configurations over 50 reviews; this one takes the configuration those runs SELECTED
(outputs/comparison/models_and_providers_v2/selection.json ->
gpt-5.6-luna / high / teacher_v2_full) and applies it to dataset_to_label.jsonl.

    python annotate_corpus.py --check                 offline: config, paths, projections
    python annotate_corpus.py --probe                 2 live calls: read the rate limits
    python annotate_corpus.py --actual --limit 200    staged rollout
    python annotate_corpus.py --actual                the full corpus
    python annotate_corpus.py --actual --resume       pick up where an interrupt stopped

WHY THIS IS NOT JUST run_teacher_openai.py WITH A BIGGER INPUT FILE
-------------------------------------------------------------------
Three things change at 200k that do not matter at 50.

1. CACHE KEY SHARDING. run_teacher_openai.py is sequential on purpose: call 1 writes the
   cached prefix at 1.25x and every later call reads it at 0.1x. At this prompt size a
   permanently cold prefix costs ~$1,290 against ~$136 warm -- roughly 3x the entire
   run's expected bill. But a single prompt_cache_key cannot absorb the traffic either:
   OpenAI's prompt-caching guide puts overflow routing at ~15 requests/minute per key,
   and at ~13s/review that ceiling is crossed at only 4 workers. So the key is SHARDED,
   one shard per worker slot, and a shard is only ever used by one in-flight request at
   a time. Each shard sees ~4.5 req/min -- comfortably under the overflow threshold, and
   frequent enough that the 30-minute TTL never expires mid-run.

2. RAMPED CONCURRENCY. Workers are added 1 -> 2 -> 4 -> 8 -> ... -> max, and the cache
   hit rate is re-measured at every level against the baseline established during the
   sequential phase. Going straight to max would mean discovering a cache problem after
   it had already been paid for on thousands of reviews.

3. STREAMING INPUT. select_reviews() reads the whole file into a list. That is fine for
   50 rows and about 2GB of Python objects for 200k, so reviews are streamed instead and
   the done-set is applied on the way past.

Output tree -- one run, so no <model>/<effort>/<prompt> nesting:

    ../outputs/llm_annotation/
        responses.jsonl        parsed + raw text + every attempt
        raw_responses.jsonl.gz complete API response dumps, for fine-tuning
        meta.jsonl             usage, cost, latency, status, contract errors
        summary.json           scoreboard + run manifest
        checkpoint.json        progress + ramp state, for --resume
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
import os
import queue
import random
import signal
import sys
import threading
import uuid
from collections import defaultdict, deque
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import httpx2
from openai import OpenAI

sys.path.insert(0, str(Path(__file__).parent))
import runner_common as rc
from build_prompt import load_prompt

SCRIPT_DIR = Path(__file__).resolve().parent

# ============================== DEFAULTS ==============================
# The frozen winner. These are not knobs to twiddle for the production pass: they are
# what the tuning ablation selected, and changing one makes the corpus inconsistent
# with the numbers the paper reports.
DEFAULT_MODEL   = "gpt-5.6-luna"
DEFAULT_EFFORT  = "high"
DEFAULT_PROMPT  = "../outputs/prompts/teacher_v2_full.txt"

DEFAULT_REVIEWS = "../dataset/dataset_to_label.jsonl"
DEFAULT_OUT     = "../outputs/llm_annotation"

MAX_OUTPUT      = 8192
MAX_OUTPUT_CAP  = 32768
TRUNCATION_BUMP = 2.0

RETRIES         = 3
PARSE_RETRIES   = 2
SEND_TEMPERATURE = False
TEMPERATURE     = 0.0
RNG_SEED        = 20260903

WEB_SEARCH_TOOL = {"type": "web_search"}

CACHE_MODE       = "explicit"
CACHE_KEY_PREFIX = "dp-annotate"

API_KEY_ENV      = "OPENAI_API_KEY"
ENV_FILE         = ".env"

# ---- concurrency ------------------------------------------------------------
# TPM per usage tier, USD-tier -> tokens/minute. Cached input still counts against TPM
# (caching cuts the price, not the quota), so the budget is the FULL per-review token
# count, not just the uncached part. --probe reads the real numbers off the response
# headers; this table only exists so --check can project offline.
TIER_TPM = {1: 30_000, 2: 450_000, 3: 800_000, 4: 2_000_000, 5: 40_000_000}
DEFAULT_TIER = 4

TPM_HEADROOM   = 0.70   # never plan to consume more than this share of the limit
WORKER_CAP     = 256    # sanity ceiling regardless of tier

# Per-review cost model, measured from outputs/runs/gpt-5.6-luna/high/teacher_v2_full.
# Used only for offline projection and for sizing the ramp; the run bills from real usage.
EST_INPUT_TOKENS  = 25_830
EST_OUTPUT_TOKENS = 1_104
EST_LATENCY_S     = 13.2

# ---- cache guarding ---------------------------------------------------------
SEQ_WARMUP_N     = 20    # reviews labelled sequentially before any fan-out
RAMP_BATCH       = 10    # reviews per ramp step (raised to >= 3 per worker)
CACHE_FLOOR      = 0.50  # a single call below this during warmup is a hard failure
CACHE_DROP_TOL   = 0.15  # absolute drop from baseline that trips the loud warning
CACHE_WINDOW     = 50    # rolling window of measured calls the warning is judged on
CACHE_MIN_SAMPLES = 10   # measured calls a level needs before the alarm may fire
MAX_CACHE_RPM    = 15.0  # OpenAI's documented per-cache-key overflow threshold
# ======================================================================


resolve, show = rc.resolve, rc.show

# Set by the SIGINT handler. Workers check it between reviews; in-flight calls are
# always allowed to finish, because they are already billed and throwing the response
# away would mean paying for it twice.
STOP = threading.Event()


# ------------------------------------------------------------------ run config

@dataclass
class RunConfig:
    model: str
    effort: str
    prompt_file: Path
    reviews_file: Path
    out_dir: Path
    web_search: bool
    max_output: int
    parse_retries: int
    retries: int
    limit: int
    only: set[str]
    max_spend: float
    workers: int
    tier: int
    seq_warmup: int
    ramp_batch: int
    prompt: str = ""
    prompt_sha: str = ""
    legal_codes: set[str] = field(default_factory=set)
    pricing: dict = field(default_factory=dict)
    paths: "FlatPaths | None" = None

    def cache_key(self, shard: int) -> str:
        """One key per worker slot. A shared prefix is readable by every shard, so this
        costs one extra cache write per shard (~$0.0065 each) and buys immunity from the
        ~15 req/min per-key overflow threshold."""
        return f"{CACHE_KEY_PREFIX}-{self.prompt_sha[:12]}-s{shard:03d}"


class FlatPaths:
    """One run, one directory. Deliberately duck-type-compatible with
    runner_common.RunPaths so load_progress / prior_state / supersede /
    write_checkpoint / summarize all work against it unchanged."""

    def __init__(self, out_dir: Path, model: str, effort: str, prompt_file: str | Path):
        self.dir = Path(out_dir)
        self.stem = rc.prompt_stem(prompt_file)
        self.effort = effort or "none"
        self.tag = f"{model}_{self.effort}_{self.stem}"
        self.responses = self.dir / "responses.jsonl"
        self.meta = self.dir / "meta.jsonl"
        self.summary = self.dir / "summary.json"
        self.checkpoint = self.dir / "checkpoint.json"
        self.raw = self.dir / "raw_responses.jsonl.gz"

    def exists(self) -> bool:
        return self.responses.exists()

    def wipe(self) -> None:
        for p in (self.responses, self.meta, self.summary, self.checkpoint, self.raw):
            p.unlink(missing_ok=True)

    def mkdir(self) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)


def build_config(a: argparse.Namespace) -> RunConfig:
    cfg = RunConfig(
        model=a.model, effort=a.effort,
        prompt_file=resolve(a.prompt), reviews_file=resolve(a.reviews),
        out_dir=resolve(a.out_dir), web_search=not a.no_web_search,
        max_output=a.max_output, parse_retries=a.parse_retries, retries=a.retries,
        limit=a.limit,
        only={s.strip() for s in a.only.split(",") if s.strip()} if a.only else set(),
        max_spend=a.max_spend, workers=a.workers, tier=a.tier,
        seq_warmup=a.seq_warmup, ramp_batch=a.ramp_batch,
    )
    if not cfg.prompt_file.exists():
        sys.exit(f"prompt not found: {cfg.prompt_file}\n  build one:  python build_prompt.py")
    if not cfg.reviews_file.exists():
        sys.exit(f"reviews not found: {cfg.reviews_file}")
    cfg.prompt = load_prompt(cfg.prompt_file)
    cfg.prompt_sha = hashlib.sha256(cfg.prompt.encode()).hexdigest()
    cfg.legal_codes = rc.legal_codes_from_prompt(cfg.prompt)
    cfg.pricing = rc.pricing_for(cfg.model)
    cfg.paths = FlatPaths(cfg.out_dir, cfg.model, cfg.effort, cfg.prompt_file)
    return cfg


# ------------------------------------------------------------- worker planning

def plan_workers(tpm_limit: int, tokens_per_review: int = None,
                 latency_s: float = EST_LATENCY_S) -> int:
    """How many workers a TPM ceiling supports.

    A worker in steady state consumes tokens_per_review every latency_s seconds, so
    W workers burn W * tokens_per_review / latency_s tokens per second. Setting that
    equal to the per-second share of the TPM budget and solving for W:

        W = (TPM / 60) * latency_s / tokens_per_review

    Cached input is included in tokens_per_review on purpose: prompt caching cuts the
    PRICE of those tokens by 90% but they still count in full against the quota."""
    tpr = tokens_per_review or (EST_INPUT_TOKENS + EST_OUTPUT_TOKENS)
    raw = (tpm_limit / 60.0) * latency_s / tpr
    return max(1, min(WORKER_CAP, int(raw * TPM_HEADROOM)))


def ramp_levels(max_workers: int) -> list[int]:
    """1 (sequential, handled separately) then 2, 4, 8, ... up to max_workers."""
    out, lv = [], 2
    while lv < max_workers:
        out.append(lv)
        lv *= 2
    if max_workers > 1:
        out.append(max_workers)
    return out


def cache_rpm(workers: int, latency_s: float = EST_LATENCY_S) -> float:
    """Requests/minute a single cache shard sees. One shard is used by at most one
    in-flight request, so this is per-shard regardless of worker count."""
    return 60.0 / latency_s


# ------------------------------------------------------------------ the client

def make_client(workers: int) -> OpenAI:
    """openai 3.x is built on httpx2, whose default pool is 100 connections. Above that
    the workers would queue on the pool rather than the API -- looking like latency, not
    like a misconfiguration -- so the pool is sized from the worker count explicitly.

    max_retries=0: retries are runner_common's job. Leaving the SDK's own retry layer on
    would double-retry every failure and hide the counts from the checkpoint."""
    limits = httpx2.Limits(max_connections=max(workers * 2, 20),
                           max_keepalive_connections=max(workers, 10),
                           keepalive_expiry=30.0)
    return OpenAI(api_key=rc.load_api_key(API_KEY_ENV, SCRIPT_DIR, ENV_FILE),
                  http_client=httpx2.Client(limits=limits, timeout=600.0),
                  max_retries=0, timeout=600.0)


# --------------------------------------------------------------------- the call

def build_kwargs(cfg: RunConfig, user_input: str, max_output: int, shard: int,
                 cached: bool = True) -> dict:
    if not cached:
        return {"model": cfg.model, "instructions": cfg.prompt, "input": user_input,
                "max_output_tokens": max_output,
                **({"reasoning": {"effort": cfg.effort}} if cfg.effort else {}),
                **({"tools": [WEB_SEARCH_TOOL]} if cfg.web_search else {})}

    kw = {
        "model": cfg.model,
        "max_output_tokens": max_output,
        "prompt_cache_key": cfg.cache_key(shard),
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
        kw["tools"] = [WEB_SEARCH_TOOL]
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
        "cache_write_tokens": written,
        "uncached_input_tokens": u.input_tokens - cached - written,
        "output_tokens": u.output_tokens,
        "reasoning_tokens": reasoning,
        "total_tokens": getattr(u, "total_tokens", None),
    }


def response_meta(resp) -> dict:
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


def dump_response(resp) -> dict:
    """The complete API object, for fine-tuning. model_dump() keeps the reasoning items,
    tool calls and content parts that output_text throws away -- output_text is a
    convenience view, and a view is not a training corpus."""
    try:
        return resp.model_dump(mode="json")
    except Exception:
        try:
            return json.loads(resp.model_dump_json())
        except Exception:
            return {"_dump_failed": True, "output_text": getattr(resp, "output_text", None)}


def call(client, cfg: RunConfig, user_input: str, rng: random.Random, shard: int,
         max_output: int | None = None, cached: bool = True):
    mo = max_output or cfg.max_output
    return rc.call_with_retries(
        lambda: client.responses.create(**build_kwargs(cfg, user_input, mo, shard, cached)),
        cfg.retries, rng)


def label_review(client, cfg: RunConfig, row: dict, rng: random.Random,
                 shard: int, watch: "ShardCache") -> dict:
    """Label one review, re-attempting while the response will not parse as JSON.

    Unchanged in substance from run_teacher_openai.label_review(); it gains a shard (so
    the call lands on the right cache key) and keeps the full response dump of every
    attempt rather than only the text."""
    review_text = row.get("review_text", "")
    payload = rc.payload_for(row)
    attempts: list[dict] = []
    dumps: list[dict] = []
    usage_total: dict = {}
    latency_total = 0.0
    n_searches = 0
    max_out = cfg.max_output
    rmeta: dict = {}

    for k in range(cfg.parse_retries + 1):
        resp, lat, etype, emsg = call(client, cfg, payload, rng, shard, max_output=max_out)
        latency_total += lat
        if etype:
            return {"api_error_type": etype, "api_error_message": emsg,
                    "attempts": attempts, "dumps": dumps, "usage": usage_total,
                    "latency_s": latency_total, "n_searches": n_searches,
                    "parsed": None, "raw": None, "parse_note": None,
                    "rmeta": rmeta, "contract": None}

        u = usage_dict(resp)
        usage_total = rc.add_usage(usage_total, u)
        watch.observe(shard, u)
        rmeta = response_meta(resp)
        n_searches += rmeta["n_web_searches"]
        text = resp.output_text
        parsed, note = rc.parse_json(text)
        attempts.append({"n": k + 1, "max_output": max_out, "status": rmeta["status"],
                         "incomplete_reason": rmeta["incomplete_reason"],
                         "parse_note": note, "latency_s": round(lat, 2),
                         "usage": u, "raw": text})
        dumps.append({"n": k + 1, "response": dump_response(resp)})

        if parsed is not None:
            return {"api_error_type": None, "api_error_message": None,
                    "attempts": attempts, "dumps": dumps, "usage": usage_total,
                    "latency_s": latency_total, "n_searches": n_searches,
                    "parsed": parsed, "raw": text, "parse_note": note, "rmeta": rmeta,
                    "contract": rc.check_contract(parsed, review_text, cfg.legal_codes)}

        if k < cfg.parse_retries:
            if rmeta["status"] == "incomplete" and max_out < MAX_OUTPUT_CAP:
                max_out = min(int(max_out * TRUNCATION_BUMP), MAX_OUTPUT_CAP)

    return {"api_error_type": None, "api_error_message": None,
            "attempts": attempts, "dumps": dumps, "usage": usage_total,
            "latency_s": latency_total, "n_searches": n_searches, "parsed": None,
            "raw": attempts[-1]["raw"] if attempts else None,
            "parse_note": "parse_failed", "rmeta": rmeta, "contract": None}


# ------------------------------------------------------------- cache guarding

class ShardCache:
    """Cache-hit tracking, per shard and rolling.

    A shard's FIRST call is its warmup: it writes the prefix and reads nothing back, so
    0% there is correct and must not trip the alarm. Every later call on that shard is
    measured. The baseline is the mean over the sequential phase, which is the best
    behaviour this prompt can achieve; every later level is judged against it."""

    def __init__(self, floor: float = CACHE_FLOOR, tol: float = CACHE_DROP_TOL,
                 window: int = CACHE_WINDOW):
        self.floor, self.tol = floor, tol
        self.lock = threading.Lock()
        self.calls_per_shard: dict[int, int] = defaultdict(int)
        self.window: deque[float] = deque(maxlen=window)
        self.measured: list[float] = []
        self.warmups = 0
        self.baseline: float | None = None
        self.level = 1
        self._alarm: dict | None = None
        self._alarmed_levels: set[int] = set()

    def observe(self, shard: int, u: dict) -> None:
        if not u.get("input_tokens"):
            return
        hit = (u.get("cached_tokens") or 0) / u["input_tokens"]
        with self.lock:
            self.calls_per_shard[shard] += 1
            if self.calls_per_shard[shard] == 1:
                self.warmups += 1          # expected miss: this call wrote the prefix
                return
            self.window.append(hit)
            self.measured.append(hit)
            if (self.baseline is not None and self.level not in self._alarmed_levels
                    and len(self.window) >= CACHE_MIN_SAMPLES):
                roll = sum(self.window) / len(self.window)
                if roll < self.baseline - self.tol:
                    self._alarmed_levels.add(self.level)
                    self._alarm = {"level": self.level, "rolling": roll,
                                   "baseline": self.baseline, "n": len(self.window)}

    def pop_alarm(self) -> dict | None:
        with self.lock:
            a, self._alarm = self._alarm, None
            return a

    def set_level(self, level: int) -> None:
        with self.lock:
            self.level = level
            self.window.clear()

    def rolling(self) -> float:
        with self.lock:
            return sum(self.window) / len(self.window) if self.window else 0.0

    def seal_baseline(self) -> float | None:
        with self.lock:
            if self.measured:
                self.baseline = sum(self.measured) / len(self.measured)
            return self.baseline


def warn_cache(alarm: dict, workers: int) -> None:
    print("\n" + "!" * 72, file=sys.stderr)
    print(f"!! CACHE DEGRADED at {workers} workers", file=sys.stderr)
    print(f"!!   rolling hit rate {alarm['rolling']:.1%} over the last {alarm['n']} calls",
          file=sys.stderr)
    print(f"!!   baseline was     {alarm['baseline']:.1%} (sequential phase)", file=sys.stderr)
    print(f"!!   every miss pays full input rate instead of 0.1x -- about 9.5x more", file=sys.stderr)
    print("!!", file=sys.stderr)
    print(f"!! Ctrl-C NOW if this should not be happening. The interrupt is graceful:", file=sys.stderr)
    print(f"!! in-flight calls finish, everything is saved, and {workers} is recorded as", file=sys.stderr)
    print(f"!! the level that broke -- a later --resume will stay strictly below it.", file=sys.stderr)
    print("!" * 72 + "\n", file=sys.stderr)


# ------------------------------------------------------------------ the writer

class Writer:
    """Every mutation of on-disk state and of the running totals happens here, under one
    lock. Results arrive out of order, which is fine -- the jsonl is keyed by review_id
    and load_progress() derives the resume set from the file itself."""

    def __init__(self, cfg: RunConfig, counters: dict, spend: float,
                 all_usage: list[dict], started: str, n_total: int):
        self.cfg, self.paths = cfg, cfg.paths
        self.counters, self.spend, self.all_usage = counters, spend, all_usage
        self.started, self.n_total = started, n_total
        self.lock = threading.Lock()
        self.n_done = 0
        self.since_checkpoint = 0
        self.stop_reason: str | None = None
        self.recent_errors: deque[bool] = deque(maxlen=50)
        self.workers = 1
        self.f_resp = open(self.paths.responses, "a", encoding="utf-8")
        self.f_meta = open(self.paths.meta, "a", encoding="utf-8")
        self.f_raw = gzip.open(self.paths.raw, "at", encoding="utf-8")

    def close(self) -> None:
        for f in (self.f_resp, self.f_meta, self.f_raw):
            try:
                f.close()
            except Exception:
                pass

    def save(self, complete: bool, ramp: dict) -> None:
        rc.write_checkpoint(self.paths, {
            "tag": self.paths.tag, "model": self.cfg.model,
            "reasoning_effort": self.cfg.effort,
            "prompt_file": str(self.cfg.prompt_file), "prompt_sha256": self.cfg.prompt_sha,
            "reviews_file": str(self.cfg.reviews_file), "n_selected": self.n_total,
            "started": self.started, "complete": complete,
            "spend_usd": round(self.spend, 6), **ramp, **self.counters})

    def record(self, row: dict, res: dict, shard: int, level: int, ramp: dict) -> None:
        rid = str(uuid.uuid4())
        u = res["usage"]
        cost = rc.cost_usd(u, self.cfg.pricing) if u else {"total": 0.0}
        n_att = len(res["attempts"])
        rmeta = res["rmeta"] or {}
        failed_parse = res["parsed"] is None and not res["api_error_type"]

        meta = {"request_id": rid, "review_id": row.get("review_id"),
                "ts": datetime.now().isoformat(timespec="seconds"),
                "model": self.cfg.model, "reasoning_effort": self.cfg.effort,
                "prompt_file": str(self.cfg.prompt_file),
                "prompt_sha256": self.cfg.prompt_sha,
                "cache_key": self.cfg.cache_key(shard), "cache_mode": CACHE_MODE,
                "cache_shard": shard, "workers_at_call": level,
                "web_search": self.cfg.web_search, "pricing": self.cfg.pricing,
                "latency_s": round(res["latency_s"], 2),
                "error_type": res["api_error_type"],
                "error_message": res["api_error_message"],
                "parse_failed": failed_parse, "n_attempts": n_att,
                "n_truncated_attempts": sum(a_["status"] == "incomplete"
                                            for a_ in res["attempts"]),
                "attempt_parse_notes": [a_["parse_note"] for a_ in res["attempts"]]}

        rec = {"request_id": rid, "review_id": row.get("review_id"),
               "raw": res["raw"], "parsed": res["parsed"],
               "parse_note": res["parse_note"], "cache_shard": shard,
               "error_type": res["api_error_type"] or ("parse_failed" if failed_parse
                                                       else None),
               "attempts": res["attempts"]}

        # The fine-tuning artifact: the complete API object for every attempt, including
        # the ones that failed to parse. Kept in its own gzipped file because it is ~10x
        # the size of everything else and nothing but the FT pipeline reads it.
        raw_rec = {"request_id": rid, "review_id": row.get("review_id"),
                   "model": self.cfg.model, "prompt_sha256": self.cfg.prompt_sha,
                   "cache_shard": shard, "responses": res["dumps"]}

        with self.lock:
            self.n_done += 1
            self.counters["extra_attempts"] += max(n_att - 1, 0)
            self.counters["retried"] += n_att > 1
            if u:
                self.all_usage.append(u)
                meta |= {"usage": u, "cost_usd": cost}
                self.spend += cost["total"]

            if res["api_error_type"]:
                self.counters["api_errors"] += 1
                self.recent_errors.append(True)
                print(f"  [{self.n_done}/{self.n_total}] API ERROR "
                      f"{res['api_error_type']}: {(res['api_error_message'] or '')[:60]}")
            else:
                self.recent_errors.append(False)
                meta |= {k: v for k, v in rmeta.items() if k != "n_web_searches"}
                meta["n_web_searches"] = res["n_searches"]
                meta["parse_note"] = res["parse_note"]
                if res["parsed"] is None:
                    self.counters["parse_failures"] += 1
                else:
                    self.counters["ok"] += 1
                    self.counters["parsed"] += 1
                    self.counters["truncated"] += rmeta.get("status") == "incomplete"
                    self.counters["searched"] += res["n_searches"] > 0
                    v = res["contract"] or {}
                    errs = rc.contract_errors(v) if v else []
                    self.counters["contract_bad"] += bool(errs)
                    meta |= {"n_labels": len(v.get("labels", [])),
                             "contract": {k: v[k] for k in
                                          ("bad_codes", "dup_codes", "missing_span",
                                           "span_bad", "span_loose")} if v else None}

            self.f_resp.write(json.dumps(rec, ensure_ascii=False) + "\n")
            self.f_meta.write(json.dumps(meta, ensure_ascii=False) + "\n")
            self.f_raw.write(json.dumps(raw_rec, ensure_ascii=False) + "\n")
            self.since_checkpoint += 1
            if self.since_checkpoint >= 50:
                self.f_resp.flush(); self.f_meta.flush(); self.f_raw.flush()
                self.save(complete=False, ramp=ramp)
                self.since_checkpoint = 0

            if self.cfg.max_spend and self.spend > self.cfg.max_spend:
                self.stop_reason = (f"spend guard: ${self.spend:.4f} over the "
                                    f"${self.cfg.max_spend:g} ceiling")
            elif (len(self.recent_errors) == self.recent_errors.maxlen
                    and sum(self.recent_errors) > 0.5 * len(self.recent_errors)):
                self.stop_reason = (f"circuit breaker: "
                                    f"{sum(self.recent_errors)}/{len(self.recent_errors)} "
                                    f"of the most recent calls failed")


# --------------------------------------------------------------- resume state
# runner_common.load_progress() / supersede() read the whole responses file into a list.
# That is right for 50 rows and wrong here: responses.jsonl carries the raw text of
# every attempt, so at 200k it is multiple GB and the resume path is the NORMAL path,
# not an edge case. Both are re-done as single streaming passes.

def scan_responses(path: Path) -> tuple[set[str], set[str]]:
    """(done, failed) in one pass. A row that errored or failed to parse is not done --
    it gets retried on the next pass, which is why it is tracked separately."""
    done: set[str] = set()
    failed: set[str] = set()
    if not path.exists():
        return done, failed
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue                 # half-written last line from a hard kill
            rid = rec.get("review_id")
            if not rid:
                continue
            if rec.get("error_type"):
                if not rec.get("superseded"):
                    failed.add(rid)
            else:
                done.add(rid)
    return done, failed


def supersede_failed(paths: FlatPaths, retry: set[str]) -> int:
    """Flag the failed rows a resumed run is about to redo. They stay on disk -- a
    paid-for failure is evidence, and the money was really spent -- but without the flag
    one review contributes two rows and its failure is counted twice."""
    if not retry:
        return 0
    n = 0
    for path in (paths.responses, paths.meta):
        if not path.exists():
            continue
        tmp = path.with_suffix(path.suffix + ".tmp")
        with open(path, encoding="utf-8") as fin, open(tmp, "w", encoding="utf-8") as fout:
            for line in fin:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("review_id") in retry and not rec.get("superseded"):
                    rec["superseded"] = True
                    n += path == paths.responses
                fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
        tmp.replace(path)
    return n


def resume_gate(paths: FlatPaths, prompt_sha: str, resume: bool,
                overwrite: bool) -> tuple[set[str], set[str], dict]:
    """Same policy as runner_common.resume_gate -- default is overwrite, an interrupted
    run stops and makes you choose -- over the streaming scan."""
    done, failed = scan_responses(paths.responses)
    state = {}
    if paths.checkpoint.exists():
        try:
            state = json.loads(paths.checkpoint.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            state = {}
    incomplete = paths.exists() and not state.get("complete", False)

    if resume:
        if not paths.exists():
            print("--resume: nothing on disk yet, starting fresh.")
            return set(), set(), state
        if state.get("prompt_sha256") and state["prompt_sha256"] != prompt_sha:
            sys.exit(
                f"refusing to resume: the prompt changed since this run started.\n"
                f"  checkpoint: {state['prompt_sha256'][:12]}\n"
                f"  now:        {prompt_sha[:12]}\n"
                f"  half the corpus would be labelled by a different prompt. Rerun with "
                f"--overwrite to start clean.")
        return done, failed - done, state

    if incomplete and not overwrite:
        sys.exit(
            f"an interrupted run is sitting in {show(paths.dir)}\n"
            f"  {len(done):,} review(s) already labelled and paid for.\n"
            f"  --resume     finish it\n"
            f"  --overwrite  discard it and start again")

    if paths.exists():
        print(f"overwriting the completed run in {show(paths.dir)}")
    paths.wipe()
    return set(), set(), {}


# ---------------------------------------------------------------- input stream

def count_selected(cfg: RunConfig) -> int:
    n = 0
    with open(cfg.reviews_file, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                n += 1
                if cfg.limit and n >= cfg.limit:
                    break
    return n


def stream_todo(cfg: RunConfig, done: set[str]):
    """Reviews still needing a label, streamed. --limit selects the first N rows of the
    file (matching select_reviews) and the done-set is applied after, so resuming a
    limited run does not silently walk further down the corpus."""
    selected = 0
    with open(cfg.reviews_file, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            rid = row.get("review_id")
            if cfg.only and rid not in cfg.only:
                continue
            selected += 1
            if cfg.limit and selected > cfg.limit:
                return
            if rid not in done:
                yield row


# ------------------------------------------------------------------ run a level

def run_level(client, cfg: RunConfig, rows, workers: int, writer: Writer,
              watch: ShardCache, ramp: dict, label: str) -> tuple[int, bool]:
    """Label `rows` with `workers` threads. Returns (n_done, broke_the_cache).

    Submission is bounded at 2x workers rather than dumping every future in at once:
    the queue for the last 199,000 reviews would otherwise be built up front, and a
    stop request could not take effect until it drained."""
    shards: queue.Queue[int] = queue.Queue()
    for s in range(workers):
        shards.put(s)
    watch.set_level(workers)
    writer.workers = workers
    ramp["workers_current"] = workers

    it = iter(rows)
    n = 0
    broke_here = False

    def task(row):
        # The shard is claimed HERE, on a pool thread, and never by the submitting
        # thread. Claiming it at submit time deadlocks: the submitter runs ahead of the
        # workers to keep the queue fed, exhausts the (worker-sized) shard pool, and
        # then blocks in the one thread that is responsible for recycling shards.
        shard = shards.get()
        try:
            rng = random.Random(f"{RNG_SEED}-{row.get('review_id')}")
            try:
                return row, shard, label_review(client, cfg, row, rng, shard, watch)
            except Exception as e:                   # never let a thread die silently
                return row, shard, {"api_error_type": type(e).__name__,
                                    "api_error_message": str(e), "attempts": [],
                                    "dumps": [], "usage": {}, "latency_s": 0.0,
                                    "n_searches": 0, "parsed": None, "raw": None,
                                    "parse_note": None, "rmeta": {}, "contract": None}
        finally:
            shards.put(shard)                        # free the moment the call returns

    with ThreadPoolExecutor(max_workers=workers) as ex:
        pending: set = set()

        def submit_one() -> bool:
            if STOP.is_set() or writer.stop_reason:
                return False
            try:
                row = next(it)
            except StopIteration:
                return False
            pending.add(ex.submit(task, row))
            return True

        for _ in range(workers * 2):
            if not submit_one():
                break

        while pending:
            done_futs, pending = wait(pending, return_when=FIRST_COMPLETED)
            for fut in done_futs:
                row, shard, res = fut.result()
                writer.record(row, res, shard, workers, ramp)
                n += 1
                alarm = watch.pop_alarm()
                if alarm:
                    broke_here = True
                    # The LOWEST level ever seen to break is the ceiling. Assigning
                    # unconditionally would let a later, higher level overwrite an
                    # earlier failure and RAISE the cap -- the opposite of safe.
                    prev = ramp.get("cache_broke_at_workers")
                    ramp["cache_broke_at_workers"] = (workers if not prev
                                                      else min(prev, workers))
                    warn_cache(alarm, workers)
                if writer.n_done % 25 == 0:
                    hit = watch.rolling()
                    print(f"  [{label}] {writer.n_done}/{writer.n_total}  "
                          f"w={workers}  cache={hit:.1%}  "
                          f"ok={writer.counters['ok']}  "
                          f"${writer.spend:.4f}")
            for _ in range(len(done_futs)):
                if not submit_one():
                    break

        if STOP.is_set() or writer.stop_reason:
            ex.shutdown(wait=True, cancel_futures=True)
    return n, broke_here


# --------------------------------------------------------------------- preflight

def preflight(cfg: RunConfig, n_sel: int, done: set[str], max_workers: int,
              cache_cap: int | None) -> None:
    man = rc.prompt_manifest(cfg.prompt_file)
    tpr = EST_INPUT_TOKENS + EST_OUTPUT_TOKENS
    todo = max(n_sel - len(done), 0)
    per = ((EST_INPUT_TOKENS * 0.964 * cfg.pricing["cached_input"]
            + EST_INPUT_TOKENS * 0.036 * cfg.pricing["input"]
            + EST_OUTPUT_TOKENS * cfg.pricing["output"]) / 1e6)
    hours = todo * EST_LATENCY_S / max(max_workers, 1) / 3600

    print("=" * 72)
    print(f"model          {cfg.model}   effort={cfg.effort or 'none'}   "
          f"web_search={cfg.web_search}")
    print(f"pricing        in ${cfg.pricing['input']} / cached ${cfg.pricing['cached_input']}"
          f" / write ${cfg.pricing['cache_write']} / out ${cfg.pricing['output']} per MTok"
          f"   (as of {cfg.pricing['as_of']})")
    print(f"prompt         {show(cfg.prompt_file)}")
    print(f"               {len(cfg.prompt):,} chars, sha {cfg.prompt_sha[:12]}")
    if man:
        print(f"               mode={man.get('mode')}  codebook={man.get('codebook_version')}"
              f"  n_labels={man.get('n_labels')}")
    print(f"legal codes    {len(cfg.legal_codes)} parsed from the prompt's output spec"
          + ("   !! NONE FOUND - contract checks disabled" if not cfg.legal_codes else ""))
    print(f"reviews        {show(cfg.reviews_file)}  ({n_sel:,} selected"
          + (f", {len(done):,} already done, {todo:,} to do" if done else "") + ")")
    print(f"cache          {max_workers} shard(s), key={cfg.cache_key(0)}  mode={CACHE_MODE}")
    print(f"               {cache_rpm(max_workers):.1f} req/min per shard "
          f"(overflow threshold {MAX_CACHE_RPM:.0f})")
    print(f"concurrency    tier {cfg.tier} -> {TIER_TPM.get(cfg.tier, 0):,} TPM, "
          f"{tpr:,} tok/review -> max {max_workers} workers "
          f"({TPM_HEADROOM:.0%} headroom)")
    print(f"               ramp 1 -> {' -> '.join(str(x) for x in ramp_levels(max_workers))}"
          f"   (sequential first {cfg.seq_warmup}, then {cfg.ramp_batch}+ per step)")
    if cache_cap:
        print(f"               !! capped: a previous run broke the cache at "
              f"{cache_cap} workers")
    print(f"budget         max_output={cfg.max_output:,} (bump to {MAX_OUTPUT_CAP:,} on "
          f"truncation)  parse_retries={cfg.parse_retries}")
    if cfg.max_spend:
        print(f"spend guard    stop above ${cfg.max_spend:g}")
    print(f"projection     ~${per:.6f}/review warm  ->  ~${per*todo:,.0f} for {todo:,}")
    print(f"               ~{hours:.1f} h at {max_workers} workers "
          f"({EST_LATENCY_S:.1f}s/review measured)")
    print(f"output         {show(cfg.paths.dir)}/")
    print("=" * 72)


# ------------------------------------------------------------------- probe mode

def probe(cfg: RunConfig) -> None:
    """Two live calls that answer the only question --check cannot: what are THIS
    account's limits, and does a cached token still cost quota?

    The second question matters. Caching cuts the price of the prefix by 90%, and if it
    also cut the quota, tier 4 would support ~200 workers rather than ~11. It does not
    -- but the decrement between two consecutive responses proves it locally rather than
    taking a doc's word for it."""
    rng = random.Random(RNG_SEED)
    client = make_client(4)
    row = next(stream_todo(cfg, set()), None)
    if row is None:
        sys.exit("no reviews to probe with")

    print("probing rate limits with 2 calls on one cache shard...\n")
    seen = []
    for n in (1, 2):
        try:
            raw = client.responses.with_raw_response.create(
                **build_kwargs(cfg, rc.payload_for(row), cfg.max_output, shard=0))
        except Exception as e:
            sys.exit(f"probe failed: {type(e).__name__}: {e}")
        h = raw.headers
        resp = raw.parse()
        u = usage_dict(resp)
        seen.append({
            "limit_requests": h.get("x-ratelimit-limit-requests"),
            "remaining_requests": h.get("x-ratelimit-remaining-requests"),
            "limit_tokens": h.get("x-ratelimit-limit-tokens"),
            "remaining_tokens": h.get("x-ratelimit-remaining-tokens"),
            "reset_tokens": h.get("x-ratelimit-reset-tokens"),
            "usage": u,
        })
        hit = (u["cached_tokens"] / u["input_tokens"]) if u["input_tokens"] else 0
        print(f"  call {n}: input={u['input_tokens']:,} cached={u['cached_tokens']:,} "
              f"({hit:.0%}) output={u['output_tokens']:,}")
        print(f"          limit_tokens={seen[-1]['limit_tokens']} "
              f"remaining={seen[-1]['remaining_tokens']}")

    tpm = None
    try:
        tpm = int(seen[-1]["limit_tokens"])
    except (TypeError, ValueError):
        pass
    rpm = None
    try:
        rpm = int(seen[-1]["limit_requests"])
    except (TypeError, ValueError):
        pass

    print()
    if len(seen) == 2 and seen[0]["remaining_tokens"] and seen[1]["remaining_tokens"]:
        try:
            drop = int(seen[0]["remaining_tokens"]) - int(seen[1]["remaining_tokens"])
            u2 = seen[1]["usage"]
            full = u2["input_tokens"] + u2["output_tokens"]
            uncached = u2["uncached_input_tokens"] + u2["output_tokens"]
            print(f"  quota drawn by call 2: {drop:,} tokens")
            print(f"    full  (input+output):     {full:,}")
            print(f"    uncached-only:            {uncached:,}")
            print(f"  -> cached tokens {'DO' if abs(drop - full) < abs(drop - uncached) else 'DO NOT'}"
                  f" count against TPM")
        except (TypeError, ValueError):
            pass

    if tpm:
        u2 = seen[-1]["usage"]
        tpr = u2["input_tokens"] + u2["output_tokens"]
        w = plan_workers(tpm, tpr)
        print(f"\n  measured TPM limit   {tpm:,}")
        if rpm:
            print(f"  measured RPM limit   {rpm:,}")
        print(f"  tokens per review    {tpr:,}")
        print(f"  -> safe workers      {w}  ({TPM_HEADROOM:.0%} of the TPM ceiling)")
        print(f"  -> ramp              1 -> {' -> '.join(str(x) for x in ramp_levels(w))}")
        print(f"  -> wall clock        ~{199_721 * EST_LATENCY_S / w / 3600:.1f} h "
              f"for 199,721 reviews")
        print(f"\n  run it with:  python annotate_corpus.py --actual --workers {w}")
    else:
        print("  no x-ratelimit-limit-tokens header returned; "
              f"falling back to --tier {cfg.tier}")


# ------------------------------------------------------------------ actual run

def actual_run(cfg: RunConfig, a: argparse.Namespace) -> None:
    paths = cfg.paths
    paths.mkdir()

    done, retry, state = resume_gate(paths, cfg.prompt_sha, a.resume, a.overwrite)
    n_super = supersede_failed(paths, retry)
    if n_super:
        print(f"superseding {n_super} failed row(s) from the previous pass")

    # A level that broke the cache in an earlier pass becomes a hard ceiling: the next
    # run stays strictly below it. Recorded rather than re-discovered, because
    # re-discovering it costs another few thousand full-rate calls.
    cache_cap = state.get("cache_broke_at_workers") if a.resume else None
    max_workers = cfg.workers or plan_workers(TIER_TPM.get(cfg.tier, TIER_TPM[DEFAULT_TIER]))
    if cache_cap:
        levels = [1] + ramp_levels(max_workers)
        good = [l for l in levels if l < cache_cap]
        max_workers = min(max_workers, good[-1] if good else 1)

    n_sel = count_selected(cfg)
    preflight(cfg, n_sel, done, max_workers, cache_cap)

    todo_iter = stream_todo(cfg, done)
    first = next(todo_iter, None)
    if first is None:
        print("nothing to do: every selected review is already labelled.")
        return
    todo_iter = itertools.chain([first], todo_iter)
    n_total = max(n_sel - len(done), 0)

    counters, spend, all_usage = rc.prior_state(paths)
    started = state.get("started") or datetime.now().isoformat(timespec="seconds")
    watch = ShardCache()
    writer = Writer(cfg, counters, spend, all_usage, started, n_total)
    ramp = {"max_workers": max_workers, "workers_current": 1,
            "cache_broke_at_workers": cache_cap, "baseline_cache_hit": None,
            "tier": cfg.tier}

    signal.signal(signal.SIGINT, _sigint_handler)
    client = make_client(max_workers)
    stopped = None

    try:
        # --- phase 1: sequential. Warms shard 0 and establishes the baseline. ---
        print(f"\n[1/3] sequential warm-up: {cfg.seq_warmup} reviews on shard 0\n")
        run_level(client, cfg, itertools.islice(todo_iter, cfg.seq_warmup), 1,
                  writer, watch, ramp, "warmup")
        base = watch.seal_baseline()
        ramp["baseline_cache_hit"] = round(base, 4) if base is not None else None
        if base is None:
            stopped = "no cache measurements in the warm-up phase"
        elif base < CACHE_FLOOR:
            stopped = (f"cache never warmed: {base:.1%} mean hit rate over the "
                       f"sequential phase, floor is {CACHE_FLOOR:.0%}")
        else:
            print(f"\n  CACHE CONFIRMED: {base:.1%} mean hit rate over "
                  f"{len(watch.measured)} measured calls.")
            print(f"  This is the baseline. Every later level is judged against it, "
                  f"with a {CACHE_DROP_TOL:.0%} tolerance.\n")

        # --- phase 2: ramp. Double the workers, re-measure, repeat. ---
        if not stopped and not STOP.is_set() and not writer.stop_reason:
            levels = ramp_levels(max_workers)
            for i, lv in enumerate(levels, 1):
                if STOP.is_set() or writer.stop_reason:
                    break
                # A level must produce enough MEASURED calls to be judgeable. Each
                # newly-added shard spends its first call warming, and warmups are
                # excluded from the hit rate, so the step has to cover both: at least
                # 3 calls per worker, and at least CACHE_MIN_SAMPLES beyond the warmups.
                n = max(cfg.ramp_batch, 3 * lv, lv + CACHE_MIN_SAMPLES)
                print(f"[2/3] ramp step {i}/{len(levels)}: {lv} workers, {n} reviews "
                      f"({lv} cache shards, {cache_rpm(lv):.1f} req/min each)")
                got, broke = run_level(client, cfg, itertools.islice(todo_iter, n),
                                       lv, writer, watch, ramp, f"ramp:{lv}")
                roll = watch.rolling()
                if broke:
                    print(f"  -> {lv} workers DEGRADED the cache "
                          f"({roll:.1%} vs {base:.1%} baseline)")
                    print(f"     ramp stops here: every level above this one would pay "
                          f"~9.5x for input and prove nothing new.")
                    break
                print(f"  -> {lv} workers OK  (cache {roll:.1%}, "
                      f"spend ${writer.spend:.4f})")
                if got < n:
                    break

        # --- phase 3: the rest, at whatever level survived the ramp. ---
        if not stopped and not STOP.is_set() and not writer.stop_reason:
            final = max_workers
            broke = ramp.get("cache_broke_at_workers")
            if broke:
                good = [l for l in [1] + ramp_levels(max_workers) if l < broke]
                final = good[-1] if good else 1
                print(f"\n[3/3] remainder at {final} workers "
                      f"(held below the {broke} that broke the cache)\n")
            else:
                print(f"\n[3/3] remainder at {final} workers\n")
            run_level(client, cfg, todo_iter, final, writer, watch, ramp, "main")

    except KeyboardInterrupt:
        stopped = "interrupted (Ctrl-C)"
    finally:
        if STOP.is_set() and not stopped:
            stopped = "interrupted (Ctrl-C)"
        if writer.stop_reason and not stopped:
            stopped = writer.stop_reason
        if stopped and ramp.get("workers_current"):
            ramp["stopped_at_workers"] = ramp["workers_current"]
        writer.save(complete=stopped is None, ramp=ramp)
        writer.close()

    rc.summarize(paths, writer.counters, writer.spend, writer.all_usage, cfg.pricing,
                 n_total or 1, extra={
        "complete": stopped is None, "stopped_because": stopped,
        "started": started, "provider": "openai",
        "model": cfg.model, "reasoning_effort": cfg.effort, "web_search": cfg.web_search,
        "prompt_file": str(cfg.prompt_file), "prompt_sha256": cfg.prompt_sha,
        "reviews_file": str(cfg.reviews_file), "cache_mode": CACHE_MODE,
        "max_output": cfg.max_output, "parse_retries": cfg.parse_retries,
        "n_selected": n_sel, "n_todo_at_start": n_total,
        "cache_shards": max_workers, "cache_warmups": watch.warmups,
        **{f"ramp_{k}": v for k, v in ramp.items()},
        "manifest": rc.run_manifest(cfg.prompt_file, __file__),
    })

    if stopped:
        print(f"\nSTOPPED: {stopped}")
        if ramp.get("cache_broke_at_workers"):
            print(f"  recorded: the cache degraded at "
                  f"{ramp['cache_broke_at_workers']} workers.")
            print(f"  --resume will hold strictly below that on the next pass.")
        print(f"\n  resume with:  python annotate_corpus.py --actual --resume")
        sys.exit(2)
    print(f"\ndone. raw responses for FT: {show(paths.raw)}")


# --------------------------------------------------------------------- signals

def _sigint_handler(signum, frame) -> None:
    """Graceful by default. In-flight calls are already billed, so they are allowed to
    finish and be written; only new submissions stop. A second Ctrl-C means the user
    wants out now and accepts losing whatever is still in the air."""
    if STOP.is_set():
        print("\n  second interrupt -- exiting now, in-flight responses are lost.",
              file=sys.stderr)
        os._exit(130)
    STOP.set()
    print("\n\n  INTERRUPT: no new calls will start. Finishing the in-flight ones "
          "(already billed),\n  then saving the checkpoint. Ctrl-C again to force.\n",
          file=sys.stderr)


# --------------------------------------------------------------------------- cli

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Label the corpus with the frozen teacher configuration.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true",
                      help="offline preflight: config, paths, projections. No API calls.")
    mode.add_argument("--probe", action="store_true",
                      help="2 live calls: read this account's real rate limits")
    mode.add_argument("--actual", action="store_true", help="label the corpus")

    ap.add_argument("--model", default=DEFAULT_MODEL,
                    help=f"one of: {', '.join(sorted(rc.PRICING_TABLE))}")
    ap.add_argument("--effort", default=DEFAULT_EFFORT,
                    choices=["none", "low", "medium", "high", "xhigh", "max"])
    ap.add_argument("--prompt", default=DEFAULT_PROMPT)
    ap.add_argument("--reviews", default=DEFAULT_REVIEWS)
    ap.add_argument("--out-dir", default=DEFAULT_OUT)

    ap.add_argument("--workers", type=int, default=0,
                    help="max concurrent workers; 0 = derive from --tier. "
                         "Also the number of cache shards.")
    ap.add_argument("--tier", type=int, default=DEFAULT_TIER, choices=sorted(TIER_TPM),
                    help="OpenAI usage tier, used to derive --workers offline")
    ap.add_argument("--seq-warmup", type=int, default=SEQ_WARMUP_N,
                    help="reviews labelled sequentially before any fan-out")
    ap.add_argument("--ramp-batch", type=int, default=RAMP_BATCH,
                    help="reviews per ramp step (raised to at least 3 per worker)")

    ap.add_argument("--resume", action="store_true",
                    help="continue an interrupted run, skipping reviews already done")
    ap.add_argument("--overwrite", action="store_true",
                    help="discard an interrupted run and start clean")

    ap.add_argument("--limit", type=int, default=0, help="0 = all")
    ap.add_argument("--only", default="", help="comma-separated review_ids")
    ap.add_argument("--max-spend", type=float, default=0.0,
                    help="stop the run once spend passes this many USD (0 = no ceiling)")
    ap.add_argument("--max-output", type=int, default=MAX_OUTPUT)
    ap.add_argument("--parse-retries", type=int, default=PARSE_RETRIES)
    ap.add_argument("--retries", type=int, default=RETRIES)
    ap.add_argument("--no-web-search", action="store_true")

    a = ap.parse_args()
    if a.effort == "none":
        a.effort = ""
    if a.resume and a.overwrite:
        ap.error("--resume and --overwrite are opposites; pick one")
    if a.workers < 0:
        ap.error("--workers cannot be negative")
    return a


def main() -> None:
    a = parse_args()
    cfg = build_config(a)
    if a.check:
        done, _failed = scan_responses(cfg.paths.responses)
        state = {}
        if cfg.paths.checkpoint.exists():
            state = json.loads(cfg.paths.checkpoint.read_text(encoding="utf-8"))
        mw = cfg.workers or plan_workers(TIER_TPM.get(cfg.tier, TIER_TPM[DEFAULT_TIER]))
        preflight(cfg, count_selected(cfg), done, mw,
                  state.get("cache_broke_at_workers"))
        if done:
            print(f"on disk: {len(done):,} labelled, complete={state.get('complete')}, "
                  f"spend=${state.get('spend_usd', 0):.4f}")
        print("\nno API calls made. --probe to read the real rate limits.")
    elif a.probe:
        probe(cfg)
    else:
        actual_run(cfg, a)


if __name__ == "__main__":
    main()
