# Error review - gpt-5.6-luna_medium_teacher_v3_full

`gpt-5.6-luna` / reasoning `medium` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v3_full.txt` sha `a6ae58246360`  
micro-F1 **0.855** (P 0.932 / R 0.791) - **17 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 4 | said NONE, gold had labels |
| SWAP | 2 | picked different labels than gold |
| MISSED ONLY | 8 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 3 | found all gold, added extras |

## The diagnostic that matters

Of **18** missed labels, **5** (28%) were named in the model's own analysis and dropped anyway; **13** (72%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `M_IntermediateCurrency` | 0 | 2 |
| `S_Reciprocity` | 1 | 1 |
| `M_DeceptiveLuxury` | 1 | 1 |
| `S_FriendSpamImpersonation` | 0 | 1 |
| `P_IllusionOfControl` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `M_Gambling` | 1 | 0 |
| `P_AestheticManipulation` | 0 | 1 |
| `T_Grinding` | 1 | 0 |
| `T_MandatoryMarathon` | 0 | 1 |
| `M_PowerCreep` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `P_RewardMania` | 1 | 0 |
| `M_PayToProgress` | 0 | 1 |

## Missed everything (predicted NONE) (4)

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
The review mainly proposes feature changes rather than describing manipulative mechanics currently present. It asks for auctions using in-game currency, removal of an existing option to delete a decorated obstacle, an account-switching and upgrade-timer widget, and access to advanced troop statistics. These requests do not establish any codebook label. The only current behavior clearly mentioned is that a decorated obstacle can be removed, but that is a gameplay option without a supported dark-pattern mechanic.
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
The reviewer is asking for a possible future save or account-preservation feature, stating that deleting the game would lose in-game purchases and accumulated progress. The saving behavior is presented as a suggestion rather than a clearly encountered current mechanic, so R12 prevents coding the proposed feature. Although the reviewer mentions purchases and hard work, they do not say that these investments are currently making them continue playing or preventing them from leaving; the concern is hypothetical loss after deletion. No label is supported.
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
The reviewer describes a clan troop-request feature, which would ordinarily involve requesting resources from existing players and could support Reciprocity. However, the feature is said to have stopped working after an update and the reviewer explicitly asks for it to be fixed. Because the only described behavior is attributed to a technical fault, R11 suppresses the otherwise implied social-transfer label.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `176aaa1f-d8f9-4a1a-9f29-64902f13be5c` - All in Hole: Black Hole Games

> I would give 5 stars, but I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used.🤨😒🙄😥

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `T_MandatoryMarathon` |
| pred | _NONE_ |
| **missed** | `M_IntermediateCurrency`, `T_MandatoryMarathon` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**
- `T_MandatoryMarathon` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a persistence or state-loss problem: after leaving with a full bag, they return to find the bag empty and both earned and purchased coins consumed. This is a reported loss of stored items and currency, not a deliberate inventory-capacity rule, purchase mechanic, or retention design. The text does not explicitly name a bug, but the described disappearance is a technical malfunction rather than a qualifying dark-pattern mechanic, and no label has a supported exact span.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (2)

### `fd1230ab-7d12-4aeb-a425-e37ed06bcd5c` - Pokémon GO

> I love this game, just started playing about 2 months ago. Though I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way. I feel taken advantage of. 3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| pred | `M_PayToProgress` |
| **missed** | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `P_IllusionOfControl` - never mentioned -> **attention / recall**
- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**
- `S_FriendSpamImpersonation` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes Poké Balls being consumed more quickly because Pokémon repeatedly break out during captures, leaving the player needing to buy more Balls. This is a resource-consumption pattern tied to continued gameplay, and the reviewer explicitly says purchasing more is necessary, which supports Pay to Progress. The review does not establish rigged capture outcomes; repeated breakouts and agreement from other players are not enough to show hidden manipulation. It also does not describe leftover currency, gambling, a purchase prompt, or a currency conversion. The final edit disputes authorship of the earlier text, but it does not identify a separate in-game mechanic.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: The consumable capture items are depleted and the reviewer states that purchasing more is required to continue the capture activity.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fdef27f2-9a21-4b8e-a04c-7a4753e0fb07` - 8 Ball Pool

> The game is great, but the user interface is completely rigged. Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins and are forced to buy real ones. ​We need a "Default Table Lock" or the game should always open the lowest bet table by default, not the highest! Fix this scammy feature. Giving 1 star

| | labels |
|---|---|
| gold | `M_Gambling`, `M_IntermediateCurrency`, `M_UIMisdirection` |
| pred | `M_IntermediateCurrency`, `M_PayToProgress`, `M_UIMisdirection` |
| **missed** | `M_Gambling` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_Gambling` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a deliberate interface behavior: opening the game or the 1v1 section automatically scrolls to and selects the highest-stakes table available, rather than the lowest or a neutral option. This steers the player toward spending more in-game coins and creates accidental mis-clicks that can make the player lose their coin balance. The reviewer then says that, after those losses, players are forced to buy more coins with real money, making payment an alternative required to continue playing. The interface manipulation itself is not an accidental real-money purchase, so M_EasyToPurchase is not supported. No chance-based outcome is described, so Gambling does not apply.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "forced to buy real ones"
  - why: The phrase describes purchasing additional in-game coins with real money, which is a real-money-to-virtual-currency conversion.
- `M_PayToProgress` - **SPURIOUS**
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: After the interface-induced coin loss, the review states that players must buy more coins with real money to keep playing.
- `M_UIMisdirection` - ok
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins"
  - why: The interface automatically steers the player toward the highest-cost table, directing selection away from the safer lower-bet option and facilitating accidental mis-clicks.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (8)

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
The review attributes the inability to open gifts, trade, catch Pokémon, and complete battles to crashing, lag, freezing, and unresponsive controls. Those technical faults do not support dark-pattern labels for the affected behaviors. The review does explicitly describe PvP, including an opponent attacking, which indicates competition as an underlying game mechanic.
```

**Labels assigned**

- `S_Competition` - ok
  - span: "the pvp & rockets battles"
  - why: PvP battles place the player against an opponent, which is competition between players.

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

- `M_PayToProgress` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a chance-based game outcome system that they believe is deliberately unfavorable: the RNG is said to be “obviously against you,” which is an allegation that the game manipulates or predetermines outcomes rather than merely producing an unlucky streak. They also describe an in-game cost of 2200 at around level 100 and rewards that barely repay that cost, but this is an economy/value complaint rather than an explicit payment gate or real-money conversion. Saying the game is not rewarding without spending actual money does not by itself establish that payment is required for progress. No label is assigned for the low rewards because Reward Mania concerns how rewards are delivered, not simply their size or value.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "the rng is so obviously against you it's crazy"
  - why: The reviewer alleges that the game’s random outcomes are systematically manipulated against the player, describing concealed outcome determination rather than an ordinary losing streak.

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

- `M_DeceptiveLuxury` - considered and rejected -> **rule interpretation**
- `P_RewardMania` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a sticker-collection goal that is effectively gated by expensive payment: the reviewer says the final stickers cannot be obtained without paying a lot, and that winning anything may cost hundreds of dollars. This supports Pay to Progress because payment is presented as necessary to advance or complete goals, and Complete the Collection because obtaining the last stickers is the stated objective. The review does not clearly describe a chance-based mechanic, a specific artificial scarcity rule, or a reward-delivery system, so Gambling, Deceptive Luxury, and Reward Mania are not assigned. The complaint about being required to give five stars to write a review concerns the store-review process rather than an in-game mechanic and is out of scope.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: The reviewer states that completing sticker progress is unavailable through the ordinary route unless substantial payment is made.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two"
  - why: The reviewer is pursuing a complete sticker set, with the remaining stickers serving as the barrier to collection completion.

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
The reviewer describes a very high level and slow advancement, but a high level and long time per level do not by themselves establish Grinding or Infinite Treadmill. Running out of lives several times daily describes resource depletion, but no refill timer or waiting schedule is stated, so it does not establish Playing by Appointment. The explicit mechanic is that buying add-ons is necessary to get through the levels; the unpaid route is described as unworkable, which is Pay to Progress. The reviewer says they are uninstalling despite wasted time and money, so the text does not show accumulated investment making it difficult to leave and does not support Easy to Get, Hard to Lose.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying."
  - why: The reviewer states that continued or workable progress requires buying add-ons, while the unpaid route is excessively difficult and time-consuming.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a2ece36d-c527-442d-8f18-9a16b63994c8` - War Robots Multiplayer Battles

> Its a p2w game. The only time you enjoy it is when you're new. As you progress, everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game. If you want to progress without paying money, goodluck! Even if you wanted to do f2p, you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it. Plus the only time you benofit by getting f2p rewards is ads... 💩

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `M_PayToProgress`, `M_PowerCreep`, `T_Advertisement` |
| pred | `M_EasyToPurchase`, `M_PayToProgress`, `T_Advertisement` |
| **missed** | `M_PowerCreep` |

**Did the model consider what it missed?**

- `M_PowerCreep` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes progression and competitive viability as dependent on spending: the player says free-to-play progression is not realistically possible and that keeping up with the changing meta requires buying the newest bot rather than earning it. It also describes purchase offers appearing on every login and blocking access to gameplay until they are dealt with, which is an in-game purchase solicitation that intercepts play. Finally, the mention of benefiting from free-to-play rewards through ads indicates rewarded or incentivized ad viewing. The review does not clearly establish currency conversion, artificial scarcity, or purchased items losing value after acquisition.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game."
  - why: Purchase offers appear at login and intercept the player before gameplay can begin, requiring the player to deal with them to continue.
- `M_PayToProgress` - ok
  - span: "If you want to progress without paying money, goodluck! Even if you wanted to do f2p, you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it."
  - why: The review contrasts an inadequate free route with paying money to obtain the newest bot and remain able to progress or keep up.
- `T_Advertisement` - ok
  - span: "the only time you benofit by getting f2p rewards is ads"
  - why: The span links free-to-play rewards with ads, implying that the player must view or engage with advertisements to receive those rewards.

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
The reviewer describes a collection goal involving photos and explicitly plays round after round to complete the set, which supports both repetitive grinding and collection completion. After losing a round, the game presents an offer to spend extra coins for a missing photo; this is a purchase prompt triggered at a point of failure and directly tied to advancement toward the set, supporting Easy to Purchase. The review does not clearly establish that real money is converted into coins, nor does it describe a chance-based reward mechanic, deliberate scarcity, or a reachable end state being continually extended. The failure to receive the promised photo is reported as a reward-delivery problem, not as a clear intentional design mechanic.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have"
  - why: A purchase prompt appears immediately after a lost round and offers a paid route to obtain the missing collection item.
- `P_CompleteTheCollection` - ok
  - span: "to complete the set"
  - why: The reviewer is pursuing completion of an in-game set of photos.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The reviewer names repeated rounds as the activity required to make progress toward collecting photos.

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
The review describes a sticker-collection system in which sticker drops repeatedly produce duplicates, indicating an unwanted or variable reward-delivery mechanic. It also describes the player's goal of completing all sticker sets, which supports collection compulsion. Finally, completion is explicitly blocked unless the player pays, making payment a requirement for progress. No real-money-to-currency conversion, limited-time scarcity, or specific purchase interface is described.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: The review explicitly states that progressing to complete the sets is unavailable without payment.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: The player is pursuing completion of all in-game sticker sets.
- `P_RewardMania` - ok
  - span: "getting stickers. always get duplicates."
  - why: Sticker acquisition repeatedly delivers unwanted duplicate rewards, describing the reward-delivery pattern rather than merely the value of the stickers.

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
The review describes several mechanics and one apparent purchase-delivery problem. Timed bonuses continue expiring while the player is away, forcing the player to return according to the game's clock rather than their own schedule. The reviewer also says there are times when they cannot play without buying, indicating that payment is required to maintain access or progress. The missing lives from a purchased package appears to be a fulfillment error, and the complaint about being charged for moves does not clearly identify a supported dark-pattern mechanic such as an accidental purchase or wasted inventory currency. The requests for cheaper packages and untimed purchases do not add labels beyond the existing timed-bonus behavior.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The free route sometimes provides insufficient gold to continue playing, making buying necessary for continued access.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone."
  - why: Bonuses expire according to an in-game timer while the player is absent, imposing the game's schedule and causing rewards to be lost.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (3)

### `95ddadb3-82cd-4042-8a51-cf8b3ed164c2` - Mech Arena - Shooting Game

> You stuck waiting 30 seconds just to connect to a match. This game makes it seem like they give so many rewards but if all just for show. Its difficult to get weapon upgrades or any percs others you stick battling to win. This kind of games just rob you of your time in my opinion

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `S_Competition` |
| **spurious** | `S_Competition` |

**Model analysis**

```
The review describes a 30-second matchmaking connection delay, but this is a service or queue wait rather than an in-game timer that deliberately gates play, so it does not support Playing by Appointment. The reviewer also says that obtaining weapon upgrades and perks requires battling to win, which describes competitive play against other players. The claim that rewards are only for show is too vague to establish a specific reward-delivery or deceptive-interface mechanic, and the general complaint about wasted time is not itself a labelable mechanic.
```

**Labels assigned**

- `S_Competition` - **SPURIOUS**
  - span: "battling to win"
  - why: The span describes competing in battles to win, indicating that the game makes players compete against others.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b93c432d-19c0-4c6c-a2d4-bb9b21a436f3` - Dice Dreams™️

> A literal brain-rot game no wonder why they're tryna promote it through Free Cash. Also if you're thinking of making in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates! A real SCAM. Play it if u want but there are games that are actually good also, DON'T GET IN-APP PURCHASES!

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_PayToProgress`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania` |
| **spurious** | `M_PayToProgress` |

**Model analysis**

```
The review describes an in-game purchase offer tied to album completion. The player was two cards short of the grand prize, paid for a deal that promised new cards, and received duplicate cards instead. This supports Pay to Progress because payment was used to advance toward completing the album, Complete the Collection because the player was pursuing the full album, and Reward Mania because the purchase delivered unwanted duplicates from a card-reward system. The promise of NEW cards also describes misleading purchase wording, supporting Aesthetic Manipulation. The mention of promoting the game through Free Cash concerns out-of-game marketing and is excluded under R13.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "I had two cards left which would grant me the grand prize for completing an album, so i bought a deal"
  - why: The player paid for a deal to obtain the remaining cards needed to advance toward the album-completion reward.
- `P_AestheticManipulation` - ok
  - span: "a deal which promised i would get NEW cards"
  - why: The purchase offer's wording represented the deal as providing new cards, while the player reports receiving duplicates instead.
- `P_CompleteTheCollection` - ok
  - span: "two cards left which would grant me the grand prize for completing an album"
  - why: The player is pursuing completion of an album collection and its completion reward.
- `P_RewardMania` - ok
  - span: "i bought a deal which promised i would get NEW cards, and all i got were useless duplicates"
  - why: The reward system delivered duplicate cards instead of the desired new cards, describing an unwanted outcome in a variable card-reward pool.

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
The review describes two current design behaviors and one update-driven consequence. First, the reviewer says spending is necessary for meaningful growth, which is payment tied directly to progression. Second, the latest update removed open silver and player-versus-player battle, but those are described as removed features rather than mechanics currently operating, so Competition is not coded. The reviewer also says the update made prior spending pointless: money invested in the game was devalued after the change, which supports Power Creep. The statement that players 'wasted money' describes loss after the fact, not continued retention caused by investment, so Easy to Get, Hard to Lose is not assigned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You have to spend to have any meaningful growth"
  - why: The reviewer explicitly states that spending money is required for meaningful in-game progression.
- `M_PowerCreep` - **SPURIOUS**
  - span: "then they go and make it all pointless by getting rid of any player vs player"
  - why: The update is described as making prior investments and progression pointless, meaning previously purchased value was devalued after acquisition.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_PayToProgress` | 1 | 3 |
| `S_Reciprocity` | 2 | 0 |
| `M_DeceptiveLuxury` | 2 | 0 |
| `M_IntermediateCurrency` | 2 | 0 |
| `M_PowerCreep` | 1 | 1 |
| `T_Grinding` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `P_EasyToGetHardToLose` | 1 | 0 |
| `S_FriendSpamImpersonation` | 1 | 0 |
| `S_Competition` | 0 | 1 |
| `P_RewardMania` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `M_Gambling` | 1 | 0 |
| `P_AestheticManipulation` | 1 | 0 |
| `P_IllusionOfControl` | 1 | 0 |
| `T_MandatoryMarathon` | 1 | 0 |

