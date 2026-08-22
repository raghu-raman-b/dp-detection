# Error review - gpt-5.6-luna_none_teacher_v2_boundary

`gpt-5.6-luna` / reasoning `` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_boundary.txt` sha `013bb31c5857`  
micro-F1 **0.773** (P 0.906 / R 0.674) - **22 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 3 | said NONE, gold had labels |
| SWAP | 4 | picked different labels than gold |
| MISSED ONLY | 15 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 0 | found all gold, added extras |

## The diagnostic that matters

Of **28** missed labels, **6** (21%) were named in the model's own analysis and dropped anyway; **22** (79%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `P_RewardMania` | 0 | 3 |
| `M_IntermediateCurrency` | 0 | 3 |
| `S_Reciprocity` | 0 | 2 |
| `P_AestheticManipulation` | 0 | 2 |
| `M_Gambling` | 1 | 1 |
| `M_PayToProgress` | 0 | 2 |
| `M_WasteAversion` | 1 | 1 |
| `M_DeceptiveLuxury` | 0 | 2 |
| `M_PowerCreep` | 1 | 0 |
| `S_FriendSpamImpersonation` | 0 | 1 |
| `S_Competition` | 1 | 0 |
| `M_RecurringFee` | 1 | 0 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `T_Advertisement` | 0 | 1 |
| `M_EasyToPurchase` | 0 | 1 |
| `T_Grinding` | 1 | 0 |
| `T_PlayingByAppointment` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |

## Missed everything (predicted NONE) (3)

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
The reviewer describes concern that deleting the game might erase in-game purchases and accumulated progress, but does not clearly state that MadOut 2 currently deletes those items. The reviewer is requesting or suggesting a save feature and says they would invest money if such protection existed. Because the described loss is hypothetical and the requested behavior is not an existing mechanic, no label is supported.
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
The reviewer describes being unable to request troops from their clan after an update, explicitly attributing the problem to a fault that needs fixing. Although requesting troops is a social resource-request mechanic, the described behavior is a malfunction preventing it rather than a functioning design that creates reciprocal obligation. Under R11, no dark-pattern label applies.
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
The reviewer describes misleading promotion of pin-pull and mini-game content, saying those features are advertised as plentiful but are actually rare. Under the codebook, out-of-game or general advertising claims do not trigger T_Advertisement, which requires being compelled or incentivized to watch ads within the game. The reviewer also says they paid for extra coins and other items hoping pin-pull games would appear, but this does not establish that payment was required for progress or that a purchase reliably unlocked progress. The repeated update connection problem is attributed to a technical fault, so it does not support a dark-pattern label. The level number is only a play-history detail, not evidence of an infinite treadmill.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (4)

### `fdef27f2-9a21-4b8e-a04c-7a4753e0fb07` - 8 Ball Pool

> The game is great, but the user interface is completely rigged. Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins and are forced to buy real ones. ​We need a "Default Table Lock" or the game should always open the lowest bet table by default, not the highest! Fix this scammy feature. Giving 1 star

| | labels |
|---|---|
| gold | `M_Gambling`, `M_IntermediateCurrency`, `M_UIMisdirection` |
| pred | `M_EasyToPurchase`, `M_IntermediateCurrency`, `M_PayToProgress`, `M_UIMisdirection`, `S_Competition` |
| **missed** | `M_Gambling` |
| **spurious** | `M_EasyToPurchase`, `M_PayToProgress`, `S_Competition` |

**Did the model consider what it missed?**

- `M_Gambling` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a deliberately manipulative table-selection interface. When the game opens or the player enters 1v1, it automatically scrolls to and selects the highest-stakes table available, creating a default that can cause accidental mis-clicks. The reviewer says this makes players lose their earned in-game coins and then buy more coins with real money, so the design both reduces friction for an unintended purchase and pushes payment after a resource loss. The 1v1 section also explicitly describes player-versus-player competition. The requested lowest-bet default and Default Table Lock are proposed features, so they are not coded.
```

**Labels assigned**

- `M_EasyToPurchase` - **SPURIOUS**
  - span: "automatically scrolls and selects the highest possible bet table based on your coins"
  - why: The interface uses an automatic high-stakes default that makes an unintended costly selection or mis-click easier.
- `M_IntermediateCurrency` - ok
  - span: "forced to buy real ones"
  - why: The reviewer describes buying replacement in-game coins with real money, establishing a real-money-to-virtual-currency conversion.
- `M_PayToProgress` - **SPURIOUS**
  - span: "lose all their hard-earned coins and are forced to buy real ones"
  - why: After the interface causes the player to lose their usable coins, the review says continued play forces a purchase of real-money coins.
- `M_UIMisdirection` - ok
  - span: "automatically scrolls and selects the highest possible bet table"
  - why: The interface deliberately directs the player toward the highest-bet option instead of a neutral or low-risk choice.
- `S_Competition` - **SPURIOUS**
  - span: "go to the 1v1 section"
  - why: The named 1v1 mode makes the player compete against another player.

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
The reviewer describes a daily reward system that requires completing a betting condition: the player cannot claim or complete the daily rewards without betting 50,000. This is a daily reward cycle with a concrete consequence for not completing its requirement, so T_DailyRewards applies. The required action is also a wager in a casino-slots game, linking the bet to a chance-based reward context, so M_Gambling applies. The review does not describe real-money payment, a wait timer, or progression being blocked beyond the daily rewards themselves.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "unless I bet 50,000"
  - why: The player must wager 50,000 within a slots-based game, making the required action a chance-based gambling stake.
- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The game conditions the daily reward on completing a required betting task, and the player forfeits completion without it.

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
The reviewer describes repeatedly playing bingo rounds to collect photos and complete a set, which is a collection goal pursued through repetitive activity. The game also presents an offer after a lost round to spend coins to obtain a missing photo, making payment an alternative route to collection progress. The reviewer says the promised photo is not delivered, but does not clearly attribute this to a bug or technical fault; it is therefore still evidence of the purchase-for-progress mechanic. The review does not establish an unattainable game-wide endpoint, a chance-based purchase, or a daily schedule.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "I'll spend coins on said offer"
  - why: The game offers a paid-currency route to obtain a photo needed for collection progress.
- `P_CompleteTheCollection` - ok
  - span: "to complete the set"
  - why: The stated goal is to acquire missing photos and complete an in-game collection.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The reviewer must repeatedly play bingo rounds to advance toward collecting photos.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b93c432d-19c0-4c6c-a2d4-bb9b21a436f3` - Dice Dreams™️

> A literal brain-rot game no wonder why they're tryna promote it through Free Cash. Also if you're thinking of making in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates! A real SCAM. Play it if u want but there are games that are actually good also, DON'T GET IN-APP PURCHASES!

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `P_CompleteTheCollection`, `P_EasyToGetHardToLose` |
| **missed** | `P_AestheticManipulation`, `P_RewardMania` |
| **spurious** | `P_EasyToGetHardToLose` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes an album-collection mechanic: the player was two cards short of completing an album and receiving its grand prize. That near-complete collection appears to have motivated a purchase of a card deal, which supports both the drive to complete the collection and the use of a partially completed goal to encourage continued investment. The purchase itself is described as failing to provide the promised new cards, but the review does not clearly establish a randomized reward system, a real-money currency conversion, or that payment was required for progress. The mention of Free Cash concerns external promotion and is out of scope. No web search was needed.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "two cards left which would grant me the grand prize for completing an album"
  - why: The player is pursuing completion of an album collection to obtain its grand prize.
- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "I had two cards left which would grant me the grand prize for completing an album, so i bought a deal"
  - why: The nearly completed album functions as a partially completed goal that discourages abandonment and leads the player to spend for the remaining cards.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (15)

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
The review primarily describes technical malfunctions: crashing when opening gifts or trading, lag preventing catching Pokémon, and freezing or unresponsive controls during battles. Under R11, these bug-related behaviors do not trigger dark-pattern labels. The review also explicitly identifies PvP battles involving an opponent, which describes competition between players; the Rocket battles are not necessarily player-versus-player, but the PvP portion supports Competition. No web search is needed because all relevant mechanics are clear from the review.
```

**Labels assigned**

- `S_Competition` - ok
  - span: "the pvp & rockets battles are also lagging switching out are too slow, charge attacks are not responding well and my game freeze while the opponent keep attacking"
  - why: The reference to PvP and an opponent attacking describes players competing against one another, although the surrounding lag and freezing are technical faults.

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

- `M_RecurringFee` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a condition involving a game element failing to appear within a fixed number of moves, but it does not clearly identify a dark-pattern mechanic such as a timer, random-reward purchase, or progress gate. The reviewer also mentions buying a pass, which indicates an existing pass-based purchase mechanic, but the text does not describe its duration or how it encourages continued play strongly enough to establish a recurring fee. Finally, the reviewer explicitly describes trading lives with friends and a team, which is a resource exchange between existing players and matches Reciprocity. The statement that players do not have to pay to win is a denial of a mechanic, not evidence for Pay to Progress.
```

**Labels assigned**

- `S_Reciprocity` - ok
  - span: "Get friends and a team and trade lives."
  - why: The review explicitly describes trading lives with existing friends or teammates, which is an in-game resource exchange.

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

- `T_PlayingByAppointment` - never mentioned -> **attention / recall**

**Model analysis**

```
The review explicitly describes a daily prize system that makes the player start over after missing a day, which is a daily-return incentive with a missed-day penalty. The mention of waiting for a new life is phrased as a suggestion for changing the timer, so it does not establish a currently present wait mechanic under R12. The harder levels and the fact that they take time to beat do not describe repetitive required activity, and the positive description of the game being addicting is not itself a mechanic.
```

**Labels assigned**

- `T_DailyRewards` - ok
  - span: "just because you miss a day doesnt mean that you need to start over on your daily prizes"
  - why: The game provides daily prizes and makes the player restart them after missing a day, explicitly describing a daily-return incentive and missed-day penalty.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fd1230ab-7d12-4aeb-a425-e37ed06bcd5c` - Pokémon GO

> I love this game, just started playing about 2 months ago. Though I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way. I feel taken advantage of. 3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| pred | `P_IllusionOfControl` |
| **missed** | `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |

**Did the model consider what it missed?**

- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**
- `S_FriendSpamImpersonation` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes purchasing Poké Balls and then experiencing repeated failed captures, causing the balls to be consumed faster and creating pressure to buy more. The claim that capture outcomes worsen after purchasing asserts that the game manipulates or changes the determination of outcomes, rather than merely reporting an unlucky streak, so it supports Illusion of Control. The mention of speaking with other players is later explicitly retracted and does not describe a game mechanic. The final claim about the review itself concerns the app-store review context, which is outside the game's in-app design.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out"
  - why: The reviewer alleges that capture results are manipulated after purchasing Poké Balls, implying the game is concealing or altering how outcomes are determined.

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

- `M_Gambling` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a friend-invitation mechanic tied to rewards: the player invited friends and got them to join Facebook, indicating social recruitment through incentives even though the rewards are currently not being granted. The sticker system produces repeated duplicate stickers; the searched game help information establishes that sticker content is random, so this is an unpredictable reward-delivery system rather than merely a complaint about low-value rewards. The shortage of dice and the failed shut downs or bank heists do not by themselves establish payment-gated progress, gambling, rigging, or competition. The inability to log in is explicitly attributed to an internet connection error, so it is a technical fault and does not trigger a dark-pattern label.
```

**Labels assigned**

- `P_RewardMania` - ok
  - span: "Stickers are duplicates all the way"
  - why: The player reports repeated duplicate sticker outcomes, which reflects unpredictable randomized reward delivery rather than only dissatisfaction with the reward's value.
- `S_ForcedFellowship` - ok
  - span: "no rewards for inviting friends and getting them to join facebook"
  - why: The span describes a reward-linked friend-recruitment mechanic, using the player's social connections to bring others into the game.

**Search:** `MONOPOLY GO official stickers duplicate sticker packs random` -> The official MONOPOLY GO help information established that sticker content is random and that duplicate stickers commonly occur over time.

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
The review describes a perceived manipulation of random outcomes: the reviewer says the RNG is obviously working against the player. This is an allegation that the game determines outcomes unfairly, which fits Illusion of Control rather than merely coding an unlucky run. The reviewer also says later levels cost 2200 while winning barely returns that amount, but this establishes poor reward value and a resource-economy complaint, not a concrete leftover, inventory loss, or explicit payment gate blocking progress. Saying the game is not rewarding without spending actual money does not by itself show that payment is required to advance.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "the rng is so obviously against you"
  - why: The reviewer attributes unfavorable results to an RNG that is deliberately or systematically biased against the player, alleging manipulated outcome determination.

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
The reviewer describes the game as a repetitive grinder, but does not identify a specific repeated activity required for progress, so the general complaint does not support T_Grinding. The main concrete mechanic is that winning an event is effectively unavailable to ordinary players and requires spending a large amount of money; this is a paid advantage tied directly to competitive success, matching Pay to Win under M_PayToProgress. The text does not clearly describe a specific opponent-based competition structure beyond winning an event, so S_Competition is not assigned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Calculated total spent on last event was 30k to win."
  - why: The reviewer states that spending approximately 30,000 was required to win the event, describing money as the route to competitive success.

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
The review describes a sticker-collection progression system in which obtaining the final one or two stickers is effectively unavailable without paying a large amount of real money. The stickers are treated as a collection the player is trying to complete, so the collection mechanic is explicit. The claim that winning anything costs hundreds of dollars also describes payment as necessary for success, but the sticker sentence is the clearest progression gate. The statements about addiction, an endless bank account, and completing a goal only one time in a hundred express evaluation or low success likelihood without identifying a specific chance-based reward mechanic, so they do not independently trigger gambling or reward-delivery labels. The review-writing restriction is outside the game mechanics covered by the labels.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: Completing the sticker objective is described as impossible without paying a large amount of real money.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two"
  - why: The reviewer describes trying to obtain the remaining stickers in order to complete an in-game collection.

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
The reviewer describes a lives-based progression system and says they repeatedly run out of lives while trying to clear levels, but does not describe a timer or regeneration schedule, so Playing by Appointment is not supported. The review explicitly states that buying add-ons is necessary to get through the game, making payment a requirement for progress. The level duration is long, but no repetitive task or repeated activity is identified, so Grinding is not assigned. Although the reviewer mentions investing money and time, they are describing that investment as already wasted while uninstalling, not as a force making it difficult to leave, so Easy to Get, Hard to Lose is not assigned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through"
  - why: The reviewer states that continued progress through the game is impossible without purchasing add-ons.

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
The reviewer describes a state-loss mechanic associated with leaving and returning to the game: a full bag becomes empty, and both earned and purchased coins have been consumed or lost. The exact cause is not identified as a bug or technical fault. Because exiting the game results in forfeiting held progress and resources, this supports Mandatory Marathon. The text does not clearly describe an inventory-capacity rule forcing disposal, reluctance to quit, or a purchase mechanism, so the other labels are not supported.
```

**Labels assigned**

- `T_MandatoryMarathon` - ok
  - span: "I would give 5 stars, but I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used."
  - why: Leaving the game causes the player to return with their bag emptied and coins lost or consumed, indicating that stopping the session forfeits accumulated resources.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a2ece36d-c527-442d-8f18-9a16b63994c8` - War Robots Multiplayer Battles

> Its a p2w game. The only time you enjoy it is when you're new. As you progress, everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game. If you want to progress without paying money, goodluck! Even if you wanted to do f2p, you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it. Plus the only time you benofit by getting f2p rewards is ads... 💩

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `M_PayToProgress`, `M_PowerCreep`, `T_Advertisement` |
| pred | `M_EasyToPurchase`, `M_PayToProgress` |
| **missed** | `M_PowerCreep`, `T_Advertisement` |

**Did the model consider what it missed?**

- `M_PowerCreep` - considered and rejected -> **rule interpretation**
- `T_Advertisement` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes purchase prompts that appear every time the player logs in and block access to gameplay until they deal with them. It also describes progression and competitive viability as dependent on spending: free players cannot keep up with the shifting meta and must buy the newest bot rather than earn it. The mention of F2P rewards and ads is too unclear to establish that the game forces ad views or rewards watching them. The shifting meta does not by itself show that previously purchased items lose value, so Power Creep is not assigned. No web search is needed because the mechanics are identifiable from the review.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game"
  - why: Purchase offers directly intercept gameplay at login and appear before the player can play.
- `M_PayToProgress` - ok
  - span: "you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it"
  - why: The review states that spending money to obtain the newest bot is necessary to maintain progress or competitive advantage, while the free route is inadequate.

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
The reviewer describes an inventory-capacity bottleneck at higher progression: storage is almost full with generator parts and high-level food items, leaving only 26 spaces. They state that continuing to store and play requires spending money to buy parts, so payment is presented as necessary for continued progress or play. The review does not describe real-money currency conversion, a paid subscription, repetitive tasks, or an item actually being discarded or lost. Although the limited inventory creates pressure, the text does not clearly show realized wasted value such as forfeited currency, sacrificed items, or a concrete purchase of extra capacity, so Waste Aversion is not assigned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Not enough slots to store and play without spending $$ to buy parts"
  - why: The reviewer states that spending money is required to keep enough parts and continue playing, making payment the alternative to an in-game progression barrier.

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
The reviewer describes a sticker-collection system in which obtaining stickers repeatedly produces duplicates, indicating an unwanted or variable reward delivery pattern. They are trying to complete all sticker sets, so collection completion is an explicit objective. The review also states that finishing the sets is unavailable unless the player pays, making payment a condition of progress. No search is needed because stickers and sets are clear from the review context.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: Completing the sticker sets is described as impossible without paying.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: The reviewer is pursuing completion of all in-game sticker sets.
- `P_RewardMania` - ok
  - span: "getting stickers. always get duplicates"
  - why: The sticker system repeatedly delivers duplicate items, describing the reward-delivery pattern rather than merely the value of the rewards.

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
The review describes several mechanics. The game uses gold to obtain additional moves, and the reviewer says that the free gold earned through play is sometimes insufficient to continue, making buying necessary for progress. It also places timers on bonuses that continue counting down while the player is away, causing the bonuses to expire before the player returns; the complaint that purchased packages should not be timed indicates a similar timed restriction on paid packages. The missing unlimited lives from a paid package is explicitly a failure to deliver the purchase, so it is treated as a technical or fulfillment problem rather than a dark pattern. The charge for moves is not described clearly enough to establish an accidental-purchase interface, and the review does not describe real money being converted into gold.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The free route does not provide enough gold to continue playing, so buying is sometimes required for continued progress.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing."
  - why: Bonuses are governed by a real-time countdown that continues while the player is absent, forcing the player to return within the game's schedule or lose the bonuses.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `727cc804-9d4b-48ef-8774-2799a2a8de08` - Genshin Impact

> with every incoming patch, we get less and less rewards and for me that wouldn't be a problem but the Meta changes more and more every single day basically forcing us to pull for new characters if we want to actually do damage. the game is getting more and more pay 2 win and the quality of the game is becoming lower. in the new archon quest when we were talking to mavuika, a multi billion dollar company just put an insanely bad picture of Natlans scenery as the background, y'all can do better.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_PowerCreep`, `P_RewardMania` |
| pred | `M_PayToProgress`, `M_PowerCreep` |
| **missed** | `P_RewardMania` |

**Did the model consider what it missed?**

- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes an escalating character-meta system: frequent balance or meta changes make newer characters increasingly necessary to deal meaningful damage, which implies that existing characters lose practical value over time. It also explicitly characterizes the game as becoming pay-to-win, with pulling for new characters presented as the route to maintaining combat effectiveness. The reduced rewards and lower visual quality are complaints about value and quality, not standalone dark-pattern mechanics. The background image complaint describes poor quality, not a coded design behavior.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "basically forcing us to pull for new characters if we want to actually do damage"
  - why: The review presents acquiring new characters through pulls as necessary to deal damage, linking continued effective advancement to monetized character acquisition.
- `M_PowerCreep` - ok
  - span: "the Meta changes more and more every single day basically forcing us to pull for new characters if we want to actually do damage"
  - why: The changing meta makes existing characters less effective and pressures players to obtain newer characters to retain combat performance.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_PayToProgress` | 2 | 2 |
| `P_RewardMania` | 3 | 0 |
| `M_Gambling` | 2 | 1 |
| `M_IntermediateCurrency` | 3 | 0 |
| `S_Reciprocity` | 2 | 0 |
| `S_Competition` | 1 | 1 |
| `P_AestheticManipulation` | 2 | 0 |
| `P_EasyToGetHardToLose` | 1 | 1 |
| `M_EasyToPurchase` | 1 | 1 |
| `M_WasteAversion` | 2 | 0 |
| `M_DeceptiveLuxury` | 2 | 0 |
| `M_PowerCreep` | 1 | 0 |
| `S_FriendSpamImpersonation` | 1 | 0 |
| `M_RecurringFee` | 1 | 0 |
| `T_Advertisement` | 1 | 0 |
| `T_Grinding` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |

