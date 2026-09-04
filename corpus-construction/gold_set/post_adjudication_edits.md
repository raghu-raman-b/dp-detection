# Post-adjudication edits to the gold set

The three-coder adjudication panel exported on **2026-09-04T06:38:46Z** (`dp_gold.html` v1.0,
codebook v0.20). Any change to the adjudicated labels made *after* that export is recorded here,
so the panel session and the author's later corrections stay distinguishable in the paper record.

Coder votes and the display-only agreement block in `gold_provenance_2026-09-04-06-38-46.json`
are never rewritten by these edits — only the adjudicated `final_labels` move.

---

## 2026-09-04 — `c63003ef-dcdd-4ef2-a54e-0c9b0dfe931a` (Kingshot, UK, 2★)

**Added:** `T_PlayingByAppointment` · **Removed:** none

Labels before: `T_DailyRewards`, `T_Grinding`
Labels after: `T_PlayingByAppointment`, `T_DailyRewards`, `T_Grinding`

**Span** (shared with `T_DailyRewards`, per R9):

> wad impossible to keep track of them without relying on the daily quests and such.

**Reason.** The Daily Rewards `vs Playing by Appointment` boundary rule states: *"Assign Playing by
Appointment additionally when the daily cycle directly gates overall game progression rather than
just a standalone reward... When a daily reward mechanism itself acts as the barrier controlling
player progression, assign both tags under R9."* Here the daily quest cycle is what the player must
rely on to advance at all, not a standalone reward — so the boundary rule requires both labels.
The panel assigned `T_DailyRewards` alone; none of the three coders raised `T_PlayingByAppointment`.

**How found.** While assembling the prompt v3 worked examples, checking each candidate example
against the boundary rules of its own label.

**Files updated.**

| file | change |
| --- | --- |
| `gold_set/gold_set.jsonl` | `actual_labels`, `actual_labels_str` |
| `validation/gold_set.jsonl` | kept byte-identical to the above |
| `gold_set/gold_provenance_*.json` | `final_labels`, `added`, `changed`, `decision_rule`, `note`; `counts.changed` 27 → 28; `post_adjudication_edit` on the review and `post_adjudication_edits` at top level |
| `gold_set/gold_changes_*.csv` | `final_labels`, `added`, `changed`, `decision_rule`, `note` |

**Not updated, deliberately.**

- `validation/validation_set.jsonl` — the author's pre-adjudication single-coder labels. It is the
  input the panel ruled on, and rewriting it would erase what was actually presented to them.
- `validation/validation_report.md` — a build-time record of how the sample was drawn (its label
  counts come from pilot labels, not from the adjudicated gold).
- The `agreement` block in the provenance — computed over coder votes, which did not change.

**Downstream impact.** Gold label instances 136 → 137; `T_PlayingByAppointment` support 6 → 7.

Rescored on 2026-09-04 with `compute_run_stats.py --eval-set validation`, which rebuilds
`index.jsonl` from the discovered runs rather than appending. The stale stats for both
`gpt-5.6-luna` runs were deleted first; the raw run outputs under
`outputs/validation/runs/` were not touched.

| run | metric | before | after |
| --- | --- | ---: | ---: |
| `gpt-5.6-luna_high_teacher_v2_full` | micro-F1 | 0.7769 | **0.7737** |
| | micro-R | 0.6912 | 0.6861 |
| | example-F1 | 0.7064 | 0.7042 |
| | meso macro-F1 | 0.7262 | 0.7232 |
| | FN | 42 | 43 |
| `gpt-5.6-luna_xhigh_teacher_v2_full` | micro-F1 | 0.8031 | **0.8000** |
| | micro-R | 0.7500 | 0.7445 |
| | example-F1 | 0.7439 | 0.7417 |
| | meso macro-F1 | 0.7492 | 0.7452 |
| | FN | 34 | 35 |

Precision, exact match and class macro-F1 are unchanged in both runs. Exactly one per-review
row moved in each — this review — and the change is a single added false negative: both runs
predicted `T_Grinding` alone here, already missing `T_DailyRewards`, and now miss
`T_PlayingByAppointment` as well. Neither run ever predicted the label on this review, so the
edit cannot flatter either score; both fell by ~0.003 micro-F1.

`T_PlayingByAppointment` per-label F1: high 0.8571 → 0.8000, xhigh 1.0000 → 0.9231.
