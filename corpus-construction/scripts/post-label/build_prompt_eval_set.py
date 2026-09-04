#!/usr/bin/env python3
"""
build_prompt_eval_set.py -- carve the contamination-free third arm out of the gold set.

Prompt v3 promotes 45 of the 75 adjudicated gold reviews into the prompt as worked
examples. A prompt cannot be scored on reviews it was shown, so the validation set stops
being a usable number for v3 the moment those examples land. This script builds the set
that remains usable: the gold reviews NOT consumed by the prompt.

    gold_set.jsonl (75)  -  prompt_v3_example_ids.json (45)  =  prompt_eval (30)

Two files come out, and they must stay in lockstep:

    prompt_eval_set_blind.jsonl   what the model sees -- gold label columns stripped
    gold_set.jsonl                what it is scored against -- a strict subset of the
                                  adjudicated gold, labels copied verbatim, never re-ruled

The blind file is built by deleting keys from the gold rows rather than by re-deriving
anything, so the two cannot drift: same rows, same order, same review text.

WHAT THIS SET IS AND IS NOT
---------------------------
It is small and it is thin. 30 reviews, 33 label instances, and 13 of the 29 labels have
no support at all -- every label with exactly two gold instances lost both, because both
became its apt and coverage example. Only 5 labels clear the support floor the validation
reports use.

So this is a contamination-free signal on roughly a fifth of the codebook, not a
replacement for the validation number. `runner_common.EVAL_SETS["prompt-eval"]` sets
`meso_macro: False` for exactly this reason: a macro-F1 over 5 labels printed next to one
over 19 invites a comparison that is not there. The report says so in words too.

The exclusion list is DATA, not a constant in this file: `prompt_eval/prompt_v3_example_ids.json`.
Pass --codebook to cross-check it against a built codebook's worked_examples -- the check
that matters is that nothing in the prompt survives into the eval set, and it is worth
re-running whenever the examples change.

Usage
-----
    cd corpus-construction/scripts/post-label
    python build_prompt_eval_set.py                       # build, write the report
    python build_prompt_eval_set.py --check               # verify only, write nothing
    python build_prompt_eval_set.py --codebook ../../../codebook_versions/codebook_adjudicated.json
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

GOLD      = "../../gold_set/gold_set.jsonl"
EXCLUDE   = "../../prompt_eval/prompt_v3_example_ids.json"
OUT_DIR   = "../../prompt_eval"
CODEBOOK  = "../../../codebook_versions/codebook_final.json"

# Columns that carry the answer. Dropped from the blind file, kept in the gold file.
GOLD_ONLY = ["sample_bucket", "from_codebook", "actual_labels", "actual_labels_str"]

CLASS_PREFIX = {"Temporal": "T", "Monetary": "M", "Social": "S",
                "Psychological": "P", "Technical": "Tech"}


def resolve(p: str) -> Path:
    return (HERE / p).resolve()


def jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")


def derive_code(label: dict) -> str:
    words = re.sub(r"[^A-Za-z0-9 ]", " ", label["meso_label"]).split()
    return (CLASS_PREFIX[label["high_level"]] + "_"
            + "".join(w[:1].upper() + w[1:] for w in words))


def label_order(codebook: dict) -> list[str]:
    return [derive_code(l) for l in codebook["labels"]]


# ------------------------------------------------------------------ the build

def build(args) -> int:
    gold_path, excl_path, out_dir = resolve(args.gold), resolve(args.exclude), resolve(args.out_dir)
    gold_rows = jsonl(gold_path)
    manifest = json.loads(excl_path.read_text(encoding="utf-8"))
    excluded = {r["review_id"] for r in manifest["reviews"]}
    order = label_order(json.loads(resolve(args.codebook).read_text(encoding="utf-8")))

    problems: list[str] = []

    # Every excluded id must actually be in the gold set. An id that matches nothing is a
    # typo silently protecting nothing, which is the failure mode worth catching early.
    missing = sorted(excluded - {r["review_id"] for r in gold_rows})
    if missing:
        problems.append(f"{len(missing)} excluded id(s) not present in the gold set: {missing}")

    kept = [r for r in gold_rows if r["review_id"] not in excluded]
    dropped = [r for r in gold_rows if r["review_id"] in excluded]

    if len(kept) + len(dropped) != len(gold_rows):
        problems.append("line accounting does not balance")

    # The property this whole file exists to guarantee.
    leaked = sorted({r["review_id"] for r in kept} & excluded)
    if leaked:
        problems.append(f"CONTAMINATION: {len(leaked)} excluded review(s) survived into the eval set: {leaked}")

    # Optional: cross-check the manifest against a built codebook's worked examples.
    if args.codebook_check:
        cb = json.loads(resolve(args.codebook_check).read_text(encoding="utf-8"))
        in_cb = {we["review_id"] for lab in cb["labels"] for we in lab.get("worked_examples", [])
                 if we.get("review_id")}
        for lab in cb["labels"]:
            for ce in lab.get("counterexamples", []):
                if ce.get("review_id"):
                    in_cb.add(ce["review_id"])
        escaped = sorted(in_cb & {r["review_id"] for r in kept})
        if escaped:
            problems.append(f"CONTAMINATION vs {args.codebook_check}: {len(escaped)} codebook "
                            f"example(s) are in the eval set: {escaped}")
        unlisted = sorted(in_cb & {r["review_id"] for r in gold_rows} - excluded)
        if unlisted:
            problems.append(f"{len(unlisted)} gold review(s) used by the codebook but absent from "
                            f"the manifest: {unlisted}")

    blind = [{k: v for k, v in r.items() if k not in GOLD_ONLY} for r in kept]
    for b, k in zip(blind, kept):
        if any(f in b for f in GOLD_ONLY) or b["review_id"] != k["review_id"]:
            problems.append(f"blind row malformed for {k['review_id']}")

    counts = collections.Counter(l for r in kept for l in r["actual_labels"])
    full = collections.Counter(l for r in gold_rows for l in r["actual_labels"])
    n_none = sum(1 for r in kept if not r["actual_labels"])
    zero = [l for l in order if counts[l] == 0]
    one = [l for l in order if counts[l] == 1]

    print(f"gold {len(gold_rows)}  -  excluded {len(dropped)}  =  eval {len(kept)}")
    print(f"label instances {sum(counts.values())}/{sum(full.values())} | true-NONE {n_none} "
          f"| labels with 0 support {len(zero)} | with 1 {len(one)}")
    if problems:
        print("\nPROBLEMS:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    print("checks passed: no excluded review reaches the eval set")

    if args.check:
        print("--check: nothing written")
        return 0

    write_jsonl(out_dir / "gold_set.jsonl", kept)
    write_jsonl(out_dir / "prompt_eval_set_blind.jsonl", blind)
    (out_dir / "prompt_eval_report.md").write_text(
        report(manifest, gold_rows, kept, dropped, counts, full, order, zero, one, n_none),
        encoding="utf-8")
    print(f"wrote {out_dir}/gold_set.jsonl, prompt_eval_set_blind.jsonl, prompt_eval_report.md")
    return 0


# ----------------------------------------------------------------- the report

def report(manifest, gold_rows, kept, dropped, counts, full, order, zero, one, n_none) -> str:
    L: list[str] = []
    a = L.append
    a("# prompt-eval set")
    a("")
    a(f"Built by `scripts/post-label/build_prompt_eval_set.py` from the adjudicated gold set, "
      f"codebook v{manifest['codebook_version']}, for prompt {manifest['prompt_version']}.")
    a("")
    a("The reviews prompt v3 does **not** contain. Everything here is a strict subset of "
      "`gold_set/gold_set.jsonl`; no label was re-ruled to build it.")
    a("")
    a("| | |")
    a("| --- | ---: |")
    a(f"| gold set | {len(gold_rows)} |")
    a(f"| consumed as v3 worked examples | {len(dropped)} |")
    a(f"| **prompt-eval set** | **{len(kept)}** |")
    a(f"| label instances | {sum(counts.values())} of {sum(full.values())} |")
    a(f"| true-NONE reviews | {n_none} ({100*n_none/len(kept):.0f}% of the set) |")
    a(f"| labels with any support | {sum(1 for l in order if counts[l])} of {len(order)} |")
    a("")
    a("## Read this before quoting a number from it")
    a("")
    a(f"**{len(zero)} of the {len(order)} labels have zero support and cannot be scored at all.** "
      "That is not random attrition: every label with exactly two gold instances lost both, "
      "because both became its apt and coverage example in the prompt.")
    a("")
    a("- zero support: " + ", ".join(f"`{l}`" for l in zero))
    a("- exactly one instance: " + ", ".join(f"`{l}`" for l in one))
    a("")
    a(f"True-NONE is {100*n_none/len(kept):.0f}% of this set against "
      f"{100*sum(1 for r in gold_rows if not r['actual_labels'])/len(gold_rows):.0f}% of the full "
      "gold set, so a model that under-labels is flattered here more than it would be there.")
    a("")
    a("`runner_common.EVAL_SETS[\"prompt-eval\"]` therefore sets `meso_macro: False`. Meso "
      "macro-F1 is **suppressed** on this arm rather than computed over the handful of labels "
      "that clear the support floor, because such a number reads as comparable to the "
      "validation figure and is not. Use micro-F1 and example-based F1.")
    a("")
    a("## Files")
    a("")
    a("| file | role |")
    a("| --- | --- |")
    a("| `prompt_eval_set_blind.jsonl` | given to the model; gold label columns stripped |")
    a("| `gold_set.jsonl` | scored against; labels copied verbatim from the adjudicated gold |")
    a("| `prompt_v3_example_ids.json` | the exclusion list, and why each id is on it |")
    a("")
    a("Run it: `python run_teacher_openai.py --actual --eval-set prompt-eval --prompt ...`, "
      "then `python compute_run_stats.py --eval-set prompt-eval`. Output lands under "
      "`outputs/prompt-eval/`.")
    a("")
    a("## Label support")
    a("")
    a("| label | full gold | prompt-eval |")
    a("| --- | ---: | ---: |")
    for l in order:
        mark = " ⚠️" if counts[l] == 0 else ""
        a(f"| `{l}` | {full[l]} | {counts[l]}{mark} |")
    a("")
    a("## Composition")
    a("")
    for field in ("stratum", "market", "star_rating"):
        c = collections.Counter(r[field] for r in kept)
        a(f"- **{field}**: " + ", ".join(f"{k} {v}" for k, v in sorted(c.items(), key=lambda kv: str(kv[0]))))
    games = collections.Counter(r["game_name"] for r in kept)
    a(f"- **distinct games**: {len(games)} (most from one game: {games.most_common(1)[0][1]})")
    a(f"- **labels per review**: mean {sum(counts.values())/len(kept):.2f}")
    a("")
    a("## Reviews")
    a("")
    a("| review_id | game | gold labels |")
    a("| --- | --- | --- |")
    for r in kept:
        labs = ", ".join(f"`{x}`" for x in r["actual_labels"]) or "_NONE_"
        a(f"| `{r['review_id']}` | {r['game_name']} | {labs} |")
    a("")
    return "\n".join(L) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Build the prompt-eval set: the gold reviews prompt v3 does not contain.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--gold", default=GOLD, help="adjudicated gold set to carve from")
    ap.add_argument("--exclude", default=EXCLUDE, help="manifest of reviews used in the prompt")
    ap.add_argument("--out-dir", default=OUT_DIR, help="where the eval set is written")
    ap.add_argument("--codebook", default=CODEBOOK, help="codebook defining the label order")
    ap.add_argument("--codebook-check", default=None,
                    help="also assert no worked example or counterexample in this codebook "
                         "survives into the eval set")
    ap.add_argument("--check", action="store_true", help="verify only, write nothing")
    sys.exit(build(ap.parse_args()))


if __name__ == "__main__":
    main()
