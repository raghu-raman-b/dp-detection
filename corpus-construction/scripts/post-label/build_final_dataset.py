#!/usr/bin/env python3
"""
build_final_dataset.py — reshape samples/pool.jsonl into the blind record
format the teacher runners (run_teacher_*.py) expect.

pool.jsonl is unlabeled, so there is no gold/blind split and no report --
this just renames/adds the fields that build_tuning_set.py's blind output
carries, so the pool can be pointed at with --reviews as-is.

Edit the CONFIG block, then:  python3 build_final_dataset.py
"""

from __future__ import annotations

import json
from pathlib import Path

# ═══════════════════════════════ CONFIG ═══════════════════════════════

POOL_IN = "../../samples/pool.jsonl"

CODEBOOK = "../../../codebook_versions/codebook_v0.20.json"

OUT = "../../dataset/final_dataset.jsonl"

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


def main() -> int:
    cb_path = Path(CODEBOOK)
    codebook_version = ""
    if cb_path.exists():
        codebook_version = str(json.loads(cb_path.read_text(encoding="utf-8"))
                                .get("version", ""))

    in_path = Path(POOL_IN)
    if not in_path.exists():
        raise SystemExit(f"input file not found: {POOL_IN}")

    records = []
    with open(in_path, encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.strip()
            if not line:
                continue
            rec = json.loads(line)
            records.append(to_record(rec, in_path.name, codebook_version))

    out_path = Path(OUT)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"wrote {len(records)} rows -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
