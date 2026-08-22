# Error review - gpt-5.6-luna_high_teacher_v2_boundary

`gpt-5.6-luna` / reasoning `high` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_boundary.txt` sha `013bb31c5857`  
micro-F1 **0.818** (P 0.890 / R 0.756) - **16 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 4 | said NONE, gold had labels |
| SWAP | 4 | picked different labels than gold |
| MISSED ONLY | 7 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 1 | found all gold, added extras |

## The diagnostic that matters

Of **21** missed labels, **8** (38%) were named in the model's own analysis and dropped anyway; **13** (62%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `S_Reciprocity` | 2 | 0 |
| `S_Competition` | 2 | 0 |
| `P_RewardMania` | 1 | 1 |
| `P_AestheticManipulation` | 0 | 2 |
| `M_PayToProgress` | 1 | 1 |
| `M_IntermediateCurrency` | 0 | 2 |
| `M_PowerCreep` | 1 | 0 |
| `S_FriendSpamImpersonation` | 0 | 1 |
| `M_Gambling` | 1 | 0 |
| `T_MandatoryMarathon` | 0 | 1 |
| `M_EasyToPurchase` | 0 | 1 |
| `M_WasteAversion` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |

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
The review gives a positive rating and lists requested changes rather than describing current game mechanics. The proposed auction system, removal restriction for decorated obstacles, account-switching widget with upgrade timers, and troop-statistics option are hypothetical additions or changes. Under R12, these requested features do not trigger labels. No existing dark-pattern mechanic is explicitly described.
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
- `S_Reciprocity` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes technical malfunctions rather than deliberate game design. Crashing prevents opening gifts and trading with friends, lag prevents throwing Poké Balls, and freezing or unresponsive controls disrupt PvP and Rocket battles while the opponent continues attacking. The references to gifts, trading, and PvP do not establish Reciprocity, Forced Fellowship, or Competition as dark-pattern mechanics because the review only says these features are malfunctioning. Under R11, the bug, lag, and freeze attributions suppress labels for the affected behaviors.
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
The review describes a troop-request feature involving the player's clan, which would ordinarily be a resource-transfer mechanic, but the reviewer says they can no longer use it because of an update and explicitly asks for it to be fixed. Under R11, the described behavior is attributed to a technical fault, so it does not support Reciprocity or any other dark-pattern label.
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
The reviewer reports that items in the bag and coins, including purchased coins, disappear after leaving and returning to the game. This describes loss of game state or resources across sessions, but it does not explicitly describe a deliberate exit penalty, a saving restriction, an inventory-capacity rule, or a monetization mechanism. The account therefore does not satisfy a dark-pattern label; it is most consistent with an unspecified persistence or technical problem.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (4)

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
The review describes a deliberate interface default: opening the game or the 1v1 area automatically moves to and selects the highest-bet table available for the player's coins. This directs the player toward the most costly table and is said to cause accidental mis-clicks that spend their accumulated coins. After those coins are lost, the reviewer says players are forced to buy more coins with real money, making payment a route to continued play. The 1v1 reference also describes player-versus-player competition. The review does not establish chance-based gambling, leftover currency waste, or an accidental real-money purchase itself; the accidental loss is of in-game coins.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "are forced to buy real ones"
  - why: The pronoun 'ones' refers to the game's coins, so the span describes acquiring in-game currency through a real-money purchase.
- `M_PayToProgress` - **SPURIOUS**
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: The review states that losing the game's coins forces players to purchase more with real money in order to keep playing.
- `M_UIMisdirection` - ok
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins"
  - why: The interface automatically directs the player toward the highest-cost betting option rather than a neutral or low-cost default.
- `S_Competition` - **SPURIOUS**
  - span: "the 1v1 section"
  - why: A 1v1 mode explicitly pits players against one another in competition.

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

- `M_PayToProgress` - considered and rejected -> **rule interpretation**
- `M_WasteAversion` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes two mechanics. First, the game has a daily-reward system that the player cannot complete or collect unless a daily wagering requirement is met, so the daily reward opportunity is conditional rather than freely available. Second, in the casino-slots context, betting 50,000 describes wagering in a chance-based game using an in-game balance; the review does not describe real money being directly used to place the wager, so Intermediate Currency is not supported. The statement about paying appears to express refusal to obtain more currency, but it does not clearly say that payment is required for overall game progression, so Pay to Progress is not assigned.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "bet 50,000"
  - why: In this casino-slots game, betting 50,000 describes staking in-game currency in a chance-based wager.
- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The player describes a daily reward system that cannot be completed or collected unless the required daily activity is performed.

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
The review describes a repeated bingo-round loop undertaken to collect missing photos and complete a set, explicitly supporting both collection completion and grinding. It also describes a coin offer appearing after a lost round that lets the player pay to obtain a missing photo, making payment an alternative route to collection progress; the reviewer further frames these expenditures as wasted money. The failure to receive the promised photo is reported, but no deliberate scarcity rule, random reward mechanism, technical fault, or purchase-interface obstruction is clearly described, so those patterns are not coded.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "spend extra coins to claim a photo I don't have to complete the set"
  - why: The offer makes spending currency the route to obtaining a missing photo and advancing toward set completion.
- `P_CompleteTheCollection` - ok
  - span: "to complete the set"
  - why: The stated goal is to acquire missing photos until the set is complete.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The player repeatedly plays bingo rounds to obtain collection items.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b93c432d-19c0-4c6c-a2d4-bb9b21a436f3` - Dice Dreams™️

