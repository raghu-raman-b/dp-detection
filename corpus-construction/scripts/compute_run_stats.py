#!/usr/bin/env python3
"""
compute_stats.py -- turn one run into a report, an error-review sheet, and a metrics row.

With no arguments it scores EVERY run under outputs/runs and overwrites what was there
before, mirroring that tree path-for-path:

    outputs/runs/     <model>/<effort>/<prompt>/<tag>_responses.jsonl
    outputs/run-stats/<model>/<effort>/<prompt>/<tag>_report.txt      full numeric report
                                                <tag>_errors.md      every disagreement
                                                <tag>_perreview.jsonl  gold vs pred
                                                <tag>_metrics.json   the metrics row
    outputs/run-stats/index.jsonl                                    one row per run

index.jsonl is REBUILT from the runs discovered on each pass, never appended: rescoring
everything with an append would give you N copies of every row on the Nth pass. Rebuilding
from the discovered runs is also what drops stats whose run has since been deleted -- the
orphaned directory stays on disk, but it cannot leak into a comparison.

Metric stack at n=50:
  micro-F1          primary tuning signal
  example-based F1  per-review overlap; analogue of coder agreement
  class macro-F1    5 classes + None; cascade stage 1
  meso macro-F1     only over labels with support >= MIN_SUPPORT
  None P/R          over-labelling is the main failure mode
No macro over all 29 labels: most have support 1-2 and one decision swings it 3+ points.
"""

from __future__ import annotations
import argparse, json, re, statistics, sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from runner_common import discover_runs, resolve, run_tags, show  # shared with the runners
from build_prompt import derive_code                              # codebook code derivation

# ============================== CONFIG ==============================
# Defaults only -- everything here is overridable on the command line, because the run
# tree now has a directory per (model, effort, prompt) and hand-editing two constants
# between every scoring pass was the friction that made runs go unscored.
RUNS_ROOT    = "../outputs/runs"                   # scored in full when --run-dir is omitted
RUN_TAG      = ""                                  # "" = the only/most recent run in the dir
GOLD_FILE    = "../tuning/tuning_set_50.jsonl"     # the file WITH actual_labels
CODEBOOK     = "../../codebook_versions/codebook_final.json"  # the legal-code vocabulary
OUT_ROOT     = "../outputs/run-stats"
PROJECT_TO   = 200_000
MIN_SUPPORT  = 3                   # labels below this are listed, never averaged
TOP_ERRORS   = 12                  # disagreements printed in the txt report
WRITE_MD     = True                # markdown triage sheet with every disagreement

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


def pct(x: float) -> str:
    return f"{100*x:5.1f}%"


def pretty(code: str) -> str:
    """T_PlayingByAppointment -> 'Playing By Appointment'."""
    stem = code.split("_", 1)[1] if "_" in code else code
    return re.sub(r"(?<!^)(?=[A-Z])", " ", stem).strip()


def mentioned(code: str, analysis: str) -> bool:
    """Did the model's own analysis name this label at all? Separates 'considered and
    rejected' (rule interpretation) from 'never came up' (attention). Heuristic - the
    markdown prints the analysis so you can confirm each call yourself."""
    if not analysis:
        return False
    t = analysis.lower()
    stem = (code.split("_", 1)[1] if "_" in code else code).lower()
    forms = {code.lower(), stem, pretty(code).lower()}
    words = pretty(code).lower().split()
    if len(words) >= 3:
        forms.add(" ".join(words[:3]))
    return any(f in t for f in forms if len(f) > 3)


def classify(g: set, p: set) -> str:
    if not p and g:
        return "FALSE NONE"
    if p < g:
        return "MISSED ONLY"
    if g < p:
        return "SPURIOUS ONLY"
    return "SWAP"


def load_gold(path: Path):
    gold, text, game = {}, {}, {}
    for row in jsonl(path):
        labs = row.get("actual_labels")
        if labs is None:
            labs = [l.strip() for l in (row.get("actual_labels_str") or "").split(";")]
        gold[row["review_id"]] = {l for l in labs if l}
        text[row["review_id"]] = row.get("review_text", "")
        game[row["review_id"]] = row.get("game_name", "")
    return gold, text, game


def load_legal_codes(path: Path) -> set[str]:
    """The full codebook vocabulary, not the codes this gold sample happens to exercise --
    a label with zero support in a 50-review draw is still legal, and scoring it as an
    'out-of-vocab' code would fail the compliance gate for guessing right on something rare."""
    labels = json.loads(path.read_text(encoding="utf-8"))["labels"]
    return {derive_code(lab) for lab in labels}


def validate(parsed: dict | None, review_text: str, legal: set) -> dict:
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


# ------------------------------------------------------ error-review markdown

def review_card(rid: str, gold_s: set, pred_s: set, text: str, game: str,
                parsed: dict | None, v: dict) -> list[str]:
    miss, extra = sorted(gold_s - pred_s), sorted(pred_s - gold_s)
    items = {i.get("label"): i for i in ((parsed or {}).get("labels") or [])
             if isinstance(i, dict)}
    analysis = (parsed or {}).get("analysis", "") or ""

    L = [f"### `{rid}`" + (f" - {game}" if game else ""), ""]
    L += ["> " + " ".join((text or "").split()), ""]
    L += ["| | labels |", "|---|---|",
          f"| gold | {', '.join(f'`{c}`' for c in sorted(gold_s)) or '_NONE_'} |",
          f"| pred | {', '.join(f'`{c}`' for c in sorted(pred_s)) or '_NONE_'} |"]
    if miss:
        L.append(f"| **missed** | {', '.join(f'`{c}`' for c in miss)} |")
    if extra:
        L.append(f"| **spurious** | {', '.join(f'`{c}`' for c in extra)} |")
    L.append("")

    if miss:
        L += ["**Did the model consider what it missed?**", ""]
        for c in miss:
            if mentioned(c, analysis):
                L.append(f"- `{c}` - considered and rejected -> **rule interpretation**")
            else:
                L.append(f"- `{c}` - never mentioned -> **attention / recall**")
        L.append("")

    L += ["**Model analysis**", "", "```", analysis.strip() or "(empty)", "```", ""]

    if items:
        L += ["**Labels assigned**", ""]
        for c in sorted(items):
            it = items[c]
            verdict = "ok" if c in gold_s else "**SPURIOUS**"
            flags = []
            if c in v.get("span_bad", []):
                flags.append("span not verbatim")
            if c in v.get("span_loose", []):
                flags.append("span loose match")
            if c in v.get("missing_span", []):
                flags.append("no span (R3)")
            tail = f"  _[{'; '.join(flags)}]_" if flags else ""
            L.append(f"- `{c}` - {verdict}{tail}")
            L.append(f"  - span: \"{' '.join((it.get('span') or '').split())}\"")
            if it.get("rationale"):
                L.append(f"  - why: {' '.join(it['rationale'].split())}")
        L.append("")

    if (parsed or {}).get("invoked_web_search"):
        L += [f"**Search:** `{parsed.get('search_query')}` -> {parsed.get('search_result')}", ""]

    L += ["`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  "
          "`[ ] codebook gap -> v0.21`  `[ ] gold was wrong`", "", "---", ""]
    return L


def write_error_review(path: Path, tag: str, meta0: dict, ids, gold, pred,
                       gold_text, gold_game, parsed_by_review, val,
                       mf: float, mp: float, mr: float) -> None:
    buckets = defaultdict(list)
    for i in ids:
        if gold[i] != pred[i]:
            buckets[classify(gold[i], pred[i])].append(i)
    order = ["FALSE NONE", "SWAP", "MISSED ONLY", "SPURIOUS ONLY"]
    n_wrong = sum(len(buckets[k]) for k in order)

    seen_dropped = never_seen = 0
    by_seen, by_unseen = Counter(), Counter()
    for i in ids:
        a = (parsed_by_review.get(i) or {}).get("analysis", "") or ""
        for c in gold[i] - pred[i]:
            if mentioned(c, a):
                seen_dropped += 1
                by_seen[c] += 1
            else:
                never_seen += 1
                by_unseen[c] += 1
    tot = seen_dropped + never_seen

    L = [f"# Error review - {tag}", "",
         f"`{meta0.get('model')}` / reasoning `{meta0.get('reasoning_effort')}` / "
         f"search `{meta0.get('web_search')}`  ",
         f"prompt `{meta0.get('prompt_file')}` sha `{(meta0.get('prompt_sha256') or '')[:12]}`  ",
         f"micro-F1 **{mf:.3f}** (P {mp:.3f} / R {mr:.3f}) - "
         f"**{n_wrong} of {len(ids)}** reviews disagree", "",
         "| pattern | n | meaning |", "|---|---|---|",
         f"| FALSE NONE | {len(buckets['FALSE NONE'])} | said NONE, gold had labels |",
         f"| SWAP | {len(buckets['SWAP'])} | picked different labels than gold |",
         f"| MISSED ONLY | {len(buckets['MISSED ONLY'])} | everything predicted was right, "
         "but incomplete |",
         f"| SPURIOUS ONLY | {len(buckets['SPURIOUS ONLY'])} | found all gold, added extras |",
         ""]

    if tot:
        L += ["## The diagnostic that matters", "",
              f"Of **{tot}** missed labels, **{seen_dropped}** ({100*seen_dropped/tot:.0f}%) "
              "were named in the model's own analysis and dropped anyway; "
              f"**{never_seen}** ({100*never_seen/tot:.0f}%) never came up at all.", "",
              "> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or "
              "the codebook boundary rule.  ",
              "> Never-named is **attention**: raise reasoning effort, or split the label "
              "list (the 1+4 cascade). Prompt wording will not help.", ""]
        if by_seen or by_unseen:
            L += ["| label | named then dropped | never named |", "|---|---|---|"]
            for c in sorted(set(by_seen) | set(by_unseen),
                            key=lambda c: -(by_seen[c] + by_unseen[c])):
                L.append(f"| `{c}` | {by_seen[c]} | {by_unseen[c]} |")
            L.append("")

    titles = {"FALSE NONE": "Missed everything (predicted NONE)",
              "SWAP": "Swapped labels",
              "MISSED ONLY": "Under-labelled (incomplete, nothing wrong)",
              "SPURIOUS ONLY": "Over-labelled"}
    for k in order:
        if not buckets[k]:
            continue
        L += [f"## {titles[k]} ({len(buckets[k])})", ""]
        for i in buckets[k]:
            L += review_card(i, gold[i], pred[i], gold_text.get(i, ""),
                             gold_game.get(i, ""), parsed_by_review.get(i),
                             val.get(i, {}))

    miss_by, extra_by = defaultdict(list), defaultdict(list)
    for i in ids:
        for c in gold[i] - pred[i]:
            miss_by[c].append(i)
        for c in pred[i] - gold[i]:
            extra_by[c].append(i)
    L += ["## By label", "", "| label | missed | spurious |", "|---|---|---|"]
    for c in sorted(set(miss_by) | set(extra_by),
                    key=lambda c: -(len(miss_by[c]) + len(extra_by[c]))):
        L.append(f"| `{c}` | {len(miss_by[c])} | {len(extra_by[c])} |")
    L.append("")
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- main

def parse_args() -> "argparse.Namespace":
    ap = argparse.ArgumentParser(
        description="Score runs against gold. With no arguments, scores every run under "
                    "outputs/runs and rebuilds the index.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--run-dir", default="",
                    help="score only this run directory (default: score all of them)")
    ap.add_argument("--tag", default=RUN_TAG,
                    help="run tag inside --run-dir; omitted = every tag there")
    ap.add_argument("--gold", default=GOLD_FILE)
    ap.add_argument("--codebook", default=CODEBOOK,
                    help="codebook JSON that defines the legal label vocabulary")
    ap.add_argument("--out-root", default=OUT_ROOT)
    ap.add_argument("--runs-root", default=RUNS_ROOT)
    ap.add_argument("--list", action="store_true",
                    help="list the run directories found and exit")
    return ap.parse_args()


