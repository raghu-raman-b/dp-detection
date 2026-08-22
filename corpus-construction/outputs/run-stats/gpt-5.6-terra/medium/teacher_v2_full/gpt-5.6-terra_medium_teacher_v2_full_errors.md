# Error review - gpt-5.6-terra_medium_teacher_v2_full

`gpt-5.6-terra` / reasoning `medium` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `6529a474a2b0`  
micro-F1 **0.805** (P 0.877 / R 0.744) - **21 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 5 | said NONE, gold had labels |
| SWAP | 5 | picked different labels than gold |
| MISSED ONLY | 8 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 3 | found all gold, added extras |

## The diagnostic that matters

Of **22** missed labels, **8** (36%) were named in the model's own analysis and dropped anyway; **14** (64%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `S_Competition` | 3 | 0 |
| `M_Gambling` | 1 | 1 |
| `P_AestheticManipulation` | 0 | 2 |
| `M_WasteAversion` | 1 | 1 |
| `M_DeceptiveLuxury` | 0 | 2 |
| `S_Reciprocity` | 0 | 2 |
| `T_MandatoryMarathon` | 0 | 1 |
| `M_UIMisdirection` | 0 | 1 |
| `P_IllusionOfControl` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `T_Grinding` | 1 | 0 |
| `M_PayToProgress` | 1 | 0 |
| `M_EasyToPurchase` | 0 | 1 |
| `M_IntermediateCurrency` | 1 | 0 |

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
The review is primarily a feature request list: auctions using in-game currency, preventing removal of converted decorations, an account-switching widget that displays upgrade time remaining, and an option to hide advanced troop statistics. Although it refers to time left for upgrades, it does not describe the upgrade timer as a barrier requiring the player to wait to play or progress, nor does it mention paying to skip it. The requested auction and interface changes are not evidence that such mechanics currently exist. No codable dark-pattern mechanic is explicitly described.
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
- `S_Reciprocity` - never mentioned -> **attention / recall**

**Model analysis**

```
The review attributes every described problem to bugs, crashes, lag, freezing, and unresponsive controls after an update. It mentions trading with friends, but only as a feature made unusable by crashes; it does not describe sending resources, social obligation, competition design, or any deliberate monetization or retention mechanic. Under R11, technical faults do not establish dark-pattern labels.
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
The reviewer describes an inability to request troops from their clan after an update and explicitly says it needs to be fixed. This attributes the behavior to a technical fault rather than a deliberate game design mechanic. Although requesting troops could ordinarily involve a social resource-transfer feature, the review does not describe that mechanic operating; it reports that it is broken. Under R11, no dark-pattern label is assigned for the bug.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `2414fb3d-38e2-4e14-a8af-925f764d2abd` - Match Masters

> Love the game its very addictive and the upgrades are okay but I think you should have a way to trade stickers with players in the game within the app because everybody is not on Facebook. I believe if i purchase a booster i should be able to use it if another player challenge me to a game.

| | labels |
|---|---|
| gold | `S_Competition` |
| pred | _NONE_ |
| **missed** | `S_Competition` |

**Did the model consider what it missed?**

- `S_Competition` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer praises the game and calls it addictive, but tone and general addictiveness alone are not mechanics under R2. They request an in-app way to trade stickers because not everyone uses Facebook; this is a proposed feature rather than an existing mechanic, and no actual resource exchange is described as currently occurring. They also say a purchased booster should be usable when challenged by another player, which expresses dissatisfaction with an existing restriction on booster use, but does not describe payment being required for progress, a purchase-friction mechanism, competition design, or another listed pattern.
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
The review mainly describes a mismatch between the game's external advertisements and its actual gameplay: the ads depict physics puzzles, while the installed game is primarily a strategy game with occasional puzzles. Under R13, misleading advertising seen before installation is outside the unit and does not trigger T_Advertisement. The reviewer calls the strategy activities "chores" required to reach puzzles, but does not describe a repeated task cycle, replaying, farming loop, or other explicit repetitive activity required for progression, so T_Grinding is not established.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (5)

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
The reviewer describes a default interface behavior in the 1v1 menu: it automatically scrolls to and selects the highest-stakes table their coin balance allows. They state that this produces accidental taps and consumes accumulated coins, after which players must buy more coins with real money to keep playing at those stakes. This supports UI Misdirection because the default selection steers the player toward the costly option and facilitates accidental selection. It also supports Pay to Progress because depleted coins are described as forcing purchases to continue, and Intermediate Currency because the review explicitly describes buying coins with real money. The review does not describe a chance-based wager, only a high-stakes game table, so Gambling is not assigned.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "forced to buy real ones"
  - why: In context, "real ones" refers to coins purchased with real money, establishing a real-money-to-in-game-currency transaction.
- `M_PayToProgress` - **SPURIOUS**
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: The reviewer describes coin loss as making players buy more in order to continue playing.
- `M_UIMisdirection` - ok
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks"
  - why: The highest-cost table is automatically selected, which the reviewer says is designed to cause accidental taps rather than allow a deliberate choice.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `cc714d17-863c-4ebd-b14f-989ba17c71c4` - Dice Dreams™️

> I played this game on a different profile. the only reason I gave it five stars is because if you don't it won't let you write a review. if you want to win anything on this game it will cost hundreds of dollars. on the stickers you will never get the last one or two unless you pay a lot of money to get them. this is not a game you want to get addicted to unless you have a endless bank account. it may let you complete a goal maybe one out of hundred times.dont get your hopes up.

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury`, `M_PayToProgress`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_Gambling`, `M_PayToProgress`, `P_CompleteTheCollection`, `P_RewardMania` |
| **missed** | `M_DeceptiveLuxury` |
| **spurious** | `M_Gambling` |

**Did the model consider what it missed?**

- `M_DeceptiveLuxury` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes progression and completion being monetized. They say winning costs hundreds of dollars, and specifically that the final one or two stickers needed for a sticker set are effectively unavailable unless the player pays heavily. In Dice Dreams, stickers are collectible items used to complete album sets, so the missing stickers describe an incomplete collection rather than a generic game objective. The statement that the game may permit completing a goal only "one out of hundred times," read with paying heavily to get the missing stickers, describes a low-probability reward path with a monetary stake. The review does not describe a subscription, purchase interface, time gate, or a specific scarcity offer.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them."
  - why: The paid route to obtain the final stickers is described alongside an extremely low completion rate, establishing a monetary stake in a chance-based reward pursuit.
- `M_PayToProgress` - ok
  - span: "if you want to win anything on this game it will cost hundreds of dollars."
  - why: The reviewer states that winning or advancing in the game requires spending substantial real money.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them."
  - why: The reviewer describes being held short of the final items required to complete a sticker collection.
- `P_RewardMania` - ok
  - span: "it may let you complete a goal maybe one out of hundred times."
  - why: The claimed one-in-a-hundred completion outcome describes highly unpredictable reward delivery sustaining repeated attempts.

**Search:** `Dice Dreams stickers how get stickers complete album official` -> Dice Dreams support establishes that stickers are collectible items in Sticker Albums and that collecting stickers completes sets/albums for rewards; stickers are obtained through packs, events, and special offers.

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
The reviewer describes a loss that occurs when they leave the game: a full bag is emptied and coins they had both earned and bought are gone upon returning. This makes leaving costly because accumulated resources are forfeited outside the player's active play. The wording also says coins were purchased, which describes acquiring the in-game currency rather than merely spending it within the game.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "coins that I earned and purchased"
  - why: The reviewer distinguishes coins they earned from coins they purchased, indicating that the in-game currency can be acquired through purchase.
- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used."
  - why: Returning after leaving means forfeiting accumulated bag contents and coins, so resources already obtained raise the cost of disengaging.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `12267c1e-47ba-4984-97c8-768e820ceb1c` - Bingo Blitz™️ - Bingo Games

> not very user-friendly. no apparent reachable goals within a decent amount of time. I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| pred | `M_PayToProgress`, `P_CompleteTheCollection`, `T_Grinding` |
| **missed** | `M_EasyToPurchase`, `P_AestheticManipulation` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - never mentioned -> **attention / recall**
- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a collection mechanic in which they repeatedly play bingo rounds to obtain missing “photos” needed to finish a set. The game also presents a coin-cost offer after losses to obtain a missing photo, making a paid in-game-resource route part of pursuing completion. The review says they have wasted money, but it does not explicitly state that real money was exchanged for coins, so Intermediate Currency cannot be assigned. The claimed failure to receive a promised photo may be a malfunction or non-delivery issue; it does not establish a deliberate dark-pattern mechanic on its own.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set"
  - why: The game offers spending as the route to obtain a missing collection item and advance toward completing the set.
- `P_CompleteTheCollection` - ok
  - span: "claim a photo I don't have to complete the set"
  - why: The mechanic explicitly frames obtaining missing photos as necessary to finish a collection set.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The reviewer identifies repeatedly playing the same rounds as the activity required to make progress toward collecting photos.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b93c432d-19c0-4c6c-a2d4-bb9b21a436f3` - Dice Dreams™️

> A literal brain-rot game no wonder why they're tryna promote it through Free Cash. Also if you're thinking of making in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates! A real SCAM. Play it if u want but there are games that are actually good also, DON'T GET IN-APP PURCHASES!

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_Gambling`, `P_CompleteTheCollection`, `P_RewardMania` |
| **missed** | `P_AestheticManipulation` |
| **spurious** | `M_Gambling` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a sticker-album collection that awards a grand prize when completed. They were two cards short, then spent real money on a deal intended to deliver missing cards; instead, the deal produced duplicate cards. The game's official support materials establish that its sticker packs have odds-based contents and can yield duplicates, so the paid deal is a real-money chance-based reward purchase. The review therefore describes a collection-completion goal, a variable-reward card-pack system, and a monetary stake in that random reward system. It does not establish Pay to Progress separately because the payment is used within the chance-based card acquisition mechanic rather than reliably unlocking progress.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: The reviewer spent real money on a card deal whose chance-based contents yielded unwanted duplicates, making this a paid wager for a prize.
- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The reviewer is pursuing the final missing items needed to complete an album and receive its completion prize.
- `P_RewardMania` - ok
  - span: "all i got were useless duplicates!"
  - why: The purchased card deal delivered duplicate cards rather than the needed ones; the search established Dice Dreams sticker packs are odds-based and can produce duplicates.

**Search:** `Dice Dreams cards albums new cards deal duplicates` -> Dice Dreams support states that sticker packs have odds-based contents, may yield duplicates, and that packs marked "new" guarantee a missing sticker only of the specified type. ([support.dicedreams.com](https://support.dicedreams.com/hc/en-us/articles/24098716134163-I-was-assured-a-Guaranteed-NEW-Sticker-but-I-received-a-duplicate-Why?utm_source=openai))

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (8)

### `b98d7e75-73da-4591-b23e-1a2951bfd856` - Township

> I like this game a lot, but recently after seeing the ads, there is no way to close it. No cross mark on the screen , if you try to click anywhere on the screen it takes you to store. If you go back to game it is still stuck in the last sceeen of the ad. You have to kill the game to come out of the ad screen , so frustrating!!!

| | labels |
|---|---|
| gold | `M_UIMisdirection`, `T_Advertisement` |
| pred | `T_Advertisement` |
| **missed** | `M_UIMisdirection` |

**Did the model consider what it missed?**

- `M_UIMisdirection` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes an in-game advertisement that cannot be dismissed normally. The ad has no close control, taps redirect the player to a store, and returning leaves the game on the ad screen, so the player must force-close the app. This directly describes compelled exposure to ads. Although the ad screen also appears to malfunction after returning, the forced, non-dismissible ad behavior itself is described as part of the encountered design.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "recently after seeing the ads, there is no way to close it. No cross mark on the screen , if you try to click anywhere on the screen it takes you to store."
  - why: The absence of a close control and taps routing to the store describe an ad the player is compelled to remain in rather than freely dismiss.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fd1230ab-7d12-4aeb-a425-e37ed06bcd5c` - Pokémon GO

> I love this game, just started playing about 2 months ago. Though I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way. I feel taken advantage of. 3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| pred | `S_FriendSpamImpersonation` |
| **missed** | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases` |

**Did the model consider what it missed?**

- `P_IllusionOfControl` - never mentioned -> **attention / recall**
- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**

**Model analysis**

```
The final edit explicitly disavows the earlier gameplay and purchasing claims: the reviewer says they did not write the review and did not make the stated claims about other players. Those earlier statements therefore cannot reliably describe game mechanics. What the reviewer does clearly describe is that a review appeared under their identity without their authorship, which is the game acting through the player's account/identity by posting content on their behalf.
```

**Labels assigned**

- `S_FriendSpamImpersonation` - ok
  - span: "I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE"
  - why: The reviewer reports that a review containing statements they did not make was posted under their identity, indicating impersonation.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `5e6a5625-5291-4f0e-897c-1b63c1a26494` - MONOPOLY GO!

> I loved this game until the new season started. Suddenly I get no rewards for inviting friends and getting them to join facebook. I am struggling to get dices and when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way... And today. Well, I cannot log in to the game at all. It keeps giving me an internet connection error which is absolute nonsense. I have connected to 3 different wifi connections. BS!!😡

| | labels |
|---|---|
| gold | `M_Gambling`, `P_RewardMania`, `S_ForcedFellowship` |
| pred | `P_RewardMania`, `S_ForcedFellowship` |
| **missed** | `M_Gambling` |

**Did the model consider what it missed?**

- `M_Gambling` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes two functional game mechanics and one technical problem. First, the game rewards players for recruiting new friends through Facebook, and the reviewer says those rewards have stopped; this is an invite-for-reward recruitment mechanic. Second, the reviewer reports receiving only duplicate stickers. A search was needed to resolve whether Monopoly GO stickers are randomised rewards; the official help result establishes that duplicate stickers occur because the content is random. This supports the unpredictable/duplicate reward-delivery pattern. The inability to log in is explicitly attributed to an internet-connection error, so it is a technical fault and does not receive a dark-pattern label. The lack of dice, failed max-bet outcomes, and absence of shutdowns or bank heists describe an unlucky run, but do not assert manipulated odds or a paid stake.
```

**Labels assigned**

- `P_RewardMania` - ok
  - span: "Stickers are duplicates all the way..."
  - why: Monopoly GO's sticker content is random, so repeated duplicate stickers describe unpredictable reward delivery from that randomised pool.
- `S_ForcedFellowship` - ok
  - span: "I get no rewards for inviting friends and getting them to join facebook."
  - why: The span describes in-game rewards tied to bringing new friends into the game through Facebook.

**Search:** `MONOPOLY GO stickers duplicate sticker packs random rewards` -> The official Monopoly GO help result states that players get many duplicate stickers because sticker content is random.

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
The review describes an event structure in which spending, rather than skill, determines whether a player can win. The reviewer explicitly calls it “pay to play” and “pay to win,” and gives a claimed spending total required to win a recent event. Although they call the game a “grinder,” they do not identify a repeated task that must be performed to progress, so Grinding is not supported. The reference to winning an event does not clearly establish direct competition against other players.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Zero skill pay to play. Zero skill pay to win. Calculated total spent on last event was 30k to win."
  - why: The span explicitly states that spending money is necessary to play effectively and to gain the advantage required to win an event.

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
The reviewer describes a changed daily-reward system in which completing the daily rewards now requires betting 50,000. They also describe a timed-reward source that yields only 40,000, leaving them unable to meet that daily requirement without paying. This explicitly names a daily reward/task mechanism and the consequence that the daily rewards cannot be completed. Although payment is mentioned, the review does not establish that paying is required for overall game progression rather than only for this optional daily-reward completion, so Pay to Progress is not assigned. The timed rewards do not independently show a progression gate beyond the daily-reward mechanism.
```

**Labels assigned**

- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards."
  - why: The span explicitly describes a daily-reward completion requirement that prevents the player from obtaining that day's daily rewards.

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
The reviewer describes an inventory-capacity barrier at higher levels: most board and refrigerator spaces are occupied by generator parts and valuable high-level items that cannot yet be merged or safely discarded. They state that they cannot store items and continue playing unless they spend real money to buy parts, making payment the stated alternative to being blocked. The review gives concrete capacity counts, but it does not say that any item has actually been deleted, forfeited, or that storage capacity itself was purchased, so the stricter Waste Aversion requirement for realized stranded or sacrificed value is not met.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Not enough slots to store and play without spending $$ to buy parts."
  - why: The reviewer explicitly says that continuing to store items and play is blocked unless they spend money on parts.

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
The reviewer describes a sticker-collection system in which earned stickers repeatedly duplicate instead of filling missing slots, making completion of every set difficult. The stated alternative is paying: the game allegedly does not allow the player to finish all sets without payment. This supports a collection-completion compulsion, a variable/random reward delivery mechanism through duplicates, and a payment gate on completing the sets. It does not explicitly say that money buys random attempts, so Gambling is not assigned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: The review explicitly states that completing the sticker sets is unavailable unless the player pays.
- `P_CompleteTheCollection` - ok
  - span: "getting stickers. always get duplicates. never lets you finish all the sets"
  - why: The player is pursuing completion of sticker sets and identifies missing completion as the central obstacle.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: Repeated duplicate stickers imply a variable sticker-reward pool that delivers unwanted repeated items instead of the missing ones.

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
The review describes several separate problems. First, it reports being charged in-game gold incorrectly for moves and not receiving purchased lives; both are presented as faulty transactions or missing content, so they are treated as technical/transaction errors rather than deliberate mechanics. The review also describes timed bonuses and a purchased package expiring while the player is offline, which imposes the game's schedule on use of already obtained benefits. Finally, the reviewer says they cannot earn enough gold to keep playing without sometimes buying, establishing that payment is an alternative required for continued play/progression. The text does not clearly establish that real money is converted specifically into gold, so Intermediate Currency is not assigned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The reviewer states that earned gold is insufficient to continue playing smoothly, making purchases necessary at times to keep playing.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone."
  - why: The bonuses expire on the game's timer even while the player is absent, pressuring use according to the game's schedule rather than the player's own time.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (3)

### `b2dc0bc8-8ebe-4c48-bc05-38d0d65acb84` - Last War:Survival Game

> It's a nice game, but it's set up in a pay to win way. I played for 10 days, and the update times for your base are becoming ridiculous. Everything scales endlessly, there is kinda no point to look forward to, just more grind. The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff. Alliances are also weird, with the top ones dictating what to develop, what to rush, etc. If you are not in one then you get attacked and bullied. Not a great experience.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_UIMisdirection`, `S_Competition`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| pred | `M_PayToProgress`, `M_UIMisdirection`, `S_Competition`, `T_Grinding`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| **spurious** | `T_Grinding` |

**Model analysis**

```
The review describes several active systems. Base upgrades take increasingly long, which imposes in-game timers on advancement. The reviewer says the game is pay-to-win and that the confusing, overwhelming interface is intentionally designed to make purchases feel necessary, describing payment-linked advantage and purchase-oriented UI obstruction. They also describe a game whose scaling continues endlessly with only further grinding ahead, rather than an attainable endpoint. Finally, alliance membership is effectively required to avoid attacks and bullying; this establishes player-versus-player competition, but the review does not state that attackers receive a specific reward for bullying or that the player is obligated to keep playing for allies.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "it's set up in a pay to win way"
  - why: The reviewer explicitly describes spending as conferring an in-game winning advantage.
- `M_UIMisdirection` - ok
  - span: "The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff."
  - why: The span attributes the confusing interface design to steering the player toward purchases.
- `S_Competition` - ok
  - span: "If you are not in one then you get attacked and bullied."
  - why: The game places players in adversarial conflict with other players through attacks.
- `T_Grinding` - **SPURIOUS**
  - span: "Everything scales endlessly, there is kinda no point to look forward to, just more grind."
  - why: The reviewer describes continued progress as requiring more repetitive grinding.
- `T_InfiniteTreadmill` - ok
  - span: "Everything scales endlessly, there is kinda no point to look forward to, just more grind."
  - why: The game is described as scaling endlessly, with no meaningful attainable endpoint.
- `T_PlayingByAppointment` - ok
  - span: "the update times for your base are becoming ridiculous"
  - why: Base-update times are in-game build/upgrade timers that make advancement wait on the game's schedule.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `32c623b4-0249-469e-968c-94f60c7fe3c2` - Royal Match

> It's an interesting game but the developers should pls try to include new cards in every card pack because I noticed when one is almost close to completing a set, new cards don't appear again especially when the set is almost expiring. So after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion because they don't add new sets to the cards once the collection is about to end.

| | labels |
|---|---|
| gold | `P_CompleteTheCollection`, `T_PlayingByAppointment` |
| pred | `P_CompleteTheCollection`, `P_IllusionOfControl`, `P_RewardMania`, `T_PlayingByAppointment` |
| **spurious** | `P_IllusionOfControl`, `P_RewardMania` |

**Model analysis**

```
The reviewer describes Royal Match's time-limited card-collection event. They are trying to complete a set of cards for its completion reward, but say that card packs cease delivering new/missing cards when a set is nearly complete and near expiry. This describes a collection-completion goal, random/variable card-pack rewards that allegedly withhold needed outcomes, and a deadline under which the completion reward is lost. The game documentation was checked because the review's "card pack" mechanic needed clarification; it establishes that cards are delivered through packs with probability rules and that Collection is time-limited.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "when one is almost close to completing a set"
  - why: The reviewer describes pursuing completion of a card set and frames the missing cards as preventing that goal.
- `P_IllusionOfControl` - **SPURIOUS**
  - span: "new cards don't appear again especially when the set is almost expiring"
  - why: The reviewer alleges that the game tunes or withholds the needed card outcomes according to a hidden end-of-event schedule.
- `P_RewardMania` - **SPURIOUS**
  - span: "the developers should pls try to include new cards in every card pack because I noticed when one is almost close to completing a set, new cards don't appear again"
  - why: Card packs deliver variable card outcomes, and the reviewer describes repeatedly receiving packs without the missing/new cards needed to complete the set.
- `T_PlayingByAppointment` - ok
  - span: "especially when the set is almost expiring. So after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion"
  - why: The collection's expiry imposes a game-set deadline, and failing to complete it before that deadline forfeits the completion reward.

**Search:** `Royal Match card collection card packs new cards set expiration` -> Royal Match's official help pages establish that Collection is a time-limited card-completion feature with rewards, and that card packs use variable/dynamic probability rules, with some packs guaranteeing or boosting new/missing cards.

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
The review describes two monetary mechanics. First, the player says meaningful in-game growth requires spending, which is a direct paid-advancement gate. Second, an update removed player-versus-player play, making the growth and advantages players had paid for pointless; this describes prior spending losing value after an update. The mention that PvP was removed does not itself assign Competition, because the review describes its removal rather than a currently present competitive mechanic.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You have to spend to have any meaningful growth"
  - why: The reviewer explicitly states that meaningful progression requires spending money.
- `M_PowerCreep` - **SPURIOUS**  _[span not verbatim]_
  - span: "they go and make it all pointless by getting rid of any player vs player, so it's now just boring farmville. ... They just screwed everyone over who wasted money on this game."
  - why: The update removing PvP is described as making players' previously purchased growth pointless, so acquired paid value was diminished after purchase.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_Gambling` | 2 | 2 |
| `S_Competition` | 3 | 0 |
| `M_PayToProgress` | 1 | 2 |
| `P_IllusionOfControl` | 1 | 1 |
| `P_AestheticManipulation` | 2 | 0 |
| `M_WasteAversion` | 2 | 0 |
| `M_DeceptiveLuxury` | 2 | 0 |
| `S_Reciprocity` | 2 | 0 |
| `T_Grinding` | 1 | 1 |
| `T_MandatoryMarathon` | 1 | 0 |
| `P_RewardMania` | 0 | 1 |
| `M_UIMisdirection` | 1 | 0 |
| `M_PowerCreep` | 0 | 1 |
| `T_PlayingByAppointment` | 1 | 0 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `M_EasyToPurchase` | 1 | 0 |
| `M_IntermediateCurrency` | 1 | 0 |

