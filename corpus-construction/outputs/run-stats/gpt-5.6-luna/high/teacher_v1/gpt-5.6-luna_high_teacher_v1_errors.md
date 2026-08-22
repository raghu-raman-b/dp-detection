# Error review - gpt-5.6-luna_high_teacher_v1

`gpt-5.6-luna` / reasoning `high` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v1.txt` sha `e8cd52987c33`  
micro-F1 **0.830** (P 0.904 / R 0.767) - **16 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 1 | said NONE, gold had labels |
| SWAP | 6 | picked different labels than gold |
| MISSED ONLY | 9 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 0 | found all gold, added extras |

## The diagnostic that matters

Of **20** missed labels, **13** (65%) were named in the model's own analysis and dropped anyway; **7** (35%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `S_Reciprocity` | 1 | 1 |
| `P_RewardMania` | 2 | 0 |
| `P_AestheticManipulation` | 0 | 2 |
| `M_PayToProgress` | 2 | 0 |
| `P_IllusionOfControl` | 0 | 1 |
| `M_Gambling` | 1 | 0 |
| `T_Grinding` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `S_Competition` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `M_RecurringFee` | 0 | 1 |
| `T_Advertisement` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `T_MandatoryMarathon` | 1 | 0 |
| `M_IntermediateCurrency` | 0 | 1 |
| `M_EasyToPurchase` | 1 | 0 |

## Missed everything (predicted NONE) (1)

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
The review describes requesting troops from a clan, which would otherwise indicate a resource-transfer mechanic relevant to S_Reciprocity. However, the inability to use that feature is explicitly attributed to an update and presented as something needing to be fixed, so R11 suppresses the label as a technical malfunction. No other mechanic is described.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (6)

### `fd1230ab-7d12-4aeb-a425-e37ed06bcd5c` - Pokémon GO

> I love this game, just started playing about 2 months ago. Though I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way. I feel taken advantage of. 3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| pred | `M_PayToProgress`, `S_FriendSpamImpersonation` |
| **missed** | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `P_IllusionOfControl` - never mentioned -> **attention / recall**
- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes capture attempts consuming Poké Balls unusually quickly, leading the player to purchase more, which makes payment necessary to continue this gameplay activity; this supports Pay to Progress. It also states that a review was posted under the player's identity despite the player denying authorship, supporting Friend Spam / Impersonation. Intermediate Currency is rejected because Poké Balls are items rather than purchased in-game currency. Gambling, Advertisement, and Easy to Purchase are rejected because no wager, ad viewing, or purchase-intercepting interface is described.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: Capture attempts consume the required Poké Balls, forcing the player to purchase more to continue capturing Pokémon.
- `S_FriendSpamImpersonation` - ok
  - span: "I DID NOT WRITE THIS REVIEW"
  - why: The review claims that content was posted under the player's account without their authorship.

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
The review describes an interface that automatically scrolls to and selects the highest-bet table, creating accidental mis-clicks, which triggers M_UIMisdirection. It also explicitly says players lose their coins and are forced to buy real ones, supporting M_IntermediateCurrency and M_PayToProgress. S_Competition applies because the 1v1 section is a player-versus-player mode. M_EasyToPurchase is rejected because no accidental real-money purchase or purchase prompt is described; M_Gambling is rejected because chance-based rewards are not stated; M_WasteAversion and P_EasyToGetHardToLose are rejected because the loss is a betting consequence, not stranded currency or reluctance to leave.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "lose all their hard-earned coins and are forced to buy real ones"
  - why: The review describes acquiring in-game coins through a real-money purchase.
- `M_PayToProgress` - **SPURIOUS**
  - span: "lose all their hard-earned coins and are forced to buy real ones"
  - why: After the coin loss, payment is described as required to continue playing.
- `M_UIMisdirection` - ok
  - span: "automatically scrolls and selects the highest possible bet table based on your coins"
  - why: The interface automatically directs the player toward the highest-bet option, facilitating unintended selection and mis-clicks.
- `S_Competition` - **SPURIOUS**
  - span: "1v1 section"
  - why: The review identifies a player-versus-player competition mode.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `3c46f5e0-6091-43dc-94a0-e3af3259a63d` - Cashman Casino Slots Games

> Resently cashman had changed it's bingo rewards and daily rewards. However lve found that I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards. The most I can seem to get on the timed rewards is 40,000. I'd not pay just to get my daily rewards. So I'm deleting them.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_WasteAversion`, `T_DailyRewards` |
| pred | `M_Gambling`, `M_WasteAversion`, `T_DailyRewards` |
| **missed** | `M_PayToProgress` |
| **spurious** | `M_Gambling` |

**Did the model consider what it missed?**

- `M_PayToProgress` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a daily reward system that requires a 50,000 bet, so T_DailyRewards applies. The phrase "bet 50,000" describes a wager in a casino-slots game, supporting M_Gambling even though the stake is not explicitly identified as real money. The 40,000 versus 50,000 gap is a concrete shortfall below the required amount, and the reviewer says they would pay to obtain the rewards, so M_WasteAversion applies. M_PayToProgress is rejected because the payment is not described as enabling general game progression; T_PlayingByAppointment is rejected because the daily cycle does not gate overall progression; M_EasyToPurchase is rejected because no purchase prompt or friction-reducing interface is described.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "bet 50,000"
  - why: This explicitly describes placing a wager in a casino-slots game.
- `M_WasteAversion` - ok
  - span: "The most I can seem to get on the timed rewards is 40,000."
  - why: The reviewer identifies a concrete 10,000 shortfall below the 50,000 amount required to obtain the daily rewards.
- `T_DailyRewards` - ok
  - span: "can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The game provides daily rewards but makes them conditional on completing a required daily activity.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `176aaa1f-d8f9-4a1a-9f29-64902f13be5c` - All in Hole: Black Hole Games

> I would give 5 stars, but I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used.🤨😒🙄😥

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `T_MandatoryMarathon` |
| pred | `P_EasyToGetHardToLose` |
| **missed** | `M_IntermediateCurrency`, `T_MandatoryMarathon` |
| **spurious** | `P_EasyToGetHardToLose` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**
- `T_MandatoryMarathon` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes accumulated in-game value being lost when the player leaves and returns: a full bag becomes empty and earned or purchased coins are gone. This supports P_EasyToGetHardToLose because leaving or disengaging entails forfeiting value already held. T_MandatoryMarathon was considered but rejected because the text does not say the player is prevented from stopping or that exiting a session directly forfeits progress. M_WasteAversion was rejected because no specific stranded currency shortfall, inventory-capacity purchase, or item sacrifice is described.
```

**Labels assigned**

- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used"
  - why: The player loses accumulated bag contents and coins after leaving, making disengagement costly.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a2ece36d-c527-442d-8f18-9a16b63994c8` - War Robots Multiplayer Battles

> Its a p2w game. The only time you enjoy it is when you're new. As you progress, everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game. If you want to progress without paying money, goodluck! Even if you wanted to do f2p, you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it. Plus the only time you benofit by getting f2p rewards is ads... 💩

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `M_PayToProgress`, `M_PowerCreep`, `T_Advertisement` |
| pred | `M_EasyToPurchase`, `M_PayToProgress`, `M_PowerCreep`, `S_Competition` |
| **missed** | `T_Advertisement` |
| **spurious** | `S_Competition` |

**Did the model consider what it missed?**

- `T_Advertisement` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes purchase offers that block access to gameplay, payment as the route to progress, and newer paid bots becoming necessary as the meta shifts. I considered Advertisement but rejected it because the review does not explicitly say ads are forced or rewarded; Intermediate Currency, Recurring Fee, Never-Ending Lure, FOMO, and Complete the Collection are not described. Competition is applicable because keeping up with the shifting meta describes maintaining a competitive position.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game"
  - why: Purchase offers directly intercept gameplay before the player can play, reducing the friction to buying.
- `M_PayToProgress` - ok
  - span: "you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it"
  - why: The span states that payment is required to obtain the bot needed to continue progressing competitively.
- `M_PowerCreep` - ok
  - span: "keep up with shifting meta where you have to buy the newest bot with money instead of earning it"
  - why: A shifting meta makes newer bots necessary, implying that previously acquired bots lose practical value as new releases appear.
- `S_Competition` - **SPURIOUS**
  - span: "keep up with shifting meta"
  - why: The span describes needing to remain current with the competitive meta.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `12267c1e-47ba-4984-97c8-768e820ceb1c` - Bingo Blitz™️ - Bingo Games

> not very user-friendly. no apparent reachable goals within a decent amount of time. I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| pred | `P_CompleteTheCollection`, `P_RewardMania`, `T_Grinding` |
| **missed** | `M_EasyToPurchase`, `P_AestheticManipulation` |
| **spurious** | `P_RewardMania` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - considered and rejected -> **rule interpretation**
- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes repeatedly playing rounds to collect photos and complete a set, plus an in-game prompt to spend coins for a missing photo that is allegedly not delivered. T_Grinding applies because the repeated activity is named and tied to collection progress. P_CompleteTheCollection applies because completing the set is an explicit acquisition goal. P_RewardMania applies because repeated attempts are used to obtain a specific reward. M_PayToProgress and M_IntermediateCurrency are rejected because the review does not explicitly connect real money to acquiring the coins or establish that payment is required for progress. M_WasteAversion is rejected because the text describes non-delivery of a promised reward, not leftover or insufficient currency. Gambling and EasyToPurchase are rejected because no explicit chance-based monetary stake or friction-reducing purchase interface is described.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "to complete the set"
  - why: The reviewer explicitly describes a goal of acquiring enough photos to complete a collection.
- `P_RewardMania` - **SPURIOUS**
  - span: "I play round after round to collect 'photos'"
  - why: Repeated attempts are used to obtain a specific reward, making the delivery pursuit itself sustain engagement.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The reviewer describes repeating rounds as the activity required to pursue collection progress.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (9)

### `b580a4c7-3c75-493e-ad3b-03b4f2bde6a5` - Pokémon GO

> This new update have many bugs. 1)I can't open any gifts or trade with friends without the keep on crashing, 2) when click on a pokemon I can't even throw the pokeball with all the lagging, 3) the pvp & rockets battles are also lagging switching out are too slow, charge attacks are not responding well and my game freeze while the opponent keep attacking. Please fix these problems!

| | labels |
|---|---|
| gold | `S_Competition`, `S_Reciprocity` |
| pred | `S_Competition` |
| **missed** | `S_Reciprocity` |

**Did the model consider what it missed?**

- `S_Reciprocity` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes crashes, lag, and freezing, all explicitly attributed to bugs or technical faults, so those malfunctioning behaviors do not trigger dark-pattern labels under R11. It also explicitly describes PvP battles and an opponent, which is a competition mechanic. Gifts and trading are mentioned, but their failure is attributed to crashing and no obligation to reciprocate is described. No other candidate label is supported.
```

**Labels assigned**

- `S_Competition` - ok
  - span: "the pvp & rockets battles are also lagging"
  - why: The span explicitly describes PvP battles, in which players compete against one another.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

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
The review describes trading lives with friends and a team, which is a resource exchange with existing players and satisfies Reciprocity. The references to 9 diamonds and a pass do not establish real-money conversion, a purchase prompt, recurring-fee pressure, or pay-to-progress. The element failing to appear within a number of moves describes an unspecified game outcome, but no clear chance mechanic or reward-delivery system is identified, so Gambling and Reward Mania are rejected under R2 and R4. The move counts are not real-world timers, so Playing by Appointment does not apply.
```

**Labels assigned**

- `S_Reciprocity` - ok
  - span: "trade lives"
  - why: Trading lives is an explicit exchange of resources with other players, creating the reciprocity mechanic.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `0347fbc7-5c01-452e-ae4b-867f5bd7dd47` - Homescapes

> I really enjoy this (very) addicting and fun game. The levels get harder, but its fun to beat after a while. I only have a few suggestions; maybe only 5-10 minutes for a new life, not as many small and unnecessary tasks like celebrating and just because you miss a day doesnt mean that you need to start over on your daily prizes. But overall, I would recommend this game to anyone and the creators did a very good job on this game.👍

| | labels |
|---|---|
| gold | `T_DailyRewards`, `T_PlayingByAppointment` |
| pred | `T_DailyRewards` |
| **missed** | `T_PlayingByAppointment` |

**Did the model consider what it missed?**

- `T_PlayingByAppointment` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes daily prizes that reset when the player misses a day, which is Daily Rewards. The suggestion about reducing the time for a new life does not establish the current wait duration and is phrased as a proposed change, so Playing by Appointment is rejected under R12. The harder levels and praise of the game do not describe grinding or another codable mechanic.
```

**Labels assigned**

- `T_DailyRewards` - ok
  - span: "just because you miss a day doesnt mean that you need to start over on your daily prizes"
  - why: Daily prizes reset when the player misses a day, providing a daily-return incentive with an explicit penalty.

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
The review describes an assertedly manipulated random-outcome mechanic: "the rng is so obviously against you". This satisfies P_IllusionOfControl because it claims the game determines outcomes unfairly. I considered M_PayToProgress, but spending actual money is described as making play more rewarding, not as required to advance past a barrier. I rejected M_Gambling and P_RewardMania because no wager or specific chance-based reward-delivery system is described. I rejected M_WasteAversion because the review does not clearly describe stranded currency or a concrete unusable shortfall.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "the rng is so obviously against you"
  - why: The reviewer claims the game’s random outcomes are manipulated against the player.

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
The review describes spending money to win an event, which is a paid in-game advantage and satisfies M_PayToProgress. I considered T_Grinding, but "Same old same old grinder" is a general characterization without a named repetitive activity or progress requirement. I rejected S_Competition because the review does not explicitly describe opponents or players competing against one another, and rejected M_Gambling because no chance-based mechanic or wager is described. No other label is supported.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Zero skill pay to win."
  - why: The span explicitly describes paying to gain the advantage needed to win in-game.

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
The review describes payment being required to obtain the final stickers and complete sticker goals, supporting Pay to Progress and Complete the Collection. The claim that the last stickers are withheld unless the player pays also describes purchase-linked artificial scarcity, supporting Deceptive Luxury. Gambling and Reward Mania are rejected because no explicit chance-based delivery mechanic is described; Intermediate Currency is rejected because no real-money conversion into game currency is mentioned. Addiction, an endless bank account, and the forced five-star review do not describe codable in-game mechanics.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "you will never get the last one or two unless you pay a lot of money to get them"
  - why: The scarcity of the final stickers is tied directly to paying money, indicating manufactured scarcity affecting purchase.
- `M_PayToProgress` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: The review says payment is necessary to obtain the final stickers and complete the goal.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two"
  - why: The span describes pursuing the final missing items in a sticker collection.

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
The review describes a payment gate: the player says they must buy add-ons to get through the game and that not paying prevents progress, which satisfies M_PayToProgress. The lives running out and taking 5-7 days per level do not specify a regeneration wait, so T_PlayingByAppointment is rejected. The time spent does not identify a repetitive task or repeated attempts, so T_Grinding is rejected. No daily reward, subscription, chance mechanic, social mechanic, or accumulated investment affecting the decision to leave is described; the money and time are reported as already wasted while uninstalling, so P_EasyToGetHardToLose is rejected.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through"
  - why: The span explicitly describes payment as necessary to continue or progress through the game.

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
The review describes repeated duplicate sticker drops, an incomplete collection of sticker sets, and payment being required to finish them. I considered P_RewardMania for the repeated unwanted duplicates, P_CompleteTheCollection for the goal of finishing all sets, and M_PayToProgress because payment is presented as necessary for completion. I rejected M_Gambling because no monetary stake in a chance mechanic is described, and M_DeceptiveLuxury because the review does not describe rarity, exclusivity, or a limited offer beyond the payment gate.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: The text states that payment is required to complete the collection and progress toward its goal.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: The review describes the compulsion or goal of completing all sticker sets.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: Repeated duplicate sticker drops describe an unwanted reward-delivery pattern.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b93c432d-19c0-4c6c-a2d4-bb9b21a436f3` - Dice Dreams™️

> A literal brain-rot game no wonder why they're tryna promote it through Free Cash. Also if you're thinking of making in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates! A real SCAM. Play it if u want but there are games that are actually good also, DON'T GET IN-APP PURCHASES!

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `P_CompleteTheCollection` |
| **missed** | `P_AestheticManipulation`, `P_RewardMania` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**
- `P_RewardMania` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes an album-collection objective and a purchase of cards toward its grand prize. P_CompleteTheCollection applies to completing the album. I considered P_RewardMania, but the review reports duplicates without explicitly describing a randomized reward pool or chance-based delivery; M_Gambling and M_IntermediateCurrency are also unsupported because no wager or real-money-to-currency conversion is described. The mention of promotion through Free Cash is out-of-game marketing and is excluded by R13.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "grand prize for completing an album"
  - why: The span explicitly describes completing an in-game album collection to obtain its grand prize.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_PayToProgress` | 2 | 2 |
| `S_Competition` | 1 | 2 |
| `P_RewardMania` | 2 | 1 |
| `S_Reciprocity` | 2 | 0 |
| `P_AestheticManipulation` | 2 | 0 |
| `M_Gambling` | 1 | 1 |
| `P_IllusionOfControl` | 1 | 0 |
| `M_RecurringFee` | 1 | 0 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `T_Advertisement` | 1 | 0 |
| `T_MandatoryMarathon` | 1 | 0 |
| `M_EasyToPurchase` | 1 | 0 |
| `T_Grinding` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `M_IntermediateCurrency` | 1 | 0 |

