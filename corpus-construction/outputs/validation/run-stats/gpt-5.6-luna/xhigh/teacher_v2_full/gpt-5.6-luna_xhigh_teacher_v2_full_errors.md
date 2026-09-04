# Error review - gpt-5.6-luna_xhigh_teacher_v2_full

`gpt-5.6-luna` / reasoning `xhigh` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `aad355174ac4`  
micro-F1 **0.800** (P 0.864 / R 0.745) - **38 of 75** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 8 | said NONE, gold had labels |
| SWAP | 5 | picked different labels than gold |
| MISSED ONLY | 15 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 10 | found all gold, added extras |

## The diagnostic that matters

Of **35** missed labels, **7** (20%) were named in the model's own analysis and dropped anyway; **28** (80%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `M_UIMisdirection` | 0 | 4 |
| `M_DeceptiveLuxury` | 0 | 3 |
| `M_IntermediateCurrency` | 0 | 3 |
| `S_Reciprocity` | 1 | 2 |
| `P_RewardMania` | 0 | 2 |
| `T_MandatoryMarathon` | 0 | 2 |
| `P_OptimismAndFrequencyBiases` | 1 | 1 |
| `M_NeverEndingLure` | 0 | 2 |
| `P_EasyToGetHardToLose` | 0 | 2 |
| `M_Gambling` | 1 | 0 |
| `T_InfiniteTreadmill` | 1 | 0 |
| `P_AestheticManipulation` | 0 | 1 |
| `T_Advertisement` | 1 | 0 |
| `T_PlayingByAppointment` | 0 | 1 |
| `T_Grinding` | 0 | 1 |
| `P_IllusionOfControl` | 0 | 1 |
| `S_Competition` | 1 | 0 |
| `M_PayToProgress` | 0 | 1 |
| `M_EasyToPurchase` | 0 | 1 |
| `Tech_FragmentedDownloads` | 0 | 1 |
| `T_DailyRewards` | 1 | 0 |

## Missed everything (predicted NONE) (8)

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
The reviewer reports an apparent unauthorized starter-pack purchase: the game said the pack had been bought even though they did not tap anything, and the expected fingerprint or password confirmation did not occur. Although this resembles an accidental purchase with absent confirmation, the reviewer explicitly attributes the event as possibly a glitch. Under R11, a specific purchase behavior attributed to a technical fault is not coded as a deliberate dark pattern. No separate functional mechanic is clearly described.
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
The reviewer praises beginner packs as an onboarding feature that helps new players get started and learn what the game offers. The text does not explicitly describe a first-purchase discount, payment being required later, time-limited starter rewards, forced play, or any other coded mechanic. No label applies.
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
The reviewer describes a completed real-money purchase for a weekly one-time offer, followed by the purchased offer being absent. This is presented as a failed transaction or delivery problem, not as a deliberate mechanic such as a subscription, pay-to-progress gate, currency conversion, scarcity tactic, or purchase-friction design. Under R11, the specific missing-offer behavior is treated as a technical or transaction fault, so no label applies.
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
The review describes technical malfunctions rather than deliberate game design: a recent update prevents catching raid bosses, accessing the friends list, and opening or sending gifts; repeated reinstalls are needed to make the game work; and the password and username recovery process falsely reports that the user's information cannot be found. These behaviors are explicitly attributed to update or account-recovery faults, so R11 suppresses dark-pattern labels. The references to raids, friends, and gifts do not independently describe competition, reciprocity, or social pressure.
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
The reviewer describes two mechanics. First, after a game the app sometimes reports brilliant moves that are absent when the free review is opened, causing the free review to be wasted; this is explicitly attributed to a malfunction, so R11 suppresses dark-pattern labels. Second, an unresolved friend request prevents sending another request, but this is only a limitation of the friend-request system and does not describe recruitment pressure, messaging spam, reciprocal resource exchange, or an obligation to keep playing. No label applies.
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

- `S_Reciprocity` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes technical malfunctions rather than deliberate game mechanics: difficulty logging in, slow gift-exchange screens, and crashes after the phone is left idle that require restarting the game. The mention of gift exchange identifies a feature but does not describe sending, requesting, or feeling obligated to exchange resources, so no social label applies. Under R11, behaviors explicitly attributed to glitches, slowness, crashing, or other technical faults do not trigger dark-pattern labels.
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
The review describes technical malfunctions: match-win progress is not saved, starting a new game can freeze, restarting after the freeze consumes energy, and the match progress is lost. These behaviors are explicitly attributed to glitches and bugs. Under R11, the progress loss and energy loss are treated as technical faults rather than deliberate game mechanics; the review does not establish that a deliberate exit would impose the same penalty. No dark-pattern label is therefore supported.
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

- `Tech_FragmentedDownloads` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes automatic background downloading of maps, outfits, and resource packs despite the player disabling the setting. However, the reviewer explicitly attributes this behavior to a persistent bug and asks support to fix it. This is a technical malfunction rather than a deliberate design mechanic. The storage and data consumption are consequences of that bug, and the review does not describe a fragmented-download pattern such as an obscured mandatory download size, a download wall, or missing assets gated by downloads.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (5)

### `2471db11-2c61-415a-8af4-33b80a05c759` - Clash of Clans

> The balancing makes this game have no point. So many bugs, to many sales, support is non existent. You will spend months upgrading troops and defenses just to be nerfed. I have a maxed out account and anyone can destroy me. The more you play the game the more it penalizes you. Reduced times for people that don't play as much. Every account recieves different reward amounts. I've played over 10 years, it's just a chore at this point, not fun. They ruin COC more with every update and event.

| | labels |
|---|---|
| gold | `M_PowerCreep`, `T_Grinding` |
| pred | `M_PowerCreep`, `S_Competition` |
| **missed** | `T_Grinding` |
| **spurious** | `S_Competition` |

**Did the model consider what it missed?**

- `T_Grinding` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes long-term investment in troop and defense upgrades being devalued by later balancing changes: the player spends months building them up and then they are nerfed. It also describes a player-versus-player attack structure in which other players can destroy even a maxed account. The mentions of bugs, sales, nonexistent support, updates, and the game being a chore are general complaints without a qualifying mechanic. Different reward amounts across accounts indicate perceived unfairness but do not by themselves establish a variable-reward engagement system, and reduced times for less-active players do not clearly match a listed schedule or retention mechanic. No external search is needed.
```

**Labels assigned**

- `M_PowerCreep` - ok
  - span: "You will spend months upgrading troops and defenses just to be nerfed."
  - why: The player's months of investment in upgraded troops and defenses are made less valuable when those upgrades are subsequently nerfed.
- `S_Competition` - **SPURIOUS**
  - span: "I have a maxed out account and anyone can destroy me."
  - why: The span describes other players being able to attack and destroy the reviewer's account in a player-versus-player structure.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a59f5319-a1b7-4991-8c6b-d2d2ca56265c` - Fate/Grand Order (English)

> It's an unregulated casino. Every part of the game is set up to direct you towards the slot machine summoning system. Story? Free buffet and show to keep you interested. Plus, you like this character? Well, either hope you have godly luck, or fork over some cash (~$140 for 50% to get a 'rate up' character), because the majority of them are limited time only. Gameplay is mostly just grind to build sunk cost. That, and an incentive to roll the slots for things to reduce the amount of grind.

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury`, `M_Gambling`, `M_PayToProgress`, `M_UIMisdirection`, `P_EasyToGetHardToLose`, `P_RewardMania` |
| pred | `M_DeceptiveLuxury`, `M_Gambling`, `P_EasyToGetHardToLose`, `P_RewardMania`, `T_Grinding` |
| **missed** | `M_PayToProgress`, `M_UIMisdirection` |
| **spurious** | `T_Grinding` |

**Did the model consider what it missed?**

- `M_PayToProgress` - never mentioned -> **attention / recall**
- `M_UIMisdirection` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a chance-based summoning system that functions like a paid slot machine: obtaining a desired character requires luck or spending about $140 for only a stated 50% chance. The characters are also limited-time, making their availability a scarcity tied directly to the decision to spend. The reviewer explicitly characterizes gameplay as grind and says rolling the slots can provide things that reduce that grind, so the game uses repetitive play and chance rewards to sustain engagement. The phrase "build sunk cost" implies accumulated investment intended to make quitting harder. No intermediate currency, purchase-interface trick, daily schedule, competition, or explicit pressure to return before a deadline is described, so those labels do not apply. No web search was needed because the mechanics are identifiable from the review itself.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "fork over some cash (~$140 for 50% to get a 'rate up' character), because the majority of them are limited time only"
  - why: The desired characters are presented as time-limited, using restricted availability to increase pressure around spending for a chance to obtain them.
- `M_Gambling` - ok
  - span: "either hope you have godly luck, or fork over some cash (~$140 for 50% to get a 'rate up' character)"
  - why: The player can spend cash on a chance-based summoning outcome with only a stated 50% chance of obtaining the desired character.
- `P_EasyToGetHardToLose` - ok
  - span: "grind to build sunk cost"
  - why: The reviewer says repetitive play is used to build sunk cost, implying that accumulated investment is intended to make leaving harder.
- `P_RewardMania` - ok
  - span: "an incentive to roll the slots for things to reduce the amount of grind"
  - why: The summoning rolls provide an unpredictable reward delivery system that motivates repeated engagement by promising items that reduce grind.
- `T_Grinding` - **SPURIOUS**
  - span: "Gameplay is mostly just grind to build sunk cost."
  - why: The reviewer explicitly describes gameplay as grind, identifying repetitive work as a central game requirement.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `03e1dcd5-9c13-4b7f-a9e1-d2ebdc8f5773` - Disney Solitaire

> This is incredibly rigged; designed to get you hooked early to develop into impossibility, to suck you into paying money. You can be down to one card and have 10 cards left in your deck and end up going through those 10 cards and still have one card left. Even if you pay the astronomical coins to get another handful of cards, you still have the same card left. If you were to take an actual deck of cards, your chances would be significantly higher. Don't install this game. It's a money scam.

| | labels |
|---|---|
| gold | `M_Gambling`, `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `P_RewardMania` |
| pred | `M_PayToProgress`, `P_IllusionOfControl` |
| **missed** | `M_Gambling`, `P_OptimismAndFrequencyBiases`, `P_RewardMania` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_Gambling` - considered and rejected -> **rule interpretation**
- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a card-draw system that the player believes deliberately withholds the one needed card, even after cycling through the remaining deck and paying for additional cards. The repeated failure is presented as engineered rather than ordinary bad luck, supporting Illusion of Control. It also describes spending coins to obtain more cards in order to continue or overcome the obstacle, which is Pay to Progress. The review does not establish that the coins were purchased with real money, so Intermediate Currency is not assigned; nor does it describe a wager or prize-based chance mechanic sufficient for Gambling.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "Even if you pay the astronomical coins to get another handful of cards"
  - why: The player can spend coins to obtain more cards and attempt to overcome the blocked solitaire state.
- `P_IllusionOfControl` - ok
  - span: "This is incredibly rigged"
  - why: The reviewer explicitly claims that the game engineers the card outcomes rather than dealing them fairly or randomly.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b6745663-5486-4e5b-9066-8a889055d8bc` - Travel Town - Merge Adventure

