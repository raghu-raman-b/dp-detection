# gold_stats.py — gold set audit

## Run

```bash
pip install pandas numpy matplotlib
python gold_stats.py --input-dir /path/to/jsonl/files --out gold_label_stats
```

Expects `random.jsonl`, `targeted.jsonl`, `targeted_2.jsonl` in `--input-dir`.
Override with `--files a.jsonl b.jsonl`. Dev/test ratio via `--dev-frac 0.55`.

## Output

```
gold_label_stats/
  stats/
    SUMMARY.md                  narrative report — read this first
    summary.json                machine-readable headline numbers
    label_prevalence_power.csv  n_pos, Wilson CI, min detectable difference, power band
    integrity_issues.csv        row-level problems, severity-tagged
    boundary_pairs.csv          codebook boundary pairs + whether they're testable
    cooccurrence_{counts,jaccard,lift}.csv
    stratum_enrichment.csv      random vs targeted prevalence, enrichment factor
    label_profile.csv           per-label solo rate, co-label load, length, stars
    split_feasibility.csv       positives surviving in each split
    split_assignment.csv        the actual dev/test assignment — freeze this
  graphs/
    01_label_prevalence_power.png
    02_min_detectable_difference.png
    03_class_and_density.png
    04_cooccurrence.png
    05_boundary_pairs.png
    06_stratum_enrichment.png
    07_label_profile.png
    08_corpus_composition.png
    09_split_feasibility.png
```

## What each analysis is for

**Power (01, 02).** `min_detectable_recall_diff` is the smallest recall gap
between two prompt configs the gold set can resolve at α=.05, power=.80.
Labels where this exceeds ~20 points cannot arbitrate the bake-off — differences
there are noise, and treating them as signal is how you pick the wrong teacher.

**Integrity.** Cross-checks the four redundant encodings in your schema
(binary columns, `labels`, `labels_str`, `none`). Also flags duplicate
`review_id` across files and R6 violations (`none=1` with labels set).

**Label isolation (07).** `pct_solo` is the share of a label's positives where
it appears alone. A label never seen alone has no independent training signal —
the student learns the co-occurrence rather than the pattern, and the label is
the one most likely to be collapsed into its partner. Read alongside the
co-occurrence matrix and the boundary pairs.

**Boundary pairs (05).** The ten pairs the v0.16 codebook writes explicit
boundary rules for. If a pair has few single-label cases, you cannot detect a
teacher collapsing one into the other — which is the systematic error that
distillation transfers perfectly to the student.

**Enrichment (06).** Random-stratum prevalence estimates the true corpus base
rate. Multiply by 200k to see how many positives random sampling would yield
per label. Labels in the low hundreds need retrieval-based oversampling, and the
enrichment factor is the sampling weight you must record to correct the prior
at training time.

**Split (09).** Iterative stratification (Sechidis et al.) — allocates the
rarest label first so low-count labels aren't stranded in one split. Freeze
`split_assignment.csv` before any prompt engineering.

## Fields used

Only fields that are reliably populated: the 29 label binaries, `labels`,
`none`, `review_id`, `review_text`, `stratum`, `star_rating`, `game_name`,
`market`, `review_date`, `codebook_version`, `pass`, `seed_keyword`.

`confidence`, `borderline`, `rule_applied`, and `rationale` are ignored.
`flagged` is dropped automatically if it is all zeros.

Because `rationale` is not used, there is no span supervision available from the
gold set. If the student should emit spans, they have to come from the teacher,
and can only be spot-checked rather than scored.

## Notes

- Label column names and the 5-class grouping are hardcoded at the top from
  codebook v0.16. Edit `LABELS` if the schema changes.
- `BOUNDARY_PAIRS` is derived from the codebook's `boundary_rules` where both
  sides are real labels. Extend it if you add pairs.
- Power thresholds (`POWER_UNUSABLE=10`, `POWER_WEAK=30`) are conventional
  rules of thumb, not derived from your data — adjust if you have a reason to.
