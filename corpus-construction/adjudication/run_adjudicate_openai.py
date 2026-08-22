#!/usr/bin/env python3
"""
run_adjudicate_openai.py -- run the adjudication prompt over labeled_data on an OpenAI model.

    python run_adjudicate_openai.py --dry       one probe call, checks caching + contract
    python run_adjudicate_openai.py --actual    checks every row

Fork of run_teacher_openai.py. Same caching discipline, same three-file output, plus a
fourth file: adjudicated.jsonl, which joins the model's verdicts back onto the input rows
and is what dp_adjudicator.html loads.

Sequential on purpose: the first call writes the cached prefix and every later call reads
it. Parallel workers launched cold would all miss at once and each pay a cache write.

RESUME is on by default. A 600-row run at ~7s a call is over an hour; if it dies, rerun
and it skips every row_uid already in adjudicated.jsonl and appends the rest.

Outputs, joined on request_id:
    runs/openai/<tag>_responses.jsonl   raw text + parsed JSON
    runs/openai/<tag>_meta.jsonl        usage, cost, latency, status, errors
    runs/openai/<tag>_summary.json      scoreboard row
    adjudicated.jsonl                   input row + verdicts   <- the tool eats this
"""

from __future__ import annotations
import argparse, hashlib, json, os, re, sys, time, uuid
from collections import Counter
from datetime import datetime
from pathlib import Path
from openai import OpenAI

sys.path.insert(0, str(Path(__file__).parent))
from build_adjudicate_prompt import load_prompt
from build_input import LABEL_CODES

# ============================== CONFIG ==============================
MODEL            = "gpt-5.6-luna"
REASONING_EFFORT = "high"        # none | low | medium | high | xhigh | max
PROMPT_FILE      = "../adjudication/prompts/adjudicate_v1.txt"
REVIEW_FILE      = "../adjudication/input/adjudication_input.jsonl"
OUT_DIR          = "../adjudication/runs/openai"
ADJUDICATED_FILE = "adjudicated.jsonl"
RESUME           = True            # skip row_uids already in ADJUDICATED_FILE, append
WEB_SEARCH       = True
MAX_OUTPUT       = 8192            # reasoning tokens count against this; too low = empty output
SEND_TEMPERATURE = False           # True only if the model accepts it
TEMPERATURE      = 0.0
RETRIES          = 3
LIMIT            = 0               # 0 = all; set 3 or 20 for a partial actual run

WEB_SEARCH_TOOL  = {"type": "web_search"}

# GPT-5.6 caching: the implicit breakpoint sits on the LATEST USER MESSAGE, which is a
# different review every call. Without an explicit breakpoint the prefix never matches and
# every request pays a 1.25x cache write. So: prompt goes in a developer message with an
# explicit breakpoint, explicit-only mode stops the review suffix being cached, and a
# stable prompt_cache_key routes requests to the same cache.
CACHE_MODE       = "explicit"      # "explicit" | "implicit"
CACHE_KEY_PREFIX = "dp-adjudicate" # prompt sha is appended automatically

API_KEY_ENV      = "OPENAI_API_KEY"
ENV_FILE         = ".env"          # optional: KEY=value lines, gitignored

# USD per million tokens. Check the pricing page on the day you run and record the date;
# these move, and the paper needs the rates that were live for the run.

# Luna
PRICING = {
    "model": "gpt-5.6-luna",
    "as_of": "2026-08-21",
    "input": 0.20,
    "cached_input": 0.02,      # 0.1x input
    "cache_write": 0.25,       # 1.25x input
    "output": 1.20,
}

# Terra
# PRICING = {
#     "model": "gpt-5.6-terra",
#     "as_of": "2026-08-21",
#     "input": 2.00,
#     "cached_input": 0.20,
#     "cache_write": 2.50,
#     "output": 12.00,
# }
# ====================================================================

VOCAB = set(LABEL_CODES)


def get_client() -> "OpenAI":
    """Key resolution: real environment first, then .env in the script's directory.
    Never hardcode the key in this file - it goes to git and into the paper repo."""
    key = os.environ.get(API_KEY_ENV)
    if not key:
        envfile = Path(__file__).parent / ENV_FILE
        if envfile.exists():
            for line in envfile.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == API_KEY_ENV:
                    key = v.strip().strip("\"'")
                    break
    if not key:
        sys.exit(
            f"No API key found.\n"
            f"  export {API_KEY_ENV}=sk-...\n"
            f"or put a line in {Path(__file__).parent / ENV_FILE}:\n"
            f"  {API_KEY_ENV}=sk-...\n"
            f"(add {ENV_FILE} to .gitignore)"
        )
    print(f"key loaded ({key[:7]}...{key[-4:]})", file=sys.stderr)
    return OpenAI(api_key=key)


def cost_usd(u: dict) -> dict:
    """Cost of one call from exact token counts. The three input buckets are disjoint."""
    c_cached = u["cached_tokens"]          * PRICING["cached_input"] / 1e6
    c_write  = u["cache_write_tokens"]     * PRICING["cache_write"]  / 1e6
    c_plain  = u["uncached_input_tokens"]  * PRICING["input"]        / 1e6
    c_out    = u["output_tokens"]          * PRICING["output"]       / 1e6
    return {"cached": round(c_cached, 8), "cache_write": round(c_write, 8),
            "uncached_input": round(c_plain, 8), "output": round(c_out, 8),
            "total": round(c_cached + c_write + c_plain + c_out, 8)}


def cache_key(prompt: str) -> str:
    return f"{CACHE_KEY_PREFIX}-{hashlib.sha256(prompt.encode()).hexdigest()[:12]}"


def build_kwargs(prompt: str, user_input: str, cached: bool = True) -> dict:
    """cached=True puts the prompt in a developer message with an explicit breakpoint.
    cached=False is for the throwaway dry-run call (too short to cache anyway)."""
    if not cached:
        return {"model": MODEL, "instructions": prompt, "input": user_input,
                "max_output_tokens": MAX_OUTPUT,
                **({"reasoning": {"effort": REASONING_EFFORT}} if REASONING_EFFORT else {}),
                **({"tools": [WEB_SEARCH_TOOL]} if WEB_SEARCH else {})}

    kw = {
        "model": MODEL,
        "max_output_tokens": MAX_OUTPUT,
        "prompt_cache_key": cache_key(prompt),
        "prompt_cache_options": {"mode": CACHE_MODE},
        "input": [
            {"type": "message", "role": "developer", "content": [
                {"type": "input_text", "text": prompt,
                 "prompt_cache_breakpoint": {"mode": "explicit"}}]},
            {"type": "message", "role": "user", "content": [
                {"type": "input_text", "text": user_input}]},
        ],
    }
    if REASONING_EFFORT:
        kw["reasoning"] = {"effort": REASONING_EFFORT}
    if WEB_SEARCH:
        kw["tools"] = [WEB_SEARCH_TOOL]          # tools render before the prefix: keep identical
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


def print_stats(tag: str, u: dict, latency: float) -> None:
    hit = u["cached_tokens"] / u["input_tokens"] if u["input_tokens"] else 0
    print(f"[{datetime.now():%H:%M:%S}] {tag}  "
          f"input={u['input_tokens']:,} cached={u['cached_tokens']:,} ({hit:.0%}) "
          f"written={u['cache_write_tokens']:,} "
          f"output={u['output_tokens']:,} (reasoning={u['reasoning_tokens']:,}) "
          f"{latency:.1f}s")


def call(client, prompt: str, user_input: str, cached: bool = True):
    """Returns (response, latency, error_type). Retries on transient failures."""
    for attempt in range(RETRIES):
        t0 = time.time()
        try:
            resp = client.responses.create(**build_kwargs(prompt, user_input, cached))
            return resp, time.time() - t0, None
        except Exception as e:
            etype = type(e).__name__
            if attempt == RETRIES - 1:
                return None, time.time() - t0, f"{etype}: {e}"
            print(f"    retry {attempt+1} after {etype}", file=sys.stderr)
            time.sleep(2 ** attempt)


def parse_json(text: str) -> tuple[dict | None, str]:
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


# ------------------------------------------------------- contract validation

def payload_for(row: dict) -> str:
    """What the model sees. Deliberately not star_rating and not seed_keyword:
    the seed keyword names the phrase the targeted rows were sampled on, so sending it
    would hand the checker the expected answer on every targeted row."""
    return json.dumps({"game_name": row.get("game_name", ""),
                       "review_text": row.get("review_text", ""),
                       "assigned_labels": row.get("assigned_labels", [])},
                      ensure_ascii=False)


def validate(parsed: dict | None, row: dict) -> list[str]:
    """Contract errors. Empty list = the response is usable as is.

    Checked here rather than in the tool because a silent contract break (a verdict for a
    label that was never assigned, a span that is not in the review) would look like a
    real disagreement in the UI and you would adjudicate against a hallucination.
    """
    if parsed is None:
        return ["unparseable"]

    errs: list[str] = []
    assigned = list(row.get("assigned_labels") or [])
    text = row.get("review_text") or ""
    verdicts = parsed.get("verdicts")
    none_check = parsed.get("none_check")

    if not isinstance(verdicts, list):
        return ["verdicts missing or not a list"]

    if assigned:
        got = [v.get("label") for v in verdicts if isinstance(v, dict)]
        if got != assigned:
            errs.append(f"verdict labels {got} != assigned {assigned}")
        if none_check not in (None, {}):
            errs.append("none_check filled on a labeled row")
    else:
        if verdicts:
            errs.append("verdicts non-empty on an unlabeled row")
        if not isinstance(none_check, dict):
            errs.append("none_check missing on an unlabeled row")
        elif none_check.get("supported") is False:
            sug = none_check.get("suggested_label")
            if sug not in VOCAB:
                errs.append(f"none_check suggested_label out of vocab: {sug!r}")
            sp = none_check.get("span")
            if not sp or sp not in text:
                errs.append("none_check span not verbatim in review_text")

    for v in verdicts:
        if not isinstance(v, dict):
            errs.append("verdict entry is not an object")
            continue
        lab, verd, span = v.get("label"), v.get("verdict"), v.get("span")
        if lab not in VOCAB:
            errs.append(f"label out of vocab: {lab!r}")
        if verd not in ("supported", "unsupported", "wrong_label"):
            errs.append(f"{lab}: bad verdict {verd!r}")
        if verd == "supported":
            if not span:
                errs.append(f"{lab}: supported with no span")
            elif span not in text:
                errs.append(f"{lab}: span not verbatim in review_text")
        if verd == "wrong_label":
            sug = v.get("suggested_label")
            if sug not in VOCAB:
                errs.append(f"{lab}: suggested_label out of vocab: {sug!r}")
            if span and span not in text:
                errs.append(f"{lab}: span not verbatim in review_text")
        if verd == "unsupported" and span:
            errs.append(f"{lab}: unsupported but a span was given")
    return errs


def load_rows() -> list[dict]:
    rows = [json.loads(l) for l in
            Path(REVIEW_FILE).read_text(encoding="utf-8").splitlines() if l.strip()]
    for i, r in enumerate(rows, 1):
        if not r.get("row_uid"):
            r["row_uid"] = f"{r.get('source_file', REVIEW_FILE)}:{r.get('source_line', i)}"
    return rows


def already_done(path: Path) -> set[str]:
    if not (RESUME and path.exists()):
        return set()
    done = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        # a row that errored is not done; it should be retried on the next pass
        if rec.get("row_uid") and not rec.get("adj", {}).get("error_type"):
            done.add(rec["row_uid"])
    return done


# --------------------------------------------------------------- dry run


def dry_run() -> None:
    client = get_client()
    print(f"model={MODEL}  effort={REASONING_EFFORT}  web_search={WEB_SEARCH}")
    print("checking prompt file...")
    prompt = load_prompt(PROMPT_FILE)
    print(f"  {PROMPT_FILE}: {len(prompt):,} chars, ~{len(prompt)//4:,} tokens")
    rows = load_rows()
    labeled = [r for r in rows if r.get("assigned_labels")]
    unlabeled = [r for r in rows if not r.get("assigned_labels")]
    files = sorted({r.get("source_file", "?") for r in rows})
    print(f"  {REVIEW_FILE}: {len(rows)} rows from {files}")
    print(f"    labeled {len(labeled)}, unlabeled {len(unlabeled)}")
    done = already_done(Path(ADJUDICATED_FILE))
    if done:
        print(f"  resume: {len(done)} row_uids already in {ADJUDICATED_FILE}, "
              f"{len(rows) - len(done)} left")

    # --- stage 1: does the API work at all, and does web search fire? ---
    print("\n[1/2] throwaway call with web search (short prompt, not cacheable)...")
    resp, latency, err = call(
        client,
        "You are a helpful assistant. Answer in one sentence.",
        "What is today's weather in Guwahati, India?",
        cached=False,
    )
    if err:
        print(f"\nFAILED: {err}\nFix the config at the top of this file and rerun --dry.")
        sys.exit(1)
    u = usage_dict(resp)
    print(f"  response.id  {resp.id}")
    print(f"  model        {resp.model}")
    print(f"  text         {resp.output_text!r}")
    print(f"  tool calls   {[i.type for i in resp.output if getattr(i,'type','')!='message'] or 'none'}")
    print_stats("  stage1", u, latency)

    # --- stage 2: caching, plus does the contract hold on a real row of each kind? ---
    probes = [r for r in (labeled[:1] + unlabeled[:1]) if r]
    print(f"\n[2/2] {len(probes) + 1} calls with the real prompt "
          f"(key={cache_key(prompt)})...")
    seq = probes + probes[:1]        # repeat the first so call 2+ can hit the cache
    for n, row in enumerate(seq, 1):
        kind = "labeled" if row.get("assigned_labels") else "unlabeled"
        r2, lat2, err2 = call(client, prompt, payload_for(row), cached=True)
        if err2:
            print(f"\nFAILED on probe {n}: {err2}")
            print("If this is a 400 on prompt_cache_breakpoint, check the block type and mode.")
            sys.exit(1)
        u2 = usage_dict(r2)
        print_stats(f"  call {n} ({kind})", u2, lat2)
        parsed, note = parse_json(r2.output_text)
        errs = validate(parsed, row)
        print(f"       parse={note}  contract={'OK' if not errs else errs}")
        if n == len(seq):
            hit = u2["cached_tokens"] / max(u2["input_tokens"], 1)
            print()
            if hit > 0.8:
                print(f"  CACHING OK: {hit:.0%} of input read from cache on the last call.")
            else:
                print(f"  CACHING BROKEN: only {hit:.0%} cached on the last call.")
                print("  Check: is the prefix >= 1024 tokens, is the breakpoint on the developer")
                print("  input_text block, is prompt_cache_key identical, did tools change?")
            per = cost_usd(u2)["total"]
            print(f"  output tokens {u2['output_tokens']:,} "
                  f"(reasoning {u2['reasoning_tokens']:,}) <- this sets the bill")
            print(f"  ~${per:.6f}/row  ->  ~${per * len(rows):.2f} for {len(rows)} rows")

    print("\nIf caching is OK and the contract held, run:  "
          "python run_adjudicate_openai.py --actual")


# ------------------------------------------------------------ actual run

def actual_run() -> None:
    client = get_client()
    prompt = load_prompt(PROMPT_FILE)
    rows = load_rows()

    adj_path = Path(ADJUDICATED_FILE)
    adj_path.parent.mkdir(parents=True, exist_ok=True)
    done = already_done(adj_path)
    todo = [r for r in rows if r["row_uid"] not in done]
    if LIMIT:
        todo = todo[:LIMIT]
    if not todo:
        print(f"nothing to do: all {len(rows)} rows already in {ADJUDICATED_FILE}")
        return

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    tag = f"{MODEL}_{REASONING_EFFORT}_{stamp}"
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    f_resp = open(Path(OUT_DIR) / f"{tag}_responses.jsonl", "w", encoding="utf-8")
    f_meta = open(Path(OUT_DIR) / f"{tag}_meta.jsonl", "w", encoding="utf-8")
    f_adj = open(adj_path, "a" if done else "w", encoding="utf-8")

    prompt_sha = hashlib.sha256(prompt.encode()).hexdigest()
    print(f"{len(todo)} rows to check ({len(done)} already done) -> {adj_path}")
    print(f"prompt sha {prompt_sha[:12]}  cache key {cache_key(prompt)}\n")

    n_ok = n_parsed = n_trunc = n_search = n_contract = 0
    verdict_counts, none_counts = Counter(), Counter()
    spend = 0.0
    all_usage = []

    for i, row in enumerate(todo, 1):
        rid = str(uuid.uuid4())
        resp, latency, err = call(client, prompt, payload_for(row))

        meta = {"request_id": rid, "row_uid": row["row_uid"],
                "review_id": row.get("review_id"),
                "source_file": row.get("source_file"),
                "ts": datetime.now().isoformat(timespec="seconds"),
                "model": MODEL, "reasoning_effort": REASONING_EFFORT,
                "prompt_file": PROMPT_FILE, "prompt_sha256": prompt_sha,
                "cache_key": cache_key(prompt), "cache_mode": CACHE_MODE,
                "web_search": WEB_SEARCH, "pricing": PRICING,
                "latency_s": round(latency, 2), "error_type": err}

        adj = {"model": MODEL, "reasoning_effort": REASONING_EFFORT,
               "run_tag": tag, "prompt_sha256": prompt_sha,
               "ts": meta["ts"], "request_id": rid, "error_type": err}

        if err:
            rec = {"request_id": rid, "row_uid": row["row_uid"], "error_type": err}
            adj |= {"contract_errors": ["call_failed"]}
            print(f"  [{i:>4}/{len(todo)}] ERROR {err[:70]}")
        else:
            n_ok += 1
            text = resp.output_text
            parsed, note = parse_json(text)
            n_parsed += parsed is not None
            errs = validate(parsed, row)
            n_contract += bool(errs)
            u = usage_dict(resp)
            cost = cost_usd(u)
            rm = response_meta(resp)
            spend += cost["total"]
            all_usage.append(u)
            n_trunc += rm["status"] == "incomplete"
            n_search += rm["n_web_searches"] > 0

            verdicts = (parsed or {}).get("verdicts") or []
            for v in verdicts:
                if isinstance(v, dict):
                    verdict_counts[v.get("verdict")] += 1
            nc = (parsed or {}).get("none_check")
            if isinstance(nc, dict):
                none_counts["agree" if nc.get("supported") else "disagree"] += 1

            meta |= {**rm, "usage": u, "cost_usd": cost, "parse_note": note,
                     "contract_errors": errs}
            rec = {"request_id": rid, "row_uid": row["row_uid"],
                   "review_id": row.get("review_id"),
                   "raw": text, "parsed": parsed, "parse_note": note,
                   "error_type": None if parsed else "parse_failed"}
            adj |= {"analysis": (parsed or {}).get("analysis"),
                    "verdicts": verdicts,
                    "none_check": (parsed or {}).get("none_check"),
                    "invoked_web_search": (parsed or {}).get("invoked_web_search"),
                    "search_query": (parsed or {}).get("search_query"),
                    "search_result": (parsed or {}).get("search_result"),
                    "parse_note": note, "contract_errors": errs,
                    "latency_s": round(latency, 2)}

            contested = sum(1 for v in verdicts
                            if isinstance(v, dict) and v.get("verdict") != "supported")
            if isinstance(nc, dict) and nc.get("supported") is False:
                contested += 1
            flags = ""
            if rm["status"] == "incomplete":
                flags += " TRUNCATED"
            if errs:
                flags += f" CONTRACT({len(errs)})"
            print(f"  [{i:>4}/{len(todo)}] {row['row_uid']:<24} {note:<16} "
                  f"contested={contested} ${spend:.4f} {latency:.1f}s{flags}")

        f_resp.write(json.dumps(rec, ensure_ascii=False) + "\n")
        f_meta.write(json.dumps(meta, ensure_ascii=False) + "\n")
        f_adj.write(json.dumps({**row, "adj": adj}, ensure_ascii=False) + "\n")
        f_resp.flush(); f_meta.flush(); f_adj.flush()

    f_resp.close(); f_meta.close(); f_adj.close()

    print(f"\ndone. ok {n_ok}/{len(todo)}  parsed {n_parsed}/{len(todo)}  "
          f"truncated {n_trunc}  searched {n_search}  contract errors {n_contract}")
    print(f"  verdicts: {dict(verdict_counts)}")
    print(f"  none_check: {dict(none_counts)}")
    if n_contract:
        print("  ^ rows with contract errors are shown in the tool but should be read "
              "with suspicion; a bad span is not a real disagreement.")
    if all_usage:
        n = len(all_usage)
        tot_in = sum(x["input_tokens"] for x in all_usage)
        tot_cached = sum(x["cached_tokens"] for x in all_usage)
        tot_out = sum(x["output_tokens"] for x in all_usage)
        tot_reas = sum(x["reasoning_tokens"] for x in all_usage)
        per = spend / n
        print(f"  cache hit rate  {tot_cached/max(tot_in,1):.3f}")
        print(f"  mean output     {tot_out/n:.0f} tokens "
              f"(reasoning {tot_reas/n:.0f}, {100*tot_reas/max(tot_out,1):.0f}% of output)")
        print(f"  spend           ${spend:.4f}   ${per:.6f}/row")
        summary = {"tag": tag, "n": n, "prompt_sha256": prompt_sha,
                   "prompt_file": PROMPT_FILE, "model": MODEL,
                   "reasoning_effort": REASONING_EFFORT, "web_search": WEB_SEARCH,
                   "pricing": PRICING, "ok": n_ok, "parsed": n_parsed,
                   "truncated": n_trunc, "searched": n_search,
                   "contract_errors": n_contract,
                   "verdict_counts": dict(verdict_counts),
                   "none_check_counts": dict(none_counts),
                   "cache_hit_rate": round(tot_cached/max(tot_in,1), 4),
                   "mean_output_tokens": round(tot_out/n, 1),
                   "mean_reasoning_tokens": round(tot_reas/n, 1),
                   "spend_usd": round(spend, 6), "usd_per_row": round(per, 8)}
        (Path(OUT_DIR) / f"{tag}_summary.json").write_text(
            json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"next: open dp_adjudicator.html and load {adj_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--actual", action="store_true")
    a = ap.parse_args()
    if a.dry:
        dry_run()
    elif a.actual:
        actual_run()
    else:
        ap.error("pass --dry or --actual")