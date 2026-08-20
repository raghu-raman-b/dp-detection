# validation set — codebook v0.20

- seed: `20260812`  |  inputs: fsi.jsonl, minors.jsonl, random.jsonl, targeted_200.jsonl, targeted_2.jsonl, targeted.jsonl
- eligible pool: **541**  |  sampled: **75** (target 75)
- true-None: **9** (want 8-10)
- multi-label: **14** (want 4-5)
- from codebook (backfill): **1**  <- over the combo ceiling; coverage took priority

## filtering
- lines read: 620
- codebook examples held out of the pool: 67
- codebook worked examples rebuilt from the codebook text: 7
- dropped, uncoded: 0
- dropped, duplicate id / text: 6 / 0

## label coverage

| label | pilot support | in sample | floor met |
| --- | ---: | ---: | :---: |
| Temporal: Playing by Appointment | 49 | 7 | yes |
| Temporal: Daily Rewards | 20 | 4 | yes |
| Temporal: Grinding | 26 | 4 | yes |
| Temporal: Advertisement | 27 | 11 | yes |
| Temporal: Infinite Treadmill | 4 | 2 | yes |
| Temporal: Mandatory Marathon | 15 | 3 | yes |
| Monetary: Pay to Progress | 109 | 6 | yes |
| Monetary: Intermediate Currency | 28 | 4 | yes |
| Monetary: Deceptive Luxury | 4 | 2 | yes |
| Monetary: Recurring Fee | 10 | 2 | yes |
| Monetary: Gambling | 24 | 2 | yes |
| Monetary: Power Creep | 9 | 2 | yes |
| Monetary: Waste Aversion | 13 | 3 | yes |
| Monetary: Easy to Purchase | 19 | 2 | yes |
| Monetary: UI Misdirection | 15 | 2 | yes |
| Monetary: Never-Ending Lure | 5 | 2 | yes |
| Social: Forced Fellowship | 11 | 2 | yes |
| Social: Friend Spam / Impersonation | 6 | 2 | yes |
| Social: Reciprocity | 16 | 2 | yes |
| Social: Encourages Anti-Social Behavior | 7 | 2 | yes |
| Social: Fear of Missing Out (FOMO) | 1 | 2 | yes |
| Social: Competition | 54 | 4 | yes |
| Psychological: Easy to Get, Hard to Lose | 8 | 4 | yes |
| Psychological: Complete the Collection | 26 | 2 | yes |
| Psychological: Illusion of Control | 42 | 6 | yes |
| Psychological: Aesthetic Manipulation | 6 | 3 | yes |
| Psychological: Optimism and Frequency Biases | 10 | 2 | yes |
| Psychological: Reward Mania | 45 | 5 | yes |
| Technical: Fragmented Downloads | 5 | 3 | yes |

## notes

- dropped 6 review(s) appearing in more than one file (id collisions: 6, text collisions: 0)
- S_FearOfMissingOutFOMO: needed multi-label reviews to reach the floor (+1 beyond the combo quota)
- M_DeceptiveLuxury: needed multi-label reviews to reach the floor (+2 beyond the combo quota)
- P_AestheticManipulation: needed multi-label reviews to reach the floor (+2 beyond the combo quota)
- S_EncouragesAntiSocialBehavior: needed multi-label reviews to reach the floor (+1 beyond the combo quota)
- M_PowerCreep: needed multi-label reviews to reach the floor (+1 beyond the combo quota)
- M_UIMisdirection: needed multi-label reviews to reach the floor (+1 beyond the combo quota)
- S_FearOfMissingOutFOMO: pilot support 1 < floor; backfilled 1 codebook worked example(s)
- 1 review(s) came from the codebook and are marked `from_codebook: true` — coders have already seen these
