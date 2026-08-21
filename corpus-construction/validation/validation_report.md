# validation set, codebook v0.20

- seed: `20260812`  |  input folder: `../labeled_data/`
- output: `../validation/validation_set.jsonl`
- eligible pool: **548**  |  sampled: **75** (target 75)
- true-None: **9** (want 8-10)
- multi-label: **17** (want 4-5)  <- over the ceiling, label coverage took priority
- codebook example ids indexed: **63**

## line accounting

| outcome | lines |
| --- | ---: |
| blank | 0 |
| unparseable JSON | 0 |
| no review_id | 0 |
| codebook example, excluded | 66 |
| repeat of an earlier review_id, collapsed | 6 |
| uncoded | 0 |
| eligible pool | 548 |
| **total lines read** | **620** |

Sum of outcomes: 620

Repeats whose labels differed from the copy that was kept: **0** (listed in the notes).
Rows whose labels array disagreed with the binary columns: **0**.

## sample composition

| bucket | n |
| --- | ---: |
| fill | 29 |
| rare | 20 |
| rare-multi | 12 |
| none | 9 |
| combo | 5 |

| field | distribution |
| --- | --- |
| stratum | targeted 57, random 18 |
| market | UK 41, IN 21, US 13 |
| star rating | 1 star 28, 2 star 13, 3 star 14, 4 star 9, 5 star 11 |
| distinct games | 65 |
| most from one game | 3 (cap 4) |
| labels per review | mean 1.33 |

## label coverage

| label | pilot support | in sample | floor met |
| --- | ---: | ---: | :---: |
| Temporal: Playing by Appointment | 50 | 5 | yes |
| Temporal: Daily Rewards | 20 | 5 | yes |
| Temporal: Grinding | 25 | 4 | yes |
| Temporal: Advertisement | 26 | 10 | yes |
| Temporal: Infinite Treadmill | 4 | 2 | yes |
| Temporal: Mandatory Marathon | 15 | 3 | yes |
| Monetary: Pay to Progress | 110 | 6 | yes |
| Monetary: Intermediate Currency | 28 | 5 | yes |
| Monetary: Deceptive Luxury | 4 | 2 | yes |
| Monetary: Recurring Fee | 10 | 2 | yes |
| Monetary: Gambling | 25 | 2 | yes |
| Monetary: Power Creep | 9 | 2 | yes |
| Monetary: Waste Aversion | 13 | 3 | yes |
| Monetary: Easy to Purchase | 20 | 3 | yes |
| Monetary: UI Misdirection | 16 | 2 | yes |
| Monetary: Never-Ending Lure | 5 | 2 | yes |
| Social: Forced Fellowship | 11 | 3 | yes |
| Social: Friend Spam / Impersonation | 3 | 2 | yes |
| Social: Reciprocity | 17 | 3 | yes |
| Social: Encourages Anti-Social Behavior | 7 | 2 | yes |
| Social: Fear of Missing Out (FOMO) | 2 | 2 | yes |
| Social: Competition | 57 | 7 | yes |
| Psychological: Easy to Get, Hard to Lose | 8 | 2 | yes |
| Psychological: Complete the Collection | 26 | 3 | yes |
| Psychological: Illusion of Control | 42 | 7 | yes |
| Psychological: Aesthetic Manipulation | 10 | 2 | yes |
| Psychological: Optimism and Frequency Biases | 10 | 2 | yes |
| Psychological: Reward Mania | 47 | 5 | yes |
| Technical: Fragmented Downloads | 5 | 2 | yes |

## notes

- read 6 file(s): `fsi.jsonl`, `minors.jsonl`, `random.jsonl`, `targeted.jsonl`, `targeted_2.jsonl`, `targeted_200.jsonl`
- S_FearOfMissingOutFOMO: needed multi-label reviews to reach the floor (+2 beyond the combo quota)
- S_FriendSpamImpersonation: needed multi-label reviews to reach the floor (+2 beyond the combo quota)
- M_DeceptiveLuxury: needed multi-label reviews to reach the floor (+2 beyond the combo quota)
- S_EncouragesAntiSocialBehavior: needed multi-label reviews to reach the floor (+1 beyond the combo quota)
- M_PowerCreep: needed multi-label reviews to reach the floor (+2 beyond the combo quota)
- P_AestheticManipulation: needed multi-label reviews to reach the floor (+1 beyond the combo quota)
- P_OptimismAndFrequencyBiases: needed multi-label reviews to reach the floor (+1 beyond the combo quota)
- M_UIMisdirection: needed multi-label reviews to reach the floor (+1 beyond the combo quota)
