# Error review - gpt-5.6-luna_low_teacher_v3_full

`gpt-5.6-luna` / reasoning `low` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v3_full.txt` sha `a6ae58246360`  
micro-F1 **0.748** (P 0.902 / R 0.640) - **23 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 8 | said NONE, gold had labels |
| SWAP | 4 | picked different labels than gold |
| MISSED ONLY | 10 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 1 | found all gold, added extras |

## The diagnostic that matters

Of **31** missed labels, **6** (19%) were named in the model's own analysis and dropped anyway; **25** (81%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `M_IntermediateCurrency` | 0 | 4 |
| `T_Grinding` | 1 | 2 |
| `S_Reciprocity` | 0 | 2 |
| `P_AestheticManipulation` | 0 | 2 |
| `M_Gambling` | 1 | 1 |
| `S_Competition` | 1 | 1 |
| `P_RewardMania` | 1 | 1 |
| `M_DeceptiveLuxury` | 0 | 2 |
| `M_PowerCreep` | 2 | 0 |
| `M_PayToProgress` | 0 | 2 |
| `T_MandatoryMarathon` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `M_WasteAversion` | 0 | 1 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `M_EasyToPurchase` | 0 | 1 |
| `P_IllusionOfControl` | 0 | 1 |
| `S_FriendSpamImpersonation` | 0 | 1 |

## Missed everything (predicted NONE) (8)

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
The review consists entirely of requested or hypothetical additions: auctions using in-game currency, preventing removal of converted decorations, an account-switching widget showing upgrade timers, and exposing advanced troop statistics. These statements do not describe mechanics currently present in the game, so none satisfy the coding rules. The 10/10 rating is not a mechanic.
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
The reviewer says they believe deleting the game would erase their in-game purchases and accumulated progress, and they request that the developer add a way to save this information. The saving feature is proposed rather than described as an existing game mechanic, so it cannot be coded under Mandatory Marathon. The reviewer also mentions invested money and effort, but does not say that these investments are currently keeping them from quitting; the loss is hypothetical if they delete the game. Therefore, no applicable label is supported.
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
The review describes a clan resource-request feature: the player is unable to request troops from clan members after an update. Although troop requests would ordinarily involve exchanging resources with other players, the reviewer explicitly attributes the unavailable behavior to an update problem and asks for it to be fixed. Under R11, the specific behavior attributed to a technical fault does not receive a dark-pattern label.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fd1230ab-7d12-4aeb-a425-e37ed06bcd5c` - Pokémon GO

> I love this game, just started playing about 2 months ago. Though I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way. I feel taken advantage of. 3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| pred | _NONE_ |
| **missed** | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |

**Did the model consider what it missed?**

- `P_IllusionOfControl` - never mentioned -> **attention / recall**
- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**
- `S_FriendSpamImpersonation` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes purchasing Poké Balls as consumable items, then having capture attempts fail because Pokémon repeatedly break out, causing the balls to be depleted faster and requiring more purchases. This establishes an in-game purchase and resource-consumption loop, but it does not explicitly describe a progression barrier, real-money-to-currency conversion, leftover value, or a chance-based purchase mechanic. The claim that this began after purchasing suggests suspected outcome manipulation, but the review does not clearly state that the game fixes or deliberately changes capture probabilities; it mainly reports an unlucky or frustrating pattern. The final edit says the review was not written by the reviewer, but it does not describe the game sending messages or posting through the player's social account. Therefore, no label is supported.
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

- `S_Competition` - never mentioned -> **attention / recall**

**Model analysis**

```
The review praises the game and mentions upgrades, stickers, boosters, and Facebook. However, the two concrete mechanics described are requested features rather than existing behaviors: trading stickers within the app and using a purchased booster when another player challenges the reviewer. The review does not describe actual social gifting or trading, messaging, recruitment, purchase friction, or a monetized gameplay advantage currently operating in the game. The Facebook reference only explains why the reviewer wants in-app trading and does not describe the game sending messages or requiring social access. Therefore, no label applies.
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

- `T_Grinding` - never mentioned -> **attention / recall**

**Model analysis**

```
The review contrasts misleading external advertisements with the actual game. The ads present the game as mainly physics-puzzle solving, but the reviewer says the installed game is primarily a strategy game involving making an army, training, building, and gathering resources, with puzzles appearing only occasionally. The statement that players will be doing chores to reach the puzzles describes a progression structure, but it does not clearly identify repetitive tasks or an explicit time gate. Because the misleading material is advertising placed outside the game, it is excluded by R13, and no in-game dark-pattern label is supported.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a5bfa159-1783-40a8-8852-ce39d7962398` - Homescapes

> They advertise many, many pin pull levels and games, but they are so few and far between, it's like false advertising. I'm over level 4000, so it's not like I haven't given it time. The "mini" games are foolish and also rare. I have also paid a lot for extra coins and things to see if pin pulls would happen, and they don't. Also, nearly everytime I do the required update, it takes days before it connects correctly again. I've tried on Gardenscapes too, same thing, false pin pulling advertising.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency` |
| pred | _NONE_ |
| **missed** | `M_IntermediateCurrency` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**

**Model analysis**

```
The review mainly describes misleading advertising for pin-pull mini-games, but advertising and store or marketing claims are outside the game-application scope under R13. Within the game, the reviewer says the mini-games are rare and paid for extra coins to try to encounter them, but does not clearly describe a current in-game mechanic that gates progress behind payment, uses paid currency in a chance system, or imposes a designed waiting schedule. The update-related connection problem is attributed to a technical fault, which does not trigger a dark-pattern label. Being over level 4000 is only a high level and does not establish an Infinite Treadmill.
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
The reviewer describes returning to the game and finding that stored items and coins have disappeared. This is a loss of game state or resources, but the review does not describe an intentional mechanic such as an inventory limit, a spending prompt, a progression gate, or a penalty for leaving. It also does not explicitly attribute the loss to a bug or technical fault. No codebook label is supported.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (4)

### `5e6a5625-5291-4f0e-897c-1b63c1a26494` - MONOPOLY GO!

> I loved this game until the new season started. Suddenly I get no rewards for inviting friends and getting them to join facebook. I am struggling to get dices and when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way... And today. Well, I cannot log in to the game at all. It keeps giving me an internet connection error which is absolute nonsense. I have connected to 3 different wifi connections. BS!!😡

| | labels |
|---|---|
| gold | `M_Gambling`, `P_RewardMania`, `S_ForcedFellowship` |
| pred | `P_RewardMania`, `S_ForcedFellowship`, `S_FriendSpamImpersonation` |
| **missed** | `M_Gambling` |
| **spurious** | `S_FriendSpamImpersonation` |

**Did the model consider what it missed?**

- `M_Gambling` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a friend-invitation reward mechanic: the player is supposed to receive rewards for inviting friends and getting them to join Facebook, which uses social recruitment as an incentive. Because invitations are being sent to friends through Facebook, it also describes the game acting through the player's social graph. The sticker system gives repeated duplicate stickers, indicating randomized reward delivery with unwanted duplicate outcomes, so Reward Mania applies. The lack of luck while playing max bet does not clearly establish a paid wager or a gambling mechanic, and the inability to log in is explicitly attributed to an internet connection error, so it does not support a dark-pattern label.
```

**Labels assigned**

- `P_RewardMania` - ok
  - span: "Stickers are duplicates all the way"
  - why: The sticker reward system delivers repeated unwanted duplicates from a randomized collection, making the delivery mechanism sustain repeated attempts.
- `S_ForcedFellowship` - ok
  - span: "rewards for inviting friends and getting them to join facebook"
  - why: The game incentivizes the player to recruit friends into the social/game ecosystem by offering rewards for their joining.
