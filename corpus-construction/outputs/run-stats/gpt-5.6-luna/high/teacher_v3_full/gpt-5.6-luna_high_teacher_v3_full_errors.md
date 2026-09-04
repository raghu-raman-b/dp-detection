# Error review - gpt-5.6-luna_high_teacher_v3_full

`gpt-5.6-luna` / reasoning `high` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v3_full.txt` sha `a6ae58246360`  
micro-F1 **0.850** (P 0.919 / R 0.791) - **17 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 4 | said NONE, gold had labels |
| SWAP | 2 | picked different labels than gold |
| MISSED ONLY | 8 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 3 | found all gold, added extras |

## The diagnostic that matters

Of **18** missed labels, **1** (6%) were named in the model's own analysis and dropped anyway; **17** (94%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `S_Reciprocity` | 0 | 2 |
| `P_AestheticManipulation` | 0 | 2 |
| `S_Competition` | 1 | 1 |
| `M_IntermediateCurrency` | 0 | 2 |
| `T_MandatoryMarathon` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `S_FriendSpamImpersonation` | 0 | 1 |
| `M_WasteAversion` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `M_EasyToPurchase` | 0 | 1 |
| `M_Gambling` | 0 | 1 |
| `M_PayToProgress` | 0 | 1 |
| `P_RewardMania` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |

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
The review consists entirely of requests for hypothetical additions or changes: auctions using in-game currency, preventing removal of converted decorations, an account-switching upgrade timer widget, and hidden advanced troop statistics. These are not described as current game mechanics, so R12 prevents assigning labels. The existing mention of in-game currency appears only within a proposed auction feature and does not establish a real-money-to-currency conversion.
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
The reviewer reports a post-update malfunction: they can no longer request troops from their clan and ask for the problem to be fixed. Although troop requests would ordinarily involve an in-game resource exchange, the review attributes the inability to a technical issue rather than describing a functioning social mechanic. Under R11, no dark-pattern label applies.
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
The reviewer describes upgrades, stickers, boosters, and challenges, but the relevant mechanics are presented as desired changes rather than current design behaviors. Trading stickers within the app is a requested feature, and the proposed ability to use a purchased booster when challenged is also hypothetical. Mentioning Facebook only explains why the reviewer wants in-app trading; it does not describe the game sending messages or using the player's contacts. The review therefore supports no label.
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
The reviewer describes leaving the game with a full bag and returning to find the bag empty, while earned and purchased coins have also been consumed. This is a loss of inventory and currency after exiting, but the review presents it as an unexpected loss or malfunction rather than a deliberate game rule. It does not clearly describe inventory capacity forcing items to be deleted, a required play schedule, or any other codable design mechanic.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (2)

### `fd1230ab-7d12-4aeb-a425-e37ed06bcd5c` - Pokémon GO

> I love this game, just started playing about 2 months ago. Though I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way. I feel taken advantage of. 3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| pred | `M_PayToProgress`, `P_IllusionOfControl` |
| **missed** | `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**
- `S_FriendSpamImpersonation` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer alleges that after beginning to purchase Poké Balls, Pokémon break out more often, causing the balls to be consumed faster and making further purchases necessary. This describes a paid replenishment loop that supports continued capture gameplay, so payment is presented as necessary to keep progressing. It also alleges that the game manipulates catch outcomes after purchases, which is a hidden outcome-determination claim rather than merely reporting bad luck. The later edit retracts the claim about speaking with other players, but it does not describe a separate social mechanic.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "so I go through the balls faster so I have to purchase more"
  - why: The reviewer says consumable Poké Balls are depleted during capture attempts and that purchasing more is necessary to continue the gameplay.
- `P_IllusionOfControl` - ok
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out"
  - why: The reviewer alleges that purchasing changes the capture outcomes so Pokémon break out more often, asserting hidden manipulation of the game's outcome determination.

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

- `M_Gambling` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a UI that automatically moves the player to and selects the highest-stakes 1v1 table rather than leaving a neutral or low-stakes option selected. This steers accidental taps toward a costly competitive match and causes players to lose their in-game coins. The reviewer further says that depleted coins must be replenished by buying more with real money, making payment the route to continued access to the tables. The reference to the 1v1 section also describes player-versus-player competition. The mechanic is not an accidental real-money purchase itself, because the accidental loss is of in-game coins rather than a direct purchase.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "are forced to buy real ones"
  - why: The review describes the in-game coins as something that must be bought with real money, establishing a real-money-to-virtual-currency conversion.
- `M_PayToProgress` - **SPURIOUS**
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: After the UI causes the player to lose their coins, the review says payment is required to replenish them and continue using the betting tables.
- `M_UIMisdirection` - ok
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins"
  - why: The interface automatically directs the player to the highest-stakes table, steering attention and selection away from a safer default and toward accidental high-cost play.
- `S_Competition` - **SPURIOUS**
  - span: "go to the 1v1 section"
  - why: A 1v1 section is a player-versus-player competitive game mode.

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
The review primarily describes technical faults: crashing while opening gifts or trading, lag preventing Poké Ball throws and battle actions, and freezing while the opponent continues attacking. These malfunction explanations suppress labels for the affected gift/trade and battle-action behaviors under R11. However, the review also explicitly names PvP, which is a functional player-versus-player competition mechanic unrelated to the dark-pattern classification of the lag itself. No label applies to the bugs, since there is no download-wall behavior, session forfeiture, reward penalty, or other qualifying mechanic.
```

**Labels assigned**

- `S_Competition` - ok
  - span: "pvp"
  - why: The explicit reference to PvP identifies a game mode in which players compete against one another.

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
The review describes a base-building game that the reviewer experiences as repetitive, but “Same old same old grinder” is only a general characterization and names no repeated activity tied to progress, so it does not meet the Grinding boundary. The review explicitly describes spending money to win an event, including a reported expenditure of 30k, which is a pay-to-win mechanic: payment provides an advantage toward winning. The event appears competitive, but the review does not explicitly identify opponents, rankings, or competition against other players, so Competition is not assigned separately.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Calculated total spent on last event was 30k to win"
  - why: The reviewer describes a large real-money expenditure being used to win an in-game event, indicating that spending provides an advantage toward success.

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
The reviewer describes a daily-reward system that has been changed so the reward cannot be completed unless the player first bets 50,000. The daily reward is therefore an active recurring incentive with a gameplay requirement attached. The mention of timed rewards only describes the maximum amount earned and does not establish a wait timer or a chance-based paid wager. The reviewer says they would not pay, but payment is not actually required or shown as the route to progress, so no monetary label applies.
```

**Labels assigned**

- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The game provides daily rewards that can only be completed after meeting a required in-game betting target.

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
The review describes a payment-dependent game outcome: the reviewer says winning anything costs hundreds of dollars. It also describes a sticker collection whose final one or two items are effectively withheld unless the player pays a large amount, which makes album completion a collection goal and ties manufactured scarcity to purchase. The search confirms that Dice Dreams stickers are album collectibles and that WILD stickers can fill missing stickers, but the review itself does not clearly describe a gambling or random-reward mechanic, so those labels are not assigned.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: The final stickers are described as being made effectively unavailable unless the player pays heavily, tying manufactured scarcity to purchase.
- `M_PayToProgress` - ok
  - span: "if you want to win anything on this game it will cost hundreds of dollars"
  - why: The span states that winning in the game requires spending a large amount of real money.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two"
  - why: The reviewer is pursuing completion of a sticker collection and identifies the missing final items as the obstacle.

**Search:** `Dice Dreams stickers albums how are stickers obtained random` -> The Dice Dreams Help Center establishes that stickers belong to sticker albums and that WILD stickers can provide any missing sticker; it does not establish a gambling mechanic from this review.

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
The review describes a collection goal: the player repeatedly plays bingo rounds to collect photos and complete a set. The repeated-round activity is explicitly tied to progress, so this is Grinding, and the desire to complete the photo set supports Complete the Collection. The game also presents a post-loss offer to spend coins for a missing photo, but the review does not clearly establish that the coins were bought with real money, so Pay to Progress and Intermediate Currency are not assigned. The failure to receive the promised photo is reported as an outcome, not explicitly attributed to a bug or technical fault, but it does not by itself establish a listed dark-pattern mechanic beyond the collection and repetition.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "to complete the set"
  - why: The player is pursuing completion of an in-game collection of photos.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The reviewer names the repeated activity—playing round after round—and ties it directly to collecting photos as progress.

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
The review describes a sticker-collection system in which sticker rewards repeatedly produce duplicates, indicating an unwanted or variable reward delivery pattern. The player is trying to complete all sticker sets, so collection completion is an active goal. The review also states that completing the sets is unavailable unless the player pays, which makes payment a requirement for progress. There is no explicit statement that the stickers are obtained through a paid chance mechanic, so Gambling is not assigned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: The review states that completing the sets is impossible without payment, making further progress contingent on spending.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: The player is pursuing completion of a collection of sticker sets.
- `P_RewardMania` - ok
  - span: "getting stickers. always get duplicates."
  - why: The sticker-delivery system repeatedly gives unwanted duplicate items, indicating a variable reward pool that sustains attempts to obtain missing stickers.

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
The review describes several mechanics, but some are only complaints about value or a failed transaction. The game consumes or charges gold for move bundles in a way the reviewer considers wasteful, but the text does not clearly describe a purchase-confirmation problem or the specific stranded-currency pattern required for a label. The paid package failing to provide lives is attributed to a delivery problem, so it is not coded as a deliberate design pattern. The timed bonuses continue expiring while the player is offline, imposing a game-controlled schedule and making the player lose bonus time while away. The reviewer also says that earning enough gold is sometimes impossible without buying, which describes payment as the route to continued play. The package's timer reinforces the scheduling mechanic, while the request for lower prices is only an evaluation of cost.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The free route does not reliably provide enough gold to continue playing, making buying the paid alternative to continued access.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone."
  - why: Bonuses expire according to an in-game timer even while the player is offline, forcing the player to use them on the game's schedule.

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
The review describes an album-collection mechanic: the player was two cards short of completing an album and receiving its grand prize. That partially completed collection motivated a purchase, but the paid card deal delivered duplicate cards instead of the promised new cards. The duplicate outcome describes an unwanted reward drop from the card-acquisition system. The mention of Free Cash is external promotion and is out of scope, and the review does not explicitly establish a paid chance mechanic or that payment is required for progress.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The player is pursuing completion of an album collection, with the missing cards blocking the grand prize.
- `P_RewardMania` - ok
  - span: "i bought a deal which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: The paid card acquisition produced unwanted duplicate rewards rather than the desired new cards, describing the reward-delivery mechanic rather than merely the cards' value.

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
The review describes a 30-second matchmaking connection wait, but this is a service or queue delay rather than an in-game timer that gates gameplay, so it does not satisfy Playing by Appointment. The reviewer also describes weapon upgrades and perks as difficult to obtain through continued battling, implying repetitive battles are required to make progress and acquire those items. The complaint that rewards are only for show is too vague to establish a specific reward-delivery or deception mechanic, and the statement that the game robs time is evaluation rather than a separate mechanic.
```

**Labels assigned**

- `T_Grinding` - **SPURIOUS**
  - span: "Its difficult to get weapon upgrades or any percs others you stick battling to win."
  - why: The span ties obtaining upgrades or perks to sticking with repeated battling, describing a repetitive activity required to obtain progress-related rewards.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `5e6a5625-5291-4f0e-897c-1b63c1a26494` - MONOPOLY GO!

> I loved this game until the new season started. Suddenly I get no rewards for inviting friends and getting them to join facebook. I am struggling to get dices and when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way... And today. Well, I cannot log in to the game at all. It keeps giving me an internet connection error which is absolute nonsense. I have connected to 3 different wifi connections. BS!!😡

| | labels |
|---|---|
| gold | `M_Gambling`, `P_RewardMania`, `S_ForcedFellowship` |
| pred | `M_Gambling`, `P_RewardMania`, `S_ForcedFellowship`, `S_FriendSpamImpersonation` |
| **spurious** | `S_FriendSpamImpersonation` |

**Model analysis**

```
The review describes several functional systems. It says the game offers rewards for inviting friends through Facebook, which is a friend-recruitment mechanic and also implies invitations being sent or prompted through the player's social account. The reviewer then describes using more than 500 dice at the maximum bet setting for chance-based Shutdown or Bank Heist outcomes; the explicit bet language supports Gambling rather than merely coding an unlucky result. The sticker complaint describes repeated unwanted duplicates from a variable reward system, supporting Reward Mania. The login failure is explicitly attributed to an internet connection error, so it is a technical fault rather than a deliberate dark pattern. The search confirms that dice rolls can trigger Shutdown or Bank Heist and that duplicate stickers are a recognized outcome. ([monopolygo.helpshift.com](https://monopolygo.helpshift.com/hc/en/3-monopoly-go/faq/66-board/?pubDate=20250530&utm_source=openai))
```

**Labels assigned**

- `M_Gambling` - ok
  - span: "more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists"
  - why: The reviewer describes using an in-game dice resource at a maximum bet for chance-based Shutdown or Bank Heist outcomes.
- `P_RewardMania` - ok
  - span: "Stickers are duplicates all the way"
  - why: The sticker system repeatedly delivers unwanted duplicate rewards instead of new stickers, making the variable delivery mechanism the source of engagement and frustration.
- `S_ForcedFellowship` - ok
  - span: "no rewards for inviting friends and getting them to join facebook"
  - why: The game uses rewards to encourage the player to recruit friends through Facebook, even though the reviewer says the rewards are no longer being granted.
- `S_FriendSpamImpersonation` - **SPURIOUS**
  - span: "inviting friends and getting them to join facebook"
  - why: The span describes invitations being solicited or sent through the player's social account, which is messaging performed via the player's social graph.

**Search:** `MONOPOLY GO max bet dice shutdown bank heist stickers duplicates` -> The search established that dice rolls move the token and can trigger Shutdown or Bank Heist, and that duplicate stickers are a recognized sticker outcome. It did not independently establish 'max bet' as a named mode. ([monopolygo.helpshift.com](https://monopolygo.helpshift.com/hc/en/3-monopoly-go/faq/66-board/?pubDate=20250530&utm_source=openai))

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
The review describes a card-collection system organized around completing sets for rewards. The player must collect a large set of cards, and the near-complete set is made harder to finish because card packs stop providing new cards. The collection also has an expiration deadline, so failing to complete it before the deadline causes the player to miss the completion reward. The review does not describe payment, purchases, or a monetary stake.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion"
  - why: The player is pursuing completion of a card collection, with the missing completion reward tied to obtaining the full set.
- `P_RewardMania` - **SPURIOUS**
  - span: "include new cards in every card pack because I noticed when one is almost close to completing a set, new cards don't appear again"
  - why: The card-pack reward system is described as failing to deliver new cards near completion, implying repeated pack rewards that do not advance the collection.
- `T_PlayingByAppointment` - ok
  - span: "especially when the set is almost expiring"
  - why: The card collection operates within a game-defined expiration window, and missing that deadline causes the completion opportunity to be lost.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `S_Competition` | 2 | 1 |
| `M_PayToProgress` | 1 | 2 |
| `S_Reciprocity` | 2 | 0 |
| `S_FriendSpamImpersonation` | 1 | 1 |
| `P_RewardMania` | 1 | 1 |
| `P_AestheticManipulation` | 2 | 0 |
| `M_IntermediateCurrency` | 2 | 0 |
| `M_WasteAversion` | 1 | 0 |
| `M_EasyToPurchase` | 1 | 0 |
| `T_MandatoryMarathon` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `T_Grinding` | 0 | 1 |
| `M_Gambling` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |

