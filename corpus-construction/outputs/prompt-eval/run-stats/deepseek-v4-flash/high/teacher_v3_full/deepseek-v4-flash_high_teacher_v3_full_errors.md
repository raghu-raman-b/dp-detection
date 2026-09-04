# Error review - deepseek-v4-flash_high_teacher_v3_full

`deepseek-v4-flash` / reasoning `high` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v3_full.txt` sha `a6ae58246360`  
micro-F1 **0.538** (P 0.737 / R 0.424) - **16 of 30** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 9 | said NONE, gold had labels |
| SWAP | 2 | picked different labels than gold |
| MISSED ONLY | 3 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 2 | found all gold, added extras |

## The diagnostic that matters

Of **19** missed labels, **2** (11%) were named in the model's own analysis and dropped anyway; **17** (89%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `M_UIMisdirection` | 0 | 4 |
| `S_Reciprocity` | 0 | 2 |
| `P_RewardMania` | 0 | 2 |
| `M_EasyToPurchase` | 1 | 1 |
| `T_MandatoryMarathon` | 0 | 2 |
| `M_IntermediateCurrency` | 0 | 1 |
| `T_Grinding` | 0 | 1 |
| `S_Competition` | 0 | 1 |
| `M_NeverEndingLure` | 0 | 1 |
| `M_WasteAversion` | 1 | 0 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `T_Advertisement` | 0 | 1 |

## Missed everything (predicted NONE) (9)

### `ac5fc6a4-b597-46f3-af5a-3735b3854e26` - Gossip Harbor: Merge & Story

> I really wanted to like this game, however not even 10 minutes into playing it, it notified me that I bought a starter pack. I didn't tap anything and my settings are set up to where I have to input my fingerprint or password to make a purchase and it did not do that. Uninstalling ASAP. Not sure if it's just a glitch or what, but I'm not chancing that again.

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `M_NeverEndingLure` |
| pred | _NONE_ |
| **missed** | `M_EasyToPurchase`, `M_NeverEndingLure` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - never mentioned -> **attention / recall**
- `M_NeverEndingLure` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes being charged for a starter pack within minutes of installing, without tapping anything and without the fingerprint/password confirmation their device settings normally require. The review presents the event as an unexplained anomaly and explicitly raises the possibility that it was a glitch ('Not sure if it's just a glitch or what'). No designed mechanic is actually described: there is no purchase prompt, no default-to-buy interface, no confirmation-free checkout flow, and no misleading UI that reduced the friction of spending. The only described fact is an unauthorized charge, which the reviewer suspects may be a technical fault rather than a deliberate design choice. Under R11, an unwanted charge that the text attributes to a possible glitch is not codable as a dark pattern, because no underlying game rule is shown that would deliberately impose the purchase independent of the malfunction. Since the whole review concerns this single anomalous event, no other mechanic is present.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `47cb4d59-0121-40f1-9ffc-220c458bd581` - Seaside Escape®: Merge & Story

> After just over a week of play, game is now gridlocked. Way too many new things on a tiny board. Ridiculous. Update: they finally started "archiving" but expect you to use your inventory space for them??? Hello?!? DELETE. Lots of witchcraft in this game, from astral events to evil eyes that I just unlocked. Although different from the ad I thought I was getting, the merging is delightful. Not enough energy to last very long, and the gems slow down a lot when you slow down on unlocking new items.

| | labels |
|---|---|
| gold | `M_WasteAversion` |
| pred | _NONE_ |
| **missed** | `M_WasteAversion` |

**Did the model consider what it missed?**

- `M_WasteAversion` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review is a mixed evaluation after about a week of play. The concrete grievances are: (1) the board fills up too fast with too many introduced features, leaving the game 'gridlocked'; (2) archived items are pushed into inventory space rather than deleted, which the reviewer rejects; (3) energy does not last long, limiting session length; and (4) gem income drops off as the pace of unlocking new items slows. None of these mentions money being spent or offered, an actual wait/refill schedule, a daily-return incentive, or a specific forfeited value. The board/inventory complaints describe capacity pressure but do not show items destroyed, storage paid for, or a concrete shortfall realized, which the Waste Aversion boundary requires. The energy complaint describes scarcity of a resource but never states the regeneration wait or timer, which the Wait to Play boundary requires; it reads as a resource-capped session complaint, not a described appointment schedule. The gems comment is about an earning rate, not a real-money conversion. The review therefore does not carry any codable dark-pattern mechanic, only dissatisfaction with scarcity and pacing.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `991f5326-63fb-4951-8773-84050dd70912` - Candy Crush Soda Saga

> I just purchased a weekly one time offer that costs R79,99 and the transaction was successful from my bank account . But the offer is not there . What kind of a sick game is this ? I NEED MY REFUND !!!!!!

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury` |
| pred | _NONE_ |
| **missed** | `M_DeceptiveLuxury` |

**Did the model consider what it missed?**

- `M_DeceptiveLuxury` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a real-money purchase ('weekly one time offer', R79.99) that was debited from their bank account but never delivered in the game, and demands a refund. This is a complaint about a failed or buggy transaction - goods paid for but not received - not a description of any deliberate design mechanic. No span describes a game design behaviour: there is no friction-reducing purchase interface, no artificial scarcity attached to the offer, no recurring subscription mechanic being evaluated, no paywall, no disguised currency exchange. A nondelivered purchase is a transactional error or technical fault, which R11 excludes from dark-pattern labelling, and no underlying game rule that imposes a deliberate penalty is being described.
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
The reviewer describes two concrete grievances. First, pop-up screens — a weekly challenge score screen and an 'are you sure you want to quit' screen — that must be X'd out before play can continue. This is interface friction, but nothing in the span connects those screens to spending: they are not purchase offers, and the review gives no indication they direct attention to a buy option or obstruct an opt-out from one. Under the boundary rule, UI Misdirection lifts to the Monetary class, so attention-direction must bear on a purchase or an opt-out from one; this span does not. Second, the reviewer says the game has 'increased the cost,' a bare pricing complaint that names no mechanic such as pay-to-progress, a currency conversion, a pass, or a payment prompt. The rest is evaluation ('annoying,' 'too bad'), which codes NONE under R2.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `7732d254-0a39-4614-acf4-e67840e14b76` - Cashman Casino Slots Games

> loading takes entirely tooooo long also the bonus lady rarely comes out or even matches with anything on ww4. iv started playing a new game and buying coins from them.ill check inevery so offethen to see if it has changed . hopefully this rating will do it.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `P_RewardMania` |
| pred | _NONE_ |
| **missed** | `M_IntermediateCurrency`, `P_RewardMania` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review makes two complaints about Cashman Casino: load times are too long, and a slot bonus feature (the "bonus lady") rarely triggers or lines up. The rest of the review describes the player switching to another game and buying coins there, which is external player behaviour, not a mechanic of this game, and the plan to check back later is not a game mechanic either. The loading complaint is an operational/service wait, not a designed appointment or timer gate the game imposes on progress. The bonus complaint reports only that a random feature is stingy and infrequent; it does not describe the reward-delivery structure as sustaining engagement, does not claim the outcomes are rigged, and names no monetary stake or near-miss perception. Taken together the text is general dissatisfaction with performance and luck, not a description of a dark-pattern mechanic.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `94246484-0b03-4247-91b7-a7b5e6c5ff5c` - Pokémon GO

> Needs improvement. It was doing fine for a while. The most recent update has caused me to not catch raid bosses, not be able to access friends list, open/send gifts, I've had to reinstall it multiple times this week to get it to work. Update. Got a new tablet and the forgot password and username features are useless. Keeps telling me my info can't be found when I try to go through the reset process.

| | labels |
|---|---|
| gold | `S_Reciprocity` |
| pred | _NONE_ |
| **missed** | `S_Reciprocity` |

**Did the model consider what it missed?**

- `S_Reciprocity` - never mentioned -> **attention / recall**

**Model analysis**

```
The review is a bug and account-recovery complaint. The opening items - not catching raid bosses after an update, friends list inaccessible, inability to open or send gifts, repeated reinstalls - are all attributed to a malfunctioning update, not to deliberate design rules. R11 suppresses dark-pattern coding for behaviors attributed to technical faults. The second paragraph describes broken password/username reset features after getting a new tablet; again this is a technical failure of an account-recovery tool, not a designed mechanic. No span describes a functional game rule that satisfies any label; there is no schedule, payment, social-incentive, or psychological mechanic being characterised.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `f112aad7-3ccd-4220-ae49-34d217dda09d` - Gardenscapes

> I downloaded it because of the ad so I thought I would have to help escape him. Little did I know that what I'm playing is nothing less than candy crush. Always you play one game you just get one star only. And all your points get lost if you don't make that level. Even for walking Austin you will have to earn a star by playing stupid game. It's all stupid and no escape game as was shown in the ad.

| | labels |
|---|---|
| gold | `T_Grinding`, `T_MandatoryMarathon` |
| pred | _NONE_ |
| **missed** | `T_Grinding`, `T_MandatoryMarathon` |

**Did the model consider what it missed?**

- `T_Grinding` - never mentioned -> **attention / recall**
- `T_MandatoryMarathon` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer's core complaint is that the game, downloaded on the strength of a promotional ad, is not the escape game the ad showed but is instead a match-3 puzzle game. That complaint concerns external marketing material, which R13 places outside the unit. The rest of the text describes the match-3 structure as the reviewer experiences it: each level awards only one star, failing a level costs the points, and story progression (walking Austin) is gated behind stars earned from the puzzle. These describe ordinary level-progression and reward mechanics for a match-3 game: earning stars, replaying for stars, and losing progress on failure. Nothing in the text describes a timer or appointment, a payment wall, social mechanics, chance-based monetisation, collection pressure, rigged outcomes, or advertisement views inside the game. The annoyance at the mismatch is an evaluation of the product against its advertising, which is not a codable dark pattern under these rules.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `8b4092da-3c5a-41fa-8d14-16c5737e6b85` - Hitwicket™ Cricket Game 2026

> There are several glitches in the game evn when i am winning the progress isnt saved and sometime when i am starting a new game its freezing and i have to restart the game snd boom energy gone but no match progress everytime it several bugs are there specially the match win progress isn't saved. Please try to fix these otherwise a great game .I will edit this review of the bugs are fixed.

| | labels |
|---|---|
| gold | `T_MandatoryMarathon` |
| pred | _NONE_ |
| **missed** | `T_MandatoryMarathon` |

**Did the model consider what it missed?**

- `T_MandatoryMarathon` - never mentioned -> **attention / recall**

**Model analysis**

```
The review is a bug report. The reviewer describes three linked failures: match wins are not being recorded ('progress isnt saved', 'match win progress isn't saved'), the game freezes when starting a new match, and restarting after such a freeze leaves the spent energy gone with no match progress. Every one of these behaviours is explicitly attributed to 'glitches', 'freezing', and 'bugs', and the reviewer's requested action is to fix the bugs. Under R11, behaviours attributed to technical faults are not dark patterns because dark patterns are deliberate design choices rather than malfunctions. Nor does the exception apply: the losses described (progress not saved, wins not recorded, energy consumed by a match that crashed before it ran) are states that no deliberate exit rule would produce — they are the fault itself. There is no description of a designed schedule, payment gate, social mechanic, psychological manipulation, or technical deception that functions independently of the reported bugs.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `5c0e0d12-6578-4169-ba24-c72a325799f1` - All in Hole: Black Hole Games

> cant back out of ads or continue once an ad comes on. i don't care if there are ads but if it gets stuck i can't continue playing after watching it. one star because of this. other than that it's a fantastic challenging game.

| | labels |
|---|---|
| gold | `T_Advertisement` |
| pred | _NONE_ |
| **missed** | `T_Advertisement` |

**Did the model consider what it missed?**

- `T_Advertisement` - never mentioned -> **attention / recall**

**Model analysis**

```
The review's entire complaint is about ads interrupting play: an ad comes on, the player cannot back out of it, and afterwards the game gets stuck so play cannot resume. The reviewer accepts the presence of ads ('i don't care if there are ads'); the harm identified is the game freezing after an ad and being unable to continue. That is a malfunction being reported, not a deliberate mechanic. The inability to back out or continue is tied directly to the ad getting stuck ('if it gets stuck i can't continue playing after watching it'), so the blockage is attributed to a technical fault rather than a designed gate such as forced ad viewing, a cooldown, or an exit rule. Under R11, a specific behavior blamed on a bug or fault does not receive a dark pattern label because dark patterns are deliberate design choices.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (2)

### `3dc64fb0-3b6a-4ba1-9966-79c09f33069c` - Royal Kingdom

> I downloaded this app today after all the hype about the game being ad free. Total lies. Although the ads are seldom, so far, they are there all the same. What has put me off is the fact that to get out of the ad, you have to go into the play store, which then uses even more data.

| | labels |
|---|---|
| gold | `M_UIMisdirection` |
| pred | `T_Advertisement` |
| **missed** | `M_UIMisdirection` |
| **spurious** | `T_Advertisement` |

**Did the model consider what it missed?**

- `M_UIMisdirection` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer's core complaint is that the game, which was marketed as ad-free, actually shows ads inside the app, and that dismissing one of these ads routes the player through the Google Play store, consuming extra data. The 'ad free' hype itself is external marketing and out of scope; what is in scope is the in-game behaviour: an interstitial ad that interrupts play and whose only exit path goes through the store rather than a simple close control. This describes in-game advertising the player is obliged to engage with, which fits the Advertisement definition. The store-routing exit is a property of the ad encounter rather than a purchase-oriented interface element within the game, so UI Misdirection does not apply.
```

**Labels assigned**

- `T_Advertisement` - **SPURIOUS**
  - span: "Although the ads are seldom, so far, they are there all the same. What has put me off is the fact that to get out of the ad, you have to go into the play store, which then uses even more data."
  - why: The game serves ads during play and the only described way out of an ad runs through the app store, so the player is compelled to view or engage with the advertisement rather than freely closing it.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `2f50b132-9762-4f48-ae35-487f414aa41a` - MONOPOLY GO!

> Okay so I started playing in October of 2023. In the beginning, it was a fun game. Over time, I started to see the real issues in the game. 1. Most other players live by the motto you have to cheat to beat the game system and I am starting to feel they are right! 2. Events have become a joke. Peg-E is a total waste the new race car game is even worse! 3. Way to many gold duplicates! 4. Not enough trades a day! 5. Not enough dice.I could keep going but I only have 500 spaces, and I am at my limit

| | labels |
|---|---|
| gold | `P_RewardMania`, `S_Reciprocity` |
| pred | `P_CompleteTheCollection`, `T_DailyRewards` |
| **missed** | `P_RewardMania`, `S_Reciprocity` |
| **spurious** | `P_CompleteTheCollection`, `T_DailyRewards` |

**Did the model consider what it missed?**

- `P_RewardMania` - never mentioned -> **attention / recall**
- `S_Reciprocity` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes several systems in Monopoly GO. 'Other players live by the motto you have to cheat to beat the game system' suggests that cheating is perceived as necessary to keep pace, but this is a description of player conduct and a general sense of unfairness, not an incentive structure the game itself rewards. The reviewer later lists 'Way too many gold duplicates,' which names a mechanic where gold stickers, a rare collectible category, are duplicated instead of missing ones, frustrating collection progress. 'Not enough trades a day' describes a daily cap on trades. 'Not enough dice' refers to scarcity of the core currency that gates play. The phrase 'at my limit' is generic frustration, not a specific mechanic.
```

**Labels assigned**

- `P_CompleteTheCollection` - **SPURIOUS**
  - span: "Way to many gold duplicates!"
  - why: The reviewer is collecting stickers and complains that the game delivers duplicates instead of the golds needed to complete the album, which is frustration with the collection-completion mechanic.
- `T_DailyRewards` - **SPURIOUS**
  - span: "Not enough trades a day!"
  - why: A stated daily limit on trades implies a daily reset schedule that the player must work within, which is a daily-reward-type system gating activity.

**Search:** `Monopoly GO what are gold stickers and duplicate gold stickers` -> Gold stickers are rare collectible stickers required for album completion; duplicates are extra copies of the same gold sticker, which frustrate players trying to complete their collection.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (3)

### `5e2d7a91-2181-4ad5-b5fb-cc1f50805d82` - Real Cricket™

> Too many issues with ads! After every over, an ad pops up. If I accidentally tap the ad instead of cancel, the game closes and the ad opens. It’s super frustrating! I have to restart the app and it ruins the whole mood. This is not acceptable. I play this game to enjoy cricket, not to fight with ads or bad app behavior. Fix the issue — either stop forcing ads like this, fix the UI, or make sure the game doesn’t close when an ad is accidentally clicked. Please fix this.

| | labels |
|---|---|
| gold | `M_UIMisdirection`, `T_Advertisement` |
| pred | `T_Advertisement` |
| **missed** | `M_UIMisdirection` |

**Did the model consider what it missed?**

- `M_UIMisdirection` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a single central problem: the game interrupts play with an advertisement after every over, and the ad's close/cancel handling is such that a mistap opens the ad and closes the game, forcing a restart. The forced, recurring ad after each over is the mechanic the reviewer names outright ('After every over, an ad pops up', 'stop forcing ads like this'). The accidental-tap behaviour is presented as bad app behaviour and a UI flaw to be fixed, but nothing connects it to a purchase decision or a deliberate in-game opt-out design, so it reads as a usability complaint about the ad overlay rather than a monetization UI pattern. No temporal, social, or psychological manipulation is described.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "After every over, an ad pops up."
  - why: Ads are forced at fixed in-game events (after every over), so the player must view them to continue playing, which is compelled ad viewing.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `40767241-e96d-4020-a23b-8e08eb00ea95` - Pixel Flow!

> Can't close the ads, therefore can't continue playing without closing and restarting the game. Not a good experience.

| | labels |
|---|---|
| gold | `M_UIMisdirection`, `T_Advertisement` |
| pred | `T_Advertisement` |
| **missed** | `M_UIMisdirection` |

**Did the model consider what it missed?**

- `M_UIMisdirection` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a single, concrete in-game behaviour: an advertisement appears that has no working close control, so the game cannot proceed. The reviewer's only way forward is to quit and relaunch the app. The ad blocks continued play and cannot be dismissed, so the player is compelled to sit through or at least be stalled by the advertisement. There is no attribution to a bug or crash, and no other mechanic (currency, payment, social, temporal) is described.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "Can't close the ads, therefore can't continue playing without closing and restarting the game."
  - why: The ad cannot be dismissed and blocks continuing play, so the player is compelled to deal with the advertisement before the game proceeds.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `42025004-6937-4657-ab75-72e97fe19166` - Lightning Link Casino Slots

> The game is great. Neat features, generous bonuses. I messed up and accidentally bought a huge coin pack and Product Madness was quick to refund me and be generally very cool and understanding. Great game made by great people.

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `M_IntermediateCurrency` |
| pred | `M_IntermediateCurrency` |
| **missed** | `M_EasyToPurchase` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review is a short positive appraisal: the reviewer praises the game's features and bonuses, then recounts a single incident in which they accidentally made a real-money purchase of a large coin pack and the developer refunded it promptly. Reading the incident for what it implies about the game's design: the game sells coin packs for real money, so the reviewer's own action evidences a real-money-to-in-game-currency purchase channel. There is no description of any interface mechanism that made the purchase easy, and the reviewer takes personal responsibility ('I messed up') while crediting the developer's refund, so the accident does not evidence absent confirmation or refund ability (M_EasyToPurchase's indicator requires the design to remove friction or confirmation). 'Generous bonuses' is a statement of reward value, not of a delivery mechanism, so it does not support Reward Mania. The one mechanic actually evidenced by the text is the sale of in-game coins for real money.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "accidentally bought a huge coin pack"
  - why: The coins are the object acquired through a real-money purchase, so the span describes the conversion of money into in-game currency regardless of the reviewer's approving tone.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (2)

### `e19dc016-9f44-4e0e-bc04-d5198a837c4a` - Ludo King®

> i feel guilty after installing it..sometime it feels like the game is meant to make you lose most of the time..it's partial.. it is totally time wasting to install it and i don't understand how players have reached higher levels..and the glitches are very much annoying..if you are meant to lose, no matter how good you play you will definitley lose and in most of the cases this is the scene always..the opponents get good counts and you get small counts..it's better to play on the board rather.

| | labels |
|---|---|
| gold | `P_IllusionOfControl` |
| pred | `P_IllusionOfControl`, `S_Competition` |
| **spurious** | `S_Competition` |

**Model analysis**

```
The reviewer is complaining that Ludo King is rigged: they believe the game is designed to make them lose regardless of skill, giving opponents better dice rolls and themselves worse ones. This is a claim about concealed or manipulated determination of match outcomes, not a report of an unlucky run or a general difficulty complaint. The mention of glitches is a technical-fault complaint and does not itself suppress the rigging claim, which is described as a design behaviour rather than a malfunction. Playing against opponents is the setting in which the rigging is alleged to operate, so the competitive structure is part of what is described.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "if you are meant to lose, no matter how good you play you will definitley lose and in most of the cases this is the scene always..the opponents get good counts and you get small counts"
  - why: The span asserts that the game fixes who wins, making skill irrelevant, which is a claim about concealed determination of outcomes rather than a bad run.
- `S_Competition` - **SPURIOUS**
  - span: "the opponents get good counts and you get small counts"
  - why: The review places the player in direct opposition to other players, whose rolls are described as favoured over the reviewer's, so the game is described as making the player compete against others.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `201672d6-579d-44c3-a1df-55a3f8182969` - Travel Town - Merge Adventure

> This game was lot more fun in the starting stage . The daily missions are impossible to do in such less attempts and it takes nearly 2 minutes for new chances to play. And the item don't even make according to the orders . Pathetic game

| | labels |
|---|---|
| gold | `T_PlayingByAppointment` |
| pred | `T_DailyRewards`, `T_PlayingByAppointment` |
| **spurious** | `T_DailyRewards` |

**Model analysis**

```
The review describes a merge game where the player's activity is constrained by a limited pool of attempts that refill on a timer ('nearly 2 minutes for new chances to play'), and where daily missions demand more attempts than the player is given ('daily missions are impossible to do in such less attempts'). The daily missions are a resetting daily task system whose rewards the player forfeits when the attempts run out before completion. The final complaint about items not matching orders is too ambiguous (possible glitch or randomness of item production) to anchor any defined dark pattern, and 'fun in the starting stage'/'pathetic' are evaluations rather than mechanics.
```

**Labels assigned**

- `T_DailyRewards` - **SPURIOUS**
  - span: "The daily missions are impossible to do in such less attempts"
  - why: Daily missions are a resetting daily task system that pulls the player into daily sessions and whose rewards are lost when the day's limited attempts cannot complete them.
- `T_PlayingByAppointment` - ok
  - span: "it takes nearly 2 minutes for new chances to play"
  - why: The span names an in-game refill timer that makes the player wait for more attempts before continuing, so play is gated by the game's clock rather than the player's choice.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_UIMisdirection` | 4 | 0 |
| `S_Reciprocity` | 2 | 0 |
| `P_RewardMania` | 2 | 0 |
| `M_EasyToPurchase` | 2 | 0 |
| `S_Competition` | 1 | 1 |
| `T_MandatoryMarathon` | 2 | 0 |
| `T_DailyRewards` | 0 | 2 |
| `T_Advertisement` | 1 | 1 |
| `M_IntermediateCurrency` | 1 | 0 |
| `T_Grinding` | 1 | 0 |
| `M_NeverEndingLure` | 1 | 0 |
| `M_WasteAversion` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `P_CompleteTheCollection` | 0 | 1 |

