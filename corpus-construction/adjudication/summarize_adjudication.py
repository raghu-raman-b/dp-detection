#!/usr/bin/env python3
"""
summarize_adjudication.py -- what the checker actually found, before you rule on any of it.

    python summarize_adjudication.py

Reads adjudicated.jsonl (and decisions.jsonl if it exists) and writes a plain-text report.

The section worth reading first is BY CODEBOOK VERSION. The whole justification for this
pass is rule drift: rules were added mid-coding (Undisclosed Purchase Terms at review
171/200, the Reciprocity mechanism rule, the FS/I rule) and earlier rows were never
rescreened. If contest rates are flat across versions, the flags are ordinary coder noise
and should be reported as such. If they concentrate in rows coded at v0.16-v0.18, that is
a rescreen finding and belongs in the paper.

Nothing here is a validity claim. A model disagreeing with you is not evidence you were
wrong; it is a queue.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

# ============================== CONFIG ==============================
ADJUDICATED_FILE = "adjudicated.jsonl"
DECISIONS_FILE   = "../adjudication/decisions/decisions.jsonl"   # optional
OUT_FILE         = "adjudication_report.txt"
MIN_SUPPORT      = 3        # below this, per-label rates are printed but marked thin
# ====================================================================


def pct(a: int, b: int) -> str:
    return f"{100*a/b:5.1f}%" if b else "    -"


def bucket(rows: list[dict], keyfn) -> dict:
    out = defaultdict(lambda: {"rows": 0, "contested": 0, "labels": 0, "unsupported": 0,
                               "wrong": 0, "none_dis": 0})
    for r in rows:
        adj = r.get("adj") or {}
        k = keyfn(r)
        b = out[k]
        b["rows"] += 1
        verdicts = adj.get("verdicts") or []
        b["labels"] += len(verdicts)
        contested = False
        for v in verdicts:
            if not isinstance(v, dict):
                continue
            if v.get("verdict") == "unsupported":
                b["unsupported"] += 1; contested = True
            elif v.get("verdict") == "wrong_label":
                b["wrong"] += 1; contested = True
        nc = adj.get("none_check")
        if isinstance(nc, dict) and nc.get("supported") is False:
            b["none_dis"] += 1; contested = True
        b["contested"] += contested
    return out


def table(title: str, buckets: dict, lines: list[str]) -> None:
    lines += ["", title, "-" * len(title),
              f"  {'':<22} {'rows':>6} {'contested':>10} {'rate':>7} "
              f"{'labels':>7} {'unsup':>6} {'wrong':>6} {'none!':>6}"]
    for k in sorted(buckets, key=lambda x: (-buckets[x]["rows"], str(x))):
        b = buckets[k]
        lines.append(f"  {str(k):<22} {b['rows']:>6} {b['contested']:>10} "
                     f"{pct(b['contested'], b['rows']):>7} {b['labels']:>7} "
                     f"{b['unsupported']:>6} {b['wrong']:>6} {b['none_dis']:>6}")


def main() -> None:
    adj_path = Path(ADJUDICATED_FILE)
    if not adj_path.exists():
        sys.exit(f"no {adj_path.resolve()} — run run_adjudicate_openai.py --actual first")

    rows = [json.loads(l) for l in adj_path.read_text(encoding="utf-8").splitlines()
            if l.strip()]
    # append-mode file: last write for a row_uid wins
    dedup = {r.get("row_uid"): r for r in rows}
    rows = list(dedup.values())

    ok_rows = [r for r in rows if (r.get("adj") or {}).get("verdicts") is not None]
    errored = [r for r in rows if (r.get("adj") or {}).get("error_type")]
    contract = [r for r in rows if ((r.get("adj") or {}).get("contract_errors") or [])]

    labeled = [r for r in ok_rows if r.get("assigned_labels")]
    unlabeled = [r for r in ok_rows if not r.get("assigned_labels")]

    verdict_counts = Counter()
    per_label = defaultdict(Counter)
    swaps = Counter()
    none_sugg = Counter()

    for r in ok_rows:
        for v in (r["adj"].get("verdicts") or []):
            if not isinstance(v, dict):
                continue
            verdict_counts[v.get("verdict")] += 1
            per_label[v.get("label")][v.get("verdict")] += 1
            if v.get("verdict") == "wrong_label":
                swaps[f"{v.get('label')} -> {v.get('suggested_label')}"] += 1
        nc = (r["adj"] or {}).get("none_check")
        if isinstance(nc, dict) and nc.get("supported") is False:
            none_sugg[nc.get("suggested_label")] += 1

    L: list[str] = []
    L += ["ADJUDICATION REPORT",
          f"source        : {adj_path.resolve()}",
          f"rows          : {len(rows)}  (labeled {len(labeled)}, unlabeled {len(unlabeled)})",
          f"call errors   : {len(errored)}",
          f"contract errs : {len(contract)}   <- read these rows with suspicion",
          ""]

    total_v = sum(verdict_counts.values())
    L += ["VERDICTS ON ASSIGNED LABELS",
          "---------------------------",
          f"  label instances checked : {total_v}"]
    for k in ("supported", "unsupported", "wrong_label"):
        L.append(f"  {k:<24}: {verdict_counts[k]:>5}  {pct(verdict_counts[k], total_v)}")
    n_dis = sum(1 for r in unlabeled
                if isinstance(r["adj"].get("none_check"), dict)
                and r["adj"]["none_check"].get("supported") is False)
    L += ["",
          "NONE ROWS",
          "---------",
          f"  unlabeled rows checked  : {len(unlabeled)}",
          f"  model says a label applies: {n_dis}  {pct(n_dis, len(unlabeled))}"]

    table("BY SOURCE FILE", bucket(ok_rows, lambda r: r.get("source_file", "?")), L)
    table("BY STRATUM", bucket(ok_rows, lambda r: r.get("stratum", "?")), L)
    table("BY CODEBOOK VERSION AT LABELLING",
          bucket(ok_rows, lambda r: r.get("codebook_version", "?")), L)

    L += ["", "PER LABEL (assigned label -> what the checker said)",
          "---------------------------------------------------",
          f"  {'label':<32} {'n':>5} {'sup':>5} {'unsup':>6} {'wrong':>6} {'contest rate':>13}"]
    for lab in sorted(per_label, key=lambda x: -sum(per_label[x].values())):
        c = per_label[lab]
        n = sum(c.values())
        bad = c["unsupported"] + c["wrong_label"]
        thin = "  (thin)" if n < MIN_SUPPORT else ""
        L.append(f"  {str(lab):<32} {n:>5} {c['supported']:>5} {c['unsupported']:>6} "
                 f"{c['wrong_label']:>6} {pct(bad, n):>13}{thin}")

    if swaps:
        L += ["", "PROPOSED SWAPS (wrong_label)", "----------------------------"]
        for k, v in swaps.most_common():
            L.append(f"  {v:>4}  {k}")
    if none_sugg:
        L += ["", "LABELS PROPOSED ON NONE ROWS", "----------------------------"]
        for k, v in none_sugg.most_common():
            L.append(f"  {v:>4}  {k}")

    dec_path = Path(DECISIONS_FILE)
    if dec_path.exists():
        decs = [json.loads(l) for l in dec_path.read_text(encoding="utf-8").splitlines()
                if l.strip()]
        decided = [d for d in decs if int(d.get("decided", 0))]
        changed = [d for d in decided if int(d.get("changed", 0))]
        contested_dec = [d for d in decided if int(d.get("contested", 0))]
        accepted = [d for d in contested_dec if int(d.get("changed", 0))]
        L += ["", "YOUR RULINGS", "------------",
              f"  decided            : {len(decided)} / {len(decs)}",
              f"  changed            : {len(changed)}  {pct(len(changed), len(decided))}",
              f"  contested rows     : {len(contested_dec)}",
              f"  of those, changed  : {len(accepted)}  {pct(len(accepted), len(contested_dec))}",
              "",
              "  The last line is the number to quote: how often the checker's flag survived",
              "  your judgement. A low rate means the checker is noisy, not that you were right",
              "  by default; read a sample of the rejected flags before concluding either."]
    else:
        L += ["", f"(no {DECISIONS_FILE} yet — rulings section will appear once you export)"]

    Path(OUT_FILE).write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))
    print(f"\nwrote {OUT_FILE}")


if __name__ == "__main__":
    main()