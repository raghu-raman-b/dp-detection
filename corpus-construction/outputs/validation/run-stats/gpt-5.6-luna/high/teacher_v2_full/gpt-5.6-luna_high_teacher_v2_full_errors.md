# Error review - gpt-5.6-luna_high_teacher_v2_full

`gpt-5.6-luna` / reasoning `high` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `aad355174ac4`  
micro-F1 **0.774** (P 0.887 / R 0.686) - **41 of 75** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 12 | said NONE, gold had labels |
| SWAP | 3 | picked different labels than gold |
| MISSED ONLY | 18 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 8 | found all gold, added extras |

## The diagnostic that matters

Of **43** missed labels, **13** (30%) were named in the model's own analysis and dropped anyway; **30** (70%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `M_UIMisdirection` | 0 | 4 |
| `M_DeceptiveLuxury` | 0 | 3 |
| `M_IntermediateCurrency` | 1 | 2 |
| `P_RewardMania` | 0 | 3 |
| `T_MandatoryMarathon` | 1 | 2 |
| `S_Reciprocity` | 2 | 1 |
| `M_Gambling` | 1 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 2 |
| `T_Grinding` | 2 | 0 |
| `T_Advertisement` | 2 | 0 |
| `S_Competition` | 0 | 2 |
| `M_EasyToPurchase` | 1 | 1 |
| `M_NeverEndingLure` | 0 | 2 |
| `P_EasyToGetHardToLose` | 1 | 1 |
| `P_AestheticManipulation` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `P_IllusionOfControl` | 0 | 1 |
| `S_FriendSpamImpersonation` | 0 | 1 |
| `M_PayToProgress` | 0 | 1 |
| `S_ForcedFellowship` | 1 | 0 |
| `Tech_FragmentedDownloads` | 1 | 0 |
| `T_DailyRewards` | 0 | 1 |

## Missed everything (predicted NONE) (12)

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
The reviewer reports an unintended starter-pack purchase notification despite not tapping anything and despite purchase authentication being enabled. The reviewer explicitly raises the possibility that this was a glitch, so the described purchase is attributed to a possible technical malfunction rather than a deliberate purchase-by-default, missing-confirmation, or other dark-pattern design. No label applies under R11.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `c1a9f304-9cc1-4eb5-84f0-7988297fe423` - Lotsa Slots - Casino Games

> The game has gone downhill. The wins are not as big, or as often. The bonus when buying is smaller. If you are considering slot games there are less costly options with more wins

| | labels |
|---|---|
| gold | `M_Gambling`, `M_IntermediateCurrency`, `P_RewardMania` |
| pred | _NONE_ |
| **missed** | `M_Gambling`, `M_IntermediateCurrency`, `P_RewardMania` |

**Did the model consider what it missed?**

- `M_Gambling` - never mentioned -> **attention / recall**
- `M_IntermediateCurrency` - never mentioned -> **attention / recall**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer compares the game's current payouts with its earlier payouts and with other slot games. They describe smaller and less frequent wins and a reduced purchase bonus, but do not identify a specific mechanic such as real-money wagering, currency conversion, a progression gate, a recurring purchase, or a chance-based reward-delivery system. The comparison to less costly alternatives is an evaluation of value, not a described dark-pattern mechanic. No label is supported.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `97c23c8d-b858-4afa-83b1-ebd08d56badc` - Dice Dreams™️

> awesome the beginner packs really help get you started so you can see what can game offers in terms of gameplay, no surprises

| | labels |
|---|---|
| gold | `M_NeverEndingLure` |
| pred | _NONE_ |
| **missed** | `M_NeverEndingLure` |

**Did the model consider what it missed?**

- `M_NeverEndingLure` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer praises beginner packs because they help new players get started and allow them to preview the game's gameplay. The text does not state that the packs are paid, discounted as a first purchase, time-limited, required for progress, or followed by a later payment obligation. Therefore, no coded mechanic is explicitly supported.
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
The reviewer describes a one-time weekly offer purchased for R79,99, with money successfully taken from the bank, but the purchased offer was not delivered. This is a failed transaction or fulfillment problem rather than a deliberate game mechanic. The offer is also explicitly one-time, so it does not establish a recurring fee or any other listed dark-pattern mechanic. Under R11, no label applies when the specific behavior is a technical transaction fault.
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
The review describes frequent in-game pop-up screens, including a weekly challenge score screen and a quit-confirmation screen that must be closed before play can continue. These are interface annoyances, but the review does not connect them to purchases or to obstructing an opt-out from a purchase, so UI Misdirection is not supported by the boundary rule. The increased cost is mentioned without explaining what was made more expensive or how payment affects progress, so no monetary label applies.
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
The review describes frequent in-game advertisements and successive pop-ups delaying access to gameplay. However, it does not explicitly say the ads are forced, unskippable, or rewarded, so the Advertisement label is not supported. The pop-ups are not identified as purchase prompts, nor is an obstructed close or opt-out control described, so no monetary or UI-misdirection label applies. The complaint about ads being endless is evaluative and does not describe an in-game completion treadmill.
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

- `S_Reciprocity` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes technical malfunctions rather than deliberate game mechanics. The update allegedly prevents catching raid bosses, accessing the friends list, and opening or sending gifts; repeated reinstallations are used to restore functionality. The account-recovery features also fail to find the player's information after moving to a new tablet. Because these behaviors are explicitly attributed to an update, reinstall issue, or faulty password-reset process, R11 suppresses dark-pattern labels. The references to friends and gifts do not establish Reciprocity or another social mechanic because they describe features failing, not a functioning obligation or exchange.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `c2c60604-401f-416e-9489-a53cbaa6a968` - Chess - Play and Learn Online

> I'm having a very good experience with the game but whenever I end a game it sometimes show that i played brilliant moves but when I review it it doesn't show any brilliant move this wastes my free review I'm so disappointed with this please fix this and there should also be a system to cancel friend requests cause sometimes someone don't accept or decline so I can't send request to anyone else

| | labels |
|---|---|
| gold | `P_AestheticManipulation` |
| pred | _NONE_ |
| **missed** | `P_AestheticManipulation` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes two issues, both attributed to missing or inadequate functionality rather than deliberate game design. First, the game sometimes incorrectly reports brilliant moves, and reviewing the game consumes a free review without showing the claimed move; under R11 this is a bug-related malfunction, not a dark pattern. Second, pending friend requests cannot be cancelled, which prevents the player from sending another request, but this is a request-management limitation and does not describe recruitment pressure, social obligation, messaging, or impersonation. No meso label is supported.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fb70e577-e644-4af9-88a1-773476a5b805` - Free Fire: 9th Anniversary

> I use to love this game is was my best game I ever played, until now. It's difficult to play if you are using a low ram end device why?,It lag alot.When I approach a enemy it starts to lag like crazy.Enemies are hard to kill now. I never top up not even once. They were always keeping away free stuffs I was hype for the update but now, it just want you to top up to get this or that. They just want your money. I want the old free fire back where you can Play worldwide etc etc please fix bigs n etc

| | labels |
|---|---|
| gold | `M_IntermediateCurrency` |
| pred | _NONE_ |
| **missed** | `M_IntermediateCurrency` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes lag and bugs, explicitly attributing the difficulty to a low-RAM device and technical problems when approaching enemies. Under R11, those technical faults do not establish a dark-pattern label. The reviewer also says the game now withholds free items and wants players to top up to obtain unspecified things, but this is a general monetization complaint without a clear payment gate on progression, a paid advantage, a purchase prompt, or a defined item. No supported mechanic is explicit enough to label.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `681563e1-227c-4af2-8a1f-a145f3a795ca` - Pokémon GO

> This game has been good for years. But lately... My god. So glitchy. Can barely log into the game these days. Gift exchange screens are ridiculously slow. If you leave your phone for a few minutes, it's probably going to crash and require a restart. Get it together, folks...

| | labels |
|---|---|
| gold | `S_Reciprocity` |
| pred | _NONE_ |
| **missed** | `S_Reciprocity` |

**Did the model consider what it missed?**

- `S_Reciprocity` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes technical malfunctions rather than deliberate game design: difficulty logging in, very slow gift-exchange screens, and crashes after leaving the phone idle that require restarting. Under R11, these bug, performance, and crash reports do not support dark-pattern labels. The gift exchange is merely mentioned as a malfunctioning screen, with no reciprocity mechanic or other qualifying design behavior described.
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
The review describes technical malfunctions rather than deliberate game mechanics: glitches, freezing when starting a game, unsaved win progress, and energy being lost after the freeze. The lost progress is explicitly attributed to bugs and failure to save, so R11 suppresses labels for penalties that arise from the malfunction itself. There is no clear deliberate timer, exit penalty, daily reward, or other codable design behavior.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `2d118652-5693-499a-8f3f-d02d0b405cd4` - BGMI: FPS Battle Royale

> Dear BGMI Support Team, I am facing a persistent bug regarding the resource download system in the game. Maps, outfits, and other resource packs are downloading automatically in the background. The main issue is that even when I manually go to the settings and turn OFF the "Auto-Download" feature, the game ignores the setting and continues to download files automatically. This is consuming a lot of my internet data and causing storage issues on my device. Please fix this bug as soon as possible

| | labels |
|---|---|
| gold | `Tech_FragmentedDownloads` |
| pred | _NONE_ |
| **missed** | `Tech_FragmentedDownloads` |

**Did the model consider what it missed?**

- `Tech_FragmentedDownloads` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a technical malfunction: resource packs such as maps and outfits download automatically in the background even after the player disables Auto-Download. Although this causes internet-data and storage consumption, the behavior is explicitly attributed to a persistent bug rather than a deliberate game design choice. It also does not establish Fragmented Downloads because there is no obscured advertised size, download wall, or missing-assets prompt; therefore no label applies under R11.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (3)

### `2471db11-2c61-415a-8af4-33b80a05c759` - Clash of Clans

> The balancing makes this game have no point. So many bugs, to many sales, support is non existent. You will spend months upgrading troops and defenses just to be nerfed. I have a maxed out account and anyone can destroy me. The more you play the game the more it penalizes you. Reduced times for people that don't play as much. Every account recieves different reward amounts. I've played over 10 years, it's just a chore at this point, not fun. They ruin COC more with every update and event.

| | labels |
|---|---|
| gold | `M_PowerCreep`, `T_Grinding` |
| pred | `M_PowerCreep`, `S_Competition` |
| **missed** | `T_Grinding` |
| **spurious** | `S_Competition` |

**Did the model consider what it missed?**

- `T_Grinding` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a multiplayer combat system in which other players can destroy the reviewer's base, so the game places players in direct competition. It also describes troops and defenses that require months of upgrading before being nerfed, meaning invested game assets lose value after acquisition through balancing updates; this matches Power Creep. The mentions of bugs, sales, support, differing reward amounts, and general frustration do not identify additional qualifying mechanics. The long play history and chore-like experience do not by themselves show Grinding or Easy to Get, Hard to Lose.
```

**Labels assigned**

- `M_PowerCreep` - ok
  - span: "You will spend months upgrading troops and defenses just to be nerfed."
  - why: Troops and defenses that took months to upgrade are subsequently nerfed, reducing the value of the player's prior investment.
- `S_Competition` - **SPURIOUS**
  - span: "I have a maxed out account and anyone can destroy me."
  - why: The span describes other players attacking and destroying the player's account, showing direct player-versus-player competition.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `036954c0-447e-460d-b81e-f26f940b2ac4` - Shadow Fight 4: Arena

> On playing the Event game Mode and Duel Mode game will be strucked or Lagged and contlors are doesn't work properly while we playing the game and finally game has suddenly stopped and says YOU HAVE LOST and then nearly -30 to -50 gaming points are lessed from my Ranked game progress , these type of game shows golden coloured network icons near the Health bar, But my network signals are perfectly alright at that time while using other online apps , please rectify this problem as soon as possible.

| | labels |
|---|---|
| gold | `T_MandatoryMarathon` |
| pred | `S_Competition` |
| **missed** | `T_MandatoryMarathon` |
| **spurious** | `S_Competition` |

**Did the model consider what it missed?**

- `T_MandatoryMarathon` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes Event and Duel modes becoming lagged or unresponsive, followed by the game declaring a loss and deducting ranked points. The lag, failed controls, network warning, and sudden stoppage are explicitly attributed to a technical problem, so they do not independently support dark-pattern labels under R11. However, Duel Mode is a competitive game mode, and the ranked-point system shows competition between players. The review does not establish that voluntarily exiting would cause the same point loss, so Mandatory Marathon is not assigned.
```

**Labels assigned**

- `S_Competition` - **SPURIOUS**
  - span: "Duel Mode"
  - why: Duel Mode identifies a game mode built around competing against another player.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `042ee18e-d78e-4a0f-9cc2-2b1e10cc46e6` - Total Battle: War Strategy

> Sometimes, it feels like 'Groundhog Day', meaning that I show up, complete tasks, spend gold and potion, spend real money, then come back tomorrow and do it all over again. It's a way to get you drawn in and invested in the game, so you feel obligated to keep playing. There is no real progress or advancement; there is no pot of gold at the end of this rainbow.

| | labels |
|---|---|
| gold | `P_EasyToGetHardToLose`, `T_Grinding`, `T_InfiniteTreadmill` |
| pred | `P_EasyToGetHardToLose`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| **missed** | `T_Grinding` |
| **spurious** | `T_PlayingByAppointment` |

**Did the model consider what it missed?**

- `T_Grinding` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a recurring daily gameplay obligation: the player shows up, completes tasks, consumes resources and money, then returns the next day to repeat the same cycle. The repeated schedule is imposed by the game, supporting Playing by Appointment. The reviewer also explicitly says the cycle creates investment and an obligation to continue, which supports Easy to Get, Hard to Lose. The statement that there is no real advancement or endpoint describes an ongoing game loop with no attainable completion, supporting Infinite Treadmill. Daily Rewards is not assigned because no daily login reward, streak, or penalty for missing a day is described. Grinding is not assigned because the reviewer explicitly says the repeated tasks produce no real progress, rather than describing repetitive work required to advance.
```

**Labels assigned**

- `P_EasyToGetHardToLose` - ok
  - span: "It's a way to get you drawn in and invested in the game, so you feel obligated to keep playing."
  - why: The game builds player investment and makes that investment create an obligation to continue playing.
- `T_InfiniteTreadmill` - ok
  - span: "There is no real progress or advancement; there is no pot of gold at the end of this rainbow."
  - why: The review describes a continuing gameplay loop with no meaningful advancement or attainable endpoint.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "then come back tomorrow and do it all over again"
  - why: The player is expected to return on the game's daily schedule and repeat the same activities rather than play only at personally chosen times.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (18)

### `2fd4ef32-a33b-44ed-a921-2889ba6e0375` - Ludo King®

> Dice rolls are not random at all, they are preplanned. Game randomly decides at the start of the play that which player has to win and dice rolls according to it. You also will know at the beginning of the game that who is going to win. One player will get more and more 6s and another one will get 1 or 2 mostly. The rolls have gone predictable. That's why I have uninstalled the game today. It's frustrating.

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_Competition` |
| pred | `P_IllusionOfControl`, `S_Competition` |
| **missed** | `P_OptimismAndFrequencyBiases` |

**Did the model consider what it missed?**

- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a competitive dice game in which players face one another to determine a winner. It also explicitly alleges that the outcome is fixed in advance: the game chooses which player will win at the start and then manipulates the dice rolls to produce that result. The predictable pattern of one player receiving mostly sixes and another mostly ones or twos is presented as evidence of concealed, non-random outcome determination, so this supports Illusion of Control. No monetary stake, reward-delivery system, or merely unlucky streak is described.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "Game randomly decides at the start of the play that which player has to win and dice rolls according to it."
  - why: The span alleges that the game secretly determines the winner in advance and tunes the dice rolls to that hidden outcome.
- `S_Competition` - ok
  - span: "which player has to win"
  - why: The review explicitly describes players competing against one another for a winner-determined match outcome.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `86de0e5d-8187-4dfd-b8c3-05e5b271d89e` - Real Cricket™

> I would have given negative ratings if possible. Too much ads are shown after every over and every wicket fell. Opponent takes catches very easily while our team drops all the catches except one or two. Worst game, totally wasting of Data and time. Please don't go for it.

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `T_Advertisement` |
| pred | `T_Advertisement` |
| **missed** | `P_IllusionOfControl` |

**Did the model consider what it missed?**

- `P_IllusionOfControl` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes advertisements appearing automatically after each over and each fallen wicket, making the player encounter repeated in-game ads during normal play. This supports Advertisement because the ads are imposed at recurring gameplay points. The complaint that the opponent catches easily while the player's team drops catches expresses perceived unfairness, but it does not explicitly describe rigging, concealed outcome determination, or another coded mechanic. The references to wasting data and time are general evaluations rather than additional mechanics.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "Too much ads are shown after every over and every wicket fell."
  - why: Ads are automatically shown during normal gameplay after recurring cricket events, compelling the player to encounter them.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `e92fc4f7-bdda-4f54-a8e2-aa591fbc7945` - Shadow Fight 4: Arena

> It's a fun game, but takes quite a long time to unlock new heros...I have done close to 100 fights and still have the first two heros you get when you start the game. Also the "share to unlock this hero" won't unlock the hero for me. So I'm thinking about installing the app.

| | labels |
|---|---|
| gold | `S_FriendSpamImpersonation`, `T_Grinding` |
| pred | `T_Grinding` |
| **missed** | `S_FriendSpamImpersonation` |

**Did the model consider what it missed?**

- `S_FriendSpamImpersonation` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes repeated fights being required to unlock additional heroes, with nearly 100 fights producing little or no progress beyond the two starting heroes. This is a repetitive activity tied directly to advancement, so it supports Grinding. The failed "share to unlock" behavior is explicitly reported as not working, making it a bug or technical fault rather than a deliberate dark pattern. The review does not establish payment, social recruitment, messaging, or competition against other players.
```

**Labels assigned**

- `T_Grinding` - ok
  - span: "I have done close to 100 fights and still have the first two heros you get when you start the game"
  - why: The reviewer has repeatedly completed fights to unlock heroes, showing a monotonous progress activity rather than merely stating that progress is slow.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `c63003ef-dcdd-4ef2-a54e-0c9b0dfe931a` - Kingshot

> The game is very meh. The ads are much more fun than the actual game, and make up only a tiny portion of it. Still, I decided to persist for a few days to see how it went, and all the game ever had me do what click to upgrade this or research that or go there. Even after such a short time, there were already so many things that it wad impossible to keep track of them without relying on the daily quests and such. It's really not my cup of tea

| | labels |
|---|---|
| gold | `T_DailyRewards`, `T_Grinding`, `T_PlayingByAppointment` |
| pred | `T_Grinding` |
| **missed** | `T_DailyRewards`, `T_PlayingByAppointment` |

**Did the model consider what it missed?**

- `T_DailyRewards` - never mentioned -> **attention / recall**
- `T_PlayingByAppointment` - never mentioned -> **attention / recall**

**Model analysis**

```
The external advertisements are described as more entertaining than the game, but under R13 that out-of-game marketing is excluded. Within the game, the reviewer describes a repetitive loop of clicking upgrades, conducting research, and moving to locations, with these activities occupying essentially all gameplay. The mention of daily quests only describes using them to keep track of numerous tasks; it does not establish a daily reward incentive or penalty.
```

**Labels assigned**

- `T_Grinding` - ok
  - span: "all the game ever had me do what click to upgrade this or research that or go there"
  - why: The reviewer describes gameplay as an ongoing cycle of repetitive upgrade, research, and movement tasks.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `57add346-8b93-4249-be50-1a39331cf79b` - RAID: Shadow Legends

> These are my views of the game after playing for almost a day. I didnt make a single purchase but got a free champion and silver from a referral. Pros: Easy to learn the controls and layout of the game, nice story line, easy combat system, no lag, nice champion designs and gameplay. Cons: Every single time you log in you are bombarded with pop ads advertising "special" or "limited time" deals, once your champions hit level 30 it becomes a horrible grind, p2p is the best way to win this game.

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury`, `M_PayToProgress`, `S_ForcedFellowship` |
| pred | `M_DeceptiveLuxury`, `M_PayToProgress` |
| **missed** | `S_ForcedFellowship` |

**Did the model consider what it missed?**

- `S_ForcedFellowship` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes three relevant mechanics or possible mechanics. The game presents limited-time purchase deals on login, which uses artificial scarcity and urgency. It also states that paying is the best way to win, indicating that spending provides an in-game advantage and supports Pay to Progress. The referral mention describes receiving a free champion and silver, but it does not explicitly say the player is rewarded for inviting new players, so Forced Fellowship is not assigned. The login pop-ups are purchase solicitations, not forced ad viewing or a clearly described friction-reducing purchase interface, so Advertisement and Easy to Purchase are not assigned. Finally, calling the late game a grind does not identify a specific repetitive task required for progress, so Grinding is not assigned.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: ""limited time" deals"
  - why: The game frames purchase offers as limited-time deals, creating urgency through manufactured scarcity.
- `M_PayToProgress` - ok
  - span: "p2p is the best way to win this game."
  - why: The reviewer states that paying is the best route to winning, implying a gameplay advantage from spending.

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
The review describes an in-game advertisement that is forced after every cricket over, so advertising interrupts normal gameplay. The app closing after an accidental tap is attributed to bad app behavior or a technical issue, so that malfunction does not create a separate dark-pattern label and does not suppress the independent forced-ad mechanic. The request to stop the ads or fix the UI is hypothetical and is not coded.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "After every over, an ad pops up."
  - why: An advertisement is imposed during gameplay after every over, describing a forced in-game ad interruption.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `da13d098-3944-4e0b-aa94-c064a56edd83` - Mystery Town: Merge Games

> the game is fun at first but it's so boring later on, you can't do anything without using in app purchases. you will never be able to complete the card packs and other mini games without being forced to pay real money for it. the energy cap will barely get you midway through an order unless you use all your gems. like everything just feels like a trap to get you to spend real money and it's so dumb.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `M_PayToProgress`, `P_CompleteTheCollection` |
| pred | `M_PayToProgress`, `P_CompleteTheCollection` |
| **missed** | `M_IntermediateCurrency` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes progress being blocked unless the player makes real-money purchases. It also describes card packs as a collection the player is expected to complete, with completion said to be impossible without payment. The energy cap limits how far the player can advance through an order, but no explicit timer or regeneration schedule is stated, so Playing by Appointment is not assigned. The mention of gems does not clearly state that real money is converted into gems, so Intermediate Currency is not assigned. General frustration about feeling trapped into spending does not by itself establish Easy to Purchase or another label.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "you can't do anything without using in app purchases. you will never be able to complete the card packs and other mini games without being forced to pay real money for it."
  - why: The reviewer explicitly says continued activity and completion of game content are impossible without real-money payment.
- `P_CompleteTheCollection` - ok
  - span: "you will never be able to complete the card packs"
  - why: Card packs are described as a collection that the player is trying to complete.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a59f5319-a1b7-4991-8c6b-d2d2ca56265c` - Fate/Grand Order (English)

> It's an unregulated casino. Every part of the game is set up to direct you towards the slot machine summoning system. Story? Free buffet and show to keep you interested. Plus, you like this character? Well, either hope you have godly luck, or fork over some cash (~$140 for 50% to get a 'rate up' character), because the majority of them are limited time only. Gameplay is mostly just grind to build sunk cost. That, and an incentive to roll the slots for things to reduce the amount of grind.

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury`, `M_Gambling`, `M_PayToProgress`, `M_UIMisdirection`, `P_EasyToGetHardToLose`, `P_RewardMania` |
| pred | `M_DeceptiveLuxury`, `M_Gambling`, `P_EasyToGetHardToLose`, `P_RewardMania` |
| **missed** | `M_PayToProgress`, `M_UIMisdirection` |

**Did the model consider what it missed?**

- `M_PayToProgress` - never mentioned -> **attention / recall**
- `M_UIMisdirection` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a monetized chance-based summoning system: players may spend about $140 for only a 50% chance of obtaining a rate-up character, which supports Gambling. The slot-machine framing and the incentive to keep rolling for rewards that reduce grind support Reward Mania because engagement is sustained by repeated, unpredictable reward delivery. The statement that most characters are limited-time only describes artificial scarcity tied to obtaining them, supporting Deceptive Luxury. Finally, the game is described as making players grind in order to build sunk cost, implying accumulated time investment that makes leaving harder, supporting Easy to Get, Hard to Lose. The review does not identify a specific repetitive activity beyond the general word 'grind,' so Grinding is not assigned under its boundary rule; nor does it explicitly state that payment is required for progression outside the chance mechanic.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "because the majority of them are limited time only"
  - why: Characters are made available only temporarily, creating manufactured scarcity around obtaining them.
- `M_Gambling` - ok
  - span: "hope you have godly luck, or fork over some cash (~$140 for 50% to get a 'rate up' character)"
  - why: The player can spend real money for only a stated 50% chance of receiving a desired character.
- `P_EasyToGetHardToLose` - ok
  - span: "Gameplay is mostly just grind to build sunk cost."
  - why: The review explicitly describes gameplay as building sunk cost, implying that accumulated investment raises the cost of quitting.
- `P_RewardMania` - ok
  - span: "slot machine summoning system"
  - why: The summoning system is framed as a slot-machine-like, repeated chance-based reward mechanism that sustains engagement.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `03e1dcd5-9c13-4b7f-a9e1-d2ebdc8f5773` - Disney Solitaire

> This is incredibly rigged; designed to get you hooked early to develop into impossibility, to suck you into paying money. You can be down to one card and have 10 cards left in your deck and end up going through those 10 cards and still have one card left. Even if you pay the astronomical coins to get another handful of cards, you still have the same card left. If you were to take an actual deck of cards, your chances would be significantly higher. Don't install this game. It's a money scam.

| | labels |
|---|---|
| gold | `M_Gambling`, `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `P_RewardMania` |
| pred | `P_IllusionOfControl` |
| **missed** | `M_Gambling`, `P_OptimismAndFrequencyBiases`, `P_RewardMania` |

**Did the model consider what it missed?**

- `M_Gambling` - considered and rejected -> **rule interpretation**
- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a solitaire draw mechanic that the player believes is deliberately manipulated: after reducing the board to one remaining card, drawing through the remaining deck still fails to provide the needed card, and purchasing additional cards leaves the same obstacle in place. The explicit claim that the game is "rigged" and the repeated outcome assertion support Illusion of Control because the game is said to conceal or manipulate how outcomes are determined. The review also mentions paying coins for more cards, but it does not clearly establish that real-world money is converted into those coins or that the payment is required for progression rather than an optional continuation, so no monetary label is assigned. No grinding, gambling, reward-delivery, or infinite-completion mechanic is clearly described.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "This is incredibly rigged"
  - why: The reviewer explicitly alleges that the game's card outcomes are rigged rather than determined fairly or randomly.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `f09401aa-1aef-4c8b-ac3a-92eec49af44d` - Homescapes

> I like the satisfaction of finishing the puzzles and renovating rooms a lot, but I hate how the game tries to force you to be competitive. every time you lose the game reminds you that unless you pay up, you're going to go down on the leaderboard and will lose all your winning streak rewards. it makes you feel bad for not winning every level on the first attempt. I just want to enjoy playing a casual puzzle game, and I think there should be opt out of the leaderboard system.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `P_EasyToGetHardToLose`, `S_Competition`, `S_FearOfMissingOutFOMO` |
| pred | `M_PayToProgress`, `S_Competition`, `S_FearOfMissingOutFOMO` |
| **missed** | `P_EasyToGetHardToLose` |

**Did the model consider what it missed?**

- `P_EasyToGetHardToLose` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a leaderboard that ranks players against one another, so the game is explicitly competitive. Losing a level threatens both leaderboard position and accumulated winning-streak rewards, creating pressure to keep winning. The reviewer also says payment is the way to avoid dropping on the leaderboard, which describes spending for a competitive advantage or status. The threat of falling behind and losing rewards supports Fear of Missing Out. The statement that the game makes the player feel bad is an evaluation of the mechanic's emotional effect, not by itself a separate label.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "unless you pay up, you're going to go down on the leaderboard"
  - why: Payment is presented as the way to preserve leaderboard standing and gain a competitive advantage.
- `S_Competition` - ok
  - span: "force you to be competitive"
  - why: The game explicitly places players in competition through its leaderboard system.
- `S_FearOfMissingOutFOMO` - ok
  - span: "you're going to go down on the leaderboard and will lose all your winning streak rewards"
  - why: The game pressures the player by threatening that stopping or failing to win will cause them to fall behind and lose rewards.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b0a2aece-2b3e-4026-966b-7836e3cfc6bc` - Genshin Impact

> I love the game, I invested so much time and effort in it. I genuinely love the art and designs but recently ever since Fontaine arrived the characters started becoming expensive because of premium team comps and some being locked and good for a specific team. old characters started falling off which I hope they could climb back up. And now the Meta shifts now are extremely fast.. and another issue is how much rewards we get.. it's so low each patch barely gives us enough to hit hard pity.

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury`, `M_PowerCreep`, `P_EasyToGetHardToLose`, `P_RewardMania` |
| pred | `M_PowerCreep`, `P_RewardMania` |
| **missed** | `M_DeceptiveLuxury`, `P_EasyToGetHardToLose` |

**Did the model consider what it missed?**

- `M_DeceptiveLuxury` - never mentioned -> **attention / recall**
- `P_EasyToGetHardToLose` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes a live-service character system in which newer characters require expensive or narrowly defined team compositions, while older characters lose effectiveness as the meta changes rapidly. This is devaluation of previously acquired characters over time, matching Power Creep. The review also names a hard-pity system and describes patch rewards in relation to reaching that threshold; the pity mechanic is a gacha reward-delivery structure, so it supports Reward Mania. The reviewer mentions substantial time investment, but does not say that this investment makes quitting difficult, so Easy to Get, Hard to Lose does not apply. Low rewards alone do not create a label beyond the explicit pity mechanic.
```

**Labels assigned**

- `M_PowerCreep` - ok
  - span: "old characters started falling off"
  - why: Previously acquired characters are described as losing effectiveness over time as newer meta requirements emerge.
- `P_RewardMania` - ok
  - span: "barely gives us enough to hit hard pity"
  - why: The span identifies a hard-pity threshold governing the delivery of character rewards in the game's gacha system.

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
The review complains that the advertised escape gameplay is not what appears in Gardenscapes; this is third-party advertising and is out of scope under R13. Within the game, Austin's progression is tied to repeatedly playing a Candy Crush-style minigame to earn stars, with only one star awarded per game. The statement that points are lost when a level is not completed describes failure-related loss, but it does not show a stopping penalty, a daily schedule, or another codable mechanic.
```

**Labels assigned**

- `T_Grinding` - ok
  - span: "Always you play one game you just get one star only. And all your points get lost if you don't make that level. Even for walking Austin you will have to earn a star by playing stupid game."
  - why: Progressing Austin requires repeatedly playing the same level-based minigame to earn stars, making a repetitive task necessary for advancement.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b6745663-5486-4e5b-9066-8a889055d8bc` - Travel Town - Merge Adventure

> it's a good hook. the completionist in me wants to get every level, and the matching is satisfying enough to really tempt me into buying gems/energy to play more. I wish there was a way to disable all the event pop-ups. opening the app and then having to click away ten different challenges is very annoying. at least there are no outside ad pop-ups but I would rather have more optional outside ads than the unskippable events. please consider having a dismiss option for the events! good game.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `M_PayToProgress`, `M_UIMisdirection` |
| pred | `M_IntermediateCurrency`, `M_PayToProgress` |
| **missed** | `M_UIMisdirection` |

**Did the model consider what it missed?**

- `M_UIMisdirection` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a merge game whose energy system limits how much they can play, while purchasing gems or energy is presented as a way to continue playing beyond that limit. This supports Pay to Progress because payment removes a barrier to continued gameplay, and Intermediate Currency because gems are an in-game currency that can be bought. The event pop-ups are annoying and unskippable, but they are not described as purchase prompts or as preventing the player from ending a session, so they do not support another label. The mention of outside ads is explicitly about their absence and a hypothetical preferred alternative, so it is not codable.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "buying gems/energy"
  - why: The reviewer describes acquiring the in-game currency or resource gems through a purchase.
- `M_PayToProgress` - ok
  - span: "really tempt me into buying gems/energy to play more"
  - why: Buying energy or gems is presented as the paid way to bypass the play limitation and continue playing.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `64e4aba6-ce6d-420a-b5cb-4422c11c4186` - Yalla Ludo - Ludo&Jackaroo

> Hello, I recommend improving the "Auto Playing" feature through "Bot". If the first player isn't responding or playing, the second player at the end have to exit and lose his credits because there are no limitations are for the Bot. Some players can also misuse this feature to grab the credits of the corresponding players. I think you must consider it, next it's up to your development team :-) Regards

| | labels |
|---|---|
| gold | `S_Competition`, `S_EncouragesAntiSocialBehavior`, `T_MandatoryMarathon` |
| pred | `S_EncouragesAntiSocialBehavior`, `T_MandatoryMarathon` |
| **missed** | `S_Competition` |

**Did the model consider what it missed?**

- `S_Competition` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a multiplayer match rule involving an auto-playing bot. When the first player stops responding, the second player is forced to exit and loses credits, so ending the session at the player's chosen moment carries a deliberate forfeiture penalty. It also describes other players misusing the bot feature to take the corresponding player's credits, showing harmful conduct that produces an in-game gain. No other label is clearly supported.
```

**Labels assigned**

- `S_EncouragesAntiSocialBehavior` - ok
  - span: "Some players can also misuse this feature to grab the credits of the corresponding players"
  - why: The feature enables players to exploit other players and obtain their credits as a result.
- `T_MandatoryMarathon` - ok
  - span: "the second player at the end have to exit and lose his credits"
  - why: The player cannot end the match freely because exiting causes a loss of credits.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `71d54398-28c7-4f4a-a67d-0914206f59c6` - GODDESS OF VICTORY: NIKKE

> Gacha is quite scummy. If you started with no currency and wanted a guaranteed unit, it's 200 tickets. You get about 20 tickets with $80 so even being generous it's still $600-$800 just to guarantee the unit you want. 4% chance to pull any SSR at any time. In a 10-pull that's around a 33% chance give or take. I failed that 15 times in a row, so 150 pulls with no SSR (supposedly 1/456 chance of happening) . Great system. Really makes players not want to quit or anything.

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury`, `M_Gambling`, `M_IntermediateCurrency`, `P_RewardMania` |
| pred | `M_Gambling`, `M_IntermediateCurrency`, `P_RewardMania` |
| **missed** | `M_DeceptiveLuxury` |

**Did the model consider what it missed?**

- `M_DeceptiveLuxury` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a paid ticket currency being used for gacha pulls: real money buys tickets, tickets fund attempts, and each attempt has a chance of producing an SSR unit, with 200 tickets needed for a guarantee. This supports Gambling because money enters a chance-based reward mechanic, Intermediate Currency because real money is converted into tickets, and Reward Mania because the game uses gacha pulls and unpredictable outcomes. The 15 failed attempts are an unlucky run, not evidence that the game manipulates outcomes, so Illusion of Control does not apply. The guaranteed unit is obtained within the gacha system rather than through a separate progression gate, so Pay to Progress does not apply.
```

**Labels assigned**

- `M_Gambling` - ok
  - span: "You get about 20 tickets with $80 so even being generous it's still $600-$800 just to guarantee the unit you want. 4% chance to pull any SSR at any time."
  - why: The review links real-money spending to ticket-funded pulls whose SSR outcome is determined by chance.
- `M_IntermediateCurrency` - ok
  - span: "You get about 20 tickets with $80"
  - why: Tickets are an in-game currency acquired with real money.
- `P_RewardMania` - ok
  - span: "Gacha is quite scummy."
  - why: The reviewer explicitly identifies a gacha system, which is a chance-based reward-delivery mechanic.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `cbcde992-08aa-4bfb-a653-a944e4b733aa` - Mech Arena - Shooting Game

> Every time you open the main menu you get a minimum of 10 pop up ads to buy gear/equipment with small x buttons in the corner. Edit: the developer responded to this review. It would be great if the frequency of offers was reduced: 2 or 3 max. My concern is if i did purchase something, Id get even more pop-ups! I didn't want to buy the first 9 items, I certainly dont want the last one any more.

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `M_UIMisdirection` |
| pred | `M_UIMisdirection` |
| **missed** | `M_EasyToPurchase` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes repeated in-game purchase offers appearing whenever the main menu is opened. The offers are not advertisements viewed in a third-party app, so T_Advertisement does not apply. The important design behavior is that the purchase pop-ups have very small close controls, obstructing the opt-out and making dismissal harder; this is UI Misdirection. The review does not explicitly describe accidental purchases, default purchases, insufficient-funds prompts, or payment being required for progress, so M_EasyToPurchase and M_PayToProgress are not assigned.
```

**Labels assigned**

- `M_UIMisdirection` - ok
  - span: "pop up ads to buy gear/equipment with small x buttons in the corner"
  - why: The purchase offers are presented through pop-ups whose small close buttons make opting out difficult.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `49a53e7c-0564-46c6-995f-1d8bc418c80a` - MONOPOLY GO!

> I used to love this game but the new sticker album has been made to be to difficult to get the non tradable gold cards, I have been needing only gold cards for two months now and have only been awarded one new card in that time, and the golden blitz has never been a card that I am in need of. After this album I will no longer be playing the game due to this and the fact that events are just too hard to finish with the small amount of dice you get in the game. It just is no longer fun anymore

| | labels |
|---|---|
| gold | `P_CompleteTheCollection`, `P_RewardMania`, `S_Reciprocity` |
| pred | `P_CompleteTheCollection` |
| **missed** | `P_RewardMania`, `S_Reciprocity` |

**Did the model consider what it missed?**

- `P_RewardMania` - never mentioned -> **attention / recall**
- `S_Reciprocity` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a sticker album as a collection goal and says the player is missing only gold cards, which indicates a drive to complete the collection. A search established that Golden Blitz is a limited-time event that temporarily allows trading of selected gold stickers that are normally untradeable. ([monopolygo.wiki](https://monopolygo.wiki/wiki/event/05132026-se-comgoldenblitz?utm_source=openai)) The review does not describe real-money payment, a stated random or duplicate reward system, repetitive tasks, a progress-blocking timer, or pressure to keep playing on a schedule. The complaint that events are hard to finish with few dice describes difficulty and limited resources, not one of the coded mechanics.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "the new sticker album"
  - why: The sticker album is an in-game collection that the player is trying to complete by obtaining the remaining gold cards.

**Search:** `MONOPOLY GO! Golden Blitz gold stickers event` -> Golden Blitz is a limited-time event that allows trading of selected gold stickers that are normally untradeable. ([monopolygo.wiki](https://monopolygo.wiki/wiki/event/05132026-se-comgoldenblitz?utm_source=openai))

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `ce1c6456-5d34-4001-a1a8-8b5991ef8ffb` - War Robots Multiplayer Battles

> Too much greed by the game devs. You are not just bombarded with tons of advertisements but after you progress up through the rankings, you notice you are always competing with gamers way above your paygrade. The strategy is to make you spend and spend to reach to upper levels. Toxic pity, I would say. Better to spend £50 in a Console game and play for ages, than spend £50 in this game just to get a lame account. The more you pay, more the prices start to increase as well. Run!!

| | labels |
|---|---|
| gold | `M_PayToProgress`, `S_Competition`, `T_Advertisement` |
| pred | `M_PayToProgress`, `S_Competition` |
| **missed** | `T_Advertisement` |

**Did the model consider what it missed?**

- `T_Advertisement` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes competition against other players, specifically opponents perceived as financially stronger. It also describes spending real money as the route to reaching higher rankings or levels, making progression contingent on payment. The mention of being bombarded with advertisements does not establish forced or rewarded ad viewing, so Advertisement is not assigned. Rising prices after spending are not, by themselves, one of the listed mechanics.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "The strategy is to make you spend and spend to reach to upper levels."
  - why: The span describes spending money as the route to progressing to higher levels and rankings.
- `S_Competition` - ok
  - span: "you are always competing with gamers way above your paygrade"
  - why: The reviewer explicitly describes the game making them compete against other players.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (8)

### `2b915fb2-6ff4-4351-9b2f-e8db5661e0a5` - Dark War Survival

> accidentally brought a pack when I double tapped the screen got a refund for the pack through Google play and now my game has been locked and they are holding my account to ransom until I pay the equivalent of the refund I got, thanks ffs, respond promptly my a**, I explained the problem and after what would be considered not very promptly was told you would continue to hold my account ransom, I explained further and you don't bother to respond at all

| | labels |
|---|---|
| gold | `M_EasyToPurchase` |
| pred | `M_EasyToPurchase`, `M_PayToProgress` |
| **spurious** | `M_PayToProgress` |

**Model analysis**

```
The reviewer describes two active mechanics. First, a pack was purchased accidentally through a double tap, implying that the purchase flow lacked sufficient confirmation or made unintended spending too easy. Second, after the refund, the game locked the account and required repayment of the refunded amount before access could be restored, making continued play contingent on payment. The review does not describe a recurring fee, currency conversion, or a technical fault causing the purchase or lock.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "accidentally brought a pack when I double tapped the screen"
  - why: The wording indicates that a simple double tap caused an unintended purchase, showing an overly frictionless purchase flow.
- `M_PayToProgress` - **SPURIOUS**
  - span: "now my game has been locked and they are holding my account to ransom until I pay the equivalent of the refund I got"
  - why: The account is locked and access to the game is withheld until the reviewer pays money.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `f62c8a1f-91fc-4866-b267-977172fa2db3` - Toon Blast

> I don't leave reviews at all, but I'm beyond angry. Im in the 11000 level area. No new levels for 2 weeks and get a champions league. Its a money grab and I fell for it. Get new levels on 3/2/26 only to go maybe 50 levels and no more levels. Come to 3/3, another champions league & have to wait another 2 weeks for levels. This is BS for so many reasons. You dont have levels but have levels for a champions league?! Not going through that again. You've lost my bankroll & me as a player. Way to go!

| | labels |
|---|---|
| gold | `S_Competition`, `T_InfiniteTreadmill` |
| pred | `S_Competition`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| **spurious** | `T_PlayingByAppointment` |

**Model analysis**

```
The review describes a recurring content schedule: ordinary level progression stops for two weeks, then only about 50 new levels are released before the player reaches another endpoint and must wait two more weeks. The wait is an in-game time gate, supporting Playing by Appointment. The repeated release of limited batches means the endpoint continually recedes rather than allowing completion, supporting Infinite Treadmill. The review also names Champions League; I searched because its mechanics are not clear from the review alone. The official Toon Blast help page establishes that Champions League places users in a league with other users and ranks them by trophies, supporting Competition. ([peakgames.helpshift.com](https://peakgames.helpshift.com/hc/en/4-toon-blast/faq/25-what-is-the-champions-league/?f=what-is-the-team-tournament&l=en&p=android&s=events&utm_source=openai)) The phrases about a money grab and losing the bankroll express dissatisfaction and spending, but do not describe a specific monetization mechanic.
```

**Labels assigned**

- `S_Competition` - ok
  - span: "get a champions league"
  - why: The named Champions League is a competitive league involving other users.
- `T_InfiniteTreadmill` - ok
  - span: "Get new levels on 3/2/26 only to go maybe 50 levels and no more levels."
  - why: The player reaches the end of a small batch, after which further progress depends on another future release.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "have to wait another 2 weeks for levels"
  - why: The game imposes a two-week real-world wait before the player can continue to new levels.

**Search:** `Toon Blast Champions League event competition` -> The official Toon Blast Help Center states that Champions League places users in a league with other users, where trophy totals determine rankings and rewards. ([peakgames.helpshift.com](https://peakgames.helpshift.com/hc/en/4-toon-blast/faq/25-what-is-the-champions-league/?f=what-is-the-team-tournament&l=en&p=android&s=events&utm_source=openai))

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `ce92d6ba-cc5f-40a1-bc8e-27a82fa0a8f8` - 8 Ball Pool

> way too many ads and paid popups. I've never seen a game ask u to watch an ad just to claim a daily reward

| | labels |
|---|---|
| gold | `T_Advertisement` |
| pred | `T_Advertisement`, `T_DailyRewards` |
| **spurious** | `T_DailyRewards` |

**Model analysis**

```
The review describes advertisements presented within the game and a daily reward that can only be claimed after watching an ad. The ad requirement is an in-game compelled or incentivized advertisement, while the daily reward is a daily-return reward mechanic. The mention of paid popups alone does not establish a specific purchase-friction mechanism, so it is not coded as Easy to Purchase.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "ask u to watch an ad just to claim a daily reward"
  - why: The player must watch an advertisement to obtain an in-game reward.
- `T_DailyRewards` - **SPURIOUS**
  - span: "claim a daily reward"
  - why: The span identifies a recurring daily reward available for claiming.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `3dc64fb0-3b6a-4ba1-9966-79c09f33069c` - Royal Kingdom

> I downloaded this app today after all the hype about the game being ad free. Total lies. Although the ads are seldom, so far, they are there all the same. What has put me off is the fact that to get out of the ad, you have to go into the play store, which then uses even more data.

| | labels |
|---|---|
| gold | `M_UIMisdirection` |
| pred | `M_UIMisdirection`, `T_Advertisement` |
| **spurious** | `T_Advertisement` |

**Model analysis**

```
The review describes advertisements appearing inside the game despite the expectation that it would be ad free. More specifically, the player cannot simply dismiss the advertisement: leaving it requires opening the Play Store, creating an obstructed opt-out and forcing additional external interaction and data use. The pre-install hype about being ad free is marketing outside the in-game design scope, so only the active in-game advertisement and its dismissal behavior are coded.
```

**Labels assigned**

- `M_UIMisdirection` - ok
  - span: "to get out of the ad, you have to go into the play store"
  - why: The advertisement obstructs the normal opt-out by routing the player into the Play Store instead of providing a straightforward dismissal.
- `T_Advertisement` - **SPURIOUS**
  - span: "to get out of the ad, you have to go into the play store"
  - why: The player is forced to remain in or interact with an in-game advertisement because exiting it requires opening the Play Store.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `443ba104-8abc-48c7-b8a7-b875ec52b05b` - Call of Duty®: Mobile

> I'm actually super impressed. It really is the next best thing to playing on the console! I see a lot of reviews about it lagging and glitching...I would recommend it, but I am so angry. Literally at least once every day, the game just force quits itself in the middle of a match and it has cost me so many wins, and to add insult to injury....I get penalized for leaving matches early on top of that and I wasn't even the one who quit the match!

| | labels |
|---|---|
| gold | `T_MandatoryMarathon` |
| pred | `S_Competition`, `T_MandatoryMarathon` |
| **spurious** | `S_Competition` |

**Model analysis**

```
The review describes a competitive match-based game, but the force-quit itself is attributed to a technical fault, so the crash does not independently receive a dark-pattern label under R11. The underlying match rule does impose a deliberate penalty for an interrupted or exited match: leaving early results in a penalty, even when the game caused the exit. That makes stopping or being removed from the session costly and supports Mandatory Marathon. The references to matches and wins also describe competition between players.
```

**Labels assigned**

- `S_Competition` - **SPURIOUS**
  - span: "in the middle of a match"
  - why: The review describes participation in matches where wins and losses are contested, indicating a player-versus-player competitive structure.
- `T_MandatoryMarathon` - ok
  - span: "I get penalized for leaving matches early on top of that and I wasn't even the one who quit the match!"
  - why: The crash is a technical fault, but the underlying rule penalizes leaving a match, making session termination costly even when the player did not voluntarily exit.

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
The review reports an excessively long loading time, but this is a technical or service delay and does not describe a coded design mechanic such as fragmented downloads. It also describes a slot-style bonus outcome: the bonus lady rarely appears or forms a match, implying an infrequent, chance-based reward event. The phrase about buying coins describes acquiring in-game currency with real money; in the casino-slots context, those purchased coins support luck-based play. The plan to check back periodically is the reviewer’s own behavior, not a game-imposed schedule. A web search was used because “WW4” and “bonus lady” were unclear; it found generic slot references but did not establish a reliable definition for that feature.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "bonus lady rarely comes out or even matches with anything on ww4. iv started playing a new game and buying coins from them"
  - why: The casino-slots context, purchased coins, and uncertain bonus outcome together describe paid participation in a game of chance.
- `M_IntermediateCurrency` - ok
  - span: "buying coins from them"
  - why: The reviewer explicitly says they are buying the game’s coins.
- `P_RewardMania` - ok
  - span: "bonus lady rarely comes out or even matches with anything on ww4"
  - why: The bonus feature appears or matches only rarely, making the unpredictable delivery of the bonus part of the engagement mechanic.

**Search:** `Cashman Casino Slots Games "bonus lady" WW4` -> The results surfaced generic slot-design references and a Cashman Casino White Tiger reference, but did not reliably identify what “WW4” or “bonus lady” denotes. ([liquidandgrit.com](https://www.liquidandgrit.com/wp-content/uploads/2019/04/Slots-Design-Report-April-2019.pdf?utm_source=openai))

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
The review describes a competitive Ludo match against opponents, with the reviewer claiming that the game manipulates the random counts so opponents receive favorable results while the reviewer receives unfavorable ones. The repeated losses are attributed to this alleged hidden outcome manipulation rather than merely bad luck. The statements about time wasting and glitches are evaluations or technical faults without a separate codable mechanic.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "if you are meant to lose, no matter how good you play you will definitley lose"
  - why: The reviewer alleges that outcomes are predetermined or manipulated so player skill cannot affect whether they win.
- `S_Competition` - **SPURIOUS**
  - span: "the opponents get good counts and you get small counts"
  - why: The review explicitly describes the player competing against opponents in the game.

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
The review describes a casino-slots game that is enjoyable enough to play but presents winning as effectively impossible. It also explicitly connects returning to the app with spending more money in pursuit of a win. The first mechanic matches the codebook's direct indicator for a game being impossible to win. The second describes real-money participation in a chance-based winning activity, so it supports Gambling. No specific rigging mechanism, variable reward schedule, payment gate, or waiting mechanic is described.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "why would I ever come back and spend more money when it is impossible to when"
  - why: In this slots-game context, the span explicitly links spending more money with trying to win.
- `T_InfiniteTreadmill` - **SPURIOUS**
  - span: "make these things so fun to play but impossible to ever win"
  - why: The reviewer explicitly describes winning as impossible, matching the label's direct indicator.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `S_Competition` | 2 | 4 |
| `M_Gambling` | 2 | 2 |
| `M_UIMisdirection` | 4 | 0 |
| `M_DeceptiveLuxury` | 3 | 0 |
| `M_IntermediateCurrency` | 3 | 0 |
| `T_MandatoryMarathon` | 3 | 0 |
| `T_Advertisement` | 2 | 1 |
| `T_PlayingByAppointment` | 1 | 2 |
| `S_Reciprocity` | 3 | 0 |
| `P_RewardMania` | 3 | 0 |
| `P_OptimismAndFrequencyBiases` | 2 | 0 |
| `T_Grinding` | 2 | 0 |
| `T_DailyRewards` | 1 | 1 |
| `M_PayToProgress` | 1 | 1 |
| `M_EasyToPurchase` | 2 | 0 |
| `M_NeverEndingLure` | 2 | 0 |
| `P_EasyToGetHardToLose` | 2 | 0 |
| `P_AestheticManipulation` | 1 | 0 |
| `T_InfiniteTreadmill` | 0 | 1 |
| `P_IllusionOfControl` | 1 | 0 |
| `S_FriendSpamImpersonation` | 1 | 0 |
| `S_ForcedFellowship` | 1 | 0 |
| `Tech_FragmentedDownloads` | 1 | 0 |

