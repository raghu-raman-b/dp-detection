# Error review - gpt-5.6-luna_low_teacher_v1

`gpt-5.6-luna` / reasoning `low` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v1.txt` sha `e8cd52987c33`  
micro-F1 **0.789** (P 0.909 / R 0.698) - **22 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 6 | said NONE, gold had labels |
| SWAP | 5 | picked different labels than gold |
| MISSED ONLY | 10 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 1 | found all gold, added extras |

## The diagnostic that matters

Of **26** missed labels, **13** (50%) were named in the model's own analysis and dropped anyway; **13** (50%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `P_RewardMania` | 2 | 1 |
| `M_PayToProgress` | 2 | 1 |
| `S_Reciprocity` | 1 | 1 |
| `S_Competition` | 1 | 1 |
| `P_AestheticManipulation` | 0 | 2 |
| `M_Gambling` | 1 | 1 |
| `T_Grinding` | 2 | 0 |
| `M_IntermediateCurrency` | 1 | 1 |
| `M_PowerCreep` | 1 | 0 |
| `M_RecurringFee` | 0 | 1 |
| `T_MandatoryMarathon` | 0 | 1 |
| `M_EasyToPurchase` | 1 | 0 |
| `M_WasteAversion` | 0 | 1 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `T_PlayingByAppointment` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |

## Missed everything (predicted NONE) (6)

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
The review consists entirely of requested or hypothetical features: auctions, removing an option, an account-toggle widget, and hidden troop statistics. Under R12, proposed additions or changes do not trigger labels. No currently present game mechanic explicitly satisfies a meso label.
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
The review describes bugs, crashing, lag, slow switching, unresponsive attacks, and freezing that interfere with opening gifts, trading, catching Pokémon, and battles. Under R11, technical faults do not trigger dark-pattern labels; no deliberate mechanic is described. Competition is considered but rejected because PvP is merely mentioned as a game activity, not as a design that makes players compete.
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
The review attributes the inability to request troops from the clan to an update-related problem and says it needs to be fixed. Under R11, behavior attributed to a bug, error, or technical fault does not trigger dark-pattern labels. Although troop requests could otherwise relate to Reciprocity, this review does not describe a functioning resource-transfer mechanic, only its malfunction.
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
The review describes requests for hypothetical features: trading stickers with players in the app and using a purchased booster when challenged. Under R12, proposed or desired additions do not trigger labels. The mention that some players are not on Facebook does not describe the game sending messages, posting, or requesting contact access, so S_FriendSpamImpersonation is rejected under its boundary rule. No other current mechanic is explicitly described.
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
The review describes external advertising that misrepresents the game, but R13 excludes third-party/store advertising from coding and no in-game ad-view mechanic is described. It also describes training, building, and gathering resources as chores required to reach the puzzles; this is a progression activity, but the text does not explicitly state that these tasks are repeated or tedious beyond the evaluative word "chores," so T_Grinding is not assigned under its boundary rule. No other candidate label is supported.
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
The review describes being stuck on one level for almost two months and refusing to pay for power-ups. This does not explicitly describe a wait timer, repetitive activity, a game-wide unattainable end state, or payment being required to progress. The suggested daily login rewards are hypothetical and are excluded under R12. No label satisfies R2 and R3.
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
The review describes purchasing Poké Balls, capture attempts failing so the player must buy more, and an alleged change in outcome after purchases. This supports Pay to Progress because payment is presented as necessary to continue capturing, and Illusion of Control because the reviewer claims the game manipulates capture outcomes after purchases. The statement that the reviewer did not write the review describes the game acting through the player's account, supporting Friend Spam / Impersonation under the destination-of-message rule. Gambling is rejected because the review does not clearly describe a monetary wager for a chance-based prize; Intermediate Currency is rejected because Poké Balls are items, not currency.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: The reviewer says purchases are necessary to continue making captures after the game depletes the Poké Balls.
- `P_IllusionOfControl` - ok
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out"
  - why: The reviewer alleges that capture outcomes are manipulated after purchases, describing a hidden or rigged outcome determination.
- `S_FriendSpamImpersonation` - ok
  - span: "I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE"
  - why: The game is described as posting or attributing a review to the player that they did not write, using the player's account identity.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fdef27f2-9a21-4b8e-a04c-7a4753e0fb07` - 8 Ball Pool

> The game is great, but the user interface is completely rigged. Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins and are forced to buy real ones. ​We need a "Default Table Lock" or the game should always open the lowest bet table by default, not the highest! Fix this scammy feature. Giving 1 star