> it's a good hook. the completionist in me wants to get every level, and the matching is satisfying enough to really tempt me into buying gems/energy to play more. I wish there was a way to disable all the event pop-ups. opening the app and then having to click away ten different challenges is very annoying. at least there are no outside ad pop-ups but I would rather have more optional outside ads than the unskippable events. please consider having a dismiss option for the events! good game.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `M_PayToProgress`, `M_UIMisdirection` |
| pred | `M_IntermediateCurrency`, `M_PayToProgress`, `P_CompleteTheCollection` |
| **missed** | `M_UIMisdirection` |
| **spurious** | `P_CompleteTheCollection` |

**Did the model consider what it missed?**

- `M_UIMisdirection` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a completionist urge to obtain every level, which fits the drive to complete all game content. It also describes gems and energy as purchasable resources used to continue playing, implying that payment bypasses or restores a play limitation. The event pop-ups are currently intrusive and unskippable, but they are not identified as purchase prompts, and the request for optional outside ads or a dismiss button describes proposed features rather than existing mechanics. Outside advertising is explicitly mentioned as absent and is out of scope.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "buying gems"
  - why: The span describes acquiring in-game gems through a purchase, establishing real money being converted into virtual currency.
- `M_PayToProgress` - ok
  - span: "buying gems/energy to play more"
  - why: The reviewer describes purchasing gems or energy as the paid means of continuing to play beyond the resource limitation.
- `P_CompleteTheCollection` - **SPURIOUS**
  - span: "the completionist in me wants to get every level"
  - why: The reviewer explicitly describes a completionist drive to obtain every level in the game.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fb70e577-e644-4af9-88a1-773476a5b805` - Free Fire: 9th Anniversary

> I use to love this game is was my best game I ever played, until now. It's difficult to play if you are using a low ram end device why?,It lag alot.When I approach a enemy it starts to lag like crazy.Enemies are hard to kill now. I never top up not even once. They were always keeping away free stuffs I was hype for the update but now, it just want you to top up to get this or that. They just want your money. I want the old free fire back where you can Play worldwide etc etc please fix bigs n etc

| | labels |
|---|---|
| gold | `M_IntermediateCurrency` |
| pred | `S_Competition` |
| **missed** | `M_IntermediateCurrency` |
| **spurious** | `S_Competition` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes lag on a low-RAM device and additional lag when approaching an enemy; these are explicitly presented as bugs or technical faults, so R11 suppresses any dark-pattern label for those spans. It also describes enemies becoming harder to kill, which is a difficulty complaint without a stated rigging or progression mechanic. The statement that the player must top up to get “this or that” describes monetization, but it does not specify a progress gate, paid advantage, currency conversion, purchase prompt, or other codable monetary pattern. The reference to approaching an enemy does describe adversarial combat against opponents, supporting Competition. No web search is needed.
```

**Labels assigned**

- `S_Competition` - **SPURIOUS**
  - span: "When I approach a enemy"
  - why: The review describes the player engaging an enemy opponent in combat, establishing a player-versus-opponent competition mechanic.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (15)

### `c1a9f304-9cc1-4eb5-84f0-7988297fe423` - Lotsa Slots - Casino Games

> The game has gone downhill. The wins are not as big, or as often. The bonus when buying is smaller. If you are considering slot games there are less costly options with more wins

| | labels |
|---|---|
| gold | `M_Gambling`, `M_IntermediateCurrency`, `P_RewardMania` |
| pred | `M_Gambling`, `P_RewardMania` |
| **missed** | `M_IntermediateCurrency` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a slot-game mechanic with chance-based wins and compares the cost of playing or buying within this game against other slot options. The wins are also described as varying in frequency, which supports a variable-reward structure. The review does not describe a previously purchased item losing value, a purchase interface reducing friction, or a spending threshold reward, so Power Creep, Easy to Purchase, and Never-Ending Lure are not supported.
```

**Labels assigned**

- `M_Gambling` - ok
  - span: "If you are considering slot games there are less costly options with more wins"
  - why: The reviewer compares the monetary cost of slot-game options with the chance-based wins they provide.
- `P_RewardMania` - ok
  - span: "The wins are not as big, or as often."
  - why: The reviewer describes slot-game rewards varying in both payout size and frequency, identifying the reward-delivery pattern.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `2fd4ef32-a33b-44ed-a921-2889ba6e0375` - Ludo King®

> Dice rolls are not random at all, they are preplanned. Game randomly decides at the start of the play that which player has to win and dice rolls according to it. You also will know at the beginning of the game that who is going to win. One player will get more and more 6s and another one will get 1 or 2 mostly. The rolls have gone predictable. That's why I have uninstalled the game today. It's frustrating.

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_Competition` |
| pred | `P_IllusionOfControl`, `S_Competition` |
| **missed** | `P_OptimismAndFrequencyBiases` |

**Did the model consider what it missed?**

- `P_OptimismAndFrequencyBiases` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a competitive multiplayer dice game whose outcomes are allegedly predetermined rather than random. It says the game selects the winner at the beginning and then distributes favorable or unfavorable rolls to different players, including repeated 6s for one player and mostly 1s or 2s for another. This is an explicit claim that the game manipulates outcome determination, which matches Illusion of Control. The reference to which player wins and the contrasting outcomes for different players also describes competition between players. The predictable-roll complaint is not Optimism and Frequency Biases because it alleges deliberate manipulation rather than merely perceiving frequent near-wins or lucky outcomes. No web search was needed.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "Dice rolls are not random at all, they are preplanned. Game randomly decides at the start of the play that which player has to win and dice rolls according to it."
  - why: The reviewer explicitly alleges that the game predetermines the winner and tunes subsequent dice rolls to produce that outcome.
- `S_Competition` - ok
  - span: "which player has to win"
  - why: The span describes a game outcome in which players compete against one another for a winner.

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
The review describes automatic in-game advertisements appearing after every over and every wicket, which interrupts normal gameplay and requires the player to encounter ads repeatedly. The comments about wasting data and time are evaluations of that ad mechanic, not separate mechanics. The catch outcomes describe perceived unfair gameplay but do not explicitly establish rigging or a hidden outcome system.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "Too much ads are shown after every over and every wicket fell."
  - why: Ads automatically appear at recurring gameplay events, making the player repeatedly encounter them during normal play.

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

- `T_DailyRewards` - considered and rejected -> **rule interpretation**
- `T_PlayingByAppointment` - never mentioned -> **attention / recall**

**Model analysis**

```
The review distinguishes the game's in-app design from its external advertising. The complaint that the ads are more fun describes third-party marketing and is out of scope under R13, so it does not trigger Advertisement. Inside the game, the reviewer says the gameplay consisted of repeatedly clicking upgrades, conducting research, and moving to locations, portraying progress as a monotonous task loop. The mention of relying on daily quests does not establish a daily login incentive, resetting reward, or penalty for missing a day, so Daily Rewards is not supported.
```

**Labels assigned**

- `T_Grinding` - ok
  - span: "all the game ever had me do what click to upgrade this or research that or go there"
  - why: The reviewer describes the game as an ongoing loop of repetitive upgrade, research, and navigation tasks rather than skill-based play.

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
The review describes an in-game advertisement appearing after every over, making the ad an imposed interruption rather than an external store or marketing ad. It also describes the app closing and requiring a restart when the player accidentally taps the ad, but that behavior is attributed to bad app behavior or a technical issue, so it does not independently support a dark-pattern label. The requests to stop the ads or fix the UI are hypothetical changes and are not coded.
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

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes payment-gated progress: the player says they cannot do anything and cannot complete the card packs or mini games without paying real money. It also describes a collection objective, namely completing card packs, which supports Complete the Collection. The energy cap limits progress through an order, but the review does not state a regeneration timer or required waiting period, so it does not independently support Playing by Appointment. General claims that the game feels like a trap do not establish a specific purchase prompt or interface manipulation.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "you will never be able to complete the card packs and other mini games without being forced to pay real money for it"
  - why: The review explicitly states that completing game content is impossible without paying real money.
- `P_CompleteTheCollection` - ok
  - span: "complete the card packs"
  - why: The player describes pursuing completion of a card collection.

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
The review describes repeated in-game pop-up screens that interrupt play. In particular, a quit-confirmation screen must be closed with an X before the player can continue. The weekly challenge score popup alone does not establish competition, scheduling, or a reward mechanic. The increased cost is too vague to establish a payment-related label. The required dismissal of the quit screen is an interface obstruction, so it supports UI Misdirection.
```

**Labels assigned**

- `M_UIMisdirection` - ok
  - span: "are you sure you want to quit screens that you have to X out of before continuing"
  - why: The game forces the player to dismiss a quit-related screen before returning to play, obstructing the exit control through the interface.

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
The review describes a competitive leaderboard system with winning-streak rewards. After a loss, the game presents payment as the way to avoid falling in the rankings and losing those rewards, which gives paying players a competitive advantage and makes payment part of maintaining progress or status. The warning also creates pressure through fear of falling behind and forfeiting rewards. The request for an opt-out is hypothetical and does not add a label, and no external search is needed.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "unless you pay up, you're going to go down on the leaderboard"
  - why: Payment is presented as the way to preserve leaderboard standing, giving paying players an advantage in competitive status.
- `S_Competition` - ok
  - span: "force you to be competitive"
  - why: The game explicitly places players in competition through its leaderboard system.
- `S_FearOfMissingOutFOMO` - ok
  - span: "unless you pay up, you're going to go down on the leaderboard and will lose all your winning streak rewards"
  - why: The game pressures the player by threatening falling behind and losing accumulated rewards.

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
- `P_EasyToGetHardToLose` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a character-collection game whose newer characters are becoming more expensive and team-specific, while older characters are losing effectiveness as the meta changes rapidly. That is devaluation of previously acquired characters over time, matching Power Creep. The review also identifies a gacha pity mechanic: patch rewards are barely sufficient to reach hard pity, so the reward-delivery system depends on repeated attempts toward a variable outcome, matching Reward Mania. It does not explicitly state that real money is required for progression, that money is wagered, or that the accumulated time makes quitting difficult, so those labels are not supported. No search is needed because Fontaine, meta, and hard pity are identifiable in this game context.
```

**Labels assigned**

- `M_PowerCreep` - ok
  - span: "old characters started falling off which I hope they could climb back up. And now the Meta shifts now are extremely fast.."
  - why: The review describes older characters becoming less effective and less valuable as the newer meta rapidly changes.
- `P_RewardMania` - ok
  - span: "another issue is how much rewards we get.. it's so low each patch barely gives us enough to hit hard pity"
  - why: Hard pity identifies a gacha reward system in which players repeatedly pursue a character through variable outcomes until reaching a guarantee.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `042ee18e-d78e-4a0f-9cc2-2b1e10cc46e6` - Total Battle: War Strategy

> Sometimes, it feels like 'Groundhog Day', meaning that I show up, complete tasks, spend gold and potion, spend real money, then come back tomorrow and do it all over again. It's a way to get you drawn in and invested in the game, so you feel obligated to keep playing. There is no real progress or advancement; there is no pot of gold at the end of this rainbow.

| | labels |
|---|---|
| gold | `P_EasyToGetHardToLose`, `T_Grinding`, `T_InfiniteTreadmill` |
| pred | `P_EasyToGetHardToLose`, `T_Grinding` |
| **missed** | `T_InfiniteTreadmill` |

**Did the model consider what it missed?**

- `T_InfiniteTreadmill` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a repeating daily loop: the player returns, completes the same tasks, spends in-game resources and real money, then returns the next day to repeat it. This is a repetitive task cycle tied to advancement, supporting Grinding. The reviewer also explicitly says the design draws players in, makes them invested, and creates an obligation to continue, which describes accumulated investment raising the cost of leaving and supports Easy to Get, Hard to Lose. The mention of returning tomorrow does not by itself establish Daily Rewards or Playing by Appointment because no daily reward, missed-day penalty, timer, or progress gate is described. The absence of meaningful progress and an end reward is not enough to establish Infinite Treadmill without a clearer claim that the game cannot be completed. No web search was needed.
```

**Labels assigned**

- `P_EasyToGetHardToLose` - ok
  - span: "It's a way to get you drawn in and invested in the game, so you feel obligated to keep playing"
  - why: The review explicitly describes the design creating investment and an obligation to continue playing, making departure feel costly.
- `T_Grinding` - ok
  - span: "complete tasks, spend gold and potion, spend real money, then come back tomorrow and do it all over again"
  - why: The player must repeatedly perform the same tasks and spend resources, with the cycle continuing without meaningful advancement.

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
The review describes an external advertisement promising an escape game, but R13 excludes misleading third-party or store advertising from coding. In the actual game, the player must repeatedly play the match-3-style game to earn stars needed for story progress, such as walking Austin. The statement about points being lost after failing a level describes a failure consequence, but it does not by itself establish a separate listed mechanic.
```

**Labels assigned**

- `T_Grinding` - ok
  - span: "Always you play one game you just get one star only. And all your points get lost if you don't make that level. Even for walking Austin you will have to earn a star by playing stupid game."
  - why: The player must keep playing the same game cycle to earn stars required for story advancement.

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
The review describes an in-game advertisement that cannot be dismissed, forcing the player to remain in the ad flow and restart the game before continuing. This is a forced or unskippable advertisement. The review does not describe a purchase prompt, spending, a timer, or progress loss, so no additional label applies.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "Can't close the ads"
  - why: The player cannot dismiss the in-game ads and therefore is compelled to view them before gameplay can resume.

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
The review describes a gacha system in which real money buys tickets, tickets are used for chance-based pulls, and the player must make many pulls to obtain a desired SSR unit or reach a guarantee. The $80-to-20-ticket exchange rate makes the real monetary cost of the pulls visible, while the 4% SSR rate and the 15 consecutive failed 10-pulls describe unpredictable, repeated reward delivery. The review does not establish that the game is rigged, that spending is required for general progression, or that the player has accumulated an investment making it difficult to quit.
```

**Labels assigned**

- `M_Gambling` - ok
  - span: "You get about 20 tickets with $80 so even being generous it's still $600-$800 just to guarantee the unit you want. 4% chance to pull any SSR at any time."
  - why: Paid tickets fund pulls whose outcome may produce the desired SSR unit; this is gambling within the gacha mechanic, not pay-to-progress outside the wager.
- `M_IntermediateCurrency` - ok
  - span: "You get about 20 tickets with $80"
  - why: The span explicitly describes purchasing 20 in-game tickets with $80.
- `P_RewardMania` - ok
  - span: "4% chance to pull any SSR at any time. In a 10-pull that's around a 33% chance give or take. I failed that 15 times in a row, so 150 pulls with no SSR"
  - why: The span describes variable SSR outcomes and repeated pulls pursued despite an extended sequence of failures.

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
The review explicitly describes a sticker album with missing non-tradable gold cards, receiving only one new card over two months, Golden Blitz events that do not feature needed cards, and events that are difficult to finish because the game provides few dice. The statement about needing only gold cards describes an incomplete collection the player is trying to finish, so Complete the Collection applies. The low number of newly awarded cards does not by itself establish random or variable reward delivery, and the event and dice complaints do not explicitly state repeated tasks, a timer, a paid alternative, or a loss for missing a deadline. I searched only to resolve “Golden Blitz”; it is a limited-time event that allows trading of selected Gold Stickers, but the review does not describe trading, schedule pressure, or a monetary stake, so this does not add another label. ([monopolygo.helpshift.com](https://monopolygo.helpshift.com/hc/en/3-monopoly-go/faq/22-golden-blitz/?pubDate=20250530&utm_source=openai))
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "I have been needing only gold cards for two months now"
  - why: The span identifies the uncollected cards remaining in the album and the player's ongoing effort to obtain them.

**Search:** `MONOPOLY GO Golden Blitz gold stickers non tradable sticker album` -> Golden Blitz is a limited-time event that permits trading of selected Gold Stickers; gold stickers are otherwise non-tradable. ([monopolygo.helpshift.com](https://monopolygo.helpshift.com/hc/en/3-monopoly-go/faq/22-golden-blitz/?pubDate=20250530&utm_source=openai))

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
The review mentions many advertisements, but only describes their volume and does not say that viewing them is forced or rewarded, so T_Advertisement is not supported. It explicitly describes player-versus-player ranking competition, supporting S_Competition. It also presents repeated spending as the intended route to reaching higher levels, which supports M_PayToProgress. The claim that prices increase after paying does not by itself establish a supported currency, interface, scarcity, subscription, or item-devaluation mechanic. No web search was needed.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "The strategy is to make you spend and spend to reach to upper levels."
  - why: The review states that repeated payment is used to reach higher levels in the game.
- `S_Competition` - ok
  - span: "you are always competing with gamers way above your paygrade."
  - why: The span explicitly describes the player competing against other gamers.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (10)

### `2b915fb2-6ff4-4351-9b2f-e8db5661e0a5` - Dark War Survival

> accidentally brought a pack when I double tapped the screen got a refund for the pack through Google play and now my game has been locked and they are holding my account to ransom until I pay the equivalent of the refund I got, thanks ffs, respond promptly my a**, I explained the problem and after what would be considered not very promptly was told you would continue to hold my account ransom, I explained further and you don't bother to respond at all

| | labels |
|---|---|
| gold | `M_EasyToPurchase` |
| pred | `M_EasyToPurchase`, `M_PayToProgress` |
| **spurious** | `M_PayToProgress` |

**Model analysis**

```
The review describes an unintended in-game purchase caused by a double tap, indicating that the purchase interface allows accidental spending. It also describes the game locking the account after the refund and making payment of the refunded amount a condition for regaining access, which functions as a payment wall blocking continued play. The account lock is presented as an intentional game or account rule, not as a bug or technical fault. No external search is needed because the mechanics are clear from the review.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "accidentally brought a pack when I double tapped the screen"
  - why: The purchase was triggered unintentionally by a double tap, showing that the interface makes it easy to spend money accidentally.
- `M_PayToProgress` - **SPURIOUS**
  - span: "now my game has been locked and they are holding my account to ransom until I pay the equivalent of the refund I got"
  - why: The game is made inaccessible until the player pays money, so payment is required to continue playing.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `57add346-8b93-4249-be50-1a39331cf79b` - RAID: Shadow Legends

> These are my views of the game after playing for almost a day. I didnt make a single purchase but got a free champion and silver from a referral. Pros: Easy to learn the controls and layout of the game, nice story line, easy combat system, no lag, nice champion designs and gameplay. Cons: Every single time you log in you are bombarded with pop ads advertising "special" or "limited time" deals, once your champions hit level 30 it becomes a horrible grind, p2p is the best way to win this game.

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury`, `M_PayToProgress`, `S_ForcedFellowship` |
| pred | `M_DeceptiveLuxury`, `M_EasyToPurchase`, `M_PayToProgress`, `S_ForcedFellowship`, `T_Grinding` |
| **spurious** | `M_EasyToPurchase`, `T_Grinding` |

**Model analysis**

```
The review describes a referral reward that grants a champion and silver, implying that the game incentivizes referrals and player recruitment. It also describes repeated in-game promotional pop-ups appearing at login; these are direct purchase solicitations, and the "limited time" framing uses artificial scarcity. After champions reach level 30, the reviewer explicitly characterizes progression as a grind, indicating repetitive and tedious effort. Finally, the statement that p2p is the best way to win describes payment as providing a gameplay advantage. The pop-ups are promotional purchase offers rather than forced third-party advertisements, so T_Advertisement is not assigned. No web search was needed because the mechanics are clear from context.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: ""special" or "limited time" deals"
  - why: The deals are framed as limited-time offers, using scarcity and urgency to influence purchases.
- `M_EasyToPurchase` - **SPURIOUS**
  - span: "Every single time you log in you are bombarded with pop ads advertising "special" or "limited time" deals"
  - why: Repeated promotional pop-ups appear at session entry and directly solicit purchases before play.
- `M_PayToProgress` - ok
  - span: "p2p is the best way to win this game"
  - why: The reviewer states that paying is the best route to winning, implying a paid gameplay advantage.
- `S_ForcedFellowship` - ok
  - span: "got a free champion and silver from a referral"
  - why: The game grants valuable rewards through a referral, incentivizing players to recruit others.
- `T_Grinding` - **SPURIOUS**
  - span: "once your champions hit level 30 it becomes a horrible grind"
  - why: The reviewer names a grind beginning at level 30, implying that advancing afterward requires repetitive, tedious play.

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
The review describes two current in-game mechanics. First, the game requires the player to watch an advertisement in order to claim a daily reward, which is an ad-gated reward. Second, the game provides a daily reward, a recurring incentive tied to daily return. The phrase about paid popups reports frequent purchase solicitation, but it does not clearly describe a specific friction-reducing purchase interface such as a default purchase, insufficient-funds prompt, or missing confirmation, so M_EasyToPurchase is not assigned. No external search was needed.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "ask u to watch an ad just to claim a daily reward"
  - why: The player must watch an advertisement to receive an in-game reward.
- `T_DailyRewards` - **SPURIOUS**
  - span: "claim a daily reward"
  - why: The game offers a reward on a daily cycle, encouraging recurring return to claim it.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `3db5f780-e8e1-44a1-b538-63120ac046a6` - Flambé®: Merge & Cook

> Love this game, I would have given it 5 stars but as you go up in levels you start to run out of space on the board when making more complicated recipes. A storage option would be fab please developers. Also when winning items you have to move them onto the board in the order won, it would be really nice if we could select which ones we want to play in our own play order. Lastly, what is the inventory? I can't do anything with mine, lots of empty slots. Still the best Merge game in my opinion!

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `M_WasteAversion` |
| **spurious** | `M_WasteAversion` |

**Model analysis**

```
The review describes a realized board-capacity shortfall: at higher levels, the player runs out of space while preparing more complicated recipes and requests storage. This is an active capacity limitation, not merely a general complaint about inventory. The forced order for placing won items and the empty inventory slots describe gameplay or interface limitations but do not match another listed dark-pattern mechanic. The requested storage feature itself is hypothetical and is not separately coded.
```

**Labels assigned**

- `M_WasteAversion` - **SPURIOUS**
  - span: "as you go up in levels you start to run out of space on the board when making more complicated recipes"
  - why: The player explicitly encounters insufficient board capacity while trying to make recipes, showing an active space shortfall.

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
The review mentions advertisements inside the game, despite the external claim that it was ad free; that marketing claim is outside the in-game unit and is not separately coded. The in-game ad is not merely present: the reviewer says leaving it requires entering the Play Store, which implies the ad cannot be dismissed through a normal in-game exit. This both compels interaction with the advertisement and obstructs the opt-out path. The extra data use is a consequence of that behavior, not a separate coded mechanic.
```

**Labels assigned**

- `M_UIMisdirection` - ok
  - span: "to get out of the ad, you have to go into the play store"
  - why: The normal opt-out from the ad is obstructed by routing the player into the Play Store.
- `T_Advertisement` - **SPURIOUS**
  - span: "to get out of the ad, you have to go into the play store"
  - why: The player is compelled to remain in or interact with an in-game advertisement to exit it.

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
The review explicitly describes lag, unresponsive controls, and the game suddenly stopping, all of which are attributed to a network or technical fault and are not coded as dark-pattern mechanics themselves. It also identifies Duel Mode and ranked progress, showing player-versus-player competition. Most importantly, when the match terminates unexpectedly, the game declares a loss and deducts 30 to 50 ranked points. Under R11 and the Mandatory Marathon boundary, the underlying match-forfeit penalty remains codable even though the malfunction triggered it. No web search was needed.
```

**Labels assigned**

- `S_Competition` - **SPURIOUS**
  - span: "Duel Mode"
  - why: Duel Mode describes players being placed against one another in direct competition.
- `T_MandatoryMarathon` - ok
  - span: "game has suddenly stopped and says YOU HAVE LOST and then nearly -30 to -50 gaming points are lessed from my Ranked game progress"
  - why: The game converts an abruptly terminated match into a loss and removes ranked progress, showing a match-termination penalty even though lag triggered it.

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
The review describes a long loading delay, but this is a technical or service-performance complaint rather than an intentional wait timer, download wall, or other coded mechanic. "the bonus lady rarely comes out or even matches with anything on ww4." describes a chance-based bonus outcome that appears or aligns only rarely, supporting Reward Mania. Because the named game is a casino slots game and the reviewer also says they are "buying coins from them," the review supports paid participation in a luck-based game, which also supports Gambling. The coin purchase independently supports Intermediate Currency. The plan to check back occasionally is voluntary and does not establish a game-imposed schedule, daily reward, or fear of missing out. The search did not reliably identify the terms "bonus lady" or "ww4," so no additional feature-specific inference is made.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "the bonus lady rarely comes out or even matches with anything on ww4. iv started playing a new game and buying coins from them."
  - why: The reviewer describes luck-based bonus results while purchasing the game's virtual coins, indicating paid participation in a chance-based game.
- `M_IntermediateCurrency` - ok
  - span: "buying coins from them."
  - why: Buying coins from the game provider describes exchanging real-world money for virtual currency.
- `P_RewardMania` - ok
  - span: "the bonus lady rarely comes out or even matches with anything on ww4."
  - why: The bonus feature is delivered through an irregular, chance-based appearance or matching outcome.

**Search:** `Cashman Casino Slots Games "bonus lady" WW4` -> The search did not reliably resolve "bonus lady" or "ww4"; it returned general or unrelated slot-machine references rather than a source identifying those terms. ([liquidandgrit.com](https://www.liquidandgrit.com/wp-content/uploads/2019/04/Slots-Design-Report-April-2019.pdf?utm_source=openai))

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `2f50b132-9762-4f48-ae35-487f414aa41a` - MONOPOLY GO!

> Okay so I started playing in October of 2023. In the beginning, it was a fun game. Over time, I started to see the real issues in the game. 1. Most other players live by the motto you have to cheat to beat the game system and I am starting to feel they are right! 2. Events have become a joke. Peg-E is a total waste the new race car game is even worse! 3. Way to many gold duplicates! 4. Not enough trades a day! 5. Not enough dice.I could keep going but I only have 500 spaces, and I am at my limit

| | labels |
|---|---|
| gold | `P_RewardMania`, `S_Reciprocity` |
| pred | `P_RewardMania`, `S_Competition`, `S_Reciprocity` |
| **spurious** | `S_Competition` |

**Model analysis**

```
The review describes several complaints, but only some identify codable mechanics. The cheating statement reports other players' behavior and does not say the game rewards or incentivizes cheating, so it does not support Encourages Anti-Social Behavior. "the new race car game" identifies a race-based mode, which is competitive play. "Way to many gold duplicates!" describes repeated duplicate collectible drops; the search established that MONOPOLY GO golds are golden stickers and that duplicate stickers result from random content, matching Reward Mania's duplicate or unwanted drops from a randomized pool. "Not enough trades a day!" identifies a capped player-to-player item-trading mechanic, supporting Reciprocity under the trade/resource-exchange boundary. The event criticism, shortage of dice, and 500-space remark do not specify another qualifying pattern: there is no stated payment route, wait timer, collection-completion goal, daily reward, or loss on missing a schedule.
```

**Labels assigned**

- `P_RewardMania` - ok
  - span: "Way to many gold duplicates!"
  - why: The span describes repeated duplicate gold-sticker drops from the game's random reward content, which is a variable-reward delivery pattern. ([monopolygo.helpshift.com](https://monopolygo.helpshift.com/hc/en/3-monopoly-go/faq/276-duplicate-stickers/?pubDate=20250530&utm_source=openai))
- `S_Competition` - **SPURIOUS**
  - span: "the new race car game"
  - why: A race-based game mode describes players competing against one another.
- `S_Reciprocity` - ok
  - span: "Not enough trades a day!"
  - why: The complaint presupposes a player-to-player trading feature whose daily exchange allowance is capped.

**Search:** `MONOPOLY GO gold duplicates stickers sticker packs random` -> The official MONOPOLY GO Help Center identifies gold duplicates as duplicate golden stickers and states that sticker content is random, establishing the randomized duplicate-drop mechanic. ([monopolygo.helpshift.com](https://monopolygo.helpshift.com/hc/en/3-monopoly-go/faq/276-duplicate-stickers/?pubDate=20250530&utm_source=openai))

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
The reviewer alleges that the game deliberately determines losses rather than letting skill decide outcomes: they say players are meant to lose, that good play cannot prevent defeat, and that opponents receive better counts while the reviewer receives small ones. This supports alleged outcome manipulation under Illusion of Control. The reference to opponents also describes direct player-versus-player competition. The statement that the game is time-wasting does not identify grinding or a time gate, and the glitches are attributed to technical faults, so they do not support a dark-pattern label.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "if you are meant to lose, no matter how good you play you will definitley lose"
  - why: The reviewer claims that the game predetermines losses and overrides player skill.
- `S_Competition` - **SPURIOUS**
  - span: "the opponents get good counts and you get small counts"
  - why: The span explicitly describes the player competing against opponents in the game.

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
The reviewer describes a casino-slots game that offers paid participation and winning as the outcome, while complaining that winning is effectively impossible. The phrase about spending more money in the app, combined with the game's casino-slot context, supports Gambling. The review does not describe a specific rigging mechanism, concealed odds, variable reward delivery, or payment as a progression gate, so no other label is supported.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "why would I ever come back and spend more money when it is impossible to when"
  - why: The reviewer explicitly describes spending more money in a casino-slots game where the intended chance-based reward is winning.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `S_Competition` | 1 | 5 |
| `M_UIMisdirection` | 4 | 0 |
| `M_DeceptiveLuxury` | 3 | 0 |
| `M_Gambling` | 1 | 2 |
| `M_IntermediateCurrency` | 3 | 0 |
| `T_Grinding` | 1 | 2 |
| `S_Reciprocity` | 3 | 0 |
| `M_PayToProgress` | 1 | 2 |
| `T_MandatoryMarathon` | 2 | 0 |
| `P_OptimismAndFrequencyBiases` | 2 | 0 |
| `T_Advertisement` | 1 | 1 |
| `T_DailyRewards` | 1 | 1 |
| `M_EasyToPurchase` | 1 | 1 |
| `M_NeverEndingLure` | 2 | 0 |
| `P_EasyToGetHardToLose` | 2 | 0 |
| `P_RewardMania` | 2 | 0 |
| `T_InfiniteTreadmill` | 1 | 0 |
| `P_AestheticManipulation` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `P_IllusionOfControl` | 1 | 0 |
| `M_WasteAversion` | 0 | 1 |
| `Tech_FragmentedDownloads` | 1 | 0 |
| `P_CompleteTheCollection` | 0 | 1 |

