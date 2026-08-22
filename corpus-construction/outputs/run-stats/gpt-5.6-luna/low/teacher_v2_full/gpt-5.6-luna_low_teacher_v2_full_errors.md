# Error review - gpt-5.6-luna_low_teacher_v2_full

`gpt-5.6-luna` / reasoning `low` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `6529a474a2b0`  
micro-F1 **0.843** (P 0.875 / R 0.814) - **19 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 3 | said NONE, gold had labels |
| SWAP | 4 | picked different labels than gold |
| MISSED ONLY | 7 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 5 | found all gold, added extras |

## The diagnostic that matters

Of **16** missed labels, **3** (19%) were named in the model's own analysis and dropped anyway; **13** (81%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `S_Reciprocity` | 0 | 2 |
| `P_AestheticManipulation` | 0 | 2 |
| `M_PayToProgress` | 0 | 2 |
| `T_Grinding` | 0 | 1 |
| `M_WasteAversion` | 1 | 0 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `P_RewardMania` | 1 | 0 |
| `T_PlayingByAppointment` | 0 | 1 |
| `M_Gambling` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `T_MandatoryMarathon` | 0 | 1 |
| `M_IntermediateCurrency` | 0 | 1 |
| `M_EasyToPurchase` | 0 | 1 |

## Missed everything (predicted NONE) (3)

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
The review lists desired additions or changes rather than describing currently operating game mechanics: auctions, preventing obstacle removal, an account-switching widget showing upgrade time, and access to advanced troop statistics. The upgrade timer is mentioned only as information the proposed widget should display, not as a complaint about a current time gate or a wait imposed by the game. Under R12, hypothetical or requested features are not coded, so no label applies.
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
The review describes a technical malfunction preventing the player from requesting troops from their clan. This is a social resource-request feature, but the reviewer explicitly attributes its absence to an update and says it needs to be fixed. Under R11, a specific behavior attributed to a bug, error, or technical fault is not coded as a dark pattern. No other mechanic is described.
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
The reviewer describes being unable to advance past a single level for almost two months and says they will uninstall. This establishes blocked or slow progress, but does not describe repetitive actions required for progress, a stated payment gate, or the game extending beyond completion. The proposed daily login rewards are a requested feature, not an existing mechanic, so they are not coded.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (4)

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
The review describes an interface that automatically scrolls to and selects the highest-bet table when the game opens or when the player enters the 1v1 section. This selection is positioned to cause accidental mis-clicks, making players lose their accumulated coins. The reviewer also states that this loss forces players to purchase more coins with real money. The automatic selection and mis-click risk support UI Misdirection. The conversion of real money into coins supports Intermediate Currency, and the stated need to buy coins to continue playing supports Pay to Progress. The review does not explicitly establish a chance-based wager, so Gambling is not assigned.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "forced to buy real ones"
  - why: The phrase implies that players purchase more in-game coins with real money after losing their existing coins.
- `M_PayToProgress` - **SPURIOUS**
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: The interface-induced loss of coins creates a barrier that the review says players must overcome by purchasing more coins to keep playing.
- `M_UIMisdirection` - ok
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins"
  - why: The interface automatically directs the player to the highest-bet table rather than a neutral or lowest-bet option, creating the described accidental mis-click risk.

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
- `M_WasteAversion` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a daily-reward system whose rewards cannot be completed unless the player places a 50,000 bet. This is a daily return incentive with a condition attached, so Daily Rewards applies. The required bet is also a chance-based wagering mechanic using in-game currency; no real-money purchase of that currency is described, so Gambling applies without Intermediate Currency. The comparison between 50,000 required and 40,000 obtainable from timed rewards describes a shortfall, but not a currency amount stranded after a purchase or an item-cost mismatch, so Waste Aversion does not apply.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "unless I bet 50,000"
  - why: The player must wager in-game currency through a betting mechanic to pursue the reward.
- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The game offers daily rewards but requires the player to complete a daily condition to obtain them.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `176aaa1f-d8f9-4a1a-9f29-64902f13be5c` - All in Hole: Black Hole Games

