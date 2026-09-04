# Error review - gpt-5.6-luna_high_teacher_v3_full

`gpt-5.6-luna` / reasoning `high` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v3_full.txt` sha `a6ae58246360`  
micro-F1 **0.781** (P 0.806 / R 0.758) - **13 of 30** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 4 | said NONE, gold had labels |
| SWAP | 0 | picked different labels than gold |
| MISSED ONLY | 4 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 5 | found all gold, added extras |

## The diagnostic that matters

Of **8** missed labels, **2** (25%) were named in the model's own analysis and dropped anyway; **6** (75%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `T_MandatoryMarathon` | 0 | 2 |
| `S_Reciprocity` | 0 | 1 |
| `M_NeverEndingLure` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `S_Competition` | 1 | 0 |
| `M_UIMisdirection` | 0 | 1 |
| `T_Advertisement` | 1 | 0 |

## Missed everything (predicted NONE) (4)

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
The reviewer describes a successful payment for a one-time weekly offer, followed by failure to receive the purchased offer and a demand for a refund. This is a purchase-delivery or transaction problem, not a described game mechanic. The wording does not establish a recurring fee, an accidental purchase, a purchase prompt, or payment being required for progress. Under R11, a missing purchased offer is a technical or fulfillment fault rather than a dark-pattern label.
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
The review describes technical failures after an update: raid bosses cannot be caught, the friends list and gift functions cannot be accessed, and reinstalling is needed to restore functionality. The later account-recovery problem is also attributed to the reset process failing to find the user's information. These are bugs or technical faults rather than deliberate game design mechanics. Although opening and sending gifts are mentioned, the review only describes being unable to use them because of the malfunction, so no social-mechanic label applies under R11.
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
The review describes glitches and bugs: match-winning progress is not saved, the game freezes when starting a new game, and restarting after the freeze consumes energy without recording match progress. These are explicitly attributed to technical faults rather than deliberate game rules. Under R11, the lost progress and energy are therefore not coded as dark patterns; no label is supported.
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

- `T_Advertisement` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes an advertisement appearing during play, but the complaint is specifically that the ad becomes stuck and prevents the player from continuing after watching it. Because the inability to proceed is attributed to a technical malfunction rather than a deliberate ad-viewing requirement, R11 suppresses the Advertisement label. No other mechanic is clearly described.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (4)

### `ac5fc6a4-b597-46f3-af5a-3735b3854e26` - Gossip Harbor: Merge & Story

> I really wanted to like this game, however not even 10 minutes into playing it, it notified me that I bought a starter pack. I didn't tap anything and my settings are set up to where I have to input my fingerprint or password to make a purchase and it did not do that. Uninstalling ASAP. Not sure if it's just a glitch or what, but I'm not chancing that again.

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `M_NeverEndingLure` |
| pred | `M_EasyToPurchase` |
| **missed** | `M_NeverEndingLure` |

**Did the model consider what it missed?**

- `M_NeverEndingLure` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes an in-game purchase being completed without tapping a purchase control and without the device's required fingerprint or password confirmation. This is an unintended purchase caused by the absence or bypass of a confirmation step, matching Accidental Purchases. The mention of a possible glitch is uncertain and does not erase the explicitly described purchase behavior; no discount or special pricing is stated for the starter pack, so Never-Ending Lure is not supported.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "I didn't tap anything and my settings are set up to where I have to input my fingerprint or password to make a purchase and it did not do that."
  - why: The purchase allegedly completed without the player's intended tap and without the required confirmation or authentication step.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

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
The review describes an in-game advertisement that appears after every over, making the player view ads at a recurring gameplay event. This is a forced ad mechanic and satisfies Advertisement. The game closing when the player accidentally taps the ad, requiring an app restart, is attributed to bad app behavior or a technical fault, so it does not independently support a dark-pattern label. The review does not clearly describe a deliberately misleading, hidden, or undersized cancel control, so UI Misdirection is not assigned. No external search is needed.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "After every over, an ad pops up."
  - why: An advertisement is imposed at a fixed in-game event, compelling the player to encounter it during play.

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
The review describes increased interface friction from repeated pop-up screens. The player must dismiss an "are you sure you want to quit" screen with an X before continuing, which obstructs the normal opt-out or continuation path and fits UI Misdirection. The weekly challenge score pop-ups are merely described as numerous and annoying; no reward, schedule pressure, competition, or advertising mechanic is clearly established. The increased cost is a pricing complaint without a described purchase mechanism, so it does not support a monetary label.
```

**Labels assigned**

- `M_UIMisdirection` - ok
  - span: "are you sure you want to quit screens that you have to X out of before continuing"
  - why: The game forces the player to dismiss an intervening screen before continuing, obstructing the normal continuation or exit flow.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `f112aad7-3ccd-4220-ae49-34d217dda09d` - Gardenscapes

> I downloaded it because of the ad so I thought I would have to help escape him. Little did I know that what I'm playing is nothing less than candy crush. Always you play one game you just get one star only. And all your points get lost if you don't make that level. Even for walking Austin you will have to earn a star by playing stupid game. It's all stupid and no escape game as was shown in the ad.

| | labels |
|---|---|
| gold | `T_Grinding`, `T_MandatoryMarathon` |
| pred | `T_Grinding` |
| **missed** | `T_MandatoryMarathon` |

**Did the model consider what it missed?**

- `T_MandatoryMarathon` - never mentioned -> **attention / recall**

**Model analysis**

```
The external advertisement is described as misleading, but advertising placed outside the installed game is out of scope under R13, so it does not receive a label. Within the game, the reviewer describes repeatedly playing a Candy Crush-like level to earn stars, with stars required to make progress such as walking Austin. This is a repetitive task used for progression, which supports Grinding. The loss of points after failing a level does not by itself show a retention or stopping mechanic covered by another label.
```

**Labels assigned**

- `T_Grinding` - ok
  - span: "Always you play one game you just get one star only. And all your points get lost if you don't make that level. Even for walking Austin you will have to earn a star by playing stupid game."
  - why: The reviewer describes repeatedly playing the same type of level to earn stars needed for game progress, which is a tedious task cycle tied to advancement.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (5)

### `3dc64fb0-3b6a-4ba1-9966-79c09f33069c` - Royal Kingdom

> I downloaded this app today after all the hype about the game being ad free. Total lies. Although the ads are seldom, so far, they are there all the same. What has put me off is the fact that to get out of the ad, you have to go into the play store, which then uses even more data.

| | labels |
|---|---|
| gold | `M_UIMisdirection` |
| pred | `M_UIMisdirection`, `T_Advertisement` |
| **spurious** | `T_Advertisement` |

**Model analysis**

```
The review describes advertisements appearing inside the game despite the claim that it was ad free. It also describes an obstructed ad exit: leaving the advertisement requires opening the Play Store, which adds friction and data use. The external hype about the game being ad free is marketing material and is out of scope, but the in-game ads and their difficult dismissal are in scope.
```

**Labels assigned**

- `M_UIMisdirection` - ok
  - span: "to get out of the ad, you have to go into the play store"
  - why: The ad obstructs the normal opt-out or exit path by requiring the player to enter the Play Store to leave it.
- `T_Advertisement` - **SPURIOUS**
  - span: "Although the ads are seldom, so far, they are there all the same."
  - why: The reviewer explicitly reports encountering advertisements within the game.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `036954c0-447e-460d-b81e-f26f940b2ac4` - Shadow Fight 4: Arena

> On playing the Event game Mode and Duel Mode game will be strucked or Lagged and contlors are doesn't work properly while we playing the game and finally game has suddenly stopped and says YOU HAVE LOST and then nearly -30 to -50 gaming points are lessed from my Ranked game progress , these type of game shows golden coloured network icons near the Health bar, But my network signals are perfectly alright at that time while using other online apps , please rectify this problem as soon as possible.

| | labels |
|---|---|
| gold | `T_MandatoryMarathon` |
| pred | `S_Competition`, `T_MandatoryMarathon` |
| **spurious** | `S_Competition` |

**Model analysis**

```
The review describes a competitive match in Duel/Event modes, with ranked points at stake. The lag, unresponsive controls, network warning, and sudden stoppage are attributed to a technical malfunction, so those faults themselves do not receive a dark-pattern label. However, the game applies an explicit match-loss penalty after the malfunction: it declares the player defeated and removes roughly 30–50 ranked points. Under R11, a malfunction does not suppress Mandatory Marathon when the underlying game rule forfeits match progress upon an interrupted session. The review does not describe advertising, payment, rewards, currencies, or a chance-based outcome.
```

**Labels assigned**

- `S_Competition` - **SPURIOUS**
  - span: "Duel Mode"
  - why: Duel Mode describes player-versus-player competition, and the associated ranked progress confirms that competitive standing is part of the mechanic.
- `T_MandatoryMarathon` - ok
  - span: "game has suddenly stopped and says YOU HAVE LOST and then nearly -30 to -50 gaming points are lessed from my Ranked game progress"
  - why: Although the stoppage is attributed to lag or a technical fault, the game treats the interrupted match as a loss and removes ranked progress, imposing a deliberate forfeiture penalty when the session ends unexpectedly.

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
The reviewer describes a competitive dice-based game in which outcomes are allegedly predetermined or manipulated against them: regardless of skill, they say they will lose, while opponents receive favorable counts and they receive unfavorable ones. That is a claim that the game determines outcomes rather than letting play skill and chance decide them, which supports Illusion of Control. The mention of opponents also explicitly describes player-versus-player competition. The references to guilt, time wasting, and glitches are evaluations or technical complaints and do not independently support a label.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "if you are meant to lose, no matter how good you play you will definitley lose and in most of the cases this is the scene always..the opponents get good counts and you get small counts"
  - why: The reviewer alleges that the game fixes or biases the outcome, giving opponents favorable counts and the player unfavorable counts regardless of skill.
- `S_Competition` - **SPURIOUS**
  - span: "the opponents get good counts and you get small counts"
  - why: The span explicitly describes the player competing against opponents in the game.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `e2a95947-be08-4077-ad5f-1e7891b9eff5` - MadOut 2: Grand Auto Racing

> the best graphics forever why you give the screen size 1GB my phone is storage full for this game I am playing this game on Red magic 11 Pro because I will download it meaning in 30 gb games on it and when I play it game has a badass graphics pick all the pictures of fake

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `Tech_FragmentedDownloads` |
| **spurious** | `Tech_FragmentedDownloads` |

**Model analysis**

```
The reviewer is describing a mismatch between the stated 1GB size and the game's actual storage demand: despite the game being presented as 1GB, it fills the phone's storage. This implies that the true storage requirement is larger than the apparent advertised size, which matches Fragmented Downloads. The comments about the phone model and graphics are not dark-pattern mechanics.
```

**Labels assigned**

- `Tech_FragmentedDownloads` - **SPURIOUS**
  - span: "why you give the screen size 1GB my phone is storage full for this game"
  - why: The reviewer contrasts the stated 1GB size with the game filling the phone's storage, implying that the actual storage requirement is obscured until installation or play.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `6ccb26a7-01e3-41a3-ba1a-bddba2063257` - Lightning Link Casino Slots

> Dont even waste you time with this app. I dont understand why you guys make these things so fun to play but impossible to ever win. I mean I know your trying to make money on the app but why would I ever come back and spend more money when it is impossible to when. Because of that this app is garbage!!!!!!!

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `M_Gambling`, `P_RewardMania` |
| **spurious** | `M_Gambling`, `P_RewardMania` |

**Model analysis**

```
The review describes a casino-slots app whose core play is gambling: the player is expected to spend money for a chance to win, but says winning is effectively impossible. The slot format also identifies a chance-based reward system that keeps play centered on repeated attempts and uncertain outcomes. The complaint does not describe a specific rigging mechanism, near-misses, progress gating, or a required wait, so those labels are not supported.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "why would I ever come back and spend more money when it is impossible to when"
  - why: The player describes spending money in a casino-slots game for the chance of winning a reward.
- `P_RewardMania` - **SPURIOUS**
  - span: "make these things so fun to play but impossible to ever win"
  - why: In the context of Lightning Link Casino Slots, the span describes repeated play driven by uncertain chance-based winnings, the reward-delivery pattern covered by Reward Mania.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `S_Competition` | 1 | 2 |
| `T_MandatoryMarathon` | 2 | 0 |
| `T_Advertisement` | 1 | 1 |
| `S_Reciprocity` | 1 | 0 |
| `M_Gambling` | 0 | 1 |
| `Tech_FragmentedDownloads` | 0 | 1 |
| `P_RewardMania` | 0 | 1 |
| `M_UIMisdirection` | 1 | 0 |
| `M_NeverEndingLure` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |

