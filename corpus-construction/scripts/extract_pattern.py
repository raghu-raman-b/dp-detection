#!/usr/bin/env python3
"""
extract_pattern.py — pull every review carrying a given dark-pattern label
into a flat text file for quick eyeball verification.

Usage:  edit the CONFIG block, then `python extract_pattern.py`
        or override from the CLI:  `python extract_pattern.py 24`
                                   `python extract_pattern.py P_IllusionOfControl`
                                   `python extract_pattern.py --list`
"""

import json
import sys
from pathlib import Path

# ─────────────────────────── CONFIG ───────────────────────────

# Which label to pull. Either the index from LABELS below, or the code string.
PATTERN = 20                      # 24 = P_IllusionOfControl

# Input files. Globs are fine.
INPUT_FILES = [
    "random.jsonl",
    "targeted_200.jsonl",
    "targeted_2.jsonl",
    "minors.jsonl",
    "fsi.jsonl",
    "targeted.jsonl"
]

INPUT_DIR = "../labeled_data/"                    # directory the filenames above live in
OUTPUT_DIR = "../outputs"                   # where the _samples.txt lands

# Treat a review as carrying the pattern if EITHER the binary column is 1
# OR the code appears in the `labels` array. Set to False to require the
# binary column only.
UNION_OF_SOURCES = True

# Include the full review text (False = ids + metadata only).
INCLUDE_TEXT = True

# Drop repeats of the same review_id (kept: first occurrence).
DEDUPE_BY_REVIEW_ID = True

# ──────────────────────────────────────────────────────────────

LABELS = [
    "T_PlayingByAppointment",          # 0
    "T_DailyRewards",                  # 1
    "T_Grinding",                      # 2
    "T_Advertisement",                 # 3
    "T_InfiniteTreadmill",             # 4
    "T_MandatoryMarathon",             # 5
    "M_PayToProgress",                 # 6
    "M_IntermediateCurrency",          # 7
    "M_DeceptiveLuxury",               # 8
    "M_RecurringFee",                  # 9
    "M_Gambling",                      # 10
    "M_PowerCreep",                    # 11
    "M_WasteAversion",                 # 12
    "M_EasyToPurchase",                # 13
    "M_UIMisdirection",                # 14
    "M_NeverEndingLure",               # 15
    "S_ForcedFellowship",              # 16
    "S_FriendSpamImpersonation",       # 17
    "S_Reciprocity",                   # 18
    "S_EncouragesAntiSocialBehavior",  # 19
    "S_FearOfMissingOutFOMO",          # 20
    "S_Competition",                   # 21
    "P_EasyToGetHardToLose",           # 22
    "P_CompleteTheCollection",         # 23
    "P_IllusionOfControl",             # 24
    "P_AestheticManipulation",         # 25
    "P_OptimismAndFrequencyBiases",    # 26
    "P_RewardMania",                   # 27
    "Tech_FragmentedDownloads",        # 28
    "none",                            # 29  (pseudo-label: the None column)
]


def resolve_pattern(spec):
    """Accept an int index or a code string (case-insensitive)."""
    if isinstance(spec, int):
        if 0 <= spec < len(LABELS):
            return LABELS[spec]
        die(f"index {spec} out of range 0..{len(LABELS) - 1}")
    s = str(spec).strip()
    if s.isdigit():
        return resolve_pattern(int(s))
    for code in LABELS:
        if code.lower() == s.lower():
            return code
    matches = [c for c in LABELS if s.lower() in c.lower()]
    if len(matches) == 1:
        return matches[0]
    if matches:
        die(f"'{spec}' is ambiguous: {', '.join(matches)}")
    die(f"unknown pattern '{spec}'. Run with --list to see the options.")


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def print_labels():
    for i, code in enumerate(LABELS):
        print(f"  {i:>2}  {code}")


def load_rows(paths):
    """Yield (source_file, line_number, record) for every parseable line."""
    bad = 0
    for p in paths:
        with open(p, "r", encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    yield p.name, lineno, json.loads(line)
                except json.JSONDecodeError as e:
                    bad += 1
                    print(f"  ! skipped {p.name}:{lineno} — bad JSON ({e.msg})",
                          file=sys.stderr)
    if bad:
        print(f"  ! {bad} unparseable line(s) skipped", file=sys.stderr)


def carries(rec, code):
    """
    Returns (hit, col_flag, in_array).
    col_flag / in_array are None when the field is absent from the record.
    """
    col = rec.get(code)
    col_flag = None if col is None else str(col).strip() in ("1", "1.0", "True", "true")

    arr = rec.get("labels")
    if code == "none":
        in_array = None          # `none` never appears in the labels array
    else:
        in_array = None if arr is None else code in arr

    if UNION_OF_SOURCES:
        hit = bool(col_flag) or bool(in_array)
    else:
        hit = bool(col_flag)
    return hit, col_flag, in_array


def all_label_codes(rec):
    """Every label code the record asserts, from the binary columns."""
    out = []
    for code in LABELS:
        if code == "none":
            continue
        v = rec.get(code)
        if v is not None and str(v).strip() in ("1", "1.0", "True", "true"):
            out.append(code)
    return out


def main():
    global PATTERN

    args = [a for a in sys.argv[1:]]
    if "--list" in args or "-l" in args:
        print_labels()
        return
    if args:
        PATTERN = args[0]

    code = resolve_pattern(PATTERN)

    in_dir = Path(INPUT_DIR)
    paths = []
    for pat in INPUT_FILES:
        matched = sorted(in_dir.glob(pat)) if any(c in pat for c in "*?[") \
            else [in_dir / pat]
        for m in matched:
            if not m.exists():
                print(f"  ! missing: {m}", file=sys.stderr)
            else:
                paths.append(m)
    if not paths:
        die("no input files found — check INPUT_FILES / INPUT_DIR")

    hits, seen, dupes, mismatches = [], set(), [], []
    total = 0

    for src, lineno, rec in load_rows(paths):
        total += 1
        hit, col_flag, in_array = carries(rec, code)
        if not hit:
            continue

        rid = rec.get("review_id", f"<no-id {src}:{lineno}>")
        if DEDUPE_BY_REVIEW_ID and rid in seen:
            dupes.append((rid, src, lineno))
            continue
        seen.add(rid)

        if col_flag is not None and in_array is not None and col_flag != in_array:
            mismatches.append((rid, col_flag, in_array))

        rec["_src"] = src
        rec["_line"] = lineno
        hits.append(rec)

    out_path = Path(OUTPUT_DIR) / f"{code}_samples.txt"
    with open(out_path, "w", encoding="utf-8") as out:
        out.write(f"PATTERN: {code}\n")
        out.write(f"SOURCES: {', '.join(p.name for p in paths)}\n")
        out.write(f"MATCHED: {len(hits)} of {total} reviews"
                  f"{' (deduped)' if DEDUPE_BY_REVIEW_ID else ''}\n")
        out.write(f"MATCH RULE: {'binary column OR labels array' if UNION_OF_SOURCES else 'binary column only'}\n")
        out.write("=" * 78 + "\n\n")

        for i, r in enumerate(hits, 1):
            co = all_label_codes(r)
            others = [c for c in co if c != code]
            out.write(f"[{i}] {r.get('review_id', '')}\n")
            out.write(f"    file        : {r['_src']}:{r['_line']}\n")
            out.write(f"    game        : {r.get('game_name', '')}  ({r.get('app_id', '')})\n")
            out.write(f"    market/date : {r.get('market', '')}  {r.get('review_date', '')}"
                      f"   stars={r.get('star_rating', '')}\n")
            out.write(f"    stratum     : {r.get('stratum', '')}"
                      f"{'  seed=' + r['seed_keyword'] if r.get('seed_keyword') else ''}\n")
            out.write(f"    all labels  : {', '.join(co) if co else '(none set)'}\n")
            if others:
                out.write(f"    co-occurring: {', '.join(others)}\n")
            out.write(f"    confidence  : {r.get('confidence', '') or '(blank)'}"
                      f"   borderline={r.get('borderline', '')}"
                      f"   flagged={r.get('flagged', '')}\n")
            out.write(f"    rule/version: {r.get('rule_applied', '') or '(blank)'}"
                      f"   / {r.get('codebook_version', '')}"
                      f"   saved={r.get('saved_at', '')}\n")
            if r.get("rationale"):
                out.write(f"    rationale   : {r['rationale']}\n")
            if INCLUDE_TEXT:
                out.write("    ---\n")
                for para in str(r.get("review_text", "")).splitlines() or [""]:
                    out.write(f"    {para}\n")
            out.write("\n" + "-" * 78 + "\n\n")

        if dupes:
            out.write(f"\nDUPLICATE review_ids skipped ({len(dupes)}):\n")
            for rid, src, lineno in dupes:
                out.write(f"  {rid}  (repeat at {src}:{lineno})\n")

        if mismatches:
            out.write(f"\nCOLUMN / labels-ARRAY DISAGREEMENTS ({len(mismatches)}):\n")
            for rid, col_flag, in_array in mismatches:
                out.write(f"  {rid}  column={int(col_flag)}  in_labels={int(in_array)}\n")

    print(f"{code}: {len(hits)} review(s) -> {out_path}")
    if dupes:
        print(f"  {len(dupes)} duplicate review_id(s) skipped")
    if mismatches:
        print(f"  {len(mismatches)} column/labels-array disagreement(s) — listed in the file")
    if not hits:
        print("  (no support for this label in the current set)")


if __name__ == "__main__":
    main()