def score_run(run_dir: Path, tag: str, gold_file: Path, gold_bundle: tuple,
              legal: set[str], out_dir: Path, print_report: bool) -> dict | None:
    """Score one run into out_dir and return its metrics row, or None if it is not
    scorable. Returning None rather than exiting matters: in a batch, one unusable run
    must not take the other nineteen down with it."""
    resp = {r["request_id"]: r for r in jsonl(run_dir / f"{tag}_responses.jsonl")
            if not r.get("superseded")}
    # Superseded rows are earlier failed attempts at a review that a --resume pass has
    # since relabelled. They stay on disk as evidence; counting them here would charge
    # the run twice for one review.
    meta = {m["request_id"]: m for m in jsonl(run_dir / f"{tag}_meta.jsonl")
            if not m.get("superseded")}
    gold, gold_text, gold_game = gold_bundle

    if not meta:
        print(f"  SKIP {tag}: no usable rows in {tag}_meta.jsonl")
        return None
    any_meta = next(iter(meta.values()))
    model = any_meta.get("model", "unknown")
    provider = provider_of(model)

    pred, val, parsed_by_review = {}, {}, {}
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
        parsed_by_review[review_id] = parsed
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
        print(f"  SKIP {tag}: no review_id overlaps {show(gold_file)}")
        return None

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

    seen_dropped = sum(
        1 for i in ids for c in gold[i] - pred[i]
        if mentioned(c, (parsed_by_review.get(i) or {}).get("analysis", "") or ""))

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

    # ---- txt report ----------------------------------------------------------
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
    add(f"gold             {gold_file}")
    add(f"scored           {len(ids)} of {comp['n']} requests")
    add("")
    add("-" * 78); add("RELIABILITY"); add("-" * 78)
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
    add("-" * 78); add("CODEBOOK COMPLIANCE"); add("-" * 78)
    add(f"  labels emitted            {comp['labels_emitted']}")
    add(f"  out-of-vocabulary codes   {comp['bad_codes']}")
    add(f"  duplicate labels (R1)     {comp['dup_codes']}")
    add(f"  labels with no span (R3)  {comp['missing_span']}")
    add(f"  span not in review        {comp['span_bad']}")
    add(f"  span matched only loosely {comp['span_loose']}")
    denom = max(comp["labels_emitted"], 1)
    add(f"  span verbatim rate        {pct(1-(comp['span_bad']+comp['missing_span'])/denom)}")
    add("")
    add("-" * 78); add("QUALITY"); add("-" * 78)
    add(f"  micro-F1            {mf:.3f}   (P {mp:.3f} / R {mr:.3f})   tp {tp} fp {fp} fn {fn}")
    add(f"  example-based F1    {ex_f1:.3f}")
    add(f"  exact set match     {exact:.3f}")
    add(f"  class macro-F1      {class_macro:.3f}   (5 classes + None)")
    add(f"  meso macro-F1       {meso_macro:.3f}   over {len(scored)} labels, support >= {MIN_SUPPORT}")
    add(f"  None P/R/F1         {np_:.3f} / {nr_:.3f} / {nf_:.3f}   (support {nt+nfn})")
    if fn:
        add(f"  missed labels named in the model's own analysis: {seen_dropped}/{fn} "
            f"({100*seen_dropped/fn:.0f}%)   rule interpretation vs attention")
    add("")
    add("  class                     P      R     F1   supp")
    for k, p, r, f, s in crows:
        add(f"    {k:<20} {p:6.3f} {r:6.3f} {f:6.3f}  {s:>4}")
    add("")
    add(f"  per-label (* = support < {MIN_SUPPORT}, excluded from meso macro)")
    add("    label                                 P      R     F1   supp")
    for c, (p, r, f, s) in sorted(per.items(), key=lambda kv: (-kv[1][3], kv[0])):
        add(f"  {' ' if s >= MIN_SUPPORT else '*'} {c:<34} {p:6.3f} {r:6.3f} {f:6.3f}  {s:>4}")
    add("")
    add("-" * 78); add("ERROR TAXONOMY"); add("-" * 78)
    add("  over-labelled  (predicted, not in gold)")
    for c, n in over.most_common(TOP_ERRORS):
        add(f"    {c:<36} {n}")
    add("  under-labelled (in gold, not predicted)")
    for c, n in under.most_common(TOP_ERRORS):
        add(f"    {c:<36} {n}")
    if confusion:
        add("  co-occurring miss/false-positive pairs")
        for (a, b), n in confusion.most_common(TOP_ERRORS):
            add(f"    {a} ~ {b}   {n}")
    add("")
    add(f"  reviews with disagreements (first {TOP_ERRORS}; full detail in the .md)")
    shown = 0
    for i in ids:
        if pred[i] == gold[i] or shown >= TOP_ERRORS:
            continue
        shown += 1
        add(f"    {i}   [{classify(gold[i], pred[i])}]")
        add(f"      gold: {sorted(gold[i]) or ['NONE']}")
        add(f"      pred: {sorted(pred[i]) or ['NONE']}")
    add("")
    add("-" * 78); add("COST"); add("-" * 78)
    pr = any_meta.get("pricing", {})
    add(f"  rates as of       {pr.get('as_of')}  in {pr.get('input')} / "
        f"cached {pr.get('cached_input')} / write {pr.get('cache_write')} / "
        f"out {pr.get('output')} per MTok")
    add(f"  input tokens      {tok['input_tokens']:,}  (cached {tok['cached_tokens']:,}, "
        f"written {tok['cache_write_tokens']:,}, plain {tok['uncached_input_tokens']:,})")
    add(f"  output tokens     {tok['output_tokens']:,}  (reasoning {tok['reasoning_tokens']:,}, "
        f"{100*tok['reasoning_tokens']/max(tok['output_tokens'],1):.0f}% of output)")
    add(f"  mean per review   in {tok['input_tokens']/n_u:,.0f}  "
        f"out {tok['output_tokens']/n_u:,.0f}  reasoning {tok['reasoning_tokens']/n_u:,.0f}")
    add(f"  cache hit rate    {hit:.3f}")
    add(f"  total spend       ${spend:.4f}")
    add(f"  per review        ${usd_per_review:.6f}")
    add("  cost split        " + "  ".join(f"{k} {pct(v)}" for k, v in cost_share.items()))
    add(f"  projected {PROJECT_TO:,}  ${usd_per_review*PROJECT_TO:,.2f}")
    if mf:
        add(f"  micro-F1 per $ at {PROJECT_TO:,}   {mf/(usd_per_review*PROJECT_TO):.5f}")
    add("")
    add("-" * 78); add("THROUGHPUT"); add("-" * 78)
    add(f"  latency p50/p95   {p50:.2f}s / {p95:.2f}s   "
        f"mean {statistics.mean(lat or [0]):.2f}s   max {max(lat or [0]):.2f}s")
    add(f"  sequential {PROJECT_TO:,}  {PROJECT_TO*p50/3600:,.0f} h at p50 "
        f"({PROJECT_TO*statistics.mean(lat or [0])/3600:,.0f} h at mean, skewed by outliers)")
    add(f"  web searches      {comp['searched']}/{comp['ok']} reviews "
        f"({pct(comp['searched']/max(comp['ok'],1))})")
    if searched_ids:
        add(f"    ids: {', '.join(searched_ids[:8])}{' ...' if len(searched_ids) > 8 else ''}")
    add("")
    add("=" * 78)

    # ---- write ---------------------------------------------------------------
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{tag}_report.txt").write_text("\n".join(L) + "\n", encoding="utf-8")

    # per-review predictions: needed for the paired bootstrap in compare_runs.py,
    # since every model sees the same 50 reviews and paired tests are far more
    # sensitive at n=50 than independent CIs.
    with open(out_dir / f"{tag}_perreview.jsonl", "w", encoding="utf-8") as f:
        for i in ids:
            f.write(json.dumps({
                "review_id": i,
                "gold": sorted(gold[i]),
                "pred": sorted(pred[i]),
                "correct": sorted(pred[i] & gold[i]),
                "missed": sorted(gold[i] - pred[i]),
                "spurious": sorted(pred[i] - gold[i]),
                "analysis_named_missed": {
                    c: mentioned(c, (parsed_by_review.get(i) or {}).get("analysis", "") or "")
                    for c in sorted(gold[i] - pred[i])},
            }, ensure_ascii=False) + "\n")

    md_path = out_dir / f"{tag}_errors.md"
    if WRITE_MD:
        write_error_review(md_path, tag, any_meta, ids, gold, pred, gold_text,
                           gold_game, parsed_by_review, val, mf, mp, mr)

    row = {
        "tag": tag, "generated": datetime.now().isoformat(timespec="seconds"),
        "provider": provider, "model": model,
        "model_version": any_meta.get("model_version"),
        "reasoning_effort": any_meta.get("reasoning_effort"),
        "web_search": any_meta.get("web_search"),
        "prompt_file": any_meta.get("prompt_file"),
        # the prompt is an ablation axis now, so the comparison needs to be able to
        # name it without hashing: teacher_v2_bare vs teacher_v2_full
        "prompt_stem": Path(any_meta.get("prompt_file") or "").name.rsplit(".txt", 1)[0],
        "prompt_sha256": any_meta.get("prompt_sha256"),
        "gold_file": str(gold_file), "n_requests": comp["n"], "n_scored": len(ids),
        "micro_f1": round(mf, 4), "micro_p": round(mp, 4), "micro_r": round(mr, 4),
        "example_f1": round(ex_f1, 4), "exact_match": round(exact, 4),
        "class_macro_f1": round(class_macro, 4),
        "meso_macro_f1": round(meso_macro, 4), "meso_macro_n_labels": len(scored),
        "none_p": round(np_, 4), "none_r": round(nr_, 4), "none_f1": round(nf_, 4),
        "tp": tp, "fp": fp, "fn": fn,
        "missed_but_named_in_analysis": seen_dropped,
        "per_label_f1": {c: round(v[2], 4) for c, v in per.items()},
        "per_label_support": {c: v[3] for c, v in per.items()},
        "class_f1": {k: round(f, 4) for k, _, _, f, _ in crows},
        "top_over_labelled": over.most_common(5),
        "top_under_labelled": under.most_common(5),
        "api_errors": comp["api_error"], "parsed": comp["parsed"],
        "truncated": comp["truncated"], "labels_emitted": comp["labels_emitted"],
        "bad_codes": comp["bad_codes"], "dup_labels_r1": comp["dup_codes"],
        "missing_span_r3": comp["missing_span"], "span_not_verbatim": comp["span_bad"],
        "span_loose": comp["span_loose"],
        "span_verbatim_rate": round(1-(comp["span_bad"]+comp["missing_span"])/denom, 4),
        "pricing": pr, "tokens": tok, "cache_hit_rate": round(hit, 4),
        "mean_output_tokens": round(tok["output_tokens"]/n_u, 1),
        "mean_reasoning_tokens": round(tok["reasoning_tokens"]/n_u, 1),
        "spend_usd": round(spend, 6), "usd_per_review": round(usd_per_review, 8),
        f"projected_usd_at_{PROJECT_TO}": round(usd_per_review*PROJECT_TO, 2),
        "cost_share": {k: round(v, 4) for k, v in cost_share.items()},
        "latency_p50": round(p50, 2), "latency_p95": round(p95, 2),
        "latency_mean": round(statistics.mean(lat or [0]), 2),
        "search_rate": round(comp["searched"]/max(comp["ok"], 1), 4),
        "perreview_file": str(out_dir / f"{tag}_perreview.jsonl"),
    }
    (out_dir / f"{tag}_metrics.json").write_text(
        json.dumps(row, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if print_report:
        print("\n".join(L))
        print(f"wrote {show(out_dir / (tag + '_report.txt'))}")
        print(f"wrote {show(out_dir / (tag + '_perreview.jsonl'))}")
        if WRITE_MD:
            print(f"wrote {show(md_path)}")
        print(f"wrote {show(out_dir / (tag + '_metrics.json'))}")
    return row


def run_is_complete(run_dir: Path) -> bool | None:
    """What the runner's checkpoint says. None when there is no checkpoint (an older
    run, or one written by hand)."""
    cp = run_dir / "checkpoint.json"
    if not cp.exists():
        return None
    try:
        return bool(json.loads(cp.read_text(encoding="utf-8")).get("complete"))
    except json.JSONDecodeError:
        return None


def main() -> None:
    a = parse_args()
    runs_root, gold_file, out_root = resolve(a.runs_root), resolve(a.gold), resolve(a.out_root)
    codebook_file = resolve(a.codebook)

    if a.list:
        for d in discover_runs(runs_root):
            print(show(d))
        return

    if a.run_dir:
        run_dirs = [resolve(a.run_dir)]
        single = True
    else:
        run_dirs = discover_runs(runs_root)
        single = False
        if not run_dirs:
            sys.exit(f"no runs under {show(runs_root)}; nothing to score")

    if not gold_file.exists():
        sys.exit(f"gold file not found: {show(gold_file)}")
    if not codebook_file.exists():
        sys.exit(f"codebook file not found: {show(codebook_file)}")
    gold_bundle = load_gold(gold_file)
    legal = load_legal_codes(codebook_file)

    # Every (run_dir, tag) pair to score. A directory normally holds one run, but a
    # config re-run under a different tag would leave two, and both deserve scoring.
    jobs = []
    for d in run_dirs:
        for tag in ([a.tag] if a.tag else run_tags(d)):
            jobs.append((d, tag))
    if not jobs:
        sys.exit("no *_responses.jsonl found in the selected run director(y|ies)")

    if not single:
        print(f"scoring {len(jobs)} run(s) under {show(runs_root)} -> {show(out_root)}\n")

    rows, skipped = [], []
    for run_dir, tag in jobs:
        # Mirror the runs tree by RELATIVE PATH rather than by re-deriving
        # model/effort/prompt from the metadata: the mirror then cannot drift from
        # whatever the runner actually wrote.
        try:
            rel = run_dir.relative_to(runs_root)
        except ValueError:
            rel = Path(run_dir.name)
        out_dir = out_root / rel

        complete = run_is_complete(run_dir)
        if complete is False:
            print(f"  NOTE {tag}: checkpoint says this run never finished")
        try:
            row = score_run(run_dir, tag, gold_file, gold_bundle, legal, out_dir,
                            print_report=single)
        except Exception as e:                 # one bad run must not end the batch
            print(f"  SKIP {tag}: {type(e).__name__}: {e}")
            row = None
        if row is None:
            skipped.append(tag)
            continue
        row["run_dir"] = str(run_dir)
        row["run_complete"] = complete
        rows.append(row)
        if not single:
            n = max(row["n_requests"], 1)
            print(f"  {row['micro_f1']:.3f} micro-F1   parsed {row['parsed']}/{n}   "
                  f"${row['spend_usd']:.4f}   {tag}")

    # index.jsonl is rebuilt, never appended -- see the module docstring.
    out_root.mkdir(parents=True, exist_ok=True)
    if single:
        # A single-run rescore must not blow away the rows for every other run, so merge
        # this row into whatever the index already holds, keyed on the run directory.
        # The exists() guard has to happen BEFORE jsonl() opens the file: as a
        # comprehension filter it runs per row, which is too late on the first
        # --run-dir score of a fresh checkout, where no index exists yet.
        index_path = out_root / "index.jsonl"
        existing = ({r.get("run_dir"): r for r in jsonl(index_path)}
                    if index_path.exists() else {})
        for r in rows:
            existing[r["run_dir"]] = r
        rows = sorted(existing.values(), key=lambda r: -r.get("micro_f1", 0))
    else:
        rows.sort(key=lambda r: -r.get("micro_f1", 0))
    with open(out_root / "index.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"\nindex   {len(rows)} run(s) -> {show(out_root / 'index.jsonl')}")
    if skipped:
        print(f"skipped {len(skipped)}: {', '.join(skipped)}")
    if not single:
        print(f"next: python compare_runs.py")


if __name__ == "__main__":
    main()