| | labels |
|---|---|
| gold | `M_Gambling`, `M_IntermediateCurrency`, `M_UIMisdirection` |
| pred | `M_IntermediateCurrency`, `M_PayToProgress`, `M_UIMisdirection` |
| **missed** | `M_Gambling` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_Gambling` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes an interface that automatically scrolls to and selects the highest-bet table, directing the player toward a costly option and causing accidental mis-clicks. It also describes losing coins and being forced to buy real ones, which establishes a paid route to continue playing and real-money acquisition of in-game currency. I rejected M_EasyToPurchase because the review describes accidental loss of coins rather than an unintended real-money purchase or an insufficient-funds purchase prompt. I rejected S_Competition because the 1v1 table is mentioned only as the location of the interface behavior, not as a competition mechanic.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "forced to buy real ones"
  - why: In context, 'ones' refers to coins, explicitly describing real-money acquisition of in-game currency.
- `M_PayToProgress` - **SPURIOUS**
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: The review describes payment as necessary to restore the currency needed to continue playing.
- `M_UIMisdirection` - ok
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins"
  - why: The interface automatically directs attention and selection toward the highest-cost betting option.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `176aaa1f-d8f9-4a1a-9f29-64902f13be5c` - All in Hole: Black Hole Games

> I would give 5 stars, but I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used.🤨😒🙄😥

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `T_MandatoryMarathon` |
| pred | `P_EasyToGetHardToLose` |
| **missed** | `M_IntermediateCurrency`, `T_MandatoryMarathon` |
| **spurious** | `P_EasyToGetHardToLose` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**
- `T_MandatoryMarathon` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes accumulated in-game holdings being lost after leaving: the bag is full when the player exits, but empty on return, and earned and purchased coins have been consumed. This supports Easy to Get, Hard to Lose because leaving results in forfeiture of value already held. Waste Aversion was considered but rejected because no specific currency shortfall, misaligned price, or inventory-capacity tradeoff is described. Playing by Appointment was rejected because no game-imposed schedule or required return window is stated.
```

**Labels assigned**

- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used"
  - why: Leaving the game causes accumulated inventory and currency to be lost, making it costly to stop playing.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a2ece36d-c527-442d-8f18-9a16b63994c8` - War Robots Multiplayer Battles

> Its a p2w game. The only time you enjoy it is when you're new. As you progress, everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game. If you want to progress without paying money, goodluck! Even if you wanted to do f2p, you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it. Plus the only time you benofit by getting f2p rewards is ads... 💩

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `M_PayToProgress`, `M_PowerCreep`, `T_Advertisement` |
| pred | `M_EasyToPurchase`, `M_PayToProgress`, `S_FearOfMissingOutFOMO`, `T_Advertisement` |
| **missed** | `M_PowerCreep` |
| **spurious** | `S_FearOfMissingOutFOMO` |

**Did the model consider what it missed?**

- `M_PowerCreep` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes purchase prompts that appear before gameplay, payment being required for smooth progression, paid access to the newest bot instead of earning it, pressure to keep up with a shifting meta, and rewards tied to ads. I considered Power Creep but rejected it under its boundary rule because the review does not explicitly state that previously acquired items lost value. I also rejected Intermediate Currency because no real-money-to-virtual-currency conversion is described.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game"
  - why: Purchase offers directly intercept gameplay before the player can play, matching prompted buying and active purchase solicitation.
- `M_PayToProgress` - ok
  - span: "If you want to progress without paying money, goodluck!"
  - why: The span explicitly contrasts progression with paying money, indicating that payment is required or strongly needed to advance.
- `S_FearOfMissingOutFOMO` - **SPURIOUS**
  - span: "you would not be able to keep up with shifting meta"
  - why: The reviewer describes pressure to keep pace with the changing competitive game state or fall behind.
- `T_Advertisement` - ok
  - span: "the only time you benofit by getting f2p rewards is ads"
  - why: The span describes free rewards being obtained through advertisements, indicating incentivized ad viewing.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b93c432d-19c0-4c6c-a2d4-bb9b21a436f3` - Dice Dreams™️

> A literal brain-rot game no wonder why they're tryna promote it through Free Cash. Also if you're thinking of making in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates! A real SCAM. Play it if u want but there are games that are actually good also, DON'T GET IN-APP PURCHASES!

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_PayToProgress`, `P_CompleteTheCollection` |
| **missed** | `P_AestheticManipulation`, `P_RewardMania` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**
- `P_RewardMania` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes purchasing a deal to obtain new cards, receiving duplicates instead, and needing two cards to complete an album for a grand prize. The purchase is tied to advancing toward the album reward, so M_PayToProgress applies. The album-completion goal describes a collection-compulsion mechanic, so P_CompleteTheCollection applies. M_Gambling and P_RewardMania were considered but rejected because the review does not explicitly describe a chance-based stake or a random delivery system; it describes a deal that promised new cards but delivered duplicates. No web search was needed.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "i bought a deal which promised i would get NEW cards"
  - why: The reviewer paid for a deal intended to advance completion of the album.
- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The span describes acquiring the remaining cards to complete an in-game collection for a reward.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (10)

### `0bc09fc3-6436-4a24-855e-0fdc56887918` - Fishdom

> EDIT 1/17/2023: Customer Service can't make good on 9 diamonds when game element doesn't appear within 5 original moves and 5 additional moves. It is a fun game, you don't have to pay to win. I suggest after this cust. svc experience that you don't buy from this game beyond the pass.Get friends and a team and trade lives.

| | labels |
|---|---|
| gold | `M_RecurringFee`, `S_Reciprocity` |
| pred | `S_Reciprocity` |
| **missed** | `M_RecurringFee` |

**Did the model consider what it missed?**

- `M_RecurringFee` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes an existing social resource exchange through "trade lives," which triggers Reciprocity. The 9-diamond complaint describes a reward or game-element condition but does not explicitly describe real money entering currency, a wager, repeated progress work, or a daily-return mechanic, so Intermediate Currency, Gambling, Pay to Progress, Grinding, and Playing by Appointment are rejected under R2 and R4. "You don't have to pay to win" is a denial of a mechanic, not evidence that payment is required.
```

**Labels assigned**

- `S_Reciprocity` - ok
  - span: "Get friends and a team and trade lives"
  - why: Trading lives is an in-game resource exchange that can create an obligation to reciprocate.

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
The review describes a reward for inviting friends and getting them to join Facebook, which triggers Forced Fellowship under the Social Pyramid Scheme indicator. It also describes chance-based gameplay and repeated duplicate sticker outcomes through "played max bet" and "Stickers are duplicates all the way...", supporting Reward Mania; Gambling is rejected because the review does not explicitly state that real money or purchased currency was wagered. The internet connection error is a technical fault, so it does not trigger a dark-pattern label under R11. No collection compulsion, competition, daily reward, or currency-conversion mechanic is explicitly described.
```

**Labels assigned**

- `P_RewardMania` - ok
  - span: "Stickers are duplicates all the way..."
  - why: Describes repeated unwanted duplicate outcomes from a variable sticker reward system.
- `S_ForcedFellowship` - ok
  - span: "no rewards for inviting friends and getting them to join facebook"
  - why: Describes inviting friends to join the game/social platform in connection with an in-game reward.

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
The review describes an alleged manipulated outcome mechanic: the RNG is said to be against the player. This supports P_IllusionOfControl under the rule covering claims that the game manipulates or predetermines outcomes. I considered M_PayToProgress, but the review does not explicitly state that payment is required to advance; it only says playing without spending is unrewarding. M_IntermediateCurrency is rejected because no named currency is described as being bought with real money. Reward Mania is rejected because no specific random reward-delivery system, such as packs, rolls, or gacha, is described.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "the rng is so obviously against you"
  - why: This asserts that the game's random outcome determination is biased against the player.

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
The review explicitly describes a daily-reward system and says the player cannot complete or receive those rewards without betting 50,000, which is an active condition attached to the daily reward cycle. This supports T_DailyRewards. I considered T_PlayingByAppointment, but the text describes a daily reward incentive rather than a real-world time gate blocking overall game progression. I rejected M_Gambling because no real-money stake or paid currency conversion is described, and rejected M_PayToProgress because the required bet is not described as a monetary payment for game advancement.
```

**Labels assigned**

- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The game ties daily rewards to completing a recurring daily task and withholds them unless the condition is met.

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
The review describes sticker collections that remain incomplete unless the player pays a lot, which is a payment-linked progression barrier and a compulsion to obtain the final collection items. The same span also describes manufactured scarcity tied to purchase, supporting Deceptive Luxury. I rejected Gambling because no chance-based paid mechanic is explicitly described, and rejected Fear of Missing Out because the review does not describe pressure from missing rewards or falling behind. The statement about needing an endless bank account is a general evaluation, not a separate mechanic.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: The final stickers are described as artificially scarce in a way that directly affects obtaining them through payment.
- `M_PayToProgress` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: The review says completing the sticker collection is effectively contingent on paying money.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two"
  - why: The span explicitly describes the player trying to obtain the remaining items needed to complete a sticker collection.

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
The review explicitly describes a payment barrier to advancement: “You must buy add ons else you can't make it through” and “it's pure time waste if you're not paying,” which satisfies M_PayToProgress. The lives running out and taking 5–7 days per level describe resource difficulty and slow progress, but do not explicitly describe a regeneration timer or repeated task activity, so T_PlayingByAppointment and T_Grinding are rejected. The reviewer is uninstalling rather than showing reluctance to leave despite investment, so P_EasyToGetHardToLose is not assigned. Daily mentions are about frequency of running out of lives, not daily login rewards.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through"
  - why: The review states that purchasing add-ons is required to progress through the game.

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

