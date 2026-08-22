# Error review - gpt-5.6-luna_medium_teacher_v2_full

`gpt-5.6-luna` / reasoning `medium` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `6529a474a2b0`  
micro-F1 **0.835** (P 0.917 / R 0.767) - **18 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 5 | said NONE, gold had labels |
| SWAP | 3 | picked different labels than gold |
| MISSED ONLY | 8 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 2 | found all gold, added extras |

## The diagnostic that matters

Of **20** missed labels, **6** (30%) were named in the model's own analysis and dropped anyway; **14** (70%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `M_PayToProgress` | 2 | 1 |
| `T_Grinding` | 2 | 0 |
| `S_Reciprocity` | 0 | 2 |
| `M_DeceptiveLuxury` | 0 | 2 |
| `S_Competition` | 1 | 1 |
| `P_AestheticManipulation` | 0 | 2 |
| `M_Gambling` | 1 | 0 |
| `M_WasteAversion` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `P_RewardMania` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `M_IntermediateCurrency` | 0 | 1 |
| `M_EasyToPurchase` | 0 | 1 |

## Missed everything (predicted NONE) (5)

### `0853c395-2040-4e0b-a56c-1591484cd35b` - Clash of Clans

> 10/10, but we would like: 1.) Bids & auctions for decorations, skins and sceneries with in-game currency. 2.) Remove the option to remove an obstacle if you've turned it into a decoration. 3.) Widget that can toggle various accounts and see how much time is left for upgrades. 4.) Hidden option for troops' advanced statistics.

| | labels |
|---|---|
| gold | `T_PlayingByAppointment` |
| pred | _NONE_ |
| **missed** | `T_PlayingByAppointment` |

**Did the model consider what it missed?**

- `T_PlayingByAppointment` - never mentioned -> **attention / recall**

**Model analysis**

```
The review gives a positive rating and then lists requested or hypothetical features: auctions using in-game currency, changing the behavior of decorated obstacles, an account-switching and upgrade-time widget, and hidden troop statistics. These are suggestions rather than descriptions of dark-pattern mechanics currently operating in the game. The mention of upgrade time remaining implies upgrade timers may exist, but it does not describe a wait imposed on the player or any other codable pattern. No label is supported.
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

- `S_Competition` - never mentioned -> **attention / recall**
- `S_Reciprocity` - never mentioned -> **attention / recall**

**Model analysis**

```
The review attributes every described problem to bugs, crashing, lag, freezing, or unresponsive controls after an update. Opening gifts, trading with friends, catching Pokémon, PvP and Rocket battles are mentioned only as activities disrupted by these technical faults, not as deliberate game-design behaviors. The opponent continuing to attack occurs while the game is frozen, so it is also part of the malfunction account rather than an intentional competitive mechanic. Under R11, no dark-pattern label is supported.
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

- `S_Reciprocity` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes being unable to request troops from their clan after an update and explicitly attributes this behavior to a problem that needs fixing. Although requesting troops could otherwise indicate a resource-exchange mechanic, the review presents it as a technical fault rather than an active game design behavior, so R11 suppresses dark-pattern labels.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fdfb3f26-0573-4cac-a0e2-ea5571bb5ad2` - Evony: The King's Return

> The ads for this game capitalize on the puzzles as if the whole game is about solving the physics puzzles. The reality is that this is an extremely involved strategy game that has, once in a while, a puzzle like those shown in the ads. If you like making an army from scratch, training, building, gathering resources then you may like this game. If you expected puzzles such as those in the ads for this game, you'll be doing chores in order to get to them.

| | labels |
|---|---|
| gold | `T_Grinding` |
| pred | _NONE_ |
| **missed** | `T_Grinding` |

**Did the model consider what it missed?**

- `T_Grinding` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review contrasts misleading third-party advertisements with the actual in-game experience. The ad claims are outside the installed game's design and therefore do not trigger T_Advertisement under R13. Inside the game, the reviewer describes army creation, training, building, and resource gathering as chores needed to reach the occasional puzzle, but does not explicitly describe these activities as repeated or performed over and over for progress. That is insufficient for T_Grinding, and no other listed mechanic is clearly established.
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

- `M_PayToProgress` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes being unable to pass one level for almost two months and considering uninstalling. This is a single blocked level, not evidence that the game continually expands beyond completion, so it does not support Infinite Treadmill. The reviewer refuses to pay for power-ups, but does not explicitly state that payment is required or that paying would enable progress, so Pay to Progress is not established. Daily login rewards are requested as a hypothetical feature rather than described as currently present, so Daily Rewards is not coded. No other current mechanic meets the codebook criteria.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (3)

### `fd1230ab-7d12-4aeb-a425-e37ed06bcd5c` - Pokémon GO

> I love this game, just started playing about 2 months ago. Though I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way. I feel taken advantage of. 3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| pred | `M_PayToProgress`, `P_IllusionOfControl`, `S_FriendSpamImpersonation` |
| **missed** | `P_OptimismAndFrequencyBiases` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a capture mechanic in which Poké Balls are consumed when Pokémon break out, and the reviewer believes that after purchasing Poké Balls, breakouts happen more often, forcing additional purchases. This supports Pay to Progress because continued capturing is presented as requiring more purchased resources, and Illusion of Control because the reviewer alleges that the game manipulates capture outcomes after purchase. The final edit states that the review itself was not written by the account holder and that the claimed conversations with other players did not occur, implying an unauthorized review posted through the player's identity, which supports Friend Spam / Impersonation. The review does not describe real money being converted into currency, a chance-based monetary wager, or a reward-delivery system.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "so I go through the balls faster so I have to purchase more"
  - why: The reviewer says the game consumes Poké Balls faster and thereby makes further purchases necessary to continue capturing.
- `P_IllusionOfControl` - ok
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out"
  - why: The reviewer alleges that capture outcomes became manipulated after purchasing Poké Balls, asserting that the game determines results in a concealed or unfair way.
- `S_FriendSpamImpersonation` - ok
  - span: "I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE"
  - why: The edit says the review and its claims were not authored by the account holder, implying that content was posted through the player's identity without consent.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fdef27f2-9a21-4b8e-a04c-7a4753e0fb07` - 8 Ball Pool

> The game is great, but the user interface is completely rigged. Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins and are forced to buy real ones. ​We need a "Default Table Lock" or the game should always open the lowest bet table by default, not the highest! Fix this scammy feature. Giving 1 star

| | labels |
|---|---|
| gold | `M_Gambling`, `M_IntermediateCurrency`, `M_UIMisdirection` |
| pred | `M_IntermediateCurrency`, `M_PayToProgress`, `M_UIMisdirection`, `S_Competition` |
| **missed** | `M_Gambling` |
| **spurious** | `M_PayToProgress`, `S_Competition` |

**Did the model consider what it missed?**

- `M_Gambling` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes an in-game interface that automatically scrolls to and selects the most expensive available 1v1 betting table, rather than leaving the player at a neutral or low-cost choice. This is UI Misdirection because the interface directs the player toward a costly option and creates accidental mis-click risk. The table entry uses coins, and the reviewer says losing those coins forces players to buy more with real money, which supports both Intermediate Currency and Pay to Progress. The mention of the 1v1 section also describes direct competition between players. The review does not establish a chance-based wager, so Gambling is not assigned.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: The reviewer describes coins as the in-game currency and says players must buy more of them with real money.
- `M_PayToProgress` - **SPURIOUS**
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: After the interface causes players to lose their coins, the review says they are forced to pay for replacement coins to keep playing.
- `M_UIMisdirection` - ok
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins"
  - why: The interface automatically places attention and selection on the highest-cost table, creating the described accidental mis-click risk.
- `S_Competition` - **SPURIOUS**
  - span: "go to the 1v1 section"
  - why: A 1v1 section explicitly describes player-versus-player competition.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `3c46f5e0-6091-43dc-94a0-e3af3259a63d` - Cashman Casino Slots Games

> Resently cashman had changed it's bingo rewards and daily rewards. However lve found that I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards. The most I can seem to get on the timed rewards is 40,000. I'd not pay just to get my daily rewards. So I'm deleting them.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_WasteAversion`, `T_DailyRewards` |
| pred | `M_Gambling`, `T_DailyRewards` |
| **missed** | `M_PayToProgress`, `M_WasteAversion` |
| **spurious** | `M_Gambling` |

**Did the model consider what it missed?**

- `M_PayToProgress` - never mentioned -> **attention / recall**
- `M_WasteAversion` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a daily-reward system that has been changed so the player cannot claim the daily rewards without first betting 50,000 in-game units. This directly identifies Daily Rewards because access to the reward is conditional on completing a daily requirement. The phrase "bet 50,000" also describes a wager in a casino-style game; the stake appears to be in-game currency, and the codebook allows Gambling when the stake is earned in-game without a real-money purchase being stated. The timed rewards and their 40,000 maximum describe reward amounts, but not a sufficiently specific unpredictable delivery mechanic for Reward Mania. The review does not establish a real-world waiting gate, payment requirement, or progress barrier.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "unless I bet 50,000"
  - why: The review explicitly describes staking 50,000 in-game units on a casino-style bet for a reward-related outcome.
- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The player must complete a daily betting requirement to obtain or complete the daily rewards.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (8)

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
The review describes a perceived outcome-manipulation mechanic: the RNG is said to be against the player, which asserts that results are being determined unfairly rather than merely reporting bad luck. The review also describes an unfavorable resource economy at higher levels: a level costs 2200 and a win barely returns that amount, while spending actual money is portrayed as the alternative. However, it does not explicitly say that payment is required to continue or progress, only that playing without spending is not rewarding, so Pay to Progress is not assigned. The weak return also does not show stranded currency or a concrete shortfall below an item cost, so Waste Aversion is not assigned.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "the rng is so obviously against you"
  - why: The reviewer asserts that the game’s random outcomes are manipulated against the player, which describes hidden or unfair outcome determination.

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
The review describes a base-building game as repetitive, but “same old same old grinder” is a general quality characterization without a named repeated activity tied to progress, so it does not support Grinding. The review explicitly describes winning events as requiring substantial spending, using “pay to play,” “pay to win,” and a reported 30k expenditure to win the last event. This is a monetary progression/competitive-advantage mechanic. It does not clearly state that the event involves competing against other players, so Competition is not assigned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Zero skill pay to win. Calculated total spent on last event was 30k to win."
  - why: The span states that spending money is required to gain the advantage needed to win an event.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `cc714d17-863c-4ebd-b14f-989ba17c71c4` - Dice Dreams™️

> I played this game on a different profile. the only reason I gave it five stars is because if you don't it won't let you write a review. if you want to win anything on this game it will cost hundreds of dollars. on the stickers you will never get the last one or two unless you pay a lot of money to get them. this is not a game you want to get addicted to unless you have a endless bank account. it may let you complete a goal maybe one out of hundred times.dont get your hopes up.

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury`, `M_PayToProgress`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_PayToProgress`, `P_CompleteTheCollection` |
| **missed** | `M_DeceptiveLuxury`, `P_RewardMania` |

**Did the model consider what it missed?**

- `M_DeceptiveLuxury` - never mentioned -> **attention / recall**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a collection-based game in which completing sticker sets is presented as effectively impossible without paying substantial real money. The player explicitly says the final one or two stickers require a large payment, which makes payment an alternative to completing the collection through ordinary play. The sticker language also directly describes the compulsion or goal of completing a collection. The statements about addiction, low odds of completing a goal, and giving five stars to submit a review do not by themselves establish additional coded mechanics: no explicit wager, randomised reward system, accumulated investment, or in-game advertising behavior is described.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: The review states that completing sticker progress is unavailable through ordinary play unless the player makes a substantial payment.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two"
  - why: The player describes pursuing the final missing stickers in order to complete a collection.

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
The review describes a level-progression barrier tied to payment: the player must buy add-ons to get through later levels, and the free route is described as effectively impossible. The player also reports repeatedly running out of lives and taking 5–7 days per level, but no explicit timer, regeneration schedule, or named repetitive activity is given, so Playing by Appointment and Grinding are not supported. Reporting wasted money and time does not by itself show that accumulated investment makes leaving difficult, so Easy to Get, Hard to Lose is not assigned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying."
  - why: The review states that continued level progress requires buying add-ons, while the unpaid route is excessively burdensome.

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
The reviewer describes a loss-of-holdings behavior tied to leaving the game: a full bag is empty on return, and both earned and purchased coins have been consumed. This is not merely a general complaint about lost value; the span connects the loss to ending or leaving a play session. The mechanic therefore prevents the player from safely stopping and forfeits accumulated holdings when they leave, matching Mandatory Marathon. The review does not explicitly say the player is reluctant to quit or pressured to continue, so Easy to Get, Hard to Lose is not assigned separately.
```

**Labels assigned**

- `T_MandatoryMarathon` - ok
  - span: "I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used"
  - why: Leaving the game results in the player's stored items and coins being lost or consumed, so the player cannot safely stop at a moment of their choosing.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `12267c1e-47ba-4984-97c8-768e820ceb1c` - Bingo Blitz™️ - Bingo Games

> not very user-friendly. no apparent reachable goals within a decent amount of time. I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| pred | `P_CompleteTheCollection`, `T_Grinding` |
| **missed** | `M_EasyToPurchase`, `P_AestheticManipulation` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - never mentioned -> **attention / recall**
- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes repeated bingo rounds being played to collect photos and complete a set, which supports Grinding and Complete the Collection. It also describes a post-loss offer to spend coins for a missing photo, but the review does not establish that the coins were bought with real money, nor that the offer is a chance-based mechanic. The statement about wasting money is a general complaint and does not independently identify a coded mechanic. The failure to receive the promised photo is reported as an outcome problem, without a clearly described dark-pattern rule.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "collect 'photos'"
  - why: Photos are collectible game items, and the reviewer is pursuing them to complete the set.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The reviewer repeatedly plays bingo rounds as the required activity for collecting progress items.

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

- `M_DeceptiveLuxury` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a sticker-collection system in which sticker rewards often produce duplicates, making completion difficult. It also explicitly states that finishing all sticker sets is unavailable unless the player pays, which is a payment gate on collection progress. The duplicate drops support Reward Mania because the reward delivery produces repeated unwanted items, while pursuing completion of all sets supports Complete the Collection. No separate gambling label is assigned because the review does not explicitly mention a paid chance-based stake.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: Completing the sticker sets is explicitly presented as impossible without payment.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: The reviewer is pursuing completion of all sticker sets, an in-game collection.
- `P_RewardMania` - ok
  - span: "getting stickers. always get duplicates"
  - why: The sticker-reward system repeatedly delivers duplicates, making the delivery mechanism rather than just the reward value sustain effort.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b93c432d-19c0-4c6c-a2d4-bb9b21a436f3` - Dice Dreams™️

> A literal brain-rot game no wonder why they're tryna promote it through Free Cash. Also if you're thinking of making in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates! A real SCAM. Play it if u want but there are games that are actually good also, DON'T GET IN-APP PURCHASES!

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `P_CompleteTheCollection`, `P_RewardMania` |
| **missed** | `P_AestheticManipulation` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes an album-collection mechanic in which only two cards remain before a grand prize is awarded, indicating a drive to complete the collection. They then describe paying for a deal that was supposed to provide new cards but instead delivered duplicate cards. The duplicate-card outcome describes an unwanted or variable reward delivery system, supporting Reward Mania. The external promotion through Free Cash is out of scope under R13, and the review does not establish that payment is required for general progress, that real money is converted into virtual currency, or that the purchase involved a chance-based wager.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The reviewer is pursuing the remaining cards needed to complete an album and obtain its completion reward.
- `P_RewardMania` - ok
  - span: "i bought a deal which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: The purchased card delivery produced unwanted duplicate rewards instead of the desired new cards, describing a reward system built around variable or repeated drops.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (2)

### `95ddadb3-82cd-4042-8a51-cf8b3ed164c2` - Mech Arena - Shooting Game

> You stuck waiting 30 seconds just to connect to a match. This game makes it seem like they give so many rewards but if all just for show. Its difficult to get weapon upgrades or any percs others you stick battling to win. This kind of games just rob you of your time in my opinion

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `S_Competition` |
| **spurious** | `S_Competition` |

**Model analysis**

```
The review describes a matchmaking wait of 30 seconds before a match begins, but this is a service or queue delay rather than an in-game timer that schedules or gates play, so it does not satisfy Playing by Appointment. It also describes matches and battling to win, which establishes player-versus-player competition. The difficulty of obtaining weapon upgrades and perks is stated as a general difficulty, without a repeated task, payment requirement, or specific reward-delivery mechanic, so it does not support additional labels.
```

**Labels assigned**

- `S_Competition` - **SPURIOUS**
  - span: "connect to a match"
  - why: Connecting to matches and battling to win describes a game structure in which players compete against one another.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `32c623b4-0249-469e-968c-94f60c7fe3c2` - Royal Match

> It's an interesting game but the developers should pls try to include new cards in every card pack because I noticed when one is almost close to completing a set, new cards don't appear again especially when the set is almost expiring. So after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion because they don't add new sets to the cards once the collection is about to end.

| | labels |
|---|---|
| gold | `P_CompleteTheCollection`, `T_PlayingByAppointment` |
| pred | `P_CompleteTheCollection`, `P_RewardMania`, `T_PlayingByAppointment` |
| **spurious** | `P_RewardMania` |

**Model analysis**

```
The review describes a card-collection system with card packs that stop yielding new cards when the player is close to completing a set. The player is pursuing a collection milestone of 125 cards and a completion reward, so the collection itself is a motivational target. The card-pack delivery is variable and produces a shortage of new cards near completion, implying repeated attempts may fail to provide the needed items; this supports Reward Mania, but no monetary stake is stated, so Gambling is not assigned. The set has an expiration point, and failing to complete it before expiry causes the reward to be lost, which is Playing by Appointment. The expiration creates a time limit, but the review does not explicitly describe anxiety or continued play driven by fear of missing out, so FOMO is not assigned.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "after collecting 125 cards from the beginning of the collection"
  - why: The reviewer describes working toward acquiring all cards needed to complete a collection and receive its reward.
- `P_RewardMania` - **SPURIOUS**
  - span: "include new cards in every card pack because I noticed when one is almost close to completing a set, new cards don't appear again"
  - why: Card packs deliver unpredictable or non-completing results, with needed new cards failing to appear as the player repeatedly pursues the set.
- `T_PlayingByAppointment` - ok
  - span: "especially when the set is almost expiring. So after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion"
  - why: The set's expiration imposes a game-defined deadline, and failing to complete the collection before it ends forfeits the completion reward.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_PayToProgress` | 3 | 2 |
| `S_Competition` | 2 | 2 |
| `T_Grinding` | 2 | 0 |
| `S_Reciprocity` | 2 | 0 |
| `M_DeceptiveLuxury` | 2 | 0 |
| `P_RewardMania` | 1 | 1 |
| `P_AestheticManipulation` | 2 | 0 |
| `M_Gambling` | 1 | 1 |
| `M_WasteAversion` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `M_IntermediateCurrency` | 1 | 0 |
| `M_EasyToPurchase` | 1 | 0 |

