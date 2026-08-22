# Error review - gpt-5.6-luna_none_teacher_v1

`gpt-5.6-luna` / reasoning `` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v1.txt` sha `e8cd52987c33`  
micro-F1 **0.824** (P 0.940 / R 0.733) - **19 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 4 | said NONE, gold had labels |
| SWAP | 4 | picked different labels than gold |
| MISSED ONLY | 11 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 0 | found all gold, added extras |

## The diagnostic that matters

Of **23** missed labels, **11** (48%) were named in the model's own analysis and dropped anyway; **12** (52%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `M_PayToProgress` | 3 | 1 |
| `T_Grinding` | 2 | 0 |
| `S_Reciprocity` | 1 | 1 |
| `P_RewardMania` | 1 | 1 |
| `P_AestheticManipulation` | 0 | 2 |
| `M_IntermediateCurrency` | 0 | 2 |
| `P_IllusionOfControl` | 1 | 0 |
| `M_WasteAversion` | 1 | 0 |
| `M_Gambling` | 0 | 1 |
| `S_Competition` | 1 | 0 |
| `M_RecurringFee` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `T_Advertisement` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `M_EasyToPurchase` | 0 | 1 |

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
The review consists entirely of requests for hypothetical or changed features: auctions using in-game currency, removing an option, an account-switching upgrade-time widget, and hidden troop statistics. Under R12, proposed additions or changes do not trigger labels. The mention of an existing removal option does not describe a dark-pattern mechanic from the review, and no applicable label is otherwise established.
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
The review describes being unable to request troops from the clan because of an update, and explicitly says it needs to be fixed. Although troop requests would normally indicate resource exchange under S_Reciprocity, R11 suppresses labeling when the described behavior is a technical malfunction. No other mechanic is described.
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
The review describes misleading advertising outside the game application, which is out of scope under R13 and does not trigger T_Advertisement or another label. The in-game activities—making an army, training, building, and gathering resources—are described as chores needed to reach occasional puzzles, but the text does not explicitly describe repetitive tasks or repeated cycles, so T_Grinding is not assigned under its boundary rule. No other qualifying mechanic is described.
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
The review describes being stuck on one level for almost two months and refusing to pay for power-ups. This does not explicitly establish that payment is required for progress, so M_PayToProgress is rejected. The single blocked level does not show that the game itself extends beyond completion, so T_InfiniteTreadmill is rejected. The requested daily login rewards are hypothetical rather than an existing mechanic, so T_DailyRewards is rejected under R12. No applicable mechanic label remains.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (4)

### `0bc09fc3-6436-4a24-855e-0fdc56887918` - Fishdom

> EDIT 1/17/2023: Customer Service can't make good on 9 diamonds when game element doesn't appear within 5 original moves and 5 additional moves. It is a fun game, you don't have to pay to win. I suggest after this cust. svc experience that you don't buy from this game beyond the pass.Get friends and a team and trade lives.

| | labels |
|---|---|
| gold | `M_RecurringFee`, `S_Reciprocity` |
| pred | `M_WasteAversion`, `S_Reciprocity` |
| **missed** | `M_RecurringFee` |
| **spurious** | `M_WasteAversion` |

**Did the model consider what it missed?**

- `M_RecurringFee` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes 9 diamonds that were not recovered when a game element failed to appear, which is a realized loss of in-game currency and supports Waste Aversion. It also explicitly describes trading lives with friends and teammates, which is resource exchange among existing players and supports Reciprocity. The move-count statement does not by itself establish Grinding, Gambling, Reward Mania, or Playing by Appointment. The mention of paying and a pass does not clearly describe a payment-gated progression mechanic or recurring-fee behavior.
```

**Labels assigned**

- `M_WasteAversion` - **SPURIOUS**
  - span: "Customer Service can't make good on 9 diamonds"
  - why: The span describes 9 diamonds of in-game value that were not recovered, showing forfeited currency.
- `S_Reciprocity` - ok
  - span: "Get friends and a team and trade lives."
  - why: The span explicitly describes exchanging resources with other players.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fd1230ab-7d12-4aeb-a425-e37ed06bcd5c` - Pokémon GO

> I love this game, just started playing about 2 months ago. Though I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way. I feel taken advantage of. 3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| pred | `M_PayToProgress`, `S_FriendSpamImpersonation` |
| **missed** | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `P_IllusionOfControl` - considered and rejected -> **rule interpretation**
- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes purchased Poké Balls being consumed quickly because captures keep breaking out, followed by having to purchase more; this is a payment-linked continuation barrier, so M_PayToProgress applies. The claim that captures keep breaking out after purchasing suggests suspicion but does not explicitly establish rigged or hidden outcome determination, so P_IllusionOfControl is rejected under its boundary rule. The text also states that a review was posted without the reviewer writing it, which is an in-app action through the player’s account and triggers S_FriendSpamImpersonation. M_IntermediateCurrency is rejected because Poké Balls are purchased items, not an in-game currency acquired with real money.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: The capture mechanic rapidly consumes the resource and requires purchasing more to continue using it.
- `S_FriendSpamImpersonation` - ok
  - span: "I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE"
  - why: The reviewer says a store review and its claimed social outreach were posted under their account without their authorship.

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
The review describes a daily-reward system that requires completing a betting target, so T_DailyRewards applies. The phrase "bet 50,000" describes a wager in a slots game, supporting M_Gambling even though no real-money purchase is mentioned. Playing by Appointment is rejected because no real-world schedule or wait gate is described. Waste Aversion is rejected because the 40,000 versus 50,000 gap is not described as stranded currency or a purchase-triggering shortfall. Reward Mania is rejected because the review does not describe unpredictable reward delivery.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "unless I bet 50,000"
  - why: This explicitly describes placing a bet within a casino slots game.
- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000"
  - why: The daily-reward mechanic requires completing a qualifying task or wager, and the reviewer cannot complete the daily rewards without it.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `7b564746-b769-4856-b686-529f8717c3ba` - Candy Crush Soda Saga

> I like the game except: 1. I was charged 10 gold pcs for 5 moves, I had 2 moves left. I had 7 moves but only used 1 move. 2. I paid for a pkg unlimited lives ect. I got the etc. but not the lives. 3. The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone. 4. You cannot win enough gold to play without buying sometimes. 5. The packages need to cost less. 6. When I buy pkg should not be timed.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `M_PayToProgress`, `T_PlayingByAppointment` |
| pred | `M_PayToProgress`, `M_WasteAversion`, `T_PlayingByAppointment` |
| **missed** | `M_IntermediateCurrency` |
| **spurious** | `M_WasteAversion` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes timed bonuses expiring while the player is away, which imposes a game-controlled schedule and forfeits rewards, so T_PlayingByAppointment applies. It also describes paying for more moves than were used, showing wasted in-game value, so M_WasteAversion applies. The inability to earn enough gold to continue without buying describes a paid alternative to continued play, so M_PayToProgress applies. The missing lives from a purchased package is described as a failure to deliver the purchase, which is a technical or fulfillment fault rather than a deliberate dark pattern under R11. The package being timed is mentioned as a complaint, but no qualifying subscription, expiry-pressure, or purchase-term deception is explicitly described. No other label is supported.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The review states that progressing or continuing to play sometimes requires buying rather than earning enough gold through play.
- `M_WasteAversion` - **SPURIOUS**
  - span: "I was charged 10 gold pcs for 5 moves, I had 2 moves left. I had 7 moves but only used 1 move."
  - why: The player describes paying for a quantity of moves that was not fully usable, demonstrating wasted in-game value.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone."
  - why: Bonuses expire according to the game clock while the player is away, imposing a schedule and forfeiting rewards.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (11)

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
The review describes PvP battles, which are a mechanic involving competition against other players, so S_Competition applies. The crashing, lag, freezing, unresponsive controls, and inability to open gifts or trade are explicitly attributed to bugs or technical faults, so they do not trigger dark-pattern labels under R11. Gifts and trades are mentioned as unavailable because of crashes, not as a social obligation or active resource exchange mechanism.
```

**Labels assigned**

- `S_Competition` - ok
  - span: "the pvp & rockets battles"
  - why: This explicitly describes battles involving competition, satisfying the Competition label.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fdef27f2-9a21-4b8e-a04c-7a4753e0fb07` - 8 Ball Pool

> The game is great, but the user interface is completely rigged. Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins and are forced to buy real ones. ​We need a "Default Table Lock" or the game should always open the lowest bet table by default, not the highest! Fix this scammy feature. Giving 1 star

| | labels |
|---|---|
| gold | `M_Gambling`, `M_IntermediateCurrency`, `M_UIMisdirection` |
| pred | `M_IntermediateCurrency`, `M_UIMisdirection` |
| **missed** | `M_Gambling` |

**Did the model consider what it missed?**

- `M_Gambling` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes an interface that automatically selects the highest-bet table, causing unintended selection and mis-clicks; this satisfies UI Misdirection. It also explicitly describes players being forced to buy real coins, which establishes Intermediate Currency. Pay to Progress was considered but rejected because the review does not explicitly state that buying coins is required to advance or continue progression. Easy to Purchase was rejected because the described accidental action spends in-game coins, not real money directly. Waste Aversion and Easy to Get Hard to Lose were rejected because no stranded currency, exit cost, or accumulated investment affecting continued play is described.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "are forced to buy real ones"
  - why: This explicitly describes acquiring in-game coins with real money.
- `M_UIMisdirection` - ok
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins"
  - why: The interface directs the player toward a costly default option and causes unintended selection.

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
The review describes RNG as being manipulated against the player, which fits Illusion of Control because it asserts that outcomes are unfairly determined rather than merely reporting a losing streak. The complaint about needing to spend money and receiving weak rewards does not clearly state that payment is required for progression, so M_PayToProgress is rejected under R2 and its boundary rule. The cost and near-equivalent return describe poor reward value, not a demonstrated stranded or insufficient currency shortfall, so M_WasteAversion is rejected. No delivery mechanism such as random reward drops, repeated attempts, or gacha is explicitly described, so P_RewardMania is not assigned.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "the rng is so obviously against you"
  - why: The span asserts that the game manipulates or determines RNG outcomes against the player.

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
The review describes spending money to win an event and explicitly calls the game pay to play/pay to win, which satisfies Pay to Progress because payment is presented as necessary for success or advancement. The event suggests competition, but the text does not explicitly describe players competing against one another, so S_Competition is rejected. “Same old same old grinder” is a general evaluation without a named repetitive task, so T_Grinding is rejected under its boundary rule. No chance mechanic, currency conversion, timed schedule, collection goal, or other listed mechanic is described.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Calculated total spent on last event was 30k to win"
  - why: The span explicitly describes spending money to win the event, making payment a route to in-game success.

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
The review describes payment as necessary to win and to complete sticker collections, so M_PayToProgress applies. The last stickers are described as intentionally unavailable unless the player pays substantially, which supports M_DeceptiveLuxury through artificial scarcity tied to purchase. The sticker-completion goal supports P_CompleteTheCollection. I rejected M_Gambling because no explicit chance-based wagering or randomized purchase mechanic is described; the statement that a goal may be completed one out of a hundred times is too vague. I rejected P_EasyToGetHardToLose because addiction is mentioned only as a general warning, without accumulated investment making it difficult to quit.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "you will never get the last one or two unless you pay a lot of money to get them"
  - why: Describes artificially scarce stickers whose acquisition is tied to paying a large amount.
- `M_PayToProgress` - ok
  - span: "if you want to win anything on this game it will cost hundreds of dollars"
  - why: States that spending substantial money is required to win or progress in the game.
- `P_CompleteTheCollection` - ok
  - span: "complete a goal"
  - why: Describes pursuing completion of an in-game goal, in the context of completing sticker collections.

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
The review explicitly describes payment as necessary to get through the game: "You must buy add ons else you can't make it through" and "it's pure time waste if you're not paying," which satisfies Pay to Progress. The repeated attempts and prolonged level completion could suggest Grinding, but the text does not clearly identify a repetitive task being performed; it mainly reports slow progress and life depletion, so Grinding is rejected under its boundary rule. Playing by Appointment is rejected because no wait or regeneration timer is described. Daily Rewards, Easy to Get Hard to Lose, and other labels are not supported by an explicit mechanic.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through"
  - why: The review says payment is required to progress through the game.

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
The review describes leaving the game and returning to find held items and coins gone, indicating that exiting or stopping a session forfeits accumulated value. This satisfies Mandatory Marathon because the player cannot safely stop without losing holdings. Easy to Get, Hard to Lose was considered but rejected because the review reports the loss without describing reluctance to quit; Waste Aversion was rejected because the loss is not a small currency shortfall or inventory-capacity waste.
```

**Labels assigned**

- `T_MandatoryMarathon` - ok
  - span: "I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used"
  - why: Leaving the game causes accumulated items and coins to be forfeited, making it costly to stop the session.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a2ece36d-c527-442d-8f18-9a16b63994c8` - War Robots Multiplayer Battles

> Its a p2w game. The only time you enjoy it is when you're new. As you progress, everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game. If you want to progress without paying money, goodluck! Even if you wanted to do f2p, you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it. Plus the only time you benofit by getting f2p rewards is ads... 💩

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `M_PayToProgress`, `M_PowerCreep`, `T_Advertisement` |
| pred | `M_EasyToPurchase`, `M_PayToProgress`, `M_PowerCreep` |
| **missed** | `T_Advertisement` |

**Did the model consider what it missed?**

- `T_Advertisement` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes payment as necessary for progression and for acquiring the newest bots, so M_PayToProgress applies. The phrase about a shifting meta and needing the newest bot indicates that older bots lose competitive value over time, so M_PowerCreep applies. In-app purchase offers appear before gameplay and intercept access to the game, satisfying M_EasyToPurchase. Advertisement is rejected because the review does not describe forced or rewarded ad viewing; S_Competition and S_FearOfMissingOutFOMO are rejected because keeping up is described as a progression problem, not explicit competition or anticipatory pressure.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game"
  - why: Purchase offers directly intercept gameplay before the player can begin playing.
- `M_PayToProgress` - ok
  - span: "If you want to progress without paying money"
  - why: The review explicitly states that progressing without payment is not possible.
- `M_PowerCreep` - ok
  - span: "keep up with shifting meta where you have to buy the newest bot with money instead of earning it"
  - why: The shifting meta and required newest bots indicate that newer releases diminish the value or viability of older bots.

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
The review describes repeatedly playing rounds to collect photos and complete a set, which supports Grinding and Complete the Collection. The offer to spend coins is a payment-like progression mechanic, but the review does not explicitly describe real money being converted into coins or state that payment is required for progress, so Pay to Progress and Intermediate Currency are rejected. The failure to receive the promised photo is not described as a bug or technical fault, and it does not establish gambling, reward randomness, or waste-aversion through leftover or insufficient currency.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok  _[span not verbatim]_
  - span: "collect 'photos' ... to complete the set"
  - why: The span explicitly describes acquiring items to complete an in-game collection.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The span describes repeating rounds as the activity required to pursue collection progress.

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
The reviewer describes an album-collection goal with two missing cards and a grand prize for completing it, which satisfies Complete the Collection. I considered Reward Mania because duplicates are mentioned, but the review does not explicitly describe a randomized delivery system or repeated chance-based attempts. I rejected Pay to Progress because the purchase was attempted to advance the album but did not establish that payment is required for progression. Advertisement is not assigned because promotion through Free Cash is out-of-game marketing under R13, and Easy to Purchase is not assigned because no purchase-friction mechanism is described.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The span explicitly describes acquiring the remaining cards to complete an album and obtain its completion reward.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `727cc804-9d4b-48ef-8774-2799a2a8de08` - Genshin Impact

> with every incoming patch, we get less and less rewards and for me that wouldn't be a problem but the Meta changes more and more every single day basically forcing us to pull for new characters if we want to actually do damage. the game is getting more and more pay 2 win and the quality of the game is becoming lower. in the new archon quest when we were talking to mavuika, a multi billion dollar company just put an insanely bad picture of Natlans scenery as the background, y'all can do better.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_PowerCreep`, `P_RewardMania` |
| pred | `M_PowerCreep`, `P_RewardMania` |
| **missed** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_PayToProgress` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes newer characters becoming necessary to deal damage, which devalues older characters and triggers Power Creep. The phrase "pull for new characters" names a gacha draw mechanic, triggering Reward Mania. I considered Pay to Progress and Gambling because the review says "pay 2 win," but it does not explicitly describe real-money spending or a paid stake tied to the pulls; the statement alone is a general characterization, so those labels are rejected under R2 and the Gambling boundary rule. Reduced rewards and poor scenery quality are not dark-pattern mechanics.
```

**Labels assigned**

- `M_PowerCreep` - ok
  - span: "the Meta changes more and more every single day basically forcing us to pull for new characters if we want to actually do damage"
  - why: The review says new characters are increasingly required for effective damage, implying older acquired characters lose value as the meta changes.
- `P_RewardMania` - ok
  - span: "pull for new characters"
  - why: The phrase names a gacha pull mechanic whose reward delivery sustains engagement.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_PayToProgress` | 4 | 1 |
| `M_WasteAversion` | 1 | 2 |
| `T_Grinding` | 2 | 0 |
| `S_Reciprocity` | 2 | 0 |
| `P_RewardMania` | 2 | 0 |
| `P_AestheticManipulation` | 2 | 0 |
| `M_Gambling` | 1 | 1 |
| `M_IntermediateCurrency` | 2 | 0 |
| `P_IllusionOfControl` | 1 | 0 |
| `S_Competition` | 1 | 0 |
| `M_RecurringFee` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `T_Advertisement` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `M_EasyToPurchase` | 1 | 0 |

