# coders/

One `coder_<id>_<stamp>.jsonl` per human coder, exactly as `dp_coder.html`
writes it ("Download labels"). Drop the files each coder returns in here and
nothing else — `compute_agreement.py` treats **every** `*.jsonl` in this
folder as a rater, so a stray file silently becomes a fifth opinion.

The author's own labels are **not** kept here. They are read from
`validation/validation_set.jsonl` (`actual_labels`) and enter as the rater
`author`.

## Consumers

| what | reads this folder |
|---|---|
| `scripts/post-label/compute_agreement.py` | α, per-label κ, pairwise tables → `outputs/agreement/` |
| `dp_gold.html` (repo root) | loads each file by hand in step 3 → `gold_set.jsonl` |

## What the reader does with each row

- `saved: 0` is an **abstention**, not a vote for NONE. Excluded from every
  numerator and denominator. Collapsing the two would dilute majorities and
  inflate agreement on exactly the rows nobody finished.
- A `review_id` not in `validation_set.jsonl` is ignored and reported.
- A `review_id` missing from a coder's file is an absence, not a NONE.
- `flagged` is never read: `dp_coder` clears it on save, so it is always 0 in
  a saved row. "Wanted to discuss" is `borderline == 1 || confidence == "L"`.
- Codes outside codebook v0.20 are counted, reported, and dropped.
- Coder identity comes from `coder_name`; if two files carry the same one,
  the second becomes `<name>#2` rather than being merged into the first.
