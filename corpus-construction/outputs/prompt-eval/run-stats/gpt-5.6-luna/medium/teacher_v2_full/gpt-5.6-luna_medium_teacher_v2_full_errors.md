# Error review - gpt-5.6-luna_medium_teacher_v2_full

`gpt-5.6-luna` / reasoning `medium` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `aad355174ac4`  
micro-F1 **0.593** (P 0.762 / R 0.485) - **16 of 30** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 10 | said NONE, gold had labels |
| SWAP | 1 | picked different labels than gold |
| MISSED ONLY | 2 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 3 | found all gold, added extras |

## The diagnostic that matters

Of **17** missed labels, **3** (18%) were named in the model's own analysis and dropped anyway; **14** (82%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `M_UIMisdirection` | 0 | 4 |
| `T_MandatoryMarathon` | 1 | 2 |
| `S_Reciprocity` | 0 | 2 |
| `P_RewardMania` | 1 | 0 |
| `T_Grinding` | 0 | 1 |
| `M_EasyToPurchase` | 0 | 1 |
| `S_Competition` | 0 | 1 |
| `M_NeverEndingLure` | 0 | 1 |
| `M_WasteAversion` | 1 | 0 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `T_Advertisement` | 0 | 1 |

## Missed everything (predicted NONE) (10)

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
The review describes an apparent unintended purchase of a starter pack: the game notified the player that the purchase happened even though they did not tap anything and the required fingerprint or password confirmation did not occur. However, the reviewer explicitly frames the behavior as possibly a glitch, so under R11 the apparent accidental-purchase behavior is treated as a technical malfunction rather than a deliberate purchase-friction design. No label applies.
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
The review describes a crowded game board and inventory pressure: many new objects fill a small board, and archived objects still consume inventory space. However, it does not explicitly state that currency, items, or capacity are actually forfeited, stranded, or insufficient to buy a target, so Waste Aversion is not supported under its boundary rule. The review also mentions energy being insufficient for long sessions, but it does not describe a timer or regeneration schedule, so Playing by Appointment does not apply. Gems slowing as the player unlocks fewer new items describes an earning-rate complaint, not a qualifying mechanic. The mismatch with the advertisement is out-of-game marketing and is excluded by R13. No other label is explicitly supported.
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
The reviewer describes paying R79,99 for a weekly one-time offer, with the bank transaction succeeding but the purchased offer not being delivered. This is a failed or missing transaction, a technical or fulfillment problem rather than a deliberate game mechanic. The request for a refund does not describe a qualifying design behavior, so no label applies.
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
The review describes increased pop-up screens, including a weekly challenge score and confirmation screens asking whether the player wants to quit. These screens must be dismissed before continuing, but the review does not connect them to purchases, spending, or obstructing a purchase opt-out. The increased cost is mentioned only as a complaint about price, without a progression or purchasing mechanic. No applicable label is supported.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `eb67d840-0a90-4d5a-875b-2ff49975ea31` - Animals & Coins: Animal Run

> This game, and all the other games by this developer are very fun to play. The problem I have with all these games is the seemingly endless in-game ads and pop-ups that cascade one after another so much that by the time I can actually play, I'm no longer interested.

| | labels |
|---|---|
| gold | `T_Advertisement` |
| pred | _NONE_ |
| **missed** | `T_Advertisement` |

**Did the model consider what it missed?**

- `T_Advertisement` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes frequent in-game ads and pop-ups that delay access to gameplay. However, the text does not explicitly say the ads are forced to be watched, rewarded, or otherwise ad-gated, and it does not identify purchase prompts or a friction-reducing purchase interface. The complaint is about excessive volume and delay alone, which does not satisfy a label under the codebook.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `036954c0-447e-460d-b81e-f26f940b2ac4` - Shadow Fight 4: Arena

> On playing the Event game Mode and Duel Mode game will be strucked or Lagged and contlors are doesn't work properly while we playing the game and finally game has suddenly stopped and says YOU HAVE LOST and then nearly -30 to -50 gaming points are lessed from my Ranked game progress , these type of game shows golden coloured network icons near the Health bar, But my network signals are perfectly alright at that time while using other online apps , please rectify this problem as soon as possible.

| | labels |
|---|---|
| gold | `T_MandatoryMarathon` |
| pred | _NONE_ |
| **missed** | `T_MandatoryMarathon` |

**Did the model consider what it missed?**

- `T_MandatoryMarathon` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a technical malfunction during Event and Duel matches: lag, nonresponsive controls, and a sudden game stoppage accompanied by a loss declaration. The deducted ranked points are attributed to that malfunction and the faulty network indicator, not to a deliberate game rule that penalizes voluntarily leaving a match. Under R11, the loss itself is suppressed because it is presented as a technical fault rather than an intentional design behavior. No other coded mechanic is explicitly supported.
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
The review describes technical failures after an update and during account recovery: raid bosses cannot be caught, the friends list and gift actions cannot be accessed, and reinstalling is needed to restore functionality. The password and username reset process also fails to find the player's information. These are explicitly attributed to an update, repeated malfunction, or a useless reset feature, so they are technical faults rather than deliberate game mechanics. Although friends and gifts are social features, the review does not describe a social obligation or resource-exchange pressure; it only reports that those features are broken. No label applies.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `2f50b132-9762-4f48-ae35-487f414aa41a` - MONOPOLY GO!

> Okay so I started playing in October of 2023. In the beginning, it was a fun game. Over time, I started to see the real issues in the game. 1. Most other players live by the motto you have to cheat to beat the game system and I am starting to feel they are right! 2. Events have become a joke. Peg-E is a total waste the new race car game is even worse! 3. Way to many gold duplicates! 4. Not enough trades a day! 5. Not enough dice.I could keep going but I only have 500 spaces, and I am at my limit

| | labels |
|---|---|
| gold | `P_RewardMania`, `S_Reciprocity` |
| pred | _NONE_ |
| **missed** | `P_RewardMania`, `S_Reciprocity` |

**Did the model consider what it missed?**

- `P_RewardMania` - considered and rejected -> **rule interpretation**
- `S_Reciprocity` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes player cheating, dissatisfaction with named events, duplicate gold items, a daily limit on trades, and insufficient dice. The cheating is attributed to other players rather than to a game design that rewards harmful behavior, so it does not establish Encourages Anti-Social Behavior. The event comments are evaluations without a specific mechanic. Duplicate golds could suggest a random reward or collection system, but the review does not explicitly describe packs, draws, chance, or a collection goal, so Reward Mania and Complete the Collection are not supported. A daily trade limit is a resource cap, not a daily login reward or a required play schedule, and not enough dice alone does not establish a wait timer or payment gate. No label is supported.
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
The review describes two distinct things. First, it complains that the game's external advertisement presented an escape-rescue scenario, while the installed game is a match-three game; under R13, that out-of-game advertising and misrepresented gameplay are outside the unit and do not receive a label. Second, within the game, progress in Austin's story or movement is tied to earning stars by playing the match-three levels, and failed progress causes points to be lost. The review does not clearly describe waiting timers, repeated tasks required for progress, payment, rewards for daily return, or a penalty for quitting, so no listed mechanic label is supported.
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

- `T_MandatoryMarathon` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review attributes all described problems to glitches, freezing, and bugs: progress is not saved after winning, restarting is required after the game freezes, energy is lost, and match progress is missing. Under R11, these are technical malfunctions rather than deliberate design mechanics. The lost energy and match progress are explicitly presented as consequences of the freezing and unsaved-progress bugs, so they do not establish Mandatory Marathon or any other dark-pattern label.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (1)

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
The review describes advertisements appearing inside the game, despite the game being promoted as ad free. The ads are reportedly infrequent, but the player says leaving one requires entering the app store, which means the player is compelled to view or interact with the advertisement before returning to gameplay. The mention of additional data use is a consequence of that ad flow, not a separate coded mechanic.
```

**Labels assigned**

- `T_Advertisement` - **SPURIOUS**
  - span: "to get out of the ad, you have to go into the play store"
  - why: The player cannot exit the in-game advertisement directly and must go through the app store, making the ad interaction compulsory.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (2)

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
The review describes an in-game advertisement mechanic that interrupts play after every over, making ad viewing compulsory. It also describes a malfunction after an accidental ad tap: the game closes and the reviewer must restart the app. The closing behavior is attributed to bad app behavior and a request to fix it, so it does not establish a deliberate UI-misdirection mechanic or a session-forfeiture rule. The requested changes are hypothetical and are not coded.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "After every over, an ad pops up."
  - why: An advertisement is imposed during gameplay after every over, describing a recurring forced ad interruption.

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
The review describes an in-game advertisement that cannot be dismissed, blocking continued play. The player must close and restart the game to get past the ad. This is a forced or unskippable advertisement, but the review does not describe a purchase prompt, spending friction, or progress loss on exit.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "Can't close the ads, therefore can't continue playing without closing and restarting the game."
  - why: The ad cannot be dismissed and prevents the player from continuing without restarting the game.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (3)

### `7732d254-0a39-4614-acf4-e67840e14b76` - Cashman Casino Slots Games

> loading takes entirely tooooo long also the bonus lady rarely comes out or even matches with anything on ww4. iv started playing a new game and buying coins from them.ill check inevery so offethen to see if it has changed . hopefully this rating will do it.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `P_RewardMania` |
| pred | `M_Gambling`, `M_IntermediateCurrency`, `P_RewardMania` |
| **spurious** | `M_Gambling` |

**Model analysis**

```
The review describes excessively long loading, which is a technical performance problem and is suppressed by R11 rather than receiving a dark-pattern label. It also describes a slot-game bonus feature involving a bonus lady that appears rarely and fails to match on WW4; the search established that WW4 refers to Wicked Winnings IV, a slot game with random bonus and wild-symbol features. The reviewer additionally says they are buying coins from the game, establishing real-money conversion into an in-game currency. Together, the slot chance mechanic and purchased coins support Gambling, while the infrequent and unpredictable bonus delivery supports Reward Mania. The reviewer says they have started playing a new game and will only check back occasionally, but this does not explicitly describe a game-imposed schedule, reward expiry, or pressure to return.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "the bonus lady rarely comes out or even matches with anything on ww4. iv started playing a new game and buying coins from them"
  - why: The span combines a slot-game bonus outcome governed by chance with the purchase of coins used to participate in the game.
- `M_IntermediateCurrency` - ok
  - span: "buying coins from them"
  - why: The reviewer describes acquiring in-game coins from the developer with real money, establishing conversion from real-world money into virtual currency.
- `P_RewardMania` - ok
  - span: "the bonus lady rarely comes out or even matches with anything on ww4"
  - why: The bonus feature is described as an infrequent, unpredictable reward outcome that sustains engagement through repeated attempts.

**Search:** `Cashman Casino Slots Games "ww4" bonus lady` -> The search established that WW4 refers to Wicked Winnings IV, a slot game featuring random bonus and wild-symbol mechanics.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `e19dc016-9f44-4e0e-bc04-d5198a837c4a` - Ludo King®

> i feel guilty after installing it..sometime it feels like the game is meant to make you lose most of the time..it's partial.. it is totally time wasting to install it and i don't understand how players have reached higher levels..and the glitches are very much annoying..if you are meant to lose, no matter how good you play you will definitley lose and in most of the cases this is the scene always..the opponents get good counts and you get small counts..it's better to play on the board rather.

| | labels |
|---|---|
| gold | `P_IllusionOfControl` |
| pred | `P_IllusionOfControl`, `S_Competition` |
| **spurious** | `S_Competition` |

**Model analysis**

```
The review describes a competitive match mechanic involving opponents and dice counts. It also alleges that outcomes are systematically manipulated: the reviewer says the game is meant to make them lose, that good play cannot change the result, and that opponents receive better counts while the reviewer receives smaller ones. This supports Illusion of Control because the game is portrayed as secretly determining outcomes rather than allowing skill to decide them. The mention of glitches is a general technical complaint and does not itself trigger a label.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "if you are meant to lose, no matter how good you play you will definitley lose"
  - why: The reviewer alleges that the game predetermines losses and overrides player skill, describing manipulated outcomes.
- `S_Competition` - **SPURIOUS**
  - span: "the opponents get good counts and you get small counts"
  - why: The span explicitly describes play against opponents in a competitive match.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `6ccb26a7-01e3-41a3-ba1a-bddba2063257` - Lightning Link Casino Slots

> Dont even waste you time with this app. I dont understand why you guys make these things so fun to play but impossible to ever win. I mean I know your trying to make money on the app but why would I ever come back and spend more money when it is impossible to when. Because of that this app is garbage!!!!!!!

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `M_Gambling`, `T_InfiniteTreadmill` |
| **spurious** | `M_Gambling`, `T_InfiniteTreadmill` |

**Model analysis**

```
The review describes a casino slot game that is fun to play but allegedly makes winning impossible. The combination of playing slots and spending money to continue or return supports a paid chance-based mechanic. The statement that it is "impossible to ever win" describes the game as having no attainable winning outcome, which matches the impossible-to-win indicator for Infinite Treadmill. It does not describe a specific rigging mechanism, repeated attempts, variable reward delivery, or payment being required for progression, so no additional labels apply.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "why would I ever come back and spend more money when it is impossible to when"
  - why: The reviewer links spending more money with trying to win in the casino slot game, describing paid participation in a chance-based activity.
- `T_InfiniteTreadmill` - **SPURIOUS**
  - span: "make these things so fun to play but impossible to ever win"
  - why: The reviewer explicitly describes the game as offering continued play without any attainable winning outcome.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_UIMisdirection` | 4 | 0 |
| `T_MandatoryMarathon` | 3 | 0 |
| `S_Reciprocity` | 2 | 0 |
| `M_Gambling` | 0 | 2 |
| `S_Competition` | 1 | 1 |
| `T_Advertisement` | 1 | 1 |
| `T_InfiniteTreadmill` | 0 | 1 |
| `P_RewardMania` | 1 | 0 |
| `T_Grinding` | 1 | 0 |
| `M_EasyToPurchase` | 1 | 0 |
| `M_NeverEndingLure` | 1 | 0 |
| `M_WasteAversion` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |

