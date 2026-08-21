#!/usr/bin/env python3
"""
run_teacher_openai.py -- run the teacher prompt over the tuning 50 on an OpenAI model.

    python run_teacher_openai.py --dry       one weather call with web search, prints stats
    python run_teacher_openai.py --actual    labels the 50

Sequential on purpose: the first call writes the cached prefix and every later call reads
it. Parallel workers launched cold would all miss at once and each pay a cache write.

Outputs three files per run, joined on request_id:
    <tag>_responses.jsonl   raw text + parsed JSON
    <tag>_meta.jsonl        usage, cost, latency, status, errors
    <tag>_summary.json      one-line scoreboard row for the bake-off
"""

from __future__ import annotations
import argparse, hashlib, json, os, re, sys, time, uuid
from datetime import datetime
from pathlib import Path
from openai import OpenAI

sys.path.insert(0, str(Path(__file__).parent))
from build_prompt import load_prompt

# ============================== CONFIG ==============================
MODEL            = "gpt-5.6-luna"
REASONING_EFFORT = "medium"        # none | low | medium | high | xhigh | max
PROMPT_FILE      = "../outputs/prompts/teacher_v1.txt"
REVIEW_FILE      = "../tuning/tuning_set_50_blind.jsonl"   # blind: no gold in this process
OUT_DIR          = "../outputs/runs/openai"
WEB_SEARCH       = True
MAX_OUTPUT       = 8192            # reasoning tokens count against this; too low = empty output
SEND_TEMPERATURE = False           # True only if Luna accepts it
TEMPERATURE      = 0.0
RETRIES          = 3
LIMIT            = 1               # 0 = all; set 3 or 20 for a partial actual run

WEB_SEARCH_TOOL  = {"type": "web_search"}

# GPT-5.6 caching: the implicit breakpoint sits on the LATEST USER MESSAGE, which is a
# different review every call. Without an explicit breakpoint the prefix never matches and
# every request pays a 1.25x cache write. So: prompt goes in a developer message with an
# explicit breakpoint, explicit-only mode stops the review suffix being cached, and a
# stable prompt_cache_key routes requests to the same cache.
CACHE_MODE       = "explicit"      # "explicit" | "implicit"
CACHE_KEY_PREFIX = "dp-teacher"    # prompt sha is appended automatically

API_KEY_ENV      = "OPENAI_API_KEY"
ENV_FILE         = ".env"          # optional: KEY=value lines, gitignored

# USD per million tokens. Check the pricing page on the day you run and record the date;
# these move, and the paper needs the rates that were live for the run.
PRICING = {
    "model": "gpt-5.6-luna",
    "as_of": "2026-08-21",
    "input": 0.20,
    "cached_input": 0.02,      # 0.1x input
    "cache_write": 0.25,       # 1.25x input
    "output": 1.20,
}
PROJECT_TO = 200_000           # for the end-of-run projection
# ====================================================================


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


# --------------------------------------------------------------- dry run

def dry_run() -> None:
    client = get_client()
    print(f"model={MODEL}  effort={REASONING_EFFORT}  web_search={WEB_SEARCH}")
    print("checking prompt file...")
    prompt = load_prompt(PROMPT_FILE)
    print(f"  {PROMPT_FILE}: {len(prompt):,} chars, ~{len(prompt)//4:,} tokens")
    rows = [json.loads(l) for l in Path(REVIEW_FILE).read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"  {REVIEW_FILE}: {len(rows)} reviews, "
          f"gold present: {'actual_labels' in rows[0]}")

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

    # --- stage 2: does the real prompt actually cache? two identical-prefix calls. ---
    print(f"\n[2/2] caching check: two calls with the real prompt "
          f"(key={cache_key(prompt)})...")
    probe = json.dumps({"game_name": rows[0].get("game_name", ""),
                        "review_text": rows[0].get("review_text", "")}, ensure_ascii=False)
    for n in (1, 2):
        r2, lat2, err2 = call(client, prompt, probe, cached=True)
        if err2:
            print(f"\nFAILED on cache probe: {err2}")
            print("If this is a 400 on prompt_cache_breakpoint, check the block type and mode.")
            sys.exit(1)
        u2 = usage_dict(r2)
        print_stats(f"  call {n}", u2, lat2)
        if n == 1:
            first = u2
        else:
            hit = u2["cached_tokens"] / max(u2["input_tokens"], 1)
            print()
            if hit > 0.8:
                print(f"  CACHING OK: {hit:.0%} of input read from cache on the second call.")
            else:
                print(f"  CACHING BROKEN: only {hit:.0%} cached on call 2.")
                print("  Check: is the prefix >= 1024 tokens, is the breakpoint on the developer")
                print("  input_text block, is prompt_cache_key identical, did tools change?")
            print(f"  parsed JSON on probe: {parse_json(r2.output_text)[1]}")
            print(f"  output tokens {u2['output_tokens']:,} "
                  f"(reasoning {u2['reasoning_tokens']:,}) <- this sets the bill")

    print("\nIf caching is OK and the JSON parsed, run:  python run_teacher_openai.py --actual")


# ------------------------------------------------------------ actual run

def actual_run() -> None:
    client = get_client()
    prompt = load_prompt(PROMPT_FILE)
    rows = [json.loads(l) for l in Path(REVIEW_FILE).read_text(encoding="utf-8").splitlines() if l.strip()]
    if LIMIT:
        rows = rows[:LIMIT]

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    tag = f"{MODEL}_{REASONING_EFFORT}_{stamp}"
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    f_resp = open(Path(OUT_DIR) / f"{tag}_responses.jsonl", "w", encoding="utf-8")
    f_meta = open(Path(OUT_DIR) / f"{tag}_meta.jsonl", "w", encoding="utf-8")

    prompt_sha = hashlib.sha256(prompt.encode()).hexdigest()
    print(f"{len(rows)} reviews -> {OUT_DIR}/{tag}_*.jsonl")
    print(f"prompt sha {prompt_sha[:12]}  cache key {cache_key(prompt)}\n")
    n_ok = n_parsed = n_trunc = n_search = 0
    spend = 0.0
    all_usage = []

    for i, row in enumerate(rows, 1):
        rid = str(uuid.uuid4())
        payload = json.dumps({"game_name": row.get("game_name", ""),
                              "review_text": row.get("review_text", "")}, ensure_ascii=False)
        resp, latency, err = call(client, prompt, payload)

        meta = {"request_id": rid, "review_id": row.get("review_id"),
                "ts": datetime.now().isoformat(timespec="seconds"),
                "model": MODEL, "reasoning_effort": REASONING_EFFORT,
                "prompt_file": PROMPT_FILE, "prompt_sha256": prompt_sha,
                "cache_key": cache_key(prompt), "cache_mode": CACHE_MODE,
                "web_search": WEB_SEARCH, "pricing": PRICING,
                "latency_s": round(latency, 2), "error_type": err}

        if err:
            rec = {"request_id": rid, "review_id": row.get("review_id"), "error_type": err}
            print(f"  [{i:>2}/{len(rows)}] ERROR {err[:70]}")
        else:
            n_ok += 1
            text = resp.output_text
            parsed, note = parse_json(text)
            n_parsed += parsed is not None
            u = usage_dict(resp)
            cost = cost_usd(u)
            rm = response_meta(resp)
            spend += cost["total"]
            all_usage.append(u)
            n_trunc += rm["status"] == "incomplete"
            n_search += rm["n_web_searches"] > 0
            meta |= {**rm, "usage": u, "cost_usd": cost, "parse_note": note,
                     "n_labels": len(parsed.get("labels") or []) if parsed else None}
            rec = {"request_id": rid, "review_id": row.get("review_id"),
                   "raw": text, "parsed": parsed, "parse_note": note,
                   "error_type": None if parsed else "parse_failed"}
            flag = " TRUNCATED" if rm["status"] == "incomplete" else ""
            print_stats(f"[{i:>2}/{len(rows)}] {note:<16}", u, latency)
            print(f"       ${cost['total']:.6f}  running ${spend:.4f}  "
                  f"labels={meta['n_labels']}  searches={rm['n_web_searches']}{flag}")

        f_resp.write(json.dumps(rec, ensure_ascii=False) + "\n")
        f_meta.write(json.dumps(meta, ensure_ascii=False) + "\n")
        f_resp.flush(); f_meta.flush()

    f_resp.close(); f_meta.close()

    print(f"\ndone. ok {n_ok}/{len(rows)}  parsed {n_parsed}/{len(rows)}  "
          f"truncated {n_trunc}  searched {n_search}")
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
        print(f"  spend           ${spend:.4f}   ${per:.6f}/review")
        print(f"  projected {PROJECT_TO:,}: ${per*PROJECT_TO:,.0f} "
              f"(rates as of {PRICING['as_of']})")
        summary = {"tag": tag, "n": n, "prompt_sha256": prompt_sha,
                   "prompt_file": PROMPT_FILE, "model": MODEL,
                   "reasoning_effort": REASONING_EFFORT, "web_search": WEB_SEARCH,
                   "pricing": PRICING, "ok": n_ok, "parsed": n_parsed,
                   "truncated": n_trunc, "searched": n_search,
                   "cache_hit_rate": round(tot_cached/max(tot_in,1), 4),
                   "mean_output_tokens": round(tot_out/n, 1),
                   "mean_reasoning_tokens": round(tot_reas/n, 1),
                   "spend_usd": round(spend, 6), "usd_per_review": round(per, 8),
                   f"projected_usd_at_{PROJECT_TO}": round(per*PROJECT_TO, 2)}
        (Path(OUT_DIR) / f"{tag}_summary.json").write_text(
            json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"next: point score.py at {OUT_DIR}/{tag}_responses.jsonl")


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