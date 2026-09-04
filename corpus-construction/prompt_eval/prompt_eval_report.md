# prompt-eval set

Built by `scripts/post-label/build_prompt_eval_set.py` from the adjudicated gold set, codebook v0.20, for prompt v3.

The reviews prompt v3 does **not** contain. Everything here is a strict subset of `gold_set/gold_set.jsonl`; no label was re-ruled to build it.

| | |
| --- | ---: |
| gold set | 75 |
| consumed as v3 worked examples | 45 |
| **prompt-eval set** | **30** |
| label instances | 33 of 137 |
| true-NONE reviews | 7 (23% of the set) |
| labels with any support | 16 of 29 |

## Read this before quoting a number from it

**13 of the 29 labels have zero support and cannot be scored at all.** That is not random attrition: every label with exactly two gold instances lost both, because both became its apt and coverage example in the prompt.

- zero support: `T_InfiniteTreadmill`, `M_RecurringFee`, `M_Gambling`, `M_PowerCreep`, `S_ForcedFellowship`, `S_FriendSpamImpersonation`, `S_EncouragesAntiSocialBehavior`, `S_FearOfMissingOutFOMO`, `P_EasyToGetHardToLose`, `P_CompleteTheCollection`, `P_AestheticManipulation`, `P_OptimismAndFrequencyBiases`, `Tech_FragmentedDownloads`
- exactly one instance: `T_Grinding`, `M_PayToProgress`, `M_DeceptiveLuxury`, `M_WasteAversion`, `M_NeverEndingLure`, `S_Competition`, `P_IllusionOfControl`

True-NONE is 23% of this set against 9% of the full gold set, so a model that under-labels is flattered here more than it would be there.

`runner_common.EVAL_SETS["prompt-eval"]` therefore sets `meso_macro: False`. Meso macro-F1 is **suppressed** on this arm rather than computed over the handful of labels that clear the support floor, because such a number reads as comparable to the validation figure and is not. Use micro-F1 and example-based F1.

## Files

| file | role |
| --- | --- |
| `prompt_eval_set_blind.jsonl` | given to the model; gold label columns stripped |
| `gold_set.jsonl` | scored against; labels copied verbatim from the adjudicated gold |
| `prompt_v3_example_ids.json` | the exclusion list, and why each id is on it |

Run it: `python run_teacher_openai.py --actual --eval-set prompt-eval --prompt ...`, then `python compute_run_stats.py --eval-set prompt-eval`. Output lands under `outputs/prompt-eval/`.

## Label support

| label | full gold | prompt-eval |
| --- | ---: | ---: |
| `T_PlayingByAppointment` | 7 | 3 |
| `T_DailyRewards` | 4 | 2 |
| `T_Grinding` | 5 | 1 |
| `T_Advertisement` | 9 | 5 |
| `T_InfiniteTreadmill` | 2 | 0 ⚠️ |
| `T_MandatoryMarathon` | 6 | 3 |
| `M_PayToProgress` | 11 | 1 |
| `M_IntermediateCurrency` | 8 | 3 |
| `M_DeceptiveLuxury` | 5 | 1 |
| `M_RecurringFee` | 2 | 0 ⚠️ |
| `M_Gambling` | 4 | 0 ⚠️ |
| `M_PowerCreep` | 2 | 0 ⚠️ |
| `M_WasteAversion` | 3 | 1 |
| `M_EasyToPurchase` | 5 | 2 |
| `M_UIMisdirection` | 8 | 4 |
| `M_NeverEndingLure` | 3 | 1 |
| `S_ForcedFellowship` | 2 | 0 ⚠️ |
| `S_FriendSpamImpersonation` | 2 | 0 ⚠️ |
| `S_Reciprocity` | 5 | 2 |
| `S_EncouragesAntiSocialBehavior` | 2 | 0 ⚠️ |
| `S_FearOfMissingOutFOMO` | 2 | 0 ⚠️ |
| `S_Competition` | 11 | 1 |
| `P_EasyToGetHardToLose` | 5 | 0 ⚠️ |
| `P_CompleteTheCollection` | 2 | 0 ⚠️ |
| `P_IllusionOfControl` | 5 | 1 |
| `P_AestheticManipulation` | 2 | 0 ⚠️ |
| `P_OptimismAndFrequencyBiases` | 3 | 0 ⚠️ |
| `P_RewardMania` | 10 | 2 |
| `Tech_FragmentedDownloads` | 2 | 0 ⚠️ |

## Composition

