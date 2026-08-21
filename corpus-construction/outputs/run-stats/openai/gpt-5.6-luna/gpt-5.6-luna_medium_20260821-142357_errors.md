# Error review - gpt-5.6-luna_medium_20260821-142357

`gpt-5.6-luna` / reasoning `medium` / search `True`  
prompt `../outputs/prompts/teacher_v1.txt` sha `519268bfa1e4`  
micro-F1 **0.734** (P 0.921 / R 0.611) - **28 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 4 | said NONE, gold had labels |
| SWAP | 2 | picked different labels than gold |
| MISSED ONLY | 19 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 3 | found all gold, added extras |

## The diagnostic that matters

Of **37** missed labels, **19** (51%) were named in the model's own analysis and dropped anyway; **18** (49%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `M_PayToProgress` | 3 | 3 |
| `S_Competition` | 3 | 2 |
| `P_RewardMania` | 2 | 2 |
| `M_Gambling` | 3 | 0 |
| `T_Grinding` | 1 | 1 |
| `T_InfiniteTreadmill` | 1 | 1 |
| `M_UIMisdirection` | 1 | 1 |
| `P_IllusionOfControl` | 0 | 1 |
| `T_Advertisement` | 1 | 0 |
| `M_RecurringFee` | 1 | 0 |
| `M_IntermediateCurrency` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `M_NeverEndingLure` | 0 | 1 |
| `P_CompleteTheCollection` | 0 | 1 |
| `T_DailyRewards` | 1 | 0 |
| `M_EasyToPurchase` | 1 | 0 |
| `P_AestheticManipulation` | 0 | 1 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `S_EncouragesAntiSocialBehavior` | 0 | 1 |

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
The review describes bugs and glitches causing overnight power loss and failed point progression, so those specific behaviours are technical malfunctions and are suppressed by R11. The repeated upgrades and building are mentioned as ineffective attempts to gain points, not as a required repetitive progression activity, so T_Grinding is rejected under R2 and R11. Wasted time and money are evaluations without a described monetization or retention mechanic, so no other label applies.
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
The review mentions that real money can help, but it does not describe payment as required for progress or identify a specific purchase mechanic, so M_PayToProgress is rejected under R2. The player getting stuck on a scene is described as a problem, so R11 suppresses mechanic labels for that span. No other codable game mechanic is described.
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
The review requests a new forfeiture rule and describes players choosing not to start a game. The requested mechanic is hypothetical and not present in the game, so it is not codable under R12. The existing player behavior does not describe a game design mechanic or a reward/incentive for harmful conduct; therefore no labels apply under R2.
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
- `S_Competition` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes more pop-up screens and a quit-confirmation screen that must be dismissed before continuing, but it does not connect these UI elements to purchases or a spending opt-out, so M_UIMisdirection is rejected under its boundary rule. “Weekly challenge score” does not describe competition against other players, and “increased the cost” does not specify a purchase, currency conversion, or payment-required progress mechanic. No codable mechanic satisfies R2 and R3.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (2)

### `fd1230ab-7d12-4aeb-a425-e37ed06bcd5c` - Pokémon GO

> I love this game, just started playing about 2 months ago. Though I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way. I feel taken advantage of. 3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| pred | `M_Gambling`, `S_FriendSpamImpersonation` |
| **missed** | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases` |
| **spurious** | `M_Gambling` |

**Did the model consider what it missed?**

- `P_IllusionOfControl` - never mentioned -> **attention / recall**
- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes paid Poké Balls being consumed during chance-based capture attempts, with failed captures causing more purchases; this satisfies Gambling. Pay to Progress is rejected because the payment is internal to the chance-based retry mechanic. Intermediate Currency and Waste Aversion are rejected because no real-money conversion into currency or stranded currency is described. The denial that the reviewer wrote the review, combined with the fabricated claim about talking to players, describes a review posted under the player's identity, satisfying Friend Spam / Impersonation.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: Paid Poké Balls are used for repeated chance-based capture attempts, with failure prompting further purchases.
- `S_FriendSpamImpersonation` - ok
  - span: "I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE"
  - why: The review states that content was posted under the player's identity and falsely attributed social interaction to them.

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
The review describes a casino-slot game and spending money in the app, so M_Gambling is a candidate; the span connects spending more money with trying to win. T_InfiniteTreadmill is rejected because "impossible to ever win" describes unsuccessful outcomes in a slot game, not an unattainable game completion state. No other label is supported: the review does not describe a specific reward-delivery mechanic, forced spending, repeated tasks, or a designed wait.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "why would I ever come back and spend more money when it is impossible to when"
  - why: This describes spending real money in a casino-slot game while pursuing a chance-based win.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (19)

### `b1cc70f9-680f-41cb-9ffc-bb9ecb4b03b9` - War Robots Multiplayer Battles

> I have been playing this for a long time and i can say that this is one of the worst pay to win games out there. If you dont want to spend, dont play. They will introduce a new robot and you will spend money to get it. And then one month later, the robot you have get nerfed and another new robot introduced. Worst of all is the lag. You could be good player, but the lag will get you if not, clans made out of players who have spent a lot of money will get you. There's nothing for free players.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_PowerCreep`, `S_Competition` |
| pred | `M_PayToProgress`, `M_PowerCreep` |
| **missed** | `S_Competition` |

**Did the model consider what it missed?**

- `S_Competition` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes payment as necessary to obtain newly introduced robots and frames the game as pay-to-win, satisfying M_PayToProgress. It also states that a purchased robot is nerfed one month later while a newer robot is introduced, showing devaluation of an acquired item and satisfying M_PowerCreep. Competition is mentioned through clans and other players defeating the reviewer, but no specific competitive game mechanic is clearly described beyond ordinary opposition, so S_Competition is rejected under R2. Lag is attributed to a technical fault and is not coded under R11. No currency conversion, gambling, advertising, scheduling, or other qualifying mechanic is described.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "They will introduce a new robot and you will spend money to get it."
  - why: The span describes spending money to obtain an in-game robot that provides gameplay advantage or progress.
- `M_PowerCreep` - ok
  - span: "And then one month later, the robot you have get nerfed and another new robot introduced."
  - why: The span describes an acquired robot being weakened after a newer robot is introduced, reducing its value over time.

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
The review describes accumulated bag contents and coins being lost after leaving and returning, which indicates that ending a session forfeits held progress or resources, satisfying Mandatory Marathon. Easy to Get, Hard to Lose is rejected because the review does not describe reluctance to quit or continued play caused by the investment. Waste Aversion is rejected because no currency-capacity mismatch or specific unusable remainder is described.
```

**Labels assigned**

- `T_MandatoryMarathon` - ok
  - span: "I would give 5 stars, but I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used."
  - why: Leaving the game results in accumulated bag contents and coins being forfeited, indicating the player cannot stop without losing held value.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `e6574f43-708e-4fd4-890d-5ae5b80d81cb` - Clash of Clans

> After a year of grinding, and buying gold/event passes, Supercell just released an update that invalidates most of the progress I achieved. New players get my current level of hero equipment progress for free, and can easily overtake me, while I get nothing and am still years away from maxing it out, despite playing actively every day and spending money on the game. For context, if I didn't focus on upgrading my heroes, I'd get 2,5k starry ores, which is ~1 year of progress.

| | labels |
|---|---|
| gold | `M_PowerCreep`, `M_RecurringFee`, `T_Grinding` |
| pred | `M_PowerCreep`, `T_Grinding` |
| **missed** | `M_RecurringFee` |

**Did the model consider what it missed?**

- `M_RecurringFee` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes repetitive effort invested toward progression and an update that devalues previously achieved progress by giving newer players equivalent hero-equipment progress for free. These support T_Grinding and M_PowerCreep. I rejected M_RecurringFee because passes are mentioned but no mechanic encouraging play to justify recurring spending is described; M_PayToProgress because spending is reported without being stated as required for progression; T_InfiniteTreadmill because being years from maxing out does not establish an unattainable end state; and T_DailyRewards because daily play is not linked to a reward or penalty for missing days.
```

**Labels assigned**

- `M_PowerCreep` - ok
  - span: "Supercell just released an update that invalidates most of the progress I achieved. New players get my current level of hero equipment progress for free, and can easily overtake me"
  - why: The update makes previously achieved progress less valuable by allowing newer players to catch up or surpass it for free.
- `T_Grinding` - ok
  - span: "After a year of grinding"
  - why: The reviewer describes extended repetitive effort invested in achieving game progress.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `432d7a64-e295-4aed-bb30-8ae44f9ddd45` - Disney Solitaire

> games alright but the prizes are wack when you beat a level, and the in-game purchase even more wack , prizes needa be better, and less expensive, I don't mind putting $1 or 2$ but 20$ for only 100k or so coins to lose in one round because the cards are not the one you need, do better disney

| | labels |
|---|---|
| gold | `M_Gambling`, `M_IntermediateCurrency`, `M_PayToProgress` |
| pred | `M_IntermediateCurrency` |
| **missed** | `M_Gambling`, `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_Gambling` - considered and rejected -> **rule interpretation**
- `M_PayToProgress` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes real money being exchanged for in-game coins, which satisfies Intermediate Currency. It does not clearly describe gambling, a progress gate, randomised reward delivery, or currency stranded through a pricing mismatch; the coins being consumed in a round is not Waste Aversion under its boundary rule.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok  _[span not verbatim]_
  - span: "$20 for only 100k or so coins"
  - why: This describes acquiring in-game coins through a real-money purchase.

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
The review describes requesting a stamp from the clan, which is a resource-help exchange and satisfies Reciprocity. It also describes promotional wording that misleads the player about the amount of extra coins received, satisfying Aesthetic Manipulation because the deception is in the text. I considered UI Misdirection for the controls that change to a higher setting, but the review does not clearly connect this to a purchase or to an obstructed purchase opt-out, so it is rejected under R2 and the UI Misdirection boundary rule. Intermediate Currency, Pay to Progress, Gambling, and Easy to Purchase are not supported because no real-money conversion, progress gate, wager, or purchase-interception mechanic is described.
```

**Labels assigned**

- `P_AestheticManipulation` - ok
  - span: "The wording makes you think you are going to get more than you think"
  - why: Misleading promotional wording exploits the player's interpretation to influence expectations about the reward.
- `S_Reciprocity` - ok
  - span: "ask our clan for a stamp"
  - why: The player requests an in-game resource or favor from existing clan members.

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
The review describes repeated purchase prompts for rolls that appear whenever the player runs out of rolls, which is an insufficient-resource interception and fits M_EasyToPurchase. T_Advertisement is rejected because the prompts are purchase offers, not ads or rewarded ad viewing. M_PayToProgress is rejected because the review does not say payment is required to continue or progress. No timer or regeneration schedule is described, so T_PlayingByAppointment is rejected.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "we don't need 6+ thrown at us every time we are out of rolls"
  - why: Purchase offers are repeatedly pushed at the player when their rolls are depleted, intercepting play at an insufficient-resource point.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `2f3e6e71-3aff-46a7-8055-04ae71d9fe90` - Fate/Grand Order (English)

> I have played for 2 years, this game has one of the best stories around. Do be warned this game is one of the rare type that doesnt use power creep to make you want to buy into the gatcha. They simply make you like the character.

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_RewardMania` |
| pred | `P_RewardMania` |
| **missed** | `P_AestheticManipulation` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The review names a gacha mechanic, which triggers P_RewardMania under the gacha-mechanics indicator. Power creep is explicitly described as absent ('doesnt use power creep'), so M_PowerCreep is rejected under R4. M_Gambling is rejected because the review does not clearly describe real-money spending or a wager; 'buy into the gatcha' is insufficiently explicit under the Gambling boundary rule.
```

**Labels assigned**

- `P_RewardMania` - ok
  - span: "buy into the gatcha"
  - why: This span names participation in a gacha mechanic, an indicator of Reward Mania.

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
The review describes randomized sticker rewards producing duplicates and a collection goal that cannot be completed without payment. These satisfy Reward Mania, Complete the Collection, and Pay to Progress. Gambling is rejected because no wager or chance-based purchase is described; Deceptive Luxury is rejected because no scarcity tied to price or purchase is stated.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: States that further collection progress is contingent on making a payment.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: Explicitly describes the compulsion or goal of acquiring items to complete all collections.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: Describes repeated duplicate drops from a randomized reward or collection system.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `ca58ab5e-d48a-4825-9466-c658f4181913` - Candy Crush Saga

> Wow what an awful experience. From the constant prompts to purchase powerups to the way it feels like almost every game is rigged to make you spend. It seems this game stopped being about fun a long time ago. I recently started as a new player. Made it to level 250 so I tried to give it an honest chance. It seems way to convenient that a level is failed 1 or 2 moves from winning. 20 or 30 times in a row. Before you get lucky enough to win. Nah. Uninstalled not coming back. Would not recommend.

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `T_Grinding` |
| pred | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases` |
| **missed** | `M_EasyToPurchase`, `T_Grinding` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - considered and rejected -> **rule interpretation**
- `T_Grinding` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes repeated near-misses and explicitly attributes them to rigging, which supports Illusion of Control and Optimism and Frequency Biases. The constant purchase prompts are solicitation volume without a described interception or friction-reducing purchase mechanism, so EasyToPurchase is rejected under its boundary rule. PayToProgress is rejected because the review does not state that payment is required to advance, only that the game seems designed to make the player spend.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "it feels like almost every game is rigged to make you spend"
  - why: The reviewer asserts that the game manipulates or rigs outcomes to create a misleading impression and induce further play or spending.
- `P_OptimismAndFrequencyBiases` - ok
  - span: "a level is failed 1 or 2 moves from winning. 20 or 30 times in a row"
  - why: This describes repeated engineered or clustered near-wins that can make success feel unusually frequent or imminent.

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
The review describes progression as requiring wealth or spending: being rich is presented as the only way to level up, and spending is explicitly linked to upgrading. This satisfies M_PayToProgress. I rejected M_IntermediateCurrency because no real-money purchase of an in-game currency is described; T_Grinding because no repetitive activity is specified; S_Competition because multiplayer competition is not described; and M_PowerCreep because no purchased item loses value over time.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Hope your rich, cause that the only way your gonna level up in the beginning."
  - why: The reviewer states that being wealthy is the only way to level up, making payment or spending a route required for progression.

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

- `M_Gambling` - considered and rejected -> **rule interpretation**
- `M_PayToProgress` - never mentioned -> **attention / recall**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a 10-hour wait to replenish a full set of spins, which is an in-game timer imposing when the player can resume play, so T_PlayingByAppointment applies. The statements that the game wants spending and that bought spins yielded nothing do not establish payment as required for progress, a real-money-to-currency conversion, gambling, or realised currency waste. The complaint about extra money taken is a transaction dispute without a qualifying purchase-interface mechanic.
```

**Labels assigned**

- `T_PlayingByAppointment` - ok
  - span: "takes 10hrs just to get a full set of spins"
  - why: Describes an in-game timer requiring the player to wait 10 hours for spins to replenish before continuing play.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `5e6a5625-5291-4f0e-897c-1b63c1a26494` - MONOPOLY GO!

> I loved this game until the new season started. Suddenly I get no rewards for inviting friends and getting them to join facebook. I am struggling to get dices and when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way... And today. Well, I cannot log in to the game at all. It keeps giving me an internet connection error which is absolute nonsense. I have connected to 3 different wifi connections. BS!!😡

| | labels |
|---|---|
| gold | `M_Gambling`, `P_CompleteTheCollection`, `P_RewardMania`, `S_ForcedFellowship` |
| pred | `S_ForcedFellowship` |
| **missed** | `M_Gambling`, `P_CompleteTheCollection`, `P_RewardMania` |

**Did the model consider what it missed?**

- `M_Gambling` - considered and rejected -> **rule interpretation**
- `P_CompleteTheCollection` - never mentioned -> **attention / recall**
- `P_RewardMania` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes an invitation mechanic tied to getting friends to join Facebook, which satisfies Forced Fellowship despite the reported reward failure. I rejected Friend Spam / Impersonation because no message, post, or invitation sent through the player's account is described. I rejected Gambling and Reward Mania because 'played max bet' and 'Stickers are duplicates all the way' do not clearly establish a qualifying wager or randomized reward-delivery mechanic. The internet connection error is attributed to a technical fault, so it is not coded under a design label.
```

**Labels assigned**

- `S_ForcedFellowship` - ok
  - span: "no rewards for inviting friends and getting them to join facebook"
  - why: Describes inviting friends to join the game or its social network in connection with an expected in-game reward.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `d64287d3-4179-440e-81b1-8aa1e5c20d7c` - MONOPOLY GO!

> Very addictive game. Massive downside is that all the cards you collect disappear after 30 days. So you have to collect them all over again, its hard enough getting all the cards as it is!!! The trading Facebook group is a waste of time, ok I've got some cards but not many from it. Problem is there is a set of 15 or so cards everyone is after, they are very rare so you lose all you have before getting the 162. Uninstalled as about to lose them all. Alot in other groups feel the same way.

| | labels |
|---|---|
| gold | `P_CompleteTheCollection`, `P_RewardMania`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| pred | `P_CompleteTheCollection`, `T_PlayingByAppointment` |
| **missed** | `P_RewardMania`, `T_InfiniteTreadmill` |

**Did the model consider what it missed?**

- `P_RewardMania` - considered and rejected -> **rule interpretation**
- `T_InfiniteTreadmill` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a 30-day expiration rule that removes collected cards and forces the collection process to restart, which satisfies Playing by Appointment because progress/rewards are governed by a game-set deadline and loss. It also explicitly describes the goal of collecting all cards, satisfying Complete the Collection. Deceptive Luxury is rejected because the rarity is not tied to price or purchase. Reward Mania and Gambling are rejected because no randomised delivery mechanism or monetary stake is described. Reciprocity and Friend Spam / Impersonation are rejected because mentioning a Facebook trading group does not describe compelled exchange or game-sent messages.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "you have to collect them all over again"
  - why: The review explicitly describes the compulsion and requirement to acquire the complete set of cards.
- `T_PlayingByAppointment` - ok
  - span: "all the cards you collect disappear after 30 days. So you have to collect them all over again"
  - why: Collected rewards expire on a game-set clock, forcing the player to complete the collection within the time window or lose progress.

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
The review describes competitive attacks by higher-level players and a paid advantage system: shields must be purchased with gems, and upgrades require payment. I considered M_IntermediateCurrency but rejected it because the review does not describe real money being converted into gems. I rejected T_PlayingByAppointment because shield duration is not a required play schedule or wait timer, and rejected S_EncouragesAntiSocialBehavior because attacking other players is described as ordinary competitive play without an explicit reward for harmful or dishonest conduct.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Definitely "pay to win" and has got that "VIP system" . If you're not willing to pay for upgrades, then this game's not for you."
  - why: This describes payment granting in-game advantages and upgrades being effectively required to play successfully.
- `S_Competition` - ok
  - span: "Players with higher levels will turn you into a punching bag."
  - why: This describes the game making players compete against one another through attacks.

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
The review describes an in-game ad required to claim a reward, which satisfies T_Advertisement. It mentions a daily reward, but does not describe a login incentive, resetting reward, streak, or penalty for missing a day, so T_DailyRewards is rejected under R2. Paid popups alone do not establish a purchase-friction mechanism for M_EasyToPurchase.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "ask u to watch an ad just to claim a daily reward"
  - why: The game requires the player to watch an advertisement to obtain an in-game reward.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b2dc0bc8-8ebe-4c48-bc05-38d0d65acb84` - Last War:Survival Game

> It's a nice game, but it's set up in a pay to win way. I played for 10 days, and the update times for your base are becoming ridiculous. Everything scales endlessly, there is kinda no point to look forward to, just more grind. The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff. Alliances are also weird, with the top ones dictating what to develop, what to rush, etc. If you are not in one then you get attacked and bullied. Not a great experience.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_UIMisdirection`, `S_Competition`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| pred | `M_PayToProgress`, `M_UIMisdirection`, `T_PlayingByAppointment` |
| **missed** | `S_Competition`, `T_InfiniteTreadmill` |

**Did the model consider what it missed?**

- `S_Competition` - never mentioned -> **attention / recall**
- `T_InfiniteTreadmill` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes payment conferring in-game advantage, base upgrade timers, endlessly scaling progression, and a deliberately confusing purchase-oriented UI. Pay to Progress applies to the explicit pay-to-win setup. Playing by Appointment applies because base updates impose waiting times. Infinite Treadmill is considered but rejected: endlessly scaling systems and a lack of future goals do not clearly state that the game itself cannot be completed. Grinding is rejected because no repetitive activity required for progress is named. UI Misdirection applies because the interface is described as deliberately confusing to push purchases. Alliance pressure is rejected under the coerced-grouping boundary: being attacked or bullied for not joining does not describe recruitment rewards or an obligation to avoid letting teammates down. Easy to Purchase is rejected because no specific purchase-friction mechanism such as a default purchase, insufficient-funds prompt, or absent confirmation is described.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "it's set up in a pay to win way"
  - why: The span describes payment granting an in-game advantage, which is an included Pay to Progress indicator.
- `M_UIMisdirection` - ok
  - span: "The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff"
  - why: The span attributes confusing interface design to steering the player toward purchases.
- `T_PlayingByAppointment` - ok
  - span: "the update times for your base are becoming ridiculous"
  - why: Base update times describe in-game timers that impose waiting before progress can continue.

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
The review describes players remaining because they are heavily invested in long-term progress: "most are too invested to leave," which satisfies Easy to Get, Hard to Lose. The statement about spending 50-100k does not clearly connect payment to a specific progression obstacle, so M_PayToProgress is rejected under R2 and the Pay to Progress boundary. Claims that the game is exploitative or has worsened over time are too general, and the theft statement does not describe a qualifying loss-on-exit rule.
```

**Labels assigned**

- `P_EasyToGetHardToLose` - ok
  - span: "most are too invested to leave"
  - why: Accumulated investment in the game is explicitly described as making players reluctant or unable to leave.

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
The review describes an in-game advertisement with no available close control and taps redirected to the store, which obstructs opting out and steers the player toward a purchase surface. This satisfies M_UIMisdirection. T_Advertisement was considered but rejected under R2 because the review does not state that viewing the ad was forced or reward-incentivized. T_MandatoryMarathon was rejected because no gameplay progress is forfeited when exiting.
```

**Labels assigned**

- `M_UIMisdirection` - ok
  - span: "No cross mark on the screen , if you try to click anywhere on the screen it takes you to store."
  - why: The interface removes the normal opt-out control and redirects taps toward the store, obstructing dismissal and steering attention toward purchase.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `14e87cfb-665b-4239-863d-2175f401d894` - Clash Royale

> this game is so annoying all you play against after 8k trophies is mega knight,pekka, and golem they need to rebuffed them they are so annoying to play against and when spammed down its annoying to defend this game is not fun for that reason its also pay to win and usually doesn't let you get higher from just using skill you have to go out of your way to be annoying to actually win in a game this game is getting more and more pay to win with each update and they buff cards people hate

| | labels |
|---|---|
| gold | `M_PayToProgress`, `S_Competition` |
| pred | `M_PayToProgress` |
| **missed** | `S_Competition` |

**Did the model consider what it missed?**

- `S_Competition` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes progression being tied to spending through the explicit pay-to-win statement, which satisfies M_PayToProgress. The card matchup and annoyance complaints are evaluations, not separate codable mechanics. S_Competition is rejected because the review says the player is fighting specific cards, not that the game mechanic makes players compete against one another. M_PowerCreep is rejected because buffs to disliked cards do not show purchased items losing value after acquisition.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "its also pay to win and usually doesn't let you get higher from just using skill"
  - why: This describes progression being restricted for players who do not use paid advantages.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (3)

### `a12fb168-3791-4d93-8cee-9b38fceb3059` - Moba Legends: 5v5!

> If you want to get some serious anger issues and frustration,the game is for you.This game simply don't care about you at all,they only need money and frame(Obv it's a complete copy of league of legends). The match making, completely illogical,if you play good,game will give you bad teammates expecting you to carry and if you play bad,game will give you more bad teammates saying that it's so called "skill based matching". The only thing game will provide you is waste of time and energy

| | labels |
|---|---|
| gold | `P_IllusionOfControl` |
| pred | `P_IllusionOfControl`, `S_Competition` |
| **spurious** | `S_Competition` |

**Model analysis**

```
The review describes competitive matchmaking against other players and alleges that matchmaking intentionally assigns bad teammates based on the player's performance, which fits Illusion of Control because the outcome-determination system is portrayed as manipulated under a hidden skill-based rule. General anger, claims that the game wants money, copying another game, and wasting time or energy do not describe codable mechanics under R2; no specific payment route, repetitive task, timer, or resource mechanic is identified.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "if you play good,game will give you bad teammates expecting you to carry and if you play bad,game will give you more bad teammates saying that it's so called "skill based matching""
  - why: The span alleges that matchmaking outcomes are deliberately tuned according to the player's performance through a concealed or misleading skill-based system.
- `S_Competition` - **SPURIOUS**
  - span: "The match making, completely illogical"
  - why: Matchmaking describes the game placing players into matches involving competition against other players.

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
The review describes spending time “grinding,” which names repetitive gameplay activity but does not explicitly state that it was required for progress; this is still the reviewer’s direct mechanic description and is the only candidate label supported. Chatting with friends does not show social obligation, recruitment, or resource exchange. Losing progress and money after a ban describes forfeited investment, but not reluctance to leave or a cost imposed by quitting, so P_EasyToGetHardToLose is rejected under its boundary rule. Automated moderation, censorship, and an unexplained ban do not match a listed mechanic label.
```

**Labels assigned**

- `T_Grinding` - **SPURIOUS**
  - span: "I mainly spent time grinding"
  - why: The span explicitly identifies grinding as the repetitive gameplay activity the reviewer spent time performing.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `61c9847d-6625-4f03-857c-eae510d042a4` - RAID: Shadow Legends

> It's very grindy but the graphics are actually nice. The game play is different from some of the ads. Is a turn based multistage battle game item customization. There is a lot of characters to choose from and to get all you would need to upgrade your storage many times. One commercial shows people changing the characters appearance I have not seen that but maybe, I did start playing a week ago and I am still playing. I think it's a good game to spend extra time while doing other things.

| | labels |
|---|---|
| gold | `M_WasteAversion` |
| pred | `M_WasteAversion`, `P_CompleteTheCollection` |
| **spurious** | `P_CompleteTheCollection` |

**Model analysis**

```
The review mentions collecting many characters and needing repeated storage upgrades to obtain them all, which describes a collection-completion mechanic and storage capacity friction. I considered T_Grinding, but "very grindy" is a general evaluation without naming a repetitive activity tied to progress, so it is rejected under the Grinding boundary rule. The comments about advertisements are out-of-game marketing and are excluded by R13. No payment, random chance, or loss-on-exit mechanic is described.
```

**Labels assigned**

- `M_WasteAversion` - ok
  - span: "to get all you would need to upgrade your storage many times"
  - why: The span describes storage-capacity friction requiring repeated inventory upgrades to hold or obtain the collection.
- `P_CompleteTheCollection` - **SPURIOUS**
  - span: "There is a lot of characters to choose from and to get all"
  - why: The span describes the goal of acquiring all available characters.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `S_Competition` | 5 | 1 |
| `M_PayToProgress` | 6 | 0 |
| `M_Gambling` | 3 | 2 |
| `P_RewardMania` | 4 | 0 |
| `T_Grinding` | 2 | 1 |
| `P_CompleteTheCollection` | 1 | 1 |
| `T_InfiniteTreadmill` | 2 | 0 |
| `M_UIMisdirection` | 2 | 0 |
| `P_IllusionOfControl` | 1 | 0 |
| `T_Advertisement` | 1 | 0 |
| `M_IntermediateCurrency` | 1 | 0 |
| `M_RecurringFee` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `M_NeverEndingLure` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `T_DailyRewards` | 1 | 0 |
| `M_EasyToPurchase` | 1 | 0 |
| `P_AestheticManipulation` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `S_EncouragesAntiSocialBehavior` | 1 | 0 |

