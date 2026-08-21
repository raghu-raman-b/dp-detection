# Error review - gpt-5.6-luna_low_20260821-131310

`gpt-5.6-luna` / reasoning `low` / search `True`  
prompt `../outputs/prompts/teacher_v1.txt` sha `519268bfa1e4`  
micro-F1 **0.775** (P 0.954 / R 0.653) - **24 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 6 | said NONE, gold had labels |
| SWAP | 2 | picked different labels than gold |
| MISSED ONLY | 15 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 1 | found all gold, added extras |

## The diagnostic that matters

Of **33** missed labels, **12** (36%) were named in the model's own analysis and dropped anyway; **21** (64%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `M_PayToProgress` | 4 | 2 |
| `P_RewardMania` | 1 | 2 |
| `P_IllusionOfControl` | 1 | 1 |
| `M_Gambling` | 1 | 1 |
| `S_Competition` | 1 | 1 |
| `M_UIMisdirection` | 0 | 2 |
| `T_Grinding` | 1 | 1 |
| `P_AestheticManipulation` | 0 | 1 |
| `M_IntermediateCurrency` | 0 | 1 |
| `S_FriendSpamImpersonation` | 0 | 1 |
| `M_NeverEndingLure` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `P_CompleteTheCollection` | 0 | 1 |
| `M_EasyToPurchase` | 1 | 0 |
| `M_RecurringFee` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `S_EncouragesAntiSocialBehavior` | 0 | 1 |
| `T_Advertisement` | 1 | 0 |
| `M_WasteAversion` | 0 | 1 |
| `T_InfiniteTreadmill` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |

## Missed everything (predicted NONE) (6)

### `fd1230ab-7d12-4aeb-a425-e37ed06bcd5c` - Pokémon GO

> I love this game, just started playing about 2 months ago. Though I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way. I feel taken advantage of. 3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| pred | _NONE_ |
| **missed** | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |

**Did the model consider what it missed?**

- `P_IllusionOfControl` - never mentioned -> **attention / recall**
- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**
- `S_FriendSpamImpersonation` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes purchasing Poké Balls and consuming them faster because Pokémon break out, but it does not clearly state that payment is required for progress or continued play. Poké Balls are items rather than intermediate currency, and there is no realised stranded value, explicit rigging mechanism, or codable social mechanic. The later statement retracts the claim about talking to other players, so it does not establish Reciprocity or Forced Fellowship. Under R2, R3, and R6, no label applies.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

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
The review attributes the loss of power and failure to gain points to a game full of “bugs and glitches,” so R11 suppresses coding those behaviors. The statements about wasted time and money are evaluations, not mechanics. No other clear mechanic is described: repeated upgrades and building are mentioned, but not as a required repetitive progression activity independent of the reported malfunction, so T_Grinding is rejected under R2 and R11.
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

- `M_PayToProgress` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes that real-money spending helps but is not necessary, which is a monetization-related statement, but it does not say payment is required for progress, advantage, or continued play. The stuck scene is described as a problem, so it is a technical malfunction and is suppressed by R11. No other codable game mechanics are described.
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

- `S_Competition` - considered and rejected -> **rule interpretation**
- `S_EncouragesAntiSocialBehavior` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a request for a new forfeiture rule and says some players avoid starting the game, but it does not describe an existing game mechanic that fits a label. Competition was considered but rejected because merely referring to players and an unsporting tactic does not describe the game making players compete; Encourages Anti-Social Behavior was rejected because no harmful action is shown as rewarded or incentivized. Under R12, the requested rule is not codable.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `6ccb26a7-01e3-41a3-ba1a-bddba2063257` - Lightning Link Casino Slots

> Dont even waste you time with this app. I dont understand why you guys make these things so fun to play but impossible to ever win. I mean I know your trying to make money on the app but why would I ever come back and spend more money when it is impossible to when. Because of that this app is garbage!!!!!!!

| | labels |
|---|---|
| gold | `M_PayToProgress` |
| pred | _NONE_ |
| **missed** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_PayToProgress` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes dissatisfaction with losing and says the player might spend more money, but it does not describe a specific wagering, chance-based, purchase-gated progress, or reward-delivery mechanic. Gambling is rejected because no wager or luck mechanic is explicitly described in the review; Pay to Progress is rejected because spending is not stated to enable progress; Illusion of Control is rejected because no rigging or concealed-outcome mechanism is identified. Under R2, the general claim that winning is impossible is insufficient.
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

- `M_UIMisdirection` - never mentioned -> **attention / recall**
- `S_Competition` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes extra pop-up screens, including a quit-confirmation screen that must be dismissed before continuing, but it does not connect these screens to a purchase or spending option. UI Misdirection is therefore rejected under its monetary boundary rule. The increased cost is mentioned without describing a purchase mechanic, so no monetary label applies. No other codable mechanic is present.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (2)

### `176aaa1f-d8f9-4a1a-9f29-64902f13be5c` - All in Hole: Black Hole Games

> I would give 5 stars, but I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used.🤨😒🙄😥

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `T_MandatoryMarathon` |
| pred | `P_EasyToGetHardToLose`, `T_MandatoryMarathon` |
| **missed** | `M_IntermediateCurrency` |
| **spurious** | `P_EasyToGetHardToLose` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes accumulated bag contents and coins being lost after leaving and returning to the game. This supports T_MandatoryMarathon because stopping the session results in forfeiting held progress, and P_EasyToGetHardToLose because leaving carries the cost of losing accumulated value. M_WasteAversion was considered but rejected under its boundary rule: the review does not describe a finite capacity forcing destruction, an unusable currency remainder, or a purchase shortfall. No bug or technical-fault attribution is present, so R11 does not suppress the labels.
```

**Labels assigned**

- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used"
  - why: Accumulated items and coins are forfeited after leaving, making disengagement costly.
- `T_MandatoryMarathon` - ok
  - span: "I leave the game with my bag full only to come back with it empty"
  - why: The player loses accumulated holdings when ending and later resuming a session, indicating that stopping forfeits progress.

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

- `M_WasteAversion` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes wanting to obtain all characters and needing repeated storage upgrades to do so, which supports Complete the Collection. The general statement "very grindy" does not identify a repetitive task tied to progress, so T_Grinding is rejected under the Grinding boundary rule. The comments about ads showing different gameplay concern third-party marketing, not in-game design, so T_Advertisement and related labels are rejected under R13. No other described mechanic satisfies the codebook.
```

**Labels assigned**

- `P_CompleteTheCollection` - **SPURIOUS**
  - span: "There is a lot of characters to choose from and to get all"
  - why: The span describes acquiring all available characters, matching the compulsion to complete an in-game collection.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (15)

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
The review describes repetitive investment in progression through "grinding," and states that a new update makes previously achieved progress less valuable by giving new players equivalent hero-equipment progress for free; this supports T_Grinding and M_PowerCreep. It also describes purchasing gold and event passes, but does not clearly state that payment is required to progress, that gold is bought with real money as an intermediate currency, or that a recurring pass is being maximized for value, so M_PayToProgress, M_IntermediateCurrency, and M_RecurringFee are rejected under R2 and R4. Playing every day is not described as a daily reward or schedule mechanic, so no temporal appointment label applies.
```

**Labels assigned**

- `M_PowerCreep` - ok
  - span: "Supercell just released an update that invalidates most of the progress I achieved. New players get my current level of hero equipment progress for free, and can easily overtake me"
  - why: The update and free access for new players devalue progress the reviewer had already acquired.