- **stratum**: random 12, targeted 18
- **market**: IN 8, UK 17, US 5
- **star_rating**: 1 14, 2 7, 3 2, 4 3, 5 4
- **distinct games**: 29 (most from one game: 2)
- **labels per review**: mean 1.10

## Reviews

| review_id | game | gold labels |
| --- | --- | --- |
| `ac5fc6a4-b597-46f3-af5a-3735b3854e26` | Gossip Harbor: Merge & Story | `M_EasyToPurchase`, `M_NeverEndingLure` |
| `47cb4d59-0121-40f1-9ffc-220c458bd581` | Seaside Escape®: Merge & Story | `M_WasteAversion` |
| `5e2d7a91-2181-4ad5-b5fb-cc1f50805d82` | Real Cricket™ | `T_Advertisement`, `M_UIMisdirection` |
| `991f5326-63fb-4951-8773-84050dd70912` | Candy Crush Soda Saga | `M_DeceptiveLuxury` |
| `6877b6bf-e9e0-4c86-a196-e7c85a51529f` | Candy Crush Saga | `M_UIMisdirection`, `S_Competition` |
| `eb67d840-0a90-4d5a-875b-2ff49975ea31` | Animals & Coins: Animal Run | `T_Advertisement` |
| `366f36fc-4496-4a46-a01e-dc43d4e20e11` | Bingo Voyage - Live Bingo Game | _NONE_ |
| `3db5f780-e8e1-44a1-b538-63120ac046a6` | Flambé®: Merge & Cook | _NONE_ |
| `3dc64fb0-3b6a-4ba1-9966-79c09f33069c` | Royal Kingdom | `M_UIMisdirection` |
| `549751b1-5735-41ac-94d3-d1bd62c47abf` | Coin Master | `T_DailyRewards` |
| `036954c0-447e-460d-b81e-f26f940b2ac4` | Shadow Fight 4: Arena | `T_MandatoryMarathon` |
| `7732d254-0a39-4614-acf4-e67840e14b76` | Cashman Casino Slots Games | `M_IntermediateCurrency`, `P_RewardMania` |
| `94246484-0b03-4247-91b7-a7b5e6c5ff5c` | Pokémon GO | `S_Reciprocity` |
| `2f50b132-9762-4f48-ae35-487f414aa41a` | MONOPOLY GO! | `S_Reciprocity`, `P_RewardMania` |
| `e19dc016-9f44-4e0e-bc04-d5198a837c4a` | Ludo King® | `P_IllusionOfControl` |
| `f112aad7-3ccd-4220-ae49-34d217dda09d` | Gardenscapes | `T_Grinding`, `T_MandatoryMarathon` |
| `01d62acd-a7ec-4bba-b0b7-1a0b600e8c04` | Coin Master - Board Adventure | _NONE_ |
| `40767241-e96d-4020-a23b-8e08eb00ea95` | Pixel Flow! | `T_Advertisement`, `M_UIMisdirection` |
| `42025004-6937-4657-ab75-72e97fe19166` | Lightning Link Casino Slots | `M_IntermediateCurrency`, `M_EasyToPurchase` |
| `ef1623a3-c6dd-4bff-b3a0-928b387776db` | Warhammer 40,000: Tacticus ™ | _NONE_ |
| `340ca9ea-754c-4fd9-ba70-70345a576196` | Free Fire MAX | _NONE_ |
| `10f3de40-f550-4205-b6fe-611aa3402917` | Cricket League | `T_Advertisement` |
| `bba96b29-914e-40d7-bc0d-49b352f54f85` | Whiteout Survival | `T_PlayingByAppointment` |
| `8b4092da-3c5a-41fa-8d14-16c5737e6b85` | Hitwicket™ Cricket Game 2026 | `T_MandatoryMarathon` |
| `e2a95947-be08-4077-ad5f-1e7891b9eff5` | MadOut 2: Grand Auto Racing | _NONE_ |
| `a472fc08-300a-44ba-bc93-910ff7dad18e` | Solitaire Grand Harvest | `T_PlayingByAppointment`, `M_PayToProgress`, `M_IntermediateCurrency` |
| `a1fa8982-758a-4925-adaf-52f14337dee1` | Zynga Poker ™ – Texas Holdem | `T_DailyRewards` |
| `201672d6-579d-44c3-a1df-55a3f8182969` | Travel Town - Merge Adventure | `T_PlayingByAppointment` |
| `6ccb26a7-01e3-41a3-ba1a-bddba2063257` | Lightning Link Casino Slots | _NONE_ |
| `5c0e0d12-6578-4169-ba24-c72a325799f1` | All in Hole: Black Hole Games | `T_Advertisement` |

