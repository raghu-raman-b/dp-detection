#!/usr/bin/env python3
"""
pilot_stats.py — pilot annotation diagnostics + targeted-stratum planner.

Reads the labelled JSONL and (optionally) the codebook JSON, then reports:

  1. Integrity      — dupes, label/binary/none/labels_str disagreement, pass & version drift
  2. Base rates     — per-label positives by stratum; random-stratum rate + Wilson 95% CI
  3. Projection     — expected positives in the frozen test split; which labels can carry
                      per-class metrics and which cannot
  4. Deficits       — positives still needed per meso label and per high-level class
  5. Seed yield     — what each seed_keyword actually surfaced (hit rate, labels hit,
                      collateral labels picked up for free)
  6. Co-occurrence  — P(B | A), so seeds that double-dip are visible
  7. Allocation     — suggested split of the targeted budget across labels, yield-adjusted
  8. Seed material  — codebook indicator text for deficit labels, to draft keywords from

Usage:
  python pilot_stats.py --data random.jsonl targeted.jsonl extra.jsonl
  python pilot_stats.py --data *.jsonl --codebook codebook_v0_16.json --outdir stats/
  python pilot_stats.py --data *.jsonl --targeted-budget 200 --assumed-yield 0.3

--data takes any number of JSONL files; they are concatenated, tagged by source, and
checked for cross-file duplicate review_ids and label-schema drift.
--codebook is OPTIONAL: it supplies readable label names, the §8 seed material, and a
column-vs-codebook cross-check. Every statistic works without it.

No third-party dependencies. CSV export is optional (--outdir).
"""

import argparse
import csv
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

HL_PREFIX = {"T": "Temporal", "M": "Monetary", "S": "Social",
             "P": "Psychological", "Tech": "Technical"}
LABEL_RE = re.compile(r"^(Tech|T|M|S|P)_[A-Za-z0-9]+$")


# ----------------------------------------------------------------------------
# loading
# ----------------------------------------------------------------------------

def load_jsonl(paths):
    """Load one or more JSONL files, tagging each row with its source file."""
    if isinstance(paths, str):
        paths = [paths]
    rows = []
    per_file = {}
    for path in paths:
        n0 = len(rows)
        with open(path, encoding="utf-8") as fh:
            for i, line in enumerate(fh, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError as e:
                    sys.exit(f"[fatal] {path}:{i} is not valid JSON — {e}")
                obj["_source_file"] = os.path.basename(path)
                rows.append(obj)
        per_file[os.path.basename(path)] = len(rows) - n0
    if not rows:
        sys.exit(f"[fatal] no rows in {', '.join(paths)}")
    return rows, per_file


def check_schema_consistency(rows, label_cols):
    """Different files must carry the same label columns, or counts silently undercount."""
    by_file = defaultdict(set)
    for r in rows:
        by_file[r["_source_file"]].update(k for k in r if LABEL_RE.match(k))
    if len(by_file) < 2:
        return
    union = set(label_cols)
    bad = False
    for f, cols in by_file.items():
        missing = union - cols
        if missing:
            bad = True
            print(f"[warn] {f} is missing label columns: {', '.join(sorted(missing))} "
                  f"(treated as 0 — verify this is intended)", file=sys.stderr)
    if not bad:
        print(f"[ok] label schema identical across {len(by_file)} files", file=sys.stderr)


def norm(s):
    """'Fear of Missing Out (FOMO)' -> 'fearofmissingoutfomo'"""
    return re.sub(r"[^a-z0-9]", "", s.lower())


def discover_label_cols(rows):
    """Label columns = keys matching the prefix scheme, present across rows."""
    keys = set()
    for r in rows:
        keys.update(r.keys())
    cols = sorted(k for k in keys if LABEL_RE.match(k))
    if not cols:
        sys.exit("[fatal] no label columns found (expected keys like 'M_PayToProgress')")
    # keep declaration order: T, M, S, P, Tech
    order = {"T": 0, "M": 1, "S": 2, "P": 3, "Tech": 4}
    first_row_order = [k for k in rows[0] if LABEL_RE.match(k)]
    if len(first_row_order) == len(cols):
        return first_row_order
    return sorted(cols, key=lambda c: (order[c.split("_", 1)[0]], c))


def hl_of(col):
    return HL_PREFIX[col.split("_", 1)[0]]


def load_codebook(path, label_cols):
    """Map column -> pretty meso label, and column -> indicator strings."""
    pretty, indicators = {}, {}
    if not path:
        return pretty, indicators
    with open(path, encoding="utf-8") as fh:
        cb = json.load(fh)
    by_norm = {}
    for entry in cb.get("labels", []):
        meso = entry.get("meso_label", "")
        if meso:
            by_norm[norm(meso)] = entry
    for col in label_cols:
        suffix = col.split("_", 1)[1]
        entry = by_norm.get(norm(suffix))
        if entry:
            pretty[col] = entry["meso_label"]
            indicators[col] = entry.get("indicators", []) or []
    missing = [c for c in label_cols if c not in pretty]
    if missing:
        print(f"[warn] no codebook entry matched: {', '.join(missing)}", file=sys.stderr)
    extra = [e["meso_label"] for n, e in by_norm.items()
             if n not in {norm(c.split('_', 1)[1]) for c in label_cols}]
    if extra:
        print(f"[warn] codebook labels with no data column: {', '.join(extra)}", file=sys.stderr)
    return pretty, indicators


# ----------------------------------------------------------------------------
# stats helpers
# ----------------------------------------------------------------------------

def wilson(k, n, z=1.96):
    """Wilson score interval — correct at the small counts we actually have."""
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / d
    return (p, max(0.0, centre - half), min(1.0, centre + half))


def bar(x, width=18, cap=None):
    cap = cap or 1.0
    n = int(round(width * min(x / cap, 1.0))) if cap else 0
    return "#" * n + "." * (width - n)


def rule(title, ch="="):
    print(f"\n{ch * 78}\n{title}\n{ch * 78}")


# ----------------------------------------------------------------------------
# 1. integrity
# ----------------------------------------------------------------------------

def check_integrity(rows, label_cols):
    rule("1. INTEGRITY")
    problems = defaultdict(list)

    ids = defaultdict(list)
    for r in rows:
        ids[r.get("review_id", "<missing>")].append(r["_source_file"])
    dupes = {k: v for k, v in ids.items() if len(v) > 1}

    for r in rows:
        rid = r.get("review_id", "<missing>")
        binaries = {c for c in label_cols if int(r.get(c, 0) or 0) == 1}

        arr = set(r.get("labels") or [])
        if arr != binaries:
            problems["labels[] != binary columns"].append(
                f"{rid[:8]}  arr-only={sorted(arr - binaries)} col-only={sorted(binaries - arr)}")

        none_flag = int(r.get("none", 0) or 0)
        if none_flag == 1 and binaries:
            problems["none=1 but labels present"].append(f"{rid[:8]}  {sorted(binaries)}")
        if none_flag == 0 and not binaries:
            problems["no labels but none=0"].append(rid[:8])

        ls = (r.get("labels_str") or "").strip()
        n_ls = len([p for p in ls.split(";") if p.strip()]) if ls else 0
        if n_ls != len(binaries):
            problems["labels_str count != binary count"].append(
                f"{rid[:8]}  labels_str={n_ls} binaries={len(binaries)}")

        if not (r.get("review_text") or "").strip():
            problems["empty review_text"].append(rid[:8])
        if r.get("stratum") not in ("random", "targeted"):
            problems["bad stratum value"].append(f"{rid[:8]}  {r.get('stratum')!r}")
        if r.get("stratum") == "targeted" and not (r.get("seed_keyword") or "").strip():
            problems["targeted row with no seed_keyword"].append(rid[:8])

    if dupes:
        cross = {k: v for k, v in dupes.items() if len(set(v)) > 1}
        problems["duplicate review_id"] = [
            f"{k[:8]} x{len(v)} in {', '.join(sorted(set(v)))}" for k, v in dupes.items()]
        if cross:
            problems["duplicate ACROSS files (same review coded twice?)"] = [
                f"{k[:8]}: {', '.join(sorted(set(v)))}" for k, v in cross.items()]

    if not problems:
        print("  clean — no issues found.")
    for kind, items in problems.items():
        print(f"\n  [{len(items):>4}] {kind}")
        for it in items[:8]:
            print(f"         {it}")
        if len(items) > 8:
            print(f"         ... and {len(items) - 8} more")

    print("\n  distributions")
    for field in ("_source_file", "stratum", "pass", "codebook_version", "market", "confidence"):
        c = Counter(str(r.get(field, "")) for r in rows)
        if len(c) > 1 or field in ("_source_file", "stratum", "pass", "codebook_version"):
            shown = ", ".join(f"{k or '<blank>'}={v}" for k, v in c.most_common(8))
            print(f"    {field:<18} {shown}")

    versions = Counter(str(r.get("codebook_version", "")) for r in rows)
    if len(versions) > 1:
        latest = max(versions, key=lambda v: [int(x) for x in re.findall(r"\d+", v)] or [0])
        stale = sum(v for k, v in versions.items() if k != latest)
        print(f"\n  [drift] {stale} rows coded under a version older than {latest} — "
              f"these are the pass-2 re-code candidates.")
    return problems


# ----------------------------------------------------------------------------
# 2-3. base rates, projection
# ----------------------------------------------------------------------------

def label_counts(rows, label_cols):
    counts = {c: Counter() for c in label_cols}
    n_by_stratum = Counter()
    for r in rows:
        st = r.get("stratum", "?")
        n_by_stratum[st] += 1
        for c in label_cols:
            if int(r.get(c, 0) or 0) == 1:
                counts[c][st] += 1
    return counts, n_by_stratum


def report_base_rates(rows, label_cols, pretty, counts, n_by_stratum):
    rule("2. PER-LABEL COUNTS  (base rate = random stratum only)")
    n_rand = n_by_stratum.get("random", 0)
    print(f"  random n={n_rand}   targeted n={n_by_stratum.get('targeted', 0)}   total n={sum(n_by_stratum.values())}\n")
    hdr = f"  {'meso label':<34}{'rand':>6}{'targ':>6}{'tot':>6}   {'rate (random, 95% CI)':<26}"
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    maxrate = max((counts[c]["random"] / n_rand if n_rand else 0) for c in label_cols) or 1.0
    rows_out = []
    for c in label_cols:
        cr, ct = counts[c]["random"], counts[c]["targeted"]
        p, lo, hi = wilson(cr, n_rand)
        name = pretty.get(c, c.split("_", 1)[1])
        flag = "  <-- ZERO" if (cr + ct) == 0 else ""
        print(f"  {name:<34}{cr:>6}{ct:>6}{cr + ct:>6}   "
              f"{p * 100:>5.1f}% [{lo * 100:>4.1f},{hi * 100:>5.1f}]  {bar(p, 12, maxrate)}{flag}")
        rows_out.append(dict(column=c, meso_label=name, high_level=hl_of(c),
                             random_pos=cr, targeted_pos=ct, total_pos=cr + ct,
                             random_n=n_rand, rate=round(p, 4),
                             ci_lo=round(lo, 4), ci_hi=round(hi, 4)))

    rule("2b. HIGH-LEVEL ROLLUP", "-")
    for hl in ["Temporal", "Monetary", "Social", "Psychological", "Technical"]:
        cols = [c for c in label_cols if hl_of(c) == hl]
        # a review counts once for the class even with several meso labels
        cr = sum(1 for r in rows if r.get("stratum") == "random"
                 and any(int(r.get(c, 0) or 0) for c in cols))
        ct = sum(1 for r in rows if r.get("stratum") == "targeted"
                 and any(int(r.get(c, 0) or 0) for c in cols))
        p, lo, hi = wilson(cr, n_rand)
        print(f"  {hl:<16} rand={cr:>4}  targ={ct:>4}  total={cr + ct:>4}   "
              f"random rate {p * 100:>5.1f}% [{lo * 100:.1f},{hi * 100:.1f}]")

    none_r = sum(1 for r in rows if r.get("stratum") == "random"
                 and not any(int(r.get(c, 0) or 0) for c in label_cols))
    none_t = sum(1 for r in rows if r.get("stratum") == "targeted"
                 and not any(int(r.get(c, 0) or 0) for c in label_cols))
    card = [sum(int(r.get(c, 0) or 0) for c in label_cols) for r in rows]
    pos_card = [x for x in card if x > 0]
    print(f"\n  NONE            rand={none_r:>4}  targ={none_t:>4}   "
          f"({none_r / n_rand * 100:.1f}% of random stratum)")
    print(f"  labels/review   mean={sum(card) / len(card):.2f}  "
          f"mean|positive={sum(pos_card) / max(len(pos_card), 1):.2f}  max={max(card)}")
    print(f"  cardinality     " + "  ".join(f"{k}:{v}" for k, v in sorted(Counter(card).items())))
    return rows_out


def report_projection(label_cols, pretty, counts, n_total_planned, test_frac, metric_floor):
    rule(f"3. TEST-SPLIT PROJECTION  (pilot -> {n_total_planned}, test = {test_frac:.0%})")
    print(f"  Assumes the split is stratified on labels, so each label's positives divide")
    print(f"  proportionally. A label needs >= {metric_floor} test positives to support a")
    print(f"  per-class F1 / kappa worth reporting.\n")
    print(f"  {'meso label':<34}{'now':>5}{'->test':>8}   verdict")
    print("  " + "-" * 66)
    verdicts = Counter()
    for c in label_cols:
        tot = counts[c]["random"] + counts[c]["targeted"]
        proj = tot * test_frac
        if proj >= metric_floor:
            v, verdicts["ok"] = "per-class metrics OK", verdicts["ok"] + 1
        elif proj >= metric_floor / 2:
            v, verdicts["thin"] = "thin — report with CI, flag as low-support", verdicts["thin"] + 1
        elif tot > 0:
            v, verdicts["pooled"] = "POOLED ONLY — cannot report per-class", verdicts["pooled"] + 1
        else:
            v, verdicts["zero"] = "ZERO — unmeasurable, cannot even scope", verdicts["zero"] + 1
        print(f"  {pretty.get(c, c):<34}{tot:>5}{proj:>8.1f}   {v}")
    print(f"\n  summary: {verdicts['ok']} reportable | {verdicts['thin']} thin | "
          f"{verdicts['pooled']} pooled-only | {verdicts['zero']} zero")
    if verdicts["zero"]:
        print("  A zero label cannot be declared 'not review-observable' — you never sampled for it.")


# ----------------------------------------------------------------------------
# 4-5. deficits and seed yield
# ----------------------------------------------------------------------------

def compute_deficits(label_cols, pretty, counts, meso_floor, test_frac, metric_floor):
    """Target = whichever is larger: the flat floor, or what the test split needs."""
    need_for_test = math.ceil(metric_floor / test_frac) if test_frac else meso_floor
    target = max(meso_floor, need_for_test)
    deficits = {}
    for c in label_cols:
        tot = counts[c]["random"] + counts[c]["targeted"]
        deficits[c] = max(0, target - tot)
    return deficits, target


def report_seed_yield(rows, label_cols, pretty, deficits):
    rule("5. SEED KEYWORD YIELD  (from existing targeted rows)")
    targeted = [r for r in rows if r.get("stratum") == "targeted"]
    if not targeted:
        print("  no targeted rows yet — no yield evidence. Use --assumed-yield for planning.")
        return {}, None
    by_seed = defaultdict(list)
    for r in targeted:
        by_seed[(r.get("seed_keyword") or "<blank>").strip().lower()].append(r)

    print(f"  {'seed keyword':<24}{'n':>4}{'any%':>6}{'best%':>7}  labels surfaced (count)")
    print("  " + "-" * 76)
    overall_hits, modal_num, modal_den = 0, 0, 0
    for seed, rs in sorted(by_seed.items(), key=lambda kv: -len(kv[1])):
        hits = sum(1 for r in rs if any(int(r.get(c, 0) or 0) for c in label_cols))
        overall_hits += hits
        lab = Counter()
        for r in rs:
            for c in label_cols:
                if int(r.get(c, 0) or 0):
                    lab[pretty.get(c, c)] += 1
        best = max(lab.values()) if lab else 0
        modal_num += best
        modal_den += len(rs)
        top = ", ".join(f"{k}({v})" for k, v in lab.most_common(4)) or "—"
        print(f"  {seed[:23]:<24}{len(rs):>4}{hits / len(rs) * 100:>5.0f}%"
              f"{best / len(rs) * 100:>6.0f}%  {top}")

    any_rate = overall_hits / len(targeted)
    modal_rate = modal_num / modal_den if modal_den else 0.0
    print(f"\n  any-label yield  : {overall_hits}/{len(targeted)} = {any_rate:.0%}  "
          f"(inflated — counts collateral labels you weren't seeding for)")
    print(f"  per-label yield  : {modal_rate:.0%}  (each seed's single most-hit label — "
          f"the honest planning number)")
    print(f"  Sizing rule: reviews_to_screen ~= positives_needed / per-label yield.")
    print(f"  NOTE: 'best%' is the modal label, not the label you intended. If a seed's top")
    print(f"  label is not its target, the seed is mis-specified — rewrite it before pulling.")
    return by_seed, modal_rate


def report_cooccurrence(rows, label_cols, pretty, min_support=3):
    rule("6. CO-OCCURRENCE  P(B | A)  — which labels ride along for free")
    joint = defaultdict(Counter)
    marg = Counter()
    for r in rows:
        present = [c for c in label_cols if int(r.get(c, 0) or 0)]
        for a in present:
            marg[a] += 1
            for b in present:
                if a != b:
                    joint[a][b] += 1
    any_shown = False
    for a in label_cols:
        if marg[a] < min_support:
            continue
        pairs = [(b, n / marg[a]) for b, n in joint[a].most_common(3) if n >= 2]
        if not pairs:
            continue
        any_shown = True
        s = ", ".join(f"{pretty.get(b, b)} {p:.0%}" for b, p in pairs)
        print(f"  {pretty.get(a, a):<32} (n={marg[a]:>3}) -> {s}")
    if not any_shown:
        print(f"  nothing above support threshold (n>={min_support}).")
    print("\n  Seeding for a label with strong co-occurrence also fills its partners;")
    print("  labels absent from this list must be seeded on their own terms.")


# ----------------------------------------------------------------------------
# 7-8. allocation and seed material
# ----------------------------------------------------------------------------

def report_allocation(label_cols, pretty, counts, deficits, target, budget,
                      assumed_yield, min_slots):
    rule(f"7. SUGGESTED TARGETED ALLOCATION  (budget = {budget} reviews)")
    print(f"  Target per meso label: {target} pilot positives.")
    print(f"  Assumed per-seed yield: {assumed_yield:.0%} (reviews screened -> positives).")
    print(f"  Minimum slots for any zero-positive label: {min_slots}.\n")

    need = {c: d for c, d in deficits.items() if d > 0}
    if not need:
        print("  every label already meets target — spend the budget on the rarest classes anyway.")
        return []

    raw = {}
    for c, d in need.items():
        est = d / max(assumed_yield, 0.05)
        tot = counts[c]["random"] + counts[c]["targeted"]
        if tot == 0:
            est = max(est, min_slots)
        raw[c] = est
    scale = budget / sum(raw.values())
    alloc = {c: max(min_slots if (counts[c]["random"] + counts[c]["targeted"]) == 0 else 1,
                    int(round(v * scale))) for c, v in raw.items()}

    # trim/pad to budget
    while sum(alloc.values()) > budget:
        c = max(alloc, key=lambda k: alloc[k])
        alloc[c] -= 1
    while sum(alloc.values()) < budget:
        c = max(need, key=lambda k: deficits[k] / max(alloc[k], 1))
        alloc[c] += 1

    print(f"  {'meso label':<34}{'have':>6}{'need':>6}{'pull':>7}  priority")
    print("  " + "-" * 68)
    out = []
    for c in sorted(need, key=lambda k: (-deficits[k], k)):
        have = counts[c]["random"] + counts[c]["targeted"]
        prio = "CRITICAL (zero)" if have == 0 else ("high" if have < 8 else "medium")
        print(f"  {pretty.get(c, c):<34}{have:>6}{deficits[c]:>6}{alloc[c]:>7}  {prio}")
        out.append(dict(column=c, meso_label=pretty.get(c, c), high_level=hl_of(c),
                        have=have, deficit=deficits[c], pull=alloc[c], priority=prio))
    print("  " + "-" * 68)
    print(f"  {'TOTAL':<34}{'':>6}{'':>6}{sum(alloc.values()):>7}")
    print("\n  These are screening quotas, not label quotas: pull this many candidate")
    print("  reviews per seed, code them all, and let co-occurrence fill neighbours.")
    return out


def report_seed_material(label_cols, pretty, indicators, deficits, max_labels=12):
    rule("8. SEED MATERIAL FROM CODEBOOK  (deficit labels only)")
    if not indicators:
        print("  no codebook supplied (--codebook) — skipping.")
        return
    ranked = sorted([c for c in label_cols if deficits.get(c, 0) > 0],
                    key=lambda c: -deficits[c])[:max_labels]
    for c in ranked:
        print(f"\n  {pretty.get(c, c)}  (deficit {deficits[c]})")
        for ind in indicators.get(c, [])[:4]:
            flat = re.sub(r"\s+", " ", ind).strip()
            print(f"    - {flat[:150]}{'...' if len(flat) > 150 else ''}")
        if not indicators.get(c):
            print("    (no indicators recorded — write player-vocabulary seeds by hand)")
    print("\n  Draft seeds from player vocabulary in these, not from the academic definition.")


# ----------------------------------------------------------------------------

def write_csv(path, rows):
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"[csv] {path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", required=True, nargs="+",
                    help="labelled reviews — one or more .jsonl files (concatenated)")
    ap.add_argument("--codebook", default=None, help="codebook JSON (for pretty names + seeds)")
    ap.add_argument("--outdir", default=None, help="write CSVs here")
    ap.add_argument("--targeted-budget", type=int, default=200,
                    help="targeted reviews you intend to code (default 200)")
    ap.add_argument("--planned-total", type=int, default=None,
                    help="final pilot size; default = random n + targeted budget")
    ap.add_argument("--test-frac", type=float, default=0.4,
                    help="fraction of pilot held out as test (default 0.4 = 200/500)")
    ap.add_argument("--metric-floor", type=int, default=10,
                    help="test positives needed for a reportable per-class metric")
    ap.add_argument("--meso-floor", type=int, default=12,
                    help="minimum pilot positives per meso label")
    ap.add_argument("--assumed-yield", type=float, default=None,
                    help="positives per screened review; default = measured from existing seeds")
    ap.add_argument("--min-slots", type=int, default=8,
                    help="minimum screening slots for a zero-positive label")
    args = ap.parse_args()

    rows, per_file = load_jsonl(args.data)
    label_cols = discover_label_cols(rows)
    check_schema_consistency(rows, label_cols)
    pretty, indicators = load_codebook(args.codebook, label_cols)
    for c in label_cols:
        pretty.setdefault(c, c.split("_", 1)[1])

    src = "  ".join(f"{f}={n}" for f, n in per_file.items())
    print(f"loaded {len(rows)} rows, {len(label_cols)} label columns")
    print(f"  from: {src}")

    check_integrity(rows, label_cols)
    counts, n_by_stratum = label_counts(rows, label_cols)
    base = report_base_rates(rows, label_cols, pretty, counts, n_by_stratum)

    planned = args.planned_total or (n_by_stratum.get("random", 0) + args.targeted_budget)
    report_projection(label_cols, pretty, counts, planned, args.test_frac, args.metric_floor)

    deficits, target = compute_deficits(label_cols, pretty, counts, args.meso_floor,
                                        args.test_frac, args.metric_floor)
    rule("4. DEFICITS")
    print(f"  target per meso label = {target} pilot positives "
          f"(max of --meso-floor={args.meso_floor} and {args.metric_floor}/{args.test_frac:.2f} "
          f"needed to land {args.metric_floor} in test)")
    short = [(c, deficits[c]) for c in label_cols if deficits[c] > 0]
    print(f"  {len(short)}/{len(label_cols)} labels below target; "
          f"total positives still needed = {sum(d for _, d in short)}")

    _, measured = report_seed_yield(rows, label_cols, pretty, deficits)
    yield_rate = args.assumed_yield if args.assumed_yield is not None else (measured or 0.35)

    report_cooccurrence(rows, label_cols, pretty)
    alloc = report_allocation(label_cols, pretty, counts, deficits, target,
                              args.targeted_budget, yield_rate, args.min_slots)
    report_seed_material(label_cols, pretty, indicators, deficits)

    if args.outdir:
        os.makedirs(args.outdir, exist_ok=True)
        write_csv(os.path.join(args.outdir, "label_base_rates.csv"), base)
        write_csv(os.path.join(args.outdir, "targeted_allocation.csv"), alloc)

    print("\ndone.\n")


if __name__ == "__main__":
    main()