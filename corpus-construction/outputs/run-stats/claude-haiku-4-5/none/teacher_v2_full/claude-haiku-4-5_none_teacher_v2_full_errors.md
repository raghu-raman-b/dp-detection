# Error review - claude-haiku-4-5_none_teacher_v2_full

`claude-haiku-4-5` / reasoning `none` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `6529a474a2b0`  
micro-F1 **0.767** (P 0.836 / R 0.709) - **25 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 6 | said NONE, gold had labels |
| SWAP | 7 | picked different labels than gold |
| MISSED ONLY | 8 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 4 | found all gold, added extras |

## The diagnostic that matters

Of **25** missed labels, **2** (8%) were named in the model's own analysis and dropped anyway; **23** (92%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `S_Competition` | 1 | 5 |
| `M_IntermediateCurrency` | 0 | 4 |
| `P_RewardMania` | 0 | 2 |
| `P_AestheticManipulation` | 0 | 2 |
| `S_Reciprocity` | 0 | 2 |
| `T_Grinding` | 1 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `M_RecurringFee` | 0 | 1 |
| `T_MandatoryMarathon` | 0 | 1 |
| `M_Gambling` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `S_ForcedFellowship` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |

## Missed everything (predicted NONE) (6)

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
This review gives a positive rating and then lists four feature requests: auctions with in-game currency for decorations/skins, removal of an obstacle-removal option, a widget for multi-account management, and hidden troop statistics. All four items are framed as suggestions ('we would like'). Per R12, requests and suggestions for non-existent features do not trigger labels; only mechanics currently present in the game and explicitly described are codable. The review does not describe any currently active game behavior or dark pattern.
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
The reviewer describes a series of technical malfunctions: crashes when opening gifts or trading, lag when throwing pokeballs, lag in PVP and rocket battles, slow switching, unresponsive charge attacks, and freezing. All issues are attributed to bugs ('This new update have many bugs'), crashes, lag, and freezing. The entire review is a complaint about technical faults and a request to fix them. R11 states that dark patterns are deliberate design choices, not technical malfunctions. The codebook requires that a label be assigned only when the review describes a game mechanic or design behaviour (R2), not technical faults. Nothing in this review describes a deliberate design pattern.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `ae51c2f5-a77c-428d-bb71-ee00109538ba` - Lords Mobile: Kingdom Wars

> Lords Mobile: Pagani Go is an immersive and exhilarating gaming experience that combines strategy, adventure, and excitement. As a fan of the Lords Mobile franchise, I was thrilled to dive into this new iteration and was not disappointed. The game's stunning graphics, intricate gameplay mechanics, and captivating storyline kept me hooked from the start. I appreciate the depth of strategy required to build and expand my empire, as well as the thrill of battling other players in real-time combat.

| | labels |
|---|---|
| gold | `S_Competition` |
| pred | _NONE_ |
| **missed** | `S_Competition` |

**Did the model consider what it missed?**

- `S_Competition` - considered and rejected -> **rule interpretation**

**Model analysis**

```
This is a positive review of Lords Mobile: Kingdom Wars praising the graphics, gameplay mechanics, storyline, strategic depth, and real-time PvP combat. The reviewer expresses enjoyment and satisfaction throughout. The review contains no descriptions of game design mechanics that constitute dark patterns, no mention of monetization or payment mechanics, no time-gating or waiting systems, no grinding described as forced, no social pressure or exploitation, and no manipulation or deceptive design. The mention of battling other players simply describes the existence of competitive gameplay that the reviewer enjoys, not a dark pattern that exploits or manipulates players through competition.
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

- `S_Reciprocity` - never mentioned -> **attention / recall**

**Model analysis**

```
The review reports that following a game update, the reviewer can no longer request troops from their clan. This describes a technical malfunction introduced by an update that broke a previously functioning feature, not a game design mechanic or dark pattern. While troop requests may ordinarily involve reciprocal cooperation between players when the system works, the review explicitly attributes the current unavailability to a bug that needs fixing. R11 directs that labels not be assigned when behavior is attributed to a bug, glitch, or technical fault.
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
The reviewer expresses enjoyment of the game and describes it as addictive. However, the review primarily consists of positive statements and feature requests rather than descriptions of problematic game mechanics. The mention of upgrades is neutral ('are okay'). The reviewer suggests two features they wish existed: (1) sticker trading within the app rather than requiring Facebook, and (2) the ability to use purchased boosters when challenged by other players. Both of these are requests for changes to the game, not descriptions of current mechanics operating as dark patterns. Per R12, suggestions and hypothetical additions do not trigger labels for the proposed mechanics. The mention that the game is 'very addictive' is an evaluation of appeal, not a description of a specific game mechanic (such as variable rewards, grinding, or endowed value) that would justify a psychological dark pattern label under R2.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fdfb3f26-0573-4cac-a0e2-ea5571bb5ad2` - Evony: The King's Return

> The ads for this game capitalize on the puzzles as if the whole game is about solving the physics puzzles. The reality is that this is an extremely involved strategy game that has, once in a while, a puzzle like those shown in the ads. If you like making an army from scratch, training, building, gathering resources then you may like this game. If you expected puzzles such as those in the ads for this game, you'll be doing chores in order to get to them.

| | labels |
|---|---|
| gold | `T_Grinding` |
| pred | _NONE_ |
| **missed** | `T_Grinding` |

**Did the model consider what it missed?**

- `T_Grinding` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a mismatch between game advertising and actual gameplay. The ads prominently feature physics puzzles, but the game is primarily a strategy game involving army building, training, building structures, and resource gathering, with puzzles appearing only occasionally. The reviewer characterizes the non-puzzle activities as 'chores' that must be completed to access the occasional puzzle content. However, the complaint centers on misleading external advertising (third-party ads, store listing), which falls outside the scope of in-game mechanics per R13. The in-game mechanics themselves—army building, training, building, resource gathering—are standard strategy game activities and are not characterized with sufficient specificity as repetitive or tedious tasks to trigger Grinding. The term 'chores' is evaluative characterization rather than a description of a specific game mechanic pattern from the codebook.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (7)

### `5f3e71b5-200c-45a3-b90e-e08b0dc0e1a3` - Cash Frenzy™ - Casino Slots

> Is a good game, but I will like to place my formal complain about the genie game, in multiple times whe the wheel spin after stopping on a great price the genie move the wheel to a spin tag, and then the prices after the spin are way lower than the original price, from 100 million with 5x multiplier to a 48 million. Is the only part I don't like. There should be a player choice to keep or spin.

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_RewardMania` |
| pred | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases` |
| **missed** | `P_RewardMania` |
| **spurious** | `P_OptimismAndFrequencyBiases` |

**Did the model consider what it missed?**

- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a specific game mechanic in the 'genie game' where the wheel stops on a high reward value (e.g., 100 million with 5x multiplier), but then an automatic action by 'the genie' moves the wheel again, resulting in a significantly lower reward (48 million). The reviewer states this happens 'in multiple times,' indicating it's a recurring pattern. The core complaint is outcome manipulation: the wheel displays a desirable result, but the game automatically changes it without player agency. This creates two related dark patterns: (1) the game is actively manipulating outcomes shown to the player (Illusion of Control), and (2) the repeated pattern of almost-winning a high value before it's automatically reduced to a much lower value creates engineered near-misses that exploit frequency bias (Optimism and Frequency Biases). The boundary rule for these patterns explicitly permits assigning both when the span carries both the manipulation claim and the frequency perception.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "the genie move the wheel to a spin tag, and then the prices after the spin are way lower than the original price"
  - why: The game deceives the player by displaying one outcome on the wheel, then automatically manipulating that outcome to a substantially lower value without player input, concealing the true outcome determination process.
- `P_OptimismAndFrequencyBiases` - **SPURIOUS**
  - span: "in multiple times whe the wheel spin after stopping on a great price the genie move the wheel to a spin tag, and then the prices after the spin are way lower than the original price, from 100 million with 5x multiplier to a 48 million"
  - why: The span describes repeated engineered near-misses (multiple times almost winning 100 million before automatic reduction to 48 million), exploiting frequency bias to create the perception that wins are nearly achieved, encouraging continued play.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b2dc0bc8-8ebe-4c48-bc05-38d0d65acb84` - Last War:Survival Game

> It's a nice game, but it's set up in a pay to win way. I played for 10 days, and the update times for your base are becoming ridiculous. Everything scales endlessly, there is kinda no point to look forward to, just more grind. The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff. Alliances are also weird, with the top ones dictating what to develop, what to rush, etc. If you are not in one then you get attacked and bullied. Not a great experience.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_UIMisdirection`, `S_Competition`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| pred | `M_PayToProgress`, `M_UIMisdirection`, `T_Grinding`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| **missed** | `S_Competition` |
| **spurious** | `T_Grinding` |

**Did the model consider what it missed?**

- `S_Competition` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes several interconnected design patterns in a war/strategy game. First, they state the game is 'set up in a pay to win way,' indicating payment is required for progression. Second, they describe 'update times for your base are becoming ridiculous'—these are cooldown/build timers that grow increasingly long, forcing the player to wait in accordance with the game's schedule. Third, they characterize the progression as 'everything scales endlessly' with 'no point to look forward to,' describing an end-to-end treadmill with no completion state and no victory condition. This endless scaling drives 'just more grind'—repetitive building/upgrading tasks that the player must cycle through. Finally, they explicitly state 'The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff,' naming a UI design intended to confuse and push purchases. The alliance section describes social mechanics but does not trigger a dark pattern label per the codebook: the reviewer is describing being attacked if unaffiliated, which is a consequence of the social structure rather than an incentive structure rewarding the attackers' behavior.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "it's set up in a pay to win way"
  - why: The reviewer directly states the game requires payment to progress or win, matching the core definition of Pay to Progress.
- `M_UIMisdirection` - ok
  - span: "The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff"
  - why: The reviewer explicitly states the UI is designed to be confusing and overwhelming with the purpose of driving purchases. This directly describes UI misdirection designed to push spending.
- `T_Grinding` - **SPURIOUS**
  - span: "Everything scales endlessly, there is kinda no point to look forward to, just more grind"
  - why: The endless scaling creates a cycle of repetitive building/upgrading tasks the player must perform to progress. The span identifies both the repeated activity (scaling) and the grind mechanic it produces.
- `T_InfiniteTreadmill` - ok
  - span: "Everything scales endlessly, there is kinda no point to look forward to"
  - why: The reviewer describes endless scaling with no attainable end state or completion goal, meaning the game extends beyond the player's ability to finish.
- `T_PlayingByAppointment` - ok
  - span: "the update times for your base are becoming ridiculous"
  - why: The span describes build/upgrade timers (update times) that impose arbitrary wait periods on the player, forcing them to play according to the game's schedule.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a5bfa159-1783-40a8-8852-ce39d7962398` - Homescapes

> They advertise many, many pin pull levels and games, but they are so few and far between, it's like false advertising. I'm over level 4000, so it's not like I haven't given it time. The "mini" games are foolish and also rare. I have also paid a lot for extra coins and things to see if pin pulls would happen, and they don't. Also, nearly everytime I do the required update, it takes days before it connects correctly again. I've tried on Gardenscapes too, same thing, false pin pulling advertising.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency` |
| pred | `M_DeceptiveLuxury` |
| **missed** | `M_IntermediateCurrency` |
| **spurious** | `M_DeceptiveLuxury` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer is describing game marketing versus actual gameplay delivery in Homescapes. The game advertises 'many, many pin pull levels and games' through its marketing materials, but in actual gameplay at level 4000+, these features are 'so few and far between.' This is characterized as 'false advertising.' The reviewer paid 'a lot for extra coins' attempting to trigger or unlock pin pull levels, but 'they don't' appear—meaning payment did not enable access to these advertised features. Additionally, mini games are 'foolish and also rare,' and update connection issues are described. The false advertising claim itself (how the game is marketed externally) falls outside scope per R13. However, the core in-game behavior is clear: pin pull levels are made artificially scarce despite being heavily advertised as a feature. The reviewer's attempt to purchase their way to these levels suggests they are gated but not reliably purchasable, and the fundamental issue is scarcity of advertised content. This could represent Deceptive Luxury (manufactured scarcity of advertised content) or potentially Reward Mania (unpredictable, rare delivery of a featured mechanic). The update connection problems are technical malfunctions and do not trigger patterns per R11.
```

**Labels assigned**

- `M_DeceptiveLuxury` - **SPURIOUS**
  - span: "They advertise many, many pin pull levels and games, but they are so few and far between"
  - why: The game advertises pin pull levels heavily but makes them artificially scarce in actual gameplay, fitting the definition of manufactured scarcity of an advertised feature.

**Search:** `Homescapes pin pull levels what are` -> Search confirmed that 'Pull the Pin' is a puzzle mini-game mechanic featured in Homescapes, establishing that pin pulls are a named, intended game feature being advertised.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `176aaa1f-d8f9-4a1a-9f29-64902f13be5c` - All in Hole: Black Hole Games

> I would give 5 stars, but I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used.🤨😒🙄😥

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `T_MandatoryMarathon` |
| pred | `P_EasyToGetHardToLose` |
| **missed** | `M_IntermediateCurrency`, `T_MandatoryMarathon` |
| **spurious** | `P_EasyToGetHardToLose` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**
- `T_MandatoryMarathon` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes leaving the game with accumulated resources (bag full of items and coins earned through gameplay and purchased with real money), then returning to find those resources gone/used. In All in Hole, coins are spent during levels to continue playing when you run out of lives. The review indicates that the game consumes these resources when the player returns, meaning stopping play results in loss of accumulated holdings—both earned currency and paid currency. This prevents the player from exiting without forfeiting value they already hold, which is the mechanism of Easy to Get, Hard to Lose.
```

**Labels assigned**

- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used"
  - why: The player accumulates items and coins (both earned and purchased with real money), but cannot preserve them when exiting—returning finds them consumed. The cost of stopping is measured in what they already own, raising the cost of disengagement.

**Search:** `All in Hole Black Hole Games bag coins mechanics` -> Game is a puzzle game where players collect items, swap colors, and spend coins during levels to continue when out of lives. Team members share hearts and coins.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `12267c1e-47ba-4984-97c8-768e820ceb1c` - Bingo Blitz™️ - Bingo Games

> not very user-friendly. no apparent reachable goals within a decent amount of time. I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| pred | `M_EasyToPurchase`, `P_CompleteTheCollection`, `P_RewardMania` |
| **missed** | `P_AestheticManipulation`, `T_Grinding` |
| **spurious** | `P_RewardMania` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**
- `T_Grinding` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a collection mechanics where the goal is to accumulate 'photos' and complete sets. When they lose a round, the game prompts them with an offer to spend coins on a specific photo they don't have to complete their set. They accept the offer, spend coins (in-game currency purchased with real money, implied by 'I've wasted so much money'), then play and win (getting bingos), but the promised photo does not appear. This happens repeatedly ('so many times I can't even count'). The core complaint is that payment is followed by unmet promises about reward delivery—they are promised a specific photo, they pay, they meet apparent win conditions (bingos), but the reward is not delivered. This indicates three distinct patterns: (1) a collection goal driving repeated play and purchases; (2) purchase prompts triggered by game states (losing); (3) unpredictable or variable reward delivery despite payment. The unmet promise and repeated failure to deliver the incentivized reward is not described as a bug but as systematic behavior.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "after each round that I lose it will ask me if I want to spend extra coins"
  - why: The game intercepts the moment of failure (losing a round) to present a purchase offer, reducing the friction and deliberation cost of spending. This is a friction-reducing mechanism built into the interface.
- `P_CompleteTheCollection` - ok  _[span not verbatim]_
  - span: "I play round after round to collect 'photos'... to complete the set"
  - why: The player's engagement is centered on accumulating photos to complete collections, a core pattern for the collection compulsion.
- `P_RewardMania` - **SPURIOUS**
  - span: "I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED"
  - why: The promised reward delivery is uncertain: payment + winning is not a deterministic path to the specific photo. The unpredictability persists despite repeated attempts ('so many times'), sustaining repeated engagement and spending through variable reinforcement.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `7b564746-b769-4856-b686-529f8717c3ba` - Candy Crush Soda Saga

> I like the game except: 1. I was charged 10 gold pcs for 5 moves, I had 2 moves left. I had 7 moves but only used 1 move. 2. I paid for a pkg unlimited lives ect. I got the etc. but not the lives. 3. The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone. 4. You cannot win enough gold to play without buying sometimes. 5. The packages need to cost less. 6. When I buy pkg should not be timed.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `M_PayToProgress`, `T_PlayingByAppointment` |
| pred | `M_PayToProgress`, `M_WasteAversion`, `T_PlayingByAppointment` |
| **missed** | `M_IntermediateCurrency` |
| **spurious** | `M_WasteAversion` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes several monetization and timing mechanics in Candy Crush. (1) They purchased a 5-move pack for 10 gold but only needed 1 move, resulting in 4 unused moves—a classic pack size misalignment where the minimum purchase exceeds the requirement. (2) A package purchase claimed unlimited lives but the lives were not delivered; this is a delivery failure rather than a dark pattern mechanic per se. (3) Time-limited bonuses (buffs or multipliers) expire in real time even when the player is not playing—the game operates on its own clock, forcing players to play before these rewards vanish. (4) Free currency generation is insufficient for continued play without payment. (5-6) Package pricing is high and packages themselves are time-limited, both complaints about friction in monetization. The core mechanics are: pack sizing creates waste, real-time timers gate rewards, and payment is required for progress.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The free currency earned through play is insufficient for continuous progression, forcing payment as an alternative route. This establishes payment as necessary for advancement.
- `M_WasteAversion` - **SPURIOUS**
  - span: "I was charged 10 gold pcs for 5 moves, I had 2 moves left. I had 7 moves but only used 1 move."
  - why: The player purchased a 5-move pack but only needed 1 additional move, leaving 4 moves unused. This demonstrates pack-sized purchases creating leftover value the player cannot use, the core mechanism of Waste Aversion.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone."
  - why: The game imposes real-world time limits on bonuses that decay whether or not the player is playing. The player must engage with the game before the bonuses expire or forfeit them, creating a schedule the game defines rather than the player.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b93c432d-19c0-4c6c-a2d4-bb9b21a436f3` - Dice Dreams™️

> A literal brain-rot game no wonder why they're tryna promote it through Free Cash. Also if you're thinking of making in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates! A real SCAM. Play it if u want but there are games that are actually good also, DON'T GET IN-APP PURCHASES!

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_Gambling`, `P_CompleteTheCollection`, `P_RewardMania` |
| **missed** | `P_AestheticManipulation` |
| **spurious** | `M_Gambling` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a collection game (Dice Dreams) where the player was 2 cards away from completing an album to earn a grand prize. They made an in-app purchase of a 'deal' that promised 'NEW cards' to complete the album. Instead of new cards, they received 'useless duplicates' from a randomized draw. The reviewer frames this as a scam, warning against making in-app purchases. The mechanics being described are: (1) a collection completion system gated toward payment, (2) a paid randomized card draw, and (3) unpredictable reward outcomes (expected new cards, received duplicates). The paid purchase with randomized results that delivered unwanted cards rather than promised ones is central to the complaint.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "bought a deal which promised i would get NEW cards, and all i got were useless duplicates"
  - why: The player spent real money (in-app purchase) on a randomized card draw with an unpredictable outcome, receiving duplicates instead of the promised new cards.
- `P_CompleteTheCollection` - ok
  - span: "had two cards left which would grant me the grand prize for completing an album"
  - why: The player is working toward completing a collection (album) to obtain a grand prize reward, demonstrating the collection completion mechanic.
- `P_RewardMania` - ok
  - span: "all i got were useless duplicates"
  - why: The paid card draw delivered unpredictable, unwanted outcomes (duplicates instead of promised new cards), showing the variable/randomized reward delivery mechanism that characterizes gacha mechanics.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (8)

### `0bc09fc3-6436-4a24-855e-0fdc56887918` - Fishdom

> EDIT 1/17/2023: Customer Service can't make good on 9 diamonds when game element doesn't appear within 5 original moves and 5 additional moves. It is a fun game, you don't have to pay to win. I suggest after this cust. svc experience that you don't buy from this game beyond the pass.Get friends and a team and trade lives.

| | labels |
|---|---|
| gold | `M_RecurringFee`, `S_Reciprocity` |
| pred | `S_Reciprocity` |
| **missed** | `M_RecurringFee` |

**Did the model consider what it missed?**

- `M_RecurringFee` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer reports a customer service issue regarding missing diamond compensation when a game element fails to appear within a limited move window (5 original + 5 additional moves). They state the game is fun and does not require payment to win. They advise against purchasing beyond 'the pass,' which implies an existing subscription or pass product, but do not describe its mechanics. They explicitly describe obtaining and trading lives with friends and teammates, which is a resource-exchange mechanism. The direct dark pattern is the social trading mechanic; the customer service complaint, the move limit mechanic itself, and the pass reference do not establish sufficient mechanical description to code dark patterns under R2 and R3.
```

**Labels assigned**

- `S_Reciprocity` - ok
  - span: "trade lives"
  - why: The span explicitly names a mechanism in which the player exchanges an in-game resource (lives) with other players, matching the Reciprocity indicator.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fd1230ab-7d12-4aeb-a425-e37ed06bcd5c` - Pokémon GO

> I love this game, just started playing about 2 months ago. Though I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way. I feel taken advantage of. 3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| pred | `P_IllusionOfControl`, `S_FriendSpamImpersonation` |
| **missed** | `P_OptimismAndFrequencyBiases` |

**Did the model consider what it missed?**

- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes two separate issues. First, they claim that after they began purchasing pokéballs, they noticed the balls 'keep breaking out' more frequently during capture attempts, causing them to consume balls faster and requiring more purchases. They characterize this as being 'taken advantage of' and report that other players they spoke with felt the same way. This constitutes an allegation that the game is manipulating catch-rate outcomes based on purchase behavior—a mechanism designed to encourage continued purchasing. Second, the reviewer appends an edit stating 'I DID NOT WRITE THIS REVIEW' and 'I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE,' directly contradicting the content of the first review. This indicates the original review was posted under the player's account without their authorship or consent, whether through account compromise, an automated system, or unauthorized access.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: The span asserts that catch success (pokéball escape rate) is manipulated after the player begins purchasing, with the causal chain implying the game deliberately increases breakout rates to encourage more purchases. This is a claim of rigged outcomes presented as a consequence of spending.
- `S_FriendSpamImpersonation` - ok
  - span: "I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE"
  - why: The reviewer's edit explicitly states the preceding review was not written by them, indicating a store review was published under their account without their authorship or consent, which triggers the pattern regardless of whether the mechanism is account compromise or an automated game feature.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `5e6a5625-5291-4f0e-897c-1b63c1a26494` - MONOPOLY GO!

> I loved this game until the new season started. Suddenly I get no rewards for inviting friends and getting them to join facebook. I am struggling to get dices and when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way... And today. Well, I cannot log in to the game at all. It keeps giving me an internet connection error which is absolute nonsense. I have connected to 3 different wifi connections. BS!!😡

| | labels |
|---|---|
| gold | `M_Gambling`, `P_RewardMania`, `S_ForcedFellowship` |
| pred | `M_Gambling`, `P_RewardMania` |
| **missed** | `S_ForcedFellowship` |

**Did the model consider what it missed?**

- `S_ForcedFellowship` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes multiple game mechanics: (1) an invitation system that previously rewarded players for inviting friends but is no longer providing rewards after a season change; (2) dice rolls as the core mechanic where they spent 500+ dice attempting to land on rare outcomes (Shut Downs, bank heists) with no success; (3) sticker collection where duplicate drops are frequent, blocking album completion; (4) a login technical error. The search confirms that MONOPOLY GO! allows players to purchase dice with real money (R10), making the dice rolls a wagering system. The reviewer accumulated dice and wagered them ('played max bet') hoping for specific outcomes ('NO LUCK! No Shut downs and no bank heists'). The duplicates from sticker rolls represent variable/unpredictable rewards that frustrate collection progress. The invitation mechanic change is ambiguous about whether the current game still has the feature working—the reviewer states 'I get no rewards' suggesting attempted action without reward, but it's unclear if the mechanic is currently operative or disabled. The login error is a technical fault, not a dark pattern.
```

**Labels assigned**

- `M_Gambling` - ok
  - span: "when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists."
  - why: The reviewer spent a large quantity of dice (which are purchasable with real money per search) on maximum-stake rolls, hoping for rare outcomes (Shut Downs, bank heists). This is wagering real-money-convertible currency on randomized outcomes with no success, which satisfies Gambling.
- `P_RewardMania` - ok
  - span: "Stickers are duplicates all the way..."
  - why: The reviewer describes receiving sticker drops that are predominantly duplicates, which is a variable/unpredictable reward system delivering unwanted items that don't help album completion. This fits Variable Rewards under Reward Mania, as the randomness of what sticker is awarded on each roll sustains engagement with the collection mechanic.

**Search:** `MONOPOLY GO dice real money purchase` -> Confirmed that MONOPOLY GO! allows players to purchase dice with real money. Multiple results confirm dice are purchasable through the official store and third-party sellers, and are the core gameplay currency for advancing on the board and earning rewards.

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
- `M_IntermediateCurrency` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a UI design that automatically scrolls to and selects the highest-bet table when opening the game or accessing the 1v1 section. This mechanism is characterized as deliberately engineering accidental selection of high-stakes bets, causing players to lose coins without intending to. The loss then drives purchases of real money currency to recover. The mechanic is interface-based placement (auto-scroll and auto-select) designed to direct the player toward an option they likely did not intend, reducing deliberation through design.
```

**Labels assigned**

- `M_UIMisdirection` - ok
  - span: "Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks"
  - why: The interface uses automatic directional placement (scrolling and selecting) to make accidental high-bet selection likely without player intention, reducing deliberation through designed misdirection.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `33c422de-1a84-4df9-accd-cdf8bfc96295` - Dark War Survival

> No ingenuity for a base builder. Same old same old grinder. After a few weeks, it became abundantly clear that there is absolutely no opportunity for a general player to win an event. Zero skill pay to play. Zero skill pay to win. Calculated total spent on last event was 30k to win. Wish serious gamers would stop perpetuating the problem by continuing to spend obnoxious amounts of money on a little app that you just want to have a little fun on.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `S_Competition` |
| pred | `M_PayToProgress` |
| **missed** | `S_Competition` |

**Did the model consider what it missed?**

- `S_Competition` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer is describing a base-building game that requires payment to succeed in competitive events. The gameplay itself is characterized as repetitive and lacking variety ('same old same old grinder'), but this is a general evaluation of quality rather than a description of a specific repeated task (replaying levels, farming, etc.), so it does not trigger Grinding under the boundary rule. The core mechanic being described is that winning events is impossible for free players: 'absolutely no opportunity for a general player to win an event' combined with 'Zero skill pay to win' and 'Calculated total spent on last event was 30k to win' establishes that payment is required to achieve event victories. This is Pay to Win, a sub-indicator of M_PayToProgress. The reviewer's final comment about other players spending money is their commentary, not a description of a game mechanic.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Calculated total spent on last event was 30k to win"
  - why: The span shows that winning requires a calculated expenditure of 30k, demonstrating that payment is the mechanism to achieve competitive victory.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `84bbc363-d55a-4cf1-a557-c61ed7ab82bc` - Last War:Survival Game

> Once you get past building the city block stage, it gets kinda boring. It's just grinding resources trying not to get raided so you can level up to have a few more attempts at the left right scroller game. The advertisement that's really becomes not that great. The bigger alliances all just attack the smaller alliances and take their resources. I dedicated some time to this game and to my alliances and am disappointed with current status.

| | labels |
|---|---|
| gold | `S_Competition`, `S_EncouragesAntiSocialBehavior`, `T_Grinding` |
| pred | `S_EncouragesAntiSocialBehavior`, `T_Grinding` |
| **missed** | `S_Competition` |

**Did the model consider what it missed?**

- `S_Competition` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes several game systems: early-stage city building that becomes tedious, a resource-grinding loop required for progression, vulnerability to raids from other alliances, a game mode accessed through leveling up with limited attempts, and a pattern of large alliances attacking smaller ones to steal resources. The core complaint is repetitive grinding to progress, combined with vulnerability to player-versus-player predation targeting the weaker (smaller alliances). The reviewer invested time in both the game and alliance engagement, but expresses disappointment rather than reluctance to quit. The phrase about bigger alliances attacking smaller ones describes an asymmetric dynamic: stronger players targeting weaker ones who cannot effectively defend themselves, with plunder (resources) flowing to the attackers. This is a mechanic the game design enables and incentivizes through the reward structure.
```

**Labels assigned**

- `S_EncouragesAntiSocialBehavior` - ok
  - span: "The bigger alliances all just attack the smaller alliances and take their resources"
  - why: The game design enables and incentivizes larger alliances to prey on smaller alliances, rewarding the aggressor with stolen resources. This is asymmetric predation beyond sanctioned play: bullying smaller players who cannot effectively retaliate.
- `T_Grinding` - ok
  - span: "It's just grinding resources trying not to get raided so you can level up"
  - why: The review explicitly names grinding resources as the required repetitive activity for progression after the early game; the player must accumulate resources (by repetition) to level up.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `73423b22-395c-49ed-8fc3-488a0b7680df` - MONOPOLY GO!

> I like the game but frustrating when it comes to getting stickers. always get duplicates. never lets you finish all the sets unless you pay

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury`, `M_PayToProgress`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_PayToProgress`, `P_CompleteTheCollection`, `P_RewardMania` |
| **missed** | `M_DeceptiveLuxury` |

**Did the model consider what it missed?**

- `M_DeceptiveLuxury` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer likes the gameplay but describes two problems with the sticker collection system in Monopoly GO!. First, when receiving stickers from pulls, the system delivers duplicates repeatedly rather than progressing toward set completion. This is a variable reward mechanism where pulls yield unwanted items. Second, completing all the available sticker sets is impossible without payment—progress is gated by a paywall. The reviewer frames the sticker sets as the goal they want to complete, and the inability to do so without spending is the frustration point.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: Progress through completing the sticker sets is blocked unless the player pays money; finishing the sets requires a purchase.
- `P_CompleteTheCollection` - ok
  - span: "never lets you finish all the sets"
  - why: The review identifies the sticker sets as the goal the player is pursuing and the inability to complete them all as the source of frustration, triggering the collection compulsion pattern.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: The sticker reward system delivers unpredictably from a randomized pool, repeatedly giving duplicate items instead of the specific stickers needed to progress.

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
The reviewer describes three connected design patterns: (1) decreasing rewards over patches, (2) constant meta shifts requiring new character acquisitions, and (3) increasing pay-to-win design. The core complaint is that to maintain damage output and progress, players must repeatedly pull for new characters as the meta shifts and older characters lose viability. Pulling in Genshin Impact requires spending real-world money on gacha currency. This creates two dark patterns simultaneously: a payment requirement to stay competitive (PayToProgress), and the systematic devaluation of previously purchased characters as new releases become mandatory (PowerCreep). The reward decrease provides context for why payment becomes more necessary, but the direct forcing mechanism is the meta shift that obsoletes older characters and necessitates new purchases. The criticism about image quality is a separate quality complaint, not a dark pattern mechanic.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "forcing us to pull for new characters if we want to actually do damage"
  - why: Pulling for new characters requires spending real money on gacha currency. The reviewer states this spending is required ('forcing') to progress (maintain damage output), establishing that payment is a necessary gate to continued advancement.
- `M_PowerCreep` - ok
  - span: "the Meta changes more and more every single day basically forcing us to pull for new characters if we want to actually do damage"
  - why: The span shows that as meta shifts with each patch and new character releases, the reviewer's older characters can no longer maintain damage output, losing their acquired value. The forced pull for new characters indicates that previously purchased characters have become obsolete, a classic power creep pattern where new releases devalue prior purchases.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (4)

### `95ddadb3-82cd-4042-8a51-cf8b3ed164c2` - Mech Arena - Shooting Game

> You stuck waiting 30 seconds just to connect to a match. This game makes it seem like they give so many rewards but if all just for show. Its difficult to get weapon upgrades or any percs others you stick battling to win. This kind of games just rob you of your time in my opinion

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `T_Grinding` |
| **spurious** | `T_Grinding` |

**Model analysis**

```
The reviewer describes waiting to connect to matches and difficulty obtaining weapon upgrades. The 30-second connection wait is operational latency from matchmaking, not a designed in-game timer like energy regeneration or cooldowns, so it does not trigger Playing by Appointment per the codebook example that excludes matchmaking waits. The core mechanic described is the need to repeatedly battle in order to progress: 'Its difficult to get weapon upgrades or any percs others you stick battling to win' states that obtaining upgrades requires continuous battling. The statement 'This game makes it seem like they give so many rewards but if all just for show' expresses dissatisfaction with reward value but does not describe a specific mechanic: the rewards are not stated to be unpredictable, time-gated, or otherwise structurally designed to exploit cognition, only that they appear generous but lack substance. This is an evaluation of quality rather than a description of a dark pattern mechanic.
```

**Labels assigned**

- `T_Grinding` - **SPURIOUS**
  - span: "you stick battling to win"
  - why: The span indicates continuous repeated battling is necessary to achieve progress (obtaining weapon upgrades), which fits the definition of performing repetitive tasks to make progress.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `ab2097d3-2f9b-4a87-885c-25dfcddb5a70` - Gardenscapes

> Have been playing this game since COVID 19 lockdown. It was fun back then. Currently at 8416 and it gets frustratingly annoying after level 8000. I run out of lives 3-4 times daily to beat every alternate level, avg 5-7 days per level. You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying. Now I'm not interested anymore. Unistalling this game to invest some quality time in a real life. Wasted too much of money and time into this game.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `T_Grinding` |
| pred | `M_PayToProgress`, `T_Grinding`, `T_PlayingByAppointment` |
| **spurious** | `T_PlayingByAppointment` |

**Model analysis**

```
The reviewer describes a progression wall at high levels (8416) where the game becomes impossible to progress through without payment. Three mechanics are evident: First, a lives/energy system where the player runs out of lives multiple times daily, indicating the game controls when they can play through resource regeneration that must be awaited. Second, the need to repeatedly attempt difficult levels (indicated by running out of lives 3-4 times daily and spending 5-7 days per level), showing grinding through repetitive content. Third, an explicit requirement to purchase add-ons to progress reasonably—without payment, progression is described as a 'time waste.' The reviewer has abandoned the game after investing significant time and money, frustrated by the time and financial demands.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through a sane mind"
  - why: Span directly states that purchased add-ons are mandatory for reasonable progression; without payment, advancing becomes infeasible.
- `T_Grinding` - ok
  - span: "I run out of lives 3-4 times daily to beat every alternate level, avg 5-7 days per level"
  - why: The span describes repeated attempts at levels (depleting lives 3-4 times per day) required to progress, with each level taking 5-7 days, indicating the repetitive grind needed for advancement.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "I run out of lives 3-4 times daily to beat every alternate level"
  - why: Running out of lives 3-4 times daily implies the game's lives/energy system with regeneration gates play, forcing the player to play according to when the game replenishes resources, not their own schedule.

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
The reviewer describes a progression bottleneck at level 34 caused by limited inventory space. The game provides 98 total spaces (63 on board, 37 in refrigerator) with 72 occupied by required items or items the player refuses to delete, leaving only 26 free spaces. Individual items like a lambchop occupy up to 9 of those 26 spaces. The reviewer explicitly states that continuing to play and store new items requires spending money ('buy parts'). The inventory limitation forces a choice between two costs: deleting accumulated items the player has invested in building (generators, corn, chicken pie) or paying for additional storage. The player is reluctant to forfeit what they've accumulated, making both continuation and deletion costly, while payment removes the barrier. This combines a payment gate blocking progression, an inventory system that manufactures waste through misaligned capacity, and accumulated holdings that raise the cost of disengagement.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Not enough slots to store and play without spending $$ to buy parts"
  - why: Player states directly that playing and progressing requires payment. Payment removes the artificial inventory barrier that blocks continued play and storage of new items.
- `M_WasteAversion` - ok
  - span: "A lambchop can take up to 9 spaces or more of my 26 spaces and I'm not deleting the chicken pie"
  - why: Capped inventory with specific capacity (26 free spaces) and item sizes (9-space lambchop) creates a realized shortfall that forces either deletion of accumulated items or purchase. The player's explicit refusal to delete demonstrates the waste mechanism is active.
- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "72 are taken up by parts of generators or lower generators that I can't merge with higher generators yet or high level items like a corn that I am not going to delete"
  - why: Player has accumulated items through gameplay (generators, high-level items) and is reluctant to abandon them. These holdings now raise the cost of continuing: progression is impossible without either forfeiting accumulated investments or paying to expand capacity.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `ae3b6309-101e-4320-99b1-aa6795602787` - Genshin Impact

> The rewarding system is just DIABOLICAL, I just finished a 7 hour quest and I barely got any primogems. exploration is debilitating. the character design is as almost lame... especially for the female characters, they all have the same bare legs curse that makes the design uninteresting. it's just a horrible game, this game used to be fine by the ways. for context I've been playing since 2021, 5 years have passed can you imagine ? and there is no resin overflow system. 😭

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `M_PayToProgress`, `T_PlayingByAppointment` |
| **spurious** | `M_PayToProgress`, `T_PlayingByAppointment` |

**Model analysis**

```
The reviewer describes several design mechanics. First, primogems (premium currency) are obtained in very small amounts relative to time investment: finishing a 7-hour quest yields barely any primogems. This suggests either grinding through repetitive content for poor rewards, or slow progression that might incentivize payment. Second, exploration itself is described as 'debilitating'—exhausting and unpleasant. Third, the resin system: the reviewer states 'there is no resin overflow system.' The search reveals that resin caps at 200 and stops regenerating at cap, forcing players to log in regularly to spend it before hitting the cap and wasting regeneration. This is an appointment-based play schedule imposed by the game's resource regeneration mechanics. Fourth, the reviewer notes the game quality has declined over 5 years. However, the character design complaint (bare legs) is aesthetic preference, not a mechanic.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "I just finished a 7 hour quest and I barely got any primogems"
  - why: After 7 hours of play, the reviewer barely obtained the premium currency needed for character acquisition (primogems). The disproportionately low reward relative to effort implies the free earning path is so slow that spending becomes the practical route to progress.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "there is no resin overflow system"
  - why: The absence of overflow protection means resin stops regenerating at cap, creating a schedule the player must follow to prevent loss. The search established resin regenerates on a fixed 8-minute cycle, establishing the schedule element. This forces appointment-based play.

**Search:** `Genshin Impact resin system regeneration cap overflow` -> Resin is the energy system capping at 200 units and regenerating at 1 unit every 8 minutes. When resin reaches the cap, regeneration stops, forcing players to log in regularly to spend it and prevent wasting future regeneration gains.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `S_Competition` | 6 | 0 |
| `T_Grinding` | 2 | 2 |
| `M_IntermediateCurrency` | 4 | 0 |
| `T_PlayingByAppointment` | 1 | 2 |
| `P_RewardMania` | 2 | 1 |
| `P_EasyToGetHardToLose` | 0 | 2 |
| `M_DeceptiveLuxury` | 1 | 1 |
| `M_Gambling` | 1 | 1 |
| `P_OptimismAndFrequencyBiases` | 1 | 1 |
| `P_AestheticManipulation` | 2 | 0 |
| `S_Reciprocity` | 2 | 0 |
| `M_PayToProgress` | 0 | 1 |
| `T_MandatoryMarathon` | 1 | 0 |
| `M_WasteAversion` | 0 | 1 |
| `M_RecurringFee` | 1 | 0 |
| `S_ForcedFellowship` | 1 | 0 |

