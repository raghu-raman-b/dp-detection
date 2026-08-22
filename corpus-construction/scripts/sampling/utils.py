"""Small shared helpers. No pipeline logic lives here."""
import csv
import json
import os
import tempfile
from pathlib import Path


def read_jsonl(path: Path):
    """Yield dicts from a jsonl file; tolerate a trailing partial line
    (possible if a previous run was killed mid-write)."""
    if not path.exists():
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue  # drop the torn tail line


def append_jsonl(path: Path, rows):
    with open(path, "a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def write_jsonl_atomic(path: Path, rows):
    """Write a whole jsonl file atomically (temp file + rename)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def write_json_atomic(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def write_csv_atomic(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def upsert_csv_row(path: Path, fieldnames, key_fields, row):
    """Idempotent per-key logging: replace the row with the same key, keep
    the rest. Used for scrape_log.csv so re-runs don't duplicate rows."""
    rows = []
    if path.exists():
        with open(path, encoding="utf-8", newline="") as f:
            rows = [r for r in csv.DictReader(f)]
    key = tuple(str(row[k]) for k in key_fields)
    rows = [r for r in rows if tuple(str(r.get(k, "")) for k in key_fields) != key]
    rows.append({k: row.get(k, "") for k in fieldnames})
    rows.sort(key=lambda r: tuple(str(r.get(k, "")) for k in key_fields))
    write_csv_atomic(path, fieldnames, rows)


def count_lines(path: Path) -> int:
    if not path.exists():
        return 0
    with open(path, "rb") as f:
        return sum(1 for _ in f)