> A literal brain-rot game no wonder why they're tryna promote it through Free Cash. Also if you're thinking of making in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates! A real SCAM. Play it if u want but there are games that are actually good also, DON'T GET IN-APP PURCHASES!

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_PayToProgress`, `P_CompleteTheCollection`, `P_EasyToGetHardToLose` |
| **missed** | `P_AestheticManipulation`, `P_RewardMania` |
| **spurious** | `M_PayToProgress`, `P_EasyToGetHardToLose` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**
- `P_RewardMania` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes an album-collection mechanic in which the player was missing only two cards and would receive a grand prize for completing the album. That nearly completed collection functions as a partially completed goal that encouraged the player to continue and spend money. The purchased deal was intended to provide the missing cards, making payment a route toward in-game progress. Although the player received duplicates, the review does not clearly establish that the cards came from a randomised reward system, so Reward Mania and Gambling are not assigned. The mention of promotion through Free Cash concerns out-of-game advertising and is excluded by R13.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "so i bought a deal which promised i would get NEW cards"
  - why: The player spent money to obtain cards needed for album completion, using a purchase as a route toward in-game progress.
- `P_CompleteTheCollection` - ok
  - span: "two cards left which would grant me the grand prize for completing an album"
  - why: The player is pursuing completion of an album collection to obtain its completion reward.
- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "I had two cards left which would grant me the grand prize for completing an album, so i bought a deal"
  - why: The nearly completed album is a partially completed goal that pulled the player into continuing and making a purchase rather than abandoning it.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (7)

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
The review describes paid Poké Balls being consumed during capture attempts, with Pokémon repeatedly breaking out after the reviewer began purchasing them. The reviewer presents this as a hidden change or manipulation of capture outcomes designed to deplete the balls and cause further purchases, which is an allegation that the game determines outcomes unfairly rather than ordinary bad luck. The later edit says the reviewer did not write the review, but it does not describe any in-game messaging, posting, or account action by Pokémon GO, so it does not support Friend Spam / Impersonation.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: The reviewer links purchasing Poké Balls to repeated failed capture outcomes and depletion, implying that the game is manipulating capture odds to encourage more play or purchases.

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
The review describes a perceived manipulation of random outcomes: the reviewer says the RNG is clearly working against the player, which is an allegation that the game determines outcomes unfairly rather than leaving them genuinely random. The review also describes a poor in-game economy: a level costs 2200 and a win barely returns that amount, while spending actual money is presented as the alternative. However, it does not explicitly state that payment is required to continue or progress, nor does it describe a currency conversion, a specific stranded shortfall, or a reward-delivery system such as loot boxes. No web search is needed because the mechanics are understandable from the review itself.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "the rng is so obviously against you it's crazy"
  - why: The reviewer alleges that the game's random outcome system is biased against the player, describing manipulated outcome determination rather than merely reporting an unlucky streak.

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
The review describes a base-building game as repetitive, but “Same old same old grinder” is only a general quality judgment with no named repeated task tied to progress, so it does not establish Grinding. The clear mechanic is monetized competitive advantage: the reviewer says winning the event requires spending money, explicitly characterizing the game as pay to win and reporting a very large expenditure to win. The event is not explicitly described as competition against other players, so Competition is not assigned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Calculated total spent on last event was 30k to win."
  - why: The span states that a large monetary expenditure was used to win an in-game event, describing payment as the route to a gameplay advantage or outcome.

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
The review describes a payment-based advantage and payment-gated collection completion. The reviewer says that winning anything costs hundreds of dollars, which indicates that spending money provides the route to success or progress. The sticker mechanic requires paying a lot to obtain the final one or two stickers, so the player is pursuing a complete collection and the scarce final items are tied directly to an expensive purchase. The statement about being unable to write a review without giving five stars concerns the review platform rather than a mechanic within the game, so it is out of scope. The low completion rate is too vague to establish gambling, a random-reward system, or grinding.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "you will never get the last one or two unless you pay a lot of money to get them."
  - why: The final stickers are presented as effectively unavailable through ordinary play and obtainable only through an expensive purchase, tying manufactured scarcity to price.
- `M_PayToProgress` - ok
  - span: "if you want to win anything on this game it will cost hundreds of dollars."
  - why: The reviewer states that spending hundreds of dollars is required to win anything in the game.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them."
  - why: The reviewer describes pursuing the final stickers in a set, making completion of the sticker collection the relevant goal.

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
The review describes a pay-to-progress and pay-to-win structure: free-to-play players are said to be unable to keep up unless they buy the newest bot with money, rather than earning it. It also describes purchase offers appearing every time the player logs in and blocking access to gameplay until the screen can be dealt with, which is an in-game buying prompt that intercepts play. Finally, the last sentence implies that free rewards are obtained through watching ads, describing incentivized in-game advertising. The mention of a shifting meta does not by itself establish Power Creep because the review does not explicitly say that an already-owned purchased item lost value.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game."
  - why: Purchase offers appear at the point of entry and intercept gameplay before the player can play.
- `M_PayToProgress` - ok
  - span: "If you want to progress without paying money, goodluck! Even if you wanted to do f2p, you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it."
  - why: The review states that progressing or keeping up requires purchasing the newest bot with real money instead of using the free route.
- `T_Advertisement` - ok
  - span: "the only time you benofit by getting f2p rewards is ads"
  - why: The wording implies that free rewards are delivered through watching in-game advertisements.

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
The review describes a sticker-collection system in which sticker rewards repeatedly produce duplicates, making it difficult to complete the available sets. It also states that completing all sets is unavailable unless the player pays, so collection progress is monetized. The duplicate outcome supports a reward-delivery pattern involving unwanted repeated drops, while the set-completion goal supports collection compulsion.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: The review explicitly states that completing the collection is blocked unless the player spends money.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: The game structures progress around acquiring items needed to complete multiple sets.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: The sticker system repeatedly delivers unwanted duplicate items instead of the missing collection pieces.

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
The review describes several mechanics. Timed bonuses continue expiring while the player is offline, so the game's clock determines when their value is lost. The reviewer also says that winning enough gold is sometimes insufficient to keep playing without buying, which describes payment as an alternative to continued progress. The charge for five moves and the missing lives from a purchased package describe either a purchase/fulfillment problem, but they do not explicitly establish accidental-purchase UI or a deliberate dark pattern. The request that packages not be timed reinforces the existence of timed purchased benefits, but the clearest codable span is the timed bonuses expiring while the player is away. No web search is needed because all relevant mechanics are clear from the review.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The reviewer states that earning gold is sometimes insufficient to continue, making a purchase necessary for continued play.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone."
  - why: The bonuses lose value according to a real-time timer while the player is offline, forcing attention to the game's schedule.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (1)

### `32c623b4-0249-469e-968c-94f60c7fe3c2` - Royal Match

> It's an interesting game but the developers should pls try to include new cards in every card pack because I noticed when one is almost close to completing a set, new cards don't appear again especially when the set is almost expiring. So after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion because they don't add new sets to the cards once the collection is about to end.

| | labels |
|---|---|
| gold | `P_CompleteTheCollection`, `T_PlayingByAppointment` |
| pred | `P_CompleteTheCollection`, `P_IllusionOfControl`, `P_RewardMania`, `T_PlayingByAppointment` |
| **spurious** | `P_IllusionOfControl`, `P_RewardMania` |

**Model analysis**

```
The review describes a card-collection system in which cards are obtained from card packs and completing a set grants a reward. The player reports that, once a set is nearly complete or close to expiring, packs stop providing needed new cards, implying that the reward delivery is repeated and produces duplicate or non-progressing outcomes. The conditional timing also implies that card outcomes are being tuned or constrained near the end of the collection rather than being purely open-ended. Because the collection has an expiration deadline and the player can lose the completion reward, the game imposes a schedule on when progress must be completed. There is no explicit payment, price, or purchase mechanism, so monetary scarcity labels do not apply. No web search was needed.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "when one is almost close to completing a set"
  - why: The span describes pursuing completion of an in-game card set as a collection goal.
- `P_IllusionOfControl` - **SPURIOUS**
  - span: "when one is almost close to completing a set, new cards don't appear again especially when the set is almost expiring"
  - why: The reviewer attributes the lack of needed cards to the set's completion and expiration state, implying that the game constrains outcomes near the deadline.
- `P_RewardMania` - **SPURIOUS**
  - span: "include new cards in every card pack because I noticed when one is almost close to completing a set, new cards don't appear again"
  - why: Card packs are the reward-delivery mechanism, and repeated packs stop yielding the needed new cards near completion, sustaining attempts through variable or duplicate outcomes.
- `T_PlayingByAppointment` - ok
  - span: "especially when the set is almost expiring. So after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion"
  - why: The expiring collection creates a game-defined deadline, and failing to complete it causes the player to forfeit the completion reward.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_PayToProgress` | 2 | 3 |
| `S_Competition` | 2 | 1 |
| `P_RewardMania` | 2 | 1 |
| `S_Reciprocity` | 2 | 0 |
| `P_AestheticManipulation` | 2 | 0 |
| `M_Gambling` | 1 | 1 |
| `M_IntermediateCurrency` | 2 | 0 |
| `P_IllusionOfControl` | 0 | 1 |
| `M_PowerCreep` | 1 | 0 |
| `S_FriendSpamImpersonation` | 1 | 0 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `T_MandatoryMarathon` | 1 | 0 |
| `M_EasyToPurchase` | 1 | 0 |
| `M_WasteAversion` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |

