# Error review - gpt-5.6-luna_medium_teacher_v1

`gpt-5.6-luna` / reasoning `medium` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v1.txt` sha `e8cd52987c33`  
micro-F1 **0.824** (P 0.940 / R 0.733) - **20 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 4 | said NONE, gold had labels |
| SWAP | 3 | picked different labels than gold |
| MISSED ONLY | 12 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 1 | found all gold, added extras |

## The diagnostic that matters

Of **23** missed labels, **17** (74%) were named in the model's own analysis and dropped anyway; **6** (26%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `S_Competition` | 3 | 0 |
| `M_PayToProgress` | 2 | 1 |
| `M_IntermediateCurrency` | 2 | 1 |
| `M_WasteAversion` | 2 | 0 |
| `S_Reciprocity` | 2 | 0 |
| `P_AestheticManipulation` | 0 | 2 |
| `P_IllusionOfControl` | 1 | 0 |
| `T_Grinding` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `P_RewardMania` | 1 | 0 |
| `M_RecurringFee` | 0 | 1 |
| `M_Gambling` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |

## Missed everything (predicted NONE) (4)

### `0853c395-2040-4e0b-a56c-1591484cd35b` - Clash of Clans

> 10/10, but we would like: 1.) Bids & auctions for decorations, skins and sceneries with in-game currency. 2.) Remove the option to remove an obstacle if you've turned it into a decoration. 3.) Widget that can toggle various accounts and see how much time is left for upgrades. 4.) Hidden option for troops' advanced statistics.

| | labels |
|---|---|
| gold | `T_PlayingByAppointment` |
| pred | _NONE_ |
| **missed** | `T_PlayingByAppointment` |

**Did the model consider what it missed?**

- `T_PlayingByAppointment` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review consists of requests for auctions, changing obstacle removal, an account-toggle widget, and hidden troop statistics. Under R12, proposed features do not trigger labels. The mention of upgrade time remaining does not explicitly describe a player-imposed wait or a penalty for failing to play, so T_PlayingByAppointment is rejected under its boundary rule. No other current game mechanic is clearly described.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b580a4c7-3c75-493e-ad3b-03b4f2bde6a5` - Pokémon GO

> This new update have many bugs. 1)I can't open any gifts or trade with friends without the keep on crashing, 2) when click on a pokemon I can't even throw the pokeball with all the lagging, 3) the pvp & rockets battles are also lagging switching out are too slow, charge attacks are not responding well and my game freeze while the opponent keep attacking. Please fix these problems!

| | labels |
|---|---|
| gold | `S_Competition`, `S_Reciprocity` |
| pred | _NONE_ |
| **missed** | `S_Competition`, `S_Reciprocity` |

**Did the model consider what it missed?**

- `S_Competition` - considered and rejected -> **rule interpretation**
- `S_Reciprocity` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review attributes all described problems to bugs, crashing, lag, and freezing, so the specific behaviors are technical faults rather than deliberate design choices under R11. It mentions gifts, trading, and PvP, but does not describe social obligation, resource reciprocity, or competition as a design pattern; the focus is that those features malfunction. No label applies.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `490ca53d-66fe-44b0-928f-ea2ba6682f0b` - Clash of Clans

> Since 1 of the updates I can no longer request troops from my clan. It needs to be fixed.

| | labels |
|---|---|
| gold | `S_Reciprocity` |
| pred | _NONE_ |
| **missed** | `S_Reciprocity` |

**Did the model consider what it missed?**

- `S_Reciprocity` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes an inability to request troops from the clan, but explicitly attributes it to an update problem and asks for it to be fixed. Under R11, a social resource-transfer mechanic attributed to a bug or technical fault is not labeled; therefore Reciprocity is rejected. No other mechanic is described.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `8d13a3c1-1982-45db-a2b4-07c61c41ba2a` - Pixel Flow!

> this WAS a favorite game and WAS fun until it became unplayable. stuck on level 195 for almost 2 months. getting ready to uninstall it. I refuse to pay for power ups. should be daily login rewards to help with these harder levels.

| | labels |
|---|---|
| gold | `M_PayToProgress` |
| pred | _NONE_ |
| **missed** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_PayToProgress` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes being stuck on one level for almost two months and refusing to pay for power-ups, but it does not explicitly describe repetitive tasks, a game-wide unattainable end state, or payment as a requirement for progress. The requested daily login rewards are hypothetical and not currently present, so R12 excludes T_DailyRewards. No applicable mechanic label is supported.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (3)

### `fd1230ab-7d12-4aeb-a425-e37ed06bcd5c` - Pokémon GO

> I love this game, just started playing about 2 months ago. Though I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way. I feel taken advantage of. 3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| pred | `M_PayToProgress`, `S_FriendSpamImpersonation` |
| **missed** | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `P_IllusionOfControl` - considered and rejected -> **rule interpretation**
- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes capture attempts consuming Poké Balls unusually quickly, leading the player to purchase more in order to continue capturing, which supports Pay to Progress. The later statement says the review was posted under the player's identity without being written by them, supporting Friend Spam / Impersonation. Intermediate Currency is rejected because Poké Balls are purchased items, not in-game currency. Gambling and Illusion of Control are rejected because no explicit chance-based monetary stake or rigging mechanism is described.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "so I go through the balls faster so I have to purchase more"
  - why: The described resource depletion makes purchasing additional Poké Balls necessary to continue the capture activity.
- `S_FriendSpamImpersonation` - ok
  - span: "I DID NOT WRITE THIS REVIEW"
  - why: The player explicitly states that a review was written under their identity without their authorship.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fdef27f2-9a21-4b8e-a04c-7a4753e0fb07` - 8 Ball Pool

> The game is great, but the user interface is completely rigged. Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins and are forced to buy real ones. ​We need a "Default Table Lock" or the game should always open the lowest bet table by default, not the highest! Fix this scammy feature. Giving 1 star

| | labels |
|---|---|
| gold | `M_Gambling`, `M_IntermediateCurrency`, `M_UIMisdirection` |
| pred | `M_PayToProgress`, `M_UIMisdirection` |
| **missed** | `M_Gambling`, `M_IntermediateCurrency` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_Gambling` - considered and rejected -> **rule interpretation**
- `M_IntermediateCurrency` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a deliberate interface default that automatically scrolls to and selects the highest-bet table, causing accidental mis-clicks and loss of coins. This satisfies UI Misdirection because the interface directs the player toward a costly option and away from the safer lowest-bet option. The review also states that losing coins forces players to buy replacements, which describes spending money to continue playing and supports Pay to Progress. Intermediate Currency was considered but rejected because the review does not explicitly state that real money is exchanged for in-game coins; it only says players are forced to buy 'real ones.' Easy to Purchase was rejected because the accidental selection concerns an in-game betting table, not a real-money purchase interface. Gambling was rejected because no chance-based mechanic is described.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: The review describes losing the resource needed to play and being forced to spend money to replace it.
- `M_UIMisdirection` - ok
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins"
  - why: The interface automatically directs and defaults the player to the highest-cost betting option.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b93c432d-19c0-4c6c-a2d4-bb9b21a436f3` - Dice Dreams™️

> A literal brain-rot game no wonder why they're tryna promote it through Free Cash. Also if you're thinking of making in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates! A real SCAM. Play it if u want but there are games that are actually good also, DON'T GET IN-APP PURCHASES!

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_PayToProgress`, `P_CompleteTheCollection`, `P_RewardMania` |
| **missed** | `P_AestheticManipulation` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes an in-app purchase made to obtain new cards toward completing an album and earning its grand prize, but the purchase delivered duplicate cards instead. This supports Pay to Progress because payment was used to advance album completion, Reward Mania because the card delivery produced unwanted duplicates, and Complete the Collection because the reviewer was pursuing the final cards and album prize. Gambling is rejected under its boundary rule because the review does not explicitly describe a chance mechanic or wager. The mention of promotion through Free Cash is out-of-game advertising and is excluded by R13; it does not trigger Advertisement.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "i bought a deal which promised i would get NEW cards"
  - why: The reviewer paid for cards intended to advance progress toward completing the album.
- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The span explicitly describes pursuing the remaining cards needed to complete an album and claim its prize.
- `P_RewardMania` - ok
  - span: "i bought a deal which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: The purchased card delivery produced unwanted duplicates, describing a reward system based on repeated randomized drops.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (12)

### `0bc09fc3-6436-4a24-855e-0fdc56887918` - Fishdom

> EDIT 1/17/2023: Customer Service can't make good on 9 diamonds when game element doesn't appear within 5 original moves and 5 additional moves. It is a fun game, you don't have to pay to win. I suggest after this cust. svc experience that you don't buy from this game beyond the pass.Get friends and a team and trade lives.

| | labels |
|---|---|
| gold | `M_RecurringFee`, `S_Reciprocity` |
| pred | `S_Reciprocity` |
| **missed** | `M_RecurringFee` |

**Did the model consider what it missed?**

- `M_RecurringFee` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes trading lives with friends and a team, which is a resource-exchange mechanic. The mention of 9 diamonds does not describe real money being converted into currency, a wager, or a purchase prompt. The statement that the player does not have to pay to win is evaluative and does not establish Pay to Progress. Mention of a pass is too vague to establish a recurring-fee mechanic under R2.
```

**Labels assigned**

- `S_Reciprocity` - ok
  - span: "Get friends and a team and trade lives"
  - why: This explicitly describes exchanging in-game lives with other players.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `549e5e94-9b59-477d-88c7-ae5e00d62514` - Disney Solitaire

> it was fine at the start but further along into the game the rng is so obviously against you it's crazy.. it's not rewarding playing the game without spending actual money.. at around level 100 it costs 2200 but if you win the level you'll barely make that back.. the rewards need a big revamp for me.. let down by alot of things with this game the further into it you get.. sort it out

| | labels |
|---|---|
| gold | `M_PayToProgress`, `P_IllusionOfControl` |
| pred | `P_IllusionOfControl` |
| **missed** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_PayToProgress` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes RNG as being manipulated against the player, which satisfies Illusion of Control under the alleged-rigging boundary. It also mentions spending actual money and a 2200 level cost, but does not clearly state that payment is required to advance; the complaint focuses on poor rewards and an unfavorable return, so Pay to Progress is rejected under R2. Reward Mania is rejected because no unpredictable reward-delivery system is described, and Waste Aversion is rejected because no stranded currency, forfeited value, or concrete purchase shortfall is shown.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "the rng is so obviously against you"
  - why: The reviewer asserts that the game manipulates RNG outcomes against the player, describing alleged rigging.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `33c422de-1a84-4df9-accd-cdf8bfc96295` - Dark War Survival

> No ingenuity for a base builder. Same old same old grinder. After a few weeks, it became abundantly clear that there is absolutely no opportunity for a general player to win an event. Zero skill pay to play. Zero skill pay to win. Calculated total spent on last event was 30k to win. Wish serious gamers would stop perpetuating the problem by continuing to spend obnoxious amounts of money on a little app that you just want to have a little fun on.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `S_Competition` |
| pred | `M_PayToProgress` |
| **missed** | `S_Competition` |

**Did the model consider what it missed?**

- `S_Competition` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a pay-to-win/pay-to-play event structure, including spending money to win, which satisfies M_PayToProgress through the Pay to Win indicator. I considered T_Grinding because it calls the game a “grinder,” but no specific repetitive activity required for progress is named, so it is rejected under the Grinding boundary rule. I rejected S_Competition because the review does not explicitly describe players competing against one another, and rejected M_Gambling because no chance-based mechanic or wager is described.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Zero skill pay to win."
  - why: This explicitly describes payment granting an advantage needed to win, satisfying the Pay to Win indicator.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b2dc0bc8-8ebe-4c48-bc05-38d0d65acb84` - Last War:Survival Game

> It's a nice game, but it's set up in a pay to win way. I played for 10 days, and the update times for your base are becoming ridiculous. Everything scales endlessly, there is kinda no point to look forward to, just more grind. The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff. Alliances are also weird, with the top ones dictating what to develop, what to rush, etc. If you are not in one then you get attacked and bullied. Not a great experience.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_UIMisdirection`, `S_Competition`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| pred | `M_PayToProgress`, `M_UIMisdirection`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| **missed** | `S_Competition` |

**Did the model consider what it missed?**

- `S_Competition` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes spending money giving gameplay advantages, so M_PayToProgress applies. "Update times for your base" describes imposed upgrade timers, triggering T_PlayingByAppointment. "Everything scales endlessly" together with having no endpoint supports T_InfiniteTreadmill, while "just more grind" is only a general evaluation without a named repetitive activity, so T_Grinding is rejected under its boundary rule. The deliberately confusing UI is explicitly said to make players buy things, triggering M_UIMisdirection; it does not describe a misleading question or emotional/aesthetic manipulation, so P_AestheticManipulation is rejected. The alliance behavior describes coercive protection through grouping, but the Forced Fellowship boundary excludes compelled grouping without recruitment incentives or an obligation to avoid letting group members down. No Competition or EncouragesAntiSocialBehavior label is assigned because competition or a reward for bullying is not explicitly described.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "it's set up in a pay to win way"
  - why: This describes spending as a way to obtain an in-game advantage.
- `M_UIMisdirection` - ok
  - span: "The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff"
  - why: The interface is described as intentionally confusing players to steer them toward purchases.
- `T_InfiniteTreadmill` - ok
  - span: "Everything scales endlessly"
  - why: Endless scaling describes progression that continually expands without an attainable completion point.
- `T_PlayingByAppointment` - ok
  - span: "the update times for your base are becoming ridiculous"
  - why: Base updates impose in-game timers that make the player wait before progressing.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `3c46f5e0-6091-43dc-94a0-e3af3259a63d` - Cashman Casino Slots Games

> Resently cashman had changed it's bingo rewards and daily rewards. However lve found that I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards. The most I can seem to get on the timed rewards is 40,000. I'd not pay just to get my daily rewards. So I'm deleting them.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_WasteAversion`, `T_DailyRewards` |
| pred | `T_DailyRewards` |
| **missed** | `M_PayToProgress`, `M_WasteAversion` |

**Did the model consider what it missed?**

- `M_PayToProgress` - considered and rejected -> **rule interpretation**
- `M_WasteAversion` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a daily reward system that cannot be completed unless the player bets 50,000, with timed rewards providing at most 40,000. This triggers T_DailyRewards because the daily reward opportunity is conditioned on completing a daily requirement. T_PlayingByAppointment is rejected because no wait or real-time progression gate is described, and the daily cycle gates a reward rather than overall game progression. M_Gambling is rejected because the review does not explicitly describe real-money or paid currency being wagered. M_PayToProgress and M_WasteAversion are rejected because payment and a realized leftover or forfeited value are not clearly described as mechanics.
```

**Labels assigned**

- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The daily rewards require completion of a daily betting requirement, making the reward conditional on returning and meeting that daily task.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `cc714d17-863c-4ebd-b14f-989ba17c71c4` - Dice Dreams™️

> I played this game on a different profile. the only reason I gave it five stars is because if you don't it won't let you write a review. if you want to win anything on this game it will cost hundreds of dollars. on the stickers you will never get the last one or two unless you pay a lot of money to get them. this is not a game you want to get addicted to unless you have a endless bank account. it may let you complete a goal maybe one out of hundred times.dont get your hopes up.

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury`, `M_PayToProgress`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_DeceptiveLuxury`, `M_PayToProgress`, `P_CompleteTheCollection` |
| **missed** | `P_RewardMania` |

**Did the model consider what it missed?**

- `P_RewardMania` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes payment being needed to obtain the final stickers and complete the sticker goal, supporting Pay to Progress and Complete the Collection. The same span describes the last stickers as effectively withheld unless the player pays, supporting Deceptive Luxury under artificial scarcity tied to purchase. The forced five-star review condition is outside the game application under R13. The statements about winning rarely and addiction do not name a sufficiently clear chance-based reward mechanic, so Gambling, Reward Mania, and other labels are rejected under R2 and R4.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "you will never get the last one or two unless you pay a lot of money to get them"
  - why: The final stickers are described as artificially scarce, with their scarcity affecting the purchase needed to obtain them.
- `M_PayToProgress` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: The review says payment is required to obtain the final stickers and advance toward completion.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two"
  - why: The span describes pursuing the remaining stickers needed to complete the collection.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `ab2097d3-2f9b-4a87-885c-25dfcddb5a70` - Gardenscapes

> Have been playing this game since COVID 19 lockdown. It was fun back then. Currently at 8416 and it gets frustratingly annoying after level 8000. I run out of lives 3-4 times daily to beat every alternate level, avg 5-7 days per level. You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying. Now I'm not interested anymore. Unistalling this game to invest some quality time in a real life. Wasted too much of money and time into this game.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `T_Grinding` |
| pred | `M_PayToProgress` |
| **missed** | `T_Grinding` |

**Did the model consider what it missed?**

- `T_Grinding` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes payment as necessary to get through the game, which satisfies Pay to Progress. The slow pace and running out of lives do not by themselves establish Grinding because no repetitive activity is explicitly named, and they do not establish Playing by Appointment because no timer or regeneration schedule is described. The reviewer says they are uninstalling, so wasted time and money do not show reluctance to abandon accumulated investment for Easy to Get, Hard to Lose. No collection, chance, competition, advertising, or other coded mechanic is described.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through"
  - why: The span explicitly states that purchasing add-ons is required to progress through the game.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `176aaa1f-d8f9-4a1a-9f29-64902f13be5c` - All in Hole: Black Hole Games

> I would give 5 stars, but I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used.🤨😒🙄😥

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `T_MandatoryMarathon` |
| pred | `T_MandatoryMarathon` |
| **missed** | `M_IntermediateCurrency` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes leaving the game and returning to find the previously held bag contents and coins gone, indicating that exiting or stopping a session results in forfeiting accumulated holdings. This supports Mandatory Marathon. Easy to Get, Hard to Lose was considered but rejected because the review does not describe reluctance to quit or leaving being made costly as a retention mechanism. Waste Aversion was rejected because it does not describe a specific currency shortfall, leftover currency, or inventory-capacity tradeoff.
```

**Labels assigned**

- `T_MandatoryMarathon` - ok
  - span: "I would give 5 stars, but I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used."
  - why: Leaving the game causes accumulated bag contents and coins to be forfeited, indicating that stopping a session results in loss of held value.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `45e3e2f0-4612-4d60-9312-3bff055ec9f3` - Merge Cooking®

> I really enjoyed this game until I got to a higher level. About to quit at level 34. Not enough slots to store and play without spending $$ to buy parts. I have 63 spots, on the board and 37 spots in the refrigerator. 98 spaces total, 72 are taken up by parts of generators or lower generators that I can't merge with higher generators yet or high level items like a corn that I am not going to delete. A lambchop can take up to 9 spaces or more of my 26 spaces and I'm not deleting the chicken pie

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_WasteAversion` |
| pred | `M_PayToProgress` |
| **missed** | `M_WasteAversion` |

**Did the model consider what it missed?**

- `M_WasteAversion` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes inventory/storage capacity becoming insufficient, with occupied slots and valuable items they will not delete, and says spending money to buy parts is needed to continue playing. This supports Pay to Progress because payment is presented as necessary to keep playing. Waste Aversion was considered but rejected under its boundary rule because the review does not state that currency or items were actually forfeited, destroyed, or left unusable due to the capacity limit. Grinding, Easy to Get Hard to Lose, and other labels are not supported by an explicitly described mechanic.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Not enough slots to store and play without spending $$ to buy parts."
  - why: The span states that spending money to buy parts is required to continue playing.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `12267c1e-47ba-4984-97c8-768e820ceb1c` - Bingo Blitz™️ - Bingo Games

> not very user-friendly. no apparent reachable goals within a decent amount of time. I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| pred | `M_EasyToPurchase`, `P_CompleteTheCollection`, `T_Grinding` |
| **missed** | `P_AestheticManipulation` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes repetitive rounds undertaken to collect photos and complete a set, supporting T_Grinding and P_CompleteTheCollection. It also describes a purchase prompt appearing after a lost round and asking the player to spend extra coins, supporting M_EasyToPurchase because the prompt directly intercepts play. I rejected M_Gambling because the span does not clearly describe a chance-based reward purchased with real money or wagered currency; M_IntermediateCurrency because it does not explicitly describe real money being converted into coins; M_WasteAversion because the loss is a failed promised transaction rather than stranded or insufficient currency; and M_PayToProgress because payment is not clearly stated as required for continued progression.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "after each round that I lose it will ask me if I want to spend extra coins"
  - why: A purchase prompt is presented immediately after a loss, directly intercepting the player's gameplay.
- `P_CompleteTheCollection` - ok
  - span: "collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set"
  - why: The span explicitly describes acquiring missing photos to complete a set.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The player performs repeated rounds to pursue progress toward collecting photos.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `73423b22-395c-49ed-8fc3-488a0b7680df` - MONOPOLY GO!

> I like the game but frustrating when it comes to getting stickers. always get duplicates. never lets you finish all the sets unless you pay

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury`, `M_PayToProgress`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_PayToProgress`, `P_CompleteTheCollection`, `P_RewardMania` |
| **missed** | `M_DeceptiveLuxury` |

**Did the model consider what it missed?**

- `M_DeceptiveLuxury` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes collecting stickers and being repeatedly given duplicates, which is a randomized or unwanted reward-delivery pattern and a compulsion to complete sets. It also explicitly says completion is blocked unless the player pays, satisfying Pay to Progress. Gambling is rejected because no paid wager or explicit monetary chance mechanic is described. Deceptive Luxury is rejected because no artificial scarcity, limited-time restriction, or rarity-based pricing is stated.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: The review explicitly states that completing the game’s sets requires payment.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: This directly describes the goal of completing all collectible sets.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: Repeated duplicate sticker drops describe unwanted or unpredictable delivery from a reward pool.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `7b564746-b769-4856-b686-529f8717c3ba` - Candy Crush Soda Saga

> I like the game except: 1. I was charged 10 gold pcs for 5 moves, I had 2 moves left. I had 7 moves but only used 1 move. 2. I paid for a pkg unlimited lives ect. I got the etc. but not the lives. 3. The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone. 4. You cannot win enough gold to play without buying sometimes. 5. The packages need to cost less. 6. When I buy pkg should not be timed.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `M_PayToProgress`, `T_PlayingByAppointment` |
| pred | `M_PayToProgress`, `T_PlayingByAppointment` |
| **missed** | `M_IntermediateCurrency` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a timed bonus that decreases while the player is away, so T_PlayingByAppointment applies because rewards expire on the game's clock. It also states that the player sometimes cannot play without buying, which is a payment-linked progression barrier and triggers M_PayToProgress. I rejected M_IntermediateCurrency because the review does not clearly describe real money being converted into gold; merely spending or being charged gold is insufficient. The missing unlimited lives are attributed to a purchase not being delivered, with no deliberate mechanic described, so R11 suppresses labels for that span. Package prices and the request that packages not be timed do not independently identify a qualifying mechanic.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The review explicitly says purchasing is sometimes necessary to continue playing.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone."
  - why: Timed rewards expire while the player is away, imposing a game-controlled clock on their availability.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (1)

### `a2ece36d-c527-442d-8f18-9a16b63994c8` - War Robots Multiplayer Battles

> Its a p2w game. The only time you enjoy it is when you're new. As you progress, everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game. If you want to progress without paying money, goodluck! Even if you wanted to do f2p, you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it. Plus the only time you benofit by getting f2p rewards is ads... 💩

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `M_PayToProgress`, `M_PowerCreep`, `T_Advertisement` |
| pred | `M_EasyToPurchase`, `M_PayToProgress`, `M_PowerCreep`, `S_FearOfMissingOutFOMO`, `T_Advertisement` |
| **spurious** | `S_FearOfMissingOutFOMO` |

**Model analysis**

```
The review describes purchase prompts that block access to gameplay, payment being required for progression and competitive advancement, newer bots replacing the value of older meta options, pressure to keep up with the shifting meta, and ads as the route to free-to-play rewards. I considered T_Grinding, but no repetitive task is named; S_Competition, but no direct player-versus-player competition mechanic is described; M_IntermediateCurrency, because no purchasable in-game currency is mentioned; and M_UIMisdirection, because the review does not describe attention-directing visuals or obstructed opt-out controls.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game"
  - why: Purchase offers appear before gameplay and must be dealt with before the player can play, directly intercepting gameplay.
- `M_PayToProgress` - ok
  - span: "you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it"
  - why: The review states that money must be spent on the newest bot to maintain advancement rather than earning it.
- `M_PowerCreep` - ok
  - span: "keep up with shifting meta where you have to buy the newest bot with money instead of earning it"
  - why: Shifting meta and the need to buy the newest bot indicate that newer releases diminish the value of older options.
- `S_FearOfMissingOutFOMO` - **SPURIOUS**
  - span: "would not be able to keep up with shifting meta"
  - why: The player is pressured by the prospect of falling behind the game's changing meta.
- `T_Advertisement` - ok
  - span: "the only time you benofit by getting f2p rewards is ads"
  - why: The span describes ads as the means through which the player receives free-to-play rewards, indicating incentivized ad viewing.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_PayToProgress` | 3 | 3 |
| `S_Competition` | 3 | 0 |
| `M_IntermediateCurrency` | 3 | 0 |
| `M_WasteAversion` | 2 | 0 |
| `S_Reciprocity` | 2 | 0 |
| `P_AestheticManipulation` | 2 | 0 |
| `P_IllusionOfControl` | 1 | 0 |
| `S_FearOfMissingOutFOMO` | 0 | 1 |
| `T_Grinding` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `M_RecurringFee` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `P_RewardMania` | 1 | 0 |
| `M_Gambling` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |

