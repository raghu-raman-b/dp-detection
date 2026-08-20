# tuning / bake-off set, codebook v0.20

**This set is burned.** Prompt refinement and provider selection run here, so no number computed on these rows belongs in a reported evaluation. Every record carries `set_role: "tuning_selection"`.

- seed: `20260820`  |  input folder: `../labeled_data/`
- output: `../tuning/tuning_set_50.jsonl`  |  blind: `../tuning/tuning_set_50_blind.jsonl`
- eligible pool: **473**  |  sampled: **50** (target 50)
- true-None: **10** (target 10)  |  single-label: **12**  |  multi-label: **28**
- labels represented: **28/29**
- codebook example ids indexed: **63**  |  validation ids excluded: **75**

## line accounting

| outcome | lines |
| --- | ---: |
| blank | 0 |
| unparseable JSON | 0 |
| no review_id | 0 |
| codebook example, excluded | 66 |
| already in the validation set, excluded | 77 |
| repeat of an earlier review_id, collapsed | 4 |
| uncoded | 0 |
| eligible pool | 473 |
| **total lines read** | **620** |

Sum of outcomes: 620

Repeats whose labels differed from the copy that was kept: **0** (listed in the notes).
Rows whose labels array disagreed with the binary columns: **0**.

## sample composition

| bucket | n |
| --- | ---: |
| fill | 25 |
| cover | 15 |
| none | 10 |

| field | distribution |
| --- | --- |
| stratum | targeted 39, random 11 |
| market | UK 27, IN 15, US 8 |
| star rating | 1 star 20, 2 star 12, 3 star 6, 4 star 4, 5 star 8 |
| distinct games | 37 |
| most from one game | 3 (no cap applied) |
| labels per review | mean 1.82 |

## label coverage

| label | left in pool | in sample | represented |
| --- | ---: | ---: | :---: |
| Temporal: Playing by Appointment | 41 | 5 | yes |
| Temporal: Daily Rewards | 16 | 2 | yes |
| Temporal: Grinding | 22 | 3 | yes |
| Temporal: Advertisement | 18 | 3 | yes |
| Temporal: Infinite Treadmill | 2 | 1 | yes |
| Temporal: Mandatory Marathon | 10 | 1 | yes |
| Monetary: Pay to Progress | 104 | 13 | yes |
| Monetary: Intermediate Currency | 25 | 5 | yes |
| Monetary: Deceptive Luxury | 2 | 1 | yes |
| Monetary: Recurring Fee | 9 | 3 | yes |
| Monetary: Gambling | 23 | 5 | yes |
| Monetary: Power Creep | 7 | 2 | yes |
| Monetary: Waste Aversion | 10 | 1 | yes |
| Monetary: Easy to Purchase | 18 | 4 | yes |
| Monetary: UI Misdirection | 14 | 4 | yes |
| Monetary: Never-Ending Lure | 4 | 1 | yes |
| Social: Forced Fellowship | 8 | 2 | yes |
| Social: Friend Spam / Impersonation | 1 | 1 | yes |
| Social: Reciprocity | 12 | 2 | yes |
| Social: Encourages Anti-Social Behavior | 5 | 1 | yes |
| Social: Fear of Missing Out (FOMO) | 0 | 0 | EMPTY POOL |
| Social: Competition | 52 | 6 | yes |
| Psychological: Easy to Get, Hard to Lose | 5 | 2 | yes |
| Psychological: Complete the Collection | 24 | 4 | yes |
| Psychological: Illusion of Control | 37 | 7 | yes |
| Psychological: Aesthetic Manipulation | 8 | 2 | yes |
| Psychological: Optimism and Frequency Biases | 8 | 1 | yes |
| Psychological: Reward Mania | 43 | 8 | yes |
| Technical: Fragmented Downloads | 2 | 1 | yes |

### labels not represented

| label | left in pool | reason |
| --- | ---: | --- |
| Social: Fear of Missing Out (FOMO) | 0 | every remaining row is a codebook example or in the validation set |

Labels with nothing left to draw from: S_FearOfMissingOutFOMO. Raising TOTAL will not help; only new coding will.

## notes

- `validation_set.jsonl`: 75 lines, 75 new ids (running union 75)
- `validation_set_blind.jsonl`: 75 lines, 0 new ids (running union 75)
- read 6 file(s): `fsi.jsonl`, `minors.jsonl`, `random.jsonl`, `targeted.jsonl`, `targeted_2.jsonl`, `targeted_200.jsonl`
- S_FearOfMissingOutFOMO: not represented (no rows left outside the codebook and validation set)
