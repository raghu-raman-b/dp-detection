#!/usr/bin/env python3
"""
compute_stats.py -- turn one run into a report and a comparable metrics row.

Reads the three files a run produces plus the gold labels, and writes:

    <OUT_ROOT>/<provider>/<model>/<tag>_report.txt      human-readable, everything
    <OUT_ROOT>/<provider>/<model>/metrics.jsonl         one line per run, appended
    <OUT_ROOT>/index.jsonl                              same line, all providers

The index is the bake-off scoreboard: every run from every provider, one row each,
so a later comparison script never has to re-parse raw responses.

Metric stack (why these, at n=50):
  micro-F1          primary; stable at this n
  example-based F1  per-review overlap; the analogue of coder agreement
  class macro-F1    5 classes + None; cascade stage 1
  meso macro-F1     ONLY over labels with support >= MIN_SUPPORT
  None P/R          over-labelling is the main failure mode
No macro over all 29 labels: most have support 1-2 and one decision swings it 3+ points.
"""

from __future__ import annotations
import json, statistics, sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

# ============================== CONFIG ==============================
RUN_DIR      = "../outputs/runs/openai"
RUN_TAG      = ""                  # "" = most recent run in RUN_DIR
GOLD_FILE    = "../tuning/tuning_set_50.jsonl"     # the file WITH actual_labels
OUT_ROOT     = "../outputs/run-stats"
PROJECT_TO   = 200_000
MIN_SUPPORT  = 3                   # labels below this are listed, never averaged
TOP_ERRORS   = 12                  # per-review disagreements printed in the report

PROVIDER_OF  = {"gpt": "openai", "claude": "anthropic", "deepseek": "deepseek",
                "kimi": "moonshot", "gemini": "google"}
CLASS_OF     = {"T": "Temporal", "M": "Monetary", "S": "Social",
                "P": "Psychological", "Tech": "Technical"}
# ====================================================================


# ------------------------------------------------------------- helpers

def jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def cls_of(code: str) -> str:
    return CLASS_OF["Tech" if code.startswith("Tech_") else code.split("_", 1)[0]]


def prf(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return p, r, (2 * p * r / (p + r) if p + r else 0.0)


def provider_of(model: str) -> str:
    for k, v in PROVIDER_OF.items():
        if k in model.lower():
            return v
    return "unknown"


def find_run(run_dir: Path, tag: str) -> str:
    if tag:
        return tag
    files = sorted(run_dir.glob("*_responses.jsonl"))
    if not files:
        sys.exit(f"no *_responses.jsonl in {run_dir}")
    return files[-1].name.replace("_responses.jsonl", "")


def pct(x: float) -> str:
    return f"{100*x:5.1f}%"


# --------------------------------------------------------------- gold

def load_gold(path: Path) -> tuple[dict[str, set[str]], dict[str, str]]:
    gold, text = {}, {}
    for row in jsonl(path):
        labs = row.get("actual_labels")
        if labs is None:
            labs = [l.strip() for l in (row.get("actual_labels_str") or "").split(";") if l.strip()]
        gold[row["review_id"]] = {l for l in labs if l}
        text[row["review_id"]] = row.get("review_text", "")
    return gold, text


# ---------------------------------------------------------- validation

def validate(parsed: dict | None, review_text: str, legal: set[str]) -> dict:
    v = {"bad_codes": [], "dup_codes": [], "missing_span": [],
         "span_bad": [], "span_loose": [], "labels": set()}
    if not parsed:
        return v
    seen = []
    for item in parsed.get("labels") or []:
        if not isinstance(item, dict):
            v["bad_codes"].append(str(item)[:40])
            continue
        code, span = item.get("label"), item.get("span")
        if code not in legal:
            v["bad_codes"].append(str(code))
            continue
        if code in seen:
            v["dup_codes"].append(code)          # R1
        seen.append(code)
        v["labels"].add(code)
        if not span:
            v["missing_span"].append(code)       # R3
        elif span not in review_text:
            norm = lambda s: " ".join(s.split()).lower()
            (v["span_loose"] if norm(span) in norm(review_text) else v["span_bad"]).append(code)
    return v


# ---------------------------------------------------------------- main

def main() -> None:
    run_dir = Path(RUN_DIR)
    tag = find_run(run_dir, RUN_TAG)
    resp = {r["request_id"]: r for r in jsonl(run_dir / f"{tag}_responses.jsonl")}
    meta = {m["request_id"]: m for m in jsonl(run_dir / f"{tag}_meta.jsonl")}
    gold, gold_text = load_gold(Path(GOLD_FILE))
    legal = {c for s in gold.values() for c in s}

    any_meta = next(iter(meta.values()))
    model = any_meta.get("model", "unknown")
    provider = provider_of(model)

    # ---- per-request roll-up -------------------------------------------------
    pred, val = {}, {}
    comp = Counter()
    lat, costs, usage_rows = [], [], []
    parse_notes, err_types, statuses = Counter(), Counter(), Counter()
    searched_ids = []

    for rid, m in meta.items():
        comp["n"] += 1
        r = resp.get(rid, {})
        review_id = m.get("review_id")
        if m.get("error_type"):
            comp["api_error"] += 1
            err_types[m["error_type"].split(":")[0]] += 1
            continue
        comp["ok"] += 1
        lat.append(m.get("latency_s", 0))
        if m.get("cost_usd"):
            costs.append(m["cost_usd"])
        if m.get("usage"):
            usage_rows.append(m["usage"])
        parse_notes[r.get("parse_note", "?")] += 1
        statuses[m.get("status") or "?"] += 1
        comp["truncated"] += m.get("status") == "incomplete"
        if m.get("n_web_searches"):
            comp["searched"] += 1
            searched_ids.append(review_id)

        parsed = r.get("parsed")
        comp["parsed"] += parsed is not None
        v = validate(parsed, gold_text.get(review_id, ""), legal)
        val[review_id] = v
        for k in ("bad_codes", "dup_codes", "missing_span", "span_bad", "span_loose"):
            comp[k] += len(v[k])
        comp["labels_emitted"] += len(v["labels"])
        if parsed is not None:
            pred[review_id] = v["labels"]

    ids = [i for i in gold if i in pred]
    if not ids:
        sys.exit("no scorable rows; check GOLD_FILE and review_id join")

    # ---- quality -------------------------------------------------------------
    tp = sum(len(pred[i] & gold[i]) for i in ids)
    fp = sum(len(pred[i] - gold[i]) for i in ids)
    fn = sum(len(gold[i] - pred[i]) for i in ids)
    mp, mr, mf = prf(tp, fp, fn)
    exact = sum(pred[i] == gold[i] for i in ids) / len(ids)
    ex_f1 = sum(2 * len(pred[i] & gold[i]) / (len(pred[i]) + len(gold[i]))
                if (pred[i] or gold[i]) else 1.0 for i in ids) / len(ids)

    per = {}
    for c in sorted(legal):
        t = sum(c in pred[i] and c in gold[i] for i in ids)
        a = sum(c in pred[i] and c not in gold[i] for i in ids)
        b = sum(c not in pred[i] and c in gold[i] for i in ids)
        per[c] = (*prf(t, a, b), t + b)
    scored = {c: v for c, v in per.items() if v[3] >= MIN_SUPPORT}
    meso_macro = statistics.mean([v[2] for v in scored.values()]) if scored else 0.0

    crows = []
    for k in sorted(set(CLASS_OF.values())):
        has = lambda s: any(cls_of(c) == k for c in s)
        t = sum(has(pred[i]) and has(gold[i]) for i in ids)
        a = sum(has(pred[i]) and not has(gold[i]) for i in ids)
        b = sum(not has(pred[i]) and has(gold[i]) for i in ids)
        crows.append((k, *prf(t, a, b), t + b))
    nt = sum(not pred[i] and not gold[i] for i in ids)
    nfp = sum(bool(not pred[i] and gold[i]) for i in ids)
    nfn = sum(bool(pred[i] and not gold[i]) for i in ids)
    np_, nr_, nf_ = prf(nt, nfp, nfn)
    crows.append(("None", np_, nr_, nf_, nt + nfn))
    class_macro = statistics.mean([x[3] for x in crows])

    over = Counter(c for i in ids for c in pred[i] - gold[i])
    under = Counter(c for i in ids for c in gold[i] - pred[i])
    confusion = Counter()
    for i in ids:
        for a in gold[i] - pred[i]:
            for b in pred[i] - gold[i]:
                confusion[tuple(sorted((a, b)))] += 1

    # ---- cost and ops --------------------------------------------------------
    spend = sum(c["total"] for c in costs)
    usd_per_review = spend / max(len(costs), 1)
    tok = {k: sum(u.get(k, 0) or 0 for u in usage_rows) for k in
           ("input_tokens", "cached_tokens", "cache_write_tokens",
            "uncached_input_tokens", "output_tokens", "reasoning_tokens")}
    hit = tok["cached_tokens"] / max(tok["input_tokens"], 1)
    n_u = max(len(usage_rows), 1)
    cost_share = {k: sum(c.get(k, 0) for c in costs) / spend if spend else 0
                  for k in ("cached", "cache_write", "uncached_input", "output")}
    lat_s = sorted(lat) or [0]
    p50, p95 = lat_s[len(lat_s)//2], lat_s[max(int(len(lat_s)*0.95)-1, 0)]

    # ---- report --------------------------------------------------------------
    L = []
    add = L.append
    add("=" * 78)
    add(f"RUN REPORT  {tag}")
    add("=" * 78)
    add(f"generated        {datetime.now().isoformat(timespec='seconds')}")
    add(f"provider/model   {provider} / {model}  (served: {any_meta.get('model_version')})")
    add(f"reasoning        {any_meta.get('reasoning_effort')}")
    add(f"web search       {any_meta.get('web_search')}")
    add(f"prompt           {any_meta.get('prompt_file')}")
    add(f"prompt sha256    {any_meta.get('prompt_sha256')}")
    add(f"cache key/mode   {any_meta.get('cache_key')} / {any_meta.get('cache_mode')}")
    add(f"gold             {GOLD_FILE}")
    add(f"scored           {len(ids)} of {comp['n']} requests")
    add("")

    add("-" * 78)
    add("RELIABILITY")
    add("-" * 78)
    add(f"  requests          {comp['n']}")
    add(f"  ok / api errors   {comp['ok']} / {comp['api_error']}")
    add(f"  parsed JSON       {comp['parsed']}/{comp['ok']}")
    add(f"  truncated         {comp['truncated']}"
        + ("   <-- RAISE MAX_OUTPUT, DO NOT SCORE THIS RUN" if comp["truncated"] else ""))
    add(f"  parse notes       {dict(parse_notes)}")
    add(f"  statuses          {dict(statuses)}")
    if err_types:
        add(f"  error types       {dict(err_types)}")
    add("")

    add("-" * 78)
    add("CODEBOOK COMPLIANCE")
    add("-" * 78)
    add(f"  labels emitted            {comp['labels_emitted']}")
    add(f"  out-of-vocabulary codes   {comp['bad_codes']}")
    add(f"  duplicate labels (R1)     {comp['dup_codes']}")
    add(f"  labels with no span (R3)  {comp['missing_span']}")
    add(f"  span not in review        {comp['span_bad']}")
    add(f"  span matched only loosely {comp['span_loose']}")
    denom = max(comp["labels_emitted"], 1)
    add(f"  span verbatim rate        {pct(1 - (comp['span_bad']+comp['missing_span'])/denom)}")
    add("")

    add("-" * 78)
    add("QUALITY")
    add("-" * 78)
    add(f"  micro-F1            {mf:.3f}   (P {mp:.3f} / R {mr:.3f})   tp {tp} fp {fp} fn {fn}")
    add(f"  example-based F1    {ex_f1:.3f}")
    add(f"  exact set match     {exact:.3f}")
    add(f"  class macro-F1      {class_macro:.3f}   (5 classes + None)")
    add(f"  meso macro-F1       {meso_macro:.3f}   over {len(scored)} labels, support >= {MIN_SUPPORT}")
    add(f"  None P/R/F1         {np_:.3f} / {nr_:.3f} / {nf_:.3f}   (support {nt+nfn})")
    add("")
    add("  class                     P      R     F1   supp")
    for k, p, r, f, s in crows:
        add(f"    {k:<20} {p:6.3f} {r:6.3f} {f:6.3f}  {s:>4}")
    add("")
    add(f"  per-label (* = support < {MIN_SUPPORT}, excluded from meso macro)")
    add("    label                                 P      R     F1   supp")
    for c, (p, r, f, s) in sorted(per.items(), key=lambda kv: (-kv[1][3], kv[0])):
        mark = " " if s >= MIN_SUPPORT else "*"
        add(f"  {mark} {c:<34} {p:6.3f} {r:6.3f} {f:6.3f}  {s:>4}")
    add("")

    add("-" * 78)
    add("ERROR TAXONOMY")
    add("-" * 78)
    add(f"  over-labelled  (predicted, not in gold)")
    for c, n in over.most_common(TOP_ERRORS):
        add(f"    {c:<36} {n}")
    add(f"  under-labelled (in gold, not predicted)")
    for c, n in under.most_common(TOP_ERRORS):
        add(f"    {c:<36} {n}")
    if confusion:
        add("  co-occurring miss/false-positive pairs")
        for (a, b), n in confusion.most_common(TOP_ERRORS):
            add(f"    {a} ~ {b}   {n}")
    add("")
    add(f"  reviews with disagreements (first {TOP_ERRORS})")
    shown = 0
    for i in ids:
        if pred[i] == gold[i] or shown >= TOP_ERRORS:
            continue
        shown += 1
        add(f"    {i}")
        add(f"      gold: {sorted(gold[i]) or ['NONE']}")
        add(f"      pred: {sorted(pred[i]) or ['NONE']}")
    add("")
    add("  triage each into: over / under / confusion / codebook-does-not-rule.")
    add("  the last bucket is a v0.21 codebook edit, NOT a prompt edit.")
    add("")

    add("-" * 78)
    add("COST")
    add("-" * 78)
    pr = any_meta.get("pricing", {})
    add(f"  rates as of       {pr.get('as_of')}  "
        f"in {pr.get('input')} / cached {pr.get('cached_input')} / "
        f"write {pr.get('cache_write')} / out {pr.get('output')} per MTok")
    add(f"  input tokens      {tok['input_tokens']:,}  "
        f"(cached {tok['cached_tokens']:,}, written {tok['cache_write_tokens']:,}, "
        f"plain {tok['uncached_input_tokens']:,})")
    add(f"  output tokens     {tok['output_tokens']:,}  "
        f"(reasoning {tok['reasoning_tokens']:,}, "
        f"{100*tok['reasoning_tokens']/max(tok['output_tokens'],1):.0f}% of output)")
    add(f"  mean per review   in {tok['input_tokens']/n_u:,.0f}  out {tok['output_tokens']/n_u:,.0f}  "
        f"reasoning {tok['reasoning_tokens']/n_u:,.0f}")
    add(f"  cache hit rate    {hit:.3f}")
    add(f"  total spend       ${spend:.4f}")
    add(f"  per review        ${usd_per_review:.6f}")
    add(f"  cost split        " + "  ".join(f"{k} {pct(v)}" for k, v in cost_share.items()))
    add(f"  projected {PROJECT_TO:,}  ${usd_per_review*PROJECT_TO:,.2f}")
    if mf:
        add(f"  micro-F1 per $ at {PROJECT_TO:,}   {mf/(usd_per_review*PROJECT_TO):.5f}")
    add("")

    add("-" * 78)
    add("THROUGHPUT")
    add("-" * 78)
    add(f"  latency p50/p95   {p50:.2f}s / {p95:.2f}s   mean {statistics.mean(lat or [0]):.2f}s")
    add(f"  sequential {PROJECT_TO:,}  {PROJECT_TO*statistics.mean(lat or [0])/3600:,.0f} h")
    add(f"  web searches      {comp['searched']}/{comp['ok']} reviews ({pct(comp['searched']/max(comp['ok'],1))})")
    if searched_ids:
        add(f"    ids: {', '.join(searched_ids[:8])}{' ...' if len(searched_ids) > 8 else ''}")
    add("")
    add("=" * 78)

    # ---- write ---------------------------------------------------------------
    out_dir = Path(OUT_ROOT) / provider / model
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{tag}_report.txt").write_text("\n".join(L) + "\n", encoding="utf-8")

    row = {
        "tag": tag,
        "generated": datetime.now().isoformat(timespec="seconds"),
        "provider": provider, "model": model,
        "model_version": any_meta.get("model_version"),
        "reasoning_effort": any_meta.get("reasoning_effort"),
        "web_search": any_meta.get("web_search"),
        "prompt_file": any_meta.get("prompt_file"),
        "prompt_sha256": any_meta.get("prompt_sha256"),
        "gold_file": GOLD_FILE, "n_requests": comp["n"], "n_scored": len(ids),
        # quality
        "micro_f1": round(mf, 4), "micro_p": round(mp, 4), "micro_r": round(mr, 4),
        "example_f1": round(ex_f1, 4), "exact_match": round(exact, 4),
        "class_macro_f1": round(class_macro, 4),
        "meso_macro_f1": round(meso_macro, 4), "meso_macro_n_labels": len(scored),
        "none_p": round(np_, 4), "none_r": round(nr_, 4), "none_f1": round(nf_, 4),
        "tp": tp, "fp": fp, "fn": fn,
        "per_label_f1": {c: round(v[2], 4) for c, v in per.items()},
        "per_label_support": {c: v[3] for c, v in per.items()},
        "class_f1": {k: round(f, 4) for k, _, _, f, _ in crows},
        "top_over_labelled": over.most_common(5),
        "top_under_labelled": under.most_common(5),
        # compliance
        "api_errors": comp["api_error"], "parsed": comp["parsed"],
        "truncated": comp["truncated"], "labels_emitted": comp["labels_emitted"],
        "bad_codes": comp["bad_codes"], "dup_labels_r1": comp["dup_codes"],
        "missing_span_r3": comp["missing_span"], "span_not_verbatim": comp["span_bad"],
        "span_loose": comp["span_loose"],
        "span_verbatim_rate": round(1-(comp["span_bad"]+comp["missing_span"])/denom, 4),
        # cost and ops
        "pricing": pr, "tokens": tok, "cache_hit_rate": round(hit, 4),
        "mean_output_tokens": round(tok["output_tokens"]/n_u, 1),
        "mean_reasoning_tokens": round(tok["reasoning_tokens"]/n_u, 1),
        "spend_usd": round(spend, 6), "usd_per_review": round(usd_per_review, 8),
        f"projected_usd_at_{PROJECT_TO}": round(usd_per_review*PROJECT_TO, 2),
        "cost_share": {k: round(v, 4) for k, v in cost_share.items()},
        "latency_p50": round(p50, 2), "latency_p95": round(p95, 2),
        "latency_mean": round(statistics.mean(lat or [0]), 2),
        "search_rate": round(comp["searched"]/max(comp["ok"], 1), 4),
    }
    line = json.dumps(row, ensure_ascii=False) + "\n"
    with open(out_dir / "metrics.jsonl", "a", encoding="utf-8") as f:
        f.write(line)
    Path(OUT_ROOT).mkdir(parents=True, exist_ok=True)
    with open(Path(OUT_ROOT) / "index.jsonl", "a", encoding="utf-8") as f:
        f.write(line)

    print("\n".join(L))
    print(f"wrote {out_dir / (tag + '_report.txt')}")
    print(f"appended {out_dir / 'metrics.jsonl'} and {Path(OUT_ROOT) / 'index.jsonl'}")


if __name__ == "__main__":
    main()