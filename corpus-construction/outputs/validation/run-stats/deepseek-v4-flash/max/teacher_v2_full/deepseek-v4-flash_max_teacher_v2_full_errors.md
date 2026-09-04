# Error review - deepseek-v4-flash_max_teacher_v2_full

`deepseek-v4-flash` / reasoning `max` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `aad355174ac4`  
micro-F1 **0.698** (P 0.853 / R 0.591) - **45 of 75** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 14 | said NONE, gold had labels |
| SWAP | 8 | picked different labels than gold |
| MISSED ONLY | 19 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 4 | found all gold, added extras |

## The diagnostic that matters

Of **56** missed labels, **8** (14%) were named in the model's own analysis and dropped anyway; **48** (86%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `S_Competition` | 0 | 7 |
| `M_UIMisdirection` | 0 | 6 |
| `M_DeceptiveLuxury` | 0 | 4 |
| `M_IntermediateCurrency` | 1 | 3 |
| `T_Grinding` | 1 | 3 |
| `S_Reciprocity` | 0 | 4 |
| `P_RewardMania` | 1 | 2 |
| `T_MandatoryMarathon` | 0 | 3 |
| `P_OptimismAndFrequencyBiases` | 0 | 2 |
| `P_EasyToGetHardToLose` | 1 | 1 |
| `M_Gambling` | 0 | 2 |
| `M_NeverEndingLure` | 0 | 2 |
| `S_FriendSpamImpersonation` | 0 | 2 |
| `T_Advertisement` | 2 | 0 |
| `P_AestheticManipulation` | 0 | 1 |
| `M_WasteAversion` | 0 | 1 |
| `M_PayToProgress` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `Tech_FragmentedDownloads` | 1 | 0 |
| `S_ForcedFellowship` | 0 | 1 |
| `M_EasyToPurchase` | 1 | 0 |
| `T_DailyRewards` | 0 | 1 |
| `T_InfiniteTreadmill` | 0 | 1 |

## Missed everything (predicted NONE) (14)

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
- `P_RewardMania` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review is a general complaint about the game's generosity: payouts from play are described as smaller and less frequent than before, and the bonus attached to making a purchase has been reduced. The reviewer ends by recommending other slot games as less costly with more wins. No mechanic is described beyond these value complaints: there is no named schedule, no forced action, no payment required for progress, no chance-based purchase described as a wager, no claim that outcomes are rigged or concealed, and no account of the reward-delivery system sustaining engagement. 'The wins are not as big, or as often' is a complaint about reward size and frequency, which the Reward Mania boundary rule expressly excludes when nothing describes the delivery mechanism itself; 'The bonus when buying is smaller' mentions buying without establishing real money being converted into currency, a wager, or a progress gate. What remains is dissatisfaction with how rewarding the game is, which under R2 does not constitute a describable dark pattern.
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

- `M_WasteAversion` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes several frustrations but mostly at the level of game-feel and design friction, not named dark patterns. (1) The board becomes overcrowded ('gridlocked', 'too many new things on a tiny board'), and the game responds by 'archiving' overflow items into the player's inventory instead of letting them delete them — a complaint about storage and management mechanics, with no purchase, upgrade, or concrete forfeiture described. (2) Energy 'not enough to last very long' names a scarce play resource but never states the regeneration schedule, the wait, or a paid refill, so it does not meet the Wait to Play boundary that requires the span to describe the wait or its regeneration timer. (3) Gems 'slow down a lot when you slow down on unlocking new items' describes progression-linked reward pacing, not a variable-reward or collection scheme. (4) Astral events and evil eyes are named as content but no schedule or pressure is described. (5) The ad mismatch is external store/marketing material, out of scope under R13. No payment, currency conversion, social mechanic, chance mechanic, or timed obligation is described anywhere in the review.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `c63003ef-dcdd-4ef2-a54e-0c9b0dfe931a` - Kingshot

> The game is very meh. The ads are much more fun than the actual game, and make up only a tiny portion of it. Still, I decided to persist for a few days to see how it went, and all the game ever had me do what click to upgrade this or research that or go there. Even after such a short time, there were already so many things that it wad impossible to keep track of them without relying on the daily quests and such. It's really not my cup of tea

| | labels |
|---|---|
| gold | `T_DailyRewards`, `T_Grinding`, `T_PlayingByAppointment` |
| pred | _NONE_ |
| **missed** | `T_DailyRewards`, `T_Grinding`, `T_PlayingByAppointment` |

**Did the model consider what it missed?**

- `T_DailyRewards` - never mentioned -> **attention / recall**
- `T_Grinding` - never mentioned -> **attention / recall**
- `T_PlayingByAppointment` - never mentioned -> **attention / recall**

**Model analysis**

```
The review is a general impression of the game rather than a report of any one mechanic being exploited. Three candidate readings exist. First, "The ads are much more fun than the actual game, and make up only a tiny portion of it" describes advertising content that promoted the game as more fun than the game really is; that is external marketing material rather than ads encountered inside the game, so it does not satisfy Advertisement. Second, "all the game ever had me do [is] click to upgrade this or research that or go there" names the activities the gameplay consists of, but it characterises the loop as uninteresting, not as a repetitive task cycle the player must grind to advance; there is no link between repetition and progress, so it is an evaluation of quality. Third, the mention of "the daily quests" describes them as a tracking aid for the many overlapping systems, not as a daily-login incentive with rewards or a penalty for missing a day. Overall the reviewer describes content that is busy, ad-mismatched, and unappealing, but no named design behaviour matches a dark pattern definition.
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
The reviewer is giving a short positive endorsement. The only design element named is "beginner packs," which are praised for helping the player get started and preview what the game offers, with the reviewer adding "no surprises" to say the experience matched expectations. No mechanic is actually described as operating on the player: there are no timers, appointments, ad views, exchange rates or purchases of currency named, no price or first-purchase discount framing, no deadlines or loss conditions, no social or collection elements, and no chance mechanics. Even if beginner packs are monetized starter offers, the text never describes the payment, a reduced price, or a first-purchase structure, so no indicator of NeverEnding Lure (First Charge Discount) is satisfied. The remaining sentences are evaluative praise (R2, R8): nothing in them describes a game design behaviour that fits any label.
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
The reviewer describes a single incident: they paid for a weekly offer with real money, the bank charge went through, but the purchased offer was never delivered, and they are demanding a refund. This describes a transaction that failed to credit the purchased item. It is a malfunction or service error, not a designed mechanic: no in-game rule, interface design, schedule, or economic structure is described. Under R11, behavior attributed to a technical fault (the offer 'is not there' despite a successful charge) does not trigger dark pattern labels, since dark patterns are deliberate design choices rather than technical malfunctions.
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
The reviewer complains that recent updates added too many interruption screens: pop-ups for the weekly challenge score and "are you sure you want to quit" confirmation dialogs that must each be X'd out or clicked through before play resumes, plus a general statement that the cost of something has gone up. The core of the complaint is friction and annoyance from having to dismiss multiple screens, and price displeasure. The pop-ups are informational or confirmatory, not purchase offers: nothing links them to spending, and the quit-confirmation screens actually guard against accidental exits rather than obstructing one. The price increase is stated without any mechanic attached — no pass, no currency, no progress gate, no purchase flow. What remains is a quality-of-life/UX complaint, which per R2 is dissatisfaction, not a described dark pattern: UI Misdirection would require the screens to direct attention to a purchase or obstruct an opt-out from one, and the codebook's counterexample (annoying suggestion UI with no way to turn it off) codes NONE on exactly this ground.
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
The reviewer reports technical failures: after the most recent update they cannot catch raid bosses, cannot access the friends list, cannot open or send gifts, and have had to reinstall the game repeatedly. On a new tablet, the forgot-password and forgot-username flows repeatedly say the info cannot be found. Everything described is attributed to software malfunctions, account-recovery failure, or broken features — not to deliberate game design. Under R11, behavior attributed to bugs, glitches, errors, or technical faults is not coded as dark patterns, and no design rule is described that would independently satisfy any label (e.g., no schedule, payment gate, social mechanic, or reward structure is mentioned).
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
The reviewer describes three things. First, the game they got does not match the ad that prompted the install: they expected an escape game and found match-3 gameplay. That complaint concerns advertising placed outside the app, which R13 excludes from coding even when it involves misrepresented gameplay. Second, they describe the reward loop: each completed level yields one star, and stars are needed for meta-game actions such as walking Austin. This describes ordinary level-to-star conversion and progression gating, with no manipulation, schedule, or monetary element attached. Third, they say points are lost when a level is failed, a frustration about failure penalties, but no label's definition covers a generic penalty for failing a level: no wait, no appointment, no accumulated investment operating on the decision to leave, no chance mechanic, no payment, no social element. The characterisation 'nothing less than candy crush' is a genre evaluation, not a described dark mechanic. Nothing in the review names a mechanic that matches a codebook pattern.
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
The review has two distinct complaints. First, the reviewer reports an inconsistency between the game's post-match screen, which sometimes labels a move 'brilliant', and the move review, which then does not show any brilliant move; the reviewer calls this a waste of a free review and asks the developer to fix it. This is framed as a technical fault or bug ('please fix this'), and per R11, behavior attributed to a malfunction rather than a deliberate design choice does not receive a dark pattern label. The limited 'free review' allowance is named only as the resource consumed by the fault, with no description of a schedule, wait, or deliberate penalty. Second, the reviewer suggests that the game should add a way to cancel friend requests, because a request that is neither accepted nor declined leaves the player unable to send requests to anyone else. The suggested cancel feature does not exist, and per R12 a wish for a non-existent feature is not coded; the underlying pending-request cap is described only as an annoyance and matches no label in the codebook.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fe4ad63c-0bee-4c2e-814f-1e4f46f14d3d` - Township

> Please have a feature where you can edit plans for your town and then if you're not finished yet, you can temporarily save it as a draft so you can continue editing it later. It doesn't have to be usable. Just a draft design that you can continue editing later. Editing the plan of the town is very time consuming and it's unfortunate that you have to put all buildings in place first before you can save it and continue. I want to edit my town like Im an urban planner and it takes time of planning.

| | labels |
|---|---|
| gold | `T_MandatoryMarathon` |
| pred | _NONE_ |
| **missed** | `T_MandatoryMarathon` |

**Did the model consider what it missed?**

- `T_MandatoryMarathon` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer is asking for a draft/save feature in Township's town layout editor: they want to edit a plan over multiple sessions rather than being forced to place all buildings before saving. The only current design behaviour described is that saving a town plan requires finishing the layout first and that editing is time-consuming. The requested draft feature does not exist, so under R12 it cannot be coded. The existing behaviour — restricted saving inside a decorative layout editor — is framed as an inconvenience of a creative planning tool, not as a session-forfeit of gameplay progress, resources, or advancement. Nothing in the text describes a monetary, social, temporal, or psychological dark pattern operating on the player; the review is a quality-of-life feature wish.
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
The review is purely a technical complaint: the reviewer reports login difficulties, slow gift-exchange screens, and crashes that require restarts. Nothing in the text describes a design mechanic, schedule, payment structure, social system, or psychological manipulation. Every issue named is attributed to glitchiness or technical malfunction rather than to a deliberate game rule, so R11 suppresses any dark-pattern reading.
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
The review describes three failure experiences, all explicitly attributed to technical faults: match-win progress not being saved, the game freezing when starting a new match, and energy being consumed without match progress after a forced restart. The reviewer closes by asking the developer to fix the bugs. Under R11, behavior attributed to a bug, glitch, error, or technical fault is not a dark pattern, because dark patterns are deliberate design choices rather than technical malfunctions. The energy loss and missing match progress are described as consequences of freezing and restarting, i.e., progress not saved and rewards not credited because of the malfunction itself; no underlying design rule (a deliberate exit penalty, a scheduled gate, a paywall, a timer) is described independently of the glitch. There is no unrelated functional design behavior described that would survive the bug attribution, so no label applies.
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
The reviewer is describing the game's resource download system: maps, outfits, and other packs download automatically in the background, and the game ignores the user's manual 'Auto-Download' off setting, consuming mobile data and storage. The only candidate label is Tech_FragmentedDownloads, whose indicators cover mandatory in-game downloads that conceal true storage requirements. But the reviewer frames the entire behavior as a malfunction: it is introduced as a 'persistent bug,' the game is said to 'ignore the setting,' and the message closes with 'Please fix this bug.' Under R11, behavior attributed to a bug or technical fault is not a dark pattern, which requires deliberate design. Fragmented Downloads additionally requires the design to obscure storage needs (advertised size versus mandatory download, a download wall, in-place download prompts for declined packages); none of that is described here, only an errant download process the player cannot stop. No other mechanic is described.
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
The reviewer describes a single recurring incident: when an advertisement plays, they cannot dismiss it or return to the game afterward, and when the ad gets stuck, continued play is impossible. The review accepts the presence of ads in principle ('i don't care if there are ads') and frames the harm as the ad freezing and blocking continuation. The inability to continue is attributed directly to the ad getting stuck, which is a technical malfunction rather than a deliberate design rule. Forced ad views as a designed mechanic would satisfy T_Advertisement, but here the blocking behaviour is blamed on the ad seizing up, so R11 suppresses the label: dark patterns are deliberate design choices, and the span describes a fault, not a designed schedule of advertisement or ad-gated progress.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (8)

### `f62c8a1f-91fc-4866-b267-977172fa2db3` - Toon Blast

> I don't leave reviews at all, but I'm beyond angry. Im in the 11000 level area. No new levels for 2 weeks and get a champions league. Its a money grab and I fell for it. Get new levels on 3/2/26 only to go maybe 50 levels and no more levels. Come to 3/3, another champions league & have to wait another 2 weeks for levels. This is BS for so many reasons. You dont have levels but have levels for a champions league?! Not going through that again. You've lost my bankroll & me as a player. Way to go!

| | labels |
|---|---|
| gold | `S_Competition`, `T_InfiniteTreadmill` |
| pred | `T_PlayingByAppointment` |
| **missed** | `S_Competition`, `T_InfiniteTreadmill` |
| **spurious** | `T_PlayingByAppointment` |

**Did the model consider what it missed?**

- `S_Competition` - never mentioned -> **attention / recall**
- `T_InfiniteTreadmill` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer is describing a content-release bottleneck that has reached a level cap: the game has run out of new levels for them at around the 11,000th level. Their account of the last few weeks establishes a repeating schedule on the game's clock: the Champions League event runs for about two weeks, then new levels arrive, then the next Champions League begins almost immediately, and then there are no levels again for another two weeks. The complaint That levels exist for the Champions League while no ordinary levels are available expresses that this event cycle is the only thing to do while the game's next content drop is pending. The phrases 'get a champions league' and 'another champions league' name the event but not what it is, so a search is needed to identify it. From my understanding, the review is about forced waiting for progress due to game-determined content releases and about the Champions League event filling that gap; it is not about grinding, payment, or social mechanics.
```

**Labels assigned**

- `T_PlayingByAppointment` - **SPURIOUS**  _[span not verbatim]_
  - span: "No new levels for 2 weeks and get a champions league. ... Get new levels on 3/2/26 only to go maybe 50 levels and no more levels. Come to 3/3, another champions league & have to wait another 2 weeks for levels."
  - why: The span describes the game forcing the player to wait on its schedule for roughly two weeks because the game has no new levels to offer, with the Champions League event filling the gap; because the appointment is required for any progress, the wait is dark and plays by appointment.

**Search:** `Toon Blast Champions League event what is it` -> Champions League is a competitive event in Toon Blast for players who completed all available levels, running in league cycles over roughly two-week periods while new level releases are pending.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `57add346-8b93-4249-be50-1a39331cf79b` - RAID: Shadow Legends

> These are my views of the game after playing for almost a day. I didnt make a single purchase but got a free champion and silver from a referral. Pros: Easy to learn the controls and layout of the game, nice story line, easy combat system, no lag, nice champion designs and gameplay. Cons: Every single time you log in you are bombarded with pop ads advertising "special" or "limited time" deals, once your champions hit level 30 it becomes a horrible grind, p2p is the best way to win this game.

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury`, `M_PayToProgress`, `S_ForcedFellowship` |
| pred | `M_EasyToPurchase`, `M_PayToProgress`, `T_Grinding` |
| **missed** | `M_DeceptiveLuxury`, `S_ForcedFellowship` |
| **spurious** | `M_EasyToPurchase`, `T_Grinding` |

**Did the model consider what it missed?**

- `M_DeceptiveLuxury` - never mentioned -> **attention / recall**
- `S_ForcedFellowship` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer summarizes a day of play and then lists three cons. The first con describes the game's monetization interface: every login is interrupted by pop-up windows pushing 'special' or 'limited time' purchase deals. The complaint is about being bombarded at session start, which describes buy prompts that intercept the player on entering the game rather than mere listing of offers in a storefront. The second con names the progression problem outright as a 'grind' once champions pass level 30, i.e., repetitive play required to keep advancing. The third states that paying is the best way to win, which asserts that spending money confers an in-game competitive advantage. The pro note about getting a free champion and silver from a referral shows the reviewer benefited from a referral reward, but does not describe the game incentivizing the reviewer to recruit others, so I do not lift that to a recruitment pattern. The pop-ups are purchase solicitations, not ad views or rewarded ads, so Advertisement does not apply.
```

**Labels assigned**

- `M_EasyToPurchase` - **SPURIOUS**
  - span: "Every single time you log in you are bombarded with pop ads advertising "special" or "limited time" deals"
  - why: Pop-up purchase offers appear at every login and interrupt entry into the game, requiring dismissal to continue, which is a buying prompt intercepting the session rather than mere advertising volume.
- `M_PayToProgress` - ok
  - span: "p2p is the best way to win this game"
  - why: Saying pay-to-play is the best way to win asserts that spending money grants an advantage over not spending, even though the reviewer has not paid themselves.
- `T_Grinding` - **SPURIOUS**
  - span: "once your champions hit level 30 it becomes a horrible grind"
  - why: The reviewer names the progression phase explicitly as a grind, meaning repetitive tedious play is required to advance champions past level 30.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a59f5319-a1b7-4991-8c6b-d2d2ca56265c` - Fate/Grand Order (English)

> It's an unregulated casino. Every part of the game is set up to direct you towards the slot machine summoning system. Story? Free buffet and show to keep you interested. Plus, you like this character? Well, either hope you have godly luck, or fork over some cash (~$140 for 50% to get a 'rate up' character), because the majority of them are limited time only. Gameplay is mostly just grind to build sunk cost. That, and an incentive to roll the slots for things to reduce the amount of grind.

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury`, `M_Gambling`, `M_PayToProgress`, `M_UIMisdirection`, `P_EasyToGetHardToLose`, `P_RewardMania` |
| pred | `M_DeceptiveLuxury`, `M_Gambling`, `M_PayToProgress`, `P_EasyToGetHardToLose`, `P_RewardMania`, `T_Grinding` |
| **missed** | `M_UIMisdirection` |
| **spurious** | `T_Grinding` |

**Did the model consider what it missed?**

- `M_UIMisdirection` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer is describing Fate/Grand Order's monetized gacha structure and how it shapes the rest of the game. They first name the summoning system outright as a casino-style slot machine that the whole game funnels players toward. Then they describe a concrete purchase decision: a character the player likes is available only through luck or a large cash outlay, because most characters are offered only in limited-time windows. That last clause describes scarcity built into the item's availability, not into its odds. Finally they characterise gameplay itself as grind, and say the grind is deliberately there to build sunk cost, while rolls of the slot machine are incentivised because what they yield reduces that grind. The reviewer's account implies gameplay consists of repetitive farming (grind), that leaving is costly because time is already invested (sunk cost), and that money spent on the gacha buys both a chance at characters and a reduction of the grind burden. No term is ambiguous enough to require a search.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "the majority of them are limited time only"
  - why: Character availability is capped by a time limit invented by the developer, and the scarcity is what forces the fork-over-cash decision, so the manufactured limit bears directly on the purchase.
- `M_Gambling` - ok
  - span: "either hope you have godly luck, or fork over some cash (~$140 for 50% to get a 'rate up' character)"
  - why: The span shows real money staked on a chance outcome (a 50% chance at a featured character), which is using money in a game of luck for a prize.
- `M_PayToProgress` - ok
  - span: "an incentive to roll the slots for things to reduce the amount of grind"
  - why: Spending on the gacha yields things that cut down the grind, i.e., payment is promoted as a way to speed past the game's tedious progression work.
- `P_EasyToGetHardToLose` - ok
  - span: "grind to build sunk cost"
  - why: The reviewer explicitly says the grind's purpose is to accumulate sunk cost, describing the design that raises the cost of leaving through value the player has already invested.
- `P_RewardMania` - ok
  - span: "Every part of the game is set up to direct you towards the slot machine summoning system"
  - why: The summoning system is described as a slot machine, naming the gacha's random reward delivery that sustains engagement through unpredictability, independent of the monetary stake coded under Gambling.
- `T_Grinding` - **SPURIOUS**
  - span: "Gameplay is mostly just grind to build sunk cost"
  - why: The reviewer states the game's core activity is grind, and the later clause that purchased items exist 'to reduce the amount of grind' confirms grind is the required repeated task that payment exists to alleviate.

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

- `M_Gambling` - never mentioned -> **attention / recall**
- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer is describing two intertwined design behaviours in Disney Solitaire. First, a claim that the card dealing is rigged: no matter how the reserve cycles, the player is left with the same one card unplayable, and the reviewer contrasts this with an actual shuffled deck to argue the outcome is manipulated rather than random — an engineered near-win that never completes. Second, a claim about the monetization structure behind that rigging: the game is designed to hook the player early, then become impossible, specifically in order to funnel the player into paying; the in-game remedy for the dead end is paying astronomical coins for another handful of cards. The rigging accusation carries the outcome-manipulation mechanic, and the impossibility-plus-payment describes a pay wall.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "designed to get you hooked early to develop into impossibility, to suck you into paying money"
  - why: The reviewer states the game is deliberately engineered to become impossible in order to force real-money spending, with paying for more cards as the only route out of the dead end.
- `P_IllusionOfControl` - ok
  - span: "This is incredibly rigged; designed to get you hooked early to develop into impossibility, to suck you into paying money. You can be down to one card and have 10 cards left in your deck and end up going through those 10 cards and still have one card left."
  - why: The reviewer asserts the deal itself is rigged and gives evidence of a manipulated non-random outcome (same single card left after the whole reserve cycles), i.e., the game conceals how results are determined.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

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
The review makes two distinct complaints. First, the game was promoted as ad-free but shows ads anyway — that claim concerns marketing material outside the app, which R13 places outside the unit. Second, and within the installed game, the reviewer describes how an in-game ad behaves: the only way to get out of the ad is to go into the Play Store, which consumes more data. That is a dismissal mechanism that prevents the player from simply closing the ad, forcing continued engagement with the ad and routing the player through a store page to escape it. The exit-route design is the actual mechanic described and it is present in the game as played, so the disapproval of it (R7) does not suppress coding. The presence of ads alone would not be enough under the T_Advertisement counterexample, but the described dismissal obstacle relates the ads to being compelled to deal with them, which satisfies the definition.
```

**Labels assigned**

- `T_Advertisement` - **SPURIOUS**
  - span: "to get out of the ad, you have to go into the play store, which then uses even more data"
  - why: The ad cannot be exited normally; its only dismissal route sends the player into the Play Store, compelling engagement with the ad and forcing the player through an external store page to escape it.

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

- `T_Grinding` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes their lived experience of a retention loop in a strategy game. First they state the loop itself: showing up, completing tasks, consuming in-game resources (gold, potion), spending real money, then finding the same cycle waiting the next day ('Groundhog Day'). This describes daily resetting obligations the game imposes on its own clock — the player does not choose the cadence; the game's daily task cycle requires them to return and repeat. Second, the reviewer reads the design's intent back to the reader: being drawn in and made to invest creates a felt obligation to keep playing, which is a description of sunk investment operating on the decision to stay. Third, the reviewer concludes that the loop has no terminal payoff: no real progress or advancement and no end reward, meaning the cycle is designed to continue indefinitely rather than reach completion. The money mention is not tied to progression or to a real-money-to-currency conversion, and no social, competitive, or chance mechanics are described.
```

**Labels assigned**

- `P_EasyToGetHardToLose` - ok
  - span: "It's a way to get you drawn in and invested in the game, so you feel obligated to keep playing"
  - why: The reviewer explicitly describes the design mechanism: low-friction entry and accumulating investment of time and money raise the perceived cost of stopping, producing the obligation to continue.
- `T_InfiniteTreadmill` - ok
  - span: "There is no real progress or advancement; there is no pot of gold at the end of this rainbow"
  - why: The reviewer states that the repeating loop never advances toward an end and offers no terminal reward, i.e., the cycle is designed to keep the player running without ever reaching completion.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "I show up, complete tasks, spend gold and potion, spend real money, then come back tomorrow and do it all over again"
  - why: The daily resetting task cycle means the game's own schedule dictates when the player must return and repeat the same activities, which the reviewer frames as an obligation rather than free choice.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `2f50b132-9762-4f48-ae35-487f414aa41a` - MONOPOLY GO!

> Okay so I started playing in October of 2023. In the beginning, it was a fun game. Over time, I started to see the real issues in the game. 1. Most other players live by the motto you have to cheat to beat the game system and I am starting to feel they are right! 2. Events have become a joke. Peg-E is a total waste the new race car game is even worse! 3. Way to many gold duplicates! 4. Not enough trades a day! 5. Not enough dice.I could keep going but I only have 500 spaces, and I am at my limit

| | labels |
|---|---|
| gold | `P_RewardMania`, `S_Reciprocity` |
| pred | `P_CompleteTheCollection`, `P_RewardMania`, `T_PlayingByAppointment` |
| **missed** | `S_Reciprocity` |
| **spurious** | `P_CompleteTheCollection`, `T_PlayingByAppointment` |

**Did the model consider what it missed?**

- `S_Reciprocity` - never mentioned -> **attention / recall**

**Model analysis**

```
The review spans several mechanics. The player completes sticker collections: gold stickers are rare album pieces whose duplicates are called out as excessive, which speaks to the collection system's delivery. Trades per day are capped, a designed daily limit constraining an activity needed for collection progress. Dice are scarce, implying the in-game economy that demands currency for continued play. Events like Peg-E and the race car game are criticized as wastefully unrewarding. The opening line about cheating describes player conduct, not a design incentivising it.
```

**Labels assigned**

- `P_CompleteTheCollection` - **SPURIOUS**
  - span: "Way to many gold duplicates!"
  - why: The complaint about receiving duplicate gold stickers when seeking missing album pieces shows the player pursuing a full collection, and the harm is being denied the items needed to complete it.
- `P_RewardMania` - ok
  - span: "Peg-E is a total waste the new race car game is even worse!"
  - why: The reviewer describes event reward structures as poor value, indicating the reward delivery mechanisms drive engagement; the named events are chance/collection reward systems whose output is the complaint's target.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "Not enough trades a day!"
  - why: A daily cap on trades is an in-game timer limiting how often the player can perform a collection-related action, scheduling when the player may act rather than letting them play freely.

**Search:** `what are gold stickers in Monopoly GO and why do duplicate gold stickers matter` -> Gold stickers are rare collection pieces; gameplay mechanics center on completing sticker albums and obtaining all stickers.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `ce1c6456-5d34-4001-a1a8-8b5991ef8ffb` - War Robots Multiplayer Battles

> Too much greed by the game devs. You are not just bombarded with tons of advertisements but after you progress up through the rankings, you notice you are always competing with gamers way above your paygrade. The strategy is to make you spend and spend to reach to upper levels. Toxic pity, I would say. Better to spend £50 in a Console game and play for ages, than spend £50 in this game just to get a lame account. The more you pay, more the prices start to increase as well. Run!!

| | labels |
|---|---|
| gold | `M_PayToProgress`, `S_Competition`, `T_Advertisement` |
| pred | `M_PayToProgress`, `P_IllusionOfControl`, `S_Competition` |
| **missed** | `T_Advertisement` |
| **spurious** | `P_IllusionOfControl` |

**Did the model consider what it missed?**

- `T_Advertisement` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review is a complaint about monetization and competitive structure in War Robots. The mechanics it actually names are: (1) heavy advertisement volume ('bombarded with tons of advertisements'), which is stated only as bombardment with no claim of being forced to watch or rewarded for watching, so it does not instantiate Advertisement; (2) PvP matchmaking that constantly pairs the reviewer against opponents far above their level ('gamers way above your paygrade'), which the reviewer explicitly interprets as a deliberate design strategy to pressure spending ('The strategy is to make you spend and spend to reach to upper levels'); and (3) an escalating price claim ('The more you pay, more the prices start to increase as well') that fits no listed label. The core coded content is competitive play against superior opponents whose advantage is tied to paying, plus the reviewer's assertion that matchmaking is deliberately arranged to extract money for advancement.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "The strategy is to make you spend and spend to reach to upper levels"
  - why: The span asserts that the design pairs the player with stronger opponents and that reaching upper levels is achieved through repeated spending, i.e., exploiting competitiveness to make the player pay to progress.
- `P_IllusionOfControl` - **SPURIOUS**
  - span: "you notice you are always competing with gamers way above your paygrade. The strategy is to make you spend and spend to reach to upper levels."
  - why: The reviewer asserts that matchmaking deliberately pits them against far stronger players as a strategy to induce further spending, a claim of manipulated matchmaking serving the developer rather than genuine competition.
- `S_Competition` - ok
  - span: "you are always competing with gamers way above your paygrade"
  - why: The reviewer describes being placed in competition against other, higher-ranked players, which is the game making players compete against each other.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (19)

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
The reviewer describes a starter pack being purchased without any deliberate action on their part: no tap, and no fingerprint or password challenge despite their device settings requiring authentication for purchases. What is being described is a purchase flow that executed with no confirmation or friction, i.e., an accidental purchase. The closing sentence ('Not sure if it's just a glitch or what') is speculative uncertainty about the cause, not a definitive attribution of the behavior to a technical fault, so R11 does not suppress the label; the described design behavior is that a real-money purchase was completed without the player's input or an authentication barrier.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "it notified me that I bought a starter pack. I didn't tap anything and my settings are set up to where I have to input my fingerprint or password to make a purchase and it did not do that"
  - why: The span shows a real-money purchase executed with no player action and no confirmation or authentication barrier, matching the accidental purchase pattern; the reviewer's 'not sure if it's just a glitch' is speculation about cause rather than an affirmative bug attribution, so the described no-confirmation purchase design is still coded.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `2fd4ef32-a33b-44ed-a921-2889ba6e0375` - Ludo King®

> Dice rolls are not random at all, they are preplanned. Game randomly decides at the start of the play that which player has to win and dice rolls according to it. You also will know at the beginning of the game that who is going to win. One player will get more and more 6s and another one will get 1 or 2 mostly. The rolls have gone predictable. That's why I have uninstalled the game today. It's frustrating.

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_Competition` |
| pred | `P_IllusionOfControl` |
| **missed** | `P_OptimismAndFrequencyBiases`, `S_Competition` |

**Did the model consider what it missed?**

- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**
- `S_Competition` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer is describing Ludo King's dice rolls as rigged: they assert that the outcome of each match is decided in advance and the dice simply follow the game's predetermined script, giving one player repeated 6s and the other low rolls. The complaint is not about bad luck in a fair game but about the game secretly controlling the results to pick a winner. That is a claim that the game conceals how outcomes are determined, which is the core of Illusion of Control. No monetary mechanic, schedule, social mechanic, or chance-based reward purchase is described; the whole review concerns one design behavior, the rigged dice.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "Dice rolls are not random at all, they are preplanned. Game randomly decides at the start of the play that which player has to win and dice rolls according to it. You also will know at the beginning of the game that who is going to win. One player will get more and more 6s and another one will get 1 or 2 mostly."
  - why: The reviewer asserts the dice outcomes are secretly predetermined by the game to fix the winner, i.e., the game manipulates the determination of results rather than running a fair random process.

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
The reviewer is describing two things about the hero unlock system. First, progression to new heroes is extremely slow: after roughly 100 fights they still only have the two starting heroes, which implies unlocking is tied to repeating matches many times over a long grind before any progress shows. The repeated fighting required to advance is the mechanic being described. Second, the in-game 'share to unlock this hero' reward feature does not work for the reviewer — that is a malfunction report about a social-sharing reward, not a description of an incentive actually operating, so R11 excludes it. The closing line ('thinking about installing' the app, i.e., uninstalling) expresses disengagement and is not a mechanic. No purchase, schedule, timer, or social obligation is described.
```

**Labels assigned**

- `T_Grinding` - ok
  - span: "takes quite a long time to unlock new heros...I have done close to 100 fights and still have the first two heros you get when you start the game"
  - why: The player must run the same repeated activity (fighting, ~100 matches) to unlock heroes, and the span shows that repetition yielding no visible progress, which is grinding.

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
The reviewer describes the ad experience in the game. Ads appear at a fixed point in gameplay ('after every over'), interrupting the session, and the reviewer calls them forced ('stop forcing ads like this'). Separately, tapping the ad instead of the cancel control causes the game to close and the ad to open; the reviewer frames this as 'bad app behavior' to fix and does not attribute any deliberate design purpose to it, which reads as a technical/ad-network fault rather than a designed manipulation. The repeated interruption of play by ads is a functional design behavior, while the app closing on an accidental tap is presented as a malfunction and is not a dark pattern under R11.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "After every over, an ad pops up."
  - why: The ad interrupts play on a fixed cadence after every over, and the reviewer explicitly calls the practice 'forcing ads', so the span describes compelled in-game ad exposure.

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
The reviewer is describing a merge-style game where continued progress stalls behind purchases. Three specific mechanics are named: (1) in-app purchases become effectively required to do anything ('you can't do anything without using in app purchases'); (2) card packs and mini-games cannot be completed without real money, which describes a collection/completion goal that the game gates behind payment; and (3) an energy cap that only covers part of an order, with gems needed to finish it, so the session's progress ceiling is a spendable-resource constraint rather than a described wait or timer. The closing line about feeling trapped is general evaluation and does not name a separate mechanic. The energy cap is described as an insufficient allowance, not as an energy refill schedule or timer, so Playing by Appointment does not apply. Gems are spent but never shown being bought with real money, so Intermediate Currency is not established.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "you can't do anything without using in app purchases. you will never be able to complete the card packs and other mini games without being forced to pay real money for it. the energy cap will barely get you midway through an order unless you use all your gems"
  - why: Progress, completing card packs and mini-games, and finishing orders are all stated to be blocked unless the player pays or spends the premium resource (gems), i.e., further progress is contingent on payment.
- `P_CompleteTheCollection` - ok
  - span: "you will never be able to complete the card packs and other mini games without being forced to pay real money for it"
  - why: The review names card packs as an in-game collection whose completion is a presented goal, and describes that goal as unachievable without payment, showing the collection system being used as a spending lever.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `ee8d0008-1f3c-400d-bbbe-d29e8a7c0405` - Tiles Survive!

> Extremely pay2win bundled with a bunch of game modes where strong players steal from weaker players, furthering a divide that only more money can bridge.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `S_Competition`, `S_EncouragesAntiSocialBehavior` |
| pred | `M_PayToProgress`, `S_EncouragesAntiSocialBehavior` |
| **missed** | `S_Competition` |

**Did the model consider what it missed?**

- `S_Competition` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a single state of affairs: the game is pay-to-win, and its multiplayer modes let established strong players take resources from weaker players, which widens the gap between paying and non-paying players. The pay-to-win claim names the monetized advantage directly, and the closing clause makes the money the only bridge across the competitive divide. The stealing modes describe a design that structures play so the stronger side can prey on the weaker side and profit from it — asymmetric predation beyond ordinary sanctioned PvP, since the harm falls on players who cannot respond. No currency, pass, timer, reward calendar, or technical feature is mentioned, so no other labels are in play.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Extremely pay2win bundled with a bunch of game modes where strong players steal from weaker players, furthering a divide that only more money can bridge"
  - why: The reviewer names the pay-to-win mechanic outright and explains that the resulting advantage gap can only be closed by spending more money, i.e., payment buys competitive advantage.
- `S_EncouragesAntiSocialBehavior` - ok
  - span: "game modes where strong players steal from weaker players"
  - why: The modes reward the stronger player for taking from weaker players who cannot defend themselves — harmful asymmetric conduct incentivized by design, which the reviewer explicitly contrasts with fair play.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `2471db11-2c61-415a-8af4-33b80a05c759` - Clash of Clans

> The balancing makes this game have no point. So many bugs, to many sales, support is non existent. You will spend months upgrading troops and defenses just to be nerfed. I have a maxed out account and anyone can destroy me. The more you play the game the more it penalizes you. Reduced times for people that don't play as much. Every account recieves different reward amounts. I've played over 10 years, it's just a chore at this point, not fun. They ruin COC more with every update and event.

| | labels |
|---|---|
| gold | `M_PowerCreep`, `T_Grinding` |
| pred | `M_PowerCreep` |
| **missed** | `T_Grinding` |

**Did the model consider what it missed?**

- `T_Grinding` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer lists several complaints: balance, bugs, sale volume, missing support, and ten years of fatigue. The one concrete design behaviour described is devaluation of invested progress: the player spends months making permanent upgrades to troops and defenses and those upgrades are later nerfed, so the value of what they built is taken away after the fact ('maxed out account and anyone can destroy me' reinforces that even full investment no longer holds value). The reward/timer comment describes the inverse of a daily-return incentive: accounts that play less get reduced upgrade times and different reward amounts, penalising active players rather than rewarding daily return — this is not Daily Rewards, which requires incentives for logging in and penalties for missing a day, and no play schedule is imposed on this player. 'Just a chore' names no repetitive activity tied to progress, so it is an evaluation rather than Grinding. 'Too many sales' names no friction-reducing purchase mechanism. Bugs are excluded under R11.
```

**Labels assigned**

- `M_PowerCreep` - ok
  - span: "You will spend months upgrading troops and defenses just to be nerfed."
  - why: Permanent upgrades the player invested months in lose their value through post-acquisition rebalancing (nerfs), which is devaluation of held progress via updates — the same mechanism as the 'they literally nerf your old stuff' worked example.

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
The reviewer is describing how Homescapes pressures them after losing a puzzle level. Three related mechanics appear. First, losing triggers a message tying the loss to the leaderboard and to losing accumulated streak rewards, with payment offered as the way to avoid both: this is a monetized competitive prompt. Second, the leaderboard itself is a system that ranks the player against other players, which the reviewer explicitly resents being forced into ('force you to be competitive', 'opt out of the leaderboard system'). Third, the same post-loss reminder works as anticipatory pressure: the player is warned they will fall down the rankings and forfeit their streak rewards unless they act, which is designed to make them feel they are falling behind. The 'winning streak rewards' here are forfeited on losing a level, not on missing a daily login, so Daily Rewards does not apply; no schedule or timer is described, so Playing by Appointment does not apply either.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "every time you lose the game reminds you that unless you pay up, you're going to go down on the leaderboard and will lose all your winning streak rewards"
  - why: The span shows the game prompting the player, after every loss, to pay in order to keep their leaderboard position and streak rewards, i.e., money buys competitive standing.
- `S_Competition` - ok
  - span: "I hate how the game tries to force you to be competitive"
  - why: The reviewer explicitly describes being made to compete through the leaderboard system and being penalised for losing, i.e., head-to-head ranking against other players.
- `S_FearOfMissingOutFOMO` - ok
  - span: "unless you pay up, you're going to go down on the leaderboard and will lose all your winning streak rewards. it makes you feel bad for not winning every level on the first attempt"
  - why: The reminder instills anticipatory pressure: the player is made to feel bad and anxious about falling behind other players and forfeiting rewards, pushing them to keep winning or pay to avoid the loss.

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
The reviewer, a long-time player, complains about the character/roster economy of Genshin Impact since the Fontaine update. Concretely: new characters now require premium team compositions and are locked to niche teams, making a usable roster costlier; previously acquired characters have lost viability ('old characters started falling off'); the meta changes too fast; and free rewards per patch are too low to reach hard pity, the guaranteed-pull threshold of the game's gacha. The devaluation of already-owned characters by new releases and fast meta shifts is the core mechanic described, which matches Power Creep directly. The mention of 'hard pity' names the gacha draw mechanic, and the complaint frames patch rewards against that delivery threshold. I considered Pay to Progress, Intermediate Currency, and Gambling, but no span explicitly describes money entering the game or payment removing a roadblock, and the codebook warns against assuming monetization for gacha and currency mechanics. The opening 'invested so much time and effort' reports investment but does not show it operating on the decision to leave, so Easy to Get, Hard to Lose is not assigned either.
```

**Labels assigned**

- `M_PowerCreep` - ok
  - span: "old characters started falling off which I hope they could climb back up. And now the Meta shifts now are extremely fast"
  - why: Characters the player already acquired are described as losing viability as new Fontaine characters and rapid meta shifts arrive, i.e., purchased items depreciating through new releases and rebalancing.
- `P_RewardMania` - ok
  - span: "it's so low each patch barely gives us enough to hit hard pity"
  - why: 'Hard pity' names the gacha delivery system through which characters are obtained, and the complaint is that the per-patch reward flow falls short of that random-reward threshold, describing the delivery schedule rather than a purchase.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `7732d254-0a39-4614-acf4-e67840e14b76` - Cashman Casino Slots Games

> loading takes entirely tooooo long also the bonus lady rarely comes out or even matches with anything on ww4. iv started playing a new game and buying coins from them.ill check inevery so offethen to see if it has changed . hopefully this rating will do it.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `P_RewardMania` |
| pred | `P_RewardMania` |
| **missed** | `M_IntermediateCurrency` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**

**Model analysis**

```
The review has three components. First, a complaint that loading takes too long: per the codebook's treatment of waits, loading times arising from the operation of the service rather than from a designed gate are not Playing by Appointment, so no tag comes from that. Second, a description of the slot game's bonus feature ('the bonus lady') rarely triggering and rarely paying out ('or even matches with anything on ww4'): this describes the reward-delivery behaviour of the slot — a rare, unpredictable bonus payout schedule — which is the variable-reward mechanism the game is built around, coded regardless of the reviewer's annoyance. Third, the reviewer announces they have moved to another game and are buying coins there; that statement concerns a different product and the reviewer's own behaviour, not a mechanic of this game, so it is not codable. No monetary stake in this game's chance mechanics is described, so Gambling is not supported.
```

**Labels assigned**

- `P_RewardMania` - ok
  - span: "the bonus lady rarely comes out or even matches with anything on ww4"
  - why: The span describes the slot's bonus as triggering rarely and paying nothing when it does, i.e., its rewards are delivered on a rare, unpredictable schedule, which is the variable-reward delivery mechanism that defines the game's engagement structure.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b6745663-5486-4e5b-9066-8a889055d8bc` - Travel Town - Merge Adventure

> it's a good hook. the completionist in me wants to get every level, and the matching is satisfying enough to really tempt me into buying gems/energy to play more. I wish there was a way to disable all the event pop-ups. opening the app and then having to click away ten different challenges is very annoying. at least there are no outside ad pop-ups but I would rather have more optional outside ads than the unskippable events. please consider having a dismiss option for the events! good game.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `M_PayToProgress`, `M_UIMisdirection` |
| pred | `M_IntermediateCurrency` |
| **missed** | `M_PayToProgress`, `M_UIMisdirection` |

**Did the model consider what it missed?**

- `M_PayToProgress` - never mentioned -> **attention / recall**
- `M_UIMisdirection` - never mentioned -> **attention / recall**

**Model analysis**

```
The review is mostly positive and describes three things. First, the reviewer's own completionist drive ('the completionist in me wants to get every level') is self-reported psychology, not a described game mechanism that capitalises on it, so no collection pattern is codable. Second, the reviewer is tempted by the satisfying matching to spend on 'gems/energy' to keep playing: this names purchasable in-game resources (premium currency and energy), i.e., real money converted into virtual currency, which is the object-acquired direction of Intermediate Currency. Third, the complaint about event/challenge pop-ups on app open with no dismiss option describes an annoyance and expresses hypothetical wishes (R12); nothing connects those pop-ups to purchases, so Easy to Purchase, UI Misdirection, and Advertisement (the reviewer explicitly says there are no outside ad pop-ups) do not apply. No wait, schedule, grind, or session-loss mechanic is described.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "really tempt me into buying gems/energy to play more"
  - why: The phrase names gems, an in-game currency the player would acquire with real money, showing the real-money-to-virtual-currency exchange that defines Intermediate Currency; the temptation to purchase presupposes the monetised currency exists in the game.

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
The reviewer describes an in-game ad that lacks a working close control. Because the ad cannot be dismissed, gameplay is halted mid-session and the only way to continue is to close and relaunch the app. This is a forced encounter with an advertisement that interrupts and blocks play, not merely the presence of ads in the game and not a complaint about ad frequency or content. Nothing in the text attributes the behavior to a bug or technical fault, so R11 does not suppress the pattern; an unclosable interstitial that gates continued play is a deliberate ad-delivery design. No payment option or alternative escape is described, so no monetary label applies. The span shows the ad compelling the player to deal with it (endure it or restart) before play can resume.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "Can't close the ads, therefore can't continue playing without closing and restarting the game."
  - why: The ad cannot be dismissed and halts continued play, forcing the player to either endure or circumvent it by restarting the game, which is a compelled encounter with an in-game advertisement.

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
The review is wholly positive: it praises the game's features and bonuses, then recounts an accidental real-money purchase of a coin pack that the developer promptly refunded. Mechanically, the only in-game design behaviour actually described is the existence of coin packs acquired for real money (the refund confirms real money was the consideration), which is the defining relation of Intermediate Currency under the direction-of-transaction rule. The accidental purchase is framed explicitly as the player's own mistake ('I messed up') and was successfully refunded, so no interface-driven accidental-purchase mechanism, absent confirmation, or inability to undo is described; if anything the working refund contradicts the Easy to Purchase indicator. Nothing in the review describes any other monetisation, temporal, social, or psychological mechanic.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "I messed up and accidentally bought a huge coin pack"
  - why: The reviewer describes acquiring a pack of in-game coins with real money (the prompt refund implies the payment), i.e., real-world money exchanged for virtual currency, which is the pattern's defining relation regardless of the review's positive tone (R7).

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a12fb168-3791-4d93-8cee-9b38fceb3059` - Moba Legends: 5v5!

> If you want to get some serious anger issues and frustration,the game is for you.This game simply don't care about you at all,they only need money and frame(Obv it's a complete copy of league of legends). The match making, completely illogical,if you play good,game will give you bad teammates expecting you to carry and if you play bad,game will give you more bad teammates saying that it's so called "skill based matching". The only thing game will provide you is waste of time and energy

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `S_Competition` |
| pred | `P_IllusionOfControl` |
| **missed** | `S_Competition` |

**Did the model consider what it missed?**

- `S_Competition` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer is complaining about a MOBA's matchmaking. Three complaints surface: the developer only wants money (a vague accusation of monetization with no purchase, currency, or paywall mechanic named, so not codeable under R2); rigged matchmaking that responds to the player's own performance by supplying bad teammates so the player must carry, with the game labeling it 'skill based matching'; and the game being a waste of time and energy (an evaluation of quality, not a described mechanic). The only concrete game behaviour described is the matchmaking rule: the reviewer asserts the game deliberately manipulates who it pairs the player with depending on how well they play, concealing a non-random schedule behind a 'skill based' label. That is a claim of concealed, outcome-tuned matchmaking rather than a losing streak, a bug, or a general unfairness complaint. Nothing describes repetitive tasks (Grinding), scheduled waits, currency systems, payments, or social mechanics.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "The match making, completely illogical,if you play good,game will give you bad teammates expecting you to carry and if you play bad,game will give you more bad teammates saying that it's so called "skill based matching""
  - why: The reviewer asserts the matchmaker operates on a hidden, performance-reactive rule — worse teammates after good play to force carrying — while the game labels it 'skill based matching', i.e., concealed manipulation of outcome determination rather than random or unlucky pairing.

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
The review is about a live Ludo match against another player. It describes an existing 'Auto Playing' feature in which a bot takes over for a player who is not responding. The practical consequence for the player still present is that the match cannot reach a normal ending and they are compelled to exit the session, which costs them their staked credits. That describes a session the player cannot leave at a moment of their choosing without forfeiting value — the bot's unlimited play removes the game-defined stopping point. The review then states that some players deliberately exploit this unlimited-bot situation to strip credits from opponents, an abuse of a designed feature rather than sanctioned competitive play. The request to improve the feature concerns the same existing mechanics, so those descriptions remain codable under R12; only the proposed limitation itself is not coded.
```

**Labels assigned**

- `S_EncouragesAntiSocialBehavior` - ok
  - span: "Some players can also misuse this feature to grab the credits of the corresponding players"
  - why: Players deliberately trigger the unlimited auto-play bot to force opponents out and take their credits; the design enables the dishonest, asymmetric conduct and the aggressor gains the victim's credits.
- `T_MandatoryMarathon` - ok
  - span: "the second player at the end have to exit and lose his credits because there are no limitations are for the Bot"
  - why: The bot plays on without limits, so the match has no reachable end; the remaining player can stop only by exiting, and exiting forfeits credits — the player is prevented from ending the session at their own choice without losing holdings.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `71d54398-28c7-4f4a-a67d-0914206f59c6` - GODDESS OF VICTORY: NIKKE

> Gacha is quite scummy. If you started with no currency and wanted a guaranteed unit, it's 200 tickets. You get about 20 tickets with $80 so even being generous it's still $600-$800 just to guarantee the unit you want. 4% chance to pull any SSR at any time. In a 10-pull that's around a 33% chance give or take. I failed that 15 times in a row, so 150 pulls with no SSR (supposedly 1/456 chance of happening) . Great system. Really makes players not want to quit or anything.

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury`, `M_Gambling`, `M_IntermediateCurrency`, `P_RewardMania` |
| pred | `M_Gambling`, `P_RewardMania` |
| **missed** | `M_DeceptiveLuxury`, `M_IntermediateCurrency` |

**Did the model consider what it missed?**

- `M_DeceptiveLuxury` - never mentioned -> **attention / recall**
- `M_IntermediateCurrency` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a gacha pull system: how they attempted to obtain an SSR unit, the advertised SSR rate (4%), the statistical failure of 150 pulls without an SSR, and an explanation of the real-money cost to reach the 200-ticket purchase guarantee. The mechanic being discussed is the premium lottery of pulls and the ticket pity system that counteracts it. The concern about how much it costs and how long the outcome of each pull takes is about gambling economics, not about a roadblock to normal game progress. The money buys pulls; the pulls are chance events; the tickets and rate stats describe the reward delivery schedule. The closing sarcasm is evaluative and does not by itself evidence sunk-cost retention.
```

**Labels assigned**

- `M_Gambling` - ok
  - span: "You get about 20 tickets with $80 so even being generous it's still $600-$800 just to guarantee the unit you want. 4% chance to pull any SSR at any time."
  - why: The span connects real money ($80, and extrapolated $600-$800) to randomized pulls at a stated SSR rate, satisfying the definition of a paid chance-based reward mechanic.
- `P_RewardMania` - ok
  - span: "4% chance to pull any SSR at any time. In a 10-pull that's around a 33% chance give or take. I failed that 15 times in a row, so 150 pulls with no SSR (supposedly 1/456 chance of happening)"
  - why: The span names a gacha draw system with advertised rates and describes the repeated random reward attempts (150 pulls), which instantiates the gacha/variable-reward indicator regardless of the monetary stake.

**Search:** `NIKKE Goddess of Victory gold mileage tickets 200 guarantee SSR how to get` -> Tickets are 'Gold Mileage Tickets' earned one per pull on the Special Recruit banner; 200 accumulated tickets can be exchanged for the featured SSR, which clarifies that the real money buys pulls rather than the tickets directly.

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
The reviewer is describing the sticker-album completion system in MONOPOLY GO!. The album is a finite set of collectible stickers; gold cards are a sub-set that cannot be traded and are rarely awarded. The reviewer states they have needed only the gold cards for two months and have been awarded just one new card in that time, and that the Golden Blitz opportunity never features a card they need. That account describes a collection mechanic that keeps the player pursuing the last unowned items, with the missing cards deliberately withheld by the delivery system. The review mentions no real-money purchase, no payment option, no wager, and no timer or daily-login rule, so no monetary or temporal label is supported: the complaints about event difficulty and limited dice describe the economy's scarcity without naming any paid alternative. The dominant mechanic described is the album/collection loop itself, which the player has chased for two months and frames as the reason they will only stop 'after this album'.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "I have been needing only gold cards for two months now and have only been awarded one new card in that time, and the golden blitz has never been a card that I am in need of"
  - why: The player is locked into finishing the sticker album, chasing only the remaining unowned gold cards for two months while the game withholds them and the blitz never offers the needed ones — the album system's unowned-item emphasis is what keeps the collection loop running, and the reviewer even frames quitting only after this album concludes.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b4d6e64c-bd0c-49aa-9023-ed3f59bc63bf` - Match Masters

> Seems like FOREVER since my last enjoyable gaming experience, until I downloaded this colorful, graphic & challenging app! Only one issue & it's a rather strange one. Played a bit this week.Really enjoyed it! I decided 2 form a team, so invites were sent 2 gaming friends fr other apps, FB friends etc. 12 hrs later I'd a chat room filled w/48 strangers on my team?? My real friends downlded & "joined" my team, but no success on their end or mine & NO coins rewarded!

| | labels |
|---|---|
| gold | `S_ForcedFellowship`, `S_FriendSpamImpersonation` |
| pred | `S_ForcedFellowship` |
| **missed** | `S_FriendSpamImpersonation` |

**Did the model consider what it missed?**

- `S_FriendSpamImpersonation` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes forming a team in Match Masters and using the game's invitation system to recruit friends from outside the game (gaming friends from other apps, Facebook friends), expecting a reward in coins when those friends downloaded the game and joined the team. The complaint is that the friends were not credited and no coins were delivered. The mechanic being exercised is a referral/recruitment design: the player brings new people into the game through invites and is incentivized with coins for successful joins. The failure to credit is reported as a malfunction of the referral accounting, but the underlying design — rewarding recruitment of new players — is a deliberate social mechanic that the review describes in operation. The 48 strangers filling the chat room describe team openness, not a codebook pattern. No term needs external resolution.
```

**Labels assigned**

- `S_ForcedFellowship` - ok
  - span: "I decided 2 form a team, so invites were sent 2 gaming friends fr other apps, FB friends etc. 12 hrs later I'd a chat room filled w/48 strangers on my team?? My real friends downlded & "joined" my team, but no success on their end or mine & NO coins rewarded!"
  - why: The reviewer was led by the game's team/coin-reward design to invite outside friends to download and join, and complains the promised coins were not credited — the invite-friends-for-rewards referral mechanic is present even though its payout failed to register.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `ab9a6418-85dc-4e82-a279-bab6e1e5e148` - Carrom Pool: Disc Game

> (1) The shooting time is too short. (2) The foul thing is unfair because if I put a chip into a pocket and I have a foul, it takes out 2 chips, not just the one I put inside. (3) The openning time for the chests is too long, 1 or 2 hours is fine, but 8 and 12 hours?!...come on! (4) The Practice option disappears when the game detects a network connection, should be available with it. (5) It's impossible to play when other players are using cheats, they do perfect shots in impossible situations.

| | labels |
|---|---|
| gold | `S_Competition`, `T_PlayingByAppointment` |
| pred | `T_PlayingByAppointment` |
| **missed** | `S_Competition` |

**Did the model consider what it missed?**

- `S_Competition` - never mentioned -> **attention / recall**

**Model analysis**

```
The review lists five separate grievances about the game. (1) The shooting timer being too short is a gameplay rule about turn length, not a manipulative scheduling mechanic. (2) The foul rule removing two chips instead of one describes an in-game penalty rule the reviewer finds unfair; nothing in the codebook covers a foul penalty of this kind. (3) Chest opening times of 8–12 hours describe an in-game timer that imposes an arbitrary wait on the player before a reward can be collected: that matches the Wait to Play pattern. (4) The Practice option disappearing when a network connection is detected is a quirky technical behavior with no listed dark-pattern equivalent. (5) Other players using cheats is player conduct, not a design that incentivizes dishonest play, so it does not trigger Encourages Anti-Social Behavior under its boundary rule.
```

**Labels assigned**

- `T_PlayingByAppointment` - ok
  - span: "The openning time for the chests is too long, 1 or 2 hours is fine, but 8 and 12 hours?!...come on!"
  - why: Chests can only be opened after a fixed in-game timer of 8–12 hours, forcing the player to wait on the game's schedule to collect the rewards they have already earned.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (4)

### `2b915fb2-6ff4-4351-9b2f-e8db5661e0a5` - Dark War Survival

> accidentally brought a pack when I double tapped the screen got a refund for the pack through Google play and now my game has been locked and they are holding my account to ransom until I pay the equivalent of the refund I got, thanks ffs, respond promptly my a**, I explained the problem and after what would be considered not very promptly was told you would continue to hold my account ransom, I explained further and you don't bother to respond at all

| | labels |
|---|---|
| gold | `M_EasyToPurchase` |
| pred | `M_EasyToPurchase`, `M_PayToProgress` |
| **spurious** | `M_PayToProgress` |

**Model analysis**

```
The review describes two separate design behaviours. First, a real-money purchase fired from a double-tap on screen, which the reviewer calls accidental: that implies the storefront committed the purchase without any meaningful confirmation or safeguard between the input and the charge. Second, after the reviewer obtained a refund through Google Play, the game locked the account and demanded repayment of the refunded amount before restoring access: that is a payment wall — the game is unplayable until money is paid. The customer-service tone of the complaint does not change the underlying mechanics described.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "accidentally brought a pack when I double tapped the screen"
  - why: A single double-tap executed a paid pack purchase, implying the interface commits real-money transactions without requiring a deliberate confirmatory step.
- `M_PayToProgress` - **SPURIOUS**
  - span: "now my game has been locked and they are holding my account to ransom until I pay the equivalent of the refund I got"
  - why: The account is locked and continued access to the game is contingent on making a payment, which is an unplayable-without-payment wall rather than a bug or technical fault.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `d8278e85-b5f2-45ef-88ad-ea3370a5195d` - Whiteout Survival

> There is basically no real time gameplay. No gameplay at all really. Loaded it up for the first time in a week to a flashing button I didn't recognise. Clicked the button "DO YOU WANT TO PAY US $8?!" lol... No whiteout survival, I don't.

| | labels |
|---|---|
| gold | `M_UIMisdirection` |
| pred | `M_EasyToPurchase`, `M_UIMisdirection` |
| **spurious** | `M_EasyToPurchase` |

**Model analysis**

```
The review opens with an evaluation that the game has no real gameplay, which is a quality judgement naming no mechanic and codes NONE. The one concrete design behaviour described is the moment the reviewer reloads the game after a week away: instead of gameplay they are greeted by a flashing button whose purpose is not recognisable until clicked, at which point it turns out to be a request to pay $8. That is a UI element using animation to draw the player's attention to a payment option, and a purchase prompt presented at the point of loading the session rather than through the player seeking out a store. Both are codable interface mechanics: the flashing attention-grabber for UI Misdirection, and the buy prompt intercepting the opened session for Easy to Purchase. The week-long absence and return carry no reward or penalty cycle, so no temporal or FOMO labels apply.
```

**Labels assigned**

- `M_EasyToPurchase` - **SPURIOUS**
  - span: "Clicked the button "DO YOU WANT TO PAY US $8?!""
  - why: A purchase prompt is presented the moment the game loads rather than being sought out by the player, intercepting the start of the session with a buying offer; per the boundary rule, a buying prompt that interrupts the session qualifies even though the player easily declined.
- `M_UIMisdirection` - ok
  - span: "Loaded it up for the first time in a week to a flashing button I didn't recognise. Clicked the button "DO YOU WANT TO PAY US $8?!""
  - why: The flashing animation on the unrecognised button directs the player's attention to a payment option and draws the click, which is the use of animation to focus attention on a buy element; the span connects that attention-direction to a purchase, satisfying the monetary-class boundary rule.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `41a6813f-af68-497a-ac7b-2532b4659186` - Jackpot Party Casino Slots

> this game isn't that great! it's IMPOSSIBLE to win ANYTHING jackpot party! you come close, but NOTHING is won or any game with REAL MONEY or prizes are always just a few points or coins away from a jackpot

| | labels |
|---|---|
| gold | `P_OptimismAndFrequencyBiases` |
| pred | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases` |
| **spurious** | `P_IllusionOfControl` |

**Model analysis**

```
The review describes a casino slots app from the player's own losing experience. What the reviewer is actually describing, without using design vocabulary, is the game's outcome behaviour: they claim it is impossible to actually win, and that play always ends just short of a jackpot — a few points or coins away. That is a description of systematic near-miss outcomes, the classic slot-machine pattern where the game presents the appearance of having almost won. No real-money spending is described, only the existence of 'REAL MONEY or prizes' games, so no wager-based gambling tag is warranted. No timers, ads, currencies, or social mechanics appear.
```

**Labels assigned**

- `P_IllusionOfControl` - **SPURIOUS**
  - span: "it's IMPOSSIBLE to win ANYTHING jackpot party! you come close, but NOTHING is won or any game with REAL MONEY or prizes are always just a few points or coins away from a jackpot"
  - why: The reviewer asserts outcomes never land on a win and are 'always just a few points or coins away from a jackpot', claiming the game systematically brings the player to the verge of winning without letting it land — an engineered near-miss pattern that conceals how results are determined.
- `P_OptimismAndFrequencyBiases` - ok
  - span: "you come close, but NOTHING is won or any game with REAL MONEY or prizes are always just a few points or coins away from a jackpot"
  - why: The span reports near-misses felt as constant ('you come close', 'always just a few points or coins away'), the perceptual frequency effect of the near-miss design, so it carries both the alleged design (IoC) and the frequency perception (O&FB).

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `6ccb26a7-01e3-41a3-ba1a-bddba2063257` - Lightning Link Casino Slots

> Dont even waste you time with this app. I dont understand why you guys make these things so fun to play but impossible to ever win. I mean I know your trying to make money on the app but why would I ever come back and spend more money when it is impossible to when. Because of that this app is garbage!!!!!!!

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `P_IllusionOfControl` |
| **spurious** | `P_IllusionOfControl` |

**Model analysis**

```
The reviewer is playing a casino-style slots app and describing the odds of the game itself. The account has three parts: the game is fun, the game is impossible to win, and the developer is trying to make money. The complaint that the developers 'make these things so fun to play but impossible to ever win' attributes the outcome distribution to deliberate design: winning is asserted to be impossible by construction, not merely unlucky on this player's session. That is a claim that the game determines or conceals the determination of its outcomes. The mention of 'spend more money' is hypothetical and framed as a reason not to return, so no purchase mechanic currently operating is described, and no wager or currency purchase is named, so Gambling and Pay to Progress are not supported. No wait, schedule, or grind is described either.
```

**Labels assigned**

- `P_IllusionOfControl` - **SPURIOUS**
  - span: "I dont understand why you guys make these things so fun to play but impossible to ever win"
  - why: The reviewer states the developers built the game so that winning is impossible, which asserts the game itself fixes the outcome of play rather than reporting a mere unlucky run.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `S_Competition` | 7 | 0 |
| `M_UIMisdirection` | 6 | 0 |
| `T_Grinding` | 4 | 2 |
| `T_PlayingByAppointment` | 1 | 3 |
| `M_DeceptiveLuxury` | 4 | 0 |
| `M_IntermediateCurrency` | 4 | 0 |
| `S_Reciprocity` | 4 | 0 |
| `P_RewardMania` | 3 | 0 |
| `M_PayToProgress` | 1 | 2 |
| `M_EasyToPurchase` | 1 | 2 |
| `T_MandatoryMarathon` | 3 | 0 |
| `P_IllusionOfControl` | 0 | 3 |
| `T_Advertisement` | 2 | 1 |
| `P_OptimismAndFrequencyBiases` | 2 | 0 |
| `P_EasyToGetHardToLose` | 2 | 0 |
| `M_Gambling` | 2 | 0 |
| `M_NeverEndingLure` | 2 | 0 |
| `S_FriendSpamImpersonation` | 2 | 0 |
| `P_AestheticManipulation` | 1 | 0 |
| `M_WasteAversion` | 1 | 0 |
| `P_CompleteTheCollection` | 0 | 1 |
| `Tech_FragmentedDownloads` | 1 | 0 |
| `S_ForcedFellowship` | 1 | 0 |
| `T_DailyRewards` | 1 | 0 |
| `T_InfiniteTreadmill` | 1 | 0 |

