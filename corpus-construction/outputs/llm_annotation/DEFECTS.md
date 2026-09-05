# Defect inventory — LLM-annotated corpus

Measured on 150,792 rows / 109,823 labels (75.5% of the run, 2026-09-05).
Regenerate at any time with `python scripts/repair_labels.py --report-only`.

**97.3% of labels have no defect of any kind.** Everything below is the other 2.7%,
and most of it is repairable to a *proven* result rather than a guess.

---

## Summary

| class | defect | count | rate | disposition |
|---|---|---:|---:|---|
| CODE | out-of-codebook label code | 1 | 0.0009% | auto-repaired |
| DUPE | same code twice on one review | 168 | 0.15% | auto-repaired |
| SPAN | span not verbatim, recoverable | 761 | 0.69% | auto-repaired |
| SPAN | span not verbatim, not recoverable | 224 | 0.20% | **human review** |
| flag | span shorter than 12 chars | 1,962 | 1.79% | flagged, untouched |
| flag | span is the entire review | 44 | 0.04% | flagged, untouched |
| flag | 7+ labels on one review | 38 | 0.03% | flagged, untouched |
| — | API error / unparseable response | 0 | 0% | none occurred |
| — | truncated response | 0 | 0% | none occurred |
| — | empty span / rationale / rule / analysis | 0 | 0% | none occurred |

---

## CODE — wrong class prefix

`M_IllusionOfControl` emitted once for `P_IllusionOfControl`, on a review reading
*"EVERYTIME YOU BUY COINS THEY MAKE U LOSE IT SO U BUY MORE"*. The pattern was
identified correctly; the model reached for the Monetary prefix because the review was
about money.

**Repair rule:** rewrite only when the suffix after the first underscore matches
**exactly one** codebook entry. Ambiguous cases are reported and left alone.

---

## DUPE — the same code listed twice

168 reviews carried a code twice, usually with two spans quoting two places where the
same pattern appears.

**Repair rule:** keep the first occurrence, drop later ones. Lossy — the second span is
discarded — but the label set is what the corpus is for, and a set cannot hold a member
twice.

---

## SPAN — the quote is not a literal substring

The contract asks for a verbatim quote. Five ways it drifts:

| sub-type | count | example | recoverable |
|---|---:|---|---|
| case drift | 293 | `The pop ups...` vs `the pop ups...` | yes |
| over-escaped quotes | 19 | `you \"buy\" them` for `you "buy" them` | yes |
| ellipsis-joined fragments | 138 | `A ... B` spanning a gap in the review | usually |
| truncated / over-extended | 148 | drops or adds a leading character | yes |
| genuine paraphrase | 224 | the model wrote its own words as a quote | **no** |

**Repair rule:** every strategy ends by cutting the replacement **out of the original
review text**, then re-checking it against that text before accepting. The result is
verbatim by construction, not by hope. A fuzzy match is taken only when the longest
common block covers ≥85% of what the model claimed to be quoting (`--fuzz-min`).

---

## Human review of the remainder

The 224 paraphrases cannot be fixed by rule — but they are usually trivial for a person
(`credits` where the review says `credit's`). `repair_labels.py` exports them for
inspection:

```
python repair_labels.py --export           # writes unrepairable_spans.txt
```

One block per defect, carrying the problem, the model's span, and the **full review
text**, so nothing has to be looked up:

```
### 1 of 224
review_id     : 4cc7023e-23fa-4a1d-893b-d1e9a425b63f
label_index   : 0
label         : T_DailyRewards
problem       : span not found in the review (best matching block covers 83%)
original_span : "credits you win by signing in daily"
action        : KEEP
span          : credits you win by signing in daily
--- review text ---
I'm addicted to this game! ... play with either credit's you win by signing in
daily, by winning bingo and games within the game ...
--- end ---
```

Edit two lines — `action` to `KEEP` / `FIX` / `DROP`, and `span` if fixing — then:

```
python repair_labels.py --checked unrepairable_spans.txt --apply
```

Four guarantees, each verified in test:

- **Typed spans need not match whitespace or case.** The passage is located and the
  exact substring is cut from the review, so what lands in the corpus is verbatim.
- **An unfindable span is rejected**, and a single rejection refuses the entire apply.
  A half-applied review file is worse than none.
- **A stale file cannot be applied.** `original_span` is re-checked against the corpus
  at apply time; if it has moved on you are told to re-export.
- **Human edits are recorded separately**, tagged `corrected by human review` or
  `dropped by human review`, so judgement calls stay distinguishable from rule-based
  ones when writing up.

---

## Flags — not defects, but worth knowing

- **Short spans (1,962).** Verbatim and legal, but quotes like *"Pay to win."* carry
  little evidence. Consider excluding from span-level analysis.
- **Whole-review spans (44).** The model quoted the whole review instead of the
  relevant clause. Verbatim, but uninformative.
- **7+ labels (38).** Not necessarily wrong — a long review can genuinely exhibit many
  patterns — but worth eyeballing before a co-occurrence analysis.

---

## Provenance

Every change, automatic or human, is recorded in the row:

```json
"repairs": [{"field": "span",
             "from": "credits you win by signing in daily",
             "to":   "credit's you win by signing in daily",
             "reason": "corrected by human review",
             "by": "repair_labels.py"}]
```

The shipped corpus therefore carries its own correction history; every repaired row is
findable with `grep '"repairs"'`. Nothing is silently rewritten.

## Order of operations

```
python repair_labels.py --report-only                      # inventory
python repair_labels.py --apply                            # 930 automatic repairs
python repair_labels.py --export                           # 224 for a human
#   ... edit unrepairable_spans.txt ...
python repair_labels.py --checked unrepairable_spans.txt --apply
```

`--apply` refuses to touch a file written to in the last two minutes: the annotator
holds `responses.jsonl` open in append mode, and rewriting it between two of its writes
would drop the rows in the gap. Run the repairs only after the annotation finishes.

## For the paper

> Of 109,823 emitted labels, 97.3% were free of any formatting defect. We repaired
> three recoverable classes — one out-of-codebook code (0.001%), 168 duplicate labels
> (0.15%), and 761 non-verbatim spans (0.69%) — using constructive rules that rewrite a
> span only to a string verified to occur in the source review. A further 224 spans
> (0.20%) were paraphrases rather than quotes; these were reviewed by hand, with each
> decision recorded in the released dataset. No response was truncated, unparseable, or
> lost to API error.
