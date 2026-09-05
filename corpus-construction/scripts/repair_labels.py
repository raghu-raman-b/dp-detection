#!/usr/bin/env python3
"""
repair_labels.py -- repair recoverable defects in the teacher's output.

Three defect families, all measured on the live corpus before this was written:

  CODES   the right pattern named with the wrong class prefix -- M_IllusionOfControl
          for P_IllusionOfControl, on a review about buying coins.   (1 in 108,579)
  DUPES   the same code listed twice on one review.                  (166 reviews)
  SPANS   a quoted span that is not a literal substring of the review: case drifted,
          quotes over-escaped, the quote truncated a word, or fragments joined with
          an ellipsis.                                               (971 in 108,579)

Every repair is CONSTRUCTIVE and VERIFIED: a span is only rewritten to a string that
is then confirmed to appear verbatim in the review text, and a code is only rewritten
when exactly one codebook entry matches. Anything that cannot be repaired to a proven
result is reported and left untouched -- a defect you can see beats a guess you cannot.

Repairs are recorded in the row under `repairs`, so the corpus carries its own
correction history and the paper can state exactly what changed.

    python repair_labels.py                     dry run: report, change nothing
    python repair_labels.py --report-only       just the defect inventory
    python repair_labels.py --apply             rewrite in place (atomic, keeps .bak)
    python repair_labels.py --apply --force     ...even if the run looks live

NEVER --apply against a live run: the annotator holds responses.jsonl open in append
mode, and rewriting it between two of its writes drops the rows in the gap.
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
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
DEFAULT_REVIEWS = "../dataset/dataset_to_label.jsonl"
LIVE_WINDOW_S = 120
FUZZ_MIN = 0.85          # matched fraction of the span required to accept a fuzzy fix
SHORT_SPAN = 12          # spans below this are flagged, never "fixed"

BS, DQ, SQ = chr(92), '"', "'"
WS = re.compile(r"\s+")


def norm(s: str) -> str:
    return WS.sub(" ", s or "").strip()


# ------------------------------------------------------------------ code repair

def resolve_code(bad: str, legal: set[str]) -> str | None:
    """The suffix after the first underscore, matched against the codebook."""
    if "_" not in bad:
        return None
    suffix = bad.split("_", 1)[1].lower()
    hits = [c for c in legal if "_" in c and c.split("_", 1)[1].lower() == suffix]
    return hits[0] if len(hits) == 1 else None


# ------------------------------------------------------------------ span repair

def _norm_map(text: str) -> tuple[str, list[int]]:
    """Whitespace-collapsed text plus, for each output char, its index in the original.
    This is what lets a match found in normalised space be cut out of the ORIGINAL
    string -- which is the whole point, since the span has to be verbatim."""
    out: list[str] = []
    idx: list[int] = []
    prev_ws = False
    for i, ch in enumerate(text):
        if ch.isspace():
            if not prev_ws and out:
                out.append(" "); idx.append(i)
            prev_ws = True
        else:
            out.append(ch); idx.append(i)
            prev_ws = False
    while out and out[-1] == " ":
        out.pop(); idx.pop()
    return "".join(out), idx


def _cut(text: str, idx: list[int], lo: int, hi: int) -> str:
    """Slice the ORIGINAL text using normalised-space offsets [lo, hi)."""
    if lo >= len(idx) or hi <= lo:
        return ""
    start = idx[lo]
    end = idx[min(hi, len(idx)) - 1] + 1
    return text[start:end]


def repair_span(span: str, text: str) -> tuple[str | None, str]:
    """Return (verbatim_span, how). None if nothing provable was found.

    Every branch ends by cutting the replacement out of the ORIGINAL review text, so
    the result is verbatim by construction rather than by hope."""
    if not span or not text:
        return None, ""
    if span in text:
        return None, "already-verbatim"

    ntext, idx = _norm_map(text)
    low = ntext.lower()

    def locate(needle: str, how: str):
        n = norm(needle)
        if not n:
            return None, ""
        p = ntext.find(n)
        if p < 0:
            p = low.find(n.lower())
        if p >= 0:
            return _cut(text, idx, p, p + len(n)), how
        return None, ""

    # 1. whitespace and/or case drift
    got, how = locate(span, "whitespace-or-case normalised")
    if got:
        return got, how

    # 2. the model escaped quotes that the review does not contain
    unesc = span.replace(BS + DQ, DQ).replace(BS + SQ, SQ).replace(BS + BS, BS)
    if unesc != span:
        got, how = locate(unesc, "unescaped")
        if got:
            return got, how

    # 3. fragments joined by an ellipsis: span from the first fragment to the last
    if "..." in span or "…" in span:
        parts = [norm(p) for p in re.split(r"\.\.\.|…", span) if norm(p)]
        if len(parts) >= 2:
            first, last = parts[0].lower(), parts[-1].lower()
            a, b = low.find(first), low.rfind(last)
            if a >= 0 and b >= a:
                got = _cut(text, idx, a, b + len(last))
                if got:
                    return got, "ellipsis fragments rejoined"
        for p in sorted(parts, key=len, reverse=True):
            got, how = locate(p, "longest ellipsis fragment")
            if got:
                return got, how

    # 4. truncated or over-extended quote: take the longest common block, and only
    #    when it accounts for most of what the model said it was quoting
    nspan = norm(span)
    sm = difflib.SequenceMatcher(None, nspan.lower(), low, autojunk=False)
    m = sm.find_longest_match(0, len(nspan), 0, len(low))
    if m.size and m.size / len(nspan) >= FUZZ_MIN:
        got = _cut(text, idx, m.b, m.b + m.size)
        if got:
            return got, f"longest common block ({m.size/len(nspan):.0%} of the span)"
    return None, ""


# ------------------------------------------------------------------------ main

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default=DEFAULT_DIR)
    ap.add_argument("--prompt", default=DEFAULT_PROMPT)
    ap.add_argument("--reviews", default=DEFAULT_REVIEWS)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--report-only", action="store_true")
    ap.add_argument("--no-backup", action="store_true")
    ap.add_argument("--fuzz-min", type=float, default=FUZZ_MIN)
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
    print(f"file       {rc.show(responses)}")
    print(f"codebook   {len(legal)} legal codes")
    print(f"last write {age:,.0f}s ago" + ("   <-- RUN LOOKS LIVE" if live else ""))
    if live and a.apply and not a.force:
        sys.exit("\nrefusing to rewrite a file written to seconds ago: the annotator\n"
                 "holds it open in append mode and the rows it writes during the\n"
                 "rewrite would be lost. Stop the run first (Ctrl-C is graceful).")

    rows = [json.loads(l) for l in responses.open(encoding="utf-8") if l.strip()]
    need = {r["review_id"] for r in rows if not r.get("superseded")}
    texts: dict[str, str] = {}
    for line in rc.resolve(a.reviews).open(encoding="utf-8"):
        if not line.strip():
            continue
        x = json.loads(line)
        if x["review_id"] in need:
            texts[x["review_id"]] = x.get("review_text", "")
        if len(texts) == len(need):
            break
    print(f"rows       {len(rows):,}   review texts loaded {len(texts):,}")

    stat = Counter()
    plans: dict[int, list[dict]] = {}
    for i, rec in enumerate(rows):
        if rec.get("superseded"):
            continue
        p = rec.get("parsed")
        if not isinstance(p, dict):
            continue
        text = texts.get(rec["review_id"], "")
        todo: list[dict] = []
        seen: set[str] = set()
        for j, item in enumerate(p.get("labels") or []):
            if not isinstance(item, dict):
                continue
            stat["labels"] += 1
            code = item.get("label")

            if code and code not in legal:
                tgt = resolve_code(code, legal)
                if tgt:
                    todo.append({"i": j, "field": "label", "from": code, "to": tgt,
                                 "how": "class prefix corrected"})
                    stat["code_fixable"] += 1
                    code = tgt
                else:
                    stat["code_unfixable"] += 1

            if code in seen:
                todo.append({"i": j, "field": "_drop", "from": code, "to": None,
                             "how": "duplicate of an earlier label on the same review"})
                stat["dupe_fixable"] += 1
                continue
            if code:
                seen.add(code)

            sp = item.get("span") or ""
            if not sp:
                stat["span_empty"] += 1
            elif sp in text:
                if len(sp) < SHORT_SPAN:
                    stat["span_short_flag"] += 1
            else:
                fixed, how = repair_span(sp, text)
                if fixed and fixed in text:
                    todo.append({"i": j, "field": "span", "from": sp, "to": fixed,
                                 "how": how})
                    stat["span_fixable"] += 1
                else:
                    stat["span_unfixable"] += 1
        if todo:
            plans[i] = todo

    print()
    print(f"  labels scanned              {stat['labels']:,}")
    print(f"  out-of-codebook  fixable    {stat['code_fixable']:,}"
          f"   unfixable {stat['code_unfixable']:,}")
    print(f"  duplicate label  fixable    {stat['dupe_fixable']:,}")
    print(f"  broken span      fixable    {stat['span_fixable']:,}"
          f"   unfixable {stat['span_unfixable']:,}")
    print(f"  empty span (left alone)     {stat['span_empty']:,}")
    print(f"  very short span (flag only) {stat['span_short_flag']:,}")
    total = stat['code_fixable'] + stat['dupe_fixable'] + stat['span_fixable']
    print(f"  -> repairable now           {total:,} in {len(plans):,} row(s)")

    if a.report_only or not a.apply or not total:
        print("\n" + ("report only." if a.report_only else
                      "dry run. re-run with --apply to rewrite."
                      if total else "nothing to repair."))
        return

    if not a.no_backup:
        bak = responses.with_suffix(".jsonl.bak")
        print(f"\nbacking up to {rc.show(bak)} ...")
        shutil.copy2(responses, bak)

    tmp = responses.with_suffix(".jsonl.repair-tmp")
    n_fix = 0
    with tmp.open("w", encoding="utf-8") as fout:
        for i, rec in enumerate(rows):
            todo = plans.get(i)
            if todo:
                labels = rec["parsed"]["labels"]
                for step in sorted(todo, key=lambda s: s["i"]):
                    if step["field"] == "_drop":
                        continue
                    labels[step["i"]][step["field"]] = step["to"]
                drop = {s["i"] for s in todo if s["field"] == "_drop"}
                if drop:
                    rec["parsed"]["labels"] = [x for k, x in enumerate(labels)
                                               if k not in drop]
                rec.setdefault("repairs", []).extend(
                    {"field": s["field"], "from": s["from"], "to": s["to"],
                     "reason": s["how"], "by": "repair_labels.py"} for s in todo)
                n_fix += len(todo)
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
    os.replace(tmp, responses)
    print(f"repaired {n_fix:,} defect(s) across {len(plans):,} row(s); "
          f"each row records what changed under `repairs`.")


if __name__ == "__main__":
    main()