- `S_FriendSpamImpersonation` - **SPURIOUS**
  - span: "inviting friends and getting them to join facebook"
  - why: The span describes invitations being sent through the player's friend and Facebook social graph, which is messaging performed via the player's identity.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fdef27f2-9a21-4b8e-a04c-7a4753e0fb07` - 8 Ball Pool

> The game is great, but the user interface is completely rigged. Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins and are forced to buy real ones. ​We need a "Default Table Lock" or the game should always open the lowest bet table by default, not the highest! Fix this scammy feature. Giving 1 star

| | labels |
|---|---|
| gold | `M_Gambling`, `M_IntermediateCurrency`, `M_UIMisdirection` |
| pred | `M_PayToProgress`, `M_UIMisdirection`, `S_Competition` |
| **missed** | `M_Gambling`, `M_IntermediateCurrency` |
| **spurious** | `M_PayToProgress`, `S_Competition` |

**Did the model consider what it missed?**

- `M_Gambling` - never mentioned -> **attention / recall**
- `M_IntermediateCurrency` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes an interface rule in which opening the game or entering the 1v1 area automatically scrolls to and selects the highest-stakes table available, making an unintended tap likely to enter a costly match. That is UI Misdirection because the interface steers attention and selection toward the expensive option. The reviewer also says that losing the coins leaves players forced to buy more real ones, describing payment as necessary to restore continued access to play, which supports Pay to Progress. The 1v1 section is a player-versus-player competitive mode, so Competition is also explicitly present. The requested Default Table Lock and lowest-table default are hypothetical fixes and are not coded.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: The span describes losing the currency needed for play and then having to purchase more to continue.
- `M_UIMisdirection` - ok
  - span: "Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks"
  - why: The interface automatically selects and presents the highest-cost table, steering the player toward an unwanted, expensive option and encouraging accidental mis-clicks.
- `S_Competition` - **SPURIOUS**
  - span: "go to the 1v1 section"
  - why: A 1v1 section is a game mode in which the player competes against another player.

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
The review describes a daily-reward system that requires the player to place a 50,000-unit bet before the daily rewards can be completed. This is a daily return incentive with a requirement attached, so Daily Rewards applies. The bet is also a chance-based casino mechanic using an in-game stake; the review does not say the stake is purchased with real money, but the codebook permits Gambling when earned in-game currency is wagered without a purchase being described. The timed rewards and their 40,000 maximum describe reward amounts, not a wait timer or an unpredictable delivery system.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "unless I bet 50,000"
  - why: The player must wager an in-game stake in a casino-slots mechanic, making the bet a chance-based activity even though real-money purchase of the stake is not stated.
- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The game provides daily rewards but requires a specified action before the daily reward cycle can be completed.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `12267c1e-47ba-4984-97c8-768e820ceb1c` - Bingo Blitz™️ - Bingo Games

> not very user-friendly. no apparent reachable goals within a decent amount of time. I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| pred | `M_PayToProgress`, `P_CompleteTheCollection` |
| **missed** | `M_EasyToPurchase`, `P_AestheticManipulation`, `T_Grinding` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - never mentioned -> **attention / recall**
- `P_AestheticManipulation` - never mentioned -> **attention / recall**
- `T_Grinding` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer is describing a collection goal: repeatedly playing bingo rounds to collect photos and complete a set. After losing a round, the game presents an offer to spend extra coins to obtain a missing photo, making payment an alternative route toward completing the collection. The reviewer says they paid but received no promised photo despite getting 2-3 bingos; this is a failure to deliver the offer, but they do not explicitly attribute it to a bug or technical fault. The review also says they wasted money, but it does not describe a specific leftover-currency shortfall or a chance-based reward mechanic clearly enough for Waste Aversion or Gambling.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "ask me if I want to spend extra coins to claim a photo I don't have to complete the set"
  - why: The game offers payment as a route to obtain a missing collection item needed for completion.
- `P_CompleteTheCollection` - ok
  - span: "I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set."
  - why: The reviewer is repeatedly pursuing missing photos in order to complete a set.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (10)

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
The review attributes the inability to open gifts, trade, throw Poké Balls, and respond during battles to crashing, lag, freezing, and unresponsive controls. Under the technical-fault rule, these malfunction-attributed behaviors do not support dark-pattern labels. The review does explicitly describe PvP and Rocket battles involving an opponent, which establishes player competition, but it does not describe a design that forces continued play or penalizes exiting.
```

**Labels assigned**

- `S_Competition` - ok
  - span: "the pvp & rockets battles are also lagging switching out are too slow, charge attacks are not responding well and my game freeze while the opponent keep attacking"
  - why: The span explicitly describes battles against an opponent, establishing competition between players or combatants despite the problems being attributed to lag and freezing.

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
The review describes a chance-based outcome system that the player believes is deliberately unfavorable: the RNG is said to be “against you,” which is an allegation that the game manipulates or predetermines outcomes rather than merely producing an unlucky result. The review also compares the cost of playing a level with the reward for winning, saying that at around level 100 the player spends 2200 and barely earns that amount back. This describes poor reward value and an unfavorable economy, but it does not explicitly state that payment is required to unlock progress, nor does it identify real money being converted into currency or a chance-based reward delivery system. Therefore, no monetary or reward-mechanic label is supported.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "the rng is so obviously against you"
  - why: The reviewer alleges that the game’s random outcomes are systematically manipulated against the player, which describes concealed or rigged outcome determination.

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
The review describes a base-building game as repetitive, but “Same old same old grinder” is a general evaluation without naming a repeated activity tied to progress, so it does not establish Grinding. The reviewer says ordinary players cannot win an event and explicitly characterizes the game as “pay to win,” with a reported $30,000 expenditure to win the last event. This describes payment granting an in-game advantage or competitive success, which supports Pay to Progress through the Pay to Win indicator. The review does not clearly describe players competing against one another as a mechanic, only winning an event, so Competition is not assigned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Zero skill pay to win."
  - why: The span explicitly states that spending money is the route to winning, describing payment as providing an in-game advantage.

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
- `P_RewardMania` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a sticker-collection game in which completing the collection is difficult because the last one or two stickers are effectively unavailable without spending a large amount of money. It also says that winning anything costs hundreds of dollars, tying payment to obtaining rewards or advancing toward completion. The statement that a goal may be completed only one out of a hundred times describes very low success from the reviewer’s perspective, but it does not explicitly identify a chance-based delivery mechanic, so it does not independently support Gambling or Reward Mania.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: Obtaining the remaining stickers and completing the collection is described as contingent on paying a large amount of money.
- `P_CompleteTheCollection` - ok
  - span: "you will never get the last one or two"
  - why: The reviewer is pursuing completion of a sticker collection, with the missing final items preventing the set from being completed.

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
The reviewer describes increasingly difficult levels, running out of lives several times per day, and taking an average of 5–7 days to complete each level. The lives are a depleted resource, but no recharge timer or required waiting schedule is stated, so this does not establish Playing by Appointment. The review explicitly says that buying add-ons is necessary to get through the game and that not paying makes progress a waste of time, which describes payment as a condition for advancement. The reviewer mentions spending too much money and time but is uninstalling, so this does not show accumulated investment making it difficult to leave. No specific repetitive activity is described, so Grinding is not supported.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying."
  - why: The reviewer states that progressing through the game requires buying add-ons and that the unpaid route is unreasonably burdensome.

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

- `M_PowerCreep` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes several active game mechanics. Progress is tied to payment: the player says free-to-play progress cannot keep up and that the newest bot must be bought with money rather than earned, which is Pay to Progress. Purchase offers appear every time the player logs in and block access to gameplay until dismissed, so they are purchase solicitations that intercept play and reduce the friction of buying, supporting Easy to Purchase. The review also says the only benefit of free-to-play rewards is watching ads, which implies rewarded advertisements. The shifting meta and newest bot do not by themselves establish Power Creep because the reviewer does not say that an item they already owned lost value, and no explicit competitive matchup is described.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game."
  - why: Purchase offers directly intercept gameplay on login and must be dealt with before the player can play.
- `M_PayToProgress` - ok
  - span: "If you want to progress without paying money, goodluck! Even if you wanted to do f2p, you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it."
  - why: The free route is described as unable to support progress or keep up, while payment is required to obtain the newest bot instead of earning it.
- `T_Advertisement` - ok
  - span: "the only time you benofit by getting f2p rewards is ads"
  - why: The span describes advertisements as the required or incentivized route for obtaining free-to-play rewards.

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
The review describes a sticker-collection system with randomized or otherwise variable sticker delivery that repeatedly gives duplicates, making completion difficult. It also describes the game as preventing completion of all sticker sets unless the player pays, which makes payment a condition for progress. The sets are collection goals, so the desire to complete them is itself part of the described mechanic. No web search is needed because stickers and sets are clear from the review context.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: The review states that completing the sets is unavailable without making a payment, so payment gates progress.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: The reviewer is pursuing completion of all sticker sets, which is a collection goal.
- `P_RewardMania` - ok
  - span: "getting stickers. always get duplicates"
  - why: Sticker delivery produces repeated unwanted duplicates, describing an unpredictable reward system rather than merely a low-value reward.

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
The review describes several mechanics. Timed bonuses continue expiring while the player is away, so the game imposes a real-time schedule on temporary rewards; this supports Playing by Appointment. The reviewer also says that the free gold earned in the game is sometimes insufficient to keep playing, making purchases necessary for progress; this supports Pay to Progress. The paid package failing to grant the promised lives is attributed to a delivery problem, so it is not coded as a dark pattern. The charge for moves and the complaint that packages should cost less do not, by themselves, establish a qualifying purchase-interface or currency-conversion mechanic. A paid package being timed does not establish a battle pass or subscription.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The free route sometimes provides insufficient gold to continue playing, making purchases necessary for continued progress.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone."
  - why: Temporary bonuses expire according to the game's real-time clock even when the player is not playing, imposing a schedule and forfeiture of the reward.

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
The review describes an album-collection system where the player is trying to obtain the final two cards needed for a grand prize. The player purchased a deal that promised new cards, but the purchase delivered duplicate cards instead, showing a reward system that can provide unwanted duplicates rather than the missing collection items. The mention of promoting the game through Free Cash is external marketing and is out of scope. The purchase itself does not clearly establish that payment is required for progress, only that the player chose to buy a deal, so Pay to Progress is not assigned.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The reviewer is pursuing the final missing items in an album to complete an in-game collection and receive its completion reward.
- `P_RewardMania` - ok
  - span: "i bought a deal which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: The card acquisition system delivered unwanted duplicate items instead of the needed new cards, indicating an unpredictable or randomized reward-delivery mechanism.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `727cc804-9d4b-48ef-8774-2799a2a8de08` - Genshin Impact

> with every incoming patch, we get less and less rewards and for me that wouldn't be a problem but the Meta changes more and more every single day basically forcing us to pull for new characters if we want to actually do damage. the game is getting more and more pay 2 win and the quality of the game is becoming lower. in the new archon quest when we were talking to mavuika, a multi billion dollar company just put an insanely bad picture of Natlans scenery as the background, y'all can do better.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_PowerCreep`, `P_RewardMania` |
| pred | `M_PayToProgress` |
| **missed** | `M_PowerCreep`, `P_RewardMania` |

**Did the model consider what it missed?**

- `M_PowerCreep` - considered and rejected -> **rule interpretation**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes declining rewards and a rapidly changing meta that pressures players to obtain new characters in order to deal meaningful damage. The explicit connection between pulling new characters and effective gameplay supports Pay to Progress, since spending through character pulls is presented as necessary for advancement or performance. The review does not explicitly say that characters the player already owns have lost value, so Power Creep is not assigned. Complaints about lower quality and a bad scenery image are evaluations of quality, not dark-pattern mechanics. The reduced rewards are described only as having lower value, without an unpredictable delivery system or a collection-completion goal.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "basically forcing us to pull for new characters if we want to actually do damage"
  - why: The review describes obtaining new characters through pulls as necessary to perform effectively, making payment-linked acquisition a requirement for meaningful gameplay progress.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (1)

### `1da19dbd-f522-43c7-95d7-df59f631cc18` - Total Battle: War Strategy

> They ruined game, there's no more "battle" in total battle with latest update to get rid of open silver. Save your time and money and don't bother. You have to spend to have any meaningful growth and then they go and make it all pointless by getting rid of any player vs player, so it's now just boring farmville. Gotta be the dumbest company i've ever dealt with. They just screwed everyone over who wasted money on this game. Response to developers response..bring back open silver!!!

| | labels |
|---|---|
| gold | `M_PayToProgress` |
| pred | `M_PayToProgress`, `M_PowerCreep` |
| **spurious** | `M_PowerCreep` |

**Model analysis**

```
The review describes a progression system in which spending is necessary for meaningful growth, so payment is tied directly to advancement. It also says a latest update removed open silver and all player-versus-player play, making prior spending and growth pointless. The removal of PvP is described as a change to the game rather than a currently present competitive mechanic, so Competition is not assigned. The statement about money being wasted reports loss after the change but does not describe reluctance to leave, so Easy to Get, Hard to Lose is not assigned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You have to spend to have any meaningful growth"
  - why: The reviewer explicitly states that spending money is required for meaningful in-game progression.
- `M_PowerCreep` - **SPURIOUS**
  - span: "then they go and make it all pointless by getting rid of any player vs player"
  - why: An update is described as making previously acquired growth and spending pointless by removing the gameplay context that gave them value.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_IntermediateCurrency` | 4 | 0 |
| `M_PayToProgress` | 2 | 2 |
| `M_Gambling` | 2 | 1 |
| `S_Competition` | 2 | 1 |
| `T_Grinding` | 3 | 0 |
| `M_PowerCreep` | 2 | 1 |
| `S_Reciprocity` | 2 | 0 |
| `P_AestheticManipulation` | 2 | 0 |
| `P_RewardMania` | 2 | 0 |
| `M_DeceptiveLuxury` | 2 | 0 |
| `S_FriendSpamImpersonation` | 1 | 1 |
| `T_MandatoryMarathon` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `M_WasteAversion` | 1 | 0 |
| `P_EasyToGetHardToLose` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `M_EasyToPurchase` | 1 | 0 |
| `P_IllusionOfControl` | 1 | 0 |