- `M_EasyToPurchase` - considered and rejected -> **rule interpretation**
- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes repetitive rounds undertaken to collect photos and complete a set, supporting Grinding and Complete the Collection. It also describes spending coins after losing, but does not clearly establish real-money conversion into coins, a chance-based wager, a purchase prompt that reduces real-money spending friction, or a deliberate currency shortfall. The failure to receive the photo is presented as a broken or misleading outcome rather than an explicitly described game mechanic, so Gambling, Pay to Progress, Intermediate Currency, Easy to Purchase, Reward Mania, and Waste Aversion are rejected under R2, R4, and R11.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "to complete the set"
  - why: The reviewer explicitly describes pursuing completion of an in-game collection.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The reviewer explicitly describes repeating rounds to pursue in-game progress.

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

- `M_DeceptiveLuxury` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes repeated duplicate sticker outcomes and difficulty completing all sets, which triggers Reward Mania for an unpredictable or repeated-attempt reward delivery and Complete the Collection for compulsion to finish sets. It also explicitly says completion requires payment, triggering Pay to Progress. Gambling is rejected because no paid chance-based stake or wager is described. Deceptive Luxury is rejected because no artificial scarcity or purchase-linked rarity is stated.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: States that payment is required to complete the sets and progress toward completion.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: Explicitly describes completing all collectible sticker sets.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: Repeated duplicate outcomes describe an unpredictable reward-delivery system requiring repeated attempts.

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
The review describes timed bonuses continuing to expire while the player is away, which imposes a game-controlled schedule and fits Playing by Appointment. It also states that progressing or continuing to play sometimes requires buying, fitting Pay to Progress. The missing lives after purchasing a package is described as a delivery failure rather than an intentional mechanic, so R11 suppresses dark-pattern labels. The gold charge does not explicitly demonstrate stranded currency or a real-money-to-currency conversion, so Waste Aversion and Intermediate Currency are rejected. The package timing is mentioned as a complaint/request but does not clearly establish a paid pass or subscription mechanic.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The review states that purchasing is sometimes necessary to obtain enough gold to continue playing.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone."
  - why: Bonuses expire according to the game's timer while the player is absent, forcing engagement on the game's schedule.

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

- `P_RewardMania` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes newer characters becoming necessary to deal damage as the meta changes, which indicates previously acquired characters lose practical value over time and triggers Power Creep. It also explicitly describes being forced to obtain new characters to perform effectively and calls the game pay to win, supporting Pay to Progress. Reduced rewards and lower quality are evaluations without a qualifying mechanic, and no separate Gambling or Reward Mania label is assigned because the review does not describe chance-based pulls or a monetary stake.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "basically forcing us to pull for new characters if we want to actually do damage"
  - why: The span describes obtaining new characters as necessary for effective gameplay progression and performance.
- `M_PowerCreep` - ok
  - span: "the Meta changes more and more every single day basically forcing us to pull for new characters if we want to actually do damage"
  - why: The changing meta makes older characters insufficient for dealing damage, showing devaluation through newer releases.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (1)

### `95ddadb3-82cd-4042-8a51-cf8b3ed164c2` - Mech Arena - Shooting Game

> You stuck waiting 30 seconds just to connect to a match. This game makes it seem like they give so many rewards but if all just for show. Its difficult to get weapon upgrades or any percs others you stick battling to win. This kind of games just rob you of your time in my opinion

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `S_Competition` |
| **spurious** | `S_Competition` |

**Model analysis**

```
The review describes a 30-second matchmaking connection wait, but this is a service or matchmaking delay rather than an in-game timer or wait-to-play mechanic, so T_PlayingByAppointment is rejected under the boundary rule. It mentions rewards being 'just for show' and difficulty obtaining weapon upgrades, but does not describe a specific reward-delivery or payment mechanic, so no reward or monetary label applies. Battling to win against others describes competitive gameplay, supporting S_Competition. The statement about being robbed of time is an evaluation and does not independently trigger Grinding.
```

**Labels assigned**

- `S_Competition` - **SPURIOUS**
  - span: "stick battling to win"
  - why: Describes competing in battles to win against other players.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_PayToProgress` | 3 | 3 |
| `S_Competition` | 2 | 1 |
| `P_RewardMania` | 3 | 0 |
| `S_Reciprocity` | 2 | 0 |
| `P_AestheticManipulation` | 2 | 0 |
| `M_Gambling` | 2 | 0 |
| `T_Grinding` | 2 | 0 |
| `M_IntermediateCurrency` | 2 | 0 |
| `M_PowerCreep` | 1 | 0 |
| `M_RecurringFee` | 1 | 0 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `T_MandatoryMarathon` | 1 | 0 |
| `M_EasyToPurchase` | 1 | 0 |
| `S_FearOfMissingOutFOMO` | 0 | 1 |
| `M_WasteAversion` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |

