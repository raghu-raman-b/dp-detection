#!/usr/bin/env python3
"""Dedupe and combine JSONL review files, keyed on review_id."""

import json
import os

# ── CONFIG ──────────────────────────────────────────────────────────
DIR = "../labeled_data"
INPUT_FILES = [
    "targeted_2.jsonl",
    "targeted_200.jsonl",
    "targeted.jsonl",
    "fsi.jsonl",
    "minors.jsonl",
]
OP = "targeted.jsonl"
# ────────────────────────────────────────────────────────────────────


def main():
    seen = {}          # review_id -> record (first occurrence wins)
    order = []          # preserves first-seen order for output
    dupes = 0
    per_file_counts = {}

    for name in INPUT_FILES:
        path = os.path.join(DIR, name)
        count = 0
        with open(path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as e:
                    raise ValueError(f"{path}:{line_no}: invalid JSON — {e}")

                rid = record.get("review_id")
                if rid is None:
                    raise ValueError(f"{path}:{line_no}: missing review_id")

                count += 1
                if rid in seen:
                    dupes += 1
                    continue
                seen[rid] = record
                order.append(rid)
        per_file_counts[path] = count

    op_path = os.path.join(DIR, OP)
    with open(op_path, "w", encoding="utf-8") as out:
        for rid in order:
            out.write(json.dumps(seen[rid], ensure_ascii=False) + "\n")

    total = sum(per_file_counts.values())
    print(f"Read {total} lines from {len(INPUT_FILES)} files:")
    for path, count in per_file_counts.items():
        print(f"  {path}: {count}")
    print(f"Duplicate review_ids skipped: {dupes}")
    print(f"Unique records written to {op_path}: {len(order)}")


if __name__ == "__main__":
    main()