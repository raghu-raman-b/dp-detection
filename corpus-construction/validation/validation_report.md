# validation set, codebook v0.20

- seed: `20260812` | input folder: `../../labeled_data/`
- output: `../../validation/validation_set.jsonl`
- eligible pool: **546** | sampled: **75** (target 75)
- true-None: **9** (want 8-10)
- multi-label: **17** (want 4-5) <- over the ceiling, label coverage took priority
- codebook example ids indexed: **65**

## line accounting

| outcome                                   |   lines |
| ----------------------------------------- | ------: |
| blank                                     |       0 |
| unparseable JSON                          |       0 |
| no review_id                              |       0 |
| codebook example, excluded                |      65 |
| repeat of an earlier review_id, collapsed |       0 |
| uncoded                                   |       0 |
| eligible pool                             |     546 |
| **total lines read**                      | **611** |

Sum of outcomes: 611

Repeats whose labels differed from the copy that was kept: **0** (listed in the notes).
Rows whose labels array disagreed with the binary columns: **0**.

## sample composition

| bucket     |   n |
| ---------- | --: |
| fill       |  29 |
| rare       |  20 |
| rare-multi |  12 |
| none       |   9 |
| combo      |   5 |

| field              | distribution                                        |
| ------------------ | --------------------------------------------------- |
| stratum            | targeted 54, random 21                              |
| market             | UK 38, IN 23, US 14                                 |
| star rating        | 1 star 35, 2 star 14, 3 star 10, 4 star 7, 5 star 9 |
| distinct games     | 63                                                  |
| most from one game | 3 (cap 4)                                           |
| labels per review  | mean 1.37                                           |

## label coverage

| label                                        | pilot support | in sample | floor met |
| -------------------------------------------- | ------------: | --------: | :-------: |
| Temporal: Playing by Appointment             |            42 |         6 |    yes    |
| Temporal: Daily Rewards                      |            15 |         3 |    yes    |
| Temporal: Grinding                           |            20 |         5 |    yes    |
| Temporal: Advertisement                      |            23 |         9 |    yes    |
| Temporal: Infinite Treadmill                 |             4 |         2 |    yes    |
| Temporal: Mandatory Marathon                 |            13 |         4 |    yes    |
| Monetary: Pay to Progress                    |            93 |         8 |    yes    |
| Monetary: Intermediate Currency              |            25 |         6 |    yes    |
| Monetary: Deceptive Luxury                   |             4 |         2 |    yes    |
| Monetary: Recurring Fee                      |            10 |         2 |    yes    |
| Monetary: Gambling                           |            22 |         5 |    yes    |
| Monetary: Power Creep                        |             8 |         2 |    yes    |
| Monetary: Waste Aversion                     |            11 |         3 |    yes    |
| Monetary: Easy to Purchase                   |            15 |         2 |    yes    |
| Monetary: UI Misdirection                    |            15 |         3 |    yes    |
| Monetary: Never-Ending Lure                  |             2 |         2 |    yes    |
| Social: Forced Fellowship                    |            10 |         2 |    yes    |
| Social: Friend Spam / Impersonation          |             3 |         2 |    yes    |
| Social: Reciprocity                          |            17 |         4 |    yes    |
| Social: Encourages Anti-Social Behavior      |             4 |         2 |    yes    |
| Social: Fear of Missing Out (FOMO)           |             2 |         2 |    yes    |
| Social: Competition                          |            55 |         6 |    yes    |
| Psychological: Easy to Get, Hard to Lose     |             8 |         3 |    yes    |
| Psychological: Complete the Collection       |            19 |         2 |    yes    |
| Psychological: Illusion of Control           |            31 |         5 |    yes    |
| Psychological: Aesthetic Manipulation        |            10 |         2 |    yes    |
| Psychological: Optimism and Frequency Biases |             9 |         2 |    yes    |
| Psychological: Reward Mania                  |            39 |         5 |    yes    |
| Technical: Fragmented Downloads              |             2 |         2 |    yes    |

## notes

- read 2 file(s): `random.jsonl`, `targeted.jsonl`
- M_NeverEndingLure: needed multi-label reviews to reach the floor (+1 beyond the combo quota)
- S_FearOfMissingOutFOMO: needed multi-label reviews to reach the floor (+2 beyond the combo quota)
- S_FriendSpamImpersonation: needed multi-label reviews to reach the floor (+2 beyond the combo quota)
- M_DeceptiveLuxury: needed multi-label reviews to reach the floor (+2 beyond the combo quota)
- S_EncouragesAntiSocialBehavior: needed multi-label reviews to reach the floor (+2 beyond the combo quota)
- T_InfiniteTreadmill: needed multi-label reviews to reach the floor (+1 beyond the combo quota)
- M_PowerCreep: needed multi-label reviews to reach the floor (+1 beyond the combo quota)
- P_CompleteTheCollection: needed multi-label reviews to reach the floor (+1 beyond the combo quota)