- `T_Grinding` - ok
  - span: "After a year of grinding"
  - why: The reviewer explicitly describes prolonged grinding as the activity invested in progression.

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
The review describes real money being exchanged for in-game coins, so M_IntermediateCurrency applies. It also describes losing those coins in one round because the dealt cards were not needed, but this does not clearly establish a chance-based monetary wager or a reward-delivery mechanic; therefore M_Gambling, P_RewardMania, and M_WasteAversion are rejected under R2 and their boundary rules. The complaints about poor prize value and high prices alone do not trigger additional labels.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "20$ for only 100k or so coins"
  - why: The span describes paying real money to acquire in-game coins.

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
The review describes requesting a resource from a clan, which satisfies Reciprocity. It also describes misleading promotional wording that makes the player expect a larger coin reward, which satisfies Aesthetic Manipulation because the deception is in the wording. I considered UI Misdirection for the control changing to a higher value, but the review does not clearly connect that interface behavior to a purchase or monetary opt-out, so it is rejected under the label boundary rule. Intermediate Currency, Gambling, and Easy to Purchase are not assigned because no real-money conversion, wager, or purchase-friction mechanism is clearly described.
```

**Labels assigned**

- `P_AestheticManipulation` - ok
  - span: "The wording makes you think you are going to get more than you think."
  - why: The promotional wording is described as misleading the player about the reward they would receive.
- `S_Reciprocity` - ok
  - span: "easier to ask our clan for a stamp"
  - why: The player describes asking clan members for an in-game resource, which is a resource-transfer or favor-exchange mechanic.

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
The review describes repeated purchase prompts appearing when the player runs out of rolls: "request to purchase rolls" and "every time we are out of rolls." This is a purchase solicitation triggered by depleted resources and interrupting continued play, satisfying M_EasyToPurchase under the Prompted to Buy indicator. Advertisement is rejected because no in-game ad viewing or ad reward is described. M_PayToProgress is rejected because the review does not explicitly connect purchasing rolls to progressing through the game.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "they inundate you with request to purchase rolls. We can easily see what offers there are we don't need 6+ thrown at us every time we are out of rolls"
  - why: Purchase offers are repeatedly displayed when the player runs out of rolls, prompting payment at the point of insufficient resources.

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
The review describes a gacha mechanic through "the gatcha," which satisfies Reward Mania's gacha-mechanics indicator. It explicitly says the game does not use power creep, so M_PowerCreep is rejected under R12 because absent mechanics are not codable. No specific real-money chance stake is clearly described, so M_Gambling is rejected.
```

**Labels assigned**

- `P_RewardMania` - ok
  - span: "the gatcha"
  - why: This names the game's gacha mechanic, an unpredictable reward-delivery system covered by Reward Mania.

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
The review describes collecting stickers to finish sets, so P_CompleteTheCollection applies. "always get duplicates" describes repeated unwanted reward drops, which satisfies P_RewardMania. "never lets you finish all the sets unless you pay" describes progress being contingent on payment, so M_PayToProgress applies. No search was needed because the mechanics are clear from the review.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: States that completing the sets is contingent on payment.
- `P_CompleteTheCollection` - ok
  - span: "getting stickers. always get duplicates. never lets you finish all the sets"
  - why: Describes pursuing completion of all sticker sets.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: Describes repeated unwanted drops in the reward system.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `62c6c0cf-e273-4b06-9506-cd81de13d2f5` - Moba Legends: 5v5!

> only if you invest some money in the game will the teammates will be good otherwise the game will select the worst ones for you and put them in your team. all bots will be in ur team no matter your rank. everyone will just play solo and then blame you for the loss. useless teammates with no skill and only give excuses of network.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `P_IllusionOfControl`, `S_Competition` |
| pred | `M_PayToProgress`, `S_Competition` |
| **missed** | `P_IllusionOfControl` |

**Did the model consider what it missed?**

- `P_IllusionOfControl` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes spending money as a route to receiving better teammates, while non-paying players are assigned worse teammates and bots. This supports M_PayToProgress because payment grants an in-game competitive advantage, and S_Competition because the mechanic concerns ranked/team matches and winning or losing against other players. P_IllusionOfControl was considered but rejected: although the reviewer alleges biased teammate selection, the span does not clearly describe the game deceiving players about their skill or hiding outcome information. S_EncouragesAntiSocialBehavior was rejected because blaming teammates is player behavior, not a game incentive for harmful conduct.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "only if you invest some money in the game will the teammates will be good otherwise the game will select the worst ones for you"
  - why: Spending money is described as granting better teammates, an in-game advantage in competition.
- `S_Competition` - ok
  - span: "everyone will just play solo and then blame you for the loss"
  - why: The span describes team-based competitive play with wins and losses.

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
The review describes repeated near-miss outcomes and explicitly claims that games are rigged to induce spending. This supports P_IllusionOfControl because the reviewer alleges manipulated game outcomes. The repeated failures just short of winning support P_OptimismAndFrequencyBiases because they describe a clustering of near-successes. The constant purchase prompts do not establish M_EasyToPurchase under its boundary rule because no interception of play, insufficient-funds trigger, default purchase, or obstructed opt-out is described. M_PayToProgress is rejected because payment is not explicitly described as required to advance, and no Advertisement or Reward Mania mechanic is described.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "almost every game is rigged to make you spend"
  - why: The reviewer explicitly alleges that the game manipulates outcomes to induce spending.
- `P_OptimismAndFrequencyBiases` - ok
  - span: "a level is failed 1 or 2 moves from winning. 20 or 30 times in a row"
  - why: This describes repeated clustered near-wins, an instance of perceived frequent near-successes.

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
The review describes spending money as necessary to level up, which satisfies Pay to Progress. I considered Intermediate Currency, but the review does not clearly describe real money being converted into in-game currency. I rejected Competition because multiplayer or high-level advantages are not explicitly described as player-versus-player competition, and rejected Grinding because no repetitive progress activity is named.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Hope your rich, cause that the only way your gonna level up in the beginning."
  - why: The span describes real-world wealth or spending as the only route to leveling up.

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
The review describes an imposed 10-hour wait to replenish a full set of spins, which fits Playing by Appointment under the wait-time indicator. I considered Pay to Progress, but the review does not clearly state that purchasing spins is required to advance in the game; it only says the game wants spending and that bought spins provided no value. I rejected Intermediate Currency because spins are not described as currency purchased with real money, and Waste Aversion because no specific stranded balance or shortfall is described. The complaint about extra money taken is a transaction problem, not a game mechanic.
```

**Labels assigned**

- `T_PlayingByAppointment` - ok
  - span: "takes 10hrs just to get a full set of spins"
  - why: This describes an in-game wait imposed by the game before the player can replenish and use a full set of spins.

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

- `P_CompleteTheCollection` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a friend-invitation mechanic tied to rewards, which satisfies Forced Fellowship. It also describes wagering dice through “played max bet” with luck-based outcomes, supporting Gambling. Repeated duplicate stickers describe unpredictable or repeated reward delivery, supporting Reward Mania. The login failure is attributed to an internet connection error, so it is a malfunction and does not receive a label under R11. No Daily Rewards, Pay to Progress, Competition, or Friend Spam / Impersonation mechanic is clearly described.
```

**Labels assigned**

- `M_Gambling` - ok
  - span: "when I finally had more than 500 dices and played max bet, absolutely NO LUCK!"
  - why: The span describes staking dice in a maximum bet with luck determining the outcome.
- `P_RewardMania` - ok
  - span: "Stickers are duplicates all the way"
  - why: Repeated duplicate sticker rewards describe a variable or repeated reward-delivery mechanic.
- `S_ForcedFellowship` - ok
  - span: "no rewards for inviting friends and getting them to join facebook"
  - why: The game rewards players for recruiting friends to join, matching the Social Pyramid Scheme indicator.

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
The review describes a 30-day expiration schedule that causes collected cards to disappear and requires recollection, so T_PlayingByAppointment applies because the game's clock imposes a deadline and loss. It also describes a compulsion to obtain the full card set, supporting P_CompleteTheCollection. M_DeceptiveLuxury is rejected because the rarity and scarcity are not tied to price or purchase. S_Reciprocity is rejected because trading is mentioned without an obligation to reciprocate. P_EasyToGetHardToLose is rejected because the reviewer is uninstalling as the collection is about to be lost, rather than describing reluctance to leave due to accumulated investment. P_RewardMania is rejected because no random delivery or repeated-attempt reward mechanism is described.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "you lose all you have before getting the 162"
  - why: The span describes pursuing the complete set of 162 cards.
- `T_PlayingByAppointment` - ok
  - span: "all the cards you collect disappear after 30 days. So you have to collect them all over again"
  - why: A game-imposed 30-day expiry causes collected rewards to be lost and requires timely completion or recollection.

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
The review describes paid shields and paid upgrades as necessary for protection and competitive advantage, so M_PayToProgress applies. It also describes higher-level players attacking the reviewer, which establishes player-versus-player competition, so S_Competition applies. M_IntermediateCurrency is rejected because the review mentions gems but does not describe real money being converted into gems. M_RecurringFee is rejected because temporary shield duration is not a subscription or battle pass. S_EncouragesAntiSocialBehavior is rejected because harmful or unfair attacks are described, but no reward or incentive for the aggressor is stated. T_PlayingByAppointment is rejected because shield duration alone does not require the player to play at specific times.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "If you're not willing to pay for upgrades, then this game's not for you."
  - why: The span describes payment as necessary to continue progressing or competing effectively.
- `S_Competition` - ok
  - span: "Players with higher levels will turn you into a punching bag."
  - why: The span describes players competing against and attacking one another.

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
The review describes a large monetary requirement to play and accumulated time investment making players reluctant to leave. I considered M_PayToProgress for "Unless you have 50-100k to throw into the game," but the span does not explicitly tie payment to progress, continued play, or overcoming an in-game obstacle, so R2 and the Pay to Progress definition do not support assigning it. The final statement directly describes investment making departure difficult, satisfying P_EasyToGetHardToLose. The claimed stealing of earned items is not assigned because it describes loss, not a mechanic that raises the cost of leaving. No other candidate label is supported.
```

**Labels assigned**

- `P_EasyToGetHardToLose` - ok
  - span: "most are too invested to leave"
  - why: The reviewer says accumulated investment makes players reluctant or unable to abandon the game.

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
The review describes an in-game advertisement screen with no close control and taps redirected to the store, satisfying UI Misdirection because the interface obstructs opting out. T_Advertisement was considered but rejected under R2 because the review says the player saw ads without explicitly describing forced viewing or reward-based viewing. T_MandatoryMarathon was rejected because no gameplay progress or session value is forfeited when exiting.
```

**Labels assigned**

- `M_UIMisdirection` - ok
  - span: "there is no way to close it. No cross mark on the screen , if you try to click anywhere on the screen it takes you to store."
  - why: The ad interface obstructs dismissal and redirects taps toward the store instead of providing a normal opt-out.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (1)

### `a12fb168-3791-4d93-8cee-9b38fceb3059` - Moba Legends: 5v5!

> If you want to get some serious anger issues and frustration,the game is for you.This game simply don't care about you at all,they only need money and frame(Obv it's a complete copy of league of legends). The match making, completely illogical,if you play good,game will give you bad teammates expecting you to carry and if you play bad,game will give you more bad teammates saying that it's so called "skill based matching". The only thing game will provide you is waste of time and energy

| | labels |
|---|---|
| gold | `P_IllusionOfControl` |
| pred | `P_IllusionOfControl`, `S_Competition` |
| **spurious** | `S_Competition` |

**Model analysis**

```
The review describes matchmaking that allegedly assigns teammates according to a hidden and illogical rule, which fits Illusion of Control because the game presents this as skill-based matching while manipulating matchmaking outcomes. Matchmaking also describes multiplayer competition, so Competition applies. I rejected Pay to Progress because 'they only need money' does not describe payment being required for progress, and rejected Grinding because 'waste of time and energy' is a general evaluation without a repetitive progress activity.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "The match making, completely illogical,if you play good,game will give you bad teammates expecting you to carry and if you play bad,game will give you more bad teammates saying that it's so called "skill based matching""
  - why: The span describes matchmaking being tuned by a hidden or misleading rule, making the purported skill-based outcome deceptive.
- `S_Competition` - **SPURIOUS**
  - span: "The match making"
  - why: Matchmaking with teammates describes the game's player-versus-player competitive structure.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_PayToProgress` | 6 | 0 |
| `P_RewardMania` | 3 | 0 |
| `S_Competition` | 2 | 1 |
| `P_IllusionOfControl` | 2 | 0 |
| `P_CompleteTheCollection` | 1 | 1 |
| `M_Gambling` | 2 | 0 |
| `M_UIMisdirection` | 2 | 0 |
| `T_Grinding` | 2 | 0 |
| `P_AestheticManipulation` | 1 | 0 |
| `M_IntermediateCurrency` | 1 | 0 |
| `S_FriendSpamImpersonation` | 1 | 0 |
| `M_NeverEndingLure` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `M_RecurringFee` | 1 | 0 |
| `M_EasyToPurchase` | 1 | 0 |
| `S_EncouragesAntiSocialBehavior` | 1 | 0 |
| `T_Advertisement` | 1 | 0 |
| `M_WasteAversion` | 1 | 0 |
| `T_InfiniteTreadmill` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `P_EasyToGetHardToLose` | 0 | 1 |

