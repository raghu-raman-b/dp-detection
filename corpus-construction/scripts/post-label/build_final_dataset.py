#!/usr/bin/env python3
"""
build_final_dataset.py — reshape samples/pool.jsonl into the blind record
format the teacher runners (run_teacher_*.py) expect.

pool.jsonl is unlabeled, so there is no gold/blind split and no report --
this just renames/adds the fields that build_tuning_set.py's blind output
carries, so the pool can be pointed at with --reviews as-is.

Reviews that already carry hand labels (labeled_data/*.jsonl) are dropped
by review_id, so the output is strictly the set still needing annotation.
Note the pilot sets were drawn from filtered/ independently of the pool,
so only the subset that happens to also be in the pool gets removed --
the run prints how many of the labeled ids were actually found.

Edit the CONFIG block, then:  python3 build_final_dataset.py
"""

from __future__ import annotations

import json
from pathlib import Path

# ═══════════════════════════════ CONFIG ═══════════════════════════════

POOL_IN = "../../samples/pool.jsonl"

CODEBOOK = "../../../codebook_versions/codebook_v0.20.json"

# Already hand-labeled -- excluded from the output by review_id.
EXCLUDE = [
    "../../labeled_data/random.jsonl",
    "../../labeled_data/targeted.jsonl",
]

OUT = "../../dataset/dataset_to_label.jsonl"

SET_ROLE = "final_dataset"

META_FIELDS = [
    "review_id", "app_id", "game_name", "market", "review_date",
    "star_rating", "review_text", "stratum", "seed_keyword",
]

# ══════════════════════════════════════════════════════════════════════


def to_record(rec: dict, source_file: str, codebook_version: str) -> dict:
    out = {f: rec.get(f, "") for f in META_FIELDS}
    out["source_file"] = source_file
    out["codebook_version"] = codebook_version
    out["set_role"] = SET_ROLE
    out["assigned_labels"] = []
    out["assigned_spans"] = []
    out["coder_id"] = ""
    out["coder_notes"] = ""
    return out


def load_excluded_ids() -> set[str]:
    """review_ids from the hand-labeled files, which must not be re-annotated."""
    ids: set[str] = set()
    for rel in EXCLUDE:
        path = Path(rel)
        if not path.exists():
            raise SystemExit(f"exclude file not found: {rel}")
        n = 0
        with open(path, encoding="utf-8") as fh:
            for lineno, raw in enumerate(fh, 1):
                line = raw.strip()
                if not line:
                    continue
                rid = json.loads(line).get("review_id")
                if not rid:
                    raise SystemExit(f"{rel}:{lineno} has no review_id")
                ids.add(rid)
                n += 1
        print(f"exclude {n:6d} rows from {path.name}")
    return ids


def main() -> int:
    cb_path = Path(CODEBOOK)
    if not cb_path.exists():
        raise SystemExit(f"codebook not found: {CODEBOOK} (run from scripts/post-label/)")
    codebook_version = str(json.loads(cb_path.read_text(encoding="utf-8"))
                            .get("version", ""))
    if not codebook_version:
        raise SystemExit(f"codebook {CODEBOOK} has no version field")

    in_path = Path(POOL_IN)
    if not in_path.exists():
        raise SystemExit(f"input file not found: {POOL_IN}")

    excluded = load_excluded_ids()

    records = []
    total = 0
    dropped = set()
    with open(in_path, encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.strip()
            if not line:
                continue
            rec = json.loads(line)
            rid = rec.get("review_id")
            if not rid:
                raise SystemExit(f"{POOL_IN}:{lineno} has no review_id")
            total += 1
            if rid in excluded:
                dropped.add(rid)
                continue
            records.append(to_record(rec, in_path.name, codebook_version))

    print(f"read    {total:6d} rows from {in_path.name}")
    print(f"dropped {len(dropped):6d} of {len(excluded)} labeled ids "
          f"({len(excluded) - len(dropped)} were not in the pool)")

    if len(records) != total - len(dropped):
        raise SystemExit("row accounting mismatch -- refusing to write")

    out_path = Path(OUT)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"wrote {len(records)} rows -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
