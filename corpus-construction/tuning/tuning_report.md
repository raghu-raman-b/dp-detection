# tuning / bake-off set, codebook v0.20

**This set is burned.** Prompt refinement and provider selection run here, so no number computed on these rows belongs in a reported evaluation. Every record carries `set_role: "tuning_selection"`.

- seed: `20260820` | input folder: `../../labeled_data/`
- output: `../../tuning/tuning_set_50.jsonl` | blind: `../../tuning/tuning_set_50_blind.jsonl`
- eligible pool: **471** | sampled: **50** (target 50)
- true-None: **10** (target 10) | single-label: **13** | multi-label: **27**
- labels represented: **26/29**
- codebook example ids indexed: **65** | validation ids excluded: **75**

## line accounting

| outcome                                   |   lines |
| ----------------------------------------- | ------: |
| blank                                     |       0 |
| unparseable JSON                          |       0 |
| no review_id                              |       0 |
| codebook example, excluded                |      65 |
| already in the validation set, excluded   |      75 |
| repeat of an earlier review_id, collapsed |       0 |
| uncoded                                   |       0 |
| eligible pool                             |     471 |
| **total lines read**                      | **611** |

Sum of outcomes: 611

Repeats whose labels differed from the copy that was kept: **0** (listed in the notes).
Rows whose labels array disagreed with the binary columns: **0**.

## sample composition

| bucket |   n |
| ------ | --: |
| fill   |  29 |
| cover  |  11 |
| none   |  10 |

| field              | distribution                                       |
| ------------------ | -------------------------------------------------- |
| stratum            | targeted 30, random 20                             |
| market             | UK 31, IN 10, US 9                                 |
| star rating        | 1 star 21, 2 star 12, 3 star 7, 4 star 4, 5 star 6 |
| distinct games     | 38                                                 |
| most from one game | 3 (no cap applied)                                 |
| labels per review  | mean 1.72                                          |

## label coverage

| label                                        | left in pool | in sample | represented |
| -------------------------------------------- | -----------: | --------: | :---------: |
| Temporal: Playing by Appointment             |           36 |         7 |     yes     |
| Temporal: Daily Rewards                      |           12 |         2 |     yes     |
| Temporal: Grinding                           |           15 |         5 |     yes     |
| Temporal: Advertisement                      |           14 |         2 |     yes     |
| Temporal: Infinite Treadmill                 |            2 |         1 |     yes     |
| Temporal: Mandatory Marathon                 |            9 |         1 |     yes     |
| Monetary: Pay to Progress                    |           85 |        18 |     yes     |
| Monetary: Intermediate Currency              |           19 |         4 |     yes     |
| Monetary: Deceptive Luxury                   |            2 |         2 |     yes     |
| Monetary: Recurring Fee                      |            8 |         1 |     yes     |
| Monetary: Gambling                           |           17 |         2 |     yes     |
| Monetary: Power Creep                        |            6 |         2 |     yes     |
| Monetary: Waste Aversion                     |            8 |         2 |     yes     |
| Monetary: Easy to Purchase                   |           13 |         2 |     yes     |
| Monetary: UI Misdirection                    |           12 |         3 |     yes     |
| Monetary: Never-Ending Lure                  |            0 |         0 | EMPTY POOL  |
| Social: Forced Fellowship                    |            8 |         1 |     yes     |
| Social: Friend Spam / Impersonation          |            1 |         1 |     yes     |
| Social: Reciprocity                          |           13 |         3 |     yes     |
| Social: Encourages Anti-Social Behavior      |            2 |         1 |     yes     |
| Social: Fear of Missing Out (FOMO)           |            0 |         0 | EMPTY POOL  |
| Social: Competition                          |           49 |         8 |     yes     |
| Psychological: Easy to Get, Hard to Lose     |            5 |         1 |     yes     |
| Psychological: Complete the Collection       |           17 |         5 |     yes     |
| Psychological: Illusion of Control           |           26 |         3 |     yes     |
| Psychological: Aesthetic Manipulation        |            8 |         2 |     yes     |
| Psychological: Optimism and Frequency Biases |            7 |         1 |     yes     |
| Psychological: Reward Mania                  |           34 |         6 |     yes     |
| Technical: Fragmented Downloads              |            0 |         0 | EMPTY POOL  |

### labels not represented

| label                              | left in pool | reason                                                             |
| ---------------------------------- | -----------: | ------------------------------------------------------------------ |
| Monetary: Never-Ending Lure        |            0 | every remaining row is a codebook example or in the validation set |
| Social: Fear of Missing Out (FOMO) |            0 | every remaining row is a codebook example or in the validation set |
| Technical: Fragmented Downloads    |            0 | every remaining row is a codebook example or in the validation set |

Labels with nothing left to draw from: M_NeverEndingLure, S_FearOfMissingOutFOMO, Tech_FragmentedDownloads. Raising TOTAL will not help; only new coding will.

## notes

- `validation_set.jsonl`: 75 lines, 75 new ids (running union 75)
- `validation_set_blind.jsonl`: 75 lines, 0 new ids (running union 75)
- read 2 file(s): `random.jsonl`, `targeted.jsonl`
- M_NeverEndingLure: not represented (no rows left outside the codebook and validation set)
- S_FearOfMissingOutFOMO: not represented (no rows left outside the codebook and validation set)
- Tech_FragmentedDownloads: not represented (no rows left outside the codebook and validation set)
