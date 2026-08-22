#!/usr/bin/env python3
"""
build_input.py -- assemble the adjudication input from labeled_data.

Reads the labeled JSONL files in order, one row at a time, no dedupe, no exclusions.
Every row goes through. Writes one flat JSONL for the runner plus an audit file.

    python build_input.py

The join key for the whole pipeline is row_uid = "<file>:<line_no>", NOT review_id.
review_id is for display. row_uid is what apply_decisions.py uses to write a decision
back to the exact line it came from, which stays unambiguous even if an id repeats.

Blinding: this file carries every source field so the HTML tool can display them, but
the RUNNER sends only game_name, review_text and assigned_labels to the model. Star
rating and seed keyword never reach the model. Seed keyword especially: it names the
phrase the targeted rows were sampled on, so showing it to the checker would hand it
the expected answer on every targeted row.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

# ============================== CONFIG ==============================
DATA_DIR = "../labeled_data"

# Processed in this order. The order is preserved in the output file.
SOURCE_FILES = ["random.jsonl", "targeted.jsonl"]

OUT_FILE   = "../adjudication/input/adjudication_input.jsonl"
AUDIT_FILE = "../adjudication/build_input_audit.txt"

# Codes must match the codebook exactly. Derived the same way build_adjudicate_prompt.py
# derives them, and asserted against the binary columns present in the data.
LABEL_CODES = [
    "T_PlayingByAppointment", "T_DailyRewards", "T_Grinding", "T_Advertisement",
    "T_InfiniteTreadmill", "T_MandatoryMarathon",
    "M_PayToProgress", "M_IntermediateCurrency", "M_DeceptiveLuxury", "M_RecurringFee",
    "M_Gambling", "M_PowerCreep", "M_WasteAversion", "M_EasyToPurchase",
    "M_UIMisdirection", "M_NeverEndingLure",
    "S_ForcedFellowship", "S_FriendSpamImpersonation", "S_Reciprocity",
    "S_EncouragesAntiSocialBehavior", "S_FearOfMissingOutFOMO", "S_Competition",
    "P_EasyToGetHardToLose", "P_CompleteTheCollection", "P_IllusionOfControl",
    "P_AestheticManipulation", "P_OptimismAndFrequencyBiases", "P_RewardMania",
    "Tech_FragmentedDownloads",
]

# Fields copied through for the HTML tool. Not sent to the model.
CARRY = ["app_id", "game_name", "market", "review_date", "star_rating", "review_text",
         "stratum", "seed_keyword", "casino", "labels_str", "confidence", "rule_applied",
         "borderline", "rationale", "flagged", "pass", "codebook_version", "saved_at"]
# ====================================================================


def labels_from_row(row: dict) -> tuple[list[str], list[str]]:
    """Return (labels, problems). Prefers the `labels` array, cross-checks the columns."""
    problems: list[str] = []

    from_cols = [c for c in LABEL_CODES if int(row.get(c, 0) or 0) == 1]
    arr = row.get("labels")

    if isinstance(arr, list):
        unknown = [c for c in arr if c not in LABEL_CODES]
        if unknown:
            problems.append(f"unknown code(s) in labels: {unknown}")
        labels = [c for c in LABEL_CODES if c in arr]      # canonical order
        if set(labels) != set(from_cols):
            problems.append(
                f"labels array != binary columns "
                f"(array only: {sorted(set(labels) - set(from_cols))}, "
                f"columns only: {sorted(set(from_cols) - set(labels))})")
    else:
        problems.append("no labels array; fell back to binary columns")
        labels = from_cols

    none_flag = int(row.get("none", 0) or 0) == 1
    if none_flag and labels:
        problems.append("none=1 but labels present")
    if not none_flag and not labels:
        problems.append("no labels and none=0 (unlabeled or unsaved?)")

    return labels, problems


def main() -> None:
    data_dir = Path(DATA_DIR)
    out_path, audit_path = Path(OUT_FILE), Path(AUDIT_FILE)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    missing = [f for f in SOURCE_FILES if not (data_dir / f).exists()]
    if missing:
        sys.exit(f"missing source file(s) under {data_dir.resolve()}: {missing}")

    records: list[dict] = []
    per_file: dict[str, dict] = {}
    problems: list[str] = []
    ids = Counter()
    support = Counter()

    for fname in SOURCE_FILES:
        n_lines = n_labeled = n_unlabeled = 0
        for line_no, line in enumerate(
                (data_dir / fname).read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            n_lines += 1
            try:
                row = json.loads(line)
            except json.JSONDecodeError as e:
                problems.append(f"{fname}:{line_no} unparseable JSON: {e}")
                continue

            rid = str(row.get("review_id", "")) or f"(missing-id-{fname}-{line_no})"
            ids[rid] += 1
            labels, probs = labels_from_row(row)
            for p in probs:
                problems.append(f"{fname}:{line_no} [{rid[:8]}] {p}")
            for c in labels:
                support[c] += 1

            n_labeled += bool(labels)
            n_unlabeled += not labels

            rec = {
                "row_uid": f"{fname}:{line_no}",
                "source_file": fname,
                "source_line": line_no,
                "review_id": rid,
                "assigned_labels": labels,
            }
            for k in CARRY:
                rec[k] = row.get(k, "")
            records.append(rec)

        per_file[fname] = {"lines": n_lines, "labeled": n_labeled,
                           "unlabeled": n_unlabeled}

    with out_path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    dupes = {k: v for k, v in ids.items() if v > 1}
    zero = [c for c in LABEL_CODES if support[c] == 0]

    lines = [
        "adjudication input build",
        f"source dir : {data_dir.resolve()}",
        f"out        : {out_path.resolve()}",
        "",
        "per file:",
    ]
    for fname, st in per_file.items():
        lines.append(f"  {fname:<20} {st['lines']:>5} rows   "
                     f"labeled {st['labeled']:>4}   unlabeled {st['unlabeled']:>4}")
    tot = sum(s["lines"] for s in per_file.values())
    tl = sum(s["labeled"] for s in per_file.values())
    lines += [
        f"  {'TOTAL':<20} {tot:>5} rows   labeled {tl:>4}   unlabeled {tot - tl:>4}",
        "",
        f"label instances : {sum(support.values())}",
        f"repeated review_ids : {len(dupes)}"
        + (f"  {list(dupes)[:10]}" if dupes else "")
        + "   (kept as is; row_uid keeps write-back unambiguous)",
        f"labels with zero support : {zero or 'none'}",
        "",
        f"data problems : {len(problems)}",
    ]
    lines += ["  " + p for p in problems[:200]]
    if len(problems) > 200:
        lines.append(f"  ... and {len(problems) - 200} more")
    lines += ["", "per-label support:"]
    for c in LABEL_CODES:
        lines.append(f"  {c:<32} {support[c]:>4}")

    audit_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"wrote {out_path}  ({tot} rows, {tl} labeled, {tot - tl} unlabeled)",
          file=sys.stderr)
    print(f"audit {audit_path}  ({len(problems)} data problems)", file=sys.stderr)
    if problems:
        print("  ^ read the audit before running; label/column mismatches will "
              "silently change what gets checked.", file=sys.stderr)


if __name__ == "__main__":
    main()