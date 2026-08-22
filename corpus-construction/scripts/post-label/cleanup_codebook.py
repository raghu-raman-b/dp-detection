#!/usr/bin/env python3
"""
clean_codebook.py  --  one-off structural cleanup of the dark-patterns codebook.

What it does (structure only, never wording):
  1. Splits the appended "Justification:" / "Labels:" prose out of every example
     text into its own field. The review text left behind is the review, nothing else.
  2. Strips the stray "Review:" prefix from example texts.
  3. Strips whitespace from review_ids.
  4. Reconciles the same review_id appearing in several slots with different text
     down to one canonical text.
  5. Prints every inconsistency it finds, and every change it made.

It does NOT paraphrase, reword, shorten or invent anything. Every character it keeps
is a character that was already in the codebook; it only moves text between fields.

Version is deliberately NOT bumped: this is a cleanup, not a content change.
"""

from __future__ import annotations

import difflib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# ------------------------------------------------------------------ config
CODEBOOK_IN = "../../codebook_versions/codebook_v0.20.json"
CODEBOOK_OUT = "codebook_final.json"

# Written into the changelog when the cleanup runs. Set to None to skip.
CHANGELOG_NOTE = ("structural cleanup: justification prose split out of example text "
                  "fields, Review: prefixes stripped, review_ids trimmed, duplicate "
                  "example texts reconciled. No wording, rule or label changes.")

# ------------------------------------------------------------------ patterns
# Line-initial markers only. Verified against v0.20: Justification (21 worked, 3 rule),
# Labels (3 rule), Review (1 worked, as a prefix). Nothing mid-sentence, nothing else.
REVIEW_PREFIX = re.compile(r"^\s*Review\s*:\s*")
MARKER = re.compile(r"(?m)^[ \t]*(Justification|Labels?)[ \t]*:[ \t]*")

CLASS_PREFIX = {
    "Temporal": "T",
    "Monetary": "M",
    "Social": "S",
    "Psychological": "P",
    "Technical": "Tech",
}

issues: list[str] = []
free_text_vs: list[str] = []
notes: list[str] = []
changes: list[str] = []


def issue(msg: str) -> None:
    issues.append(msg)


def note(msg: str) -> None:
    notes.append(msg)


def change(msg: str) -> None:
    changes.append(msg)


# ------------------------------------------------------------------ helpers

def derive_code(label: dict) -> str:
    """Identical to build_prompt.derive_code. Kept in sync by hand; the build asserts."""
    prefix = CLASS_PREFIX[label["high_level"]]
    words = re.sub(r"[^A-Za-z0-9 ]", " ", label["meso_label"]).split()
    return prefix + "_" + "".join(w[:1].upper() + w[1:] for w in words)


def norm_ws(text: str) -> str:
    """Whitespace-insensitive key for comparing two copies of the same review."""
    return " ".join(str(text).split())


def segment(raw: str, where: str) -> tuple[str, dict[str, str]]:
    """Split one example string into (review_text, {justification, labels}).

    Nothing is dropped: every character either stays in the review or moves into
    one of the returned segments.
    """
    text = str(raw).replace("\r\n", "\n").replace("\r", "\n")

    stripped = REVIEW_PREFIX.sub("", text, count=1)
    if stripped != text:
        change(f"{where}: stripped 'Review:' prefix")
        text = stripped

    marks = list(MARKER.finditer(text))
    if not marks:
        return text.strip(), {}

    review = text[: marks[0].start()].strip()
    segs: dict[str, str] = {}
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        key = "labels" if m.group(1).lower().startswith("label") else "justification"
        value = text[m.end(): end].strip()
        if key in segs:
            issue(f"{where}: '{m.group(1)}:' appears more than once; segments concatenated")
            segs[key] = segs[key] + "\n" + value
        else:
            segs[key] = value
        change(f"{where}: split out {key} ({len(value)} chars)")

    if not review:
        issue(f"{where}: review text is empty after splitting off the markers")
    return review, segs


def parse_label_names(raw: str, name_to_code: dict[str, str], where: str) -> list[str] | None:
    """Map a 'Labels: A, B' line onto codes. Returns None if anything fails to map."""
    body = raw.strip()
    if body.lower().rstrip(".").strip() == "none":
        return []
    parts = [p.strip().rstrip(".").strip() for p in re.split(r",|;| and ", body) if p.strip()]
    codes, unmatched = [], []
    for p in parts:
        key = p.lower()
        if key in name_to_code:
            codes.append(name_to_code[key])
        else:
            unmatched.append(p)
    if unmatched:
        issue(f"{where}: cannot map label name(s) to codes: {unmatched!r} "
              f"(raw line kept verbatim, no codes assigned)")
        return None
    return codes


# ------------------------------------------------------------------ main

def main() -> int:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(CODEBOOK_IN)
    if not src.exists():
        print(f"codebook not found: {src}", file=sys.stderr)
        return 2
    cb = json.loads(src.read_text(encoding="utf-8"))

    labels = cb["labels"]
    name_to_code = {lab["meso_label"].strip().lower(): derive_code(lab) for lab in labels}
    valid_codes = set(name_to_code.values())
    class_names = {c["name"] for c in cb["high_level_classes"]}
    meso_names = {lab["meso_label"] for lab in labels}

    if len(valid_codes) != len(labels):
        issue("derived label codes are not 1:1 with labels; build_prompt.py will refuse to build")

    # ---- pass 1: structural integrity of the label objects
    for lab in labels:
        name = lab["meso_label"]
        if lab["high_level"] not in class_names:
            issue(f"label {name!r}: high_level {lab['high_level']!r} is not a declared class")
        if not str(lab.get("canonical_definition", "")).strip():
            issue(f"label {name!r}: canonical_definition is empty")
        if not lab.get("indicators"):
            note(f"label {name!r}: no indicators")
        for br in lab.get("boundary_rules", []):
            vs = str(br.get("vs_label", "")).strip()
            if not vs:
                issue(f"label {name!r}: boundary rule with no vs_label")
            elif vs not in meso_names:
                # vs_label is often a contrast case rather than another label
                # ("UI complaint", "NONE"). Only flag the near-misses, which are
                # almost certainly meant to name a real label.
                close = difflib.get_close_matches(vs.lower(),
                                                  [m.lower() for m in meso_names],
                                                  n=1, cutoff=0.85)
                if close:
                    real = next(m for m in meso_names if m.lower() == close[0])
                    issue(f"label {name!r}: boundary rule vs_label {vs!r} nearly matches "
                          f"the label {real!r}; if it means that label the naming should match")
                else:
                    free_text_vs.append(f"{name} vs {vs!r}")
            if not str(br.get("rule", "")).strip():
                issue(f"label {name!r}: boundary rule vs {br.get('vs_label')!r} has no text")
        if not lab.get("counterexamples"):
            note(f"label {name!r}: no counterexample")
        if not lab.get("worked_examples"):
            note(f"label {name!r}: no worked example")

    # ---- pass 2: clean every example slot
    # slot registry: review_id -> list of (where, container, key_for_text)
    by_id: dict[str, list[tuple[str, dict, str]]] = defaultdict(list)
    slots_with_text = 0
    slots_with_id = 0
    no_justification = []

    for lab in labels:
        name = lab["meso_label"]

        for i, we in enumerate(lab.get("worked_examples", [])):
            where = f"{name} worked_examples[{i}]"
            slots_with_text += 1
            rid = str(we.get("review_id", ""))
            if rid != rid.strip():
                change(f"{where}: trimmed whitespace from review_id")
                rid = rid.strip()
                we["review_id"] = rid
            if not rid:
                issue(f"{where}: no review_id; this example cannot be excluded from sampling")
            else:
                slots_with_id += 1

            review, segs = segment(we.get("text", ""), where)
            we["text"] = review
            if "justification" in segs:
                we["justification"] = segs["justification"]
            else:
                we.setdefault("justification", None)
                no_justification.append(where)
            if "labels" in segs:
                codes = parse_label_names(segs["labels"], name_to_code, where)
                existing = we.get("labels_assigned") or []
                if codes is not None and existing and sorted(codes) != sorted(existing):
                    issue(f"{where}: inline 'Labels:' line disagrees with labels_assigned "
                          f"({codes} vs {existing}); labels_assigned kept")
                if codes is not None and not existing:
                    we["labels_assigned"] = codes
                    change(f"{where}: labels_assigned populated from inline Labels: line")
                we["labels_line_raw"] = segs["labels"]

            bad = [c for c in (we.get("labels_assigned") or []) if c not in valid_codes]
            if bad:
                issue(f"{where}: labels_assigned contains unknown code(s) {bad}")
            if not we.get("labels_assigned"):
                issue(f"{where}: worked example has no labels_assigned")
            if rid:
                by_id[rid].append((where, we, "text"))

        for i, ce in enumerate(lab.get("counterexamples", [])):
            where = f"{name} counterexamples[{i}]"
            slots_with_text += 1
            rid = str(ce.get("review_id", ""))
            if rid != rid.strip():
                change(f"{where}: trimmed whitespace from review_id")
                rid = rid.strip()
                ce["review_id"] = rid
            if not rid:
                issue(f"{where}: no review_id; this example cannot be excluded from sampling")
            else:
                slots_with_id += 1

            review, segs = segment(ce.get("text", ""), where)
            ce["text"] = review
            if segs:
                issue(f"{where}: counterexample carried inline {sorted(segs)} prose; "
                      "split out, but check it against why_not")
                for k, v in segs.items():
                    ce[f"inline_{k}"] = v
            if not str(ce.get("why_not", "")).strip():
                issue(f"{where}: why_not is empty")
            if rid:
                by_id[rid].append((where, ce, "text"))

    # ---- pass 3: rule-level examples
    for r in cb["global_rules"]:
        raw = str(r.get("worked_example_text", "") or "")
        rid = str(r.get("worked_example_review_id", "") or "")
        if rid != rid.strip():
            change(f"rule {r['id']}: trimmed whitespace from worked_example_review_id")
            rid = rid.strip()
            r["worked_example_review_id"] = rid
        if not raw and not rid:
            note(f"rule {r['id']}: no worked example")
            continue
        where = f"rule {r['id']}"
        slots_with_text += 1
        if not rid:
            issue(f"{where}: has {len(raw)} chars of example text but no review_id")
        else:
            slots_with_id += 1

        review, segs = segment(raw, where)
        r["worked_example_text"] = review
        r["worked_example_justification"] = segs.get("justification")
        if "labels" in segs:
            codes = parse_label_names(segs["labels"], name_to_code, where)
            r["worked_example_labels_raw"] = segs["labels"]
            r["worked_example_labels"] = codes if codes is not None else None
        else:
            r.setdefault("worked_example_labels_raw", None)
            r.setdefault("worked_example_labels", None)
        if not r["worked_example_justification"] and not r.get("worked_example_labels_raw"):
            note(f"{where}: worked example has no justification and no labels line")
        if rid:
            by_id[rid].append((where, r, "worked_example_text"))

    # ---- pass 4: reconcile one review_id to one text
    for rid, slots in sorted(by_id.items()):
        if len(slots) < 2:
            continue
        variants = {norm_ws(obj[key]) for _, obj, key in slots}
        if len(variants) == 1:
            continue
        longest_where, longest_obj, longest_key = max(
            slots, key=lambda s: len(s[1][s[2]]))
        canonical = longest_obj[longest_key]
        trivial = len({norm_ws(obj[key]).rstrip(".!? ") for _, obj, key in slots}) == 1
        msg = (f"review_id {rid[:8]}: {len(slots)} slots held different text "
               f"({', '.join(w for w, _, _ in slots)}); adopted the longest, "
               f"from {longest_where}")
        if trivial:
            change(msg + " (differed only in whitespace/terminal punctuation)")
        else:
            issue(msg + " -- the texts differ in substance, check which is the real review")
        for where, obj, key in slots:
            if obj[key] != canonical:
                change(f"{where}: text replaced with the canonical copy of {rid[:8]}")
                obj[key] = canonical

    # ---- pass 5: totals
    all_ids = sorted(by_id)
    idless = [w for w, _, _ in
              [(f"rule {r['id']}", None, None) for r in cb["global_rules"]
               if str(r.get("worked_example_text", "") or "")
               and not str(r.get("worked_example_review_id", "") or "").strip()]]

    if CHANGELOG_NOTE and changes:
        entry = {"version": cb.get("version"), "note": CHANGELOG_NOTE}
        if isinstance(cb.get("changelog"), list):
            cb["changelog"].append(entry)
        else:
            cb["changelog"] = [cb.get("changelog"), entry]

    out = src.parent / CODEBOOK_OUT
    out.write_text(json.dumps(cb, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # ---- report
    w = sys.stdout.write
    w("\n" + "=" * 78 + "\n")
    w(f"codebook cleanup   {src.name}  ->  {out.name}\n")
    w(f"version {cb.get('version')} (unchanged; cleanup only)\n")
    w("=" * 78 + "\n\n")

    w("TOTALS\n")
    w(f"  rules                    : {len(cb['global_rules'])}\n")
    w(f"  classes                  : {len(cb['high_level_classes'])}\n")
    w(f"  labels                   : {len(labels)}\n")
    w(f"  example slots with text  : {slots_with_text}\n")
    w(f"  slots carrying an id     : {slots_with_id}\n")
    w(f"  distinct review ids      : {len(all_ids)}\n")
    w(f"  distinct example reviews : {len(all_ids) + len(idless)}"
      f"{'  (' + str(len(idless)) + ' with no id)' if idless else ''}\n")
    w(f"  worked examples w/ justification : "
      f"{sum(1 for lab in labels for we in lab.get('worked_examples', []) if we.get('justification'))}"
      f" of {sum(len(lab.get('worked_examples', [])) for lab in labels)}\n")
    w("\n")

    if changes:
        w(f"CHANGES MADE ({len(changes)})\n")
        for c in changes:
            w(f"  - {c}\n")
        w("\n")

    if free_text_vs:
        w(f"BOUNDARY RULES vs A CONTRAST CASE, not a label ({len(free_text_vs)}, expected)\n")
        for v in free_text_vs:
            w(f"  . {v}\n")
        w("\n")

    if notes:
        w(f"NOTES ({len(notes)}, not blocking)\n")
        for n in notes:
            w(f"  - {n}\n")
        w("\n")

    if issues:
        w(f"INCONSISTENCIES ({len(issues)}) -- fix these before building prompts\n")
        for i in issues:
            w(f"  ! {i}\n")
        w("\n")
        w(f"wrote {out}\n")
        return 1

    w("A-OK ready to move\n\n")
    w(f"wrote {out}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())