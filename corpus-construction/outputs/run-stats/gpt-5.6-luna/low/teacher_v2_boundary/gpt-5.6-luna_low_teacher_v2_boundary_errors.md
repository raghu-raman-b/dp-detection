# Error review - gpt-5.6-luna_low_teacher_v2_boundary

`gpt-5.6-luna` / reasoning `low` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_boundary.txt` sha `013bb31c5857`  
micro-F1 **0.795** (P 0.967 / R 0.674) - **23 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 7 | said NONE, gold had labels |
| SWAP | 1 | picked different labels than gold |
| MISSED ONLY | 14 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 1 | found all gold, added extras |

## The diagnostic that matters

Of **28** missed labels, **9** (32%) were named in the model's own analysis and dropped anyway; **19** (68%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `M_PayToProgress` | 0 | 3 |
| `M_IntermediateCurrency` | 0 | 3 |
| `S_Reciprocity` | 1 | 1 |
| `S_Competition` | 2 | 0 |
| `P_RewardMania` | 0 | 2 |
| `P_AestheticManipulation` | 0 | 2 |
| `M_WasteAversion` | 1 | 1 |
| `M_DeceptiveLuxury` | 0 | 2 |
| `P_IllusionOfControl` | 1 | 0 |
| `M_PowerCreep` | 1 | 0 |
| `S_FriendSpamImpersonation` | 0 | 1 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `T_Advertisement` | 1 | 0 |
| `M_Gambling` | 1 | 0 |
| `T_MandatoryMarathon` | 0 | 1 |
| `M_EasyToPurchase` | 0 | 1 |
| `T_Grinding` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |

## Missed everything (predicted NONE) (7)

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
The reviewer is expressing concern that deleting the game would erase in-game purchases and accumulated progress, and is asking the developer to add persistent saving before investing money. The requested saving feature is hypothetical and cannot itself be coded. The review does not describe an existing retention mechanic that makes abandoning the game difficult; it describes a feared loss of progress and purchases, partly based on experiences with other games. Therefore, no label is supported.
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
The reviewer describes a technical malfunction introduced by an update: they can no longer request troops from their clan. This reports a broken social feature, not a deliberate game mechanic such as reciprocity or forced fellowship. No dark-pattern label applies.
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

- `P_IllusionOfControl` - considered and rejected -> **rule interpretation**
- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**
- `S_FriendSpamImpersonation` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes buying Poké Balls and then having Pokémon break out repeatedly, causing the player to use the balls faster and buy more. This implies a suspicion that capture outcomes may be manipulated after purchases, but the text does not explicitly assert a fixed or hidden outcome system, engineered near-misses, or concealed odds; it mainly reports repeated failed captures and the resulting need to purchase more items. That is insufficient for Illusion of Control or any other listed mechanic. The later claim that the reviewer did not write the review concerns authorship outside the game's design and does not add a label.
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
The review describes misleading advertising, but the ads are outside the installed game's design and therefore are not coded under T_Advertisement or another label. Within the game, the reviewer says players make an army, train, build, gather resources, and do chores before reaching the occasional puzzle. These are progression activities, but the text does not explicitly describe them as repeated or mandatory cycles, so it does not meet the Grinding indicator. No other listed mechanic is clearly supported.
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
The review primarily complains that external advertising promises many pin-pull levels and mini-games, while the reviewer encounters very few of them. Under R13, misleading advertising placed outside the game is out of scope and does not trigger T_Advertisement, which covers compelled or rewarded ads encountered inside the game. The reviewer also describes paying for extra coins and other items in an attempt to make pin-pull content appear, but this does not establish that payment is required for progress or that the purchase directly unlocks advancement. Being over level 4000 is only a play-history detail and does not establish Infinite Treadmill. The connection problems after required updates are attributed to a technical issue, so they do not support a dark-pattern label.
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
The reviewer describes a loss of stored items and currency after leaving and returning: the bag is full when they exit, but empty on return, and both earned and purchased coins have been spent. This reports unexpected loss or possible malfunction, not a clearly described deliberate mechanic such as inventory-capacity waste, a purchase prompt, or a penalty for stopping play. No label is supported.
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
The reviewer describes being unable to advance beyond level 195 for almost two months and says they refuse to pay for power-ups. This indicates difficult or stalled progress and a possible paid convenience, but the review does not explicitly state that payment is required to continue, that power-ups directly unlock progress, or that a repetitive task must be performed. The requested daily login rewards are hypothetical and do not describe an existing mechanic. No label is supported.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (1)

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
The review describes a deliberate interface default that automatically scrolls to and selects the highest-stakes table rather than the lowest-risk option. This directs the player's attention and input toward the costly table and is said to cause accidental mis-clicks that make players lose their accumulated in-game coins. The reviewer further states that, after those losses, players are forced to buy more coins with real money. The interface behavior supports UI Misdirection. The real-money purchase of replacement in-game coins supports Intermediate Currency, and the stated need to buy coins to continue playing supports Pay to Progress. The review does not explicitly establish a chance-based wager, so Gambling is not assigned.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "are forced to buy real ones"
  - why: The phrase describes purchasing replacement in-game coins with real money.
- `M_PayToProgress` - **SPURIOUS**
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: After the interface-induced coin loss, the reviewer says players must pay for more coins, making continued play dependent on spending.
- `M_UIMisdirection` - ok
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks"
  - why: The interface deliberately defaults attention and selection to the highest-bet table, making accidental mis-clicks more likely.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (14)

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
The review primarily describes technical faults: crashes prevent opening gifts and trading, lag prevents throwing Poké Balls and makes battles unresponsive, and freezing allows the opponent to continue attacking. These malfunctions do not establish dark-pattern mechanics under R11. The review does explicitly mention PvP competition against an opponent, which is an in-game competitive mechanic independent of the malfunction, so Competition applies.
```

**Labels assigned**

- `S_Competition` - ok
  - span: "the opponent keep attacking"
  - why: The span explicitly describes an opponent attacking the reviewer in a PvP battle, establishing player-versus-player competition.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b98d7e75-73da-4591-b23e-1a2951bfd856` - Township

> I like this game a lot, but recently after seeing the ads, there is no way to close it. No cross mark on the screen , if you try to click anywhere on the screen it takes you to store. If you go back to game it is still stuck in the last sceeen of the ad. You have to kill the game to come out of the ad screen , so frustrating!!!

| | labels |
|---|---|
| gold | `M_UIMisdirection`, `T_Advertisement` |
| pred | `M_UIMisdirection` |
| **missed** | `T_Advertisement` |

**Did the model consider what it missed?**

- `T_Advertisement` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes an in-game advertisement screen that obstructs the player’s return to gameplay. The ad has no visible close control, and tapping elsewhere redirects the player to the store, so the opt-out path is absent or misdirected. Although the reviewer says they must kill the game to leave the screen, no progress loss or inability to end a session under the game’s rules is described. Merely seeing or being stuck on an ad does not establish compelled or rewarded ad viewing under T_Advertisement.
```

**Labels assigned**

- `M_UIMisdirection` - ok
  - span: "there is no way to close it. No cross mark on the screen , if you try to click anywhere on the screen it takes you to store."
  - why: The advertisement screen removes the normal opt-out and redirects taps toward the store instead of closing the ad.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `5e6a5625-5291-4f0e-897c-1b63c1a26494` - MONOPOLY GO!

> I loved this game until the new season started. Suddenly I get no rewards for inviting friends and getting them to join facebook. I am struggling to get dices and when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way... And today. Well, I cannot log in to the game at all. It keeps giving me an internet connection error which is absolute nonsense. I have connected to 3 different wifi connections. BS!!😡

| | labels |
|---|---|
| gold | `M_Gambling`, `P_RewardMania`, `S_ForcedFellowship` |
| pred | `M_Gambling`, `S_ForcedFellowship` |
| **missed** | `P_RewardMania` |

**Did the model consider what it missed?**

- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a social-recruitment mechanic that rewards inviting friends and getting them to join through Facebook, even though the reviewer says those rewards have stopped appearing. That supports Forced Fellowship because recruitment of new players is tied to in-game rewards. The reviewer also describes spending dice on a maximum bet and receiving no chance-based outcomes such as shutdowns or bank heists; this is an in-game wager using earned currency, which supports Gambling. The duplicate stickers alone do not establish a sufficiently clear randomised reward-delivery mechanic or a compulsion to complete the collection. The inability to log in is explicitly attributed to an internet connection error, so it is a technical fault and does not support a dark-pattern label.
```

**Labels assigned**

- `M_Gambling` - ok
  - span: "when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists."
  - why: The reviewer describes staking dice on a maximum bet for chance-based outcomes, namely shutdowns and bank heists.
- `S_ForcedFellowship` - ok
  - span: "no rewards for inviting friends and getting them to join facebook"
  - why: The game ties rewards to recruiting new players through the reviewer's friends and Facebook network.

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
The reviewer describes a hidden-outcome manipulation: they believe the game's RNG is deliberately unfavorable, rather than merely reporting an unlucky streak. The review also describes poor reward economics at around level 100, where a level costs 2200 and winning barely returns that amount, but this is a low-value reward complaint rather than a stated payment gate, currency shortfall, or repetitive progression requirement. No web search is needed because RNG is clear from context.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "the rng is so obviously against you"
  - why: The reviewer alleges that the game's random outcome system is deliberately biased against players, indicating manipulated outcomes rather than ordinary bad luck.

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
The review describes a base-building game the reviewer experiences as a repetitive grinder, but it does not name a repeated task or activity, so that general characterization does not independently trigger Grinding. The review explicitly says that winning events is effectively unavailable to ordinary players without spending, and reports spending 30k to win the last event. This describes payment providing an advantage or serving as the route to event success, which matches Pay to Progress through its Pay to Win indicator. No separate Competition label is assigned because the review does not explicitly describe competition against other players.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "there is absolutely no opportunity for a general player to win an event. Zero skill pay to play. Zero skill pay to win. Calculated total spent on last event was 30k to win."
  - why: The span explicitly links spending money with winning events and states that a general player cannot win without that paid advantage.

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
The review describes several active game mechanics. It explicitly says the game is pay-to-win, which indicates that spending money grants gameplay advantages. Base upgrades use increasingly long update timers, imposing waits on progress. The statement that everything scales endlessly and there is no point to look forward to describes an expanding game with no attainable end state, fitting Infinite Treadmill. The reviewer calls the experience more grind, but does not identify a specific repetitive task required for progress, so that alone does not support Grinding. The UI is described as deliberately confusing and overwhelming in order to push purchases, which supports UI Misdirection because the interface obstructs informed choice and directs the player toward buying. The alliance section describes coercive social grouping for protection, but the codebook excludes coerced grouping where no obligation to group members is described; it also does not clearly establish competition or harmful conduct being rewarded.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "set up in a pay to win way"
  - why: The review explicitly characterizes the game as pay-to-win, meaning payment provides an in-game advantage.
- `M_UIMisdirection` - ok
  - span: "The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff"
  - why: The reviewer attributes confusing and overwhelming interface design to steering players toward purchases.
- `T_InfiniteTreadmill` - ok
  - span: "Everything scales endlessly, there is kinda no point to look forward to, just more grind"
  - why: The game is described as scaling endlessly without a meaningful completion point.
- `T_PlayingByAppointment` - ok
  - span: "the update times for your base are becoming ridiculous"
  - why: Base updates are governed by increasingly long in-game timers that delay continued progress.

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

- `M_PayToProgress` - never mentioned -> **attention / recall**
- `M_WasteAversion` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a daily-reward system whose rewards cannot be completed or collected unless the player first bets 50,000. The timed rewards provide at most 40,000, creating a concrete gap between available rewards and the 50,000 requirement, but the review does not clearly describe real-money currency, a purchase prompt, or a progression barrier. The daily cycle is a reward condition rather than a gate on overall game progress, so Daily Rewards applies without Playing by Appointment. The betting mechanic is not coded as Gambling because no real-money or paid-currency stake is explicitly described.
```

**Labels assigned**

- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The game offers daily rewards but withholds completion of those rewards unless the player performs the required daily betting activity.

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
The review describes a sticker-collection goal where obtaining the final one or two stickers is effectively unavailable unless the player spends a large amount of money. That makes payment an alternative required for completing the collection and makes the sticker set itself a collection target. The statements about winning and completing a goal only once in a hundred attempts express poor odds and discouragement, but they do not identify a specific chance-based wagering mechanic, random reward-delivery system, or rigged outcome. The statement about being unable to write a review without giving five stars concerns the review interface rather than an identified codebook mechanic.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: Completing the sticker-related goal is described as requiring substantial payment because the final items cannot otherwise be obtained.
- `P_CompleteTheCollection` - ok
  - span: "you will never get the last one or two"
  - why: The reviewer describes pursuing the final missing items in a sticker collection, implying a compulsion or goal to complete the set.

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
The reviewer describes an inventory-capacity barrier at a higher level: the available board and refrigerator slots are occupied by generator parts and high-level items that cannot yet be merged or that the player refuses to delete. They state that playing without spending money to buy parts is not viable, which implies payment is presented as the route around the storage/progression obstacle. The review does not describe actually discarding items, losing currency, or buying additional storage, so Waste Aversion is not established. Mentioning that they are about to quit does not by itself show accumulated investment making departure difficult.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Not enough slots to store and play without spending $$ to buy parts."
  - why: The reviewer presents spending money to buy parts as necessary to keep playing once the inventory-space obstacle is reached.

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
The reviewer describes repeatedly playing bingo rounds to obtain photos needed to complete a set, which is a named repetitive activity tied to collection progress. The game also presents a post-loss offer to spend coins for a missing photo, but the reviewer says the promised photo is not delivered. Because the failure is described as the game not awarding what was promised, rather than as an intentional rule that makes the item random or unavailable, I do not code an additional monetization or reward-delivery label from that complaint. The statement about wasted money is an evaluation of the outcome, not by itself a separate mechanic.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "to complete the set"
  - why: The stated goal is obtaining the missing photos needed to complete a set.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The reviewer repeatedly plays bingo rounds in order to advance the photo collection.

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
The reviewer describes a sticker-collection system in which sticker acquisition repeatedly produces duplicate items, implying a randomized or variable reward delivery mechanism that makes obtaining missing stickers require repeated attempts. The goal is to finish all sticker sets, which supports a collection-completion mechanic. The reviewer also states that completing the sets is unavailable unless they pay, making payment a condition of progress. No web search is needed because the mechanics are clear from the review.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: Finishing the sticker sets is explicitly described as impossible unless the player pays.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: The reviewer describes pursuing completion of all sticker sets in the game.
- `P_RewardMania` - ok
  - span: "getting stickers. always get duplicates"
  - why: Repeated duplicate stickers imply a reward-delivery system with variable outcomes that requires continued attempts to obtain missing items.

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
The review describes several mechanics. The game charges gold for extra moves, and the reviewer says that sometimes playing requires buying gold because normal rewards are insufficient; this makes payment an alternative route to continued progress. Timed bonuses continue to expire while the player is away, so the game imposes a real-world clock on the reward window and causes rewards to be lost if the player does not return in time. The complaint that a purchased package supplied the other contents but not the lives is attributed to a failure to deliver the purchase, so it is a technical or fulfillment problem rather than a dark-pattern mechanic. The requests for cheaper packages and untimed packages do not themselves establish additional labels.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The free route does not provide enough gold to continue playing, making purchase the necessary alternative for progress or continued play.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone."
  - why: Bonuses expire while the player is away, imposing a time window and forfeiting rewards unless the player returns according to the game's schedule.

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
The review describes an album-based card collection with a grand prize for completing the album. The reviewer was two cards short, purchased a deal that promised new cards, and received duplicate cards instead. This explicitly describes pursuing completion of a collection and an unwanted duplicate reward outcome from a card-delivery system. The promotion through Free Cash is external marketing and outside the game-application scope. The purchase itself does not establish Pay to Progress, Gambling, Intermediate Currency, or Easy to Purchase because the review does not say payment was required for progress, describe odds or a wager, mention currency conversion, or describe a purchase-interface mechanism.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "completing an album"
  - why: The reviewer is pursuing the complete set of album cards in order to obtain the grand prize.
- `P_RewardMania` - ok
  - span: "i bought a deal which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: The purchased card reward delivered unwanted duplicate cards rather than the desired new cards, describing a reward-delivery system whose outcome sustains collection attempts.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `727cc804-9d4b-48ef-8774-2799a2a8de08` - Genshin Impact

