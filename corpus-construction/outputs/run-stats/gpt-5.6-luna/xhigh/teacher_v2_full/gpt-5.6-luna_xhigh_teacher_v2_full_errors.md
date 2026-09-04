# Error review - gpt-5.6-luna_xhigh_teacher_v2_full

`gpt-5.6-luna` / reasoning `xhigh` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `aad355174ac4`  
micro-F1 **0.851** (P 0.841 / R 0.860) - **16 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 3 | said NONE, gold had labels |
| SWAP | 5 | picked different labels than gold |
| MISSED ONLY | 2 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 6 | found all gold, added extras |

## The diagnostic that matters

Of **12** missed labels, **2** (17%) were named in the model's own analysis and dropped anyway; **10** (83%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `P_AestheticManipulation` | 0 | 2 |
| `P_RewardMania` | 1 | 0 |
| `T_PlayingByAppointment` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `S_Reciprocity` | 0 | 1 |
| `M_WasteAversion` | 1 | 0 |
| `M_EasyToPurchase` | 0 | 1 |
| `M_Gambling` | 0 | 1 |
| `M_PayToProgress` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `S_Competition` | 0 | 1 |

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
The review is a list of requested changes rather than descriptions of dark-pattern mechanics currently operating in the game. The reviewer proposes auctions using in-game currency, removal of an option related to decorated obstacles, an account-switching widget showing upgrade timers, and access to hidden troop statistics. These suggestions do not establish any applicable coded mechanic under R12. The mention of an existing option to remove a decorated obstacle does not match any available label.
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
The reviewer describes being unable to use Clash of Clans' clan troop-request feature after an update. The problem is presented as a malfunction that needs fixing, not as a deliberate social design that pressures players to exchange resources or continue playing. Because the only described behavior is attributed to an update-related technical fault, no dark-pattern label applies under R2 and R11.
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
The review praises the game's addictiveness and upgrades but does not describe a current dark-pattern mechanic. Trading stickers with other players is explicitly requested as a missing feature, so it cannot be labeled under R12. The statement about purchasing a booster and using it when challenged is also framed as a desired rule rather than a clearly described current payment, progression, or advantage mechanic. The Facebook reference only explains why the reviewer wants in-app trading; it does not describe messaging, social login, or contact access.
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
The review describes failed Pokémon captures consuming Poké Balls quickly enough that the player says they must purchase more to continue capturing, which supports Pay to Progress. It also alleges that capture outcomes became unusually unfavorable after purchasing balls and that this depletion serves to drive further purchases; this is a claimed manipulation of outcome determination rather than a mere statement of bad luck, supporting Illusion of Control. The edit denies authorship of the review and the claimed conversations with other players, implying that a store review was posted under the player's identity, which supports Friend Spam / Impersonation. No external search was needed because Poké Balls and the capture mechanic are identifiable from the review and game name.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "so I go through the balls faster so I have to purchase more"
  - why: Failed captures consume the usable Poké Balls, and the reviewer says continued capturing requires buying more.
- `P_IllusionOfControl` - ok
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: The reviewer attributes repeated capture failures to a purchase-linked outcome pattern that drains balls and drives further purchases, implying manipulated capture odds.
- `S_FriendSpamImpersonation` - ok
  - span: "I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE"
  - why: The edit denies authorship of a store review and the social claims it contains, implying that the review was posted under the player's identity.

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
The review describes an intentional interface behavior: when the game opens or the player enters 1v1, the UI automatically chooses the highest-stakes table rather than a neutral or lowest-stakes option. This directs the player toward a costly in-game choice and can cause accidental loss of coins. The reviewer further states that losing those coins forces them to buy more with real money, describing both a real-money-to-virtual-currency conversion and a payment barrier to continued play. The 1v1 reference also identifies player-versus-player competition. No web search was needed because all relevant mechanics are clear from the review.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: The review describes in-game coins being depleted and replaced by purchasing more coins with real money.
- `M_PayToProgress` - **SPURIOUS**
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: The wording that players are 'forced to buy' after losing their coins implies that spending money is required to continue playing.
- `M_UIMisdirection` - ok
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins"
  - why: The UI automatically steers the player to the highest-bet table, creating a misleading default that can cause accidental selection.
- `S_Competition` - **SPURIOUS**
  - span: "1v1 section"
  - why: A 1v1 section is an explicit player-versus-player competitive mode.

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
The review describes a daily-reward system that cannot be completed unless the player places a 50,000-unit bet, so the daily reward is an active recurring incentive with a completion condition. In the context of a casino slots game, the phrase "bet 50,000" also describes wagering in a chance-based mechanic using in-game currency. The 40,000 timed-reward amount is a shortfall relative to the required bet, but it is not an item price or a demonstrated leftover purchase balance, so Waste Aversion does not apply. There is no described real-money purchase, progression gate, or wait timer.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "unless I bet 50,000"
  - why: The player must wager 50,000 in-game units, implying participation in a chance-based betting mechanic.
- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The game offers daily rewards but requires the player to complete a recurring daily condition to obtain them.

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
The reviewer describes repeatedly playing bingo rounds to obtain collectible photos and finish a set. The repeated rounds are a progress-related, tedious activity, supporting Grinding. The explicit goal of obtaining photos to complete a set supports Complete the Collection. The game also presents spending extra coins as a route to obtain a missing photo and advance that collection, supporting Pay to Progress; the later statement about wasted money confirms the player experienced this as monetary expenditure. The failure to receive the promised photo does not by itself establish Gambling, Reward Mania, Intermediate Currency, or a technical-fault label, and there is no explicit time-gated schedule or UI-friction mechanism.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "spend extra coins to claim a photo I don't have to complete the set"
  - why: The game presents spending currency as the route to obtain a missing photo and move toward completing the set.
- `P_CompleteTheCollection` - ok
  - span: "a photo I don't have to complete the set"
  - why: The reviewer is pursuing a missing collectible specifically so the set can be completed.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The reviewer repeatedly plays bingo rounds as the activity required to advance the photo collection.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b93c432d-19c0-4c6c-a2d4-bb9b21a436f3` - Dice Dreams™️

> A literal brain-rot game no wonder why they're tryna promote it through Free Cash. Also if you're thinking of making in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates! A real SCAM. Play it if u want but there are games that are actually good also, DON'T GET IN-APP PURCHASES!

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_PayToProgress`, `P_CompleteTheCollection`, `P_RewardMania` |
| **missed** | `P_AestheticManipulation` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The promotion through Free Cash is out-of-game marketing and is excluded under R13; the warnings, tone, and accusation of a scam are not mechanics by themselves. The review describes an album made up of cards, with two missing cards standing between the player and a grand prize, which supports a collection-completion mechanic. It also describes buying an in-app deal specifically to obtain those missing cards, linking payment to advancement toward the album reward. The deal's card rewards produced duplicates instead of the promised new cards, describing an unwanted or variable reward-delivery mechanic. The review does not explicitly establish a wager or chance-based draw, so Gambling is not assigned.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "so i bought a deal which promised i would get NEW cards"
  - why: The reviewer paid for a deal intended to obtain cards needed to advance toward completing the album and claiming its grand prize.
- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The game motivates the player to acquire the remaining cards in an album to complete the collection and receive its reward.
- `P_RewardMania` - ok
  - span: "which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: The purchased card reward delivered unwanted duplicate items instead of the needed new cards, showing variable reward delivery.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (2)

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
The review describes success as financially gated: winning anything is said to require hundreds of dollars, and obtaining the final one or two stickers requires paying a large amount. The stickers are therefore part of a collection the player is expected to complete, while the apparent scarcity of the final items is tied directly to purchase. The statement that a goal may be completed only one time in a hundred expresses low success odds, but it does not identify a chance-based reward mechanic or allege rigging, so it does not independently support Gambling, Reward Mania, or Illusion of Control. The forced five-star review condition is not covered by any listed label.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them."
  - why: The final stickers are presented as deliberately scarce and obtainable only through a costly payment.
- `M_PayToProgress` - ok
  - span: "if you want to win anything on this game it will cost hundreds of dollars."
  - why: The review states that winning anything is contingent on spending hundreds of dollars.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two"
  - why: The span describes pursuing the final missing stickers needed to complete the collection.

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
The reviewer describes a sticker-collection system organized into sets. Repeated duplicate stickers indicate an unwanted or unpredictable reward-delivery pattern, which supports Reward Mania. The goal of finishing all sets is an explicit collection-completion objective, supporting Complete the Collection. The reviewer also says the game does not allow completion unless the player pays, making payment a condition for progress and supporting Pay to Progress. The review does not state that payment buys chances or wagers, so Gambling is not assigned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: Completion of the sticker sets is described as unavailable unless the player pays.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: The reviewer identifies completing all sticker sets as the collection goal.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: Repeated duplicate stickers describe an unwanted reward-delivery outcome that sustains effort toward completing the sets.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (6)

### `95ddadb3-82cd-4042-8a51-cf8b3ed164c2` - Mech Arena - Shooting Game

> You stuck waiting 30 seconds just to connect to a match. This game makes it seem like they give so many rewards but if all just for show. Its difficult to get weapon upgrades or any percs others you stick battling to win. This kind of games just rob you of your time in my opinion

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `S_Competition`, `T_Grinding` |
| **spurious** | `S_Competition`, `T_Grinding` |

**Model analysis**

```
The review describes a 30-second matchmaking delay, but this is a connection or queueing delay rather than an in-game timer that forces the player to follow a schedule, so it does not support Playing by Appointment. The statement that rewards are 'just for show' criticizes their apparent value or presentation, but it does not describe a complex, random, or otherwise manipulative reward-delivery system. The clearest design behavior is that obtaining weapon upgrades or perks requires continuing to battle and win, which describes repeated combat for progress and also places the player in competitive matches.
```

**Labels assigned**

- `S_Competition` - **SPURIOUS**
  - span: "stick battling to win"
  - why: Battling to win describes competitive gameplay against an opposing side.
- `T_Grinding` - **SPURIOUS**
  - span: "Its difficult to get weapon upgrades or any percs others you stick battling to win"
  - why: The reviewer implies that players must keep battling and winning to obtain weapon upgrades or perks.

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
The review describes a session-break consequence: the player leaves while holding a full bag, returns to find the bag emptied, and also loses coins that were both earned and purchased. This makes stopping costly because accumulated holdings are forfeited, and it implies the game does not preserve those holdings across leaving and returning. The phrase about purchased coins also identifies real-money acquisition of an in-game currency. There is no price mismatch, purchase prompt, advertising, daily schedule, or bug attribution described.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "coins that I earned and purchased"
  - why: The review explicitly describes coins obtained both through play and by purchasing them.
- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used"
  - why: The player's accumulated inventory and coins make leaving costly because those holdings are gone on return.
- `T_MandatoryMarathon` - ok
  - span: "I leave the game with my bag full only to come back with it empty"
  - why: Leaving the game causes accumulated inventory to be lost before the player returns.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a2ece36d-c527-442d-8f18-9a16b63994c8` - War Robots Multiplayer Battles

> Its a p2w game. The only time you enjoy it is when you're new. As you progress, everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game. If you want to progress without paying money, goodluck! Even if you wanted to do f2p, you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it. Plus the only time you benofit by getting f2p rewards is ads... 💩

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `M_PayToProgress`, `M_PowerCreep`, `T_Advertisement` |
| pred | `M_EasyToPurchase`, `M_PayToProgress`, `M_PowerCreep`, `M_UIMisdirection`, `S_FearOfMissingOutFOMO`, `T_Advertisement` |
| **spurious** | `M_UIMisdirection`, `S_FearOfMissingOutFOMO` |

**Model analysis**

```
The review describes several current in-game mechanics. Login is interrupted by purchase offers that appear before play, so the offers directly intercept gameplay and the purchase screen obstructs access. Progress and competitive viability are tied to buying the newest bot with money rather than earning it, which is pay-to-progress/pay-to-win. The reference to a shifting meta and needing the newest bot also implies power creep, where newer releases reduce the value of older bots and drive further purchases. The statement about not keeping up describes pressure to avoid falling behind. Finally, free-to-play rewards are linked to ads, implying incentivized ad viewing. No virtual-currency conversion, chance mechanic, daily reward, social mechanic, or repetitive task is explicitly described. I did not search because the mechanics and terms are identifiable from the review itself.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game"
  - why: The in-app purchase offers appear as an obstruction immediately before play, reducing the friction of being prompted to buy at the point of access.
- `M_PayToProgress` - ok
  - span: "where you have to buy the newest bot with money instead of earning it"
  - why: The reviewer says money must be spent on the newest bot instead of earning it in order to remain viable.
- `M_PowerCreep` - ok
  - span: "keep up with shifting meta where you have to buy the newest bot with money instead of earning it"
  - why: The shifting meta and need for the newest bot imply that older bots lose competitive value as new bots are introduced.
- `M_UIMisdirection` - **SPURIOUS**
  - span: "your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game"
  - why: The purchase-filled screen blocks access to the game until the player handles that interface.
- `S_FearOfMissingOutFOMO` - **SPURIOUS**
  - span: "you would not be able to keep up with shifting meta"
  - why: Non-paying players are described as being left behind by ongoing meta changes, creating pressure to stay current through payment.
- `T_Advertisement` - ok
  - span: "the only time you benofit by getting f2p rewards is ads"
  - why: The review links free-to-play rewards to ads, implying that ad viewing is the rewarded route.

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
The review describes a time-limited card collection with sets, card packs, and rewards for completing sets. The reviewer reports that card packs stop yielding new cards when a set is nearly complete, implying repeated or unwanted card drops from a variable reward pool; the Royal Match sources confirm that packs can produce duplicate cards and use a dynamic card-pool probability system. ([dreamgames.helpshift.com](https://dreamgames.helpshift.com/hc/en/3-royal-match/section/55-collection/?utm_source=openai)) The reviewer is also pursuing completion of the collection and may lose the completion reward when the collection deadline arrives, which imposes a game-controlled schedule. The request to add new cards is not itself coded, but the currently described lack of new cards and expiring collection are.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion"
  - why: The reviewer is collecting cards toward completing a set and receiving its completion reward.
- `P_RewardMania` - **SPURIOUS**
  - span: "include new cards in every card pack because I noticed when one is almost close to completing a set, new cards don't appear again especially when the set is almost expiring"
  - why: The card-pack system is described as failing to provide missing cards near completion, implying variable or duplicate-prone reward delivery.
- `T_PlayingByAppointment` - ok
  - span: "you will miss the reward for the set completion because they don't add new sets to the cards once the collection is about to end"
  - why: The collection's game-controlled end date causes the player to lose the completion reward if the set is not finished in time.

**Search:** `Royal Match card packs card collection sets reward expiration` -> Official Royal Match sources establish that the Collection is time-limited, card packs provide collection cards, duplicate cards can occur, and card-pack contents use a dynamic probability/card-pool system. ([dreamgames.helpshift.com](https://dreamgames.helpshift.com/hc/en/3-royal-match/section/55-collection/?utm_source=openai))

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
The review complains that a seven-hour quest yields very few primogems, but this describes reward quantity rather than an unpredictable or complex reward-delivery system, so it does not establish Reward Mania. “Exploration is debilitating,” the character-design criticism, and the five-year play history are evaluations or background rather than coded mechanics; the quest is not described as repetitive or impossible to stop. The actionable mechanic is the lack of a resin overflow system. The permitted search resolves this as Genshin’s time-regenerating Original Resin being subject to a cap, with excess regeneration able to be wasted, which makes play or return timing follow the game’s schedule. Therefore I assign Playing by Appointment only.
```

**Labels assigned**

- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "there is no resin overflow system."
  - why: The absence of overflow implies capped, time-based resin regeneration, pressuring the player to return or spend resin before timer-generated resource is wasted.

**Search:** `Genshin Impact "resin overflow system"` -> The search established that Original Resin replenishes over time and that an overflow feature would preserve excess above the cap; without overflow, capped regeneration can be wasted. ([gamewith.net](https://gamewith.net/genshin-impact/article/show/22375?utm_source=openai))

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `7b564746-b769-4856-b686-529f8717c3ba` - Candy Crush Soda Saga

> I like the game except: 1. I was charged 10 gold pcs for 5 moves, I had 2 moves left. I had 7 moves but only used 1 move. 2. I paid for a pkg unlimited lives ect. I got the etc. but not the lives. 3. The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone. 4. You cannot win enough gold to play without buying sometimes. 5. The packages need to cost less. 6. When I buy pkg should not be timed.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `M_PayToProgress`, `T_PlayingByAppointment` |
| pred | `M_IntermediateCurrency`, `M_PayToProgress`, `P_EasyToGetHardToLose`, `T_PlayingByAppointment` |
| **spurious** | `P_EasyToGetHardToLose` |

**Model analysis**

```
The review describes several active mechanics rather than only complaints about price. Gold is spent for extra moves, and the player says they cannot earn enough gold to keep playing without buying, which makes payment a route to continued play and implies that gold is a purchasable intermediate currency. The paid unlimited-lives package is described as failing to deliver the lives; that is a failed purchase outcome rather than a deliberate mechanic, so it is not separately coded. The strongest temporal mechanic is that timed bonuses continue expiring while the player is asleep, meaning the game clock determines their availability even when the player is not playing. Because bonuses already held are lost by stopping, this also makes disengagement costly. The requests for cheaper packages do not independently identify a dark-pattern mechanic.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The sentence implies that gold is an in-game currency that can also be acquired through real-money purchases.
- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The free route does not provide enough gold to continue playing, so buying becomes necessary for continued access.
- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "I go to bed with bonuses to wake up with them almost gone or gone."
  - why: Stopping for the night causes already-held bonuses to disappear, making disengagement costly.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone."
  - why: The game imposes a real-time expiration schedule on bonuses, forcing their availability to be governed by the game's clock rather than the player's play session.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_PayToProgress` | 1 | 4 |
| `S_Competition` | 1 | 2 |
| `T_PlayingByAppointment` | 1 | 1 |
| `P_EasyToGetHardToLose` | 0 | 2 |
| `P_AestheticManipulation` | 2 | 0 |
| `M_Gambling` | 1 | 1 |
| `P_RewardMania` | 1 | 1 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `M_UIMisdirection` | 0 | 1 |
| `S_Reciprocity` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `T_Grinding` | 0 | 1 |
| `M_WasteAversion` | 1 | 0 |
| `M_EasyToPurchase` | 1 | 0 |
| `S_FearOfMissingOutFOMO` | 0 | 1 |

