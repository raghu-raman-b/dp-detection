# Error review - gpt-5.6-luna_high_teacher_v2_full

`gpt-5.6-luna` / reasoning `high` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `aad355174ac4`  
micro-F1 **0.754** (P 0.821 / R 0.697) - **13 of 30** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 4 | said NONE, gold had labels |
| SWAP | 1 | picked different labels than gold |
| MISSED ONLY | 4 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 4 | found all gold, added extras |

## The diagnostic that matters

Of **10** missed labels, **2** (20%) were named in the model's own analysis and dropped anyway; **8** (80%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `T_MandatoryMarathon` | 1 | 2 |
| `M_EasyToPurchase` | 1 | 1 |
| `S_Reciprocity` | 0 | 1 |
| `S_Competition` | 0 | 1 |
| `M_UIMisdirection` | 0 | 1 |
| `M_NeverEndingLure` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |

## Missed everything (predicted NONE) (4)

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
The reviewer reports an apparent unintended purchase of a starter pack: the game notified them that they had bought it even though they did not tap anything and the expected fingerprint or password confirmation did not occur. However, the reviewer explicitly treats the incident as possibly a glitch rather than describing a deliberate purchase-by-default interface, missing confirmation design, or other intentional monetization mechanic. Under R11, a specific purchase failure attributed to a glitch or technical fault is not coded as a dark pattern.
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
The reviewer describes a failed purchase transaction: money was successfully taken from the bank, but the purchased weekly offer was not delivered. The missing offer is attributed to a transaction or delivery fault, and the request for a refund is not itself a game mechanic. The wording does not establish a recurring fee, artificial scarcity, easy-purchase interface, or any other coded design behavior.
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
The review describes technical malfunctions rather than deliberate game mechanics: an update prevents catching raid bosses, accessing the friends list, and opening or sending gifts; repeated reinstalls are needed to restore functionality; and account-recovery features fail to find the user's information. Under R11, these bug, update, and technical-fault attributions suppress dark-pattern labels, including any social or progression mechanics that are merely inaccessible because of the malfunction.
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
The review attributes the problems to glitches and bugs: matches freeze, the player must restart, and progress is not saved. The lost energy and absent match progress are described as consequences of the freezing malfunction, not as a deliberate rule that penalizes quitting or restarting. Under R11, technical-fault-attributed behavior is not coded as a dark pattern, and no separate functional mechanic is clearly described.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (1)

### `036954c0-447e-460d-b81e-f26f940b2ac4` - Shadow Fight 4: Arena

> On playing the Event game Mode and Duel Mode game will be strucked or Lagged and contlors are doesn't work properly while we playing the game and finally game has suddenly stopped and says YOU HAVE LOST and then nearly -30 to -50 gaming points are lessed from my Ranked game progress , these type of game shows golden coloured network icons near the Health bar, But my network signals are perfectly alright at that time while using other online apps , please rectify this problem as soon as possible.

| | labels |
|---|---|
| gold | `T_MandatoryMarathon` |
| pred | `S_Competition` |
| **missed** | `T_MandatoryMarathon` |
| **spurious** | `S_Competition` |

**Did the model consider what it missed?**

- `T_MandatoryMarathon` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes Event and Duel modes becoming unresponsive because of lag or a suspected network fault, followed by the game declaring a loss and deducting ranked points. The malfunction itself does not support a dark-pattern label under R11. Although the game applies a loss and point penalty, the review attributes that outcome to the technical failure and does not show that the same penalty would follow a deliberate exit or normal game rule. Duel Mode and ranked progress do indicate a competitive game structure, so Competition is supported.
```

**Labels assigned**

- `S_Competition` - **SPURIOUS**
  - span: "Duel Mode game"
  - why: Duel Mode describes gameplay structured around competition between players.

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
The reviewer describes an in-game advertisement appearing after every over, making ad viewing a recurring and forced part of play. The accidental tap, ad opening, app closure, and required restart are attributed to bad app behavior or a UI issue, so those technical faults do not independently receive a dark-pattern label under R11. The review does not describe a purchase prompt, deceptive control placement, or lost progress.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "After every over, an ad pops up."
  - why: An advertisement is imposed during gameplay after each over, making ad exposure a recurring forced interruption.

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

- `S_Competition` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes intrusive in-game pop-up screens. The weekly challenge score screen is only mentioned as a pop-up and does not by itself establish a coded mechanic. The quit-confirmation screens must be dismissed with an X before the player can continue, which is an interface obstruction requiring the player to clear an unwanted screen. The increased cost is not tied to a specific purchase or progression mechanic, so it does not support a monetary label.
```

**Labels assigned**

- `M_UIMisdirection` - ok
  - span: "are you sure you want to quit screens that you have to X out of before continuing"
  - why: The game forces the player to dismiss quit-confirmation screens before resuming play, obstructing the exit-related interface flow.

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

- `T_MandatoryMarathon` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes an in-game progression system where the player must repeatedly play a Candy Crush-style level to earn stars, including to advance Austin's story. Receiving only one star per game means progress depends on repeated play of the same type of activity, which supports Grinding. The loss of points after failing a level is a failure penalty, not a stopping or exit penalty, so it does not support Mandatory Marathon or Easy to Get, Hard to Lose. The misleading escape-game advertisement is third-party marketing and is outside the application's scope under R13, so it does not support Advertisement or another label.
```

**Labels assigned**

- `T_Grinding` - ok
  - span: "Always you play one game you just get one star only. And all your points get lost if you don't make that level. Even for walking Austin you will have to earn a star by playing stupid game."
  - why: The player must repeatedly complete the same game to earn stars and advance Austin's progression, making the activity a required and tedious progress loop.

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
The reviewer describes purchasing a large pack of in-game coins and receiving a refund after the purchase was accidental. Buying a coin pack indicates real money being converted into virtual currency, supporting Intermediate Currency. The accidental nature alone does not establish an interface design such as missing confirmation, a default purchase, or a deceptive control, so Easy to Purchase is not assigned. The review does not explicitly describe wagering money or chance-based rewards, so Gambling is not assigned.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "accidentally bought a huge coin pack"
  - why: The reviewer describes acquiring in-game coins through a purchase, implying real money was exchanged for virtual currency.

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
The review describes advertisements appearing inside the game despite the advertised claim that it was ad free. More specifically, the player cannot dismiss an ad normally: exiting it requires opening the Google Play Store, which obstructs the opt-out and causes additional data use. The ad is therefore a compelled in-game advertisement, and the forced store redirect is an interface-level obstruction to dismissing it.
```

**Labels assigned**

- `M_UIMisdirection` - ok
  - span: "to get out of the ad, you have to go into the play store"
  - why: The ad's dismissal path is obstructed by routing the player into the Play Store instead of providing a normal exit.
- `T_Advertisement` - **SPURIOUS**
  - span: "to get out of the ad, you have to go into the play store"
  - why: The player is required to interact with the advertisement and open the Play Store in order to exit it.

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
The reviewer describes a competitive board game with opponents whose rolls or counts are perceived as unequal: opponents receive good counts while the reviewer receives small counts. They also explicitly allege that the game determines losses regardless of player skill, describing a hidden or manipulated outcome rule rather than merely an unlucky streak. The mention of glitches is attributed to technical faults and does not itself support a dark-pattern label. The comments about time wasting, installing the game, and players reaching higher levels do not describe grinding, infinite progression, or a time-gated mechanic.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "if you are meant to lose, no matter how good you play you will definitley lose"
  - why: The reviewer alleges that outcomes are fixed or manipulated so player skill cannot affect the result.
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
The reviewer is praising the graphics but describes a storage-size mismatch: the game is presented as having a 1GB size, while downloading or running it appears to consume enough space to fill the phone and is associated with roughly 30GB of game data. This is a technical storage requirement rather than a gameplay or monetization mechanic, so the applicable label is Fragmented Downloads.
```

**Labels assigned**

- `Tech_FragmentedDownloads` - **SPURIOUS**
  - span: "why you give the screen size 1GB my phone is storage full for this game I am playing this game on Red magic 11 Pro because I will download it meaning in 30 gb games on it"
  - why: The span contrasts a stated 1GB game size with storage being filled and roughly 30GB of game data, implying that the true download requirement is much larger than advertised.

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
The review describes a casino-style game where the player is expected to spend real money while pursuing wins. The phrase about coming back to spend more money despite it being impossible to win implies a monetized chance-based activity, which supports Gambling. The review does not describe a specific rigging mechanism, variable reward delivery, progression barrier, or in-game currency, so no other label applies.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "why would I ever come back and spend more money when it is impossible to when"
  - why: The span explicitly connects spending real money with trying to win in a casino-slots game, indicating paid participation in a chance-based game for a possible reward.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `S_Competition` | 1 | 2 |
| `T_MandatoryMarathon` | 3 | 0 |
| `M_EasyToPurchase` | 2 | 0 |
| `S_Reciprocity` | 1 | 0 |
| `M_Gambling` | 0 | 1 |
| `Tech_FragmentedDownloads` | 0 | 1 |
| `M_UIMisdirection` | 1 | 0 |
| `M_NeverEndingLure` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `T_Advertisement` | 0 | 1 |

