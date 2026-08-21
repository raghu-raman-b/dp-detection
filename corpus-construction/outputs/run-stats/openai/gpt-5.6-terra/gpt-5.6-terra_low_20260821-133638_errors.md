# Error review - gpt-5.6-terra_low_20260821-133638

`gpt-5.6-terra` / reasoning `low` / search `True`  
prompt `../outputs/prompts/teacher_v1.txt` sha `519268bfa1e4`  
micro-F1 **0.833** (P 0.959 / R 0.737) - **21 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 5 | said NONE, gold had labels |
| SWAP | 2 | picked different labels than gold |
| MISSED ONLY | 13 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 1 | found all gold, added extras |

## The diagnostic that matters

Of **25** missed labels, **14** (56%) were named in the model's own analysis and dropped anyway; **11** (44%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `M_PayToProgress` | 4 | 1 |
| `S_Competition` | 2 | 1 |
| `M_UIMisdirection` | 0 | 2 |
| `P_RewardMania` | 1 | 1 |
| `M_EasyToPurchase` | 1 | 0 |
| `M_WasteAversion` | 1 | 0 |
| `T_InfiniteTreadmill` | 0 | 1 |
| `M_NeverEndingLure` | 0 | 1 |
| `Tech_FragmentedDownloads` | 1 | 0 |
| `S_EncouragesAntiSocialBehavior` | 1 | 0 |
| `M_IntermediateCurrency` | 0 | 1 |
| `T_Grinding` | 1 | 0 |
| `P_CompleteTheCollection` | 0 | 1 |
| `M_Gambling` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `M_PowerCreep` | 1 | 0 |
| `T_PlayingByAppointment` | 0 | 1 |

## Missed everything (predicted NONE) (5)

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
The review describes lost power and failure to gain points after upgrades/building, but it explicitly attributes the relevant behavior to "bugs and glitches." Under R11, behavior attributed to a technical fault is not coded as a dark-pattern mechanic. Grinding was considered because the reviewer mentions upgrades and building, but no repetitive task cycle required for progress is described, and the stated lack of progress is within the bug complaint.
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
- `S_EncouragesAntiSocialBehavior` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes players passing or not starting a match to avoid risk, and suggests an automatic-forfeit rule. It does not describe the game rewarding, incentivizing, or requiring this unsporting conduct, so S_EncouragesAntiSocialBehavior is rejected under the permitted-harm/incentive boundary. No other mechanic in the codebook is described as present; the forfeit rule is only a requested change and is not codable under R12.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a4d925c0-1248-4d12-ad93-5b8b1ced3b8d` - Shadow Fight 4: Arena

> This is probably the first fighting game I liked in my opinion I like the characters the moves but the downloading system sucks I thought I already download the file but I still get an additional download and when that happens the matchmaking is broken it doesn't works anymore cause there's a problem on my wifi but my wifi is good pls fix this😿

| | labels |
|---|---|
| gold | `Tech_FragmentedDownloads` |
| pred | _NONE_ |
| **missed** | `Tech_FragmentedDownloads` |

**Did the model consider what it missed?**

- `Tech_FragmentedDownloads` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes an additional in-game download after the initial file download: "I thought I already download the file but I still get an additional download." This could be Fragmented Downloads if the additional download is mandatory and obscures the true storage requirement, but the span does not say it blocks progress, reveals unexpectedly large storage use, or causes missing assets when declined. The matchmaking problem is attributed to a technical issue and Wi‑Fi, not a designed time gate, so Playing by Appointment does not apply under R11 and the scheduling boundary rule.
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
The reviewer says the app is "impossible to ever win" and mentions potentially "spend[ing] more money," but does not describe a specific in-game mechanic showing a paid wager, chance-based reward delivery, a purchase that enables progress, or a manipulated outcome rule. The supplied game title cannot substitute for a mechanic described in the review (R4). Gambling, Reward Mania, Pay to Progress, and Illusion of Control were considered but rejected because the review only gives general dissatisfaction with losing and monetization.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `61c9847d-6625-4f03-857c-eae510d042a4` - RAID: Shadow Legends

> It's very grindy but the graphics are actually nice. The game play is different from some of the ads. Is a turn based multistage battle game item customization. There is a lot of characters to choose from and to get all you would need to upgrade your storage many times. One commercial shows people changing the characters appearance I have not seen that but maybe, I did start playing a week ago and I am still playing. I think it's a good game to spend extra time while doing other things.

| | labels |
|---|---|
| gold | `M_WasteAversion` |
| pred | _NONE_ |
| **missed** | `M_WasteAversion` |

**Did the model consider what it missed?**

- `M_WasteAversion` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer explicitly describes the game as "very grindy," but does not identify a repetitive task performed to make progress, so Grinding is rejected under its gameplay-described-as-repetitive boundary rule. They mention needing to "upgrade your storage," but describe neither a capacity-forced forfeit nor payment for capacity, so Waste Aversion and Pay to Progress are rejected. The comments about commercials and ads concern external advertising/misrepresented gameplay rather than ads encountered inside the installed game, so Advertisement is rejected under R13. No other described mechanic satisfies a label.
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
The review describes resources being forfeited after the player leaves and returns: a full bag becomes empty, and earned and purchased coins are used. This supports Mandatory Marathon because ending play causes loss of accumulated session value. It also supports Easy to Get, Hard to Lose because leaving entails forfeiting value already held. Waste Aversion is rejected because no pack-size, price-gap, capacity, or stranded-currency mechanism is described. No bug or glitch attribution is attached to this loss.
```

**Labels assigned**

- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used."
  - why: The span describes exit entailing the loss of value the player had already accumulated or purchased.
- `T_MandatoryMarathon` - ok
  - span: "I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used."
  - why: Leaving the game results in forfeiture of accumulated bag contents and coins, so the player cannot stop without losing progress/value.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `ca58ab5e-d48a-4825-9466-c658f4181913` - Candy Crush Saga

> Wow what an awful experience. From the constant prompts to purchase powerups to the way it feels like almost every game is rigged to make you spend. It seems this game stopped being about fun a long time ago. I recently started as a new player. Made it to level 250 so I tried to give it an honest chance. It seems way to convenient that a level is failed 1 or 2 moves from winning. 20 or 30 times in a row. Before you get lucky enough to win. Nah. Uninstalled not coming back. Would not recommend.

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `T_Grinding` |
| pred | `M_PayToProgress`, `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `T_Grinding` |
| **missed** | `M_EasyToPurchase` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes alleged hidden manipulation of level outcomes: games are "rigged to make you spend" and levels repeatedly fail one or two moves short of completion. That supports Illusion of Control, and the repeated near-wins also describe a frequency/near-miss perception supporting Optimism and Frequency Biases. Repeating a level 20 or 30 times to win is a named repetitive activity tied to progression, so Grinding applies. Pay to Progress is also supported because the alleged rigging is explicitly described as designed "to make you spend," making payment the route around the obstacle. I considered Easy to Purchase for the purchase prompts, but "constant prompts" alone does not show that they intercept play, appear upon insufficient funds, or reduce purchase friction under the boundary rule.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "almost every game is rigged to make you spend"
  - why: The reviewer describes payment as the intended way past manipulated level difficulty.
- `P_IllusionOfControl` - ok
  - span: "almost every game is rigged to make you spend"
  - why: The reviewer alleges the game secretly determines outcomes to drive continued play and spending.
- `P_OptimismAndFrequencyBiases` - ok
  - span: "a level is failed 1 or 2 moves from winning. 20 or 30 times in a row."
  - why: The span describes repeated near-wins and their perceived frequency.
- `T_Grinding` - ok
  - span: "a level is failed 1 or 2 moves from winning. 20 or 30 times in a row. Before you get lucky enough to win."
  - why: This describes repeated level attempts required before progression.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (13)

### `fd1230ab-7d12-4aeb-a425-e37ed06bcd5c` - Pokémon GO

> I love this game, just started playing about 2 months ago. Though I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way. I feel taken advantage of. 3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| pred | `P_IllusionOfControl`, `S_FriendSpamImpersonation` |
| **missed** | `P_OptimismAndFrequencyBiases` |

**Did the model consider what it missed?**

- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes Pokémon repeatedly escaping from purchased Poké Balls, which the reviewer links to needing to buy more; this is an allegation that capture outcomes are being manipulated to induce further spending, satisfying Illusion of Control. It does not clearly establish real-money conversion into an in-game currency, a paid progress gate, or a chance-based paid wager, so Intermediate Currency, Pay to Progress, and Gambling are rejected. The edited portion says a review was posted despite the player not writing it, which describes content published under the player’s identity and satisfies Friend Spam / Impersonation.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "they keep breaking out so I go through the balls faster so I have to purchase more."
  - why: This alleges capture outcomes are being tuned to make the player buy more items.
- `S_FriendSpamImpersonation` - ok
  - span: "I DID NOT WRITE THIS REVIEW"
  - why: The reviewer states that a review was posted under their identity without their authorship.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fd9e64df-55b4-47f7-a338-8b6bce4df1be` - Mech Arena - Shooting Game

> use to love playing this game. been playing for years. they keep making changes and after each change, my robots get weaker and weaker. it's too the point where, even if you spend money, you're not going to win long. they'll make a change or over night, the algorithm will put you against real players that are way over powered for you to fight. I hate to say it, I think I'm going to delete this game. it has become a scam unless you're willing to dump thousands into it and max out every option.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_PowerCreep`, `P_IllusionOfControl`, `S_Competition` |
| pred | `M_PayToProgress`, `P_IllusionOfControl`, `S_Competition` |
| **missed** | `M_PowerCreep` |

**Did the model consider what it missed?**

- `M_PowerCreep` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes monetized advantage, player-versus-player matchmaking, and an alleged hidden algorithm that places the reviewer against stronger opponents. Pay to Progress applies because spending thousands and maxing options is presented as necessary to remain viable; Competition applies because the game matches the player against other real players; Illusion of Control applies because the reviewer attributes unfair matchups to an algorithm. Power Creep was considered from robots becoming weaker after changes, but rejected because the review does not state that the weakened robots were purchased items.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "it has become a scam unless you're willing to dump thousands into it and max out every option."
  - why: This presents spending large amounts of money as necessary to obtain sufficient in-game advantage.
- `P_IllusionOfControl` - ok
  - span: "the algorithm will put you against real players that are way over powered for you to fight."
  - why: This alleges that a hidden algorithm determines unfair competitive outcomes through matchmaking.
- `S_Competition` - ok
  - span: "the algorithm will put you against real players that are way over powered for you to fight."
  - why: This describes being matched to compete against other real players.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `432d7a64-e295-4aed-bb30-8ae44f9ddd45` - Disney Solitaire

> games alright but the prizes are wack when you beat a level, and the in-game purchase even more wack , prizes needa be better, and less expensive, I don't mind putting $1 or 2$ but 20$ for only 100k or so coins to lose in one round because the cards are not the one you need, do better disney

| | labels |
|---|---|
| gold | `M_Gambling`, `M_IntermediateCurrency`, `M_PayToProgress` |
| pred | `M_Gambling`, `M_IntermediateCurrency` |
| **missed** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_PayToProgress` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes real money being exchanged for in-game coins, then those coins being risked in a round whose outcome depends on receiving needed cards; beating levels yields prizes. This supports Intermediate Currency and Gambling. Pay to Progress was considered but rejected because the payment is described as a stake lost within the chance-based round, not as a purchase that bypasses a separate progression obstacle. Waste Aversion was rejected because no stranded balance, inventory forfeit, or specific shortfall is described.
```

**Labels assigned**

- `M_Gambling` - ok
  - span: "20$ for only 100k or so coins to lose in one round because the cards are not the one you need"
  - why: Purchased coins are risked in a round with a chance-based card outcome and level prizes.
- `M_IntermediateCurrency` - ok
  - span: "20$ for only 100k or so coins"
  - why: This explicitly describes spending real money to acquire in-game coins.

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
The reviewer describes a clan resource-request feature: "ask our clan for a stamp," which is a request for an in-game resource among existing players and satisfies Reciprocity. The reviewer also describes deceptive promotional wording that led them to expect a larger coin reward but receive only 20%, which fits Aesthetic Manipulation's misleading text/wording indicator. I considered UI Misdirection for the controls that "changes it to higher," but the span does not connect the higher setting to a real-money purchase or an obstructed purchase opt-out, so it does not satisfy the monetary UI rule. A big win and a Spin button do not by themselves establish a codable variable-reward or monetary-wager mechanic under the review text alone.
```

**Labels assigned**

- `P_AestheticManipulation` - ok
  - span: "Beware of the wording on promotions with extra coins.The wording makes you think you are going to get more than you think."
  - why: This describes misleading promotional text influencing the player's expectation of the reward.
- `S_Reciprocity` - ok
  - span: "now is easier to ask our clan for a stamp."
  - why: This describes asking existing clan members for an in-game resource.

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
The review describes repeated purchase requests that appear specifically when the player has exhausted rolls: "every time we are out of rolls." This is a purchase prompt intercepting a spent-resource state, satisfying Easy to Purchase under the Prompted to Buy boundary rule. It does not describe payment as necessary to progress, only that offers are repeatedly shown, so Pay to Progress is not assigned. No ad viewing, timer, or other mechanic is described.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "they inundate you with request to purchase rolls. We can easily see what offers there are we don't need 6+ thrown at us every time we are out of rolls."
  - why: Repeated purchase offers are thrown at the player when rolls are depleted, a spent-resource purchase prompt that intercepts play.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `62c6c0cf-e273-4b06-9506-cd81de13d2f5` - Moba Legends: 5v5!

> only if you invest some money in the game will the teammates will be good otherwise the game will select the worst ones for you and put them in your team. all bots will be in ur team no matter your rank. everyone will just play solo and then blame you for the loss. useless teammates with no skill and only give excuses of network.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `P_IllusionOfControl`, `S_Competition` |
| pred | `P_IllusionOfControl` |
| **missed** | `M_PayToProgress`, `S_Competition` |

**Did the model consider what it missed?**

- `M_PayToProgress` - never mentioned -> **attention / recall**
- `S_Competition` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes alleged matchmaking manipulation: the game supposedly selects weak teammates and bots for the reviewer regardless of rank. This satisfies Illusion of Control because it asserts outcomes are determined by a concealed, biased matchmaking rule. Competition was considered, but the span does not explicitly describe competing against other players; complaints about teammates alone do not establish that label. Anti-Social Behavior was rejected because blaming teammates is player conduct without a stated in-game incentive.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "otherwise the game will select the worst ones for you and put them in your team. all bots will be in ur team no matter your rank."
  - why: This alleges the game secretly manipulates matchmaking outcomes by assigning weak teammates and bots regardless of rank.

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
The review describes progression being contingent on spending money: new players allegedly cannot level up without being rich. It also says upgrades become slower as spending increases, but does not describe repetitive tasks, a purchasable in-game currency, chance-based rewards, a specific purchase interface, or older purchased items losing value after acquisition. High-level players being favored does not itself describe direct player-versus-player competition.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Hope your rich, cause that the only way your gonna level up in the beginning."
  - why: This explicitly describes spending money as the only route to early-game leveling progress.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `5e6a5625-5291-4f0e-897c-1b63c1a26494` - MONOPOLY GO!

> I loved this game until the new season started. Suddenly I get no rewards for inviting friends and getting them to join facebook. I am struggling to get dices and when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way... And today. Well, I cannot log in to the game at all. It keeps giving me an internet connection error which is absolute nonsense. I have connected to 3 different wifi connections. BS!!😡

| | labels |
|---|---|
| gold | `M_Gambling`, `P_CompleteTheCollection`, `P_RewardMania`, `S_ForcedFellowship` |
| pred | `P_RewardMania`, `S_ForcedFellowship` |
| **missed** | `M_Gambling`, `P_CompleteTheCollection` |

**Did the model consider what it missed?**

- `M_Gambling` - considered and rejected -> **rule interpretation**
- `P_CompleteTheCollection` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a recruitment reward tied to getting friends to join Facebook, which fits Forced Fellowship. It also describes dice rolls producing variable outcomes—no Shutdowns or Bank Heists—and sticker rewards yielding duplicates; the search established that Shutdown/Bank Heist are outcomes triggered by board movement and sticker packs yield random stickers, so this is Reward Mania. The inability to log in is explicitly attributed to an internet connection error, a technical fault, so it does not code any design pattern under R11. No payment, purchase, or stake is described, so Gambling, Pay to Progress, and Intermediate Currency are rejected.
```

**Labels assigned**

- `P_RewardMania` - ok
  - span: "when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way..."
  - why: This describes repeated play producing variable reward outcomes and duplicate drops from a randomized reward system.
- `S_ForcedFellowship` - ok
  - span: "I get no rewards for inviting friends and getting them to join facebook."
  - why: This describes rewards for recruiting new friends into the game.

**Search:** `MONOPOLY GO max bet shutdown bank heist stickers duplicate random rewards` -> The official MONOPOLY GO! help center established that landing on Railroad tiles initiates Shutdown or Bank Heist minigames; search results also established that sticker packs provide random stickers and can produce duplicates.

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
The review describes a 30-day expiry that removes collected cards and forces the player to rebuild the collection, which is a game-clock loss/return pressure and supports Playing by Appointment. It also explicitly describes the goal of obtaining all 162 cards, supporting Complete the Collection. The rare-card complaint does not establish a paid purchase, chance-based draw mechanism, or scarcity tied to a price, so Gambling, Reward Mania, and Deceptive Luxury are rejected. The Facebook trading-group comment does not describe an in-game resource-transfer mechanic, so Reciprocity is rejected.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "its hard enough getting all the cards as it is!!!"
  - why: The reviewer explicitly describes pursuing completion of the card collection.
- `T_PlayingByAppointment` - ok
  - span: "all the cards you collect disappear after 30 days. So you have to collect them all over again"
  - why: A game-set 30-day clock removes progress and requires the player to return and rebuild it.

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
The review describes paid upgrades as necessary for remaining viable against stronger players, which satisfies Pay to Progress. It also describes higher-level players attacking the reviewer, establishing player-versus-player competition. “Gems” are only named as the in-game means of payment for a shield; the review does not describe real money being converted into gems, so Intermediate Currency is rejected. The shield’s limited duration does not itself describe a required schedule, wait timer, or artificial scarcity.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "If you're not willing to pay for upgrades, then this game's not for you."
  - why: This describes payment for upgrades as necessary to remain able to play competitively.
- `S_Competition` - ok
  - span: "Players with higher levels will turn you into a punching bag."
  - why: This describes higher-level players competing against and repeatedly defeating weaker players.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `6877b6bf-e9e0-4c86-a196-e7c85a51529f` - Candy Crush Saga

> In the past I would have rated this game higher, but recent changes have result in too many pop up screens with weekly challenge score, and are you sure you want to quit screens that you have to X out of before continuing. It was a fun way to kill a few minutes on a break, but now it has so many screens to go through it has just become annoying. They have also increased the cost, so I will probably uninstall it all together. Too bad.

| | labels |
|---|---|
| gold | `M_UIMisdirection`, `S_Competition` |
| pred | `M_UIMisdirection` |
| **missed** | `S_Competition` |

**Did the model consider what it missed?**

- `S_Competition` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes repeated pop-up screens that must be dismissed before play can continue. This obstructs an opt-out/dismissal control and therefore fits UI Misdirection. The weekly challenge score is not described as requiring participation, giving rewards, or pressuring return, so Competition, Daily Rewards, Playing by Appointment, and FOMO are rejected. “Increased the cost” does not identify what is purchased or link payment to progression, so monetary labels are rejected.
```

**Labels assigned**

- `M_UIMisdirection` - ok
  - span: "pop up screens with weekly challenge score, and are you sure you want to quit screens that you have to X out of before continuing."
  - why: The interface presents screens the player must dismiss before continuing, obstructing the opt-out/dismissal path.

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
The review describes accumulated long-term investment making it difficult for players to quit: “most are too invested to leave.” This satisfies Easy to Get, Hard to Lose because invested value operates on the choice to leave. I considered Pay to Progress because it mentions spending money, but it does not describe payment as required to advance, bypass an obstacle, or gain a specified gameplay advantage. The claim that the game will “steal things” is not tied to a specified designed mechanic, and “gotten worse every year” does not establish purchased items losing value after acquisition, so Power Creep is not assigned.
```

**Labels assigned**

- `P_EasyToGetHardToLose` - ok
  - span: "most are too invested to leave"
  - why: This explicitly describes accumulated investment making players reluctant or unable to leave.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

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
The review describes in-game advertisements that cannot be closed and force the player to exit the app to escape them. This satisfies Advertisement because the player is compelled to view an ad. UI Misdirection is rejected because the obstructed opt-out is from an advertisement, not a purchase; Mandatory Marathon is rejected because no forfeiture of session progress from exiting is described.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "recently after seeing the ads, there is no way to close it."
  - why: The player describes being unable to dismiss an in-game advertisement, compelling ad viewing.

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
The review describes a matchmaking system that allegedly responds to performance by assigning bad teammates, which is a claim that outcomes are covertly tuned rather than determined transparently and satisfies Illusion of Control. It also describes team-based matchmaking, supporting Competition. “they only need money” is general monetization criticism without a stated purchase route to progress, so Pay to Progress is rejected under R2.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "if you play good,game will give you bad teammates expecting you to carry and if you play bad,game will give you more bad teammates saying that it's so called "skill based matching""
  - why: The reviewer alleges matchmaking is secretly manipulated according to performance while being presented as skill-based.
- `S_Competition` - **SPURIOUS**
  - span: "The match making, completely illogical"
  - why: This describes the game's player matchmaking in its team-based competitive play.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_PayToProgress` | 5 | 1 |
| `S_Competition` | 3 | 1 |
| `M_UIMisdirection` | 2 | 0 |
| `P_RewardMania` | 2 | 0 |
| `M_EasyToPurchase` | 1 | 0 |
| `M_WasteAversion` | 1 | 0 |
| `T_InfiniteTreadmill` | 1 | 0 |
| `M_NeverEndingLure` | 1 | 0 |
| `Tech_FragmentedDownloads` | 1 | 0 |
| `S_EncouragesAntiSocialBehavior` | 1 | 0 |
| `M_IntermediateCurrency` | 1 | 0 |
| `T_Grinding` | 1 | 0 |
| `P_CompleteTheCollection` | 1 | 0 |
| `M_Gambling` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `M_PowerCreep` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `P_EasyToGetHardToLose` | 0 | 1 |