> with every incoming patch, we get less and less rewards and for me that wouldn't be a problem but the Meta changes more and more every single day basically forcing us to pull for new characters if we want to actually do damage. the game is getting more and more pay 2 win and the quality of the game is becoming lower. in the new archon quest when we were talking to mavuika, a multi billion dollar company just put an insanely bad picture of Natlans scenery as the background, y'all can do better.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_PowerCreep`, `P_RewardMania` |
| pred | `M_PayToProgress`, `P_RewardMania` |
| **missed** | `M_PowerCreep` |

**Did the model consider what it missed?**

- `M_PowerCreep` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a changing combat meta in which newer characters are increasingly necessary to deal meaningful damage, and it explicitly characterizes this as becoming pay to win. The pull mechanic is also named, which indicates a chance-based character acquisition system, but the review does not explicitly state that money is being spent on those pulls, so Gambling is not assigned. The changing meta does not clearly state that characters the player already purchased have lost value, so Power Creep is not assigned. Complaints about reduced rewards and lower visual quality are evaluations without a qualifying dark-pattern mechanic.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "basically forcing us to pull for new characters if we want to actually do damage"
  - why: The review says obtaining newer characters is effectively necessary to deal damage, describing paid character acquisition as a route to combat advantage.
- `P_RewardMania` - ok
  - span: "pull for new characters"
  - why: The span explicitly names character pulls, a chance-based reward-delivery mechanic that sustains engagement independently of the characters' stated value.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (1)

### `14e87cfb-665b-4239-863d-2175f401d894` - Clash Royale

> this game is so annoying all you play against after 8k trophies is mega knight,pekka, and golem they need to rebuffed them they are so annoying to play against and when spammed down its annoying to defend this game is not fun for that reason its also pay to win and usually doesn't let you get higher from just using skill you have to go out of your way to be annoying to actually win in a game this game is getting more and more pay to win with each update and they buff cards people hate

| | labels |
|---|---|
| gold | `M_PayToProgress`, `S_Competition` |
| pred | `M_PayToProgress`, `S_Competition`, `S_EncouragesAntiSocialBehavior` |
| **spurious** | `S_EncouragesAntiSocialBehavior` |

**Model analysis**

```
The review describes competitive battles against other players, including repeated use of powerful cards and card-spamming that makes defense difficult. It explicitly claims that spending money provides an advantage and that skill alone is insufficient to advance, which supports Pay to Progress through the Pay to Win indicator. The reviewer also describes deliberately annoying play as a way to win, indicating an incentive to use harmful or aggravating conduct for advantage. The updates buff cards that players dislike, but the review does not say that previously purchased items lost value, so Power Creep is not supported.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "its also pay to win and usually doesn't let you get higher from just using skill"
  - why: The review states that spending money provides an advantage needed to advance to higher progression.
- `S_Competition` - ok
  - span: "all you play against after 8k trophies is mega knight,pekka, and golem"
  - why: The span explicitly describes the player competing against other players using particular cards.
- `S_EncouragesAntiSocialBehavior` - **SPURIOUS**
  - span: "you have to go out of your way to be annoying to actually win in a game"
  - why: The span describes deliberately aggravating other players as a strategy for gaining victory.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_PayToProgress` | 3 | 1 |
| `M_IntermediateCurrency` | 3 | 0 |
| `S_Reciprocity` | 2 | 0 |
| `S_Competition` | 2 | 0 |
| `P_RewardMania` | 2 | 0 |
| `P_AestheticManipulation` | 2 | 0 |
| `M_WasteAversion` | 2 | 0 |
| `M_DeceptiveLuxury` | 2 | 0 |
| `P_IllusionOfControl` | 1 | 0 |
| `M_PowerCreep` | 1 | 0 |
| `S_FriendSpamImpersonation` | 1 | 0 |
| `P_EasyToGetHardToLose` | 1 | 0 |
| `T_Advertisement` | 1 | 0 |
| `M_Gambling` | 1 | 0 |
| `T_MandatoryMarathon` | 1 | 0 |
| `M_EasyToPurchase` | 1 | 0 |
| `T_Grinding` | 1 | 0 |
| `S_EncouragesAntiSocialBehavior` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |

