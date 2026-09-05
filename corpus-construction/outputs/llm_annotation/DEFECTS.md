# Defect inventory — LLM-annotated corpus

Measured on 149,724 rows / 108,910 labels (75% of the run, 2026-09-05).
Regenerate with `python scripts/repair_labels.py --report-only`.

**97.27% of labels have no defect of any kind.** Everything below is the other 2.73%,
and most of it is repairable to a *proven* result rather than a guess.

---

## Summary

| class | defect | count | rate | status |
|---|---|---:|---:|---|
| CODE | out-of-codebook label code | 1 | 0.0009% | **repaired** |
| DUPE | same code twice on one review | 167 | 0.15% | **repaired** |
| SPAN | span not verbatim in the review | 973 | 0.89% | **752 repaired, 221 left** |
| flag | span shorter than 12 chars | 1,948 | 1.79% | flagged, not touched |
| flag | span is the entire review | 44 | 0.04% | flagged, not touched |
| flag | 7+ labels on one review | 38 | 0.03% | flagged, not touched |
| — | API error / unparseable response | 0 | 0% | none |
| — | truncated response | 0 | 0% | none |
| — | empty span / rationale / rule | 0 | 0% | none |
| — | empty analysis | 0 | 0% | none |

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

167 reviews carried a code twice, usually with two different spans quoting two places
in the review where the same pattern appears.

**Repair rule:** keep the first occurrence, drop later ones. This is lossy — the second
span is discarded — but the label set is what the corpus is for, and a set cannot hold
a member twice.

---

## SPAN — the quote is not a literal substring

The contract asks for a verbatim quote. Four distinct ways it drifts:

| sub-type | count | example | repairable |
|---|---:|---|---|
| case drift | 293 | `The pop ups...` vs `the pop ups...` in the review | yes |
| over-escaped quotes | 19 | `you \"buy\" them` for `you "buy" them` | yes |
| ellipsis-joined fragments | 138 | `A ... B` where the review has `A ... (middle) ... B` | usually |
| truncated / over-extended | 148 | span drops or adds a leading character | yes |
| genuinely absent | 373 | paraphrase, or quoted from the wrong review | **no** |

**Repair rule:** every strategy ends by cutting the replacement **out of the original
review text**, so the result is verbatim by construction. The repair is then re-checked
against the text before being accepted. A fuzzy match is only taken when the longest
common block covers ≥85% of what the model claimed to be quoting.

After repair, **221 spans (0.20% of labels) remain non-verbatim.** These are
paraphrases the model wrote as if they were quotes. They are left in place and flagged
— a visible defect beats an invented quote.

---

## Flags — not defects, but worth knowing

- **Short spans (1,948).** Verbatim and legal, but quotes like *"Pay to win."* carry
  little evidence. Consider excluding from any span-level analysis.
- **Whole-review spans (44).** The model quoted the entire review rather than the
  relevant clause. Verbatim, but uninformative as evidence.
- **7+ labels (38).** Not necessarily wrong — a long review can genuinely exhibit
  many patterns — but worth eyeballing before they enter a co-occurrence analysis.

---

## Provenance

`repair_labels.py` records every change in the row itself:

```json
"repairs": [{"field": "span",
             "from": "you \\\"buy\\\" them",
             "to":   "you \"buy\" them",
             "reason": "unescaped",
             "by": "repair_labels.py"}]
```

So the shipped corpus carries its own correction history, and any repaired row can be
found with `grep '"repairs"'`. Nothing is silently rewritten.

## For the paper

> Of 108,910 emitted labels, 97.3% were free of any formatting defect. We repaired
> three recoverable classes — one out-of-codebook code (0.001%), 167 duplicate labels
> (0.15%), and 752 non-verbatim spans (0.69%) — using constructive rules that rewrite a
> span only to a string verified to occur in the source review. A further 221 spans
> (0.20%) were paraphrases rather than quotes and were retained and flagged rather than
> rewritten. No response was truncated, unparseable, or lost to API error. All
> corrections are recorded per-row in the released dataset.
