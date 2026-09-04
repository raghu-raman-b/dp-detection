#!/usr/bin/env python3
"""
annotate_corpus.py -- label the whole corpus with the frozen teacher configuration.

This is the production sibling of run_teacher_openai.py. That script exists to compare
configurations over the tuning set; this one takes the configuration the validation
stage SELECTED (outputs/validation/comparison/validation_all/selection.json) and applies
it to dataset_to_label.jsonl. Set DEFAULT_EFFORT to match that file before launching --
selection.json is the record the paper cites, and a mismatch means the corpus was not
labelled by the configuration the paper reports.

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

4. STOPPING ON FAILURE. At 50 reviews a failed call is a row you look at afterwards. At
   200k the cause -- no credit, a revoked key, a withdrawn model -- applies to every
   remaining review, so the run stops at the FIRST failure (--max-failures) and says
   what happened. A failure is written with parsed=null and the error in error_message:
   an error is never stored as if it were a label. It is not counted as done, so
   --resume re-labels it, and the run is only marked complete when every selected
   review carries a label.

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
import time
import uuid
from collections import Counter, defaultdict, deque
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
    max_failures: int
    progress_every: int
    stats_every: int
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
        max_spend=a.max_spend, max_failures=a.max_failures,
        progress_every=a.progress_every, stats_every=a.stats_every,
        workers=a.workers, tier=a.tier,
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

def hms(seconds: float) -> str:
    """h:mm for anything long enough to care about, m:ss below an hour."""
    if seconds != seconds or seconds in (float("inf"), float("-inf")) or seconds < 0:
        return "--:--"
    s = int(seconds)
    return f"{s//3600}:{(s%3600)//60:02d}" if s >= 3600 else f"{s//60}:{s%60:02d}"


class C:
    """ANSI colour, off unless stdout is a terminal that wants it.

    Colour is applied to the DISPLAY string only; every width calculation in Progress
    uses the uncoloured text, because a terminal counts escape sequences as zero columns
    and Python's len() does not. Mixing the two is how progress bars end up smeared."""

    ON = False
    _CODES = {"red": 31, "green": 32, "yellow": 33, "blue": 34,
              "magenta": 35, "cyan": 36, "grey": 90}

    @classmethod
    def enable(cls) -> None:
        if os.environ.get("NO_COLOR") or not sys.stdout.isatty():
            cls.ON = False
            return
        if sys.platform == "win32":
            # Windows consoles need VT processing switched on explicitly; without it
            # the escape codes are printed literally. Harmless if it fails -- modern
            # Windows Terminal and the VS Code terminal already have it on.
            try:
                import ctypes
                k = ctypes.windll.kernel32
                h = k.GetStdHandle(-11)
                mode = ctypes.c_uint32()
                if k.GetConsoleMode(h, ctypes.byref(mode)):
                    k.SetConsoleMode(h, mode.value | 0x0004)
            except Exception:
                pass
        cls.ON = True

    @classmethod
    def p(cls, text: str, colour: str = "", bold: bool = False) -> str:
        if not cls.ON or (not colour and not bold):
            return text
        parts = []
        if bold:
            parts.append("1")
        if colour in cls._CODES:
            parts.append(str(cls._CODES[colour]))
        return f"\033[{';'.join(parts)}m{text}\033[0m"


def heat(value: float, good: float, ok: float) -> str:
    """green / yellow / red by how a measured value compares to its thresholds."""
    return "green" if value >= good else ("yellow" if value >= ok else "red")


class G:
    """Display glyphs, downgraded to ASCII where the console cannot encode them.

    A legacy Windows codepage (cp1252 is still the default for a bare cmd.exe, and for
    a redirected stream) raises UnicodeEncodeError on the block and braille characters.
    Raised from the progress line that runs under the writer's lock, that would take
    down the run -- for decoration. So the glyph set is chosen once, at startup, by
    asking the actual stream whether it can encode them."""

    FANCY = {"spin": "\u280b\u2819\u2839\u2838\u283c\u2834\u2826\u2827"
                     "\u2807\u280f",
             "full": "\u2588", "empty": "\u00b7", "rule": "\u2500",
             "ok": "\u2713", "bad": "\u2717", "star": "\u2726",
             "parts": " \u258f\u258e\u258d\u258c\u258b\u258a\u2589\u2588"}
    PLAIN = {"spin": "|/-\\", "full": "#", "empty": ".", "rule": "-",
             "ok": "OK", "bad": "XX", "star": "*", "parts": " ...::::#"}

    _g = FANCY

    @classmethod
    def pick(cls) -> None:
        enc = getattr(sys.stdout, "encoding", None) or "ascii"
        probe = "".join(cls.FANCY.values())
        try:
            probe.encode(enc)
            cls._g = cls.FANCY
        except (UnicodeEncodeError, LookupError):
            cls._g = cls.PLAIN

    def __class_getitem__(cls, key):
        return cls._g[key]


class Progress:
    """Live one-line status, redrawn in place on a terminal.

    A 200k run is a multi-day process watched by a human, and printing only every 25
    completions means the 20-review sequential warm-up emits nothing at all for its
    first three minutes -- indistinguishable from a hang. So every completion redraws a
    status line, and every --progress-every completions leaves a permanent line behind
    so the scrollback still tells the story.

    The rate is measured over a rolling window rather than over the whole run: workers
    ramp 1 -> 2 -> ... -> 11, so a whole-run average would badly under-report the
    current throughput and inflate the ETA for hours.

    Redraw only happens on a tty. Under nohup or a pipe, carriage returns would turn a
    log file into one enormous line, so there the periodic lines are all that is
    written."""


    def __init__(self, every: int, window: int = 300, beat: float = 1.0):
        self.every = max(1, every)
        self.t0 = time.monotonic()
        self.marks: deque[float] = deque(maxlen=window)
        self.tty = sys.stdout.isatty()
        self.width = 0
        self.plock = threading.Lock()
        self.state: tuple | None = None     # last completion's counters
        self.inflight = 0                   # calls currently out to the API
        self.spin = 0
        self.beat = beat
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        try:
            self.cols = os.get_terminal_size().columns
        except OSError:
            self.cols = 100

    # -- the heartbeat ------------------------------------------------------------
    # A completion-driven redraw is only as live as the completions. At one worker and
    # ~20s per review the line would sit unchanged for twenty seconds at a time, which
    # reads as a hang -- the exact thing this display exists to disprove. So a daemon
    # thread redraws once a second from the last known counters, advancing the clock,
    # the ETA and a spinner. It never touches the writer's lock, so it cannot deadlock
    # against a worker; it only ever holds its own print lock.

    def start(self) -> None:
        if not self.tty or self._thread:
            return
        self._thread = threading.Thread(target=self._pulse, daemon=True,
                                        name="progress")
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()

    def _pulse(self) -> None:
        while not self._stop.wait(self.beat):
            with self.plock:
                if self.state is not None:
                    self.spin += 1
                    self._redraw()

    def rate_per_min(self) -> float:
        """Reviews per minute over the rolling window."""
        if len(self.marks) < 2:
            return 0.0
        span = self.marks[-1] - self.marks[0]
        return (len(self.marks) - 1) / span * 60.0 if span > 0 else 0.0

    def bar(self, frac: float, cells: int = 18) -> str:
        """A fractional block bar. At 200k reviews a whole-cell bar would sit still for
        11,000 reviews at a time, which looks exactly like a hang -- hence eighths."""
        frac = min(max(frac, 0.0), 1.0)
        filled = frac * cells
        whole = int(filled)
        rest = G["parts"][int((filled - whole) * 8)] if whole < cells else ""
        return (G["full"] * whole + rest).ljust(cells, G["empty"])

    def line(self, label, done, total, workers, cache, ok, errs, spend):
        """Returns (plain, coloured). Plain is what the widths are measured on."""
        rpm = self.rate_per_min()
        left = max(total - done, 0)
        eta = (left / rpm * 60.0) if rpm > 0 else float("inf")
        frac = (done / total) if total else 0.0
        cells = 18 if self.cols >= 118 else (10 if self.cols >= 96 else 0)
        wide = self.cols >= 118

        seg = []                                   # (plain, colour, bold)
        if self.tty:
            spin = G["spin"]
            seg.append((spin[self.spin % len(spin)] + " ", "cyan", False))
        seg.append((f"[{label}] ", "cyan", True))
        if cells:
            seg.append((self.bar(frac, cells) + " ", "green", False))
        seg.append((f"{frac*100:5.1f}% ", "green", True))
        seg.append((f" {done:,}/{total:,} ", "", True))
        seg.append((f" w={workers}", "magenta", False))
        seg.append((f"+{self.inflight} " if self.inflight else " ", "grey", False))
        seg.append((f" {rpm:5.1f}/min ", "yellow", False))
        seg.append((f" cache {cache:.0%} ", heat(cache, 0.80, 0.50), False))
        seg.append((f" ok {ok:,} ", "green", False))
        seg.append((f" err {errs} ", "red" if errs else "grey", errs > 0))
        seg.append((f" ${spend:,.2f} ", "yellow", True))
        if wide:
            seg.append((f" up {hms(time.monotonic()-self.t0)} ", "grey", False))
        seg.append((f" eta {hms(eta)}", "cyan", True))

        plain = "".join(p for p, _, _ in seg)
        return plain, "".join(C.p(p, c, b) for p, c, b in seg)

    def tick(self, *args) -> None:
        """Called on every completion, under the writer's lock."""
        with self.plock:
            self.marks.append(time.monotonic())
            self.state = args
            done = args[1]
            if done % self.every == 0:
                self._clear()
                print(self.line(*args)[1], flush=True)
            else:
                self._redraw()

    def _redraw(self) -> None:
        """In-place update from the stored counters. Caller holds plock."""
        if not self.tty or self.state is None:
            return
        plain, coloured = self.line(*self.state)
        pad = " " * max(self.width - len(plain), 0)
        self.width = len(plain)
        print("\r" + coloured + pad, end="", flush=True)

    def _clear(self) -> None:
        """Caller holds plock."""
        if self.tty and self.width:
            print("\r" + " " * self.width + "\r", end="", flush=True)
            self.width = 0

    def clear(self) -> None:
        with self.plock:
            self._clear()

    def emit(self, lines) -> None:
        """Print permanent lines without the heartbeat scribbling over them."""
        with self.plock:
            self._clear()
            print("\n".join(lines), flush=True)


CLASS_NAMES = {"M": "Monetary", "P": "Psychological", "S": "Social",
               "T": "Temporal", "Tech": "Technical"}


class LiveStats:
    """What the corpus is turning out to look like, while it is being built.

    This is not decoration. A 60-hour run that is quietly emitting the wrong label
    distribution is worth catching at hour two, and the two failure modes that actually
    happen -- the abstention rate drifting, and one label swallowing everything -- are
    both visible in this digest within the first few thousand reviews. The first-sighting
    line doubles as taxonomy coverage: when all 29 have fired, the codebook is reachable
    end to end on real data."""

    def __init__(self, every: int, legal: set[str]):
        self.every = max(0, every)
        self.legal = set(legal)
        self.counts: Counter = Counter()
        self.per_class: Counter = Counter()
        self.first_seen: dict[str, int] = {}
        self.pending: list[tuple[str, int, int]] = []
        self.n = 0
        self.none = 0
        self.n_labels = 0
        self.multi = 0

    def observe(self, parsed: dict | None, n_done: int) -> None:
        if parsed is None:
            return
        self.n += 1
        labels = [x.get("label") for x in (parsed.get("labels") or [])
                  if isinstance(x, dict) and x.get("label")]
        if not labels:
            self.none += 1
            return
        if len(labels) > 1:
            self.multi += 1
        for lab in labels:
            self.n_labels += 1
            self.counts[lab] += 1
            self.per_class[lab.split("_")[0]] += 1
            if lab not in self.first_seen:
                self.first_seen[lab] = n_done
                # the coverage count is snapshotted HERE: two new labels in one
                # review would otherwise both report the post-flush total.
                self.pending.append((lab, n_done, len(self.first_seen)))

    def due(self) -> bool:
        return bool(self.every) and self.n and self.n % self.every == 0

    def firsts(self) -> list[str]:
        """New labels since the last call, as printable lines."""
        out, self.pending = self.pending, []
        lines = []
        for lab, at, seen in out:
            total = len(self.legal) or 29
            lines.append(C.p(f"  {G['star']} first {lab}", "magenta", True)
                         + C.p(f"  at review {at:,}   ({seen}/{total} of the codebook "
                               f"seen)", "grey"))
        return lines

    def digest(self) -> list[str]:
        """The periodic block. Deliberately short -- it prints many times over a run."""
        if not self.n:
            return []
        w = 34
        pct = lambda k, d: (k / d * 100.0) if d else 0.0
        lines = [C.p(f"  {G['rule'] * 2} corpus so far  ({self.n:,} reviews) "
                     + G["rule"] * 28, "grey")]

        none_pct = pct(self.none, self.n)
        lines.append("   " + C.p("NONE", "", True)
                     + C.p(f" {self.none:,} ({none_pct:.1f}%)",
                           heat(1 - none_pct / 100, 0.80, 0.70), True)
                     + C.p(f"    labels {self.n_labels:,}"
                           f"    {self.n_labels/max(self.n,1):.2f}/review"
                           f"    multi-label {pct(self.multi, self.n):.0f}%", "grey"))

        if self.per_class:
            bits = []
            for cls in ("M", "P", "S", "T", "Tech"):
                n = self.per_class.get(cls, 0)
                bits.append(C.p(f"{CLASS_NAMES[cls]} ", "cyan")
                            + C.p(f"{pct(n, self.n_labels):4.1f}%", "", True))
            lines.append("   " + "  ".join(bits))

        top = self.counts.most_common(5)
        if top:
            peak = top[0][1]
            lines.append(C.p("   top", "grey"))
            for lab, n in top:
                bar = G["full"] * max(1, round(n / peak * 18))
                lines.append(f"     {lab:<{w}} " + C.p(bar, "green")
                             + C.p(f" {n:,}  {pct(n, self.n_labels):.1f}%", "grey"))

        rare = [(l, c) for l, c in self.counts.most_common()][-3:]
        if len(self.counts) > 8 and rare:
            lines.append(C.p("   rarest seen   ", "grey")
                         + C.p("  ".join(f"{l} ({c})" for l, c in reversed(rare)),
                               "yellow"))
        missing = sorted(self.legal - set(self.counts)) if self.legal else []
        if missing:
            head = ", ".join(missing[:4]) + (f" +{len(missing)-4} more"
                                             if len(missing) > 4 else "")
            lines.append(C.p(f"   not yet seen  ({len(missing)})  ", "grey")
                         + C.p(head, "grey"))
        return lines


class Writer:
    """Every mutation of on-disk state and of the running totals happens here, under one
    lock. Results arrive out of order, which is fine -- the jsonl is keyed by review_id
    and load_progress() derives the resume set from the file itself."""

    def __init__(self, cfg: RunConfig, counters: dict, spend: float,
                 all_usage: list[dict], started: str, n_total: int,
                 n_prior: int = 0, n_selected: int = 0):
        self.cfg, self.paths = cfg, cfg.paths
        self.counters, self.spend, self.all_usage = counters, spend, all_usage
        self.started, self.n_total = started, n_total
        # n_total is what THIS pass has to do; n_prior is what earlier passes
        # already finished. Progress is reported against the corpus, because
        # '11/199,693' next to 'ok 39' on a resumed run is just confusing --
        # one number was per-pass and the other cumulative.
        self.n_prior = n_prior
        self.n_selected = n_selected or (n_prior + n_total)
        self.lock = threading.Lock()
        self.n_done = 0
        self.since_checkpoint = 0
        self.stop_reason: str | None = None
        self.last_failure: dict | None = None
        self.recent_errors: deque[bool] = deque(maxlen=50)
        self.workers = 1
        self.progress = Progress(cfg.progress_every)
        self.stats = LiveStats(cfg.stats_every, cfg.legal_codes)
        self.level_label = "run"
        self.cache_hit = 0.0
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
                self.progress.clear()
                print(f"  [{self.n_prior + self.n_done:,}/{self.n_selected:,}] API ERROR "
                      f"{res['api_error_type']}: {(res['api_error_message'] or '')[:60]}",
                      flush=True)
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

            self.progress.tick(self.level_label, self.n_prior + self.n_done,
                               self.n_selected, level,
                               self.cache_hit,
                               self.counters["ok"],
                               self.counters["api_errors"] + self.counters["parse_failures"],
                               self.spend)

            self.stats.observe(res["parsed"], self.n_prior + self.n_done)
            extra_lines = self.stats.firsts()
            if self.stats.due():
                extra_lines += [""] + self.stats.digest() + [""]
            if extra_lines:
                self.progress.emit(extra_lines)

            # A review that errored or would not parse carries NO label. It is written
            # to disk as evidence (with parsed=null and the error in error_message --
            # the error text is never mistaken for a label) and it is not counted as
            # done, so --resume re-labels it. But the run stops here by default rather
            # than walking on: the same cause -- no credit, a revoked key, a changed
            # model -- will hit every remaining review, and finding that out at review
            # 199,000 is not the same as finding it out at review 21.
            n_failed = self.counters["api_errors"] + self.counters["parse_failures"]
            if res["api_error_type"]:
                self.last_failure = {
                    "review_id": row.get("review_id"), "kind": "api_error",
                    "error_type": res["api_error_type"],
                    "message": (res["api_error_message"] or "")[:400]}
            elif failed_parse:
                self.last_failure = {
                    "review_id": row.get("review_id"), "kind": "parse_failure",
                    "error_type": "parse_failed",
                    "message": (res["raw"] or "")[:400]}

            if self.cfg.max_spend and self.spend > self.cfg.max_spend:
                self.stop_reason = (f"spend guard: ${self.spend:.4f} over the "
                                    f"${self.cfg.max_spend:g} ceiling")
            elif self.cfg.max_failures and n_failed >= self.cfg.max_failures:
                self.stop_reason = (
                    f"{n_failed} review(s) failed and the failure ceiling is "
                    f"{self.cfg.max_failures} (--max-failures)")
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

def scan_responses(path: Path, legal: set[str] | None = None):
    """(done, failed, stats) in ONE pass over the file.

    A row that errored or failed to parse is not done -- it gets retried on the
    next pass, which is why it is tracked separately.

    The label distribution is rebuilt here too. It could be recomputed separately,
    but responses.jsonl is ~0.8GB at 200k and this loop is already reading every
    line of it; a resumed run would otherwise report "first M_PayToProgress
    (1/29 of the codebook seen)" for a label it found on day one."""
    done: set[str] = set()
    failed: set[str] = set()
    stats = LiveStats(0, legal or set())
    if not path.exists():
        return done, failed, stats
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
            elif not rec.get("superseded"):
                done.add(rid)
                stats.observe(rec.get("parsed"), len(done))
    stats.pending.clear()      # history, not news: do not re-announce it
    return done, failed, stats


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
                overwrite: bool, legal: set[str] | None = None):
    """Same policy as runner_common.resume_gate -- default is overwrite, an interrupted
    run stops and makes you choose -- over the streaming scan."""
    done, failed, stats = scan_responses(paths.responses, legal)
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
            return set(), set(), state, stats
        if state.get("prompt_sha256") and state["prompt_sha256"] != prompt_sha:
            sys.exit(
                f"refusing to resume: the prompt changed since this run started.\n"
                f"  checkpoint: {state['prompt_sha256'][:12]}\n"
                f"  now:        {prompt_sha[:12]}\n"
                f"  half the corpus would be labelled by a different prompt. Rerun with "
                f"--overwrite to start clean.")
        return done, failed - done, state, stats

    # Any existing run is protected, finished or not. A finished 200k run represents
    # days of wall clock and real money, and `--actual` with no flags -- the most
    # natural thing to type twice -- used to wipe it silently.
    if paths.exists() and not overwrite:
        sys.exit(
            f"a{'n interrupted' if incomplete else ' completed'} run is sitting in "
            f"{show(paths.dir)}\n"
            f"  {len(done):,} review(s) already labelled and paid for"
            + (f", {len(failed - done):,} failed\n" if failed - done else "\n") +
            f"  --resume     finish it (re-labels the failed ones, skips the rest)\n"
            f"  --overwrite  discard it and start again")

    if paths.exists():
        print(f"overwriting the run in {show(paths.dir)}")
    paths.wipe()
    return set(), set(), {}, LiveStats(0, legal or set())


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
    writer.level_label = label
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
            writer.progress.inflight = len(pending)
            done_futs, pending = wait(pending, return_when=FIRST_COMPLETED)
            for fut in done_futs:
                row, shard, res = fut.result()
                # Read the cache rate BEFORE recording, so the status line this
                # completion draws carries a current number rather than last one's.
                writer.cache_hit = watch.rolling()
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
                    writer.progress.clear()
                    warn_cache(alarm, workers)
            for _ in range(len(done_futs)):
                if not submit_one():
                    break
            writer.progress.inflight = len(pending)

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
    print(f"failure guard  " + (f"stop at failure #{cfg.max_failures} and report it"
                                if cfg.max_failures else
                                "OFF -- failures are recorded and the run walks on"))
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

    done, retry, state, prior_stats = resume_gate(paths, cfg.prompt_sha, a.resume,
                                                 a.overwrite, cfg.legal_codes)
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
    writer = Writer(cfg, counters, spend, all_usage, started, n_total,
                    n_prior=len(done), n_selected=n_sel)
    if done:
        # carry the earlier passes' distribution forward so the digest describes
        # the corpus, not just today's slice of it
        prior_stats.every = writer.stats.every
        writer.stats = prior_stats
        print(f"  carried forward: {prior_stats.n_labels:,} label(s) over "
              f"{len(prior_stats.first_seen)} distinct code(s) from earlier passes")
    ramp = {"max_workers": max_workers, "workers_current": 1,
            "cache_broke_at_workers": cache_cap, "baseline_cache_hit": None,
            "tier": cfg.tier}

    signal.signal(signal.SIGINT, _sigint_handler)
    writer.progress.start()
    client = make_client(max_workers)
    stopped = None

    try:
        # --- phase 1: sequential. Warms shard 0 and establishes the baseline. ---
        print(C.p(f"\n[1/3] sequential warm-up: {cfg.seq_warmup} reviews on shard 0\n", "cyan", True))
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
            print(C.p(f"\n  {G['ok']} CACHE CONFIRMED: {base:.1%} mean hit rate over "
                  f"{len(watch.measured)} measured calls.", "green", True))
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
                print(C.p(f"[2/3] ramp step {i}/{len(levels)}: {lv} workers, {n} reviews "
                      f"({lv} cache shards, {cache_rpm(lv):.1f} req/min each)", "cyan", True))
                got, broke = run_level(client, cfg, itertools.islice(todo_iter, n),
                                       lv, writer, watch, ramp, f"ramp:{lv}")
                roll = watch.rolling()
                if broke:
                    print(C.p(f"  {G['bad']} {lv} workers DEGRADED the cache "
                          f"({roll:.1%} vs {base:.1%} baseline)", "red", True))
                    print(f"     ramp stops here: every level above this one would pay "
                          f"~9.5x for input and prove nothing new.")
                    break
                print(C.p(f"  {G['ok']} {lv} workers OK", "green", True)
                      + C.p(f"  (cache {roll:.1%}, spend ${writer.spend:.4f})", "grey"))
                if got < n:
                    break

        # --- phase 3: the rest, at whatever level survived the ramp. ---
        if not stopped and not STOP.is_set() and not writer.stop_reason:
            final = max_workers
            broke = ramp.get("cache_broke_at_workers")
            if broke:
                good = [l for l in [1] + ramp_levels(max_workers) if l < broke]
                final = good[-1] if good else 1
                print(C.p(f"\n[3/3] remainder at {final} workers "
                          f"(held below the {broke} that broke the cache)\n",
                          "cyan", True))
            else:
                print(C.p(f"\n[3/3] remainder at {final} workers\n", "cyan", True))
            run_level(client, cfg, todo_iter, final, writer, watch, ramp, "main")

    except KeyboardInterrupt:
        stopped = "interrupted (Ctrl-C)"
    finally:
        if STOP.is_set() and not stopped:
            stopped = "interrupted (Ctrl-C)"
        if writer.stop_reason and not stopped:
            stopped = writer.stop_reason
        writer.progress.stop()
        writer.progress.inflight = 0
        if stopped and ramp.get("workers_current"):
            ramp["stopped_at_workers"] = ramp["workers_current"]
        writer.close()
        writer.progress.clear()

        # Coverage is read back off disk, not from the in-memory counters: the counters
        # describe what THIS pass did, and the question that matters is whether every
        # selected review now carries a label. A pass that ends without stopping but
        # leaves reviews unlabelled is NOT complete -- marking it complete would let a
        # later plain --actual wipe the run, and would ship a corpus with holes in it.
        labelled, still_failed, _ = scan_responses(paths.responses)
        n_missing = max(n_sel - len(labelled), 0)
        if n_missing and not stopped:
            stopped = (f"{n_missing:,} of {n_sel:,} selected review(s) carry no label "
                       f"({len(still_failed):,} failed, {n_missing - len(still_failed):,} "
                       f"never attempted)")
        writer.save(complete=stopped is None, ramp=ramp)

    rc.summarize(paths, writer.counters, writer.spend, writer.all_usage, cfg.pricing,
                 n_total or 1, extra={
        "complete": stopped is None, "stopped_because": stopped,
        "n_labelled": len(labelled), "n_missing": n_missing,
        "label_counts": dict(writer.stats.counts.most_common()),
        "class_counts": dict(writer.stats.per_class),
        "n_none": writer.stats.none,
        "n_labels_emitted": writer.stats.n_labels,
        "labels_never_seen": sorted(set(writer.stats.legal) - set(writer.stats.counts)),
        "n_failed_on_disk": len(still_failed),
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

    print(C.p(f"\ncoverage       {len(labelled):,}/{n_sel:,} review(s) labelled"
              + (f"   ({n_missing:,} MISSING)" if n_missing
                 else "   (none missing)"),
              "red" if n_missing else "green", True))

    if stopped:
        print("\n" + "!" * 72, file=sys.stderr)
        print(f"!! STOPPED: {stopped}", file=sys.stderr)
        f = writer.last_failure
        if f:
            print("!!", file=sys.stderr)
            print(f"!! last failure   review_id  {f['review_id']}", file=sys.stderr)
            print(f"!!                kind       {f['kind']}", file=sys.stderr)
            print(f"!!                error      {f['error_type']}", file=sys.stderr)
            for i, chunk in enumerate(_wrap(f["message"], 62)):
                print(f"!!                {'message   ' if i == 0 else '          '}"
                      f"{chunk}", file=sys.stderr)
        print("!!", file=sys.stderr)
        print(f"!! Nothing is lost: {len(labelled):,} labelled review(s) are on disk and",
              file=sys.stderr)
        print(f"!! every failure is written with parsed=null -- an error is never stored",
              file=sys.stderr)
        print(f"!! as if it were a label, and a failed review is retried on --resume.",
              file=sys.stderr)
        print("!!", file=sys.stderr)
        print(f"!! LOOK AT THIS BEFORE CONTINUING:", file=sys.stderr)
        print(f"!!   grep '\"error_type\"' {show(paths.meta)} | tail -5", file=sys.stderr)
        if ramp.get("cache_broke_at_workers"):
            print("!!", file=sys.stderr)
            print(f"!! recorded: the cache degraded at "
                  f"{ramp['cache_broke_at_workers']} workers;", file=sys.stderr)
            print(f"!! --resume will hold strictly below that on the next pass.",
                  file=sys.stderr)
        print("!!", file=sys.stderr)
        print(f"!! when you have diagnosed it, continue with:", file=sys.stderr)
        print(f"!!   python annotate_corpus.py --actual --resume", file=sys.stderr)
        print("!" * 72 + "\n", file=sys.stderr)
        sys.exit(2)
    print(C.p(f"\n  {G['ok']} DONE", "green", True)
          + C.p(f"   raw responses for FT: {show(paths.raw)}", "grey"))


def _wrap(text: str, width: int) -> list[str]:
    text = " ".join((text or "").split())
    return [text[i:i + width] for i in range(0, len(text), width)] or [""]


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
    ap.add_argument("--progress-every", type=int, default=25,
                    help="leave a permanent progress line every N reviews. On a "
                         "terminal the status line is redrawn on EVERY review "
                         "regardless; this only controls the scrollback history.")
    ap.add_argument("--stats-every", type=int, default=500,
                    help="print a live digest of the label distribution every N "
                         "labelled reviews (0 = off)")
    ap.add_argument("--max-failures", type=int, default=1,
                    help="stop after this many reviews fail (API error or unparseable "
                         "response). 1 = stop at the first and let you look at it. "
                         "Raise it for an unattended run; 0 = never stop on failures.")
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
    C.enable()
    G.pick()
    a = parse_args()
    cfg = build_config(a)
    if a.check:
        done, _failed, _stats = scan_responses(cfg.paths.responses)
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
