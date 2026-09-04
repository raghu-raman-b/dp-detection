# Error review - gpt-5.6-luna_xhigh_teacher_v2_full

`gpt-5.6-luna` / reasoning `xhigh` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `aad355174ac4`  
micro-F1 **0.678** (P 0.769 / R 0.606) - **17 of 30** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 6 | said NONE, gold had labels |
| SWAP | 1 | picked different labels than gold |
| MISSED ONLY | 5 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 5 | found all gold, added extras |

## The diagnostic that matters

Of **13** missed labels, **3** (23%) were named in the model's own analysis and dropped anyway; **10** (77%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `M_UIMisdirection` | 1 | 3 |
| `S_Reciprocity` | 0 | 2 |
| `T_MandatoryMarathon` | 0 | 2 |
| `S_Competition` | 1 | 0 |
| `M_NeverEndingLure` | 0 | 1 |
| `M_WasteAversion` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `T_Advertisement` | 1 | 0 |

## Missed everything (predicted NONE) (6)

### `47cb4d59-0121-40f1-9ffc-220c458bd581` - Seaside Escape®: Merge & Story

> After just over a week of play, game is now gridlocked. Way too many new things on a tiny board. Ridiculous. Update: they finally started "archiving" but expect you to use your inventory space for them??? Hello?!? DELETE. Lots of witchcraft in this game, from astral events to evil eyes that I just unlocked. Although different from the ad I thought I was getting, the merging is delightful. Not enough energy to last very long, and the gems slow down a lot when you slow down on unlocking new items.

| | labels |
|---|---|
| gold | `M_WasteAversion` |
| pred | _NONE_ |
| **missed** | `M_WasteAversion` |

**Did the model consider what it missed?**

- `M_WasteAversion` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a merge-board and storage bottleneck: the board becomes overcrowded, archived objects still consume inventory space, and energy runs out quickly. It also says gem generation slows when unlocking slows, but does not state that gems are bought with real money or that energy is controlled by a stated timer. The ad mismatch concerns third-party advertising and is out of scope. The inventory complaint does not explicitly show items being destroyed, value being forfeited, or capacity being purchased; "DELETE" refers to deleting the app. No coded mechanic is therefore supported.
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
The reviewer describes buying a one-time weekly offer with real money, seeing the bank transaction succeed, and then not receiving the offer. This is a failed purchase-delivery or transaction problem, not a described mechanic such as a subscription, purchase prompt, limited-time scarcity tactic, or payment-gated progression. The complaint is about a missing purchased item, so no dark-pattern label is supported.
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
The reviewer describes more frequent popup screens, including a weekly challenge score notice and a quit-confirmation screen that must be dismissed before continuing. These screens are annoying interface friction, but the review does not connect them to purchases, spending, or an obstructed purchase opt-out, so M_UIMisdirection is not supported under its boundary rule. The mention that the cost increased does not identify a monetization mechanic such as paid progression, currency conversion, or a recurring fee. The weekly challenge reference does not explicitly describe competition, required scheduling, or expiring rewards. Therefore, no label is supported.
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

- `T_Advertisement` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes frequent in-game advertisements and pop-ups appearing one after another before gameplay can begin. However, the review does not say the ads are forced to be watched, offer rewards for viewing, or require payment to remove them. The pop-ups are not identified as purchase prompts, insufficient-funds prompts, or interface tricks that reduce purchase friction. Therefore, no coded mechanic is sufficiently supported.
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
The review describes technical failures rather than deliberate game mechanics: an update prevents catching raid bosses, accessing the friends list, opening or sending gifts, and functioning without repeated reinstalls. After changing devices, the account-recovery features also fail to find the user's information. The references to friends and gifts occur only as features broken by the malfunction, so they do not establish a social dark pattern under R11. No applicable label remains.
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
The review describes glitches and freezing that cause progress not to save, energy to be consumed without match progress, and the player to restart the game. These are explicitly attributed to bugs and technical faults rather than deliberate game mechanics. Under R11, the resulting loss of progress and energy does not support a dark-pattern label because the review does not establish that the same penalty would occur after a deliberate exit.
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
The review distinguishes between the external claim that the game is ad free, which is marketing material and not coded under R13, and the actual in-game behavior: advertisements appear, and leaving one requires entering the Play Store. That makes the player compelled to encounter the ad rather than freely dismissing it. No reward for watching ads, payment mechanic, currency conversion, or other coded design behavior is described.
```

**Labels assigned**

- `T_Advertisement` - **SPURIOUS**
  - span: "to get out of the ad, you have to go into the play store"
  - why: The ad cannot be exited normally; the player must enter the Play Store to leave it, making exposure to the advertisement compulsory.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (5)

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
The review describes an in-app starter-pack purchase appearing without the player tapping to buy and without the configured fingerprint or password confirmation. This is an unintended purchase caused by absent purchase confirmation, matching the Accidental Purchases indicator under Easy to Purchase. The reviewer only tentatively wonders whether it was a glitch, so the behavior is not definitively attributed to a technical fault that would suppress the label under R11.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "I didn't tap anything and my settings are set up to where I have to input my fingerprint or password to make a purchase and it did not do that."
  - why: The game allegedly completed a purchase without the player's tap or required authentication, describing an unintended purchase with no confirmation.

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
The review describes a recurring in-game advertisement interruption: an ad appears after every over, and the reviewer explicitly calls these ads forced. It also describes an accidental ad tap that closes the game and opens the advertisement, followed by restarting the app; this is attributed to bad app behavior or a UI issue, not a deliberate purchase or opt-out manipulation. The forced advertisement mechanic supports Advertisement, while the technical failure does not add another label.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "After every over, an ad pops up."
  - why: The game inserts recurring advertisements during play, and the review explicitly characterizes them as forced.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `2f50b132-9762-4f48-ae35-487f414aa41a` - MONOPOLY GO!

> Okay so I started playing in October of 2023. In the beginning, it was a fun game. Over time, I started to see the real issues in the game. 1. Most other players live by the motto you have to cheat to beat the game system and I am starting to feel they are right! 2. Events have become a joke. Peg-E is a total waste the new race car game is even worse! 3. Way to many gold duplicates! 4. Not enough trades a day! 5. Not enough dice.I could keep going but I only have 500 spaces, and I am at my limit

| | labels |
|---|---|
| gold | `P_RewardMania`, `S_Reciprocity` |
| pred | `P_RewardMania` |
| **missed** | `S_Reciprocity` |

**Did the model consider what it missed?**

- `S_Reciprocity` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes other players cheating, dissatisfaction with named events, repeated gold duplicates, a daily trade limit, and insufficient dice. The cheating accusation describes player behavior rather than a game mechanic that rewards harmful conduct. The event complaints are evaluations without a described mechanic. The duplicate-gold complaint implies repeated unwanted drops from a randomized reward pool, which matches Reward Mania. The trade and dice complaints state scarcity but do not explicitly show wasted currency, a purchase requirement, a wait timer, or a daily-login reward system. The final reference to 500 spaces is a review-length limit, not an in-game mechanic.
```

**Labels assigned**

- `P_RewardMania` - ok
  - span: "Way to many gold duplicates!"
  - why: The complaint identifies repeated unwanted gold drops, implying a reward system that can repeatedly deliver duplicates rather than desired collection items.

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
The review mainly describes misleading out-of-game advertising: the player installed Gardenscapes expecting an escape game but found a Candy Crush-style match-3 game. Under R13, that advertising misrepresentation is outside the app's scope and does not receive a label. Inside the game, the reviewer describes earning only one star per completed game and having to play the match-3 game to earn stars for actions involving Austin. This is a repetitive gameplay task required for progression, supporting Grinding. The loss of points after failing a level is a consequence of failure, not a described appointment, purchase gate, or exit penalty.
```

**Labels assigned**

- `T_Grinding` - ok
  - span: "Even for walking Austin you will have to earn a star by playing stupid game."
  - why: The reviewer must repeatedly play the match-3 game to earn stars needed for in-game progression involving Austin.

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
The reviewer describes an in-game advertisement that cannot be closed and blocks continued play until the app is closed and restarted. This is a forced or unskippable ad, so Advertisement applies. Restarting the app is described as a workaround, but no lost progress or exit penalty is stated, so Mandatory Marathon does not apply. The blocked close control is not connected to a purchase or purchase opt-out, so UI Misdirection does not apply.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "Can't close the ads, therefore can't continue playing"
  - why: The ad cannot be dismissed and prevents the player from continuing the game.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (5)

### `036954c0-447e-460d-b81e-f26f940b2ac4` - Shadow Fight 4: Arena

> On playing the Event game Mode and Duel Mode game will be strucked or Lagged and contlors are doesn't work properly while we playing the game and finally game has suddenly stopped and says YOU HAVE LOST and then nearly -30 to -50 gaming points are lessed from my Ranked game progress , these type of game shows golden coloured network icons near the Health bar, But my network signals are perfectly alright at that time while using other online apps , please rectify this problem as soon as possible.

| | labels |
|---|---|
| gold | `T_MandatoryMarathon` |
| pred | `S_Competition`, `T_MandatoryMarathon` |
| **spurious** | `S_Competition` |

**Model analysis**

```
The review primarily reports a technical malfunction: lag, unresponsive controls, and a sudden game stoppage are attributed to the game's network or technical failure, despite the reviewer saying their network works normally in other apps. The important design consequence is that the interrupted ranked match is recorded as a loss and deducts 30–50 points from ranked progress; under R11, the underlying match-forfeit penalty remains codable even though the malfunction triggered it. The mention of Duel Mode and ranked progress also describes competitive play. The golden network icons are only diagnostic indicators and do not describe UI misdirection, advertising, or monetization.
```

**Labels assigned**

- `S_Competition` - **SPURIOUS**
  - span: "Duel Mode game"
  - why: Duel Mode describes competitive match-based play.
- `T_MandatoryMarathon` - ok
  - span: "game has suddenly stopped and says YOU HAVE LOST and then nearly -30 to -50 gaming points are lessed from my Ranked game progress"
  - why: An interrupted ranked session is forcibly ended as a loss and the player forfeits accumulated ranked points.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `7732d254-0a39-4614-acf4-e67840e14b76` - Cashman Casino Slots Games

> loading takes entirely tooooo long also the bonus lady rarely comes out or even matches with anything on ww4. iv started playing a new game and buying coins from them.ill check inevery so offethen to see if it has changed . hopefully this rating will do it.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `P_RewardMania` |
| pred | `M_Gambling`, `M_IntermediateCurrency`, `P_RewardMania` |
| **spurious** | `M_Gambling` |

**Model analysis**

```
The review describes three mechanics. The long loading time is a technical performance complaint, not an in-game wait timer or an obscured mandatory download, so it does not receive a label. The complaint that the bonus lady rarely appears or matches describes an infrequent chance-based slot outcome, which is a variable reward delivery mechanic. The reviewer also says they are buying coins from the game; because coins are the acquired virtual currency, this supports Intermediate Currency, and in the slot-game context the purchased coins fund participation in chance-based play, supporting Gambling as well. The intention to check back occasionally and the hope that the rating changes the game do not describe FOMO, daily rewards, or another retention mechanic.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "bonus lady rarely comes out or even matches with anything on ww4. iv started playing a new game and buying coins from them"
  - why: The slot-game review links purchased coins with a chance-based bonus and matching outcome, indicating a paid stake in luck-based play.
- `M_IntermediateCurrency` - ok
  - span: "buying coins from them"
  - why: The reviewer describes acquiring virtual coins through a purchase, indicating real money is being converted into in-game currency.
- `P_RewardMania` - ok
  - span: "bonus lady rarely comes out or even matches with anything on ww4"
  - why: The bonus feature's infrequent appearance and unpredictable matching describe chance-based reward delivery.

**Search:** `Cashman Casino "bonus lady" WW4` -> No reliable result established what "bonus lady" or "ww4" specifically names in Cashman Casino, so the labels rely on the review's plain description and the supplied slot-game context.

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
The reviewer describes a competitive board game against opponents and claims that outcomes are deliberately manipulated so the player loses regardless of skill. The statements that the game is "meant to make you lose" and that good play cannot change the result assert rigged or concealed outcome determination, which supports Illusion of Control. The reference to opponents receiving better counts than the reviewer also establishes player-versus-player competition. The mention of glitches is attributed to technical faults and does not support a dark-pattern label.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "if you are meant to lose, no matter how good you play you will definitley lose"
  - why: The reviewer claims that the game fixes losses so skill cannot affect the result, implying concealed or manipulated outcome determination.
- `S_Competition` - **SPURIOUS**
  - span: "the opponents get good counts and you get small counts"
  - why: The review describes the player competing against opponents in the game.

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
The review is fragmented, but it describes a storage discrepancy: the game is presented as having a 1GB size while installing or running it fills the phone's storage. That implies the game's actual storage demand is substantially larger than the stated size, matching the hidden or fragmented download pattern. The comments about impressive graphics and fake pictures are evaluations or marketing claims, which are outside the in-game design scope and do not add labels.
```

**Labels assigned**

- `Tech_FragmentedDownloads` - **SPURIOUS**
  - span: "why you give the screen size 1GB my phone is storage full for this game"
  - why: The reviewer contrasts a stated 1GB size with the game filling the phone's storage, implying that the true storage requirement is concealed until installation or play.

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
The reviewer describes a casino slot game as enjoyable to play but says winning is effectively impossible. They also explicitly connect returning to the app with spending more money, which establishes paid participation in a chance-based game for the possibility of winning. The complaint does not describe a progress gate, virtual-currency conversion, or a specific manipulation of outcome determination, so no additional labels apply.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "why would I ever come back and spend more money when it is impossible to when"
  - why: The game is identified as casino slots, and this span links spending more money with attempting to win a chance-based reward.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_UIMisdirection` | 4 | 0 |
| `S_Competition` | 1 | 2 |
| `S_Reciprocity` | 2 | 0 |
| `M_Gambling` | 0 | 2 |
| `T_MandatoryMarathon` | 2 | 0 |
| `T_Advertisement` | 1 | 1 |
| `Tech_FragmentedDownloads` | 0 | 1 |
| `M_NeverEndingLure` | 1 | 0 |
| `M_WasteAversion` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |

