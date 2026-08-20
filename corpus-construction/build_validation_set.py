#!/usr/bin/env python3
"""
build_validation_set.py — sample a coder-training / validation set from pilot-coded
dark-pattern review files.

Usage
-----
    python3 build_validation_set.py \
        --inputs random.jsonl targetted.jsonl targetted_2.jsonl \
        --codebook codebook_v0_16.json \
        --out validation_set.jsonl \
        --report validation_set_report.md \
        --seed 20260812

Sampling rules implemented
--------------------------
  * every meso label >= --per-label-min (default 2) where pilot support allows
  * --none-min .. --none-max true-None reviews (default 8-10)
  * --combo-min .. --combo-max multi-label combo reviews (default 4-5)
  * EXCLUDE any review used as a worked example or counterexample in the codebook
    (matched by review_id AND by normalised review text, since several codebook
    examples carry no usable id -- 'targetted', 'seed: contacts', '', etc.)
  * cross-file duplicates are dropped entirely (id or normalised-text collision)

Output record shape: metadata + review + actual_labels + empty assigned_labels.
Deterministic given --seed.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

# --------------------------------------------------------------------------- #
# label plumbing
# --------------------------------------------------------------------------- #

CLASS_PREFIX = {
    "Temporal": "T",
    "Monetary": "M",
    "Social": "S",
    "Psychological": "P",
    "Technical": "Tech",
}


def label_key(high_level: str, meso_label: str) -> str:
    """'Social' + 'Fear of Missing Out (FOMO)' -> 'S_FearOfMissingOutFOMO'."""
    prefix = CLASS_PREFIX[high_level]
    words = re.split(r"[^0-9A-Za-z]+", meso_label)
    camel = "".join(w[:1].upper() + w[1:] for w in words if w)
    return f"{prefix}_{camel}"


def load_codebook(path: Path):
    """Return (ordered label keys, key->meso name, example index).

    The example index lets us both EXCLUDE codebook examples from the main pool
    and hold them in reserve, so a label with too little pilot support can be
    backfilled with at most one of its own worked examples.
    """
    cb = json.loads(path.read_text(encoding="utf-8"))

    keys, pretty = [], {}
    for lab in cb["labels"]:
        k = label_key(lab["high_level"], lab["meso_label"])
        keys.append(k)
        pretty[k] = f"{lab['high_level']}: {lab['meso_label']}"

    examples: list[dict] = []

    def note(rid, text, kind, labels, owner):
        rid = (rid or "").strip()
        full, prefix = text_fingerprints(text or "")
        if not rid and not full:
            return
        examples.append({
            "id": rid.lower() if re.fullmatch(r"[0-9a-fA-F-]{32,40}", rid) else "",
            "raw_id": rid,
            "text": text or "",
            "full": full,
            "prefix": prefix,
            "kind": kind,                 # worked | counter | rule
            "labels": [l for l in (labels or []) if l in keys],
            "owner": owner,               # meso label the example sits under
        })

    for lab in cb["labels"]:
        owner = label_key(lab["high_level"], lab["meso_label"])
        for ex in lab.get("worked_examples") or []:
            note(ex.get("review_id"), ex.get("text"), "worked",
                 ex.get("labels_assigned"), owner)
        for ex in lab.get("counterexamples") or []:
            note(ex.get("review_id"), ex.get("text"), "counter", [], owner)
    for rule in cb.get("global_rules", []):
        note(rule.get("worked_example_review_id"), rule.get("worked_example_text"),
             "rule", [], rule.get("id", ""))

    return keys, pretty, examples


def match_example(rid: str, text: str, examples: list[dict]):
    """Is this row one of the codebook's examples? Returns the example or None."""
    rid = (rid or "").strip().lower()
    full, prefix = text_fingerprints(text)
    for ex in examples:
        if ex["id"] and rid and ex["id"] == rid:
            return ex
        if full and ex["full"] and (full == ex["full"]):
            return ex
        if prefix and ex["prefix"] and (
            prefix.startswith(ex["prefix"]) or ex["prefix"].startswith(prefix)
        ):
            return ex
    return None


def clean_example_text(s: str) -> str:
    """Codebook example texts sometimes wrap the review in 'Review: ... Labels: ...'."""
    if not s:
        return ""
    s = re.sub(r"^\s*review\s*:\s*", "", s, flags=re.I)
    s = re.split(r"\n\s*labels?\s*:", s, flags=re.I)[0]
    return s.strip()


def norm_text(s: str) -> str:
    """Aggressive normalisation for text-based example matching."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKC", s)
    s = s.lower()
    # codebook example texts sometimes carry a trailing 'Labels: ...' annotation
    s = re.split(r"\blabels?\s*:", s)[0]
    s = re.sub(r"[^0-9a-z]+", " ", s)
    return " ".join(s.split())


def text_fingerprints(s: str) -> tuple[str, str]:
    """(full normalised text, first 200 chars of it) — the prefix catches truncation."""
    n = norm_text(s)
    return n, n[:200]


# --------------------------------------------------------------------------- #
# loading
# --------------------------------------------------------------------------- #

META_FIELDS = [
    "review_id", "app_id", "game_name", "market", "review_date",
    "star_rating", "review_text", "stratum", "seed_keyword", "casino",
]


def labels_of(rec: dict, keys: list[str]) -> list[str]:
    """Prefer the explicit labels array; fall back to the binary columns."""
    from_cols = [k for k in keys if str(rec.get(k, 0)) in ("1", "1.0", "True", "true")]
    arr = rec.get("labels")
    if isinstance(arr, list):
        arr = [a for a in arr if a in keys]
        return sorted(set(arr), key=keys.index), sorted(set(from_cols), key=keys.index)
    return sorted(set(from_cols), key=keys.index), sorted(set(from_cols), key=keys.index)


def is_none_coded(rec: dict, labs: list[str]) -> bool:
    return not labs and str(rec.get("none", 0)) in ("1", "1.0", "True", "true")


def is_coded(rec: dict, labs: list[str]) -> bool:
    """A row counts as coded if it has labels, an explicit none=1, or was saved."""
    if labs:
        return True
    if is_none_coded(rec, labs):
        return True
    return str(rec.get("saved", 0)) in ("1", "1.0", "True", "true")


def load_inputs(paths, keys, examples, include_uncoded, log):
    """Load every file, hold codebook examples in reserve, drop cross-file duplicates."""
    by_id: dict[str, dict] = {}
    reserve: dict[str, dict] = {}           # codebook examples found in the data
    dup_ids, dup_texts = set(), set()
    seen_text: dict[str, str] = {}          # fingerprint -> review_id
    stats = Counter()

    for path in paths:
        src = Path(path).name
        with open(path, encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, 1):
                line = line.strip()
                if not line:
                    continue
                stats["lines"] += 1
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError as exc:
                    log.append(f"- bad JSON at {src}:{lineno} ({exc}); skipped")
                    stats["bad_json"] += 1
                    continue

                rid = str(rec.get("review_id", "")).strip()
                if not rid:
                    stats["no_id"] += 1
                    continue

                labs, col_labs = labels_of(rec, keys)
                if labs != col_labs:
                    log.append(
                        f"- {rid}: `labels` array and binary columns disagree "
                        f"(array={labs}, cols={col_labs}); used the array"
                    )
                    stats["label_mismatch"] += 1

                entry = {
                    "rec": rec,
                    "labels": labs,
                    "source_file": src,
                    "none": is_none_coded(rec, labs),
                    "from_codebook": False,
                }

                ex = match_example(rid, rec.get("review_text", ""), examples)
                if ex is not None:
                    stats["codebook_example"] += 1
                    ex["matched"] = True
                    # worked examples are held in reserve for the backfill stage;
                    # counterexamples and rule examples are simply out
                    if ex["kind"] == "worked" and rid not in reserve:
                        cb_labs = ex["labels"] or [ex["owner"]]
                        if labs and sorted(labs) != sorted(cb_labs):
                            log.append(
                                f"- codebook example {rid}: data labels {labs} differ from "
                                f"codebook labels_assigned {cb_labs}; kept the data labels"
                            )
                        entry["labels"] = labs or cb_labs
                        entry["from_codebook"] = True
                        reserve[rid] = entry
                    continue

                if not include_uncoded and not is_coded(rec, labs):
                    stats["uncoded"] += 1
                    continue

                full, _ = text_fingerprints(rec.get("review_text", ""))
                if rid in by_id:
                    dup_ids.add(rid)
                    stats["dup_id"] += 1
                    continue
                if full and full in seen_text:
                    dup_texts.add(rid)
                    dup_texts.add(seen_text[full])
                    stats["dup_text"] += 1
                    continue

                seen_text[full] = rid
                by_id[rid] = entry

    # a review seen in more than one file is dropped entirely, not kept once
    for rid in dup_ids | dup_texts:
        by_id.pop(rid, None)
    if dup_ids or dup_texts:
        log.append(
            f"- dropped {len(dup_ids | dup_texts)} review(s) appearing in more than "
            f"one file (id collisions: {len(dup_ids)}, text collisions: {len(dup_texts)})"
        )

    # worked examples that never turned up in the data (their codebook review_id
    # is a placeholder like 'targetted' and the text didn't match) are rebuilt
    # from the codebook itself, with metadata left blank
    for i, ex in enumerate(examples):
        if ex["kind"] != "worked" or ex.get("matched") or not ex["text"]:
            continue
        rid = ex["raw_id"] if ex["id"] else f"cb-{ex['owner']}-{i}"
        reserve[rid] = {
            "rec": {"review_id": rid, "review_text": clean_example_text(ex["text"]),
                    "stratum": "codebook", "seed_keyword": ex["raw_id"]},
            "labels": ex["labels"] or [ex["owner"]],
            "source_file": "codebook",
            "none": False,
            "from_codebook": True,
        }
        stats["codebook_synthesised"] += 1

    return list(by_id.values()), list(reserve.values()), stats


# --------------------------------------------------------------------------- #
# sampling
# --------------------------------------------------------------------------- #

def sample(pool, reserve, keys, args, rng, log):
    none_pool = [r for r in pool if r["none"]]
    single_pool = [r for r in pool if len(r["labels"]) == 1]
    multi_pool = [r for r in pool if len(r["labels"]) >= 2]

    support = Counter()
    for r in pool:
        for k in r["labels"]:
            support[k] += 1

    chosen: dict[str, dict] = {}
    bucket: dict[str, str] = {}
    per_game = Counter()
    counts = Counter()

    def key_of(r):
        return r["rec"]["review_id"]

    def take(r, why):
        rid = key_of(r)
        if rid in chosen:
            return False
        chosen[rid] = r
        bucket[rid] = why
        per_game[r["rec"].get("app_id", "")] += 1
        for k in r["labels"]:
            counts[k] += 1
        return True

    def deficit():
        return {k for k in keys if counts[k] < min(args.per_label_min, support[k])}

    def score(r, want):
        """Higher is better: covers more deficient labels, few extras, unseen game."""
        gain = len(set(r["labels"]) & want)
        extra = len(r["labels"]) - gain
        game_pen = 2 if per_game[r["rec"].get("app_id", "")] >= args.max_per_game else 0
        return (gain, -extra, -game_pen, -per_game[r["rec"].get("app_id", "")])

    def pick(cands, want, n, why):
        """Greedy, deterministic: best score, ties broken by seeded shuffle order."""
        taken = 0
        cands = sorted(cands, key=key_of)
        rng.shuffle(cands)
        while taken < n:
            avail = [r for r in cands if key_of(r) not in chosen]
            if not avail:
                break
            best = max(avail, key=lambda r: score(r, want))
            if want and not (set(best["labels"]) & want) and why.startswith("rare"):
                break
            take(best, why)
            taken += 1
            want = deficit()
        return taken

    # 1. true-None reviews
    n_none = (args.none_min + args.none_max) // 2
    got = pick(none_pool, set(), n_none, "none")
    if got < args.none_min:
        log.append(f"- only {got} true-None reviews available (wanted {args.none_min}-{args.none_max})")

    # 2. multi-label combos, chosen to cover the rarest labels
    combo_cands = [r for r in multi_pool if len(r["labels"]) <= args.max_combo_labels] or multi_pool
    n_combo = (args.combo_min + args.combo_max + 1) // 2
    got = pick(combo_cands, deficit(), n_combo, "combo")
    if got < args.combo_min:
        log.append(f"- only {got} multi-label reviews available (wanted {args.combo_min}-{args.combo_max})")

    # 3. per-label floor, rarest labels first
    for k in sorted(keys, key=lambda k: (support[k], k)):
        need = min(args.per_label_min, support[k]) - counts[k]
        if need <= 0:
            continue
        singles = [r for r in single_pool if k in r["labels"]]
        pick(singles, {k}, need, f"rare:{k}")
        need = min(args.per_label_min, support[k]) - counts[k]
        if need > 0:
            multis = [r for r in multi_pool if k in r["labels"]]
            got = pick(multis, {k}, need, f"rare-multi:{k}")
            if got:
                log.append(f"- {k}: needed multi-label reviews to reach the floor "
                           f"(+{got} beyond the combo quota)")

    # 3b. backfill from the codebook's own worked examples where the pilot data
    #     simply doesn't have enough: at most --max-codebook-per-label each.
    if args.max_codebook_per_label > 0:
        used_cb = 0
        for k in sorted(keys, key=lambda k: (support[k], k)):
            need = args.per_label_min - counts[k]
            if need <= 0:
                continue
            cands = sorted([r for r in reserve if k in r["labels"]], key=key_of)
            rng.shuffle(cands)
            got = 0
            for r in cands:
                if got >= min(need, args.max_codebook_per_label):
                    break
                if take(r, f"codebook-backfill:{k}"):
                    got += 1
                    used_cb += 1
            if got:
                log.append(f"- {k}: pilot support {support[k]} < floor; backfilled "
                           f"{got} codebook worked example(s)")
        if used_cb:
            log.append(f"- {used_cb} review(s) came from the codebook and are marked "
                       f"`from_codebook: true` — coders have already seen these")

    # 4. top up toward --total, spreading across games / markets / ratings
    if len(chosen) < args.total:
        n_multi = sum(1 for r in chosen.values() if len(r["labels"]) >= 2)
        rest = [r for r in pool if key_of(r) not in chosen and not r["none"]]
        rest = sorted(rest, key=key_of)
        rng.shuffle(rest)
        # single-label first: the combo quota is a ceiling, not a floor
        rest.sort(key=lambda r: (len(r["labels"]) >= 2,
                                 per_game[r["rec"].get("app_id", "")],
                                 sum(counts[k] for k in r["labels"]) / max(1, len(r["labels"]))))
        for r in rest:
            if len(chosen) >= args.total:
                break
            if len(r["labels"]) >= 2 and n_multi >= args.combo_max:
                continue
            if take(r, "fill") and len(r["labels"]) >= 2:
                n_multi += 1

    short = [k for k in keys if counts[k] < args.per_label_min]
    for k in short:
        log.append(f"- {k}: pilot support = {support[k]}, in sample = {counts[k]} "
                   f"(still below the floor of {args.per_label_min}, codebook included)")

    return chosen, bucket, counts, support


# --------------------------------------------------------------------------- #
# output
# --------------------------------------------------------------------------- #

def to_record(r, why, codebook_version):
    rec = r["rec"]
    out = {f: rec.get(f, "") for f in META_FIELDS}
    out["source_file"] = r["source_file"]
    out["codebook_version"] = codebook_version
    out["sample_bucket"] = why
    out["from_codebook"] = bool(r.get("from_codebook"))
    out["actual_labels"] = r["labels"]
    out["actual_labels_str"] = "; ".join(r["labels"])
    out["assigned_labels"] = []
    out["assigned_spans"] = []
    out["coder_id"] = ""
    out["coder_notes"] = ""
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inputs", nargs="+", required=True,
                    help="random.jsonl targetted.jsonl targetted_2.jsonl")
    ap.add_argument("--codebook", required=True)
    ap.add_argument("--out", default="validation_set.jsonl")
    ap.add_argument("--blind-out", default=None,
                    help="optional second file with actual_labels stripped, for coders")
    ap.add_argument("--report", default=None, help="write a markdown coverage report here")
    ap.add_argument("--seed", type=int, default=20260812)
    ap.add_argument("--total", type=int, default=75)
    ap.add_argument("--per-label-min", type=int, default=2)
    ap.add_argument("--none-min", type=int, default=8)
    ap.add_argument("--none-max", type=int, default=10)
    ap.add_argument("--combo-min", type=int, default=4)
    ap.add_argument("--combo-max", type=int, default=5)
    ap.add_argument("--max-combo-labels", type=int, default=3,
                    help="prefer combos with at most this many labels")
    ap.add_argument("--max-per-game", type=int, default=4,
                    help="soft cap on reviews from one app_id")
    ap.add_argument("--max-codebook-per-label", type=int, default=1,
                    help="when pilot support is short of the floor, top a label up with "
                         "this many of its codebook worked examples (0 disables)")
    ap.add_argument("--include-uncoded", action="store_true",
                    help="keep rows with no labels, no none=1 and saved!=1")
    args = ap.parse_args()

    log: list[str] = []
    cb_path = Path(args.codebook)
    keys, pretty, examples = load_codebook(cb_path)
    codebook_version = json.loads(cb_path.read_text(encoding="utf-8")).get("version", "")

    pool, reserve, stats = load_inputs(args.inputs, keys, examples, args.include_uncoded, log)
    if not pool:
        print("No eligible reviews after filtering.", file=sys.stderr)
        return 1

    rng = random.Random(args.seed)
    chosen, bucket, counts, support = sample(pool, reserve, keys, args, rng, log)

    ordered = sorted(chosen.values(), key=lambda r: r["rec"]["review_id"])
    rng.shuffle(ordered)

    with open(args.out, "w", encoding="utf-8") as fh:
        for r in ordered:
            fh.write(json.dumps(to_record(r, bucket[r["rec"]["review_id"]], codebook_version),
                                ensure_ascii=False) + "\n")

    if args.blind_out:
        with open(args.blind_out, "w", encoding="utf-8") as fh:
            for r in ordered:
                rec = to_record(r, bucket[r["rec"]["review_id"]], codebook_version)
                for k in ("actual_labels", "actual_labels_str", "sample_bucket",
                          "from_codebook"):
                    rec.pop(k, None)
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # ---- report -----------------------------------------------------------
    n_none = sum(1 for r in ordered if r["none"])
    n_multi = sum(1 for r in ordered if len(r["labels"]) >= 2)
    n_cb = sum(1 for r in ordered if r.get("from_codebook"))
    lines = [
        f"# validation set — codebook v{codebook_version}",
        "",
        f"- seed: `{args.seed}`  |  inputs: {', '.join(Path(p).name for p in args.inputs)}",
        f"- eligible pool: **{len(pool)}**  |  sampled: **{len(ordered)}** (target {args.total})",
        f"- true-None: **{n_none}** (want {args.none_min}-{args.none_max})",
        f"- multi-label: **{n_multi}** (want {args.combo_min}-{args.combo_max})",
        f"- from codebook (backfill): **{n_cb}**"
        + ("  <- over the combo ceiling; coverage took priority"
           if n_multi > args.combo_max else ""),
        "",
        "## filtering",
        f"- lines read: {stats['lines']}",
        f"- codebook examples held out of the pool: {stats['codebook_example']}",
        f"- codebook worked examples rebuilt from the codebook text: "
        f"{stats['codebook_synthesised']}",
        f"- dropped, uncoded: {stats['uncoded']}",
        f"- dropped, duplicate id / text: {stats['dup_id']} / {stats['dup_text']}",
        "",
        "## label coverage",
        "",
        "| label | pilot support | in sample | floor met |",
        "| --- | ---: | ---: | :---: |",
    ]
    for k in keys:
        ok = "yes" if counts[k] >= min(args.per_label_min, support[k]) else "NO"
        lines.append(f"| {pretty[k]} | {support[k]} | {counts[k]} | {ok} |")
    if log:
        lines += ["", "## notes", ""] + log

    report = "\n".join(lines)
    print(report)
    if args.report:
        Path(args.report).write_text(report + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())