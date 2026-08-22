#!/usr/bin/env python3
"""
build_tuning_set.py — sample the 50-review tuning / provider-bake-off set.

This set is BURNED: it is where prompt refinement and provider selection
happen, so nothing scored on it may appear in any reported evaluation.
Every record carries set_role = "tuning_selection" as a reminder.

Edit the CONFIG block, then:  python3 build_tuning_set.py

Order of operations
-------------------
  1. index every review_id used as an example in the codebook
  2. index every review_id already in the validation set(s)
  3. load every *.jsonl in INPUT_DIR, collapse repeated review_ids to their
     first occurrence, skip anything indexed in steps 1 and 2
  4. sample: true-Nones, then greedy label coverage, then a random
     (corpus-proportional) fill
  5. write the gold jsonl, the blind jsonl, and a markdown report

Sampling differs from build_validation_set.py on purpose: the floor is one
row per label rather than two, there is no per-game cap, and the coverage
phase PREFERS multi-label rows because 29 labels have to fit inside a
40-row budget.
"""

from __future__ import annotations

import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

# ═══════════════════════════════ CONFIG ═══════════════════════════════

INPUT_DIR = "../../labeled_data"

CODEBOOK = "../../../codebook_versions/codebook_v0.20.json"

# Everything already spent on the human-validation set. Both files hold the
# same reviews; ids are unioned and deduped, so listing both is harmless.
EXCLUDE_FILES = [
    "../../validation/validation_set.jsonl",
    "../../validation/validation_set_blind.jsonl",
]

OUT = "../../tuning/tuning_set_50.jsonl"
BLIND_OUT = "../../tuning/tuning_set_50_blind.jsonl"   # None to skip
REPORT = "../../tuning/tuning_report.md"               # None to skip

SEED = 20260820              # different from the validation seed on purpose

TOTAL = 50                   # target size
NONE_TARGET = 10             # true-None reviews
PER_LABEL_MIN = 1            # floor per meso label, where support allows
SET_ROLE = "tuning_selection"

INCLUDE_UNCODED = False      # keep rows with no labels, no none=1, saved != 1

# ══════════════════════════════════════════════════════════════════════

CLASS_PREFIX = {
    "Temporal": "T",
    "Monetary": "M",
    "Social": "S",
    "Psychological": "P",
    "Technical": "Tech",
}

META_FIELDS = [
    "review_id", "app_id", "game_name", "market", "review_date",
    "star_rating", "review_text", "stratum", "seed_keyword",
]

TRUE = ("1", "1.0", "True", "true")


# ──────────────────────────────── codebook ────────────────────────────────

def label_key(high_level: str, meso_label: str) -> str:
    """'Social' + 'Fear of Missing Out (FOMO)' -> 'S_FearOfMissingOutFOMO'."""
    words = re.split(r"[^0-9A-Za-z]+", meso_label)
    camel = "".join(w[:1].upper() + w[1:] for w in words if w)
    return f"{CLASS_PREFIX[high_level]}_{camel}"


def collect_review_ids(node, out: set):
    """Every value under any key containing 'review_id', anywhere in the tree."""
    if isinstance(node, dict):
        for k, v in node.items():
            if "review_id" in k.lower():
                if isinstance(v, str) and v.strip():
                    out.add(v.strip().lower())
                elif isinstance(v, list):
                    out.update(x.strip().lower() for x in v
                               if isinstance(x, str) and x.strip())
            else:
                collect_review_ids(v, out)
    elif isinstance(node, list):
        for v in node:
            collect_review_ids(v, out)


def load_codebook(path: Path):
    cb = json.loads(path.read_text(encoding="utf-8"))
    keys, pretty = [], {}
    for lab in cb["labels"]:
        k = label_key(lab["high_level"], lab["meso_label"])
        keys.append(k)
        pretty[k] = f"{lab['high_level']}: {lab['meso_label']}"
    example_ids: set = set()
    collect_review_ids(cb, example_ids)
    return keys, pretty, str(cb.get("version", "")), example_ids


def load_excluded_ids(paths, log):
    """Union of review_ids across the already-spent sets."""
    ids: set = set()
    for spec in paths:
        p = Path(spec)
        if not p.exists():
            log.append(f"- exclusion file `{spec}` not found; nothing excluded from it")
            continue
        n_before, n_lines = len(ids), 0
        with open(p, encoding="utf-8") as fh:
            for lineno, raw in enumerate(fh, 1):
                line = raw.strip()
                if not line:
                    continue
                n_lines += 1
                try:
                    rid = str(json.loads(line).get("review_id", "")).strip()
                except json.JSONDecodeError as exc:
                    log.append(f"- bad JSON at {p.name}:{lineno} ({exc}); skipped")
                    continue
                if rid:
                    ids.add(rid.lower())
        log.append(f"- `{p.name}`: {n_lines} lines, {len(ids) - n_before} new ids "
                   f"(running union {len(ids)})")
    return ids


# ───────────────────────────────── loading ─────────────────────────────────

def labels_of(rec: dict, keys: list[str]):
    """Returns (labels from the array, labels from the binary columns)."""
    from_cols = sorted({k for k in keys if str(rec.get(k, 0)) in TRUE},
                       key=keys.index)
    arr = rec.get("labels")
    if isinstance(arr, list):
        return sorted({a for a in arr if a in keys}, key=keys.index), from_cols
    return from_cols, from_cols


def load_pool(input_dir, keys, example_ids, spent_ids, log):
    d = Path(input_dir)
    if not d.is_dir():
        raise SystemExit(f"input folder not found: {input_dir}/")

    skip_names = {Path(x).name for x in (OUT, BLIND_OUT) if x}
    skip_names |= {Path(x).name for x in EXCLUDE_FILES}
    paths = [p for p in sorted(d.glob("*.jsonl")) if p.name not in skip_names]
    if not paths:
        raise SystemExit(f"no .jsonl files found in {input_dir}/")
    log.append(f"- read {len(paths)} file(s): "
               + ", ".join(f"`{p.name}`" for p in paths))

    stats = Counter()
    pool: dict[str, dict] = {}

    for p in paths:
        with open(p, encoding="utf-8") as fh:
            for lineno, raw in enumerate(fh, 1):
                stats["lines_total"] += 1
                line = raw.strip()
                if not line:
                    stats["blank"] += 1
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError as exc:
                    log.append(f"- bad JSON at {p.name}:{lineno} ({exc}); skipped")
                    stats["bad_json"] += 1
                    continue

                rid = str(rec.get("review_id", "")).strip()
                if not rid:
                    log.append(f"- no review_id at {p.name}:{lineno}; skipped")
                    stats["no_id"] += 1
                    continue

                low = rid.lower()
                if low in example_ids:
                    stats["codebook"] += 1
                    continue
                if low in spent_ids:
                    stats["validation"] += 1
                    continue

                labs, col_labs = labels_of(rec, keys)

                if rid in pool:
                    stats["duplicate"] += 1
                    prev = pool[rid]
                    if prev["labels"] != labs:
                        log.append(
                            f"- `{rid}` repeats at {p.name}:{lineno} with different "
                            f"labels (kept {prev['labels']} from "
                            f"{prev['source_file']}:{prev['lineno']}, "
                            f"ignored {labs})"
                        )
                        stats["duplicate_conflict"] += 1
                    continue

                if labs != col_labs:
                    log.append(f"- `{rid}`: labels array {labs} and binary columns "
                               f"{col_labs} disagree; used the array")
                    stats["label_mismatch"] += 1

                is_none = not labs and str(rec.get("none", 0)) in TRUE
                coded = bool(labs) or is_none or str(rec.get("saved", 0)) in TRUE
                if not INCLUDE_UNCODED and not coded:
                    stats["uncoded"] += 1
                    continue

                pool[rid] = {
                    "rec": rec,
                    "labels": labs,
                    "none": is_none,
                    "source_file": p.name,
                    "lineno": lineno,
                }
                stats["pool"] += 1

    return list(pool.values()), stats


# ───────────────────────────────── sampling ─────────────────────────────────

def sample(pool, keys, rng, log):
    """
    Nones -> greedy label coverage (multi-label rows preferred) -> random fill.
    The fill is uniform over what is left, so it inherits the corpus label
    distribution rather than imposing one.
    """
    support = Counter()
    for r in pool:
        support.update(r["labels"])

    chosen: dict[str, dict] = {}
    bucket: dict[str, str] = {}
    counts = Counter()

    def key_of(r):
        return r["rec"]["review_id"]

    def take(r, why):
        rid = key_of(r)
        if rid in chosen:
            return False
        chosen[rid] = r
        bucket[rid] = why
        counts.update(r["labels"])
        return True

    def deficit():
        return {k for k in keys if counts[k] < min(PER_LABEL_MIN, support[k])}

    def shuffled(rows):
        rows = sorted(rows, key=key_of)
        rng.shuffle(rows)
        return rows

    # 1. true-None reviews
    none_pool = shuffled([r for r in pool if r["none"]])
    for r in none_pool[:NONE_TARGET]:
        take(r, "none")
    if len(none_pool) < NONE_TARGET:
        log.append(f"- only {len(none_pool)} true-None reviews left in the pool "
                   f"(wanted {NONE_TARGET})")

    # 2. greedy coverage of every label with support left
    labelled = shuffled([r for r in pool if r["labels"]])
    while True:
        want = deficit()
        if not want or len(chosen) >= TOTAL:
            break
        avail = [r for r in labelled if key_of(r) not in chosen
                 and set(r["labels"]) & want]
        if not avail:
            break
        # Most needed labels per row wins, so multi-label rows carry the budget.
        # Ties: fewer already-covered extras, then rarer labels first.
        best = max(avail, key=lambda r: (
            len(set(r["labels"]) & want),
            -len(set(r["labels"]) - want),
            -min(support[k] for k in r["labels"]),
        ))
        gained = sorted(set(best["labels"]) & want, key=keys.index)
        take(best, "cover:" + "+".join(gained))

    if len(chosen) >= TOTAL and deficit():
        log.append(f"- budget of {TOTAL} ran out during coverage; "
                   f"{len(deficit())} label(s) never reached the floor")

    # 3. fill at random from what is left, which tracks corpus prevalence
    rest = shuffled([r for r in pool if key_of(r) not in chosen and not r["none"]])
    for r in rest:
        if len(chosen) >= TOTAL:
            break
        take(r, "fill")

    if len(chosen) < TOTAL:
        log.append(f"- pool exhausted at {len(chosen)} rows (target {TOTAL})")

    missing = [k for k in keys if counts[k] < PER_LABEL_MIN]
    for k in missing:
        why = ("no rows left outside the codebook and validation set"
               if support[k] == 0 else f"{support[k]} available, budget ran out")
        log.append(f"- {k}: not represented ({why})")

    return chosen, bucket, counts, support


# ────────────────────────────────── output ──────────────────────────────────

def to_record(r, why, codebook_version):
    rec = r["rec"]
    out = {f: rec.get(f, "") for f in META_FIELDS}
    out["source_file"] = r["source_file"]
    out["codebook_version"] = codebook_version
    out["set_role"] = SET_ROLE
    out["sample_bucket"] = why
    out["from_codebook"] = False
    out["actual_labels"] = r["labels"]
    out["actual_labels_str"] = "; ".join(r["labels"])
    out["assigned_labels"] = []
    out["assigned_spans"] = []
    out["coder_id"] = ""
    out["coder_notes"] = ""
    return out


def write_jsonl(path, records):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def main() -> int:
    log: list[str] = []

    cb_path = Path(CODEBOOK)
    if not cb_path.exists():
        print(f"codebook not found: {CODEBOOK}", file=sys.stderr)
        return 1
    keys, pretty, version, example_ids = load_codebook(cb_path)

    spent_ids = load_excluded_ids(EXCLUDE_FILES, log)
    pool, stats = load_pool(INPUT_DIR, keys, example_ids, spent_ids, log)
    if not pool:
        print("no eligible reviews after filtering", file=sys.stderr)
        return 1

    rng = random.Random(SEED)
    chosen, bucket, counts, support = sample(pool, keys, rng, log)

    ordered = sorted(chosen.values(), key=lambda r: r["rec"]["review_id"])
    rng.shuffle(ordered)
    records = [to_record(r, bucket[r["rec"]["review_id"]], version)
               for r in ordered]

    # hard guarantee: nothing here is also in the validation set
    leaked = [rec["review_id"] for rec in records
              if str(rec["review_id"]).lower() in spent_ids]
    if leaked:
        print(f"ABORT: {len(leaked)} sampled id(s) are in the validation set: "
              f"{leaked[:5]}", file=sys.stderr)
        return 1

    write_jsonl(OUT, records)
    if BLIND_OUT:
        blind = []
        for rec in records:
            b = dict(rec)
            for k in ("actual_labels", "actual_labels_str",
                      "sample_bucket", "from_codebook"):
                b.pop(k, None)
            blind.append(b)
        write_jsonl(BLIND_OUT, blind)

    # ---- report -------------------------------------------------------
    n_none = sum(1 for r in ordered if r["none"])
    n_multi = sum(1 for r in ordered if len(r["labels"]) >= 2)
    n_single = sum(1 for r in ordered if len(r["labels"]) == 1)
    accounted = (stats["blank"] + stats["bad_json"] + stats["no_id"]
                 + stats["codebook"] + stats["validation"] + stats["duplicate"]
                 + stats["uncoded"] + stats["pool"])

    covered = sum(1 for k in keys if counts[k] >= 1)
    zero_support = [k for k in keys if support[k] == 0]
    missing = [k for k in keys if counts[k] == 0]

    bucket_counts = Counter(bucket[r["rec"]["review_id"]].split(":")[0]
                            for r in ordered)
    markets = Counter(r["rec"].get("market", "") for r in ordered)
    stars = Counter(r["rec"].get("star_rating", "") for r in ordered)
    strata = Counter(r["rec"].get("stratum", "") for r in ordered)
    games = Counter(r["rec"].get("game_name", "") for r in ordered)

    lines = [
        f"# tuning / bake-off set, codebook v{version}",
        "",
        "**This set is burned.** Prompt refinement and provider selection run "
        "here, so no number computed on these rows belongs in a reported "
        "evaluation. Every record carries "
        f"`set_role: \"{SET_ROLE}\"`.",
        "",
        f"- seed: `{SEED}`  |  input folder: `{INPUT_DIR}/`",
        f"- output: `{OUT}`" + (f"  |  blind: `{BLIND_OUT}`" if BLIND_OUT else ""),
        f"- eligible pool: **{len(pool)}**  |  sampled: **{len(ordered)}** "
        f"(target {TOTAL})",
        f"- true-None: **{n_none}** (target {NONE_TARGET})  |  "
        f"single-label: **{n_single}**  |  multi-label: **{n_multi}**",
        f"- labels represented: **{covered}/{len(keys)}**",
        f"- codebook example ids indexed: **{len(example_ids)}**  |  "
        f"validation ids excluded: **{len(spent_ids)}**",
        "",
        "## line accounting",
        "",
        "| outcome | lines |",
        "| --- | ---: |",
        f"| blank | {stats['blank']} |",
        f"| unparseable JSON | {stats['bad_json']} |",
        f"| no review_id | {stats['no_id']} |",
        f"| codebook example, excluded | {stats['codebook']} |",
        f"| already in the validation set, excluded | {stats['validation']} |",
        f"| repeat of an earlier review_id, collapsed | {stats['duplicate']} |",
        f"| uncoded | {stats['uncoded']} |",
        f"| eligible pool | {stats['pool']} |",
        f"| **total lines read** | **{stats['lines_total']}** |",
        "",
        f"Sum of outcomes: {accounted}"
        + ("" if accounted == stats["lines_total"]
           else f"  <- DOES NOT MATCH {stats['lines_total']}, investigate"),
        "",
        f"Repeats whose labels differed from the copy that was kept: "
        f"**{stats['duplicate_conflict']}** (listed in the notes).",
        f"Rows whose labels array disagreed with the binary columns: "
        f"**{stats['label_mismatch']}**.",
        "",
        "## sample composition",
        "",
        "| bucket | n |",
        "| --- | ---: |",
    ]
    for k, v in bucket_counts.most_common():
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "| field | distribution |",
        "| --- | --- |",
        "| stratum | " + ", ".join(f"{k or 'blank'} {v}"
                                   for k, v in strata.most_common()) + " |",
        "| market | " + ", ".join(f"{k or 'blank'} {v}"
                                  for k, v in markets.most_common()) + " |",
        "| star rating | " + ", ".join(
            f"{k} star {v}" for k, v in sorted(stars.items(),
                                               key=lambda x: str(x[0]))) + " |",
        f"| distinct games | {len(games)} |",
        f"| most from one game | {games.most_common(1)[0][1] if games else 0} "
        f"(no cap applied) |",
        f"| labels per review | mean "
        f"{sum(len(r['labels']) for r in ordered) / max(1, len(ordered)):.2f} |",
        "",
        "## label coverage",
        "",
        "| label | left in pool | in sample | represented |",
        "| --- | ---: | ---: | :---: |",
    ]
    for k in keys:
        ok = "yes" if counts[k] >= 1 else ("EMPTY POOL" if support[k] == 0 else "NO")
        lines.append(f"| {pretty[k]} | {support[k]} | {counts[k]} | {ok} |")

    if missing:
        lines += [
            "",
            "### labels not represented",
            "",
            "| label | left in pool | reason |",
            "| --- | ---: | --- |",
        ]
        for k in missing:
            reason = ("every remaining row is a codebook example or in the "
                      "validation set" if support[k] == 0
                      else "rows exist, but the 50-row budget ran out")
            lines.append(f"| {pretty[k]} | {support[k]} | {reason} |")
    if zero_support:
        lines += ["", f"Labels with nothing left to draw from: "
                      f"{', '.join(zero_support)}. Raising TOTAL will not help; "
                      f"only new coding will."]
    if log:
        lines += ["", "## notes", ""] + log

    report = "\n".join(lines)
    print(report)
    if REPORT:
        rp = Path(REPORT)
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(report + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())