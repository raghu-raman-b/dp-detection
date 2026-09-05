#!/usr/bin/env python3
"""
repair_labels.py -- fix label codes the teacher emitted outside the codebook.

The teacher occasionally names the right pattern with the wrong class prefix:
`M_IllusionOfControl` for `P_IllusionOfControl`, because the review it was reading was
about money. The pattern identification is correct; the two-letter prefix is not.

A repair is only made when it is UNAMBIGUOUS -- the part after the first underscore
matches exactly one legal code. Anything else is reported and left alone, because a
label nobody can resolve is data, and quietly rewriting it to a guess is worse than
leaving it visible.

Every repair is recorded in the row itself under `repairs`, so the corpus carries its
own correction history and the paper can state exactly what was changed and why.

    python repair_labels.py                    dry run: report, change nothing
    python repair_labels.py --apply            rewrite in place (atomic)
    python repair_labels.py --apply --force    ...even if the run looks live

NEVER run --apply against a live run. The annotator holds responses.jsonl open in
append mode; rewriting it between two of its writes drops the rows in the gap, and
those rows are already paid for. The freshness check below is the guard, and --force
exists only for the case where you have confirmed the process is gone.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import runner_common as rc
from build_prompt import load_prompt

DEFAULT_DIR = "../outputs/llm_annotation"
DEFAULT_PROMPT = "../outputs/prompts/teacher_v2_full.txt"
LIVE_WINDOW_S = 120          # a write this recent means the run is probably still going


def resolve_code(bad: str, legal: set[str]) -> str | None:
    """The suffix after the first underscore, matched against the codebook.
    Returns the single legal code that fits, or None if 0 or >1 fit."""
    if "_" not in bad:
        return None
    suffix = bad.split("_", 1)[1].lower()
    hits = [c for c in legal if "_" in c and c.split("_", 1)[1].lower() == suffix]
    return hits[0] if len(hits) == 1 else None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default=DEFAULT_DIR)
    ap.add_argument("--prompt", default=DEFAULT_PROMPT)
    ap.add_argument("--apply", action="store_true", help="rewrite the file (default: dry run)")
    ap.add_argument("--force", action="store_true", help="proceed even if the run looks live")
    ap.add_argument("--no-backup", action="store_true")
    a = ap.parse_args()

    out = rc.resolve(a.dir)
    responses = out / "responses.jsonl"
    if not responses.exists():
        sys.exit(f"not found: {responses}")

    legal = rc.legal_codes_from_prompt(load_prompt(rc.resolve(a.prompt)))
    if not legal:
        sys.exit("could not parse the codebook out of the prompt; refusing to guess")

    age = time.time() - responses.stat().st_mtime
    live = age < LIVE_WINDOW_S
    print(f"file      {rc.show(responses)}")
    print(f"codebook  {len(legal)} legal codes")
    print(f"last write {age:,.0f}s ago" + ("   <-- RUN LOOKS LIVE" if live else ""))
    if live and a.apply and not a.force:
        sys.exit("\nrefusing to rewrite a file that was written to seconds ago.\n"
                 "  the annotator holds it open in append mode; rewriting it now would\n"
                 "  drop whatever it writes in the gap -- reviews you have paid for.\n"
                 "  stop the run (Ctrl-C is graceful), then run this again.")

    # ---- pass 1: find what needs fixing -------------------------------------
    bad = Counter()
    fixable: dict[str, str] = {}
    unfixable: set[str] = set()
    n_rows = 0
    for line in responses.open(encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        n_rows += 1
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        p = rec.get("parsed")
        if not isinstance(p, dict):
            continue
        for item in p.get("labels") or []:
            code = item.get("label") if isinstance(item, dict) else None
            if code and code not in legal:
                bad[code] += 1
                if code not in fixable and code not in unfixable:
                    tgt = resolve_code(code, legal)
                    (fixable.__setitem__(code, tgt) if tgt else unfixable.add(code))

    print(f"rows      {n_rows:,}")
    if not bad:
        print("\nno out-of-codebook labels. nothing to do.")
        return
    print(f"\nout-of-codebook labels: {sum(bad.values())} occurrence(s), "
          f"{len(bad)} distinct")
    for code, n in bad.most_common():
        if code in fixable:
            print(f"  FIX    {code:32s} -> {fixable[code]:32s} ({n})")
        else:
            print(f"  LEAVE  {code:32s}    no unambiguous match     ({n})")
    if not fixable:
        print("\nnothing unambiguously fixable; leaving the file untouched.")
        return
    if not a.apply:
        print("\ndry run. re-run with --apply to rewrite.")
        return

    # ---- pass 2: rewrite atomically -----------------------------------------
    if not a.no_backup:
        bak = responses.with_suffix(".jsonl.bak")
        print(f"\nbacking up to {rc.show(bak)} ...")
        shutil.copy2(responses, bak)

    tmp = responses.with_suffix(".jsonl.repair-tmp")
    n_fixed = 0
    n_rows_touched = 0
    with responses.open(encoding="utf-8") as fin, tmp.open("w", encoding="utf-8") as fout:
        for line in fin:
            stripped = line.strip()
            if not stripped:
                continue
            try:
                rec = json.loads(stripped)
            except json.JSONDecodeError:
                fout.write(line if line.endswith("\n") else line + "\n")
                continue
            p = rec.get("parsed")
            touched = []
            if isinstance(p, dict):
                for item in p.get("labels") or []:
                    if not isinstance(item, dict):
                        continue
                    code = item.get("label")
                    if code in fixable:
                        item["label"] = fixable[code]
                        touched.append({"field": "label", "from": code,
                                        "to": fixable[code],
                                        "reason": "class prefix corrected; suffix "
                                                  "matches exactly one codebook entry",
                                        "by": "repair_labels.py"})
                        n_fixed += 1
            if touched:
                rec.setdefault("repairs", []).extend(touched)
                n_rows_touched += 1
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")

    os.replace(tmp, responses)
    print(f"repaired {n_fixed} label(s) across {n_rows_touched} row(s)")
    print("each repaired row now carries a `repairs` entry recording the change.")


if __name__ == "__main__":
    main()
