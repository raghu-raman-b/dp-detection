# Error review - gpt-5.6-sol_high_teacher_v2_full

`gpt-5.6-sol` / reasoning `high` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `6529a474a2b0`  
micro-F1 **0.822** (P 0.768 / R 0.884) - **20 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 2 | said NONE, gold had labels |
| SWAP | 1 | picked different labels than gold |
| MISSED ONLY | 5 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 12 | found all gold, added extras |

## The diagnostic that matters

Of **10** missed labels, **2** (20%) were named in the model's own analysis and dropped anyway; **8** (80%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `S_Reciprocity` | 0 | 2 |
| `S_Competition` | 0 | 1 |
| `P_IllusionOfControl` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `M_Gambling` | 1 | 0 |
| `S_ForcedFellowship` | 1 | 0 |
| `M_UIMisdirection` | 0 | 1 |
| `P_RewardMania` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |

## Missed everything (predicted NONE) (2)

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
The review describes technical malfunctions introduced by an update: crashes prevent opening gifts or trading, lag interferes with catching Pokémon and switching during battles, attacks fail to respond, and freezing leaves the opponent able to continue attacking. Although gifts, trading, and PvP are named as contexts, the complained-of behaviors are expressly attributed to bugs, crashing, lagging, and freezing. Under R11, these technical faults do not qualify as deliberate design patterns, and the review does not independently describe a codable mechanic operating apart from the malfunctions.
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
The reviewer describes a technical malfunction introduced by an update: the existing clan troop-request feature no longer works for them. Although requesting troops would normally identify a resource-transfer mechanic between clan members, the review explicitly says they can no longer use it and asks for it to be fixed. Under R11, behavior attributed to a bug or technical fault is not coded, and under R12, a feature described as currently unavailable does not establish a currently present mechanic.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (1)

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
The reviewer describes a 1v1 wagering interface that automatically scrolls to and preselects the highest table the player's coin balance permits. This default steers players toward a high-stakes option and allegedly causes accidental taps that wager and lose their accumulated coins. The review further states that losing those coins pushes players to purchase replacements, implying both a real-money-to-virtual-currency conversion and payment as the route back to continued play. The 1v1 tables also explicitly involve competition against another player. This is not Gambling because the review describes a competitive pool match but does not identify a chance-based reward mechanism.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: The object being bought is replacement in-game coins, establishing real-world purchasing of virtual currency.
- `M_PayToProgress` - **SPURIOUS**
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: The review implies that after the required table-entry coins are lost, buying replacement coins is forced as the route to continue playing.
- `M_UIMisdirection` - ok
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks"
  - why: The interface automatically directs and defaults the player to the highest monetary stake, creating unintended high-bet selections.
- `S_Competition` - **SPURIOUS**
  - span: "go to the 1v1 section"
  - why: A 1v1 section explicitly places the player in direct competition with another player.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (5)

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
The reviewer describes an advertisement displayed inside the game that cannot be dismissed: it has no close control, tapping anywhere redirects to the store, and returning leaves the advertisement on screen. This makes viewing the ad compulsory until the player terminates the application, satisfying Advertisement. Although the player must kill the game, no match or accumulated progress is said to be forfeited, so Mandatory Marathon does not apply. The stuck screen may be a technical fault, but the missing close control and store redirect are described as the operative advertisement design.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "after seeing the ads, there is no way to close it. No cross mark on the screen , if you try to click anywhere on the screen it takes you to store."
  - why: The in-game advertisement has no dismissal control and redirects every tap to the store, compelling the player to remain on the ad screen.

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
The earlier portion alleges that purchased Poké Balls are consumed faster because captures break out, leading to further purchases. However, the account owner explicitly states that they did not write that portion and specifically repudiates its claim about speaking to other players, so those alleged mechanics are not treated as the reviewer's own account. The mechanic the genuine edit does describe is a review being posted under the player's identity without their authorship. That is impersonation through the player's account and falls within Friend Spam / Impersonation even though the destination is an app-store review.
```

**Labels assigned**

- `S_FriendSpamImpersonation` - ok
  - span: "I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE"
  - why: The edit states that a review containing fabricated personal claims was posted under the player's identity without their authorship.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `5e6a5625-5291-4f0e-897c-1b63c1a26494` - MONOPOLY GO!

> I loved this game until the new season started. Suddenly I get no rewards for inviting friends and getting them to join facebook. I am struggling to get dices and when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way... And today. Well, I cannot log in to the game at all. It keeps giving me an internet connection error which is absolute nonsense. I have connected to 3 different wifi connections. BS!!😡

| | labels |
|---|---|
| gold | `M_Gambling`, `P_RewardMania`, `S_ForcedFellowship` |
| pred | `M_Gambling`, `P_RewardMania` |
| **missed** | `S_ForcedFellowship` |

**Did the model consider what it missed?**

- `S_ForcedFellowship` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer says the referral rewards stopped after the new season, so the current text negates rather than establishes an active incentive for inviting friends; Forced Fellowship is not assigned. The reviewer also describes accumulating more than 500 dice and staking them at the maximum bet on chance-based play, without obtaining the desired random board events. This is a wager using an earned game resource. The repeated duplicate stickers describe unwanted results from a variable reward pool. The internet connection error is explicitly presented as a technical malfunction, so R11 excludes it.
```

**Labels assigned**

- `M_Gambling` - ok
  - span: "when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists."
  - why: The player stakes accumulated dice at the maximum bet in chance-based play for possible board outcomes.
- `P_RewardMania` - ok
  - span: "Stickers are duplicates all the way..."
  - why: Repeated duplicate stickers imply unwanted random outcomes from the sticker reward pool.

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
The reviewer describes a sticker collection whose final one or two items are effectively withheld unless the player spends substantial money. This simultaneously establishes a paid barrier to completing an in-game goal, a collection-completion mechanic, and monetized artificial scarcity focused on the final stickers. The broad statements about addiction, expense, and completing goals only about one time in a hundred do not identify additional mechanics such as wagering or a randomized reward-delivery system. The claim that a five-star rating is required to write a review describes review-interface manipulation, but none of the available labels covers that behavior without improperly treating it as a monetary UI pattern.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them."
  - why: The final stickers are described as deliberately scarce, with obtaining them tied directly to substantial spending.
- `M_PayToProgress` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them."
  - why: Completing the sticker goal is described as effectively impossible unless the player pays substantial money.
- `P_CompleteTheCollection` - ok
  - span: "you will never get the last one or two"
  - why: The mechanic centers on obtaining the final missing stickers needed to complete a collection.

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
The reviewer describes collecting stickers to complete sets. The sticker-delivery system repeatedly gives duplicate items rather than needed ones, indicating unpredictable or unwanted drops from a reward pool. Completing every set is the stated goal, so the collection mechanic is active. The reviewer also says set completion is prevented unless the player pays, making payment the route past the progression barrier. The review does not establish that money buys randomized attempts rather than reliably enabling completion, so Gambling is not assigned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: The reviewer states that completing the sticker sets is blocked unless the player pays.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: Finishing all sticker sets is an explicit goal of acquiring every item required for the collections.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: Repeated duplicate stickers imply unwanted outcomes from a reward pool rather than predictable delivery of needed items.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (12)

### `5f3e71b5-200c-45a3-b90e-e08b0dc0e1a3` - Cash Frenzy™ - Casino Slots

> Is a good game, but I will like to place my formal complain about the genie game, in multiple times whe the wheel spin after stopping on a great price the genie move the wheel to a spin tag, and then the prices after the spin are way lower than the original price, from 100 million with 5x multiplier to a 48 million. Is the only part I don't like. There should be a player choice to keep or spin.

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_RewardMania` |
| pred | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `P_RewardMania` |
| **spurious** | `P_OptimismAndFrequencyBiases` |

**Model analysis**

```
The reviewer describes a chance-based prize wheel whose displayed outcome is allegedly altered after it appears to have stopped. The genie repeatedly moves the wheel away from a large prize to a spin result, after which the player receives a substantially smaller prize. This describes a variable reward mechanism, an assertion that the game manipulates or predetermines outcomes, and repeated engineered near-misses involving memorable high prizes. No wager, purchased spin, or monetary stake is described, so Gambling does not apply. The lack of a choice to keep the first prize concerns the wheel's outcome rule, not an inability to end a gameplay session.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "after stopping on a great price the genie move the wheel to a spin tag"
  - why: The reviewer asserts that the game changes the wheel's apparent result after it stops, indicating concealed manipulation of the outcome.
- `P_OptimismAndFrequencyBiases` - **SPURIOUS**
  - span: "in multiple times whe the wheel spin after stopping on a great price the genie move the wheel to a spin tag"
  - why: The reviewer describes a recurring pattern of apparent high-prize near-wins being taken away, carrying both frequency perception and an engineered near-miss.
- `P_RewardMania` - ok
  - span: "the wheel spin after stopping on a great price the genie move the wheel to a spin tag, and then the prices after the spin are way lower than the original price"
  - why: The wheel and additional spin deliver unpredictable prizes, including a rerolled reward substantially different from the initially displayed result.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `95ddadb3-82cd-4042-8a51-cf8b3ed164c2` - Mech Arena - Shooting Game

> You stuck waiting 30 seconds just to connect to a match. This game makes it seem like they give so many rewards but if all just for show. Its difficult to get weapon upgrades or any percs others you stick battling to win. This kind of games just rob you of your time in my opinion

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `T_Grinding` |
| **spurious** | `T_Grinding` |

**Model analysis**

```
The 30-second wait is described as matchmaking or connection time, not an arbitrary in-game timer or regeneration schedule, so it does not qualify as Playing by Appointment. The claim that the rewards are "just for show" does not identify a specific reward-delivery mechanic or deception about outcomes. The reviewer does describe being stuck repeatedly battling and winning to obtain weapon upgrades or perks, linking a repeated gameplay activity to progression; this supports Grinding. No payment mechanic or paid shortcut is described.
```

**Labels assigned**

- `T_Grinding` - **SPURIOUS**
  - span: "Its difficult to get weapon upgrades or any percs others you stick battling to win."
  - why: The span implies that obtaining upgrades and perks requires the player to remain stuck repeatedly battling for wins, making repeated combat the activity required for progress.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `21021f9a-e106-4e51-b01d-3fe4a4c941fc` - MONOPOLY GO!

> Deleted the game now. The latest event I was about to get 525 dice as reward, I had 3 left to go and I ran out of dice, it said 2Days left. Now just logged in after sleeping and the event is now changed. Deleting this game and what an absolute waste of time. Never purchased anything coz i have trust issues with F2P model games, and my gutt was right all along. Fun when it lasted, but that was a low blow.

| | labels |
|---|---|
| gold | `T_PlayingByAppointment` |
| pred | `P_AestheticManipulation`, `P_EasyToGetHardToLose`, `T_PlayingByAppointment` |
| **spurious** | `P_AestheticManipulation`, `P_EasyToGetHardToLose` |

**Model analysis**

```
The reviewer describes a time-limited event with a 525-dice reward and a displayed countdown of two days. They had nearly completed the event, ran out of dice, and returned after sleeping, only to find that the event had changed despite the stated time remaining. This shows an event schedule controlling reward availability and a partially completed goal drawing the player back. The displayed countdown also appears to have misrepresented when the event would end. The reference to F2P games and never purchasing anything does not itself describe a paid progression route, and running out of dice does not specify a regeneration wait or purchase prompt.
```

**Labels assigned**

- `P_AestheticManipulation` - **SPURIOUS**
  - span: "it said 2Days left. Now just logged in after sleeping and the event is now changed."
  - why: The displayed two-day countdown appears to have falsely represented how long the event and its reward would remain available.
- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "The latest event I was about to get 525 dice as reward, I had 3 left to go and I ran out of dice, it said 2Days left. Now just logged in after sleeping"
  - why: Being only three steps from the reward leaves a nearly completed goal that implies why the reviewer returned after sleeping.
- `T_PlayingByAppointment` - ok
  - span: "it said 2Days left. Now just logged in after sleeping and the event is now changed."
  - why: The event's schedule determines when the reward remains available, and the reviewer loses the opportunity after returning later.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b2dc0bc8-8ebe-4c48-bc05-38d0d65acb84` - Last War:Survival Game

> It's a nice game, but it's set up in a pay to win way. I played for 10 days, and the update times for your base are becoming ridiculous. Everything scales endlessly, there is kinda no point to look forward to, just more grind. The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff. Alliances are also weird, with the top ones dictating what to develop, what to rush, etc. If you are not in one then you get attacked and bullied. Not a great experience.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_UIMisdirection`, `S_Competition`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| pred | `M_PayToProgress`, `M_UIMisdirection`, `S_Competition`, `T_Grinding`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| **spurious** | `T_Grinding` |

**Model analysis**

```
The review describes several current design mechanics. Real-money spending grants competitive advantage, explicitly framed as pay-to-win. Base upgrades are governed by increasingly long timers, imposing waits before progression. Progression and required effort scale without an attainable endpoint, with the reviewer explicitly describing continued grinding. The interface is allegedly made confusing and overwhelming for the deliberate purpose of pushing purchases, which satisfies UI Misdirection rather than a general UI-quality complaint. Alliances and attacks place players in competition. Being attacked when outside an alliance does not assign Forced Fellowship because the coerced-grouping boundary excludes joining for protection, and the bullying does not assign Encourages Anti-Social Behavior because no reward or gain for the aggressor is described.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "it's set up in a pay to win way"
  - why: The reviewer explicitly states that spending provides an advantage in the game.
- `M_UIMisdirection` - ok
  - span: "The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff."
  - why: The span attributes the confusing interface to a deliberate purpose against the player's intent: steering the player toward purchases.
- `S_Competition` - ok
  - span: "If you are not in one then you get attacked and bullied."
  - why: The alliance and attack system places players and player groups against one another.
- `T_Grinding` - **SPURIOUS**
  - span: "just more grind"
  - why: The reviewer explicitly identifies repetitive effort as the continuing requirement for progression.
- `T_InfiniteTreadmill` - ok
  - span: "Everything scales endlessly, there is kinda no point to look forward to, just more grind."
  - why: Endless scaling means the progression target continually expands rather than reaching a meaningful completion point.
- `T_PlayingByAppointment` - ok
  - span: "the update times for your base are becoming ridiculous"
  - why: The context implies increasingly long base-upgrade timers that make the player wait for progression.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `3c46f5e0-6091-43dc-94a0-e3af3259a63d` - Cashman Casino Slots Games

> Resently cashman had changed it's bingo rewards and daily rewards. However lve found that I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards. The most I can seem to get on the timed rewards is 40,000. I'd not pay just to get my daily rewards. So I'm deleting them.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_WasteAversion`, `T_DailyRewards` |
| pred | `M_Gambling`, `M_IntermediateCurrency`, `M_PayToProgress`, `M_WasteAversion`, `T_DailyRewards` |
| **spurious** | `M_Gambling`, `M_IntermediateCurrency` |

**Model analysis**

```
The reviewer describes a daily reward task that cannot be completed unless the player wagers 50,000 units. The game supplies at most 40,000 through timed rewards, leaving a concrete 10,000-unit shortfall. The statement that the reviewer would need to pay implies that real money can be used to obtain additional wagering currency and overcome this shortfall. Thus, the review describes a daily-return incentive, casino gambling with virtual currency, paid progression through the daily task, conversion of money into wagering currency, and a deliberately insufficient currency amount that prompts a further purchase. The timed rewards do not independently establish Playing by Appointment because the review does not describe their waiting interval or a timer directly blocking general progression.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "unless I bet 50,000"
  - why: The player must wager virtual currency in this casino-slots game, which is an explicit stake in chance-based play.
- `M_IntermediateCurrency` - **SPURIOUS**
  - span: "The most I can seem to get on the timed rewards is 40,000. I'd not pay just to get my daily rewards."
  - why: The contrast between insufficient free wagering funds and paying implies that real money can be converted into additional in-game currency.
- `M_PayToProgress` - ok
  - span: "I'd not pay just to get my daily rewards."
  - why: Payment is presented as the route to overcoming the currency shortage and completing the daily reward task.
- `M_WasteAversion` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards. The most I can seem to get on the timed rewards is 40,000."
  - why: The game supplies 40,000 against a 50,000 requirement, creating a realized 10,000-unit shortfall that pressures the player to obtain more currency.
- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards."
  - why: The daily reward is tied to completing a daily wagering requirement, and failing that requirement forfeits the reward opportunity.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `176aaa1f-d8f9-4a1a-9f29-64902f13be5c` - All in Hole: Black Hole Games

> I would give 5 stars, but I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used.🤨😒🙄😥

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `T_MandatoryMarathon` |
| pred | `M_IntermediateCurrency`, `M_WasteAversion`, `T_MandatoryMarathon` |
| **spurious** | `M_WasteAversion` |

**Model analysis**

```
The reviewer describes accumulated game value disappearing after they stop playing: a full bag becomes empty, and coins they both earned and bought are consumed. The named bag is game-specific, so a search was needed to identify it. The search established that Molly's Bag contains boosters accumulated through consecutive level wins and normally resets after a failed level. Thus, losing the full bag upon leaving represents forfeiture of accumulated progress when ending a session. The coins are also an in-game currency obtainable both through play and purchase, and their unexplained consumption realizes a loss of held value. The reviewer does not explicitly attribute this behavior to a bug or glitch.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "coins that I earned and purchased"
  - why: The span states that the in-game coins can be acquired through purchase as well as earned through gameplay.
- `M_WasteAversion` - **SPURIOUS**
  - span: "coins that I earned and purchased used"
  - why: Coins already held by the player, including purchased coins, are consumed while the player is away, demonstrating realized loss of accumulated value.
- `T_MandatoryMarathon` - ok
  - span: "I leave the game with my bag full only to come back with it empty"
  - why: Stopping play causes the accumulated bag bonus to be forfeited, preventing the player from ending at their chosen time without losing progress.

**Search:** `All in Hole Black Hole Games bag full empty coins used when away` -> The official support page establishes that Molly's Bag contains boosters earned by winning consecutive levels and resets after a failed level. ([homa.helpshift.com](https://homa.helpshift.com/hc/en/9-all-in-hole/faq/22-what-is-molly-s-bag/?utm_source=openai))

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
The review describes a time-limited card collection made up of cards obtained from packs. The player collects cards to complete a set and earn its completion reward, but reports that packs stop producing new cards as the player approaches completion, particularly near the collection's expiration. This describes a collection-completion mechanic, unpredictable pack rewards with missing or duplicate outcomes, alleged outcome manipulation based on proximity to completion and expiry, and a game-set deadline that causes the completion reward to be lost. The review does not mention paying for packs or cards, so Gambling, Pay to Progress, and Deceptive Luxury are not supported.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion"
  - why: The mechanic requires collecting a complete card set to obtain a completion reward.
- `P_IllusionOfControl` - **SPURIOUS**
  - span: "new cards don't appear again especially when the set is almost expiring"
  - why: The reviewer alleges that pack outcomes are secretly adjusted to withhold needed cards as the deadline approaches.
- `P_RewardMania` - **SPURIOUS**
  - span: "include new cards in every card pack because I noticed when one is almost close to completing a set, new cards don't appear again"
  - why: Card packs deliver uncertain outcomes, requiring repeated openings while needed new cards may fail to appear.
- `T_PlayingByAppointment` - ok
  - span: "you will miss the reward for the set completion because they don't add new sets to the cards once the collection is about to end"
  - why: The collection ends on the game's schedule, and failing to complete it before that deadline forfeits the set-completion reward.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `12267c1e-47ba-4984-97c8-768e820ceb1c` - Bingo Blitz™️ - Bingo Games

> not very user-friendly. no apparent reachable goals within a decent amount of time. I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| pred | `M_DeceptiveLuxury`, `M_EasyToPurchase`, `M_Gambling`, `M_IntermediateCurrency`, `M_PayToProgress`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania`, `T_Grinding` |
| **spurious** | `M_DeceptiveLuxury`, `M_Gambling`, `M_IntermediateCurrency`, `M_PayToProgress`, `P_RewardMania` |

**Model analysis**

```
The general statement that the game is not user-friendly is an evaluation and is not coded. The reviewer describes repeatedly playing bingo rounds to obtain photos, tying a named repetitive activity to progress toward a collection. The missing photos form a set that the player is trying to complete. After a failed round, the game repeatedly presents a paid-currency offer for another opportunity at the missing photo; this is a purchase prompt intercepting play and a costly second chance at a scarce collection item. The reviewer distinguishes spending coins from ultimately wasting money, implying that real money enters through the virtual currency. The purchased opportunity still depends on the bingo round's chance outcome, so the paid stake, randomized reward delivery, and external collection progress are all present. The claim that the offer promises the photo while actually delivering only another opportunity also describes misleading offer wording. The repeated failure is not attributed to a bug or technical fault.
```

**Labels assigned**

- `M_DeceptiveLuxury` - **SPURIOUS**
  - span: "after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set"
  - why: After the player misses a needed photo, the game sells a second opportunity to obtain that specific scarce collection item.
- `M_EasyToPurchase` - ok
  - span: "after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set"
  - why: Every lost round triggers an immediate spending prompt tied to continuing the attempt for the missing photo.
- `M_Gambling` - **SPURIOUS**
  - span: "I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money"
  - why: The player repeatedly stakes virtual currency connected to real-money loss for a chance to obtain the photo, without a guaranteed successful outcome.
- `M_IntermediateCurrency` - **SPURIOUS**
  - span: "I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money"
  - why: The distinction between spending coins on the offer and wasting money implies that real money was converted into the virtual coins being spent.
- `M_PayToProgress` - **SPURIOUS**
  - span: "no apparent reachable goals within a decent amount of time. I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set"
  - why: Spending currency is presented as the route to obtaining a missing collection item and advancing the set-completion goal outside the wager itself.
- `P_AestheticManipulation` - ok
  - span: "it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED"
  - why: The reviewer describes the offer's question as promising that spending will claim the photo, although it actually purchases only another chance.
- `P_CompleteTheCollection` - ok
  - span: "claim a photo I don't have to complete the set"
  - why: The mechanic targets the player's pursuit of the missing photo required to finish an in-game set.
- `P_RewardMania` - **SPURIOUS**
  - span: "I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set"
  - why: Obtaining the desired photo depends on repeated bingo attempts with an unpredictable reward outcome.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The player repeatedly performs bingo rounds in order to obtain the photos needed for progress.

**Search:** `Bingo Blitz photos offer spend extra coins claim missing photo complete set after round` -> Bingo Blitz's official Second Chance Cards information established that a missed Pic is offered in the next round: the specific Pic is guaranteed to appear, but the player must still achieve a bingo on it to receive it, so the purchase is another chance rather than a guaranteed photo.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `84bbc363-d55a-4cf1-a557-c61ed7ab82bc` - Last War:Survival Game

> Once you get past building the city block stage, it gets kinda boring. It's just grinding resources trying not to get raided so you can level up to have a few more attempts at the left right scroller game. The advertisement that's really becomes not that great. The bigger alliances all just attack the smaller alliances and take their resources. I dedicated some time to this game and to my alliances and am disappointed with current status.

| | labels |
|---|---|
| gold | `S_Competition`, `S_EncouragesAntiSocialBehavior`, `T_Grinding` |
| pred | `P_EasyToGetHardToLose`, `S_Competition`, `S_EncouragesAntiSocialBehavior`, `T_Grinding` |
| **spurious** | `P_EasyToGetHardToLose` |

**Model analysis**

```
The reviewer describes a progression loop in which resources must be repeatedly gathered to level up and obtain more attempts at another game mode. Those accumulated resources are exposed to raids, so protecting them affects how the player plays. The alliance system also creates direct competition, with larger alliances gaining resources by attacking smaller ones; because the benefit specifically comes from stronger groups preying on weaker groups, this is both competition and incentivized asymmetric harm. The reference to an advertisement does not describe an in-game forced or rewarded ad view, so it does not trigger Advertisement. Dedicating time to an alliance does not by itself establish a social obligation to continue playing.
```

**Labels assigned**

- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "grinding resources trying not to get raided"
  - why: The player must protect accumulated resources from raids, making already-earned value influence continued play.
- `S_Competition` - ok
  - span: "The bigger alliances all just attack the smaller alliances and take their resources."
  - why: The alliance system places groups against one another through attacks and resource seizure.
- `S_EncouragesAntiSocialBehavior` - ok
  - span: "The bigger alliances all just attack the smaller alliances and take their resources."
  - why: The design rewards stronger alliances for asymmetrically targeting weaker alliances by letting them take the victims' resources.
- `T_Grinding` - ok
  - span: "It's just grinding resources trying not to get raided so you can level up to have a few more attempts at the left right scroller game."
  - why: The reviewer identifies repetitive resource gathering as the activity required to level up and unlock more attempts.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `7b564746-b769-4856-b686-529f8717c3ba` - Candy Crush Soda Saga

> I like the game except: 1. I was charged 10 gold pcs for 5 moves, I had 2 moves left. I had 7 moves but only used 1 move. 2. I paid for a pkg unlimited lives ect. I got the etc. but not the lives. 3. The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone. 4. You cannot win enough gold to play without buying sometimes. 5. The packages need to cost less. 6. When I buy pkg should not be timed.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `M_PayToProgress`, `T_PlayingByAppointment` |
| pred | `M_IntermediateCurrency`, `M_PayToProgress`, `M_WasteAversion`, `T_PlayingByAppointment` |
| **spurious** | `M_WasteAversion` |

**Model analysis**

```
The review describes three functional designs alongside one apparent delivery fault. The unlimited-lives package not providing the lives is attributed to a purchase malfunction, so R11 excludes that failure. The timed bonuses continue expiring while the player is offline, making their availability operate on the game’s clock. The reviewer also says earned gold is insufficient for continued play, requiring purchases; gold is therefore both a paid route past a play barrier and an intermediate virtual currency. Finally, the reviewer identifies purchased packages as timed, which means unused paid value can expire. Complaints that packages cost too much, or that purchased moves were not fully used, do not alone establish additional mechanics such as accidental purchasing because no missing confirmation or deceptive control is described.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The antecedent of “buying” is gold, implying that real money is converted into the virtual gold used to play.
- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The amount of freely earned gold is insufficient for continued play, making purchases necessary at times.
- `M_WasteAversion` - **SPURIOUS**
  - span: "When I buy pkg should not be timed."
  - why: A purchased package has a timer, implying that any unused portion of the paid package expires and is forfeited.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone."
  - why: The bonuses continue counting down during absence and can disappear overnight, so their use is scheduled by the game rather than by the player.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b93c432d-19c0-4c6c-a2d4-bb9b21a436f3` - Dice Dreams™️

> A literal brain-rot game no wonder why they're tryna promote it through Free Cash. Also if you're thinking of making in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates! A real SCAM. Play it if u want but there are games that are actually good also, DON'T GET IN-APP PURCHASES!

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_Gambling`, `M_PayToProgress`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_EasyToGetHardToLose`, `P_RewardMania` |
| **spurious** | `M_Gambling`, `M_PayToProgress`, `P_EasyToGetHardToLose` |

**Model analysis**

```
The reviewer describes a nearly completed card album: only two cards remain, and completing it awards a grand prize. That partial completion directly motivates the reviewer to spend money on a deal intended to supply the missing cards. The purchased deal presents its cards as new, but delivers duplicates instead. This describes a paid chance-based card-reward mechanism with unwanted duplicate outcomes, as well as misleading purchase text. The causal wording—having only two cards left, "so" buying the deal—also shows the partially completed goal increasing the cost of walking away.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "i bought a deal which promised i would get NEW cards, and all i got were useless duplicates"
  - why: Real money purchases access to card rewards whose actual results can be unwanted duplicates, establishing a paid chance-based reward.
- `M_PayToProgress` - **SPURIOUS**
  - span: "so i bought a deal which promised i would get NEW cards"
  - why: The paid deal is offered as a way to acquire missing cards and advance toward album completion.
- `P_AestheticManipulation` - ok
  - span: "a deal which promised i would get NEW cards, and all i got were useless duplicates"
  - why: The offer's text allegedly promises new cards while the purchased contents are duplicates, describing misleading purchase wording.
- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The reviewer is pursuing the final two items needed to complete a card album and obtain its completion prize.
- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "I had two cards left which would grant me the grand prize for completing an album, so i bought a deal"
  - why: Being only two cards short of the prize motivates the purchase, showing that investment in a partially completed goal makes abandoning it costly.
- `P_RewardMania` - ok
  - span: "all i got were useless duplicates"
  - why: Duplicate card drops describe unpredictable delivery from a reward pool rather than merely complaining that a fixed reward is too small.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `727cc804-9d4b-48ef-8774-2799a2a8de08` - Genshin Impact

> with every incoming patch, we get less and less rewards and for me that wouldn't be a problem but the Meta changes more and more every single day basically forcing us to pull for new characters if we want to actually do damage. the game is getting more and more pay 2 win and the quality of the game is becoming lower. in the new archon quest when we were talking to mavuika, a multi billion dollar company just put an insanely bad picture of Natlans scenery as the background, y'all can do better.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_PowerCreep`, `P_RewardMania` |
| pred | `M_Gambling`, `M_PayToProgress`, `M_PowerCreep`, `P_RewardMania` |
| **spurious** | `M_Gambling` |

**Model analysis**

```
The reviewer describes the combat meta repeatedly changing so that newer characters are increasingly necessary to deal effective damage. This implies that previously acquired characters lose practical value as new patches and characters arrive, which is Power Creep. Obtaining those new characters requires pulls, explicitly naming a gacha delivery mechanic. The reviewer connects those pulls to an increasingly pay-to-win game, establishing both a monetary stake in the chance-based character system and a paid gameplay advantage. The declining reward amounts alone concern reward value rather than a qualifying delivery mechanism. The low-quality quest background is a general production-quality complaint and does not describe a coded mechanic.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "basically forcing us to pull for new characters if we want to actually do damage. the game is getting more and more pay 2 win"
  - why: The character pulls are a chance-based mechanic, and the adjoining pay-to-win statement connects obtaining the necessary characters to spending.
- `M_PayToProgress` - ok
  - span: "the game is getting more and more pay 2 win"
  - why: The reviewer explicitly states that spending increasingly provides the advantage needed to remain effective in gameplay.
- `M_PowerCreep` - ok
  - span: "the Meta changes more and more every single day basically forcing us to pull for new characters if we want to actually do damage"
  - why: The need for new characters to continue dealing damage implies that older acquired characters are losing effectiveness as the meta changes.
- `P_RewardMania` - ok
  - span: "pull for new characters"
  - why: Pulling for characters explicitly names a gacha-style variable reward delivery mechanism.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_Gambling` | 1 | 4 |
| `P_EasyToGetHardToLose` | 0 | 3 |
| `M_PayToProgress` | 0 | 3 |
| `P_RewardMania` | 1 | 2 |
| `S_Competition` | 1 | 1 |
| `P_IllusionOfControl` | 1 | 1 |
| `M_WasteAversion` | 0 | 2 |
| `M_DeceptiveLuxury` | 1 | 1 |
| `M_IntermediateCurrency` | 0 | 2 |
| `T_Grinding` | 0 | 2 |
| `P_OptimismAndFrequencyBiases` | 1 | 1 |
| `S_Reciprocity` | 2 | 0 |
| `M_UIMisdirection` | 1 | 0 |
| `P_AestheticManipulation` | 0 | 1 |
| `S_ForcedFellowship` | 1 | 0 |