> I would give 5 stars, but I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used.🤨😒🙄😥

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `T_MandatoryMarathon` |
| pred | `M_IntermediateCurrency`, `P_EasyToGetHardToLose` |
| **missed** | `T_MandatoryMarathon` |
| **spurious** | `P_EasyToGetHardToLose` |

**Did the model consider what it missed?**

- `T_MandatoryMarathon` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes accumulated in-game holdings being lost while away: they leave with a full bag and return to find it empty, while coins they had earned or purchased have been consumed. This makes leaving costly because value already held is forfeited or depleted. The mention of purchased coins also establishes that real money can be converted into the game's coin currency, although the review does not describe a timer, daily schedule, or explicit purchase prompt.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "coins that I earned and purchased"
  - why: The reviewer explicitly states that coins are a game currency acquired through purchase, establishing real-money acquisition of virtual currency.
- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used"
  - why: The span implies that leaving the game causes value already accumulated in the bag and coin balance to be forfeited or depleted, making disengagement costly.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `12267c1e-47ba-4984-97c8-768e820ceb1c` - Bingo Blitz™️ - Bingo Games

> not very user-friendly. no apparent reachable goals within a decent amount of time. I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| pred | `M_PayToProgress`, `M_WasteAversion`, `P_CompleteTheCollection`, `T_Grinding` |
| **missed** | `M_EasyToPurchase`, `P_AestheticManipulation` |
| **spurious** | `M_PayToProgress`, `M_WasteAversion` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - never mentioned -> **attention / recall**
- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes repeated bingo rounds undertaken to collect photos and complete a set, which is a collection goal pursued through repetitive play. After a lost round, the game presents a paid-in-coins offer for a missing photo, making payment an alternative route to completing the set and advancing the collection. The reviewer says they spent coins but received neither the promised offer nor photo, so the currency was consumed without obtaining the intended value. The review does not establish that coins were bought with real money, so Intermediate Currency is not assigned. The failure to deliver is described as an outcome of the offer, but no explicit bug or technical fault is named.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "ask me if I want to spend extra coins to claim a photo I don't have to complete the set"
  - why: The game offers spending coins as a way to obtain a missing collection item and complete the set.
- `M_WasteAversion` - **SPURIOUS**
  - span: "I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED"
  - why: Coins are spent on the offer, but the promised photo is not delivered, leaving the spent value wasted.
- `P_CompleteTheCollection` - ok
  - span: "to complete the set"
  - why: The photos form a set that the player is trying to complete.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The reviewer repeatedly plays bingo rounds as the activity needed to collect photos.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (7)

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
The review attributes nearly all described behaviors to bugs, crashing, lag, freezing, and unresponsive controls, so those technical malfunctions do not support dark-pattern labels under R11. It explicitly mentions PvP, which is a game mode involving competition against other players; that functional mechanic remains codable despite the reported lag. Opening gifts and trading with friends are mentioned as activities disrupted by crashes, but no obligation to reciprocate or social recruitment pressure is described.
```

**Labels assigned**

- `S_Competition` - ok
  - span: "the pvp"
  - why: PvP explicitly describes competition against other players, even though the review says the mode is malfunctioning.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fd1230ab-7d12-4aeb-a425-e37ed06bcd5c` - Pokémon GO

> I love this game, just started playing about 2 months ago. Though I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way. I feel taken advantage of. 3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| pred | `P_IllusionOfControl`, `S_FriendSpamImpersonation` |
| **missed** | `P_OptimismAndFrequencyBiases` |

**Did the model consider what it missed?**

- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes purchased Poké Balls being consumed when Pokémon break out of attempted captures, leading the player to buy more. The reviewer is alleging that capture outcomes are manipulated after purchases so that the player depletes the balls faster; this is a claim that the game determines outcomes in a concealed or engineered way, supporting Illusion of Control. The later edit says the displayed review was not written by the reviewer and falsely claimed conversations with other players, which describes a review being posted under the player's identity by someone else, supporting Friend Spam / Impersonation under the destination-of-message rule. The text does not clearly establish that payment is required for progression, nor that real money is converted into currency or wagered in a gambling mechanic.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: The reviewer attributes repeated capture failures and faster ball depletion to a concealed change in outcome determination after purchasing.
- `S_FriendSpamImpersonation` - ok
  - span: "I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE"
  - why: The edit explicitly denies authorship of the review and denies the interactions it reports, implying that a review was posted on the player's behalf.

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
The review describes monetized progression and sticker collection. The reviewer says winning anything costs hundreds of dollars, and specifically states that completing the final one or two stickers requires paying a large amount, making payment the route to completion. The sticker goal is a collection objective, so the review also supports a collection-completion mechanic. The final stickers are portrayed as deliberately unavailable through ordinary play and obtainable through expensive payment, which implies manufactured scarcity tied to purchase. The statements about completing a goal only one time out of one hundred suggest poor odds, but they do not clearly identify a chance-based reward mechanism or wager, so Gambling and Reward Mania are not assigned.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "you will never get the last one or two unless you pay a lot of money to get them"
  - why: The final stickers are described as artificially scarce and tied to an expensive purchase route.
- `M_PayToProgress` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: Completion of the sticker objective is described as unavailable through ordinary play unless the player pays substantially.
- `P_CompleteTheCollection` - ok
  - span: "you will never get the last one or two"
  - why: The reviewer is pursuing the final missing items in a sticker collection.

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

- `T_Grinding` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a lives-based obstacle to progression: the player runs out of lives several times per day while trying to clear levels, and levels take an average of 5–7 days to complete. However, no explicit regeneration timer or required waiting schedule is described, so Playing by Appointment is not assigned. The reviewer explicitly states that buying add-ons is necessary to get through the game and that non-paying play wastes time, which directly describes payment as the route to progress. The money and time already spent are described as wasted after deciding to uninstall, not as investments making it difficult to leave, so Easy to Get, Hard to Lose is not assigned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying."
  - why: The reviewer says continued progress is effectively contingent on buying add-ons, while the unpaid route is excessively difficult and time-consuming.

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
The review describes a sticker-collection system where attempts to obtain stickers frequently produce duplicates, indicating unwanted repeated rewards from a variable or randomized reward pool. The player is trying to complete all sticker sets, so collection completion is an active goal. The review also explicitly says that finishing the sets is unavailable unless the player pays, making payment a progression gate. It does not explicitly state that money is wagered on a chance mechanic, so Gambling is not assigned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: The review explicitly states that completing the sets is blocked unless the player pays.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: The player is pursuing completion of all sticker sets, which is an in-game collection goal.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: Repeated duplicate stickers describe an unwanted, variable reward outcome that sustains attempts to obtain the missing items.

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
The review describes several mechanics and one apparent malfunction. The game consumes or charges gold for extra moves, but the account is too unclear to establish a specific dark pattern beyond the broader payment-for-play complaint. A purchased package failed to deliver its promised lives; because the reviewer attributes this to not receiving what was bought, this is a product/payment error rather than a deliberate design mechanic under R11. Timed bonuses continue expiring while the player is offline, imposing the game’s schedule and making the player return before the timer runs out. The reviewer also says there is sometimes insufficient free gold to continue playing without buying, which describes payment as an alternative to continued progress. Complaints that packages should cost less or not be timed do not independently establish additional labels.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The review states that free gold is sometimes insufficient to continue, making buying necessary for continued play.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone."
  - why: Bonuses expire in real time while the player is away, pressuring the player to play within the timer’s window.

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
The review describes an album-collection mechanic with a grand prize for completion. The player had two cards remaining, purchased a deal that promised new cards, and received duplicates instead. This supports the compulsion to complete a collection and describes unwanted duplicate rewards from a card-acquisition system, which indicates a variable or randomized reward delivery. The mention of promotion through Free Cash is third-party marketing and is out of scope. The review does not explicitly establish a monetary wager or chance mechanic strongly enough for Gambling, and it does not describe leftover currency or a direct progress gate requiring payment.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "two cards left which would grant me the grand prize for completing an album"
  - why: The reviewer is pursuing the completion of an album collection to obtain its grand prize.
- `P_RewardMania` - ok
  - span: "a deal which promised i would get NEW cards, and all i got were useless duplicates"
  - why: The paid card reward delivered unwanted duplicates rather than the needed new cards, describing a reward system whose delivery depends on variable card outcomes.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (5)

### `95ddadb3-82cd-4042-8a51-cf8b3ed164c2` - Mech Arena - Shooting Game

> You stuck waiting 30 seconds just to connect to a match. This game makes it seem like they give so many rewards but if all just for show. Its difficult to get weapon upgrades or any percs others you stick battling to win. This kind of games just rob you of your time in my opinion

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `S_Competition` |
| **spurious** | `S_Competition` |

**Model analysis**

```
The review describes a matchmaking connection wait, but this is a service or matchmaking delay rather than an in-game timer that schedules play, so it does not support Playing by Appointment. It also describes difficulty obtaining weapon upgrades and perks through continued battling, but it does not clearly identify repetitive or tedious activity as the required progression method, so Grinding is not assigned. The references to connecting to a match and battling to win indicate competition against other players. The claim that rewards are merely for show is evaluative and does not name a specific reward-delivery mechanic.
```

**Labels assigned**

- `S_Competition` - **SPURIOUS**
  - span: "connect to a match"
  - why: Connecting to a match indicates participation in competitive gameplay against other players.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `0bc09fc3-6436-4a24-855e-0fdc56887918` - Fishdom

> EDIT 1/17/2023: Customer Service can't make good on 9 diamonds when game element doesn't appear within 5 original moves and 5 additional moves. It is a fun game, you don't have to pay to win. I suggest after this cust. svc experience that you don't buy from this game beyond the pass.Get friends and a team and trade lives.

| | labels |
|---|---|
| gold | `M_RecurringFee`, `S_Reciprocity` |
| pred | `M_RecurringFee`, `M_WasteAversion`, `S_Reciprocity` |
| **spurious** | `M_WasteAversion` |

**Model analysis**

```
The review describes a chance-based game mechanic in which a game element may fail to appear after five original moves and five additional moves, leaving the player disputing a charge or loss of 9 diamonds. This establishes a concrete loss of in-game currency without the expected result, supporting Waste Aversion; it does not clearly establish a wager or a real-money conversion, so Gambling and Intermediate Currency are not assigned. The reference to buying “the pass” describes a paid pass, which supports Recurring Fee. Finally, trading lives with friends is a resource exchange with existing players, supporting Reciprocity.
```

**Labels assigned**

- `M_RecurringFee` - ok
  - span: "you don't buy from this game beyond the pass"
  - why: The review explicitly identifies a paid game pass as a purchase option.
- `M_WasteAversion` - **SPURIOUS**
  - span: "Customer Service can't make good on 9 diamonds when game element doesn't appear within 5 original moves and 5 additional moves"
  - why: The player spent or lost 9 diamonds but did not receive the expected game element, showing realized wasted in-game value.
- `S_Reciprocity` - ok
  - span: "trade lives"
  - why: Trading lives is an explicit resource exchange with friends and a team.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a2ece36d-c527-442d-8f18-9a16b63994c8` - War Robots Multiplayer Battles

> Its a p2w game. The only time you enjoy it is when you're new. As you progress, everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game. If you want to progress without paying money, goodluck! Even if you wanted to do f2p, you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it. Plus the only time you benofit by getting f2p rewards is ads... 💩

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `M_PayToProgress`, `M_PowerCreep`, `T_Advertisement` |
| pred | `M_EasyToPurchase`, `M_PayToProgress`, `M_PowerCreep`, `S_FearOfMissingOutFOMO`, `T_Advertisement` |
| **spurious** | `S_FearOfMissingOutFOMO` |

**Model analysis**

```
The review describes several active game mechanics. The game interrupts access to play with repeated in-app purchase offers, which directly prompts buying before gameplay. Progress is described as effectively requiring payment: free-to-play players cannot progress smoothly or keep up. The shifting meta and requirement to buy the newest bot imply that newer paid content devalues older bots and pressures players to replace them. The review also describes ads as the route to receiving free-to-play rewards, which indicates incentivized ad viewing. The pressure to keep up with the shifting meta additionally reflects fear of falling behind other players.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game"
  - why: Repeated purchase offers appear before the player can access gameplay, directly prompting spending at the point of play.
- `M_PayToProgress` - ok
  - span: "If you want to progress without paying money, goodluck! Even if you wanted to do f2p, you would not be able to keep up"
  - why: The span states that progressing as a free player is not realistically possible.
- `M_PowerCreep` - ok
  - span: "keep up with shifting meta where you have to buy the newest bot with money instead of earning it"
  - why: A shifting meta and the need to buy the newest bot imply that older bots become insufficient as new content is introduced.
- `S_FearOfMissingOutFOMO` - **SPURIOUS**
  - span: "you would not be able to keep up with shifting meta"
  - why: The player is pressured to spend and obtain new bots to avoid being left behind by the changing meta.
- `T_Advertisement` - ok
  - span: "the only time you benofit by getting f2p rewards is ads"
  - why: The review describes ads as the means of obtaining free-to-play rewards, indicating incentivized ad viewing.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `ae3b6309-101e-4320-99b1-aa6795602787` - Genshin Impact

> The rewarding system is just DIABOLICAL, I just finished a 7 hour quest and I barely got any primogems. exploration is debilitating. the character design is as almost lame... especially for the female characters, they all have the same bare legs curse that makes the design uninteresting. it's just a horrible game, this game used to be fine by the ways. for context I've been playing since 2021, 5 years have passed can you imagine ? and there is no resin overflow system. 😭

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `T_PlayingByAppointment` |
| **spurious** | `T_PlayingByAppointment` |

**Model analysis**

```
The review mainly expresses dissatisfaction with low rewards, character aesthetics, and the absence of a resin overflow feature. The seven-hour quest describes a long activity but not repetitive actions required for progress, so it does not establish Grinding or Mandatory Marathon. The complaint that the reward was small concerns reward value rather than an unpredictable or complex delivery mechanism, so it does not establish Reward Mania. The character-design comments are aesthetic preferences and criticism, not aesthetic manipulation. The named resin overflow system refers to storing resin generated over time beyond the normal cap; its absence leaves the game's regenerating resource constrained by a time-based cap, which fits Playing by Appointment. No search was needed to identify the term because the review context and game name make the resin mechanic sufficiently clear.
```

**Labels assigned**

- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "there is no resin overflow system"
  - why: The span implies that resin is a time-regenerating resource whose accumulation is limited, requiring the player to manage play around the game's regeneration schedule.

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
The review describes two current game mechanics. First, progression is effectively monetized: the reviewer says spending is required for meaningful growth, which directly supports Pay to Progress. Second, a latest update removed open silver and player-versus-player activity, making prior spending and progression feel pointless. The removal of PvP itself does not support the Competition label because the review describes competition as absent rather than as a mechanic the game imposes. The search established that open silver is exposed silver that can be targeted or taken by other players, and that it formed part of the game's PvP layer.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You have to spend to have any meaningful growth"
  - why: The reviewer explicitly states that spending money is required for meaningful in-game progression.
- `M_PowerCreep` - **SPURIOUS**
  - span: "They just screwed everyone over who wasted money on this game."
  - why: In the context of the latest update removing open silver and PvP, the span says that previously spent money and its resulting value were rendered pointless.

**Search:** `Total Battle War Strategy "open silver"` -> The search established that open silver is exposed silver that can be targeted or taken by other players and that it formed part of the game's player-versus-player battle layer.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_PayToProgress` | 2 | 2 |
| `M_WasteAversion` | 1 | 2 |
| `S_Reciprocity` | 2 | 0 |
| `P_AestheticManipulation` | 2 | 0 |
| `M_Gambling` | 1 | 1 |
| `T_PlayingByAppointment` | 1 | 1 |
| `M_PowerCreep` | 0 | 1 |
| `S_Competition` | 0 | 1 |
| `P_RewardMania` | 1 | 0 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `T_MandatoryMarathon` | 1 | 0 |
| `M_EasyToPurchase` | 1 | 0 |
| `S_FearOfMissingOutFOMO` | 0 | 1 |
| `T_Grinding` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `M_IntermediateCurrency` | 1 | 0 |

