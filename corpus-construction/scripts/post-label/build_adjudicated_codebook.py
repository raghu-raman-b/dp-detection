#!/usr/bin/env python3
"""
build_adjudicated_codebook.py -- codebook_final (v0.20) + adjudicated examples -> v0.21.

The only thing this changes is `worked_examples`. Every definition, indicator, boundary
rule, counterexample and global rule is copied through byte for byte: v0.21 and v0.20 have
the same label vocabulary and the same coding instructions, which is why the other scripts
that read the codebook for its vocabulary (compute_run_stats, build_final_dataset,
compute_agreement, the set builders) can stay pointed at codebook_final.json.

WHAT REPLACES WHAT
------------------
v0.20 carried 40 worked examples, unevenly spread: some labels had two, some had one, some
had none, and each was a review plus its label set. v0.21 carries 58 -- exactly two per
meso label, all 29 covered -- and each one is written in the shape the teacher model must
emit: the span that triggered the label, the codebook material the label rests on, and a
one-line rationale. The prompt can then show a model the reasoning it is being asked to
reproduce, instead of only the answer.

The examples come from the adjudicated gold set. That is a deliberate trade with a cost:
those 45 reviews can no longer score a prompt that quotes them, which is why
`corpus-construction/prompt_eval/` exists. See prompt_v3_examples.md.

THE ONE RETAINED v0.20 EXAMPLE
------------------------------
`build_prompt.py` pins two global exemplars and pulls their review text out of the codebook
by review_id at build time, so the text can never drift from its source. The positive one,
9d76ef06, lives in Deceptive Luxury's worked_examples and nowhere else. Dropping it would
make find_review() exit and take the build with it.

So Deceptive Luxury keeps three entries: 9d76ef06 first, then its apt and coverage examples.
The retained entry is never rendered into the prompt -- render_label() skips anything whose
review_id is in `used_ids`, and both pinned exemplars are in that set -- so it costs nothing
in the prompt and every label still shows exactly two. It is a lookup source, not an example.
`retained_for` on the entry says so, and `--check` asserts it is still there.

Usage
-----
    cd corpus-construction/scripts/post-label
    python build_adjudicated_codebook.py            # validate and write
    python build_adjudicated_codebook.py --check    # validate only, write nothing
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

SRC       = "../../../codebook_versions/codebook_final.json"
EXAMPLES  = "../../../codebook_versions/adjudicated_examples.json"
GOLD      = "../../gold_set/gold_set.jsonl"
OUT       = "../../../codebook_versions/codebook_adjudicated.json"

NEW_VERSION = "0.21"
NEW_DATE    = "2026-09-04"

# Pinned in build_prompt.py. Their review text is looked up in the codebook by id, so the
# slot holding each one has to survive this rebuild.
PINNED = {
    "9d76ef06-a218-4ef4-b835-75443f4ec987": "positive global exemplar in build_prompt.py",
    "331c695a-8b57-4a46-b4d2-00fcdff9ec1a": "NONE global exemplar in build_prompt.py",
}

CLASS_PREFIX = {"Temporal": "T", "Monetary": "M", "Social": "S",
                "Psychological": "P", "Technical": "Tech"}


def resolve(p: str) -> Path:
    return (HERE / p).resolve()


def derive_code(label: dict) -> str:
    words = re.sub(r"[^A-Za-z0-9 ]", " ", label["meso_label"]).split()
    return (CLASS_PREFIX[label["high_level"]] + "_"
            + "".join(w[:1].upper() + w[1:] for w in words))


def build(args) -> int:
    cb = json.loads(resolve(args.src).read_text(encoding="utf-8"))
    ex = json.loads(resolve(args.examples).read_text(encoding="utf-8"))
    gold = {json.loads(l)["review_id"]: json.loads(l)
            for l in resolve(args.gold).read_text(encoding="utf-8").splitlines() if l.strip()}

    by_code = {derive_code(l): l for l in cb["labels"]}
    legal = set(by_code)
    problems: list[str] = []

    # ---------------------------------------------------------------- validate
    per_label: dict[str, list[dict]] = collections.defaultdict(list)
    for e in ex["examples"]:
        lab, rid, span = e["anchor_label"], e["review_id"], e["span"]
        where = f"{lab}/{e['role']}"

        if lab not in legal:
            problems.append(f"{where}: unknown label")
            continue
        if rid not in gold:
            problems.append(f"{where}: review {rid} is not in the gold set")
            continue

        row = gold[rid]
        if lab not in row["actual_labels"]:
            problems.append(f"{where}: gold does not carry this label for {rid} "
                            f"(has {row['actual_labels']})")
        # R3: the span has to be quotable from the review, character for character.
        if span not in row["review_text"]:
            problems.append(f"{where}: span is not a verbatim substring of the review text")
        if not e.get("rationale", "").strip():
            problems.append(f"{where}: empty rationale")

        # rule_applied must name material that exists ON THIS LABEL. A boundary rule is
        # written from one side, so citing one that lives on the other label is a real
        # error and not a stylistic one -- it points the model at text it cannot find.
        rule = e.get("rule_applied", "").strip()
        if not rule:
            problems.append(f"{where}: empty rule_applied")
        elif rule != "definition":
            L = by_code[lab]
            if rule.startswith("vs "):
                owned = [b["vs_label"] for b in L.get("boundary_rules", [])]
                if rule[3:] not in owned:
                    problems.append(f"{where}: boundary rule {rule!r} is not listed under this "
                                    f"label (it has: {owned})")
            else:
                inds = " || ".join(str(i) for i in L.get("indicators", [])).lower()
                for part in [p.strip() for p in rule.split("+")]:
                    if part.lower() not in inds:
                        problems.append(f"{where}: indicator {part!r} is not in this label's "
                                        f"indicators list")

        bad = [c for c in row["actual_labels"] if c not in legal]
        if bad:
            problems.append(f"{where}: gold row carries unknown codes {bad}")
        per_label[lab].append(e)

    for code in by_code:
        n = len(per_label[code])
        if n != 2:
            problems.append(f"{code}: {n} example(s), expected exactly 2 (apt + coverage)")
        roles = sorted(e["role"] for e in per_label[code])
        if n == 2 and roles != ["apt", "coverage"]:
            problems.append(f"{code}: roles are {roles}, expected ['apt', 'coverage']")

    # ------------------------------------------------------------------- build
    for code, L in by_code.items():
        retained = [we for we in L.get("worked_examples", [])
                    if we.get("review_id") in PINNED]
        for we in retained:
            we["retained_for"] = PINNED[we["review_id"]]
            we["rendered_in_prompt"] = False

        fresh = []
        for e in sorted(per_label[code], key=lambda x: (x["role"] != "apt",)):
            row = gold[e["review_id"]]
            entry = {
                "review_id": e["review_id"],
                "text": row["review_text"],
                "labels_assigned": list(row["actual_labels"]),
                "anchor_label": code,
                "role": e["role"],
                "span": e["span"],
                "rule_applied": e["rule_applied"],
                "rationale": e["rationale"],
                "source": "adjudicated gold set, 2026-09-04",
                "game_name": row["game_name"],
            }
            for k in ("invoked_web_search", "search_query", "search_result"):
                if k in e:
                    entry[k] = e[k]
            fresh.append(entry)
        L["worked_examples"] = retained + fresh

    for rid, why in PINNED.items():
        found = any(we.get("review_id") == rid
                    for L in cb["labels"] for we in L.get("worked_examples", [])) or \
                any(ce.get("review_id") == rid
                    for L in cb["labels"] for ce in L.get("counterexamples", [])) or \
                any(r.get("worked_example_review_id") == rid for r in cb["global_rules"])
        if not found:
            problems.append(f"pinned exemplar {rid} ({why}) is no longer reachable in the "
                            f"codebook; build_prompt.find_review() would exit")

    cb["version"] = NEW_VERSION
    cb["changelog"].append({
        "version": NEW_VERSION,
        "date": NEW_DATE,
        "change": (
            "Replaced worked_examples with 58 adjudicated examples, two per meso label across "
            "all 29 labels (v0.20 had 40, unevenly spread). Each carries the span that triggered "
            "the label, the rule_applied it rests on, and a one-line rationale, so the prompt can "
            "show the reasoning and not only the answer. Drawn from the adjudicated gold set of "
            "2026-09-04; the 45 reviews consumed are listed in "
            "corpus-construction/prompt_eval/prompt_v3_example_ids.json and are excluded from the "
            "prompt-eval arm. Deceptive Luxury retains its v0.20 example 9d76ef06 as the lookup "
            "source for build_prompt.py's pinned positive exemplar; it is not rendered. No "
            "definition, indicator, boundary rule, counterexample or global rule changed, so the "
            "label vocabulary is identical to v0.20."),
        "invalidates_prior_coding": False,
        "rows_rechecked": "",
    })

    n_we = sum(len(L.get("worked_examples", [])) for L in cb["labels"])
    n_rendered = sum(1 for L in cb["labels"] for we in L["worked_examples"]
                     if we.get("review_id") not in PINNED)
    print(f"labels {len(cb['labels'])} | worked_examples {n_we} "
          f"({n_rendered} renderable + {n_we - n_rendered} retained lookup source)")
    print(f"reviews consumed: {len({e['review_id'] for e in ex['examples']})}")

    if problems:
        print(f"\n{len(problems)} PROBLEM(S):", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    print("all checks passed: spans verbatim, rules owned by their label, 2 per label, "
          "pinned exemplars reachable")

    if args.check:
        print("--check: nothing written")
        return 0

    out = resolve(args.out)
    out.write_text(json.dumps(cb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out}  (v{NEW_VERSION})")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Build codebook v0.21 from v0.20 plus the adjudicated worked examples.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--src", default=SRC)
    ap.add_argument("--examples", default=EXAMPLES)
    ap.add_argument("--gold", default=GOLD)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--check", action="store_true", help="validate only, write nothing")
    sys.exit(build(ap.parse_args()))


if __name__ == "__main__":
    main()
