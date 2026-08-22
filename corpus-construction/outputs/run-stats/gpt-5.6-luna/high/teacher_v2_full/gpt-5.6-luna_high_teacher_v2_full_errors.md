# Error review - gpt-5.6-luna_high_teacher_v2_full

`gpt-5.6-luna` / reasoning `high` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `6529a474a2b0`  
micro-F1 **0.845** (P 0.866 / R 0.826) - **17 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 2 | said NONE, gold had labels |
| SWAP | 5 | picked different labels than gold |
| MISSED ONLY | 6 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 4 | found all gold, added extras |

## The diagnostic that matters

Of **15** missed labels, **3** (20%) were named in the model's own analysis and dropped anyway; **12** (80%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `S_Reciprocity` | 1 | 1 |
| `P_AestheticManipulation` | 0 | 2 |
| `M_PayToProgress` | 1 | 1 |
| `M_Gambling` | 0 | 1 |
| `M_WasteAversion` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `S_Competition` | 0 | 1 |
| `P_RewardMania` | 1 | 0 |
| `T_PlayingByAppointment` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `M_IntermediateCurrency` | 0 | 1 |
| `M_EasyToPurchase` | 0 | 1 |

## Missed everything (predicted NONE) (2)

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
The review mainly proposes feature changes rather than describing dark-pattern mechanics currently operating in the game. It asks for auctions using in-game currency, a change to the existing obstacle-decoration removal option, an account-switching widget showing upgrade timers, and access to advanced troop statistics. These requests do not establish any listed pattern such as payment gating, waiting imposed by timers, currency conversion, or UI manipulation. The positive rating and requests themselves do not trigger labels.
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
The review describes an inability to request troops from the clan after an update and explicitly attributes it to something that needs to be fixed, so this is a reported malfunction rather than a deliberate social resource-sharing mechanic. Under R11, the bug attribution suppresses labels, including Reciprocity.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (5)

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
The reviewer describes a paid consumable-item loop: after purchasing Poké Balls, captures allegedly fail more often, causing the balls to be depleted faster and requiring additional purchases. This is presented as outcome manipulation intended to create a payment-dependent path to continued capturing, supporting Illusion of Control and Pay to Progress. The edit separately claims that the original review and its statement about consulting other players were not written by the account holder, which describes the game posting a review under the player's identity and supports Friend Spam / Impersonation under the destination-of-message rule. No web search is needed because the mechanics are identifiable from the review.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "so I go through the balls faster so I have to purchase more"
  - why: The consumable Poké Balls are needed for capturing, and the reviewer says continued play requires purchasing additional balls.
- `P_IllusionOfControl` - ok
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out"
  - why: The reviewer attributes repeated capture failures to a change associated with purchasing, implying that the game manipulates outcome determination to make the player use more balls.
- `S_FriendSpamImpersonation` - ok
  - span: "I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE"
  - why: The reviewer alleges that the installed game posted a store review under their account and fabricated statements in their identity.

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
The review describes a deliberate interface behavior in which opening the game or entering the 1v1 area automatically moves the player to the highest-stakes table affordable with their coins and selects it. This directs the player toward a costly option and is said to cause accidental mis-clicks. The resulting loss of all accumulated coins creates pressure to purchase more currency with real money, so the review also describes both payment being used to continue playing and real money being converted into in-game coins. The mention of a 1v1 section explicitly describes competition against another player. The requested Default Table Lock and lowest-table default are hypothetical fixes and are not coded.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "forced to buy real ones"
  - why: The span describes purchasing replacement in-game coins with real money.
- `M_PayToProgress` - **SPURIOUS**
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: The review says players are forced to pay for replacement currency after losing their coins, making payment the route to continued play.
- `M_UIMisdirection` - ok
  - span: "Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins"
  - why: The interface automatically scrolls to and selects the highest-bet option, directing attention and interaction toward a costly choice.
- `S_Competition` - **SPURIOUS**
  - span: "go to the 1v1 section"
  - why: A 1v1 section describes a mode in which the player competes directly against another player.

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
The review describes a daily-reward system that requires the player to complete a wagering threshold: the daily rewards cannot be collected unless the player bets 50,000. This supports Daily Rewards because the game incentivizes activity within a daily cycle and withholds the daily reward when the condition is not met. The required bet is also a chance-based casino action, so Gambling applies even though the review does not say that the wager itself uses real money; the codebook permits Gambling when an in-game currency stake is wagered and no purchase is described. The mention of timed rewards only gives their amount and does not establish a separate reward-delivery manipulation.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "unless I bet 50,000"
  - why: The player must stake 50,000 in a chance-based casino-style wager to qualify for the reward.
- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The daily reward system imposes a daily wagering requirement, so failing to meet it prevents completion and collection of the daily rewards.

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
The review describes a collection goal involving photos and a repetitive loop of playing bingo rounds to obtain them. The repeated rounds are the activity required to make collection progress, which supports Grinding, and the stated aim of completing a photo set supports Complete the Collection. The game also presents spending extra coins as a way to obtain a missing photo and advance the set, so this is a paid progress route. The failure to receive the promised photo is described as an outcome of the offer, not explicitly as a bug or technical fault. The review does not establish that real money is converted into coins, so Intermediate Currency is not assigned; it also does not describe a chance-based paid stake, a timer, or a specific leftover-currency shortfall.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "spend extra coins to claim a photo I don't have to complete the set"
  - why: Spending currency is presented as the route to obtaining a missing collection item and advancing toward set completion.
- `P_CompleteTheCollection` - ok
  - span: "collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set"
  - why: The game encourages acquiring missing photos to complete a collection set.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The reviewer describes repeating bingo rounds in order to make collection progress.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b93c432d-19c0-4c6c-a2d4-bb9b21a436f3` - Dice Dreams™️

> A literal brain-rot game no wonder why they're tryna promote it through Free Cash. Also if you're thinking of making in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates! A real SCAM. Play it if u want but there are games that are actually good also, DON'T GET IN-APP PURCHASES!

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_Gambling`, `M_PayToProgress`, `P_CompleteTheCollection`, `P_RewardMania` |
| **missed** | `P_AestheticManipulation` |
| **spurious** | `M_Gambling`, `M_PayToProgress` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes an in-app purchase made to obtain the last two cards needed to complete an album and receive its grand prize. The purchased deal was expected to provide new cards but delivered duplicates, which describes a paid, chance-variable card-reward mechanic and an unwanted duplicate outcome. The album completion itself supports Complete the Collection. The mention of promotion through Free Cash is third-party marketing and is excluded under R13; the negative evaluations and warnings alone do not receive labels. The search established that Dice Dreams uses sticker/card albums, that card packs use odds, and that packs marked “new” can still result in duplicates under the game’s stated type rules. ([support.dicedreams.com](https://support.dicedreams.com/hc/en-us/articles/24098716134163-I-was-assured-a-Guaranteed-NEW-Sticker-but-I-received-a-duplicate-Why))
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "bought a deal which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: An in-app purchase was used for a card reward whose delivered contents differed from the expected new card, indicating paid participation in a luck-based reward mechanic.
- `M_PayToProgress` - **SPURIOUS**
  - span: "in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal"
  - why: The reviewer paid for a deal specifically to obtain the remaining cards needed to complete an album and advance to its grand prize.
- `P_CompleteTheCollection` - ok
  - span: "two cards left which would grant me the grand prize for completing an album"
  - why: The reviewer is compelled to acquire the final missing cards in an album collection to obtain its completion prize.
- `P_RewardMania` - ok
  - span: "which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: The reward system delivers card contents unpredictably, with an unwanted duplicate outcome instead of the expected new card.

**Search:** `Dice Dreams album cards deal new cards duplicates` -> Dice Dreams' official help center identifies album sticker/card packs, documents odds-based pack contents, and explains that a Guaranteed NEW card can still be a duplicate when the relevant card type is already complete. ([support.dicedreams.com](https://support.dicedreams.com/hc/en-us/articles/24098716134163-I-was-assured-a-Guaranteed-NEW-Sticker-but-I-received-a-duplicate-Why))

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (6)

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
The review primarily attributes the described problems to bugs, crashing, lag, unresponsive controls, and freezing after an update. Under R11, those technical faults do not themselves receive dark-pattern labels. The review also explicitly identifies PvP battles, which are competitive gameplay between players; this underlying mechanic remains codable even though the reviewer says it is malfunctioning. Trading and gifts with friends are mentioned, but no obligation to reciprocate or social pressure is described.
```

**Labels assigned**

- `S_Competition` - ok
  - span: "the pvp & rockets battles"
  - why: The span explicitly describes PvP battles, a game mode in which players compete against one another; the accompanying lag is a technical fault and does not erase the underlying competition mechanic.

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
The review describes a perceived outcome-manipulation mechanic: the random number generation is said to work against the player, which implies that results are not fairly random. It also describes an unfavorable progression economy at about level 100, where entering a level costs 2200 and winning returns barely that amount, but it does not clearly state that payment is required to advance, that real money buys the 2200 currency, or that the level is a wager for a prize. The complaint that play without spending is not rewarding is evaluative and does not independently establish Pay to Progress, Gambling, Intermediate Currency, or Reward Mania. No web search is needed.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "the rng is so obviously against you"
  - why: The reviewer claims the RNG is deliberately unfavorable, describing concealed or manipulated outcome determination.

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

- `S_Competition` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes an event whose outcome is effectively gated by spending: it calls the game pay to play and pay to win, then says 30k was spent to win the last event. This supports Pay to Progress because money is used to access or win event content. The phrase "same old same old grinder" is only a general evaluation of repetition and does not name a repeated task required for progress, so it does not support Grinding. No clear chance mechanic, currency conversion, daily schedule, collection pressure, or sunk-cost pressure is described.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Zero skill pay to play. Zero skill pay to win. Calculated total spent on last event was 30k to win."
  - why: The review states that playing or winning the event requires substantial spending, including 30k spent to win.

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
The review describes monetized success and collection completion. It says that winning anything requires spending hundreds of dollars, which directly describes payment as the route to advantage or success. It also describes sticker sets whose final one or two items are effectively unavailable unless the player pays substantially, implying both a collection-completion pressure and developer-imposed scarcity tied to purchase. The statement that a goal succeeds only about one time in one hundred expresses poor odds, but it does not identify a chance-based reward system or a wager, so it is insufficient for Gambling or Reward Mania. The review-gating complaint concerns submitting a store review and does not match any listed in-game mechanic.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "you will never get the last one or two unless you pay a lot of money to get them"
  - why: The final stickers are described as deliberately scarce or unavailable through ordinary play, with payment presented as the way to obtain them.
- `M_PayToProgress` - ok
  - span: "if you want to win anything on this game it will cost hundreds of dollars"
  - why: The reviewer says real-money spending is required to win or succeed in the game.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two"
  - why: The reference to obtaining the last stickers describes pressure to complete a sticker collection.

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
The reviewer describes a sticker-collection system in which sticker acquisition repeatedly produces duplicates, making completion difficult. The goal is to finish all sticker sets, which supports Complete the Collection. The statement that the sets cannot be finished unless the player pays describes payment-gated progress. The duplicate outcome may reflect an unpredictable or repeated reward-delivery system, supporting Reward Mania, but there is no explicit monetary wager, currency conversion, limited-time scarcity, or social mechanic.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: Completion of the sets is described as unavailable unless the player makes a payment.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: The reviewer identifies completing all sets as the collection goal.
- `P_RewardMania` - ok
  - span: "getting stickers. always get duplicates"
  - why: Sticker acquisition repeatedly delivers unwanted duplicate outcomes, describing a reward-delivery structure that sustains attempts to obtain missing items.

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
The review describes a timer-based reward mechanic: timed bonuses continue expiring while the player is offline, so the player must return according to the game's clock to avoid losing them. It also describes progression being financially constrained because the player cannot earn enough gold through play and sometimes must buy something to continue playing. The paid package not delivering its promised lives is a purchase-fulfillment failure, not a deliberate dark-pattern mechanic, and the complaints about package price and timing do not independently establish a recurring fee or another label. The gold charge for extra moves does not by itself show real-money conversion or an accidental-purchase interface.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The player states that earning gold through play is sometimes insufficient and buying is needed to continue playing.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone."
  - why: Bonuses expire during offline time, forcing the player to play according to a schedule set by the game.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (4)

### `95ddadb3-82cd-4042-8a51-cf8b3ed164c2` - Mech Arena - Shooting Game

> You stuck waiting 30 seconds just to connect to a match. This game makes it seem like they give so many rewards but if all just for show. Its difficult to get weapon upgrades or any percs others you stick battling to win. This kind of games just rob you of your time in my opinion

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `T_Grinding` |
| **spurious** | `T_Grinding` |

**Model analysis**

```
The review describes a 30-second matchmaking connection wait, but the codebook excludes service-operation waits such as matchmaking queues from Playing by Appointment. It also describes weapon upgrades and perks as difficult to obtain, with the player having to keep battling to win; this implies repeated gameplay activity is required for advancement, supporting Grinding. The complaint that rewards are merely 'for show' is too vague to identify a specific reward-delivery mechanic, and no payment, purchase, or explicit opponent relationship is described.
```

**Labels assigned**

- `T_Grinding` - **SPURIOUS**
  - span: "Its difficult to get weapon upgrades or any percs others you stick battling to win."
  - why: The span implies that the player must keep battling repeatedly to obtain upgrades or perks and achieve wins.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `176aaa1f-d8f9-4a1a-9f29-64902f13be5c` - All in Hole: Black Hole Games

> I would give 5 stars, but I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used.🤨😒🙄😥

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `T_MandatoryMarathon` |
| pred | `M_IntermediateCurrency`, `P_EasyToGetHardToLose`, `T_MandatoryMarathon` |
| **spurious** | `P_EasyToGetHardToLose` |

**Model analysis**

```
The review describes accumulated in-game holdings being lost when the player exits and returns: a full bag becomes empty, and coins previously earned or purchased have been consumed. The exit-related forfeiture supports both Mandatory Marathon, because stopping the session results in loss of held value, and Easy to Get, Hard to Lose, because accumulated resources make leaving costly. The phrase about purchased coins also describes real money being converted into an in-game currency, supporting Intermediate Currency. No label is assigned for Waste Aversion because the review does not describe a price mismatch, leftover currency shortfall, or inventory-capacity purchase decision.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "coins that I earned and purchased"
  - why: The reviewer explicitly identifies coins as a currency that can be purchased, establishing a real-money-to-virtual-currency conversion.
- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "my bag full only to come back with it empty and coins that I earned and purchased used"
  - why: Resources accumulated or purchased by the player are lost or consumed after leaving, making disengagement costly.
- `T_MandatoryMarathon` - ok
  - span: "I leave the game with my bag full only to come back with it empty"
  - why: Leaving the game results in the player returning with previously held bag contents gone, showing a cost attached to ending the session.

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
The review describes repeated in-game purchase offers that appear before gameplay, directly interrupting access to the game. Progress is presented as dependent on paying, especially because the player cannot keep up with a shifting competitive meta without buying the newest bot rather than earning it. The reference to a shifting meta and needing the newest bot implies that newer releases diminish the usefulness of older bots, driving further purchases. The review also describes falling behind the meta without paying, creating pressure not to miss the current competitive state. Finally, ads appear to be the route for obtaining free-to-play rewards, which indicates incentivized advertisement viewing.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game"
  - why: Purchase offers appear before gameplay and directly intercept the player’s ability to start playing.
- `M_PayToProgress` - ok
  - span: "where you have to buy the newest bot with money instead of earning it"
  - why: The review states that obtaining the bot needed to keep progressing or keeping up requires payment rather than ordinary earning.
- `M_PowerCreep` - ok
  - span: "keep up with shifting meta where you have to buy the newest bot"
  - why: A shifting meta requiring the newest bot implies that newer releases reduce the practical value of older bots and drive purchases of replacements.
- `S_FearOfMissingOutFOMO` - **SPURIOUS**
  - span: "would not be able to keep up with shifting meta"
  - why: The player describes pressure from falling behind the current meta when not paying.
- `T_Advertisement` - ok
  - span: "the only time you benofit by getting f2p rewards is ads"
  - why: The span implies that free-to-play rewards are obtained through engaging with advertisements, indicating rewarded ad viewing.

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
The review describes a card-collection system with set-completion rewards. Card packs stop yielding new cards when a set is nearly complete, implying repeated or unwanted card drops from a variable reward pool and making completion difficult. The collection also has an expiry deadline, so failing to complete the set before it ends causes the player to lose the completion reward. No real-money purchase or payment-based mechanic is explicitly described.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "almost close to completing a set"
  - why: The review describes the player pursuing completion of a card set to obtain its completion reward.
- `P_RewardMania` - **SPURIOUS**
  - span: "include new cards in every card pack because I noticed when one is almost close to completing a set, new cards don't appear again"
  - why: Card packs are described as repeatedly failing to deliver needed new cards near completion, indicating a reward-delivery mechanic that sustains repeated attempts.
- `T_PlayingByAppointment` - ok
  - span: "especially when the set is almost expiring. So after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion"
  - why: The collection has a game-defined expiry window, and failing to finish before it causes the completion reward to be forfeited.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_PayToProgress` | 2 | 4 |
| `M_Gambling` | 1 | 2 |
| `S_Reciprocity` | 2 | 0 |
| `S_Competition` | 1 | 1 |
| `P_RewardMania` | 1 | 1 |
| `P_AestheticManipulation` | 2 | 0 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `M_EasyToPurchase` | 1 | 0 |
| `S_FearOfMissingOutFOMO` | 0 | 1 |
| `T_Grinding` | 0 | 1 |
| `M_WasteAversion` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `M_IntermediateCurrency` | 1 | 0 |

