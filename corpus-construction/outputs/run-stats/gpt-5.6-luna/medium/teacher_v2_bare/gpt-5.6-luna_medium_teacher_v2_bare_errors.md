# Error review - gpt-5.6-luna_medium_teacher_v2_bare

`gpt-5.6-luna` / reasoning `medium` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_bare.txt` sha `ecd3c1810cf2`  
micro-F1 **0.720** (P 0.844 / R 0.628) - **27 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 7 | said NONE, gold had labels |
| SWAP | 3 | picked different labels than gold |
| MISSED ONLY | 10 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 7 | found all gold, added extras |

## The diagnostic that matters

Of **32** missed labels, **6** (19%) were named in the model's own analysis and dropped anyway; **26** (81%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `P_RewardMania` | 0 | 6 |
| `P_IllusionOfControl` | 1 | 2 |
| `S_Reciprocity` | 1 | 1 |
| `S_Competition` | 0 | 2 |
| `P_AestheticManipulation` | 0 | 2 |
| `M_Gambling` | 1 | 1 |
| `M_PayToProgress` | 1 | 1 |
| `M_EasyToPurchase` | 1 | 1 |
| `M_DeceptiveLuxury` | 0 | 2 |
| `M_IntermediateCurrency` | 1 | 1 |
| `S_FriendSpamImpersonation` | 0 | 1 |
| `T_MandatoryMarathon` | 0 | 1 |
| `T_Grinding` | 0 | 1 |
| `M_WasteAversion` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `S_EncouragesAntiSocialBehavior` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |

## Missed everything (predicted NONE) (7)

### `0853c395-2040-4e0b-a56c-1591484cd35b` - Clash of Clans

> 10/10, but we would like: 1.) Bids & auctions for decorations, skins and sceneries with in-game currency. 2.) Remove the option to remove an obstacle if you've turned it into a decoration. 3.) Widget that can toggle various accounts and see how much time is left for upgrades. 4.) Hidden option for troops' advanced statistics.

| | labels |
|---|---|
| gold | `T_PlayingByAppointment` |
| pred | _NONE_ |
| **missed** | `T_PlayingByAppointment` |

**Did the model consider what it missed?**

- `T_PlayingByAppointment` - never mentioned -> **attention / recall**

**Model analysis**

```
The review consists entirely of requested features rather than complaints describing current manipulative mechanics. It asks for auctions using in-game currency, a change to obstacle-removal behavior, an account-switching widget showing upgrade time, and hidden advanced troop statistics. These suggestions do not explicitly establish a currently present dark-pattern mechanic, and the mention of upgrade time does not by itself show that players are forced to wait or play at scheduled times.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `5f3e71b5-200c-45a3-b90e-e08b0dc0e1a3` - Cash Frenzy™ - Casino Slots

> Is a good game, but I will like to place my formal complain about the genie game, in multiple times whe the wheel spin after stopping on a great price the genie move the wheel to a spin tag, and then the prices after the spin are way lower than the original price, from 100 million with 5x multiplier to a 48 million. Is the only part I don't like. There should be a player choice to keep or spin.

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_RewardMania` |
| pred | _NONE_ |
| **missed** | `P_IllusionOfControl`, `P_RewardMania` |

**Did the model consider what it missed?**

- `P_IllusionOfControl` - considered and rejected -> **rule interpretation**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a chance-based in-game wheel whose favorable result is overridden: after the wheel appears to stop on a high prize, the genie changes the result to a required additional spin, and the replacement prize can be much lower. The player is not given a choice to keep the original result or spin again. This is a forced outcome change and loss of an apparent reward, but the codebook has no label for deceptive rerolls or overridden gambling outcomes. Gambling is not assigned because the review does not explicitly state that real money is used to participate, and Illusion of Control does not fit because the complaint concerns the game's handling of a chance result rather than deception about the player's skill.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b580a4c7-3c75-493e-ad3b-03b4f2bde6a5` - Pokémon GO

> This new update have many bugs. 1)I can't open any gifts or trade with friends without the keep on crashing, 2) when click on a pokemon I can't even throw the pokeball with all the lagging, 3) the pvp & rockets battles are also lagging switching out are too slow, charge attacks are not responding well and my game freeze while the opponent keep attacking. Please fix these problems!

| | labels |
|---|---|
| gold | `S_Competition`, `S_Reciprocity` |
| pred | _NONE_ |
| **missed** | `S_Competition`, `S_Reciprocity` |

**Did the model consider what it missed?**

- `S_Competition` - never mentioned -> **attention / recall**
- `S_Reciprocity` - never mentioned -> **attention / recall**

**Model analysis**

```
The review attributes all described behavior to technical faults in a new update: crashing when opening gifts or trading, lag preventing Poké Ball throws, slow or unresponsive PvP and Team GO Rocket battle controls, and freezing while the opponent continues attacking. These are bugs, lag, or freezes rather than deliberate game design mechanics. Under R11, no dark-pattern label applies.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `490ca53d-66fe-44b0-928f-ea2ba6682f0b` - Clash of Clans

> Since 1 of the updates I can no longer request troops from my clan. It needs to be fixed.

| | labels |
|---|---|
| gold | `S_Reciprocity` |
| pred | _NONE_ |
| **missed** | `S_Reciprocity` |

**Did the model consider what it missed?**

- `S_Reciprocity` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes a bug or technical fault: after an update, they can no longer request troops from their clan. This does not explicitly describe a deliberate social mechanic such as Forced Fellowship, Reciprocity, or Friend Spam / Impersonation, so no label applies under R2 and R11.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `2414fb3d-38e2-4e14-a8af-925f764d2abd` - Match Masters

> Love the game its very addictive and the upgrades are okay but I think you should have a way to trade stickers with players in the game within the app because everybody is not on Facebook. I believe if i purchase a booster i should be able to use it if another player challenge me to a game.

| | labels |
|---|---|
| gold | `S_Competition` |
| pred | _NONE_ |
| **missed** | `S_Competition` |

**Did the model consider what it missed?**

- `S_Competition` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer praises the game and calls it addictive, but those are evaluations rather than mechanics. They suggest adding sticker trading within the app because the current trading route appears to depend on Facebook; this is a requested feature, not an explicitly described dark-pattern mechanic, so it is not coded. They also state that a purchased booster should be usable when another player challenges them, but this does not clearly describe a pay-to-progress rule, gambling, or another listed mechanic. No currently present qualifying mechanic is explicitly described.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `176aaa1f-d8f9-4a1a-9f29-64902f13be5c` - All in Hole: Black Hole Games

> I would give 5 stars, but I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used.🤨😒🙄😥

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `T_MandatoryMarathon` |
| pred | _NONE_ |
| **missed** | `M_IntermediateCurrency`, `T_MandatoryMarathon` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**
- `T_MandatoryMarathon` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes losing stored gameplay resources after exiting and returning: a full bag becomes empty, and both earned and purchased coins have been used. This is a specific progress or data-loss problem, but the review does not describe a deliberate retention, monetization, social, or temporal mechanic. Because the behavior is presented as an unexpected malfunction rather than an intentional game rule, no label applies.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `8d13a3c1-1982-45db-a2b4-07c61c41ba2a` - Pixel Flow!

> this WAS a favorite game and WAS fun until it became unplayable. stuck on level 195 for almost 2 months. getting ready to uninstall it. I refuse to pay for power ups. should be daily login rewards to help with these harder levels.

| | labels |
|---|---|
| gold | `M_PayToProgress` |
| pred | _NONE_ |
| **missed** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_PayToProgress` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes being unable to progress beyond level 195 for almost two months and considering uninstalling. They mention refusing to pay for power-ups, but do not explicitly state that payment is required for progress or that the game imposes a paywall; the refusal alone is insufficient for M_PayToProgress. The requested daily login rewards are a hypothetical feature, not an existing mechanic, so they do not trigger T_DailyRewards. No other codebook mechanic is explicitly supported.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (3)

### `fd1230ab-7d12-4aeb-a425-e37ed06bcd5c` - Pokémon GO

> I love this game, just started playing about 2 months ago. Though I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way. I feel taken advantage of. 3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| pred | `M_Gambling` |
| **missed** | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| **spurious** | `M_Gambling` |

**Did the model consider what it missed?**

- `P_IllusionOfControl` - never mentioned -> **attention / recall**
- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**
- `S_FriendSpamImpersonation` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes purchasing Poké Balls and then using them in capture attempts that repeatedly fail, causing the consumable supply to run out faster and allegedly forcing further purchases. This is a chance-based capture mechanic linked to purchased items, which supports Gambling under the codebook’s broad definition. The later edit disputes authorship and retracts the claim about speaking with other players, but it does not describe a separate in-game mechanic or technical fault. No other label is clearly supported: the text does not establish that payment is required for progress, that purchases use an intermediate currency, or that the interface makes spending unusually easy.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out"
  - why: Purchased Poké Balls are used in capture attempts with an element of chance, where the desired Pokémon may or may not be obtained.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `12267c1e-47ba-4984-97c8-768e820ceb1c` - Bingo Blitz™️ - Bingo Games

> not very user-friendly. no apparent reachable goals within a decent amount of time. I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| pred | `M_PayToProgress`, `P_CompleteTheCollection`, `T_Grinding` |
| **missed** | `M_EasyToPurchase`, `P_AestheticManipulation` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - never mentioned -> **attention / recall**
- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a collection goal involving photos, with the player repeatedly playing bingo rounds to obtain missing items and complete a set. This repeated round-by-round activity is a progression grind. The game also offers a paid shortcut after a lost round: spending extra coins is presented as a way to claim a missing photo and complete the set, so the mechanic is pay-to-progress. The reviewer additionally says the promised photo is not delivered, but this is a failure of the offer rather than a separate codebook mechanic; no label is assigned solely from the complaint about money wasted.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "spend extra coins to claim a photo I don't have to complete the set"
  - why: The game offers spending currency to bypass the normal obstacle of obtaining a missing collection item and advance completion.
- `P_CompleteTheCollection` - ok
  - span: "collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set"
  - why: The game centers progress on obtaining missing photos and completing a set, directly invoking the compulsion to complete an in-game collection.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The player performs repeated bingo rounds in order to make progress toward collecting the photos.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b93c432d-19c0-4c6c-a2d4-bb9b21a436f3` - Dice Dreams™️

> A literal brain-rot game no wonder why they're tryna promote it through Free Cash. Also if you're thinking of making in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates! A real SCAM. Play it if u want but there are games that are actually good also, DON'T GET IN-APP PURCHASES!

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_PayToProgress`, `P_CompleteTheCollection` |
| **missed** | `P_AestheticManipulation`, `P_RewardMania` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes an album-collection system with a grand prize awarded for completing the album, and the reviewer was only two cards short. The reviewer then spent money on an in-app deal intended to provide new cards, which is a purchase aimed at advancing collection progress. The deal instead supplied duplicate cards, but the review does not clearly establish that the cards came from a chance-based gambling mechanic, a deliberately limited-time scarcity system, or a purchase interface designed to reduce deliberation. The mention of promotion through Free Cash concerns third-party advertising and is outside the game-application scope.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "so i bought a deal which promised i would get NEW cards"
  - why: The reviewer spent money on cards specifically to advance toward completing the album.
- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The reviewer is pursuing the remaining cards needed to complete an in-game album and obtain its completion reward.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (10)

### `5e6a5625-5291-4f0e-897c-1b63c1a26494` - MONOPOLY GO!

> I loved this game until the new season started. Suddenly I get no rewards for inviting friends and getting them to join facebook. I am struggling to get dices and when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way... And today. Well, I cannot log in to the game at all. It keeps giving me an internet connection error which is absolute nonsense. I have connected to 3 different wifi connections. BS!!😡

| | labels |
|---|---|
| gold | `M_Gambling`, `P_RewardMania`, `S_ForcedFellowship` |
| pred | `S_ForcedFellowship` |
| **missed** | `M_Gambling`, `P_RewardMania` |

**Did the model consider what it missed?**

- `M_Gambling` - considered and rejected -> **rule interpretation**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes an invitation-based social reward mechanic: the player is expected to invite friends and get them to join Facebook in exchange for rewards. This matches Forced Fellowship's social recruitment indicator even though the reviewer says the rewards have stopped. The difficulty obtaining dice is resource scarcity but does not, by itself, identify a listed pattern. The references to max bet, luck, Shut downs, and bank heists describe chance-based gameplay, but no real-money participation is stated, so M_Gambling is not supported. Duplicate stickers do not explicitly state a compulsion to complete the collection. The inability to log in is attributed to an internet connection error, so it is a technical malfunction and does not trigger a dark-pattern label.
```

**Labels assigned**

- `S_ForcedFellowship` - ok
  - span: "no rewards for inviting friends and getting them to join facebook"
  - why: The span describes an existing social-recruitment mechanic in which inviting friends and bringing them into the game is tied to rewards.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fdef27f2-9a21-4b8e-a04c-7a4753e0fb07` - 8 Ball Pool

> The game is great, but the user interface is completely rigged. Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins and are forced to buy real ones. ​We need a "Default Table Lock" or the game should always open the lowest bet table by default, not the highest! Fix this scammy feature. Giving 1 star

| | labels |
|---|---|
| gold | `M_Gambling`, `M_IntermediateCurrency`, `M_UIMisdirection` |
| pred | `M_UIMisdirection` |
| **missed** | `M_Gambling`, `M_IntermediateCurrency` |

**Did the model consider what it missed?**

- `M_Gambling` - never mentioned -> **attention / recall**
- `M_IntermediateCurrency` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes a default-selection interface behavior: opening the game or entering the 1v1 section automatically scrolls to and selects the highest-bet table available for the player's coin balance. This steers players toward the most expensive wager and creates a risk of unintended high-stakes play. The review also says that losing coins leads players to buy more coins with real money, but it does not clearly state that payment is required for progress, so M_PayToProgress and M_IntermediateCurrency are not assigned. The mention of a 1v1 section identifies player-versus-player competition, but it is contextual rather than a described pressure or manipulation mechanic, so S_Competition is not assigned.
```

**Labels assigned**

- `M_UIMisdirection` - ok
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins"
  - why: The interface automatically directs attention and selection toward the highest-stakes option instead of a neutral or low-bet starting choice.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `549e5e94-9b59-477d-88c7-ae5e00d62514` - Disney Solitaire

> it was fine at the start but further along into the game the rng is so obviously against you it's crazy.. it's not rewarding playing the game without spending actual money.. at around level 100 it costs 2200 but if you win the level you'll barely make that back.. the rewards need a big revamp for me.. let down by alot of things with this game the further into it you get.. sort it out

| | labels |
|---|---|
| gold | `M_PayToProgress`, `P_IllusionOfControl` |
| pred | `M_PayToProgress` |
| **missed** | `P_IllusionOfControl` |

**Did the model consider what it missed?**

- `P_IllusionOfControl` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes increasingly unfavorable random outcomes, saying the RNG is against them, but does not establish that the game hides information about skill or uses chance-based rewards purchased with real money. They also describe a progression economy in which playing without spending actual money is unrewarding and a level costs 2200 while the victory reward barely replenishes that cost. This implies that continued progress or economically viable play is pressured toward real-money spending, supporting Pay to Progress. The near break-even level cost does not by itself establish Waste Aversion because no leftover premium currency or small currency mismatch is described.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "it's not rewarding playing the game without spending actual money"
  - why: The span describes progression-oriented play as effectively requiring or pressuring real-money spending to remain worthwhile.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `3c46f5e0-6091-43dc-94a0-e3af3259a63d` - Cashman Casino Slots Games

> Resently cashman had changed it's bingo rewards and daily rewards. However lve found that I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards. The most I can seem to get on the timed rewards is 40,000. I'd not pay just to get my daily rewards. So I'm deleting them.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_WasteAversion`, `T_DailyRewards` |
| pred | `T_DailyRewards` |
| **missed** | `M_PayToProgress`, `M_WasteAversion` |

**Did the model consider what it missed?**

- `M_PayToProgress` - never mentioned -> **attention / recall**
- `M_WasteAversion` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a daily-reward system that has been changed so the player must first bet 50,000 in order to complete and collect the daily rewards. This is an existing recurring reward task with a condition for claiming it, so it supports Daily Rewards. The review does not establish real-money spending, repetitive grinding, or a specific play time or wait imposed by a timer.
```

**Labels assigned**

- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards."
  - why: The game provides daily rewards and requires the player to complete a daily betting requirement to obtain them.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `cc714d17-863c-4ebd-b14f-989ba17c71c4` - Dice Dreams™️

> I played this game on a different profile. the only reason I gave it five stars is because if you don't it won't let you write a review. if you want to win anything on this game it will cost hundreds of dollars. on the stickers you will never get the last one or two unless you pay a lot of money to get them. this is not a game you want to get addicted to unless you have a endless bank account. it may let you complete a goal maybe one out of hundred times.dont get your hopes up.

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury`, `M_PayToProgress`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_PayToProgress`, `P_CompleteTheCollection` |
| **missed** | `M_DeceptiveLuxury`, `P_RewardMania` |

**Did the model consider what it missed?**

- `M_DeceptiveLuxury` - never mentioned -> **attention / recall**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a monetization gate on obtaining wins and completing sticker collections: the reviewer says winning costs hundreds of dollars and that the final stickers cannot be obtained without paying substantially. The sticker statement also describes a collection-completion objective, with the last one or two items serving as the missing pieces. The claim that goals succeed only rarely expresses frustration and low odds, but it does not clearly describe repetitive tasks, gambling, or an impossible-to-complete game mechanic. The statement about becoming addicted is a warning about engagement, not a specific coded mechanic. No web search is needed because the relevant mechanics are explicit in the review.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "if you want to win anything on this game it will cost hundreds of dollars"
  - why: The reviewer states that achieving wins requires substantial real-money spending, describing payment as necessary for progress or advantage.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: The review describes pursuing the final missing stickers in order to complete a sticker collection.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `ab2097d3-2f9b-4a87-885c-25dfcddb5a70` - Gardenscapes

> Have been playing this game since COVID 19 lockdown. It was fun back then. Currently at 8416 and it gets frustratingly annoying after level 8000. I run out of lives 3-4 times daily to beat every alternate level, avg 5-7 days per level. You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying. Now I'm not interested anymore. Unistalling this game to invest some quality time in a real life. Wasted too much of money and time into this game.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `T_Grinding` |
| pred | `M_PayToProgress` |
| **missed** | `T_Grinding` |

**Did the model consider what it missed?**

- `T_Grinding` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a level-based puzzle game in which progress has become difficult and slow. The clearest mechanic is that the player must purchase add-ons to get through the later levels, making payment a condition of progress. The limited lives are mentioned as a source of repeated failure and delay, but the review does not explicitly describe a wait timer, daily reward, repetitive task requirement, or a session that cannot be stopped. The statements about wasting money and time describe the player's accumulated investment, but do not by themselves establish a design that makes leaving difficult.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through a sane mind."
  - why: The reviewer explicitly states that purchasing add-ons is necessary to make progress through the game.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a2ece36d-c527-442d-8f18-9a16b63994c8` - War Robots Multiplayer Battles

> Its a p2w game. The only time you enjoy it is when you're new. As you progress, everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game. If you want to progress without paying money, goodluck! Even if you wanted to do f2p, you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it. Plus the only time you benofit by getting f2p rewards is ads... 💩

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `M_PayToProgress`, `M_PowerCreep`, `T_Advertisement` |
| pred | `M_PayToProgress`, `M_PowerCreep`, `T_Advertisement` |
| **missed** | `M_EasyToPurchase` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a pay-to-win progression system: the reviewer says progress cannot realistically be made without paying and that the newest bot must be bought rather than earned. The reference to a shifting meta implies that newly introduced bots replace or devalue older options, supporting Power Creep. The game also presents in-game purchase deals every time the player logs in before play, but the review does not clearly describe a purchase-by-default option, accidental purchase risk, insufficient-funds prompt, or attention-directing UI, so M_EasyToPurchase and M_UIMisdirection are not assigned. Finally, free-to-play rewards are obtained through ads, which describes incentivized advertising.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "If you want to progress without paying money, goodluck! Even if you wanted to do f2p, you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it."
  - why: The review states that progression and keeping up with the game require purchasing the newest bot with real money rather than earning it.
- `M_PowerCreep` - ok
  - span: "keep up with shifting meta where you have to buy the newest bot"
  - why: The shifting meta and need to buy the newest bot imply that newer purchased bots diminish the usefulness or competitiveness of existing options over time.
- `T_Advertisement` - ok
  - span: "the only time you benofit by getting f2p rewards is ads"
  - why: The reviewer describes free-to-play rewards as being obtained through viewing or engaging with advertisements.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `84bbc363-d55a-4cf1-a557-c61ed7ab82bc` - Last War:Survival Game

> Once you get past building the city block stage, it gets kinda boring. It's just grinding resources trying not to get raided so you can level up to have a few more attempts at the left right scroller game. The advertisement that's really becomes not that great. The bigger alliances all just attack the smaller alliances and take their resources. I dedicated some time to this game and to my alliances and am disappointed with current status.

| | labels |
|---|---|
| gold | `S_Competition`, `S_EncouragesAntiSocialBehavior`, `T_Grinding` |
| pred | `S_Competition`, `T_Grinding` |
| **missed** | `S_EncouragesAntiSocialBehavior` |

**Did the model consider what it missed?**

- `S_EncouragesAntiSocialBehavior` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes repetitive resource collection as the main route to leveling up, which directly supports Grinding. It also describes alliances attacking one another and taking resources, so the game places players or alliances in direct competition. The reviewer mentions spending time on the game and alliances, but does not say that this investment makes quitting difficult, nor that alliance participation creates an obligation to keep playing. The reference to an advertisement is unclear and appears to concern marketing rather than an in-game mechanic, so it is outside scope and does not support Advertisement.
```

**Labels assigned**

- `S_Competition` - ok
  - span: "The bigger alliances all just attack the smaller alliances and take their resources."
  - why: The game makes alliances compete directly by attacking one another and taking resources.
- `T_Grinding` - ok
  - span: "It's just grinding resources trying not to get raided so you can level up"
  - why: The reviewer explicitly describes repetitive resource collection as the activity required for progress and leveling up.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `73423b22-395c-49ed-8fc3-488a0b7680df` - MONOPOLY GO!

> I like the game but frustrating when it comes to getting stickers. always get duplicates. never lets you finish all the sets unless you pay

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury`, `M_PayToProgress`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_PayToProgress`, `P_CompleteTheCollection` |
| **missed** | `M_DeceptiveLuxury`, `P_RewardMania` |

**Did the model consider what it missed?**

- `M_DeceptiveLuxury` - never mentioned -> **attention / recall**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a sticker-collection mechanic in which obtaining stickers often produces duplicates, while completing all sets is gated behind payment. The sets are collection goals, so the review supports Complete the Collection. It also explicitly says finishing them requires payment, supporting Pay to Progress. The duplicate outcome alone does not establish gambling or a random-reward mechanic strongly enough to add another label.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: The review explicitly states that completing the sets is unavailable unless the player pays.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: The reviewer describes trying to complete all sticker sets, which is a compulsion or goal to acquire a complete in-game collection.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `727cc804-9d4b-48ef-8774-2799a2a8de08` - Genshin Impact

> with every incoming patch, we get less and less rewards and for me that wouldn't be a problem but the Meta changes more and more every single day basically forcing us to pull for new characters if we want to actually do damage. the game is getting more and more pay 2 win and the quality of the game is becoming lower. in the new archon quest when we were talking to mavuika, a multi billion dollar company just put an insanely bad picture of Natlans scenery as the background, y'all can do better.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_PowerCreep`, `P_RewardMania` |
| pred | `M_PayToProgress`, `M_PowerCreep` |
| **missed** | `P_RewardMania` |

**Did the model consider what it missed?**

- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a recurring balance change in which each patch makes existing characters less sufficient for the current meta, while newer characters become necessary to deal meaningful damage. This is power creep because the value or effectiveness of prior character investments declines and the player is pushed toward acquiring newer characters. The review also explicitly connects acquiring those new characters with the game becoming pay-to-win, describing payment-linked acquisition of combat advantages. The reduced rewards and lower visual quality are complaints about rewards and presentation, not mechanics covered by the codebook.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "basically forcing us to pull for new characters if we want to actually do damage. the game is getting more and more pay 2 win"
  - why: The review links acquiring new characters with obtaining the combat advantage needed to deal damage and explicitly characterizes the system as increasingly pay-to-win.
- `M_PowerCreep` - ok
  - span: "the Meta changes more and more every single day basically forcing us to pull for new characters if we want to actually do damage"
  - why: Ongoing meta changes make existing characters less effective and push players to acquire new characters for comparable combat performance.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (7)

### `66698c5c-8577-46fe-b796-8e93ad782166` - Teen Patti GOLD: 3 Patti Rummy

> Finally you forced me to uninstall the game. Forced notifications to give you permission to my contact list, for what? Is this a game or data collecting app?why I am bound to give you that permission? Better to keep you as spam app.

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `S_FriendSpamImpersonation` |
| **spurious** | `S_FriendSpamImpersonation` |

**Model analysis**

```
The reviewer describes the game using forced notifications to request permission to access the player's contact list. This explicitly describes the game seeking access to the player's social graph, which supports Friend Spam / Impersonation even though the review does not state that messages were actually sent to contacts. The statements about uninstalling and calling it a spam app are evaluations, not separate mechanics.
```

**Labels assigned**

- `S_FriendSpamImpersonation` - **SPURIOUS**
  - span: "Forced notifications to give you permission to my contact list"
  - why: The game is described as using notifications to obtain permission to access the player's contact list, which is access to the player's social graph.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `21021f9a-e106-4e51-b01d-3fe4a4c941fc` - MONOPOLY GO!

> Deleted the game now. The latest event I was about to get 525 dice as reward, I had 3 left to go and I ran out of dice, it said 2Days left. Now just logged in after sleeping and the event is now changed. Deleting this game and what an absolute waste of time. Never purchased anything coz i have trust issues with F2P model games, and my gutt was right all along. Fun when it lasted, but that was a low blow.

| | labels |
|---|---|
| gold | `T_PlayingByAppointment` |
| pred | `S_FearOfMissingOutFOMO`, `T_PlayingByAppointment` |
| **spurious** | `S_FearOfMissingOutFOMO` |

**Model analysis**

```
The reviewer describes a time-limited event with a reward nearly reached: they had only three steps remaining toward 525 dice but could not continue after running out of dice. The event displayed two days remaining, yet after the reviewer stopped to sleep and logged back in, the event had changed. This makes the game’s event schedule determine when the player must participate and creates pressure that stopping will cause a missed reward. The review does not explicitly describe purchasing dice, watching ads, daily rewards, or repetitive grinding, so those are not coded.
```

**Labels assigned**

- `S_FearOfMissingOutFOMO` - **SPURIOUS**
  - span: "I was about to get 525 dice as reward, I had 3 left to go and I ran out of dice"
  - why: The nearly completed reward and lack of dice create pressure to keep playing so the player does not miss the event reward.
- `T_PlayingByAppointment` - ok
  - span: "it said 2Days left. Now just logged in after sleeping and the event is now changed"
  - why: The event schedule determines the available play window, and the event changed while the player was away despite showing two days remaining.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `33c422de-1a84-4df9-accd-cdf8bfc96295` - Dark War Survival

> No ingenuity for a base builder. Same old same old grinder. After a few weeks, it became abundantly clear that there is absolutely no opportunity for a general player to win an event. Zero skill pay to play. Zero skill pay to win. Calculated total spent on last event was 30k to win. Wish serious gamers would stop perpetuating the problem by continuing to spend obnoxious amounts of money on a little app that you just want to have a little fun on.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `S_Competition` |
| pred | `M_PayToProgress`, `S_Competition`, `T_Grinding` |
| **spurious** | `T_Grinding` |

**Model analysis**

```
The review describes a base-building game requiring repetitive progression, explicitly called a grinder. It also describes competitive events where winning is effectively unavailable to ordinary players unless they spend very large amounts of money, including a reported 30k expenditure to win the last event. The event language and pay-to-win claim describe competition between players, while the money-for-advantage mechanic supports Pay to Progress. The spending amount alone is not a separate label, and the review does not describe a specific purchase interface, currency, gambling, or recurring fee.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Zero skill pay to win"
  - why: The span explicitly describes spending money as the route to gaining an advantage and winning.
- `S_Competition` - ok
  - span: "no opportunity for a general player to win an event"
  - why: The review describes players competing in events for a win.
- `T_Grinding` - **SPURIOUS**
  - span: "Same old same old grinder"
  - why: Calling the game a grinder describes repetitive and tedious gameplay used for progression.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b2dc0bc8-8ebe-4c48-bc05-38d0d65acb84` - Last War:Survival Game

> It's a nice game, but it's set up in a pay to win way. I played for 10 days, and the update times for your base are becoming ridiculous. Everything scales endlessly, there is kinda no point to look forward to, just more grind. The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff. Alliances are also weird, with the top ones dictating what to develop, what to rush, etc. If you are not in one then you get attacked and bullied. Not a great experience.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_UIMisdirection`, `S_Competition`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| pred | `M_PayToProgress`, `M_UIMisdirection`, `S_Competition`, `T_Grinding`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| **spurious** | `T_Grinding` |

**Model analysis**

```
The review describes several current game mechanics. It explicitly identifies a pay-to-win structure, meaning spending money provides gameplay advantages. Base upgrades use increasingly long update timers, imposing waits before progress can continue. Progress also expands endlessly and requires ongoing repetitive grinding, which supports both Infinite Treadmill and Grinding. The UI is described as intentionally confusing and overwhelming in order to push purchases; this is purposeful UI direction away from clear choices and toward buying. The alliance system creates multiplayer conflict and pressure: dominant alliances dictate development choices, while unaffiliated players are attacked and bullied. This supports Competition, but not Forced Fellowship because the review does not describe recruiting friends or an obligation to avoid letting down allies.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "it's set up in a pay to win way"
  - why: The review explicitly describes a design where paying players receive gameplay advantages.
- `M_UIMisdirection` - ok
  - span: "The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff"
  - why: The UI is intentionally made confusing and overwhelming to steer players toward purchasing.
- `S_Competition` - ok
  - span: "If you are not in one then you get attacked and bullied"
  - why: The alliance system places players in hostile conflict with other players, including attacks against those outside alliances.
- `T_Grinding` - **SPURIOUS**
  - span: "just more grind"
  - why: The reviewer explicitly characterizes continued progress as requiring more grind.
- `T_InfiniteTreadmill` - ok
  - span: "Everything scales endlessly"
  - why: Endless scaling implies that progression continually extends rather than reaching a meaningful completion point.
- `T_PlayingByAppointment` - ok
  - span: "the update times for your base are becoming ridiculous"
  - why: Base progress is delayed by increasingly long game-imposed update timers.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `32c623b4-0249-469e-968c-94f60c7fe3c2` - Royal Match

> It's an interesting game but the developers should pls try to include new cards in every card pack because I noticed when one is almost close to completing a set, new cards don't appear again especially when the set is almost expiring. So after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion because they don't add new sets to the cards once the collection is about to end.

| | labels |
|---|---|
| gold | `P_CompleteTheCollection`, `T_PlayingByAppointment` |
| pred | `P_CompleteTheCollection`, `S_FearOfMissingOutFOMO`, `T_PlayingByAppointment` |
| **spurious** | `S_FearOfMissingOutFOMO` |

**Model analysis**

```
The review describes a time-limited card-collection set. Card packs stop providing new cards when the player is close to completing the set, especially near the set's expiration, so the player can fail to obtain the completion reward despite having collected 125 cards. This directly creates pressure to complete the collection before the game-defined deadline and fear of missing the reward. The review does not clearly describe repetitive tasks, paid currency, gambling, or a purchase-related scarcity tactic.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion"
  - why: The mechanic centers on acquiring all cards in a set to obtain a completion reward.
- `S_FearOfMissingOutFOMO` - **SPURIOUS**
  - span: "especially when the set is almost expiring"
  - why: The expiring set creates a risk of missing the completion reward.
- `T_PlayingByAppointment` - ok
  - span: "when the set is almost expiring"
  - why: The set's expiration imposes a game-defined time window in which players must continue pursuing cards.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `45e3e2f0-4612-4d60-9312-3bff055ec9f3` - Merge Cooking®

> I really enjoyed this game until I got to a higher level. About to quit at level 34. Not enough slots to store and play without spending $$ to buy parts. I have 63 spots, on the board and 37 spots in the refrigerator. 98 spaces total, 72 are taken up by parts of generators or lower generators that I can't merge with higher generators yet or high level items like a corn that I am not going to delete. A lambchop can take up to 9 spaces or more of my 26 spaces and I'm not deleting the chicken pie

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_WasteAversion` |
| pred | `M_PayToProgress`, `M_WasteAversion`, `P_EasyToGetHardToLose` |
| **spurious** | `P_EasyToGetHardToLose` |

**Model analysis**

```
The reviewer describes a capped inventory system that limits available board and refrigerator storage. Many spaces are occupied by generator parts, lower-level generators that cannot yet be merged, and high-level food items the player refuses to delete. This storage pressure makes continued play depend on spending money to buy parts, so payment is presented as necessary to keep playing. The reluctance to delete valuable accumulated items also makes abandoning or discarding progress costly. No grinding, daily schedule, competition, advertising, or gambling mechanic is described.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Not enough slots to store and play without spending $$ to buy parts."
  - why: The review states that continued play is not possible without spending money to obtain parts, making payment a requirement for progress or continued gameplay.
- `M_WasteAversion` - ok
  - span: "98 spaces total, 72 are taken up by parts of generators or lower generators that I can't merge with higher generators yet"
  - why: The game imposes a limited storage capacity that becomes occupied by unusable or not-yet-mergeable items, creating pressure to discard items or spend to overcome the capacity constraint.
- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "high level items like a corn that I am not going to delete"
  - why: The player’s accumulated high-level items are treated as valuable investments that they are unwilling to discard, making departure or abandoning progress more difficult.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `7b564746-b769-4856-b686-529f8717c3ba` - Candy Crush Soda Saga

> I like the game except: 1. I was charged 10 gold pcs for 5 moves, I had 2 moves left. I had 7 moves but only used 1 move. 2. I paid for a pkg unlimited lives ect. I got the etc. but not the lives. 3. The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone. 4. You cannot win enough gold to play without buying sometimes. 5. The packages need to cost less. 6. When I buy pkg should not be timed.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `M_PayToProgress`, `T_PlayingByAppointment` |
| pred | `M_EasyToPurchase`, `M_IntermediateCurrency`, `M_PayToProgress`, `T_PlayingByAppointment` |
| **spurious** | `M_EasyToPurchase` |

**Model analysis**

```
The review describes several current game mechanics. The game can charge gold for a package of extra moves, apparently resulting in an unintended or insufficiently deliberate purchase, which supports Easy to Purchase. Timed bonuses continue expiring while the player is away, and purchased packages are also timed; these mechanics make the player conform to the game's timer and support Playing by Appointment. The reviewer also states that normal play does not provide enough gold to continue playing without buying, making payment a route to progress and indicating that real money is exchanged for an intermediate in-game currency. The missing lives from a purchased package is described as a failure to deliver what was bought, so it is treated as a technical or fulfillment problem rather than a dark pattern. The requests for cheaper packages and untimed purchases do not describe additional mechanics.
```

**Labels assigned**

- `M_EasyToPurchase` - **SPURIOUS**
  - span: "I was charged 10 gold pcs for 5 moves"
  - why: The wording 'I was charged' describes an unintended charge for an in-game purchase, indicating low-friction or insufficiently deliberate purchasing.
- `M_IntermediateCurrency` - ok
  - span: "win enough gold to play without buying"
  - why: Gold is an in-game currency that the player can acquire by buying it with real money and then use for gameplay.
- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The review states that continuing to play sometimes requires buying rather than earning enough gold through gameplay.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing."
  - why: Bonuses expire according to an in-game timer even while the player is absent, pressuring the player to return and play within the game's scheduled time window.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `P_RewardMania` | 6 | 0 |
| `M_PayToProgress` | 2 | 2 |
| `P_IllusionOfControl` | 3 | 0 |
| `M_Gambling` | 2 | 1 |
| `M_EasyToPurchase` | 2 | 1 |
| `T_Grinding` | 1 | 2 |
| `S_Reciprocity` | 2 | 0 |
| `S_FriendSpamImpersonation` | 1 | 1 |
| `S_Competition` | 2 | 0 |
| `P_AestheticManipulation` | 2 | 0 |
| `S_FearOfMissingOutFOMO` | 0 | 2 |
| `M_DeceptiveLuxury` | 2 | 0 |
| `M_IntermediateCurrency` | 2 | 0 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `T_MandatoryMarathon` | 1 | 0 |
| `M_WasteAversion` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `S_EncouragesAntiSocialBehavior` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |

