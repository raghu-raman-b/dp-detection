# Error review - gpt-5.6-luna_none_teacher_v2_full

`gpt-5.6-luna` / reasoning `` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `6529a474a2b0`  
micro-F1 **0.840** (P 0.895 / R 0.791) - **18 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 5 | said NONE, gold had labels |
| SWAP | 4 | picked different labels than gold |
| MISSED ONLY | 6 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 3 | found all gold, added extras |

## The diagnostic that matters

Of **18** missed labels, **1** (6%) were named in the model's own analysis and dropped anyway; **17** (94%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `M_PayToProgress` | 1 | 2 |
| `S_Reciprocity` | 0 | 2 |
| `P_AestheticManipulation` | 0 | 2 |
| `M_IntermediateCurrency` | 0 | 2 |
| `M_Gambling` | 0 | 1 |
| `M_WasteAversion` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `S_Competition` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `P_RewardMania` | 0 | 1 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
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
The review consists entirely of requested or hypothetical features: auctions using in-game currency, preserving converted decorations, an account-switching widget showing upgrade time, and hidden troop statistics. These suggestions do not explicitly describe currently operating dark-pattern mechanics. The mention of upgrade time is part of a proposed widget rather than a description of an existing wait gate or schedule imposed on play, so no label is supported.
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
The review is a technical-fault report. It describes crashing when opening gifts or trading, lag preventing Poké Ball throws, and freezing or delayed battle controls in PvP and Team GO Rocket battles. These behaviors are explicitly attributed to bugs, lag, crashing, and freezing rather than deliberate game design. Although gifts, trading, and PvP are mentioned, the review does not describe a dark-pattern mechanic operating independently of the technical malfunction, so R11 requires NONE.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a12b6d56-8505-4b4e-9b43-cde2d1085360` - MadOut 2: Grand Auto Racing

> well I LOVE the game BUT I know if I deleted the game I would lose everything my in-game purchases and my hard work I really don't want that to happen because it has happened on other games it's just a suggestion is there anyway possible to where you guys can make it where you save all our progress in-game purchases and everything else that we have done because if this game can hold that then I will be looking forward to be putting money in this game

| | labels |
|---|---|
| gold | `P_EasyToGetHardToLose` |
| pred | _NONE_ |
| **missed** | `P_EasyToGetHardToLose` |

**Did the model consider what it missed?**

- `P_EasyToGetHardToLose` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer says that deleting the game would erase in-game purchases and accumulated progress, and expresses concern about that possible loss. They are asking the developer to add persistent saving and condition future spending on that feature. This describes a loss-of-data or missing-save concern, not a deliberate mechanic that makes continuing to play difficult because of accumulated investment. The requested saving feature is hypothetical and is not coded under R12. No supported dark-pattern label applies.
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
The review describes a technical malfunction after an update: the player can no longer request troops from their clan and asks for a fix. Although troop requests imply an existing clan resource-sharing feature, the review does not describe players being pressured to donate or reciprocate. Under R11, the specific behavior is attributed to an update-related fault, so no dark-pattern label applies.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `64f944c2-f4b3-4af9-806d-25c57b5f976e` - Candy Crush Saga

> This game is no longer fun. I will uninstall if it still takes a week to pass hard levels. Plus there are way too many impossible tasks unless you buy boosters.

| | labels |
|---|---|
| gold | `M_PayToProgress` |
| pred | _NONE_ |
| **missed** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_PayToProgress` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes slow advancement through difficult levels, saying that passing hard levels can take a week, but does not describe a timer, required repeated task, or a game-defined schedule. They also say some tasks are impossible unless boosters are bought, but the review does not establish that the boosters are purchased with real money or that buying them is a monetary progression gate. The text therefore supports no meso label.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (4)

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
The review describes capture attempts consuming Poké Balls unusually quickly after the player began purchasing them, creating a need to buy more. This supports a payment-linked progression or continuation barrier: the player must purchase additional consumable capture attempts to keep capturing. The claim that Pokémon keep breaking out specifically after purchases alleges that the game manipulates or tunes capture outcomes to increase resource consumption, which fits Illusion of Control as an alleged hidden determination of outcomes. The final edit says the review was posted without the account holder writing it and denies the claimed conversations, describing an unauthorized review under the player's identity; this supports Friend Spam / Impersonation under the store-review destination exception. No currency conversion, gambling, reward-delivery, or social-recruitment mechanic is described.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "so I go through the balls faster so I have to purchase more"
  - why: The player says that faster depletion of capture balls makes purchasing more necessary to continue capturing Pokémon.
- `P_IllusionOfControl` - ok
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out"
  - why: The span alleges that capture outcomes are manipulated after purchases, causing repeated breakouts and concealing the game's true outcome determination.
- `S_FriendSpamImpersonation` - ok
  - span: "I DID NOT WRITE THIS REVIEW"
  - why: The account holder states that the review was posted in their name without their authorship, implying unauthorized impersonation through the game's review activity.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fdef27f2-9a21-4b8e-a04c-7a4753e0fb07` - 8 Ball Pool

> The game is great, but the user interface is completely rigged. Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins and are forced to buy real ones. ​We need a "Default Table Lock" or the game should always open the lowest bet table by default, not the highest! Fix this scammy feature. Giving 1 star

| | labels |
|---|---|
| gold | `M_Gambling`, `M_IntermediateCurrency`, `M_UIMisdirection` |
| pred | `M_EasyToPurchase`, `M_IntermediateCurrency`, `M_UIMisdirection`, `S_Competition` |
| **missed** | `M_Gambling` |
| **spurious** | `M_EasyToPurchase`, `S_Competition` |

**Did the model consider what it missed?**

- `M_Gambling` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes an interface that automatically scrolls to and selects the highest-bet 1v1 table, directing the player toward a risky option instead of a neutral or low-bet choice. The reviewer says this causes accidental mis-clicks and loss of accumulated coins. It also states that, after losing those coins, players are forced to buy more with real money, establishing a real-money-to-virtual-currency conversion. The 1v1 section describes competition against other players. The requested default lock and lowest-table behavior are hypothetical additions and are not coded.
```

**Labels assigned**

- `M_EasyToPurchase` - **SPURIOUS**
  - span: "This is a cheap "Dark UX" trick to force accidental mis-clicks"
  - why: The default interface setup is described as causing unintended taps that make the player enter a high-cost table.
- `M_IntermediateCurrency` - ok
  - span: "are forced to buy real ones"
  - why: The wording implies that players must replace lost virtual coins by purchasing them with real money.
- `M_UIMisdirection` - ok
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins"
  - why: The interface automatically focuses the player on the highest-bet table, steering attention and selection toward a costly option.
- `S_Competition` - **SPURIOUS**
  - span: "go to the 1v1 section"
  - why: A 1v1 section is a game mode in which the player competes directly against another player.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `176aaa1f-d8f9-4a1a-9f29-64902f13be5c` - All in Hole: Black Hole Games

> I would give 5 stars, but I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used.🤨😒🙄😥

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `T_MandatoryMarathon` |
| pred | `P_EasyToGetHardToLose`, `T_MandatoryMarathon` |
| **missed** | `M_IntermediateCurrency` |
| **spurious** | `P_EasyToGetHardToLose` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes accumulated in-game value being lost when the player stops and returns: a full bag becomes empty, and both earned and purchased coins have been consumed. This is not merely a complaint about a bug because no technical fault is named; it describes a game behavior tied to leaving. The loss makes stopping costly, supporting Easy to Get, Hard to Lose, and the forfeiture on exiting supports Mandatory Marathon.
```

**Labels assigned**

- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used"
  - why: The player’s accumulated items and currency are forfeited or depleted after leaving, making the existing investment costly to abandon.
- `T_MandatoryMarathon` - ok
  - span: "I leave the game with my bag full only to come back with it empty"
  - why: Leaving the game results in the loss of accumulated holdings, indicating that the player cannot stop without forfeiting progress or value.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `12267c1e-47ba-4984-97c8-768e820ceb1c` - Bingo Blitz™️ - Bingo Games

> not very user-friendly. no apparent reachable goals within a decent amount of time. I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| pred | `M_WasteAversion`, `P_CompleteTheCollection`, `T_Grinding` |
| **missed** | `M_EasyToPurchase`, `P_AestheticManipulation` |
| **spurious** | `M_WasteAversion` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - never mentioned -> **attention / recall**
- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes repeatedly playing bingo rounds to collect photos and complete a set, which is a repetitive progress task and a collection goal. The game also presents an in-game coin offer after a lost round, and the reviewer spends coins but receives neither the promised photo nor the offer, meaning currency is consumed without receiving the intended value. The review does not explicitly state that real money is converted into coins, nor does it clearly describe a chance-based paid wager, so Intermediate Currency and Gambling are not assigned. The failure to receive the promised photo is not attributed to a bug or technical fault.
```

**Labels assigned**

- `M_WasteAversion` - **SPURIOUS**
  - span: "I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED."
  - why: Coins are spent on the offer, but the promised photo is not delivered, leaving the spent currency without its purchased value.
- `P_CompleteTheCollection` - ok
  - span: "collect 'photos'"
  - why: The photos are collectible items, and the reviewer is pursuing them to complete the set.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The reviewer repeatedly plays bingo rounds as the activity needed to collect progress items.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (6)

### `549e5e94-9b59-477d-88c7-ae5e00d62514` - Disney Solitaire

> it was fine at the start but further along into the game the rng is so obviously against you it's crazy.. it's not rewarding playing the game without spending actual money.. at around level 100 it costs 2200 but if you win the level you'll barely make that back.. the rewards need a big revamp for me.. let down by alot of things with this game the further into it you get.. sort it out

| | labels |
|---|---|
| gold | `M_PayToProgress`, `P_IllusionOfControl` |
| pred | `P_IllusionOfControl` |
| **missed** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_PayToProgress` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a random-number-based outcome system that the player believes is deliberately unfavorable: "the rng is so obviously against you" asserts that outcomes are being manipulated rather than determined fairly, which fits Illusion of Control. The reviewer also mentions spending actual money and a level costing 2200, but does not clearly state that payment is required to progress, that real money buys in-game currency, or that a specific amount of currency is stranded or unusable. "you'll barely make that back" describes poor reward value rather than a realized leftover or concrete shortfall, so it does not support Waste Aversion. No other mechanic is explicitly established.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "the rng is so obviously against you"
  - why: The reviewer alleges that the game manipulates or rigs random outcomes against the player, rather than merely reporting an unlucky run.

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
- `M_WasteAversion` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a daily-reward system that requires the player to place a 50,000 bet before the daily rewards can be completed. The player also describes timed rewards with a maximum payout, but this is an amount limit rather than a wait imposed on gameplay. The daily cycle is a standalone reward opportunity, not a gate on overall progression, so Daily Rewards applies without Playing by Appointment. The bet is not explicitly tied to real money or purchased currency, so Gambling and Pay to Progress are not assigned.
```

**Labels assigned**

- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The game makes completion of the daily-reward cycle conditional on placing a 50,000 bet.

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

- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a collection-based game where meaningful success is made extremely expensive: winning anything supposedly costs hundreds of dollars. Sticker completion is explicitly monetized, with the final one or two stickers portrayed as unavailable unless the player pays heavily. That supports payment-gated progress, collection completion, and manufactured scarcity tied to purchase. The statement that a goal succeeds only about one time in a hundred describes an extremely low or unpredictable reward outcome, but it does not identify a specific chance mechanic or monetary wager, so Gambling is not assigned. The addiction warning is evaluative and does not independently establish a label.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "you will never get the last one or two unless you pay a lot of money to get them"
  - why: The final stickers are portrayed as deliberately scarce and obtainable through heavy payment, tying manufactured rarity to purchase.
- `M_PayToProgress` - ok
  - span: "if you want to win anything on this game it will cost hundreds of dollars"
  - why: The review states that spending substantial real money is required to achieve meaningful in-game success.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two"
  - why: The span describes the player pursuing completion of a sticker collection and being blocked from obtaining its final items.

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
The review describes a sticker-collection system in which rewards repeatedly produce duplicates, implying an unpredictable or repeated reward-delivery mechanic rather than direct progress. The player is trying to complete all sticker sets, which supports the collection-compulsion label. Completion is also explicitly blocked unless the player pays, establishing a pay-to-progress barrier. The review does not explicitly describe sticker packs, draws, or a monetary wager within a chance mechanic, so Gambling is not assigned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: The review explicitly states that completing the sets is unavailable without payment.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: The reviewer describes pursuing completion of all in-game sticker sets.
- `P_RewardMania` - ok
  - span: "getting stickers. always get duplicates"
  - why: Repeatedly receiving duplicate stickers describes a reward-delivery system with unwanted or unpredictable outcomes.

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

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a timed reward and purchase system. Timed bonuses continue expiring while the player is away, so the game imposes a clock that controls when the player must use them. The reviewer also says free gold is sometimes insufficient to keep playing, making buying the paid alternative necessary for continued access. The charged gold and unused moves describe an unwanted or questionable transaction, but do not clearly establish accidental purchase design or stranded currency under the codebook. The missing lives from a paid package is a purchase-fulfillment complaint, not a listed dark pattern.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The reviewer states that earning enough gold through play is not reliable and that buying is sometimes required to continue playing.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone."
  - why: Bonuses expire during real-world time even while the player is absent, imposing a game-controlled usage schedule.

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
The reviewer describes an album-collection goal with only two cards remaining before the grand prize, which supports Complete the Collection. They then purchased an in-app deal advertised as providing new cards but received duplicates instead. The duplicate outcome describes an unwanted reward-delivery result from a card acquisition mechanic, supporting Reward Mania. The review does not explicitly establish random odds, a monetary progress gate, leftover currency, or a purchase-interface manipulation. The mention of promotion through Free Cash concerns external marketing and is out of scope under R13.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The reviewer is pursuing the completion of an in-game card album to obtain its grand prize.
- `P_RewardMania` - ok
  - span: "i bought a deal which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: The card deal delivered unwanted duplicate rewards rather than the needed new cards, describing the reward-delivery mechanic rather than merely the reward's value.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (3)

### `95ddadb3-82cd-4042-8a51-cf8b3ed164c2` - Mech Arena - Shooting Game

> You stuck waiting 30 seconds just to connect to a match. This game makes it seem like they give so many rewards but if all just for show. Its difficult to get weapon upgrades or any percs others you stick battling to win. This kind of games just rob you of your time in my opinion

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `T_Grinding` |
| **spurious** | `T_Grinding` |

**Model analysis**

```
The review describes a 30-second matchmaking connection wait, but this is a service or matchmaking delay rather than an in-game timer that gates play, so it does not qualify as Playing by Appointment. It also describes weapon upgrades and perks as difficult to obtain, requiring the player to keep battling to win them. That identifies repeated gameplay activity being used to obtain progression-related upgrades, which supports Grinding. The statement that rewards are 'just for show' is a general complaint about reward value or presentation and does not identify a qualifying reward-delivery mechanic. No purchase, social, competition, or other dark-pattern mechanic is explicitly described.
```

**Labels assigned**

- `T_Grinding` - **SPURIOUS**
  - span: "Its difficult to get weapon upgrades or any percs others you stick battling to win."
  - why: The player must continue battling repeatedly to win weapon upgrades or perks, emphasizing repetitive effort for progress.

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
The review describes a time-limited card-collection event. The player collects cards toward completing a set and receiving a completion reward, but near the event deadline, card packs stop yielding missing cards, making completion difficult or impossible before the collection expires. This supports Complete the Collection because the player is pursuing a full card set, Reward Mania because card packs deliver variable cards and the player reports needing missing cards from repeated packs, and Playing by Appointment because the expiring collection imposes a game-defined time window and causes the player to miss the reward. The review does not mention payment, so monetary labels are not supported.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion"
  - why: The player is pursuing completion of a card set to obtain its completion reward.
- `P_RewardMania` - **SPURIOUS**
  - span: "include new cards in every card pack because I noticed when one is almost close to completing a set, new cards don't appear again"
  - why: Card packs provide variable card rewards, and the player describes repeated packs failing to deliver the missing cards needed for completion.
- `T_PlayingByAppointment` - ok
  - span: "especially when the set is almost expiring. So after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion"
  - why: The collection has a game-defined expiration window, and failing to complete it before that deadline forfeits the completion reward.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `1da19dbd-f522-43c7-95d7-df59f631cc18` - Total Battle: War Strategy

> They ruined game, there's no more "battle" in total battle with latest update to get rid of open silver. Save your time and money and don't bother. You have to spend to have any meaningful growth and then they go and make it all pointless by getting rid of any player vs player, so it's now just boring farmville. Gotta be the dumbest company i've ever dealt with. They just screwed everyone over who wasted money on this game. Response to developers response..bring back open silver!!!

| | labels |
|---|---|
| gold | `M_PayToProgress` |
| pred | `M_PayToProgress`, `M_PowerCreep` |
| **spurious** | `M_PowerCreep` |

**Model analysis**

```
The review describes a payment-linked progression system: the player says spending is necessary for meaningful growth. It also describes an update that removed open silver and player-versus-player content, making prior paid growth or investment pointless. That is a devaluation of earlier spending caused by an update, supporting Power Creep. The review does not describe current competition because it says player-versus-player play was removed, and it does not provide a repetitive activity, timed wait, social obligation, or specific purchase-interface behavior.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You have to spend to have any meaningful growth"
  - why: The reviewer explicitly states that spending money is required for meaningful in-game progression.
- `M_PowerCreep` - **SPURIOUS**
  - span: "then they go and make it all pointless by getting rid of any player vs player"
  - why: An update removes the activity that gave prior paid growth value, implying that the player's earlier investment has been devalued over time.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_PayToProgress` | 3 | 1 |
| `S_Reciprocity` | 2 | 0 |
| `S_Competition` | 1 | 1 |
| `P_RewardMania` | 1 | 1 |
| `P_AestheticManipulation` | 2 | 0 |
| `P_EasyToGetHardToLose` | 1 | 1 |
| `M_EasyToPurchase` | 1 | 1 |
| `M_WasteAversion` | 1 | 1 |
| `M_IntermediateCurrency` | 2 | 0 |
| `M_PowerCreep` | 0 | 1 |
| `M_Gambling` | 1 | 0 |
| `T_Grinding` | 0 | 1 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |

