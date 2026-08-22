#!/usr/bin/env python3
"""
build_validation_set.py — sample a coder-training / validation set from the
pilot-coded dark-pattern review files.

Edit the CONFIG block, then:  python3 build_validation_set.py

Order of operations
-------------------
  1. index every review_id used as an example in the codebook (worked
     examples, counterexamples, rule examples)
  2. load every *.jsonl in INPUT_DIR, collapse repeated review_ids to their
     first occurrence, skip anything indexed in step 1
  3. sample, then write the validation jsonl and a markdown report

Codebook examples are matched by review_id alone. No text matching.
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

OUT = "../../validation/validation_set.jsonl"
BLIND_OUT = "../../validation/validation_set_blind.jsonl"   # None to skip
REPORT = "../../validation/validation_report.md"        # None to skip

SEED = 20260812

TOTAL = 75                   # target size of the validation set
PER_LABEL_MIN = 2            # floor per meso label, where support allows
NONE_MIN, NONE_MAX = 8, 10   # true-None reviews
COMBO_MIN, COMBO_MAX = 4, 5  # multi-label reviews
MAX_COMBO_LABELS = 3         # prefer combos with at most this many labels
MAX_PER_GAME = 4             # soft cap on reviews from one app_id

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


# ───────────────────────────────── loading ─────────────────────────────────

def labels_of(rec: dict, keys: list[str]):
    """Returns (labels from the array, labels from the binary columns)."""
    from_cols = sorted({k for k in keys if str(rec.get(k, 0)) in TRUE},
                       key=keys.index)
    arr = rec.get("labels")
    if isinstance(arr, list):
        return sorted({a for a in arr if a in keys}, key=keys.index), from_cols
    return from_cols, from_cols


def load_pool(input_dir, keys, example_ids, log):
    d = Path(input_dir)
    if not d.is_dir():
        raise SystemExit(f"input folder not found: {input_dir}/")

    skip_names = {Path(x).name for x in (OUT, BLIND_OUT) if x}
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

                if rid.lower() in example_ids:
                    stats["codebook"] += 1
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
    none_pool = [r for r in pool if r["none"]]
    single_pool = [r for r in pool if len(r["labels"]) == 1]
    multi_pool = [r for r in pool if len(r["labels"]) >= 2]

    support = Counter()
    for r in pool:
        support.update(r["labels"])

    chosen: dict[str, dict] = {}
    bucket: dict[str, str] = {}
    per_game = Counter()
    counts = Counter()

    def key_of(r):
        return r["rec"]["review_id"]

    def take(r, why):
        rid = key_of(r)
        if rid in chosen:
            return False
        chosen[rid] = r
        bucket[rid] = why
        per_game[r["rec"].get("app_id", "")] += 1
        counts.update(r["labels"])
        return True

    def deficit():
        return {k for k in keys if counts[k] < min(PER_LABEL_MIN, support[k])}

    def score(r, want):
        gain = len(set(r["labels"]) & want)
        extra = len(r["labels"]) - gain
        pen = 2 if per_game[r["rec"].get("app_id", "")] >= MAX_PER_GAME else 0
        return (gain, -extra, -pen, -per_game[r["rec"].get("app_id", "")])

    def pick(cands, want, n, why):
        taken = 0
        cands = sorted(cands, key=key_of)
        rng.shuffle(cands)
        while taken < n:
            avail = [r for r in cands if key_of(r) not in chosen]
            if not avail:
                break
            best = max(avail, key=lambda r: score(r, want))
            if want and not (set(best["labels"]) & want) and why.startswith("rare"):
                break
            take(best, why)
            taken += 1
            want = deficit()
        return taken

    # 1. true-None reviews
    got = pick(none_pool, set(), (NONE_MIN + NONE_MAX) // 2, "none")
    if got < NONE_MIN:
        log.append(f"- only {got} true-None reviews available "
                   f"(wanted {NONE_MIN}-{NONE_MAX})")

    # 2. multi-label combos, chosen to cover the rarest labels
    combo_cands = [r for r in multi_pool
                   if len(r["labels"]) <= MAX_COMBO_LABELS] or multi_pool
    got = pick(combo_cands, deficit(), (COMBO_MIN + COMBO_MAX + 1) // 2, "combo")
    if got < COMBO_MIN:
        log.append(f"- only {got} multi-label reviews available "
                   f"(wanted {COMBO_MIN}-{COMBO_MAX})")

    # 3. per-label floor, rarest labels first
    for k in sorted(keys, key=lambda k: (support[k], k)):
        need = min(PER_LABEL_MIN, support[k]) - counts[k]
        if need <= 0:
            continue
        pick([r for r in single_pool if k in r["labels"]], {k}, need, f"rare:{k}")
        need = min(PER_LABEL_MIN, support[k]) - counts[k]
        if need > 0:
            got = pick([r for r in multi_pool if k in r["labels"]], {k},
                       need, f"rare-multi:{k}")
            if got:
                log.append(f"- {k}: needed multi-label reviews to reach the floor "
                           f"(+{got} beyond the combo quota)")

    # 4. top up toward TOTAL, spreading across games
    if len(chosen) < TOTAL:
        n_multi = sum(1 for r in chosen.values() if len(r["labels"]) >= 2)
        rest = sorted([r for r in pool
                       if key_of(r) not in chosen and not r["none"]], key=key_of)
        rng.shuffle(rest)
        rest.sort(key=lambda r: (len(r["labels"]) >= 2,
                                 per_game[r["rec"].get("app_id", "")],
                                 sum(counts[k] for k in r["labels"])
                                 / max(1, len(r["labels"]))))
        for r in rest:
            if len(chosen) >= TOTAL:
                break
            if len(r["labels"]) >= 2 and n_multi >= COMBO_MAX:
                continue
            if take(r, "fill") and len(r["labels"]) >= 2:
                n_multi += 1

    for k in keys:
        if counts[k] < PER_LABEL_MIN:
            log.append(f"- {k}: pilot support {support[k]}, in sample {counts[k]} "
                       f"(below the floor of {PER_LABEL_MIN})")

    return chosen, bucket, counts, support


# ────────────────────────────────── output ──────────────────────────────────

def to_record(r, why, codebook_version):
    rec = r["rec"]
    out = {f: rec.get(f, "") for f in META_FIELDS}
    out["source_file"] = r["source_file"]
    out["codebook_version"] = codebook_version
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

    pool, stats = load_pool(INPUT_DIR, keys, example_ids, log)
    if not pool:
        print("no eligible reviews after filtering", file=sys.stderr)
        return 1

    rng = random.Random(SEED)
    chosen, bucket, counts, support = sample(pool, keys, rng, log)

    ordered = sorted(chosen.values(), key=lambda r: r["rec"]["review_id"])
    rng.shuffle(ordered)
    records = [to_record(r, bucket[r["rec"]["review_id"]], version)
               for r in ordered]

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
    accounted = (stats["blank"] + stats["bad_json"] + stats["no_id"]
                 + stats["codebook"] + stats["duplicate"] + stats["uncoded"]
                 + stats["pool"])

    bucket_counts = Counter(bucket[r["rec"]["review_id"]].split(":")[0]
                            for r in ordered)
    markets = Counter(r["rec"].get("market", "") for r in ordered)
    stars = Counter(r["rec"].get("star_rating", "") for r in ordered)
    strata = Counter(r["rec"].get("stratum", "") for r in ordered)
    games = Counter(r["rec"].get("game_name", "") for r in ordered)

    lines = [
        f"# validation set, codebook v{version}",
        "",
        f"- seed: `{SEED}`  |  input folder: `{INPUT_DIR}/`",
        f"- output: `{OUT}`",
        f"- eligible pool: **{len(pool)}**  |  sampled: **{len(ordered)}** "
        f"(target {TOTAL})",
        f"- true-None: **{n_none}** (want {NONE_MIN}-{NONE_MAX})",
        f"- multi-label: **{n_multi}** (want {COMBO_MIN}-{COMBO_MAX})"
        + ("  <- over the ceiling, label coverage took priority"
           if n_multi > COMBO_MAX else ""),
        f"- codebook example ids indexed: **{len(example_ids)}**",
        "",
        "## line accounting",
        "",
        "| outcome | lines |",
        "| --- | ---: |",
        f"| blank | {stats['blank']} |",
        f"| unparseable JSON | {stats['bad_json']} |",
        f"| no review_id | {stats['no_id']} |",
        f"| codebook example, excluded | {stats['codebook']} |",
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
        f"(cap {MAX_PER_GAME}) |",
        f"| labels per review | mean "
        f"{sum(len(r['labels']) for r in ordered) / max(1, len(ordered)):.2f} |",
        "",
        "## label coverage",
        "",
        "| label | pilot support | in sample | floor met |",
        "| --- | ---: | ---: | :---: |",
    ]
    for k in keys:
        ok = "yes" if counts[k] >= min(PER_LABEL_MIN, support[k]) else "NO"
        lines.append(f"| {pretty[k]} | {support[k]} | {counts[k]} | {ok} |")
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