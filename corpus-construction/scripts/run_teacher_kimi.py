#!/usr/bin/env python3
"""
run_teacher_kimi.py -- run the teacher prompt over the tuning 50 on Kimi K3.

    python run_teacher_kimi.py --dry       one weather call with search, then a cache probe
    python run_teacher_kimi.py --actual    labels the 50

Needs:  pip install openai requests   (Moonshot's chat surface is OpenAI-compatible;
                                        the Formula API used below for k3 web search is
                                        a separate plain-REST surface, hence requests)

Sequential on purpose, same as the OpenAI runner: Moonshot's automatic prefix caching
rewards a stable prefix sent repeatedly, so cold parallel workers would all miss.

Outputs three files per run, joined on request_id, with the SAME field names the OpenAI
runner writes, so compute_stats.py needs no changes:
    <tag>_responses.jsonl   raw text + parsed JSON
    <tag>_meta.jsonl        usage, cost, latency, status, errors
    <tag>_summary.json      one-line scoreboard row for the bake-off

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
     from the search's trigger fee -- see the PRICING note below.
  2. reasoning_effort is low | high | max, default max. There is no "medium", so this is
     not directly comparable to the Luna sweep. Defaulted to "high".
  3. Caching is automatic prefix caching -- no breakpoint to set, no write charge.
     Stable prefix first, per-review text last, which the prompt already does.
  4. K3 always reasons; thinking cannot be turned off, only turned down. Multi-turn tool
     loops on k3 need the assistant's reasoning_content preserved across rounds, not
     just role/content/tool_calls -- run_review() echoes the full message dump (not a
     filtered subset) for that reason; see the comment at the echo line below.
"""

from __future__ import annotations
import argparse, hashlib, json, os, re, sys, time, uuid
from datetime import datetime
from pathlib import Path
import requests
from openai import OpenAI

sys.path.insert(0, str(Path(__file__).parent))
from build_prompt import load_prompt

# ============================== CONFIG ==============================
MODEL            = "kimi-k3"
REASONING_EFFORT = "high"          # low | high | max   (KIMI DIFF 2; no "medium")
BASE_URL         = "https://api.moonshot.ai/v1"
PROMPT_FILE      = "../outputs/prompts/teacher_v1.txt"
REVIEW_FILE      = "../tuning/tuning_set_50_blind.jsonl"   # blind: no gold in this process
OUT_DIR          = "../outputs/runs/kimi"
WEB_SEARCH       = True
MAX_OUTPUT       = 8192            # reasoning counts against this; too low = truncated JSON
SEND_TEMPERATURE = False           # K3 is a reasoning model; leave off unless you decide
TEMPERATURE      = 0.0
RETRIES          = 3
LIMIT            = 0               # 0 = all; set 3 or 20 for a partial actual run

# KIMI DIFF 1: your frozen policy is one search per review. The loop enforces it: after
# MAX_TOOL_ROUNDS the next call goes out with tool_choice="none" so the model must answer.
MAX_TOOL_ROUNDS  = 1

# KIMI DIFF 1 (k3 path): the web-search tool for k3 lives behind the Formula API, not
# the $web_search builtin -- see the module docstring. The declaration is static, so
# it's fetched once per run (get_web_search_tools) and reused for every call in the loop.
FORMULA_URI      = "moonshot/web-search:latest"

API_KEY_ENV      = "MOONSHOT_API_KEY"
ENV_FILE         = ".env"          # optional: KEY=value lines, gitignored

# USD per million tokens. Check the pricing page on the day you run and record the date;
# these move, and the paper needs the rates that were live for the run.
PRICING = {
    "model": "kimi-k3",
    "as_of": "2026-08-21",
    "input": 3.00,             # cache miss
    "cached_input": 0.30,      # cache hit, 0.1x
    "cache_write": 0.0,        # automatic caching: no write charge
    "output": 15.00,
    # $0.005 is Moonshot's confirmed fee for the $web_search BUILTIN's trigger
    # (platform.kimi.ai/docs/pricing/tools). This run uses the Formula channel instead
    # (moonshot/web-search:latest); its fiber-execution fee was NOT separately confirmed
    # at write time -- check the pricing page before trusting spend totals from a run.
    "search_per_call": 0.005,
}
PROJECT_TO = 200_000           # for the end-of-run projection
# ====================================================================


def get_client() -> tuple["OpenAI", str]:
    """Key resolution: real environment first, then .env in the script's directory.
    Never hardcode the key in this file - it goes to git and into the paper repo.
    Returns (client, key) -- the raw key is also needed for the Formula API's plain
    HTTP endpoints below, which sit outside the openai SDK's chat-completions surface."""
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
    return OpenAI(api_key=key, base_url=BASE_URL), key


def formula_call(key: str, method: str, path: str, body: dict | None = None) -> dict:
    """Raw HTTP call to a Formula API endpoint (GET .../tools, POST .../fibers). These
    are separate REST endpoints alongside /chat/completions, not part of the OpenAI-
    compatible chat surface, so the openai SDK client doesn't reach them -- plain
    requests, same bearer auth as everything else."""
    url = BASE_URL + path
    for attempt in range(RETRIES):
        try:
            resp = requests.request(
                method, url,
                headers={"Authorization": f"Bearer {key}"},
                json=body, timeout=30,
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            if attempt == RETRIES - 1:
                raise
            wait = 2 ** attempt
            print(f"    retry {attempt+1} after formula call error ({e}) (sleep {wait}s)",
                  file=sys.stderr)
            time.sleep(wait)


def get_web_search_tools(key: str) -> list:
    """Fetch the 'web_search' function declaration for the Formula channel. Static per
    run -- callers fetch this once and pass it into every run_review() call."""
    data = formula_call(key, "GET", f"/formulas/{FORMULA_URI}/tools")
    return data["tools"]


def run_formula_search(key: str, tool_call) -> str:
    """Execute one web_search tool call server-side via the Formula API and return the
    real result content as a string, ready to drop straight into a role=tool message.
    This is the step the old $web_search builtin used to do for you automatically on
    the round-2 /chat/completions call; on k3 that automatic path 400s, so you run it
    yourself here (this call is where the fiber-execution fee is billed)."""
    fiber = formula_call(key, "POST", f"/formulas/{FORMULA_URI}/fibers",
                         {"name": tool_call.function.name,
                          "arguments": tool_call.function.arguments})
    ctx = fiber.get("context", {})
    return ctx.get("output") or ctx.get("encrypted_output") or ""


def cost_usd(u: dict, n_searches: int) -> dict:
    """Cost of one REVIEW (summed across the tool loop). Cached and uncached input are
    disjoint. Reasoning tokens are inside completion_tokens and bill at the output rate.
    n_searches counts fiber-execution calls, billed separately from chat tokens."""
    c_cached = u["cached_tokens"]         * PRICING["cached_input"] / 1e6
    c_plain  = u["uncached_input_tokens"] * PRICING["input"]        / 1e6
    c_out    = u["output_tokens"]         * PRICING["output"]       / 1e6
    c_search = n_searches * PRICING["search_per_call"]
    return {"cached": round(c_cached, 8), "cache_write": 0.0,
            "uncached_input": round(c_plain, 8), "output": round(c_out, 8),
            "search": round(c_search, 8),
            "total": round(c_cached + c_plain + c_out + c_search, 8)}


def build_kwargs(messages: list, use_tools: bool, tools_list: list | None) -> dict:
    kw = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": MAX_OUTPUT,          # chat-completions name, not max_output_tokens
    }
    if REASONING_EFFORT:
        kw["reasoning_effort"] = REASONING_EFFORT   # top-level on K3, not nested
    if WEB_SEARCH and tools_list:
        kw["tools"] = tools_list                     # resent on every call in the loop
        if not use_tools:
            kw["tool_choice"] = "none"              # forces a final answer at the cap
    if SEND_TEMPERATURE:
        kw["temperature"] = TEMPERATURE
    return kw


def usage_of(resp) -> dict:
    """One API call's usage. Field names match the OpenAI runner so compute_stats.py
    is shared. Moonshot has moved cached_tokens around between versions, so probe both
    the flat field and prompt_tokens_details."""
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


def add_usage(a: dict, b: dict) -> dict:
    """Sum usage across the calls that make up one review."""
    if not a:
        return dict(b)
    out = {k: (a.get(k) or 0) + (b.get(k) or 0) for k in b if k != "total_tokens"}
    out["total_tokens"] = (a.get("total_tokens") or 0) + (b.get("total_tokens") or 0)
    return out


def print_stats(tag: str, u: dict, latency: float) -> None:
    hit = u["cached_tokens"] / u["input_tokens"] if u["input_tokens"] else 0
    print(f"[{datetime.now():%H:%M:%S}] {tag}  "
          f"input={u['input_tokens']:,} cached={u['cached_tokens']:,} ({hit:.0%}) "
          f"output={u['output_tokens']:,} (reasoning={u['reasoning_tokens']:,}) "
          f"{latency:.1f}s")


def one_call(client, messages: list, use_tools: bool, tools_list: list | None):
    """A single API call with retries. Returns (response, latency, error_type)."""
    for attempt in range(RETRIES):
        t0 = time.time()
        try:
            resp = client.chat.completions.create(
                **build_kwargs(messages, use_tools, tools_list))
            return resp, time.time() - t0, None
        except Exception as e:
            etype = type(e).__name__
            if attempt == RETRIES - 1:
                return None, time.time() - t0, f"{etype}: {e}"
            # 429 is Moonshot's common failure at low top-up tiers; back off harder
            wait = 10 * (attempt + 1) if "RateLimit" in etype else 2 ** attempt
            print(f"    retry {attempt+1} after {etype} (sleep {wait}s)", file=sys.stderr)
            time.sleep(wait)


def run_review(client, key: str, tools_list: list | None, system_prompt: str, user_input: str):
    """KIMI DIFF 1 (k3 path): the whole tool loop for ONE review, via the Formula API.

    Returns (text, usage, latency, n_calls, searches, finish_reason, error).
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
        at_cap = rounds >= MAX_TOOL_ROUNDS
        resp, lat, err = one_call(client, messages, use_tools=not at_cap,
                                   tools_list=tools_list)
        total_latency += lat
        n_calls += 1
        if err:
            return None, usage, total_latency, n_calls, searches, None, err

        usage = add_usage(usage, usage_of(resp))
        choice = resp.choices[0]

        if choice.finish_reason != "tool_calls":
            return (choice.message.content, usage, total_latency, n_calls,
                    searches, choice.finish_reason, None)

        # Echo the assistant message back verbatim, unfiltered. K3 requires its own
        # reasoning_content to be replayed across tool rounds (unlike the trimmed
        # role/content/tool_calls-only example in Moonshot's docs, which is not enough
        # for k3's always-on reasoning) -- model_dump keeps everything the SDK parsed.
        messages.append(choice.message.model_dump(exclude_none=True))
        for tc in choice.message.tool_calls or []:
            if tc.function.name == "web_search":
                args = json.loads(tc.function.arguments)
                content = run_formula_search(key, tc)
                searches.append({
                    "query": args.get("query"),
                    "result_chars": len(content),
                    "raw_arguments": args,
                })
            else:
                content = f"Error: unable to find tool by name '{tc.function.name}'"
            messages.append({"role": "tool", "tool_call_id": tc.id,
                             "name": tc.function.name, "content": content})
        rounds += 1


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
    client, key = get_client()
    print(f"model={MODEL}  effort={REASONING_EFFORT}  search={WEB_SEARCH}  "
          f"max_tool_rounds={MAX_TOOL_ROUNDS}")
    print("checking prompt file...")
    prompt = load_prompt(PROMPT_FILE)
    print(f"  {PROMPT_FILE}: {len(prompt):,} chars, ~{len(prompt)//4:,} tokens")
    rows = [json.loads(l) for l in Path(REVIEW_FILE).read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"  {REVIEW_FILE}: {len(rows)} reviews, "
          f"gold present: {'actual_labels' in rows[0]}")

    tools_list = None
    if WEB_SEARCH:
        print(f"fetching web-search tool declaration from formula {FORMULA_URI}...")
        tools_list = get_web_search_tools(key)
        print(f"  got {len(tools_list)} tool(s): "
              f"{[t['function']['name'] for t in tools_list]}")

    # --- stage 1: does the API work, and does the tool loop actually complete? ---
    print("\n[1/2] throwaway call with search (short prompt, below the cache floor)...")
    text, u, lat, n_calls, searches, fin, err = run_review(
        client, key, tools_list,
        "You are a helpful assistant. Answer in one sentence.",
        "Search for today's weather in Guwahati, India.",
    )
    if err:
        print(f"\nFAILED: {err}\nFix the config at the top of this file and rerun --dry.")
        sys.exit(1)
    print(f"  api calls    {n_calls}  (2 means the search loop ran)")
    print(f"  finish       {fin}")
    print(f"  text         {text!r}")
    print(f"  searches     {[s['query'] for s in searches] or 'none'}")
    if searches and searches[0]["result_chars"]:
        print(f"  search result {searches[0]['result_chars']:,} chars fetched via the fiber call")
    print_stats("  stage1", u, lat)

    # --- stage 2: does the real prompt cache? two identical-prefix calls. ---
    print("\n[2/2] automatic caching check: two calls with the real prompt...")
    probe = json.dumps({"game_name": rows[0].get("game_name", ""),
                        "review_text": rows[0].get("review_text", "")}, ensure_ascii=False)
    for n in (1, 2):
        text2, u2, lat2, nc2, s2, fin2, err2 = run_review(client, key, tools_list, prompt, probe)
        if err2:
            print(f"\nFAILED on cache probe: {err2}")
            sys.exit(1)
        print_stats(f"  call {n}", u2, lat2)
        if n == 2:
            hit = u2["cached_tokens"] / max(u2["input_tokens"], 1)
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
            print(f"  parsed JSON on probe: {parse_json(text2)[1]}")
            print(f"  output tokens {u2['output_tokens']:,} "
                  f"(reasoning {u2['reasoning_tokens']:,}) <- this sets the bill")

    print("\nIf caching is OK and the JSON parsed, run:  python run_teacher_kimi.py --actual")


# ------------------------------------------------------------ actual run

def actual_run() -> None:
    client, key = get_client()
    prompt = load_prompt(PROMPT_FILE)
    rows = [json.loads(l) for l in Path(REVIEW_FILE).read_text(encoding="utf-8").splitlines() if l.strip()]
    if LIMIT:
        rows = rows[:LIMIT]

    tools_list = get_web_search_tools(key) if WEB_SEARCH else None

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    tag = f"{MODEL}_{REASONING_EFFORT}_{stamp}"
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    f_resp = open(Path(OUT_DIR) / f"{tag}_responses.jsonl", "w", encoding="utf-8")
    f_meta = open(Path(OUT_DIR) / f"{tag}_meta.jsonl", "w", encoding="utf-8")

    prompt_sha = hashlib.sha256(prompt.encode()).hexdigest()
    print(f"{len(rows)} reviews -> {OUT_DIR}/{tag}_*.jsonl")
    print(f"prompt sha {prompt_sha[:12]}\n")
    n_ok = n_parsed = n_trunc = n_search = n_extra_calls = 0
    spend = 0.0
    all_usage = []

    for i, row in enumerate(rows, 1):
        rid = str(uuid.uuid4())
        payload = json.dumps({"game_name": row.get("game_name", ""),
                              "review_text": row.get("review_text", "")}, ensure_ascii=False)
        text, u, latency, n_calls, searches, fin, err = run_review(
            client, key, tools_list, prompt, payload)

        meta = {"request_id": rid, "review_id": row.get("review_id"),
                "ts": datetime.now().isoformat(timespec="seconds"),
                "provider": "moonshot", "model": MODEL,
                "reasoning_effort": REASONING_EFFORT,
                "prompt_file": PROMPT_FILE, "prompt_sha256": prompt_sha,
                "cache_mode": "automatic", "base_url": BASE_URL,
                "temperature": TEMPERATURE if SEND_TEMPERATURE else "default",
                "web_search": WEB_SEARCH, "web_search_channel": f"formula:{FORMULA_URI}",
                "max_tool_rounds": MAX_TOOL_ROUNDS,
                "pricing": PRICING,
                "latency_s": round(latency, 2), "error_type": err}

        if err:
            rec = {"request_id": rid, "review_id": row.get("review_id"), "error_type": err}
            print(f"  [{i:>2}/{len(rows)}] ERROR {err[:70]}")
        else:
            n_ok += 1
            parsed, note = parse_json(text)
            n_parsed += parsed is not None
            cost = cost_usd(u, len(searches))
            spend += cost["total"]
            all_usage.append(u)
            truncated = fin == "length"
            n_trunc += truncated
            n_search += len(searches) > 0
            n_extra_calls += n_calls - 1
            meta |= {"status": fin,
                     "incomplete_reason": "max_tokens" if truncated else None,
                     "n_api_calls": n_calls,
                     "n_web_searches": len(searches),
                     "search_queries": [s["query"] for s in searches],
                     "search_result_chars": [s["result_chars"] for s in searches],
                     "usage": u, "cost_usd": cost, "parse_note": note,
                     "n_labels": len(parsed.get("labels") or []) if parsed else None}
            rec = {"request_id": rid, "review_id": row.get("review_id"),
                   "raw": text, "parsed": parsed, "parse_note": note,
                   "error_type": None if parsed else "parse_failed"}
            flag = " TRUNCATED" if truncated else ""
            print_stats(f"[{i:>2}/{len(rows)}] {note:<16}", u, latency)
            print(f"       ${cost['total']:.6f}  running ${spend:.4f}  "
                  f"labels={meta['n_labels']}  searches={len(searches)}  "
                  f"calls={n_calls}{flag}")

        f_resp.write(json.dumps(rec, ensure_ascii=False) + "\n")
        f_meta.write(json.dumps(meta, ensure_ascii=False) + "\n")
        f_resp.flush(); f_meta.flush()

    f_resp.close(); f_meta.close()

    print(f"\ndone. ok {n_ok}/{len(rows)}  parsed {n_parsed}/{len(rows)}  "
          f"truncated {n_trunc}  searched {n_search}  extra tool-loop calls {n_extra_calls}")
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
                   "prompt_file": PROMPT_FILE, "provider": "moonshot", "model": MODEL,
                   "reasoning_effort": REASONING_EFFORT, "web_search": WEB_SEARCH,
                   "web_search_channel": f"formula:{FORMULA_URI}",
                   "cache_mode": "automatic", "max_tool_rounds": MAX_TOOL_ROUNDS,
                   "temperature": TEMPERATURE if SEND_TEMPERATURE else "default",
                   "pricing": PRICING, "ok": n_ok, "parsed": n_parsed,
                   "truncated": n_trunc, "searched": n_search,
                   "extra_tool_loop_calls": n_extra_calls,
                   "cache_hit_rate": round(tot_cached/max(tot_in,1), 4),
                   "mean_output_tokens": round(tot_out/n, 1),
                   "mean_reasoning_tokens": round(tot_reas/n, 1),
                   "spend_usd": round(spend, 6), "usd_per_review": round(per, 8),
                   f"projected_usd_at_{PROJECT_TO}": round(per*PROJECT_TO, 2)}
        (Path(OUT_DIR) / f"{tag}_summary.json").write_text(
            json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"next: point compute_stats.py at {OUT_DIR}/{tag}_responses.jsonl")


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