#!/usr/bin/env python3
"""
build_prompt.py  --  v2  (PROMPT_VERSION p2)

Deterministically renders the teacher prompt from the dark-patterns codebook JSON.

Design rules (do not relax without a reason you would write in the paper):
  1. The codebook is the single source of truth. Every rule, definition, indicator,
     boundary rule, counterexample and worked example in the prompt is copied verbatim
     from the JSON. Nothing is paraphrased, summarised, or invented at build time.
  2. The two global exemplars are the one exception. They are pinned near the top of
     this file, in plain sight. The build validates them against the
     codebook: every span must be a verbatim substring of the codebook's own review
     text, and the label set must match that review's labels_assigned.
  3. The build is a pure function of (codebook, exemplars, mode). Same inputs ->
     byte-identical prompt body -> same SHA -> same provider cache entry.
  4. The build log (timestamp, sizes, SHA) is written ABOVE the sentinel line and is NOT
     part of the prompt. Anything below the sentinel is the prompt, exactly.

     >>> Never send the header to a model. Use load_prompt() or --emit-prompt-only. <<<
     A timestamp inside the cached prefix means a cache miss on every single call.

One invocation writes all three modes, each with its own manifest and SHA:
    python build_prompt.py
    python build_prompt.py --mode full          # just one
    python build_prompt.py --mode full --out -  # prompt body to stdout
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import re
import sys
from pathlib import Path

# ------------------------------------------------------------------------- config

CODEBOOK = "../../codebook_versions/codebook_final.json"
OUT_DIR = "../outputs/prompts"
OUT_STEM = "teacher"

PROMPT_VERSION = "v2"

# The ablation. Each mode is the one above it plus one more kind of codebook material,
# so a score difference is attributable to exactly one addition.
MODES: dict[str, dict[str, bool]] = {
    "bare":     {"indicators": True, "boundary_rules": False,
                 "counterexamples": False, "worked_examples": False,
                 "rule_examples": False},
    "boundary": {"indicators": True, "boundary_rules": True,
                 "counterexamples": True,  "worked_examples": False,
                 "rule_examples": False},
    "full":     {"indicators": True, "boundary_rules": True,
                 "counterexamples": True,  "worked_examples": True,
                 "rule_examples": True},
}

# Everything after this line in the output file is the prompt. Nothing before it is.
SENTINEL = "=============================== PROMPT BODY ==============================="

# Class name -> code prefix. Verified against the codes used in the codebook's own
# worked_examples[].labels_assigned; the build asserts the derived set matches.
FROM_CODEBOOK_WHY_NOT = object()

CLASS_PREFIX = {
    "Temporal": "T",
    "Monetary": "M",
    "Social": "S",
    "Psychological": "P",
    "Technical": "Tech",
}


# ------------------------------------------------------------------------- exemplars
# The two global exemplars. This is the ONLY text in the prompt not lifted from the
# codebook, which is why it sits here in plain sight rather than in a data file.
#
# The review text is NOT stored here. It is pulled from the codebook by review_id at
# build time so it can never drift. Everything below is the expected OUTPUT.
#
# The build validates all of it against the codebook before rendering: every span must
# be a verbatim substring of the codebook's review text, the label set must match that
# review's labels_assigned exactly, no label may repeat, and the search fields must
# agree with each other. Edit here, rebuild, and the checks will catch a bad edit.

NONE_EXEMPLAR = {
    "review_id": "331c695a-8b57-4a46-b4d2-00fcdff9ec1a",
    # Rendered verbatim from this review's counterexample why_not in the codebook.
    "analysis": FROM_CODEBOOK_WHY_NOT,
    "labels": [],
    "invoked_web_search": False,
    "search_query": None,
    "search_result": None,
}

POSITIVE_EXEMPLAR = {
    "review_id": "9d76ef06-a218-4ef4-b835-75443f4ec987",
    "analysis": (
        "The reviewer is describing sticker album completion in a collection game. "
        "Three things are being described at once. Progress through the albums is gated "
        "behind real money: finishing is stated to be impossible without paying. The "
        "albums themselves are a set the player is working to complete, and the reviewer "
        "frames not finishing as the harm. And the golds are made scarce by the "
        "developer, with a purchasable item, the wilds, offered as the way to obtain "
        "them anyway. I do not know from the review alone what golds and wilds are as "
        "game items, so that needs resolving before the third reading can be checked."
    ),
    "labels": [
        {
            "label": "M_PayToProgress",
            "span": "unless you pay real money you dont get to finish alot of the albums",
            "rule_applied": "definition",
            "rationale": (
                "Progress through the albums is available on payment and stated to be "
                "unavailable without it."
            ),
        },
        {
            "label": "P_CompleteTheCollection",
            "span": "they make it almost impossible to get all the golds",
            "rule_applied": "definition",
            "rationale": (
                "The player is working toward a complete set and the review frames the "
                "missing pieces as what keeps them playing and paying."
            ),
        },
        {
            "label": "M_DeceptiveLuxury",
            "span": "they make sure you cant get them all so you dont finish unless you buy the wilds",
            "rule_applied": "Remedy Consumption",
            "rationale": (
                "The golds are made deliberately unobtainable and the wilds are sold as "
                "a second route to the same limited items, which is Remedy Consumption."
            ),
        },
    ],
    "invoked_web_search": True,
    "search_query": "Monopoly Go gold stickers wild stickers",
    "search_result": (
        "Golds are restricted from ordinary trading and wilds convert into any missing "
        "sticker and are sold in bundles."
    ),
}


# --------------------------------------------------------------------------- helpers

def derive_code(label: dict) -> str:
    prefix = CLASS_PREFIX[label["high_level"]]
    words = re.sub(r"[^A-Za-z0-9 ]", " ", label["meso_label"]).split()
    return prefix + "_" + "".join(w[:1].upper() + w[1:] for w in words)


def codes_declared_in_codebook(labels: list[dict]) -> set[str]:
    """Every code the codebook itself uses in worked_examples[].labels_assigned."""
    found: set[str] = set()
    for lab in labels:
        for we in lab.get("worked_examples", []):
            found.update(we.get("labels_assigned", []))
    return found


def block(text: str, indent: str = "    ") -> str:
    """Indent a possibly multi-line codebook string without altering its wording."""
    lines = [ln.rstrip() for ln in str(text).strip().splitlines()]
    return "\n".join(indent + ln if ln else "" for ln in lines)


def approx_tokens(text: str) -> int:
    return len(text) // 4


def find_review(cb: dict, review_id: str) -> dict:
    """Locate an example slot by review_id. Returns {text, labels_assigned, why_not}."""
    for lab in cb["labels"]:
        for we in lab.get("worked_examples", []):
            if we.get("review_id") == review_id:
                return {"text": we["text"],
                        "labels_assigned": list(we.get("labels_assigned") or []),
                        "why_not": None,
                        "where": f"{lab['meso_label']} worked example"}
        for ce in lab.get("counterexamples", []):
            if ce.get("review_id") == review_id:
                return {"text": ce["text"],
                        "labels_assigned": [],
                        "why_not": ce.get("why_not"),
                        "where": f"{lab['meso_label']} counterexample"}
    for r in cb["global_rules"]:
        if r.get("worked_example_review_id") == review_id:
            return {"text": r["worked_example_text"],
                    "labels_assigned": list(r.get("worked_example_labels") or []),
                    "why_not": None,
                    "where": f"rule {r['id']} worked example"}
    raise SystemExit(f"exemplar review_id not found in the codebook: {review_id}")


# ----------------------------------------------------------------------- fixed prose
# The only text in the prompt not lifted from the codebook. Kept minimal and confined
# to: role, search procedure, output contract. Every coding claim below points at a
# codebook rule id rather than restating the rule in new words.

ROLE = """\
You are coding ONE app-store review of a mobile game against the codebook below.

A review usually describes more than one mechanic. Assign every label the review
supports, not the single best one (R9). Read the review closely first, including what
the reviewer describes without naming, then decide."""

SEARCH_POLICY = """\
WEB SEARCH

R10 permits a search. Operationally:
  - At most one search per review.
  - Search only to resolve what a term the reviewer used refers to: a named game mode,
    event, currency, item, or feature you cannot identify from the review text. The game
    name is supplied for this purpose.
  - Report every search in the output: the query and what it established. If you did not
    search, report that."""


def output_spec(codes: list[str]) -> str:
    code_lines = "\n".join("    " + c for c in codes)
    return f"""\
OUTPUT

Return one JSON object and nothing else. No prose before it, no prose after it, no markdown
code fences. The keys must appear in exactly this order:

{{
  "analysis": "<Work out what the review is actually describing, before you choose any
                label. The mechanics the reviewer names outright; the mechanics they
                describe without naming; what their account of their own play implies
                about how the game is built. Write this FIRST.>",
  "labels": [
    {{
      "label": "<one code from the list below>",
      "span": "<the exact words from the review that carry this mechanic, copied
                character for character from the review text>",
      "rule_applied": "<the codebook material this label rests on: the indicator the span
                        matches, the boundary rule that settled it, or the word
                        definition if the span meets the canonical definition directly>",
      "rationale": "<one line: why this span satisfies this label. If the mechanic is
                     implied rather than stated, say what the span implies and how.>"
    }}
  ],
  "invoked_web_search": <true|false>,
  "search_query": <null or the query string>,
  "search_result": <null or a short statement of what the search established>
}}

Constraints:
  - "labels" may contain only these {len(codes)} codes, spelled exactly:

{code_lines}

  - An empty "labels" array means NONE (R6). Never write the string "None" as a label.
    Never invent a code that is not in the list.
  - Each label appears at most once (R1), no matter how many times the review mentions it.
  - Every label carries a span, and the span is a verbatim substring of the review text
    (R3). A mechanic can be implied rather than stated; the span is then the exact words
    that carry the implication, and "rationale" explains the step.
  - Write "analysis" first and let it do the reasoning. Do not decide the labels and then
    write a justification for them."""


# ------------------------------------------------------------------------- rendering

def render_rules(cb: dict, flags: dict, used_ids: set[str]) -> str:
    out = ["GLOBAL RULES", ""]
    for r in cb["global_rules"]:
        out.append(f"{r['id']}. {' '.join(str(r['statement']).split())}")
        if not flags["rule_examples"]:
            continue
        text = str(r.get("worked_example_text") or "").strip()
        if not text or r.get("worked_example_review_id") in used_ids:
            continue
        out.append("")
        out.append("    Worked example:")
        out.append(block('"' + text + '"', "      "))
        codes = r.get("worked_example_labels")
        if codes is not None:
            out.append(f"      Labels assigned: {', '.join(codes) if codes else 'NONE'}")
        if r.get("worked_example_justification"):
            out.append("      Why:")
            out.append(block(r["worked_example_justification"], "        "))
        out.append("")
    return "\n".join(out).rstrip()


def render_label(label: dict, code: str, flags: dict, used_ids: set[str]) -> str:
    out = [f"[{code}]  {label['meso_label']}", ""]
    out.append("  Definition:")
    out.append(block(label["canonical_definition"], "    "))

    if flags["indicators"] and label.get("indicators"):
        out.append("")
        out.append("  Indicators (each is an instance of this pattern; see R5):")
        for ind in label["indicators"]:
            out.append(block("- " + str(ind), "    "))

    if flags["boundary_rules"] and label.get("boundary_rules"):
        out.append("")
        out.append("  Boundary rules:")
        for br in label["boundary_rules"]:
            out.append(f"    vs {br['vs_label']}:")
            out.append(block(br["rule"], "      "))

    if flags["counterexamples"]:
        for ce in label.get("counterexamples", []):
            if ce.get("review_id") in used_ids:
                continue
            out.append("")
            out.append("  Counterexample (does NOT get this label):")
            out.append(block('"' + str(ce["text"]).strip() + '"', "    "))
            out.append("    Why not:")
            out.append(block(ce["why_not"], "      "))

    if flags["worked_examples"]:
        for we in label.get("worked_examples", []):
            if we.get("review_id") in used_ids:
                continue
            out.append("")
            out.append("  Worked example:")
            out.append(block('"' + str(we["text"]).strip() + '"', "    "))
            assigned = ", ".join(we.get("labels_assigned", [])) or "(none)"
            out.append(f"    Labels assigned: {assigned}")
            if we.get("justification"):
                out.append("    Why:")
                out.append(block(we["justification"], "      "))

    return "\n".join(out)


def render_exemplar(review_text: str, output_obj: dict) -> str:
    return "\n".join([
        "Review:",
        block('"' + str(review_text).strip() + '"', "  "),
        "",
        "Output:",
        block(json.dumps(output_obj, indent=2, ensure_ascii=False), "  "),
    ])


# ------------------------------------------------------------------------ validation

def validate_exemplar(name: str, spec: dict, cb: dict, valid_codes: set[str]) -> dict:
    """Check a pinned exemplar against the codebook and return the output object."""
    rid = spec["review_id"]
    src = find_review(cb, rid)
    review_text = src["text"]

    labels = spec.get("labels") or []
    codes = [l["label"] for l in labels]

    if len(set(codes)) != len(codes):
        raise SystemExit(f"{name}: a label appears twice, which violates R1")
    bad = [c for c in codes if c not in valid_codes]
    if bad:
        raise SystemExit(f"{name}: unknown code(s) {bad}")
    if sorted(codes) != sorted(src["labels_assigned"]):
        raise SystemExit(
            f"{name}: label set does not match the codebook's own labels for {rid[:8]}\n"
            f"  exemplar: {sorted(codes)}\n"
            f"  codebook: {sorted(src['labels_assigned'])} (from {src['where']})")

    for l in labels:
        if l["span"] not in review_text:
            raise SystemExit(
                f"{name}: span is not a verbatim substring of the codebook review text\n"
                f"  span : {l['span']!r}\n"
                f"  review: {review_text!r}")
        if not str(l.get("rule_applied", "")).strip():
            raise SystemExit(f"{name}: label {l['label']} has no rule_applied")
        if not str(l.get("rationale", "")).strip():
            raise SystemExit(f"{name}: label {l['label']} has no rationale")

    analysis = spec.get("analysis")
    if analysis is FROM_CODEBOOK_WHY_NOT:
        if not src["why_not"]:
            raise SystemExit(f"{name}: asked for the codebook why_not but {rid[:8]} has none")
        analysis = " ".join(str(src["why_not"]).split())
    if not str(analysis or "").strip():
        raise SystemExit(f"{name}: analysis is empty")

    if spec.get("invoked_web_search") and not spec.get("search_query"):
        raise SystemExit(f"{name}: invoked_web_search is true but search_query is null")
    if not spec.get("invoked_web_search") and spec.get("search_query"):
        raise SystemExit(f"{name}: search_query is set but invoked_web_search is false")

    out = {
        "analysis": analysis,
        "labels": [{"label": l["label"], "span": l["span"],
                    "rule_applied": l["rule_applied"], "rationale": l["rationale"]}
                   for l in labels],
        "invoked_web_search": bool(spec.get("invoked_web_search")),
        "search_query": spec.get("search_query"),
        "search_result": spec.get("search_result"),
    }
    return {"review_id": rid, "review_text": review_text, "output": out}


def assert_rule_ids(cb: dict, *texts: str) -> None:
    """Every R<n> mentioned in the fixed prose must exist in the codebook."""
    known = {r["id"] for r in cb["global_rules"]}
    cited = set()
    for t in texts:
        cited.update(re.findall(r"\bR\d{1,2}\b", t))
    missing = sorted(cited - known, key=lambda s: int(s[1:]))
    if missing:
        raise SystemExit(
            f"fixed prose cites rule id(s) not in the codebook: {missing}\n"
            f"  codebook has: {sorted(known, key=lambda s: int(s[1:]))}")


# --------------------------------------------------------------------------- build

def build(cb: dict, mode: str) -> tuple[str, dict]:
    flags = MODES[mode]
    labels = cb["labels"]
    code_of = {lab["meso_label"]: derive_code(lab) for lab in labels}

    derived = set(code_of.values())
    declared = codes_declared_in_codebook(labels)
    if declared and not declared <= derived:
        raise SystemExit(
            "the codebook's own labels_assigned use codes this build cannot derive.\n"
            f"  codebook only: {sorted(declared - derived)}\n"
            "Fix CLASS_PREFIX / derive_code, or the codebook, before building.")
    if len(derived) != len(labels):
        raise SystemExit("duplicate label codes derived; codes must be 1:1 with labels.")

    spec_codes = sorted(derived)
    assert_rule_ids(cb, ROLE, SEARCH_POLICY, output_spec(spec_codes))

    none_ex = validate_exemplar("NONE_EXEMPLAR", NONE_EXEMPLAR, cb, derived)
    pos_ex = validate_exemplar("POSITIVE_EXEMPLAR", POSITIVE_EXEMPLAR, cb, derived)
    if none_ex["output"]["labels"]:
        raise SystemExit("none_exemplar must have an empty labels array")
    if not pos_ex["output"]["labels"]:
        raise SystemExit("positive_exemplar must assign at least one label")
    used_ids = {none_ex["review_id"], pos_ex["review_id"]}

    parts: list[tuple[str, str]] = []
    parts.append(("role", ROLE))
    parts.append(("rules", render_rules(cb, flags, used_ids)))
    parts.append(("search_policy", SEARCH_POLICY))

    lab_sections = ["LABELS", "",
                    f"{len(labels)} labels in {len(cb['high_level_classes'])} classes. "
                    "A label assigns its class; you output meso codes only."]
    by_class: dict[str, list[dict]] = {}
    for lab in labels:
        by_class.setdefault(lab["high_level"], []).append(lab)
    for cls in cb["high_level_classes"]:
        name = cls["name"]
        if name not in by_class:
            continue
        lab_sections.append("")
        lab_sections.append("-" * 75)
        lab_sections.append(f"CLASS: {name.upper()}")
        lab_sections.append(block(cls["canonical_definition"], "  "))
        lab_sections.append("-" * 75)
        for lab in by_class[name]:
            lab_sections.append("")
            lab_sections.append(
                render_label(lab, code_of[lab["meso_label"]], flags, used_ids))
    parts.append(("labels", "\n".join(lab_sections)))

    parts.append(("output_spec", output_spec(spec_codes)))
    parts.append(("exemplars", "\n\n".join([
        "EXAMPLES",
        render_exemplar(pos_ex["review_text"], pos_ex["output"]),
        "-" * 75,
        render_exemplar(none_ex["review_text"], none_ex["output"]),
    ])))

    body = ("\n\n" + "=" * 75 + "\n\n").join(text.rstrip() for _, text in parts) + "\n"

    rendered_ce = sum(
        1 for lab in labels for ce in lab.get("counterexamples", [])
        if flags["counterexamples"] and ce.get("review_id") not in used_ids)
    rendered_we = sum(
        1 for lab in labels for we in lab.get("worked_examples", [])
        if flags["worked_examples"] and we.get("review_id") not in used_ids)
    rendered_rule_ex = sum(
        1 for r in cb["global_rules"]
        if flags["rule_examples"] and str(r.get("worked_example_text") or "").strip()
        and r.get("worked_example_review_id") not in used_ids)
    rendered_we_why = sum(
        1 for lab in labels for we in lab.get("worked_examples", [])
        if flags["worked_examples"] and we.get("review_id") not in used_ids
        and we.get("justification"))

    manifest = {
        "prompt_version": PROMPT_VERSION,
        "mode": mode,
        "codebook_version": cb["version"],
        "flags": flags,
        "n_labels": len(labels),
        "none_exemplar_id": none_ex["review_id"],
        "positive_exemplar_id": pos_ex["review_id"],
        "rule_examples_rendered": rendered_rule_ex,
        "counterexamples_rendered": rendered_ce,
        "worked_examples_rendered": rendered_we,
        "worked_examples_with_why": rendered_we_why,
        "prompt_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "chars": len(body),
        "approx_tokens": approx_tokens(body),
        "section_approx_tokens": {name: approx_tokens(text) for name, text in parts},
    }
    return body, manifest


def render_header(manifest: dict, codebook_path: str) -> str:
    now = _dt.datetime.now().astimezone()
    lines = [
        "# BUILD LOG -- NOT PART OF THE PROMPT.",
        "# Everything above the sentinel line is metadata. Sending it to a model changes the",
        "# cached prefix on every build and destroys prompt caching. Use load_prompt().",
        "#",
        f"# built_at                 : {now.isoformat(timespec='seconds')}",
        f"# codebook_file            : {codebook_path}",
        f"# codebook_version         : {manifest['codebook_version']}",
        f"# prompt_version           : {manifest['prompt_version']}",
        f"# mode                     : {manifest['mode']}",
        f"# flags                    : {manifest['flags']}",
        f"# n_labels                 : {manifest['n_labels']}",
        f"# none_exemplar_id         : {manifest['none_exemplar_id']}",
        f"# positive_exemplar_id     : {manifest['positive_exemplar_id']}",
        f"# rule_examples_rendered   : {manifest['rule_examples_rendered']}",
        f"# counterexamples_rendered : {manifest['counterexamples_rendered']}",
        f"# worked_examples_rendered : {manifest['worked_examples_rendered']}"
        f"  ({manifest['worked_examples_with_why']} with a Why: block)",
        f"# prompt_sha256            : {manifest['prompt_sha256']}",
        f"# chars                    : {manifest['chars']}",
        f"# approx_tokens            : {manifest['approx_tokens']}  (chars/4, rough)",
        "#",
        "# section approx tokens:",
    ]
    for name, tok in manifest["section_approx_tokens"].items():
        lines.append(f"#   {name:<18}: {tok}")
    lines += ["#", SENTINEL, ""]
    return "\n".join(lines)


def load_prompt(path: str | Path) -> str:
    """Read a built prompt file and return ONLY the prompt body. Use this everywhere."""
    text = Path(path).read_text(encoding="utf-8")
    if SENTINEL not in text:
        raise ValueError(f"{path}: no sentinel found; not a build_prompt.py output")
    return text.split(SENTINEL, 1)[1].lstrip("\n")


def main() -> None:
    ap = argparse.ArgumentParser(description="Build the teacher prompt from the codebook.")
    ap.add_argument("--codebook", default=CODEBOOK)
    ap.add_argument("--mode", choices=list(MODES), default=None,
                    help="build one mode only (default: all three)")
    ap.add_argument("--out", default=None,
                    help="output path for a single mode, or - for stdout")
    ap.add_argument("--emit-prompt-only", action="store_true",
                    help="write the prompt body with no build-log header")
    args = ap.parse_args()

    cb = json.loads(Path(args.codebook).read_text(encoding="utf-8"))
    modes = [args.mode] if args.mode else list(MODES)

    if args.out == "-":
        if len(modes) != 1:
            raise SystemExit("--out - needs a single --mode")
        body, _ = build(cb, modes[0])
        sys.stdout.write(body)
        return

    summary = {}
    for mode in modes:
        body, manifest = build(cb, mode)
        text = body if args.emit_prompt_only else render_header(
            manifest, args.codebook) + body

        if args.out and len(modes) == 1:
            out = Path(args.out)
        else:
            out = Path(OUT_DIR) / f"{OUT_STEM}_{PROMPT_VERSION}_{mode}.txt"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        Path(str(out) + ".manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        summary[mode] = {"path": str(out),
                         "approx_tokens": manifest["approx_tokens"],
                         "prompt_sha256": manifest["prompt_sha256"],
                         "rule_examples_rendered": manifest["rule_examples_rendered"],
                         "counterexamples_rendered": manifest["counterexamples_rendered"],
                         "worked_examples_rendered": manifest["worked_examples_rendered"]}
        print(f"{mode:<9} {manifest['approx_tokens']:>6} tok   "
              f"sha {manifest['prompt_sha256'][:12]}   {out}", file=sys.stderr)

    if len(modes) > 1:
        sp = Path(OUT_DIR) / f"{OUT_STEM}_{PROMPT_VERSION}_summary.json"
        sp.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(f"summary   {sp}", file=sys.stderr)


if __name__ == "__main__":
    main()