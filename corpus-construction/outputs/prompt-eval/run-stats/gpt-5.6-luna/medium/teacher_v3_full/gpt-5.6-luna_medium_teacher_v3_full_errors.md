# Error review - gpt-5.6-luna_medium_teacher_v3_full

`gpt-5.6-luna` / reasoning `medium` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v3_full.txt` sha `a6ae58246360`  
micro-F1 **0.724** (P 0.840 / R 0.636) - **14 of 30** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 6 | said NONE, gold had labels |
| SWAP | 0 | picked different labels than gold |
| MISSED ONLY | 4 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 4 | found all gold, added extras |

## The diagnostic that matters

Of **12** missed labels, **3** (25%) were named in the model's own analysis and dropped anyway; **9** (75%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `T_MandatoryMarathon` | 1 | 2 |
| `P_RewardMania` | 0 | 2 |
| `M_UIMisdirection` | 0 | 2 |
| `S_Reciprocity` | 0 | 1 |
| `M_EasyToPurchase` | 1 | 0 |
| `S_Competition` | 1 | 0 |
| `M_NeverEndingLure` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |

## Missed everything (predicted NONE) (6)

### `ac5fc6a4-b597-46f3-af5a-3735b3854e26` - Gossip Harbor: Merge & Story

> I really wanted to like this game, however not even 10 minutes into playing it, it notified me that I bought a starter pack. I didn't tap anything and my settings are set up to where I have to input my fingerprint or password to make a purchase and it did not do that. Uninstalling ASAP. Not sure if it's just a glitch or what, but I'm not chancing that again.

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `M_NeverEndingLure` |
| pred | _NONE_ |
| **missed** | `M_EasyToPurchase`, `M_NeverEndingLure` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - considered and rejected -> **rule interpretation**
- `M_NeverEndingLure` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes an unintended in-game purchase of a starter pack without tapping anything. Although this resembles Accidental Purchases under Easy to Purchase, the reviewer attributes the missing confirmation/authentication to a possible glitch: the purchase should have required a fingerprint or password, but did not. Under R11, a specific purchase behavior attributed to a glitch or technical fault is not coded as a deliberate dark pattern. The mention of a starter pack alone does not establish a first-purchase discount or another mechanic.
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
The reviewer describes a real-money purchase for a weekly one-time offer, with the bank transaction succeeding but the purchased offer not being delivered. This is attributed to a failed transaction or technical/accounting problem rather than a deliberate game design mechanic. The span does not establish a recurring fee, pay-to-progress mechanic, easy purchase interface, or any other coded pattern.
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
- `S_Competition` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes increased interface friction: repeated pop-up screens showing a weekly challenge score and confirmation screens asking whether the player wants to quit. The player must press an X before continuing, but the screens are not described as purchase prompts, ads, or barriers tied to progress. A weekly challenge score alone does not establish competition or a schedule-based obligation. The increased cost is mentioned without explaining what is being purchased or how payment affects progress. Therefore, no meso label is supported.
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

- `T_MandatoryMarathon` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a technical malfunction during Event and Duel matches: lag, nonresponsive controls, and a sudden stoppage while the reviewer’s network was functioning normally. The game then incorrectly records a loss and deducts roughly 30–50 ranked points. Under R11, the malfunction itself does not create a dark-pattern label, and the review does not say that voluntarily leaving a match would trigger the same penalty, so Mandatory Marathon is not supported. The text also does not clearly describe a functional competition mechanic; it only mentions ranked progress in the context of the technical failure.
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
The review describes technical failures after an update: raid bosses cannot be caught, the friends list cannot be accessed, gifts cannot be opened or sent, and the app must be reinstalled repeatedly. The password and username recovery process also fails by saying the information cannot be found. These are bugs or account-access errors, not deliberate game design behaviors. The references to friends and gifts do not establish a social dark pattern because no recruitment, unsolicited messaging, or reciprocal obligation is described.
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
The review attributes all described problems to glitches and bugs: match-win progress is not saved, the game freezes when starting a new match, and restarting after the freeze consumes energy without recording match progress. Under R11, these are technical malfunctions rather than deliberate game-design mechanics. The lost energy and match progress are presented as consequences of the freezing and saving failure, not as penalties imposed by an intentional exit rule. No label applies.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (4)

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
The review describes an in-game advertisement mechanic: an ad is forced after every over, requiring the player to encounter it during normal cricket gameplay. The app closing when the ad is accidentally tapped is attributed to bad app behavior and is a technical malfunction, so it does not establish a separate dark-pattern label. The request to fix the UI is hypothetical and does not describe a confirmed UI-misdirection mechanism such as a hidden or undersized cancel control.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "After every over, an ad pops up."
  - why: Ads are automatically shown at a fixed in-game event, compelling the player to view them during play.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `7732d254-0a39-4614-acf4-e67840e14b76` - Cashman Casino Slots Games

> loading takes entirely tooooo long also the bonus lady rarely comes out or even matches with anything on ww4. iv started playing a new game and buying coins from them.ill check inevery so offethen to see if it has changed . hopefully this rating will do it.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `P_RewardMania` |
| pred | `M_IntermediateCurrency` |
| **missed** | `P_RewardMania` |

**Did the model consider what it missed?**

- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes excessively long loading, which is a technical or service delay rather than a defined in-game timer or other coded mechanic. It also mentions a bonus feature that rarely appears or matches, but the meaning of “bonus lady” and “ww4” cannot be established from the review or the search results, so no reward-delivery label is assigned. The reviewer explicitly says they are buying coins from the game, describing real money being converted into in-game currency.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "buying coins from them"
  - why: The reviewer describes purchasing in-game coins with real money, which is the currency-acquisition pattern.

**Search:** `Cashman Casino "WW4" "bonus lady"` -> The search did not establish what “bonus lady” or “ww4” refers to in Cashman Casino, so those terms were not used to assign an additional label.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `2f50b132-9762-4f48-ae35-487f414aa41a` - MONOPOLY GO!

> Okay so I started playing in October of 2023. In the beginning, it was a fun game. Over time, I started to see the real issues in the game. 1. Most other players live by the motto you have to cheat to beat the game system and I am starting to feel they are right! 2. Events have become a joke. Peg-E is a total waste the new race car game is even worse! 3. Way to many gold duplicates! 4. Not enough trades a day! 5. Not enough dice.I could keep going but I only have 500 spaces, and I am at my limit

| | labels |
|---|---|
| gold | `P_RewardMania`, `S_Reciprocity` |
| pred | `S_Reciprocity` |
| **missed** | `P_RewardMania` |

**Did the model consider what it missed?**

- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review reports several complaints but only one clearly describes a coded mechanic. The statement about cheating describes other players' conduct and does not say the game rewards or incentivizes cheating. Peg-E and the race car game are named events, but no specific event mechanic is described. Gold duplicates indicate unwanted sticker copies, but the review does not describe the randomized delivery process or a compulsion to complete the collection. The complaint about limited daily trades does describe an in-game exchange of stickers with other players; a search confirms that MONOPOLY GO! treats duplicate stickers as tradable with friends and imposes a daily trade limit. That supports Reciprocity. The lack of dice is resource scarcity alone and does not establish a listed label.
```

**Labels assigned**

- `S_Reciprocity` - ok
  - span: "Not enough trades a day!"
  - why: The span describes a capped mechanic for trading resources with other players, which is an exchange-based favor mechanism.

**Search:** `MONOPOLY GO gold duplicates trades a day sticker packs` -> The search established that duplicate stickers in MONOPOLY GO! can be traded with friends and that the game imposes a daily trade limit, supporting the interpretation of 'trades' as player-to-player resource exchange. ([monopolygo.helpshift.com](https://monopolygo.helpshift.com/hc/en/3-monopoly-go/faq/276-duplicate-stickers/?pubDate=20250530&utm_source=openai))

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
The review describes Gardenscapes as an in-game match-three puzzle structure rather than the escape gameplay shown in advertising. The misleading advertisement is outside the app-design scope under R13, so it does not receive a label. Within the game, Austin's progress is tied to repeatedly playing the puzzle game to earn stars, and each game yields only one star; this names a repetitive activity required for character progress, supporting Grinding. The loss of points after failing a level is a failure penalty, but it does not describe a retention mechanic based on accumulated investment or a real-world time gate.
```

**Labels assigned**

- `T_Grinding` - ok
  - span: "Even for walking Austin you will have to earn a star by playing stupid game."
  - why: The player must repeatedly play the puzzle game to earn stars and advance Austin, which is a tedious task cycle required for progress.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (4)

### `3dc64fb0-3b6a-4ba1-9966-79c09f33069c` - Royal Kingdom

> I downloaded this app today after all the hype about the game being ad free. Total lies. Although the ads are seldom, so far, they are there all the same. What has put me off is the fact that to get out of the ad, you have to go into the play store, which then uses even more data.

| | labels |
|---|---|
| gold | `M_UIMisdirection` |
| pred | `M_UIMisdirection`, `T_Advertisement` |
| **spurious** | `T_Advertisement` |

**Model analysis**

```
The review describes advertisements appearing inside the game despite the game being promoted as ad free. The player is required to interact with the advertisement and enter the app store to exit it, so the ad is not merely mentioned but functions as a forced interruption. The exit path is also obstructed because closing the ad requires going somewhere else and consumes additional data. This supports Advertisement and UI Misdirection. The claim that the game was advertised as ad free concerns external marketing and is not coded under R13.
```

**Labels assigned**

- `M_UIMisdirection` - ok
  - span: "to get out of the ad, you have to go into the play store"
  - why: The ad obstructs the player's opt-out by routing the exit through the play store rather than providing a straightforward close control.
- `T_Advertisement` - **SPURIOUS**
  - span: "to get out of the ad, you have to go into the play store"
  - why: The player is compelled to interact with an in-game advertisement and cannot simply continue without going through the play store.

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
The review describes a competitive Ludo game in which the player plays against opponents. It also alleges that outcomes are deliberately manipulated: the player is supposedly meant to lose regardless of skill, with opponents receiving favorable dice counts while the reviewer receives unfavorable small counts. This is a claim that the game determines or tunes outcomes unfairly, which fits Illusion of Control. The separate mention of glitches is a technical complaint and does not itself create a dark-pattern label.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "if you are meant to lose, no matter how good you play you will definitley lose and in most of the cases this is the scene always..the opponents get good counts and you get small counts"
  - why: The reviewer alleges that the game fixes or manipulates dice outcomes so the player loses regardless of skill and opponents receive better counts.
- `S_Competition` - **SPURIOUS**
  - span: "the opponents get good counts and you get small counts"
  - why: The span explicitly describes the player competing against opponents in the game.

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
The review describes a daily mission system that limits what can be completed within the available attempts, implying a recurring daily task structure. It also describes an in-game timer that takes nearly two minutes to restore new chances to play, which imposes a wait before gameplay can continue. The complaint that items do not appear according to orders describes an unfavorable or possibly malfunctioning outcome, but it does not clearly establish a coded dark-pattern mechanic.
```

**Labels assigned**

- `T_DailyRewards` - **SPURIOUS**
  - span: "The daily missions are impossible to do in such less attempts"
  - why: The span identifies a daily mission system that constrains the player's tasks within a recurring daily cycle.
- `T_PlayingByAppointment` - ok
  - span: "it takes nearly 2 minutes for new chances to play"
  - why: New chances are restored only after an in-game timer, forcing the player to wait before playing again.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `6ccb26a7-01e3-41a3-ba1a-bddba2063257` - Lightning Link Casino Slots

> Dont even waste you time with this app. I dont understand why you guys make these things so fun to play but impossible to ever win. I mean I know your trying to make money on the app but why would I ever come back and spend more money when it is impossible to when. Because of that this app is garbage!!!!!!!

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `M_Gambling` |
| **spurious** | `M_Gambling` |

**Model analysis**

```
The review describes a casino slot game that is intentionally engaging but offers extremely poor chances of winning. The reviewer explicitly refers to returning to spend more money, so real money is being used in a luck-based game, which supports Gambling. However, the statement that winning is impossible is only a general complaint about outcomes; it does not describe rigging, near-misses, a fixed schedule, or a specific reward-delivery mechanism. It therefore does not support Illusion of Control, Optimism and Frequency Biases, or Reward Mania.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "why would I ever come back and spend more money when it is impossible to when"
  - why: The reviewer describes spending more money in a casino slots app, linking real-money participation to a luck-based chance game.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `T_MandatoryMarathon` | 3 | 0 |
| `P_RewardMania` | 2 | 0 |
| `S_Competition` | 1 | 1 |
| `M_UIMisdirection` | 2 | 0 |
| `S_Reciprocity` | 1 | 0 |
| `M_Gambling` | 0 | 1 |
| `M_EasyToPurchase` | 1 | 0 |
| `M_NeverEndingLure` | 1 | 0 |
| `T_DailyRewards` | 0 | 1 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `T_Advertisement` | 0 | 1 |

