# Error review - gpt-5.6-luna_high_20260821-143046

`gpt-5.6-luna` / reasoning `high` / search `True`  
prompt `../outputs/prompts/teacher_v1.txt` sha `519268bfa1e4`  
micro-F1 **0.795** (P 0.895 / R 0.716) - **24 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 4 | said NONE, gold had labels |
| SWAP | 4 | picked different labels than gold |
| MISSED ONLY | 12 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 4 | found all gold, added extras |

## The diagnostic that matters

Of **27** missed labels, **14** (52%) were named in the model's own analysis and dropped anyway; **13** (48%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `M_PayToProgress` | 5 | 1 |
| `P_RewardMania` | 0 | 3 |
| `M_Gambling` | 1 | 1 |
| `S_Competition` | 0 | 2 |
| `M_UIMisdirection` | 1 | 1 |
| `T_DailyRewards` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `P_CompleteTheCollection` | 1 | 0 |
| `T_Grinding` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `T_InfiniteTreadmill` | 0 | 1 |
| `M_WasteAversion` | 1 | 0 |
| `T_PlayingByAppointment` | 0 | 1 |
| `M_EasyToPurchase` | 1 | 0 |
| `T_Advertisement` | 1 | 0 |
| `S_EncouragesAntiSocialBehavior` | 0 | 1 |
| `M_NeverEndingLure` | 0 | 1 |

## Missed everything (predicted NONE) (4)

### `a7787e46-b95d-49e7-b1f5-e5d728141502` - Evony: The King's Return

> Waste of time and money,game full of bugs and glitches, not getting forward with the experience and power earning as you loose points and power overnight and can't get it back, last night I had over 9 mil power and this morning I had 7 without being attacked or something,no matter how many upgrades I do or how much I built still not getting points, that means loads of wasted time,as for costumer service is useless,so if you want to waste your time and money just feel free to play this game

| | labels |
|---|---|
| gold | `T_Grinding` |
| pred | _NONE_ |
| **missed** | `T_Grinding` |

**Did the model consider what it missed?**

- `T_Grinding` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes unexplained loss of power overnight and failure to gain points despite upgrades and building, while attributing the game generally to bugs and glitches. Under R11, the specific malfunction-related behavior is not codable. The references to wasted time and money are evaluations, and doing upgrades or building is not described as repetitive grinding under R2 and the Grinding boundary rule. No other label is supported by a clear mechanic.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `0d4962b2-8fd0-44d9-9cb9-0b801a39d408` - Dark War Survival

> This game is easy to understand, real money helps but not extremely necessary like other games, characters are not boring, good story, and abilities of each character are unique, so plan well. Great work development team, only encountered a slight problem with getting stuck on a certain scene at the beginning of game. No big deal tho

| | labels |
|---|---|
| gold | `M_PayToProgress` |
| pred | _NONE_ |
| **missed** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_PayToProgress` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes that real money provides some help, but does not link payment to progressing past an obstacle or gaining a required advantage, so M_PayToProgress is rejected under its progress-consequence rule. The reviewer also mentions getting stuck on a scene as a problem, but no codable mechanic is described; it is a technical issue, and no label applies.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `26b701e6-545c-4a13-b0ed-1bf4537a6852` - Carrom Pool: Disc Game

> It's a wonderful game. It would be nice if the developers put a rule where if a player passes without touching a coin more than once then he would automatically forfeit the game. Many of the player so prefer not to start the game to be on teh safer side. It's a bit unsporting.

| | labels |
|---|---|
| gold | `S_Competition`, `S_EncouragesAntiSocialBehavior` |
| pred | _NONE_ |
| **missed** | `S_Competition`, `S_EncouragesAntiSocialBehavior` |

**Did the model consider what it missed?**

- `S_Competition` - never mentioned -> **attention / recall**
- `S_EncouragesAntiSocialBehavior` - never mentioned -> **attention / recall**

**Model analysis**

```
The review requests a new forfeiture rule and describes players choosing not to start, but it does not describe an existing game mechanic that rewards, forces, or otherwise structures this behavior. The proposed rule is excluded under R12, and the complaint about unsporting conduct is evaluation alone under R2. No candidate label satisfies the codebook.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `6877b6bf-e9e0-4c86-a196-e7c85a51529f` - Candy Crush Saga

> In the past I would have rated this game higher, but recent changes have result in too many pop up screens with weekly challenge score, and are you sure you want to quit screens that you have to X out of before continuing. It was a fun way to kill a few minutes on a break, but now it has so many screens to go through it has just become annoying. They have also increased the cost, so I will probably uninstall it all together. Too bad.

| | labels |
|---|---|
| gold | `M_UIMisdirection`, `S_Competition` |
| pred | _NONE_ |
| **missed** | `M_UIMisdirection`, `S_Competition` |

**Did the model consider what it missed?**

- `M_UIMisdirection` - considered and rejected -> **rule interpretation**
- `S_Competition` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes frequent pop-up and confirmation screens, including "are you sure you want to quit" screens that must be dismissed before continuing, plus increased cost. I considered M_EasyToPurchase and M_UIMisdirection, but no purchase prompt, default purchase, misleading purchase control, or obstructed purchase opt-out is described. T_MandatoryMarathon does not apply because the review does not say quitting forfeits progress or that the player must continue playing. The increased cost is not linked to progress or a recurring fee. Under R2, the remaining complaints are general annoyance, so NONE.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (4)

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
The review describes Poké Balls being consumed unusually quickly after purchase, allegedly because captures break out more often, so the player must buy more. This supports Pay to Progress because payment is presented as necessary to continue capture gameplay, and Illusion of Control because the reviewer alleges purchase-linked manipulation of capture outcomes. The edit states that the review was not written by the reviewer, which fits store-review impersonation. Intermediate Currency is rejected because Poké Balls are items, not currency; Waste Aversion and Reward Mania are not supported because no stranded currency or reward-delivery mechanic is described. Reciprocity is rejected because the reviewer denies actually talking to other players.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "so I go through the balls faster so I have to purchase more"
  - why: The span describes needing to spend money on more Poké Balls to continue capture gameplay.
- `P_IllusionOfControl` - ok
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out"
  - why: The reviewer alleges that purchasing is associated with manipulated or worse capture outcomes.
- `S_FriendSpamImpersonation` - ok
  - span: "I DID NOT WRITE THIS REVIEW"
  - why: The edit describes a store review appearing under the player's identity without being authored by them, fitting the store-review impersonation boundary.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `6ccb26a7-01e3-41a3-ba1a-bddba2063257` - Lightning Link Casino Slots

> Dont even waste you time with this app. I dont understand why you guys make these things so fun to play but impossible to ever win. I mean I know your trying to make money on the app but why would I ever come back and spend more money when it is impossible to when. Because of that this app is garbage!!!!!!!

| | labels |
|---|---|
| gold | `M_PayToProgress` |
| pred | `M_Gambling` |
| **missed** | `M_PayToProgress` |
| **spurious** | `M_Gambling` |

**Did the model consider what it missed?**

- `M_PayToProgress` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a slot-style chance mechanic involving spending money and trying to win, which satisfies Gambling. I rejected Illusion of Control because “impossible to ever win” is only a general outcome complaint with no claim that the game conceals or manipulates how results are determined. No progress gate, currency conversion, reward-delivery pattern, or social mechanic is described.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "why would I ever come back and spend more money when it is impossible to when"
  - why: This span describes spending money in a slot-style game for the possibility of winning a reward.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `d64287d3-4179-440e-81b1-8aa1e5c20d7c` - MONOPOLY GO!

> Very addictive game. Massive downside is that all the cards you collect disappear after 30 days. So you have to collect them all over again, its hard enough getting all the cards as it is!!! The trading Facebook group is a waste of time, ok I've got some cards but not many from it. Problem is there is a set of 15 or so cards everyone is after, they are very rare so you lose all you have before getting the 162. Uninstalled as about to lose them all. Alot in other groups feel the same way.

| | labels |
|---|---|
| gold | `P_CompleteTheCollection`, `P_RewardMania`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| pred | `P_CompleteTheCollection`, `T_Grinding`, `T_PlayingByAppointment` |
| **missed** | `P_RewardMania`, `T_InfiniteTreadmill` |
| **spurious** | `T_Grinding` |

**Did the model consider what it missed?**

- `P_RewardMania` - never mentioned -> **attention / recall**
- `T_InfiniteTreadmill` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a 30-day expiration schedule that removes collected cards, forcing the player to repeat the collection process. This supports T_PlayingByAppointment because rewards are lost according to the game's clock, T_Grinding because the same collection activity must be repeated, and P_CompleteTheCollection because the player is required or motivated to obtain all cards. M_DeceptiveLuxury is rejected because rarity is not tied to price or purchase. P_EasyToGetHardToLose is rejected because the review describes impending loss and uninstalling, not reluctance to leave. S_Reciprocity is rejected because a trading group is mentioned without an obligation to reciprocate.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "collect them all over again"
  - why: The span describes acquiring the complete set of cards.
- `T_Grinding` - **SPURIOUS**
  - span: "you have to collect them all over again"
  - why: The player must repeat the same collection activity to regain progress.
- `T_PlayingByAppointment` - ok
  - span: "all the cards you collect disappear after 30 days"
  - why: The game imposes a 30-day schedule after which collected rewards are lost.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `61c9847d-6625-4f03-857c-eae510d042a4` - RAID: Shadow Legends

> It's very grindy but the graphics are actually nice. The game play is different from some of the ads. Is a turn based multistage battle game item customization. There is a lot of characters to choose from and to get all you would need to upgrade your storage many times. One commercial shows people changing the characters appearance I have not seen that but maybe, I did start playing a week ago and I am still playing. I think it's a good game to spend extra time while doing other things.

| | labels |
|---|---|
| gold | `M_WasteAversion` |
| pred | `P_CompleteTheCollection` |
| **missed** | `M_WasteAversion` |
| **spurious** | `P_CompleteTheCollection` |

**Did the model consider what it missed?**

- `M_WasteAversion` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a roster of characters and the possibility of acquiring all of them, which supports Complete the Collection. The statement that the game is "grindy" does not identify a repeated task required for progress, so T_Grinding is rejected under its boundary rule. The references to ads and a commercial describe out-of-game marketing, so they are excluded under R13. Storage upgrades are mentioned, but no capacity limit, stranded currency, or forfeited value is described, so M_WasteAversion is rejected.
```

**Labels assigned**

- `P_CompleteTheCollection` - **SPURIOUS**
  - span: "There is a lot of characters to choose from and to get all"
  - why: This describes acquiring the complete set of available characters.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (12)

### `432d7a64-e295-4aed-bb30-8ae44f9ddd45` - Disney Solitaire

> games alright but the prizes are wack when you beat a level, and the in-game purchase even more wack , prizes needa be better, and less expensive, I don't mind putting $1 or 2$ but 20$ for only 100k or so coins to lose in one round because the cards are not the one you need, do better disney

| | labels |
|---|---|
| gold | `M_Gambling`, `M_IntermediateCurrency`, `M_PayToProgress` |
| pred | `M_IntermediateCurrency` |
| **missed** | `M_Gambling`, `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_Gambling` - considered and rejected -> **rule interpretation**
- `M_PayToProgress` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes purchasing in-game coins with real money: "$20 for only 100k or so coins." This satisfies M_IntermediateCurrency because real money is exchanged for virtual currency. The poor prize value does not itself describe a codable mechanic under R2. M_Gambling is rejected because the review does not clearly describe paying to participate in a chance-based reward mechanic; M_PayToProgress is rejected because the purchase is not explicitly tied to progressing; M_WasteAversion is rejected because no stranded currency, capacity limit, or specific shortfall is described; and P_RewardMania is rejected because the complaint concerns prize value rather than reward delivery.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok  _[span not verbatim]_
  - span: "$20 for only 100k or so coins"
  - why: The span describes exchanging real-world money for in-game coins.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `dcae7f00-139f-4fc2-afdd-ea6e55a81188` - Lotsa Slots - Casino Games

> Favorite,but: now is easier to ask our clan for a stamp.I wasn't able to figure that out before and that was frustrating.Beware when you are clicking on the times at the top,or the Spin,because it changes it to higher.Beware of the wording on promotions with extra coins.The wording makes you think you are going to get more than you think.I got a big win of over a trillion.My extra coins for their promotion was worded so that I thought I was getting a trillion and up to 300%.I got only the 20%.

| | labels |
|---|---|
| gold | `M_UIMisdirection`, `P_AestheticManipulation`, `S_Reciprocity` |
| pred | `P_AestheticManipulation`, `S_Reciprocity` |
| **missed** | `M_UIMisdirection` |

**Did the model consider what it missed?**

- `M_UIMisdirection` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes requesting a resource from an existing clan, which satisfies Reciprocity. It also describes misleading wording in an in-game coin promotion, satisfying Aesthetic Manipulation. I rejected UI Misdirection and Easy to Purchase because the clicking behavior is too unclear and does not explicitly describe a purchase interface or obstructed opt-out. Gambling and Reward Mania are not assigned because no real-money stake or sufficiently explicit random-reward mechanic is described. No temporal, progression, collection, or technical mechanic is stated.
```

**Labels assigned**

- `P_AestheticManipulation` - ok
  - span: "The wording makes you think you are going to get more than you think."
  - why: Misleading promotional wording manipulates the player's understanding of the reward offered.
- `S_Reciprocity` - ok
  - span: "ask our clan for a stamp"
  - why: The player describes asking existing clan members for an in-game resource.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `e01c9ca3-6f2b-48b7-9efa-29730c872c74` - Dice Dreams™️

> This game is engaging, and fun. It offers high enough rewards that you don't run out of rolls too quickly. The only thing I don't like is they inundate you with request to purchase rolls. We can easily see what offers there are we don't need 6+ thrown at us every time we are out of rolls.

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `M_PayToProgress`, `P_RewardMania` |
| pred | `M_EasyToPurchase` |
| **missed** | `M_PayToProgress`, `P_RewardMania` |

**Did the model consider what it missed?**

- `M_PayToProgress` - considered and rejected -> **rule interpretation**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes repeated purchase offers appearing when the player runs out of rolls, so M_EasyToPurchase applies because the prompt is triggered by depletion of a gameplay resource and interrupts play. I rejected T_Advertisement because the review does not describe watching advertisements, M_PayToProgress because it does not state that payment is required to advance, and M_IntermediateCurrency because it does not describe real money being converted into in-game currency.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "We can easily see what offers there are we don't need 6+ thrown at us every time we are out of rolls."
  - why: Purchase offers are repeatedly presented at the point when the player’s rolls are depleted, intercepting continued play.

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
The review describes duplicate sticker drops and an inability to complete all sets without payment. P_RewardMania applies because duplicate sticker delivery is an unwanted outcome of the sticker-pack system, and P_CompleteTheCollection applies because finishing all sets is the stated goal. M_PayToProgress applies because payment is described as necessary to finish them. M_Gambling was rejected under its boundary rule because the review does not state that money is spent on a chance-based stake. M_DeceptiveLuxury was rejected because no scarcity, rarity, or limited-time purchase condition is described; no social, daily-return, technical, or time-gating mechanic is present.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: Payment is described as necessary to complete the game's sets, making progress contingent on spending.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: The span explicitly describes the goal of completing an in-game collection.
- `P_RewardMania` - ok
  - span: "always get duplicates."
  - why: The span describes repeated unwanted duplicate sticker outcomes in the sticker collection system.

**Search:** `MONOPOLY GO stickers duplicate sticker packs complete sets mechanic` -> Confirmed that MONOPOLY GO uses collectible sticker sets and that sticker packs can produce duplicate stickers, resolving the sticker mechanic. ([play.google.com](https://play.google.com/store/apps/editorial?hl=en&id=mc_games_editorialevergreen_monopoly_go_all_about_stickers_postinstall_fcp&utm_source=openai))

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `ca58ab5e-d48a-4825-9466-c658f4181913` - Candy Crush Saga

> Wow what an awful experience. From the constant prompts to purchase powerups to the way it feels like almost every game is rigged to make you spend. It seems this game stopped being about fun a long time ago. I recently started as a new player. Made it to level 250 so I tried to give it an honest chance. It seems way to convenient that a level is failed 1 or 2 moves from winning. 20 or 30 times in a row. Before you get lucky enough to win. Nah. Uninstalled not coming back. Would not recommend.

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `T_Grinding` |
| pred | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `T_Grinding` |
| **missed** | `M_EasyToPurchase` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes repeated failed attempts to clear a level, which satisfies T_Grinding. It also alleges that outcomes are manipulated to induce spending, satisfying P_IllusionOfControl, and reports repeated near-wins, satisfying P_OptimismAndFrequencyBiases under the near-miss frequency rule. The constant purchase prompts do not establish M_EasyToPurchase because the review does not say they interrupt play, appear after insufficient funds, or require dismissal; they are solicitation volume alone. M_PayToProgress is rejected because payment is not explicitly described as required for progress.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "almost every game is rigged to make you spend"
  - why: The reviewer alleges that the game manipulates outcome determination to influence continued play and spending.
- `P_OptimismAndFrequencyBiases` - ok
  - span: "a level is failed 1 or 2 moves from winning. 20 or 30 times in a row."
  - why: The span describes repeated near-wins, an experienced clustering of almost-successes that can sustain optimism and further attempts.
- `T_Grinding` - ok
  - span: "a level is failed 1 or 2 moves from winning. 20 or 30 times in a row."
  - why: The span describes repeated attempts and failures while trying to progress past a level.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fd8ef7be-59cb-494a-b1ec-36466c3b7217` - War Robots Multiplayer Battles

> The game is great. The graphics are phenomenal. But the gameplay plays more for the people who are high levels. If you just starting out, Good luck getting off the ground. Hope your rich, cause that the only way your gonna level up in the beginning. Gameplay is fun, but ridiculously challenging. Anything and everything is costly and the more you spend, the slower it is to get upgraded. Bring your millions!! Dont try to contact the makers of the game to complain, your 1 of 1000's that do, so tough tots for you!

| | labels |
|---|---|
| gold | `M_PayToProgress`, `T_PlayingByAppointment` |
| pred | `M_PayToProgress` |
| **missed** | `T_PlayingByAppointment` |

**Did the model consider what it missed?**

- `T_PlayingByAppointment` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes progression as requiring wealth or spending: being rich is stated to be the only way to level up at the beginning. This satisfies M_PayToProgress. I considered T_Grinding, but the review describes slow upgrading without naming repetitive tasks, so it does not meet the grinding boundary. I rejected M_IntermediateCurrency because no in-game currency purchased with real money is named, and S_Competition because no explicit player-versus-player competition mechanic is described.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Hope your rich, cause that the only way your gonna level up in the beginning."
  - why: The span states that spending wealth is the only route to leveling up, directly describing payment as required for progress.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `2b3f7920-4f71-44b3-95c6-001ff525009b` - Coin Master

> this game is really wack! it wants you to spend money, but takes 10hrs just to get a full set of spins! Then when you buy the spins they still don't give you nothing! it is really a waste of money. and to top it off I contacted Coin Master about the extra money they took and never even received a response. now i remember why i stopped playing this game!

| | labels |
|---|---|
| gold | `M_Gambling`, `M_PayToProgress`, `P_RewardMania`, `T_PlayingByAppointment` |
| pred | `T_PlayingByAppointment` |
| **missed** | `M_Gambling`, `M_PayToProgress`, `P_RewardMania` |

**Did the model consider what it missed?**

- `M_Gambling` - never mentioned -> **attention / recall**
- `M_PayToProgress` - considered and rejected -> **rule interpretation**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a 10-hour wait to replenish a full set of spins, which is an in-game regeneration schedule and satisfies Playing by Appointment. The reviewer also mentions being encouraged to spend money and buying spins, but does not clearly state that payment is required for progress or that spins are an intermediate currency, so M_PayToProgress and M_IntermediateCurrency are rejected under R2 and R4. Complaints about money taken and poor customer service describe an outcome and support failure, not a codable mechanic.
```

**Labels assigned**

- `T_PlayingByAppointment` - ok
  - span: "takes 10hrs just to get a full set of spins"
  - why: The span describes an in-game wait and regeneration schedule that governs when the player can regain spins.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `5e6a5625-5291-4f0e-897c-1b63c1a26494` - MONOPOLY GO!

> I loved this game until the new season started. Suddenly I get no rewards for inviting friends and getting them to join facebook. I am struggling to get dices and when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way... And today. Well, I cannot log in to the game at all. It keeps giving me an internet connection error which is absolute nonsense. I have connected to 3 different wifi connections. BS!!😡

| | labels |
|---|---|
| gold | `M_Gambling`, `P_CompleteTheCollection`, `P_RewardMania`, `S_ForcedFellowship` |
| pred | `M_Gambling`, `P_RewardMania`, `S_ForcedFellowship` |
| **missed** | `P_CompleteTheCollection` |

**Did the model consider what it missed?**

- `P_CompleteTheCollection` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a reward tied to inviting friends, which satisfies Forced Fellowship. “Played max bet” with dice and “NO LUCK” describes wagering an in-game resource in a chance-based mechanic, so Gambling applies. Repeated duplicate stickers and unfavorable random outcomes describe Reward Mania. No Pay to Progress, Complete the Collection, or Waste Aversion mechanic is stated. The internet connection error is a technical fault, so it is suppressed under R11.
```

**Labels assigned**

- `M_Gambling` - ok
  - span: "when I finally had more than 500 dices and played max bet, absolutely NO LUCK!"
  - why: This describes wagering earned dice at a maximum bet in a luck-based mechanic.
- `P_RewardMania` - ok
  - span: "No Shut downs and no bank heists. Stickers are duplicates all the way..."
  - why: The span describes unfavorable random outcomes and repeated duplicate rewards.
- `S_ForcedFellowship` - ok
  - span: "no rewards for inviting friends and getting them to join facebook"
  - why: The game ties rewards to inviting friends and getting them to join.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `877dd32e-be8b-4100-aaa2-550c4cdbee0d` - Last War:Survival Game

> It's all fun and games until you hit level 8 and you lose the given shield. Players with higher levels will turn you into a punching bag. You may need a shield, but you'll have to buy one that costs a lot of gems and would only last for a few hours to 3 days (depending on the price). Definitely "pay to win" and has got that "VIP system" . If you're not willing to pay for upgrades, then this game's not for you. 🚮

| | labels |
|---|---|
| gold | `M_NeverEndingLure`, `M_PayToProgress`, `S_Competition` |
| pred | `M_PayToProgress`, `S_Competition` |
| **missed** | `M_NeverEndingLure` |

**Did the model consider what it missed?**

- `M_NeverEndingLure` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes player-versus-player attacks and a paid advantage system: the free shield expires at level 8, stronger players attack, and buying shields or upgrades is presented as necessary to compete. M_PayToProgress applies because the review explicitly describes the game as pay to win. S_Competition applies because players are set against one another. M_IntermediateCurrency is rejected because gems are only described as the payment medium, not as being acquired with real money. S_EncouragesAntiSocialBehavior is rejected because no reward or advantage for the attacking players is stated. M_RecurringFee and T_PlayingByAppointment are rejected because a VIP system and shield duration alone do not describe a subscription or a required play schedule.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Definitely "pay to win""
  - why: This explicitly describes spending as a route to gaining an in-game competitive advantage.
- `S_Competition` - ok
  - span: "Players with higher levels will turn you into a punching bag."
  - why: This describes players being placed against one another in adversarial gameplay.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `ce92d6ba-cc5f-40a1-bc8e-27a82fa0a8f8` - 8 Ball Pool

> way too many ads and paid popups. I've never seen a game ask u to watch an ad just to claim a daily reward

| | labels |
|---|---|
| gold | `T_Advertisement`, `T_DailyRewards` |
| pred | `T_Advertisement` |
| **missed** | `T_DailyRewards` |

**Did the model consider what it missed?**

- `T_DailyRewards` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes an ad-gated reward: the player must watch an advertisement to claim a reward, satisfying T_Advertisement. I considered T_DailyRewards, but the span only names a daily reward and does not describe a daily login incentive, reset, streak, or penalty for missing a day. I rejected M_EasyToPurchase because “paid popups” describes solicitation volume without a specific friction-reducing purchase mechanism or intercepted play.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "watch an ad just to claim a daily reward"
  - why: The game requires the player to watch an advertisement to obtain an in-game reward.

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
The review describes in-app purchase offers appearing before play, which supports Easy to Purchase because the offers intercept gameplay. It also describes progress requiring money and a shifting meta that makes the newest bot necessary, supporting Pay to Progress and Power Creep. I rejected Advertisement because the purchase offers are not described as ads, FOMO because no explicit pressure to continue or fear of missing out is stated, and ad-related labeling because the final malformed phrase does not clearly describe forced or rewarded ad viewing.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game"
  - why: Purchase offers are presented before the player can access gameplay, so the solicitation intercepts play.
- `M_PayToProgress` - ok
  - span: "If you want to progress without paying money, goodluck! Even if you wanted to do f2p, you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it"
  - why: The span states that progressing and keeping up requires buying the newest bot with real money.
- `M_PowerCreep` - ok
  - span: "you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it"
  - why: A shifting meta requiring the newest bot indicates that newer releases diminish the competitive value of earlier holdings and drive new purchases.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `85e4fd2a-3f2f-4fd5-9665-b7a22e0866cf` - Evony: The King's Return

> Don't even try playing. A lot of people play for the puzzles but this is actually a war game and quite an addictive one at that. The game has decided to start exploiting their customers in order to get them to spend money. They claim they're within their rights and will steal things from you that you worked for years to obtain. Unless you have 50-100k to throw into the game, I'd highly suggest not downloading or playing. It's simply gotten worse every year but most are too invested to leave.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `P_EasyToGetHardToLose` |
| pred | `P_EasyToGetHardToLose` |
| **missed** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_PayToProgress` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes accumulated long-term investment making players reluctant to quit: "most are too invested to leave." This satisfies P_EasyToGetHardToLose. I considered M_PayToProgress, but "Unless you have 50-100k to throw into the game" states a financial burden without clearly describing payment as a route to in-game progress, so it does not meet the label's mechanic requirement.
```

**Labels assigned**

- `P_EasyToGetHardToLose` - ok
  - span: "most are too invested to leave"
  - why: The span explicitly describes accumulated investment raising the cost of leaving the game.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (4)

### `176aaa1f-d8f9-4a1a-9f29-64902f13be5c` - All in Hole: Black Hole Games

> I would give 5 stars, but I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used.🤨😒🙄😥

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `T_MandatoryMarathon` |
| pred | `M_IntermediateCurrency`, `P_EasyToGetHardToLose`, `T_MandatoryMarathon` |
| **spurious** | `P_EasyToGetHardToLose` |

**Model analysis**

```
The review describes accumulated bag contents and coins, including purchased coins, being lost after leaving and returning. This supports P_EasyToGetHardToLose because exit causes forfeiture of held value, and T_MandatoryMarathon because stopping the session results in loss. M_IntermediateCurrency also applies because the review explicitly describes coins as purchased. M_WasteAversion and M_PayToProgress are rejected: no stranded currency shortfall or payment-for-progress gate is described.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "coins that I earned and purchased"
  - why: The review describes in-game coins as a currency acquired through purchase.
- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used"
  - why: Leaving and returning causes accumulated inventory and coins to be forfeited, making disengagement costly.
- `T_MandatoryMarathon` - ok
  - span: "I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used"
  - why: The session cannot be safely ended because leaving results in the loss of held value.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a12fb168-3791-4d93-8cee-9b38fceb3059` - Moba Legends: 5v5!

> If you want to get some serious anger issues and frustration,the game is for you.This game simply don't care about you at all,they only need money and frame(Obv it's a complete copy of league of legends). The match making, completely illogical,if you play good,game will give you bad teammates expecting you to carry and if you play bad,game will give you more bad teammates saying that it's so called "skill based matching". The only thing game will provide you is waste of time and energy

| | labels |
|---|---|
| gold | `P_IllusionOfControl` |
| pred | `P_IllusionOfControl`, `S_Competition` |
| **spurious** | `S_Competition` |

**Model analysis**

```
The review describes competitive 5v5 matchmaking through the references to "match making" and "teammates", so S_Competition applies. It also alleges that matchmaking deliberately assigns worse teammates based on whether the player performs well or poorly, which is a claim that outcomes are tuned by a hidden rule and triggers P_IllusionOfControl. Anger, frustration, wasting time and energy, wanting money, and copying another game are evaluations or general complaints without a codable mechanic; no grinding or payment mechanic is described.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "if you play good,game will give you bad teammates expecting you to carry and if you play bad,game will give you more bad teammates saying that it's so called "skill based matching""
  - why: The span alleges that matchmaking outcomes are deliberately tuned according to the player's performance, a hidden manipulation of match determination.
- `S_Competition` - **SPURIOUS**
  - span: "The match making, completely illogical"
  - why: Matchmaking in the named 5v5 game organizes players into competitive matches against other players.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `2f3e6e71-3aff-46a7-8055-04ae71d9fe90` - Fate/Grand Order (English)

> I have played for 2 years, this game has one of the best stories around. Do be warned this game is one of the rare type that doesnt use power creep to make you want to buy into the gatcha. They simply make you like the character.

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_RewardMania` |
| pred | `M_Gambling`, `P_AestheticManipulation`, `P_RewardMania` |
| **spurious** | `M_Gambling` |

**Model analysis**

```
The review describes a gacha mechanic and says players are encouraged to purchase into it because they like the characters. Gacha supports P_RewardMania, and "buy into the gatcha" describes a purchased chance-based stake, supporting M_Gambling. The character appeal is presented as the design's persuasion mechanism, supporting P_AestheticManipulation. M_PowerCreep is rejected because the review explicitly says the game does not use it; duration of play is not a mechanic.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "buy into the gatcha"
  - why: This describes purchasing access to a gacha mechanic involving chance-based rewards.
- `P_AestheticManipulation` - ok
  - span: "They simply make you like the character."
  - why: The game uses emotional attachment to characters to influence players toward the gacha.
- `P_RewardMania` - ok
  - span: "the gatcha"
  - why: The review names a gacha mechanic, an unpredictable reward-delivery structure.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `2d824d09-c570-40f8-86e5-4dbc6aaf28d8` - Roblox

> 1 star. Extremely disappointed with Roblox moderation. I recently returned to the game after a long break and was banned with the reason listed as “Other” without a clear explanation. I mainly spent time grinding and chatting with friends, yet my account was suddenly punished. The moderation system feels heavily automated and unfair, especially for players who use other languages that constantly get falsely censored. It’s frustrating to lose years of progress and money spent on an account becau

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `T_Grinding` |
| **spurious** | `T_Grinding` |

**Model analysis**

```
The review describes spending time grinding, which names repetitive gameplay activity, so T_Grinding applies. The ban, automated moderation, false censorship, and unclear punishment are not covered by any listed mechanic label. Chatting with friends does not describe recruitment, obligation, or resource exchange, so no social label applies. Losing years of progress and money is a realized loss caused by moderation, not investment making it difficult to quit, so P_EasyToGetHardToLose is rejected under its counterexample rule. No schedule, reward cadence, purchase prompt, gambling, or other codable mechanic is described.
```

**Labels assigned**

- `T_Grinding` - **SPURIOUS**
  - span: "I mainly spent time grinding"
  - why: This explicitly describes grinding as the gameplay activity the reviewer spent time performing.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_PayToProgress` | 6 | 1 |
| `M_Gambling` | 2 | 2 |
| `T_Grinding` | 1 | 2 |
| `P_RewardMania` | 3 | 0 |
| `S_Competition` | 2 | 1 |
| `P_CompleteTheCollection` | 1 | 1 |
| `M_UIMisdirection` | 2 | 0 |
| `T_DailyRewards` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `T_InfiniteTreadmill` | 1 | 0 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `M_WasteAversion` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `M_EasyToPurchase` | 1 | 0 |
| `T_Advertisement` | 1 | 0 |
| `S_EncouragesAntiSocialBehavior` | 1 | 0 |
| `M_NeverEndingLure` | 1 | 0 |

