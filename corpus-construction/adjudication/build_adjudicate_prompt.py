#!/usr/bin/env python3
"""
build_adjudicate_prompt.py  --  a1

Deterministically renders the ADJUDICATION prompt from the dark-patterns codebook JSON.

This is a fork of build_prompt.py. The teacher prompt and this prompt render the same
codebook body byte for byte; only the task framing and the output contract differ.
Keep the fork: build_prompt.py must stay untouched so teacher_v1.txt's SHA never moves
mid-bake-off.

The task is VERIFICATION, not labeling. The model receives one review plus the labels a
human coder already assigned, and decides, per label, whether the codebook supports it.
On a review with no labels it decides instead whether NONE is supported.

Design rules (identical to build_prompt.py, do not relax):
  1. The codebook is the single source of truth. Every rule, definition, indicator,
     boundary rule and example in the prompt is copied verbatim from the JSON.
     Nothing is paraphrased, summarised, or invented at build time.
  2. The build is a pure function of (codebook file, flags). Same inputs -> byte-identical
     prompt body -> same prompt SHA -> same provider cache entry.
  3. The build log (timestamp, sizes, SHA) is written ABOVE the sentinel line and is NOT
     part of the prompt. Anything below the sentinel is the prompt, exactly.

     >>> Never send the header to a model. Use load_prompt() or --emit-prompt-only. <<<
     A timestamp inside the cached prefix means a cache miss on every single call.

Usage:
    python build_adjudicate_prompt.py --codebook codebook_v0_20.json \
        --out adjudication/prompts/adjudicate_v1.txt
    python build_adjudicate_prompt.py --codebook codebook_v0_20.json --examples boundary
    python build_adjudicate_prompt.py --out - --emit-prompt-only
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import re
import sys
from pathlib import Path

PROMPT_VERSION = "a1"

# Everything after this line in the output file is the prompt. Nothing before it is.
SENTINEL = "=============================== PROMPT BODY ==============================="

# Class name -> code prefix. Verified against the codes used in the codebook's own
# worked_examples[].labels_assigned; the build asserts the derived set matches.
CLASS_PREFIX = {
    "Temporal": "T",
    "Monetary": "M",
    "Social": "S",
    "Psychological": "P",
    "Technical": "Tech",
}

# Pin this before the real run and never change it again. Leave None to let the build
# pick deterministically; it prints what it picked so you can paste it back here.
# The exemplar is drawn from the codebook's counterexamples: a counterexample is already
# "this review does NOT get this label, and here is why", which is exactly one
# verification decision. Nothing is invented to build it.
VERIFY_EXEMPLAR_ID: str | None = None


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


# ----------------------------------------------------------------------- fixed prose
# The only text in the prompt not lifted from the codebook. Kept minimal and confined
# to: role, construct restatement, search procedure, output contract. Every coding
# claim below points at a codebook rule id rather than restating the rule in new words.

ROLE = """\
You check the work of a human annotator. You are given ONE app-store review of a mobile
game and the labels that annotator assigned to it. You do not relabel the review.

Your task, for each label the annotator assigned: does the codebook below support that
label on this review's own words? A label is supported only where the review itself
describes the mechanic and you can quote the reviewer's exact words that trigger it.

If the annotator assigned no labels, decide instead whether the codebook supports that:
is there a mechanic described in this review that one of the labels covers?

Apply the codebook as written. The annotator may be right. Do not manufacture a
disagreement, and do not defer to the assigned label either; check it."""

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
INPUT

You receive one JSON object:

{{
  "game_name": "<title of the game>",
  "review_text": "<the review>",
  "assigned_labels": ["<code>", ...]      // may be empty
}}


OUTPUT

Return one JSON object and nothing else. No prose before it, no prose after it, no markdown
code fences. The keys must appear in exactly this order:

{{
  "analysis": "<short. Which mechanics the reviewer describes, in the reviewer's terms.
                Write this BEFORE deciding anything.>",
  "verdicts": [
    {{
      "label": "<one of the assigned_labels, echoed exactly>",
      "verdict": "<supported | unsupported | wrong_label>",
      "span": "<verbatim substring of review_text that supports it, or null>",
      "suggested_label": <null, or the code that fits instead>,
      "rule_id": "<the codebook rule or boundary rule your decision rests on, e.g. R1>",
      "why": "<one line>"
    }}
  ],
  "none_check": {{
    "supported": <true|false>,
    "suggested_label": <null or a code>,
    "span": <null or a verbatim substring>,
    "why": "<one line>"
  }},
  "invoked_web_search": <true|false>,
  "search_query": <null or the query string>,
  "search_result": <null or a short statement of what the search established>
}}

Which of the two branches you fill depends on the input:

  - assigned_labels NOT empty: emit exactly one entry in "verdicts" for every assigned
    label, in the order given, and set "none_check" to null. Never add a verdict for a
    label that was not assigned, and never drop one that was. Do NOT report labels you
    think are missing from the review; you are checking what is there.

  - assigned_labels EMPTY: set "verdicts" to [] and fill "none_check". The annotator
    called this review NONE. "supported": true agrees. "supported": false means one of
    the codes below does apply, and you must name it and quote its span.

The three verdicts:

  - "supported": the codebook backs this label on this review. Quote the span.
  - "unsupported": no label applies to what the annotator saw here. span is null.
  - "wrong_label": the review does describe a codeable mechanic, but a different code
    covers it. Name it in "suggested_label" and quote the span that fits that code.

Constraints:
  - "label", "suggested_label" and the "none_check" suggestion may use only these
    {len(codes)} codes, spelled exactly:

{code_lines}

  - Never invent a code that is not in the list. Never write the string "None" as a code;
    absence is expressed by the fields above, not by a code (R6).
  - Every span must be a verbatim substring of review_text, copied character for
    character. If you cannot quote it verbatim, the label is not supported (R3).
  - "supported" requires a span. "unsupported" requires span null.
  - Write "analysis" first and let it do the reasoning. Do not decide the verdicts and
    then write a justification for them."""


# ------------------------------------------------------------------------- rendering

def render_rules(cb: dict) -> str:
    out = ["GLOBAL RULES", ""]
    for r in cb["global_rules"]:
        out.append(f"{r['id']}. {' '.join(str(r['statement']).split())}")
    return "\n".join(out)


def render_label(label: dict, code: str, args, used_ids: set[str]) -> str:
    out = [f"[{code}]  {label['meso_label']}", ""]
    out.append("  Definition:")
    out.append(block(label["canonical_definition"], "    "))

    if args.indicators and label.get("indicators"):
        out.append("")
        out.append("  Indicators (each is an instance of this pattern; see R5):")
        for ind in label["indicators"]:
            out.append(block("- " + str(ind), "    "))

    if args.boundary_rules and label.get("boundary_rules"):
        out.append("")
        out.append("  Boundary rules:")
        for br in label["boundary_rules"]:
            out.append(f"    vs {br['vs_label']}:")
            out.append(block(br["rule"], "      "))

    if args.examples in ("boundary", "full"):
        for ce in label.get("counterexamples", []):
            if ce.get("review_id") in used_ids:
                continue
            out.append("")
            out.append("  Counterexample (does NOT get this label):")
            out.append(block('"' + str(ce["text"]).strip() + '"', "    "))
            out.append("    Why not:")
            out.append(block(ce["why_not"], "      "))

    if args.examples == "full":
        for we in label.get("worked_examples", []):
            if we.get("review_id") in used_ids:
                continue
            out.append("")
            out.append("  Worked example:")
            out.append(block('"' + str(we["text"]).strip() + '"', "    "))
            assigned = ", ".join(we.get("labels_assigned", [])) or "(none)"
            out.append(f"    Labels assigned: {assigned}")

    return "\n".join(out)


def pick_verify_exemplar(cb: dict, code_of: dict, rid: str | None) -> tuple[dict, str]:
    """One counterexample, re-read as a verification decision.

    A counterexample in the codebook is already the exact shape of this task: a review,
    a label that does NOT apply to it, and the reason. Rendering it as an annotator who
    assigned that label and a verdict of "unsupported" invents nothing. Returns
    (counterexample, code_of_the_label_it_belongs_to).

    Note the asymmetry: this exemplar demonstrates the "unsupported" branch only. The
    "supported" and "wrong_label" branches are specified by the output contract alone,
    because the codebook's worked_examples carry labels_assigned but no spans, and a
    "supported" exemplar would require inventing one.
    """
    candidates = []
    for lab in cb["labels"]:
        for ce in lab.get("counterexamples", []):
            candidates.append((ce, code_of[lab["meso_label"]]))
    if rid:
        for ce, code in candidates:
            if ce.get("review_id") == rid:
                return ce, code
        raise SystemExit(f"verify-exemplar id not found among counterexamples: {rid}")
    if not candidates:
        raise SystemExit("codebook has no counterexamples to draw a verify exemplar from")
    return candidates[0]


def render_verify_exemplar(ce: dict, code: str) -> str:
    why = " ".join(str(ce["why_not"]).split())
    # If the codebook's own why_not names a rule, use it. Never invent one.
    m = re.search(r"\bR\d{1,2}\b", why)
    demo_in = {
        "game_name": "<game>",
        "review_text": str(ce["text"]).strip(),
        "assigned_labels": [code],
    }
    demo_out = {
        "analysis": why,
        "verdicts": [{
            "label": code,
            "verdict": "unsupported",
            "span": None,
            "suggested_label": None,
            "rule_id": m.group(0) if m else None,
            "why": why,
        }],
        "none_check": None,
        "invoked_web_search": False,
        "search_query": None,
        "search_result": None,
    }
    return "\n".join([
        "EXAMPLE",
        "",
        "Input:",
        block(json.dumps(demo_in, indent=2, ensure_ascii=False), "  "),
        "",
        "Output:",
        block(json.dumps(demo_out, indent=2, ensure_ascii=False), "  "),
    ])


def build(cb: dict, args) -> tuple[str, dict]:
    labels = cb["labels"]
    code_of = {lab["meso_label"]: derive_code(lab) for lab in labels}

    derived = set(code_of.values())
    declared = codes_declared_in_codebook(labels)
    if declared and derived != declared:
        raise SystemExit(
            "code derivation does not match the codebook's own labels_assigned.\n"
            f"  derived only: {sorted(derived - declared)}\n"
            f"  codebook only: {sorted(declared - derived)}\n"
            "Fix CLASS_PREFIX / derive_code, or the codebook, before building."
        )
    if len(derived) != len(labels):
        raise SystemExit("duplicate label codes derived; codes must be 1:1 with labels.")

    verify_ex, verify_code = pick_verify_exemplar(
        cb, code_of, args.verify_exemplar or VERIFY_EXEMPLAR_ID)
    used_ids = {verify_ex["review_id"]}

    parts: list[tuple[str, str]] = []
    parts.append(("role", ROLE))
    parts.append(("rules", render_rules(cb)))
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
            lab_sections.append(render_label(lab, code_of[lab["meso_label"]], args, used_ids))
    parts.append(("labels", "\n".join(lab_sections)))

    parts.append(("output_spec", output_spec(sorted(derived))))
    parts.append(("verify_exemplar", render_verify_exemplar(verify_ex, verify_code)))

    body = ("\n\n" + "=" * 75 + "\n\n").join(text.rstrip() for _, text in parts) + "\n"

    manifest = {
        "prompt_version": PROMPT_VERSION,
        "codebook_version": cb["version"],
        "examples_mode": args.examples,
        "indicators": args.indicators,
        "boundary_rules": args.boundary_rules,
        "n_labels": len(labels),
        "verify_exemplar_id": verify_ex["review_id"],
        "verify_exemplar_label": verify_code,
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
        f"# built_at            : {now.isoformat(timespec='seconds')}",
        f"# codebook_file       : {codebook_path}",
        f"# codebook_version    : {manifest['codebook_version']}",
        f"# prompt_version      : {manifest['prompt_version']}",
        f"# examples_mode       : {manifest['examples_mode']}",
        f"# indicators          : {manifest['indicators']}",
        f"# boundary_rules      : {manifest['boundary_rules']}",
        f"# n_labels            : {manifest['n_labels']}",
        f"# verify_exemplar_id  : {manifest['verify_exemplar_id']}",
        f"# verify_exemplar_lab : {manifest['verify_exemplar_label']}",
        f"# prompt_sha256       : {manifest['prompt_sha256']}",
        f"# chars               : {manifest['chars']}",
        f"# approx_tokens       : {manifest['approx_tokens']}  (chars/4, rough)",
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
    ap = argparse.ArgumentParser(description="Build the adjudication prompt from the codebook.")
    ap.add_argument("--codebook", default="codebook_v0_20.json")
    ap.add_argument("--out", default="prompts/adjudicate_v1.txt",
                    help="output path, or - for stdout")
    ap.add_argument("--examples", choices=["none", "boundary", "full"], default="full",
                    help="none: definitions only. boundary: + counterexamples. "
                         "full: + worked examples (default)")
    ap.add_argument("--no-indicators", dest="indicators", action="store_false", default=True)
    ap.add_argument("--no-boundary-rules", dest="boundary_rules", action="store_false",
                    default=True)
    ap.add_argument("--verify-exemplar", default=None,
                    help="counterexample review_id to pin as the verification exemplar")
    ap.add_argument("--emit-prompt-only", action="store_true",
                    help="write the prompt body with no build-log header")
    args = ap.parse_args()

    cb = json.loads(Path(args.codebook).read_text(encoding="utf-8"))
    body, manifest = build(cb, args)
    text = body if args.emit_prompt_only else render_header(manifest, args.codebook) + body

    if args.out == "-":
        sys.stdout.write(text)
    else:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        Path(str(out) + ".manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {out}  ({manifest['approx_tokens']} approx tokens, "
              f"sha {manifest['prompt_sha256'][:12]})", file=sys.stderr)
        print(f"verify exemplar: {manifest['verify_exemplar_id']} "
              f"({manifest['verify_exemplar_label']})", file=sys.stderr)


if __name__ == "__main__":
    main()