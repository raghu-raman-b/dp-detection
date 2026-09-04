# Error review - deepseek-v4-flash_max_teacher_v3_full

`deepseek-v4-flash` / reasoning `max` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v3_full.txt` sha `a6ae58246360`  
micro-F1 **0.777** (P 0.859 / R 0.709) - **25 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 7 | said NONE, gold had labels |
| SWAP | 3 | picked different labels than gold |
| MISSED ONLY | 9 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 6 | found all gold, added extras |

## The diagnostic that matters

Of **25** missed labels, **2** (8%) were named in the model's own analysis and dropped anyway; **23** (92%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `S_Competition` | 0 | 3 |
| `M_UIMisdirection` | 0 | 2 |
| `M_DeceptiveLuxury` | 0 | 2 |
| `P_RewardMania` | 0 | 2 |
| `M_Gambling` | 0 | 2 |
| `T_Grinding` | 0 | 2 |
| `M_IntermediateCurrency` | 0 | 2 |
| `S_Reciprocity` | 1 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `M_PayToProgress` | 0 | 1 |
| `M_WasteAversion` | 0 | 1 |
| `P_EasyToGetHardToLose` | 1 | 0 |
| `T_MandatoryMarathon` | 0 | 1 |
| `P_AestheticManipulation` | 0 | 1 |
| `S_FriendSpamImpersonation` | 0 | 1 |

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
The review is a 10/10 rating followed by four numbered feature requests. None of the four describes a mechanic currently present in the game: item 1 asks for a new auction/bid system, item 2 asks to change how obstacle decoration removal works, item 3 asks for an out-of-game widget showing upgrade timers across accounts, and item 4 asks for a hidden advanced-stats option. Under R12, requests, suggestions, or hypothetical additions do not trigger tags for the proposed mechanics, even where a proposal (e.g., seeing upgrade time remaining) gestures at an existing timer system. Nothing in the text describes an active design behaviour that is currently in the game, so no meso label is supportable.
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
The review is entirely a technical bug report. Every mechanic named — opening gifts, trading with friends, throwing pokeballs at pokemon, PvP and rocket battles, switching pokemon, charge attacks — appears only as the site of crashing, lagging, freezing, or unresponsive input. The reviewer attributes all of these to the game failing, not to design rules, and asks for fixes. Under R11, behaviour attributed to bugs, glitches, or technical faults is not coded as a dark pattern because dark patterns are deliberate design choices rather than malfunctions. No span describes a working design mechanic with a reward, penalty, schedule, or payment attached, and no span describes an exit rule being imposed by design rather than by the freeze itself.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a12b6d56-8505-4b4e-9b43-cde2d1085360` - MadOut 2: Grand Auto Racing

> well I LOVE the game BUT I know if I deleted the game I would lose everything my in-game purchases and my hard work I really don't want that to happen because it has happened on other games it's just a suggestion is there anyway possible to where you guys can make it where you save all our progress in-game purchases and everything else that we have done because if this game can hold that then I will be looking forward to be putting money in this game

| | labels |
|---|---|
| gold | `P_EasyToGetHardToLose` |
| pred | _NONE_ |
| **missed** | `P_EasyToGetHardToLose` |

**Did the model consider what it missed?**

- `P_EasyToGetHardToLose` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer says they love the game but believe that deleting it would erase their in-game purchases and hard-earned progress, and asks the developers to add a feature that saves progress and purchases so they can feel safe spending money. What is actually being described: (1) the reviewer's belief or experience that progress is stored only on the device with no account-linked cloud save, and (2) a request/suggestion for a new feature. The request itself is hypothetical and cannot trigger a label under R12. The fear of losing invested purchases and time expresses caution, but nothing attributes that loss exposure to a designed dark pattern, and no label covers 'no cloud save.' It does not describe an exit penalty imposed by a game rule (Mandatory Marathon requires being prevented from stopping or losing progress by the game's own exit rules, which is not what is said), nor a designed mechanism that builds investment to raise the cost of leaving (Easy to Get Hard to Lose requires the design operating on the player's choice to stay; here the reviewer is actively engaged and merely asking for protection). This is a feature suggestion, not a description of a present manipulative design, so no meso label applies.
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
The reviewer describes a regression: after one of the updates, the troop-request feature in their clan stopped working, and they ask for it to be fixed. Even though requesting troops is a clan-based resource-transfer mechanic that could in principle match S_Reciprocity, the text attributes the behaviour to an update-induced fault and requests a repair. Per R11, a behaviour attributed to a bug, glitch, or technical fault is not a deliberate design choice and does not trigger a dark-pattern label. Nothing in the review describes any other game mechanic or design behaviour.
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
The review is essentially two feature requests plus one mild complaint, all in a positive tone. The first sentence praises the game and its upgrades. The second sentence asks for an in-app way to trade stickers, motivated by the fact that not every player uses Facebook; per R12, a requested feature that does not currently exist is not codable, and no existing mechanic (messaging, posting, or recruitment through Facebook) is described as currently active. The third sentence states that when another player challenges the reviewer to a match, a purchased booster cannot be used, which the reviewer believes is wrong. This names two existing behaviours - purchasable boosters and player-to-player challenges - but describes no listed dark pattern: there is no pay wall or paid progress gate, no devaluation of a purchased item over time, no stranded currency or inventory forfeiture, no chance mechanic, no schedule, no reward cadence, and no social exploitation. The mention of another player challenging is purely contextual framing for the booster complaint, not a description of the game pitting players against each other for manipulative purposes. No label is supported.
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

- `T_Grinding` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer is describing a mismatch between the game's external advertisements, which promise physics puzzles, and the actual in-game experience, an involved strategy game with only occasional puzzles. Under R13, marketing material and misleading advertising placed outside the game are outside the analysis unit, so the central complaint cannot generate a label. The remaining in-game mechanics mentioned (making an army, training, building, gathering resources) are described neutrally or favourably, and the phrase 'doing chores in order to get to them' is an evaluative comment on pacing rather than a specific description of a repetitive, tedious activity cycle tied to progress. No temporal, monetary, social, psychological, or technical dark pattern is actually described inside the game.
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
The reviewer describes closing the game with a full inventory and earned-plus-purchased coins, then returning to find the bag empty and the coins gone. This is a report of state loss between sessions: items and currency the player held are not there when they come back. Nothing in the text describes a designed mechanic that deliberately consumes holdings, imposes a penalty rule, or gates progress. The plain reading is that the game failed to preserve the player's session state, i.e., a save/progress fault. Under R11, losses attributed to technical malfunction rather than to an explicit game rule are not coded; here the loss itself (progress not saved, holdings not credited) is the fault, and no exit rule or design penalty is described that would have produced it. No other mechanic is named or implied.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (3)

### `fdef27f2-9a21-4b8e-a04c-7a4753e0fb07` - 8 Ball Pool

> The game is great, but the user interface is completely rigged. Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins and are forced to buy real ones. ​We need a "Default Table Lock" or the game should always open the lowest bet table by default, not the highest! Fix this scammy feature. Giving 1 star

| | labels |
|---|---|
| gold | `M_Gambling`, `M_IntermediateCurrency`, `M_UIMisdirection` |
| pred | `M_EasyToPurchase` |
| **missed** | `M_Gambling`, `M_IntermediateCurrency`, `M_UIMisdirection` |
| **spurious** | `M_EasyToPurchase` |

**Did the model consider what it missed?**

- `M_Gambling` - never mentioned -> **attention / recall**
- `M_IntermediateCurrency` - never mentioned -> **attention / recall**
- `M_UIMisdirection` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a specific UI behaviour in 8 Ball Pool: whenever the game opens or the player enters the 1v1 section, the interface automatically scrolls to and pre-selects the highest-stakes table the player's coin balance can cover. The reviewer explains the design intent: because the high-stakes table is already selected, the player's normal tap lands on a bet they did not deliberately choose, causing accidental mis-clicks that drain their earned coins and push them toward buying coins with real money. This is a default-option deception: the player must notice and manually change the selection to avoid the unintended stake, and the trick is explicitly tied by the reviewer to real-money purchases ('forced to buy real ones'). The mechanic described is interface-driven friction reduction on spending, not grinding, scheduling, social pressure, or chance-based rewards.
```

**Labels assigned**

- `M_EasyToPurchase` - **SPURIOUS**
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins and are forced to buy real ones."
  - why: Auto-selecting the highest-stakes table as the default makes an unintended stake easy to commit by a normal mis-click, and the reviewer states the purpose of the design is to drain coins so players have to buy currency with real money; the trick is a default-option deception with no protective step between the tap and the loss.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `ab2097d3-2f9b-4a87-885c-25dfcddb5a70` - Gardenscapes

> Have been playing this game since COVID 19 lockdown. It was fun back then. Currently at 8416 and it gets frustratingly annoying after level 8000. I run out of lives 3-4 times daily to beat every alternate level, avg 5-7 days per level. You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying. Now I'm not interested anymore. Unistalling this game to invest some quality time in a real life. Wasted too much of money and time into this game.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `T_Grinding` |
| pred | `M_PayToProgress`, `T_PlayingByAppointment` |
| **missed** | `T_Grinding` |
| **spurious** | `T_PlayingByAppointment` |

**Did the model consider what it missed?**

- `T_Grinding` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer is describing their endgame experience of Gardenscapes: the lives system depletes several times a day so play stops until lives regenerate, levels now take days each, and the only way through without heavy time investment is buying add-ons. The mention of running out of lives implies the game's timer-based regeneration gate. The statement that add-ons are needed and that it is a time waste if you are not paying describes a paid shortcut against a slow free route. The closing line about wasted money and time is a disengagement statement, not a description of investment keeping the player in the game.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying."
  - why: Continued progress is stated to require buying add-ons, and the free route is framed as a time-wasting alternative that falls short of smooth advancement.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "I run out of lives 3-4 times daily to beat every alternate level"
  - why: Running out of lives forces the player to stop and wait for the game's timer-based regeneration before continuing, so play happens on the game's schedule.

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
The review is mostly about in-app purchases for an album-completion collectible system. The reviewer is two cards short of completing an album and buying a deal seemingly promising to supply cards; instead of the missing cards they receive duplicates, so they call it a scam. The core mechanics described are: collecting a fixed album set where completion carries a grand prize (collectible/collection drive); purchasable deals that deliver randomly drawn cards so duplicates are possible (chance-based reward delivery with a real-money stake); and I need to clarify that 'cards' here come from Dice Dreams' sticker/album system rather than, say, card game strategy.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "i bought a deal which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: The purchase is a real-money stake, and the outcome is not fixed: the deal is said to promise new cards but the player still receives duplicates, so the cards appear delivered by a chance-based draw rather than a guaranteed item.
- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The player is only two cards away from a complete album and frames that missing-card state as the motivation for the purchase, so the collection drive is what the text describes.
- `P_RewardMania` - ok
  - span: "all i got were useless duplicates!"
  - why: The deal draws from a random card pool, and receiving duplicates shows the delivery is unpredictable and repeated rather than based on the reward's value, which is the variable-reward delivery mechanism.

**Search:** `Dice Dreams sticker album deal buying cards duplicates new cards` -> Dice Dreams' 'cards' are collectible album stickers, and purchases/deals deliver cards that can duplicate; players seek missing stickers to complete albums for a grand prize.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (9)

### `5f3e71b5-200c-45a3-b90e-e08b0dc0e1a3` - Cash Frenzy™ - Casino Slots

> Is a good game, but I will like to place my formal complain about the genie game, in multiple times whe the wheel spin after stopping on a great price the genie move the wheel to a spin tag, and then the prices after the spin are way lower than the original price, from 100 million with 5x multiplier to a 48 million. Is the only part I don't like. There should be a player choice to keep or spin.

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_RewardMania` |
| pred | `P_IllusionOfControl` |
| **missed** | `P_RewardMania` |

**Did the model consider what it missed?**

- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer is describing a bonus mini-game inside the slot machine experience, apparently a genie-themed wheel. Mechanically, the player watches the wheel land on a large prize, then the genie moves the wheel to a 'spin' outcome and the credited prize ends up far smaller than what was first shown. The reviewer wants the choice to keep the first result instead of being forced to spin on. This describes the game overriding a visibly displayed reward with a lower actual payout - the presentation of the outcome diverges from the settlement of the outcome. No real-money purchase, wager, ad, timer, or social mechanic is mentioned, so monetary, temporal, and social labels are not supported by the text.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "in multiple times whe the wheel spin after stopping on a great price the genie move the wheel to a spin tag, and then the prices after the spin are way lower than the original price, from 100 million with 5x multiplier to a 48 million"
  - why: The wheel visibly settles on a 500-million-equivalent result and the game then overrides it to a much smaller payout, so the span asserts that the shown outcome is not the real outcome - concealed manipulation of the result rather than a mere unlucky run.

**Search:** `Cash Frenzy casino slots "genie" wheel bonus game what does the genie do` -> The search identified that the genie feature can activate Wheel Bonus and multiplier events in Cash Frenzy, but did not establish an official rule about the genie overriding an already-landed prize. The reading therefore relies on the reviewer's own description of the displayed wheel outcome being changed.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b98d7e75-73da-4591-b23e-1a2951bfd856` - Township

> I like this game a lot, but recently after seeing the ads, there is no way to close it. No cross mark on the screen , if you try to click anywhere on the screen it takes you to store. If you go back to game it is still stuck in the last sceeen of the ad. You have to kill the game to come out of the ad screen , so frustrating!!!

| | labels |
|---|---|
| gold | `M_UIMisdirection`, `T_Advertisement` |
| pred | `T_Advertisement` |
| **missed** | `M_UIMisdirection` |

**Did the model consider what it missed?**

- `M_UIMisdirection` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer is describing ads encountered while playing the game. The complaint centers on the ad interface: no close control is offered, tapping anywhere redirects to the app store, and returning leaves the game stuck on the ad screen until the player force-closes the app. This describes an in-game ad experience that is non-dismissable and intercepts the session, which is a design behavior rather than a technical malfunction in the game itself; the reviewer attributes the behavior to the ad presentation, not to a crash or bug.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "after seeing the ads, there is no way to close it. No cross mark on the screen , if you try to click anywhere on the screen it takes you to store. If you go back to game it is still stuck in the last sceeen of the ad. You have to kill the game to come out of the ad screen"
  - why: The player is compelled to view the ad to completion because there is no way to dismiss it, and any click routes to the store rather than back to play.

**Search:** `Township mobile game ads no close button stuck` -> Some Township mobile game ads lack a close button, causing users to force close the game; solutions include waiting for a hidden close button or clearing the game's cache.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fd1230ab-7d12-4aeb-a425-e37ed06bcd5c` - Pokémon GO

> I love this game, just started playing about 2 months ago. Though I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way. I feel taken advantage of. 3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| pred | `P_IllusionOfControl` |
| **missed** | `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |

**Did the model consider what it missed?**

- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**
- `S_FriendSpamImpersonation` - never mentioned -> **attention / recall**

**Model analysis**

```
The body of the review claims that after the reviewer started making purchases, Poké Balls break out of captures more often, burning through balls faster and forcing more purchases. Whatever the plausibility, this is an assertion that the game's outcome determination (catch success) is manipulated once the player spends, with the manipulation framed as driving further spending. The appended note disclaiming authorship is about review integrity and describes no game mechanic. No timers, ads, currencies, social mechanics, or reward schedules are described, so the only mechanic the review carries is the alleged rigging of capture outcomes.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: The span asserts that the game concealed or manipulated the determination of capture outcomes after the player began paying, so the deception is about how results are decided rather than a report of a losing run.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `5e6a5625-5291-4f0e-897c-1b63c1a26494` - MONOPOLY GO!

> I loved this game until the new season started. Suddenly I get no rewards for inviting friends and getting them to join facebook. I am struggling to get dices and when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way... And today. Well, I cannot log in to the game at all. It keeps giving me an internet connection error which is absolute nonsense. I have connected to 3 different wifi connections. BS!!😡

| | labels |
|---|---|
| gold | `M_Gambling`, `P_RewardMania`, `S_ForcedFellowship` |
| pred | `P_RewardMania`, `S_ForcedFellowship` |
| **missed** | `M_Gambling` |

**Did the model consider what it missed?**

- `M_Gambling` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer is describing several MONOPOLY GO! systems across one season change. First, they describe a referral-style mechanic: the game had been rewarding them for inviting friends and getting them to join through Facebook, and they complain the reward stopped when the new season started — the recruitment incentive is the mechanic being described even as it fails. Second, they mention struggling to obtain dice, a resource-scarcity complaint with no timer, wait, or payment structure described. Third, playing at max bet and getting no shutdowns or bank heists is a report of an unlucky run, with no claim that outcomes are rigged or that near-wins were frequent. Fourth, sticker rewards arriving 'as duplicates all the way' describes the delivery of repeated, unwanted drops from the randomized sticker pool. Fifth, the login failure with an internet connection error is a technical fault, which R11 excludes. No term is obscure enough to require a search.
```

**Labels assigned**

- `P_RewardMania` - ok
  - span: "Stickers are duplicates all the way"
  - why: The span describes how rewards are delivered — repeated duplicate drops from the random sticker pool — which is the duplicate-drop delivery indicator, rather than a complaint about a reward's size or value.
- `S_ForcedFellowship` - ok
  - span: "Suddenly I get no rewards for inviting friends and getting them to join facebook"
  - why: The span describes a design in which in-game rewards are attached to recruiting friends to join through Facebook, which is the invite-others-for-rewards instance of Forced Fellowship; the complaint that the reward stopped does not change what the mechanic is.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b2dc0bc8-8ebe-4c48-bc05-38d0d65acb84` - Last War:Survival Game

> It's a nice game, but it's set up in a pay to win way. I played for 10 days, and the update times for your base are becoming ridiculous. Everything scales endlessly, there is kinda no point to look forward to, just more grind. The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff. Alliances are also weird, with the top ones dictating what to develop, what to rush, etc. If you are not in one then you get attacked and bullied. Not a great experience.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_UIMisdirection`, `S_Competition`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| pred | `M_PayToProgress`, `M_UIMisdirection`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| **missed** | `S_Competition` |

**Did the model consider what it missed?**

- `S_Competition` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes several structural design features of an idle/base-building war game after ten days of play. (1) They state the game is pay-to-win: spending is the route to advantage, though no specific purchase is named. (2) They describe base upgrade timers growing 'ridiculous', which is an in-game wait imposed by the game's clock rather than by the player. (3) They describe the progression system as scaling endlessly with nothing to look forward to, i.e., an unattainable end state where content keeps expanding. (4) They attribute the confusing, overwhelming UI to a deliberate purpose: pushing the player toward buying, which ties the interface design to purchases rather than being a mere quality complaint. The alliance remarks describe coerced grouping for protection (join or get attacked), with no recruitment reward, resource transfer, or incentive for harmful acts shown, so no social label fits. 'Just more grind' is a bare characterisation of tedium with no repeated activity specified, so Grinding is not separately coded.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "it's set up in a pay to win way"
  - why: The reviewer states the game grants advantage to players who spend, which is the Pay to Win instance of Pay to Progress.
- `M_UIMisdirection` - ok
  - span: "The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff"
  - why: The interface design is attributed to a purpose that serves the game against the player's intent - steering them to purchases - so it is UI Misdirection rather than a quality complaint.
- `T_InfiniteTreadmill` - ok
  - span: "Everything scales endlessly, there is kinda no point to look forward to, just more grind"
  - why: Progression is described as endlessly scaling with no attainable goal ahead, so the game never permits completion.
- `T_PlayingByAppointment` - ok
  - span: "the update times for your base are becoming ridiculous"
  - why: Base upgrade timers are in-game timers that force the player to wait on the game's schedule, which is the Wait to Play instance.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `3c46f5e0-6091-43dc-94a0-e3af3259a63d` - Cashman Casino Slots Games

> Resently cashman had changed it's bingo rewards and daily rewards. However lve found that I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards. The most I can seem to get on the timed rewards is 40,000. I'd not pay just to get my daily rewards. So I'm deleting them.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_WasteAversion`, `T_DailyRewards` |
| pred | `M_PayToProgress`, `T_DailyRewards` |
| **missed** | `M_WasteAversion` |

**Did the model consider what it missed?**

- `M_WasteAversion` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer is describing a change to the game's reward structure: collecting the daily rewards now requires wagering 50,000 chips first, and the free timed rewards only ever supply up to 40,000, so the daily reward target cannot be met with free play alone. The reviewer explicitly frames paying as the alternative and says they will not do it just for the daily rewards, then uninstalls. Two mechanics are being described: a daily reward system whose completion depends on a daily task (the 50k bet) and is forfeited if the task is not met, and a design in which the free path falls short of the requirement so that completing the reward is contingent on payment. No luck-based real-money wager, no timer-driven schedule complaint, and no unknown terminology requiring a search are present.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "The most I can seem to get on the timed rewards is 40,000. I'd not pay just to get my daily rewards."
  - why: Free earnings are stated to cap at 40,000 below the 50,000 the daily reward demands, and payment is framed as the route that would obtain the reward; because the free path cannot reach the target, completing the reward is contingent on paying.
- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The daily reward is only available if the player completes a resetting daily task (wagering 50,000), and failing that task forfeits that day's reward, which is the daily-incentive-with-consequence structure the label covers.

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
The reviewer is describing Dice Dreams as a game where success and completion are gated behind real-money spending. The opening comment about the five-star rating relates to the store-review system, which is outside the game application and not a codable mechanic. The substantive descriptions are: (1) winning or achieving anything requires hundreds of dollars, so the free route does not deliver progress; (2) the sticker album can never be finished because the last one or two stickers are unobtainable unless the player pays a lot, so payment is the only route to completing the collection; (3) goal completion succeeds only rarely, which reads as a complaint about odds or difficulty rather than a claim of a rigged mechanism or of manipulated near-misses, so no Illusion of Control or Optimism/Frequency label is supported. No chance-based purchase, loot box, or wager is described, so Gambling does not apply.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: Completing the sticker collection is stated to be impossible without payment, so further progress is contingent on spending money.
- `P_CompleteTheCollection` - ok
  - span: "you will never get the last one or two unless you pay a lot of money to get them"
  - why: The player is working toward a complete sticker album, and the review frames the missing last stickers as the goal that payment alone can reach, which is collection-driven play.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `45e3e2f0-4612-4d60-9312-3bff055ec9f3` - Merge Cooking®

> I really enjoyed this game until I got to a higher level. About to quit at level 34. Not enough slots to store and play without spending $$ to buy parts. I have 63 spots, on the board and 37 spots in the refrigerator. 98 spaces total, 72 are taken up by parts of generators or lower generators that I can't merge with higher generators yet or high level items like a corn that I am not going to delete. A lambchop can take up to 9 spaces or more of my 26 spaces and I'm not deleting the chicken pie

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_WasteAversion` |
| pred | `M_WasteAversion` |
| **missed** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_PayToProgress` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a storage/inventory bottleneck in a merge game at higher levels. The board (63 spots) and refrigerator (37 spots) together hold 98 slots, of which 72 are occupied by generator parts that cannot be merged yet or by high-level items the player refuses to delete, leaving 26 free spaces—and a single item (lambchop) can demand up to 9 of those. The player states the only alternative to this squeeze is paying real money for more capacity ('spending $$ to buy parts'). The mechanic being described is a capped inventory that forces the choice between sacrificing invested items and paying to expand capacity—the canonical capped-inventory scenario. No other mechanics (timers, dailies, grinding, social features, ads) are described. The player's refusal to delete items is a gameplay choice, not a claim that sunk investment is keeping them in the game, since they explicitly say they are about to quit.
```

**Labels assigned**

- `M_WasteAversion` - ok
  - span: "Not enough slots to store and play without spending $$ to buy parts. I have 63 spots, on the board and 37 spots in the refrigerator. 98 spaces total, 72 are taken up by parts of generators or lower generators that I can't merge with higher generators yet or high level items like a corn that I am not going to delete. A lambchop can take up to 9 spaces or more of my 26 spaces and I'm not deleting the chicken pie"
  - why: The inventory is full of un-mergeable and high-level items, leaving a realized shortfall (only 26 free slots, one item needing 9), and the stated way out is paying real money to expand capacity rather than deleting invested items—exactly the capped-inventory scenario the definition names.

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
The reviewer is describing the sticker album collection mechanic in MONOPOLY GO. Cards come in as sticker packs that produce repeated duplicates, and set completion is blocked unless money is spent. Three mechanics are in play: the collection-compulsion frame (the player is trying to finish the sticker sets and not finishing is the stated frustration), the randomised delivery of sticker packs that keeps yielding duplicates rather than new cards, and a pay gate where completing the sets is unavailable without payment.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: Completing the sets is stated to be contingent on payment and unobtainable without it, which is the Pay Wall instance.
- `P_CompleteTheCollection` - ok
  - span: "never lets you finish all the sets"
  - why: The reviewer is working toward completing all the sticker sets and frames the inability to finish them as the harm, which is the collection-compulsion pattern.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: Duplicates from randomised sticker packs show the delivery mechanism producing repeated unwanted drops, which sustains engagement through the random schedule rather than the reward's value.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (6)

### `95ddadb3-82cd-4042-8a51-cf8b3ed164c2` - Mech Arena - Shooting Game

> You stuck waiting 30 seconds just to connect to a match. This game makes it seem like they give so many rewards but if all just for show. Its difficult to get weapon upgrades or any percs others you stick battling to win. This kind of games just rob you of your time in my opinion

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `T_Grinding` |
| **spurious** | `T_Grinding` |

**Model analysis**

```
The review complains that the game consumes the player's time. First, a 30-second wait to connect to a match: this is matchmaking/queue latency, a service-side wait rather than a designed timer gate, so Playing by Appointment does not apply. Second, the claim that the game appears to give many rewards but they are 'just for show': this evaluates the reward's worthlessness rather than describing how rewards are delivered, so Reward Mania does not apply. Third, difficulty obtaining weapon upgrades and perks, requiring the player to keep battling: this names the repeated activity (matches/battling) as the route to progression items and frames the time spent as stolen, which matches the repetitive-task-for-progress structure of Grinding. The closing 'rob you of your time' is an evaluation that supports the time-investment reading rather than adding a separate mechanic.
```

**Labels assigned**

- `T_Grinding` - **SPURIOUS**
  - span: "Its difficult to get weapon upgrades or any percs others you stick battling to win"
  - why: The span names the activity the player must persist in (battling matches) as the way to earn weapon upgrades/perks and win, describing time invested in repeated play rather than skill, which the reviewer then frames as being robbed of time.

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
The reviewer describes a base-builder they dismiss as a generic grinder, then focuses on event participation: after weeks of play, a non-spending player cannot win events because skill is irrelevant and victory is determined by money instead ('pay to play' / 'pay to win'), citing that a rival spent a huge real-money amount on the last event to win. The recurring events appear to be ranked contests with other players, since the alternative to paying is framed as having 'no opportunity … to win', and the spend is what purchased the win. The complaint is about design that uses repetitive progression and competitive, pay-gated events rather than about technical quality.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Zero skill pay to play. Zero skill pay to win. Calculated total spent on last event was 30k to win."
  - why: The reviewer attributes event success to payment rather than skill, with an explicit account of spending a large amount to win.
- `S_Competition` - ok
  - span: "there is absolutely no opportunity for a general player to win an event. Zero skill pay to play. Zero skill pay to win. Calculated total spent on last event was 30k to win."
  - why: The event is presented as a ranking contest where the winner is decided by rival spending, so players are made to compete against each other.
- `T_Grinding` - **SPURIOUS**
  - span: "Same old same old grinder."
  - why: Calling the game a 'grinder' names the repetitive task cycle required to advance, rather than merely the review's mood.

**Search:** `Dark War Survival events leaderboard gameplay` -> Dark War Survival events are leaderboard competitions between players and alliances, with rewards and high ranks driven by progress and spending.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `32c623b4-0249-469e-968c-94f60c7fe3c2` - Royal Match

> It's an interesting game but the developers should pls try to include new cards in every card pack because I noticed when one is almost close to completing a set, new cards don't appear again especially when the set is almost expiring. So after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion because they don't add new sets to the cards once the collection is about to end.

| | labels |
|---|---|
| gold | `P_CompleteTheCollection`, `T_PlayingByAppointment` |
| pred | `P_CompleteTheCollection`, `P_IllusionOfControl`, `P_RewardMania`, `T_PlayingByAppointment` |
| **spurious** | `P_IllusionOfControl`, `P_RewardMania` |

**Model analysis**

```
The reviewer is describing a limited-time collectible-card event inside Royal Match: cards arrive through card packs, players assemble sets, and completing a set before the event ends pays out a completion reward. Two layered grievances drive the review. First, the delivery mechanism: the reviewer claims the packs stop yielding new cards precisely as a set nears completion and as the event nears its end, i.e., the random-seeming card distribution is conditioned to withhold the missing pieces. Second, the time pressure: because the collection expires on the game's clock, the withheld cards mean the completion reward is forfeited. There is no mention of money, ads, or other players, so monetary, advertisement, and social labels do not apply. The card packs are a chance-based delivery system for rewards (the player only gets repeats near completion), the withholding itself is framed as deliberate manipulation, the completion of the set is the goal whose loss is the stated harm, and the expiry of the collection on the game's schedule is what converts the withheld cards into a lost reward.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion"
  - why: The player is pursuing the completion of card sets within a collection, and the review frames not finishing the set as the harm.
- `P_IllusionOfControl` - **SPURIOUS**
  - span: "I noticed when one is almost close to completing a set, new cards don't appear again especially when the set is almost expiring"
  - why: The reviewer asserts the card draws are conditioned to withhold new cards near completion and expiry, which is a claim that the game manipulates a random-seeming outcome.
- `P_RewardMania` - **SPURIOUS**
  - span: "when one is almost close to completing a set, new cards don't appear again especially when the set is almost expiring"
  - why: Cards are delivered through packs as a variable-reward pool, and the span describes repeated attempts yielding no needed new cards, i.e., the delivery schedule of the reward system itself.
- `T_PlayingByAppointment` - ok
  - span: "you will miss the reward for the set completion because they don't add new sets to the cards once the collection is about to end."
  - why: The completion reward expires on the game's clock when the collection ends, so the reward is lost because the player could not finish before the game-defined deadline.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `ae3b6309-101e-4320-99b1-aa6795602787` - Genshin Impact

> The rewarding system is just DIABOLICAL, I just finished a 7 hour quest and I barely got any primogems. exploration is debilitating. the character design is as almost lame... especially for the female characters, they all have the same bare legs curse that makes the design uninteresting. it's just a horrible game, this game used to be fine by the ways. for context I've been playing since 2021, 5 years have passed can you imagine ? and there is no resin overflow system. 😭

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `T_PlayingByAppointment` |
| **spurious** | `T_PlayingByAppointment` |

**Model analysis**

```
The review is a frustration rant about three things: (1) quest rewards are stingy - a 7-hour quest yielded few primogems; this is a complaint about reward value and pacing, not about how rewards are delivered or about money being spent, so it does not trigger Reward Mania (value complaints do not assign it) or Intermediate Currency (no real-money conversion is described); (2) exploration and character design are called tedious and bland - these are quality evaluations and code NONE under R2, including for Aesthetic Manipulation, which requires the game deploying aesthetics to influence behavior rather than the reviewer disliking the art; (3) the closing remark about 'no resin overflow system' - in Genshin Impact, resin is the stamina-style resource that regenerates over real time up to a hard cap; the reviewer's complaint is that time away from the game wastes regeneration because nothing accrues beyond the cap. That last point describes the game's energy-timer schedule operating on the player: play must fit the game's clock or the resource is forfeited, which is a Wait to Play instance of Playing by Appointment. The 5-year tenure is context, not an investment-retention claim, so Easy to Get, Hard to Lose does not apply.
```

**Labels assigned**

- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "there is no resin overflow system"
  - why: Resin is Genshin's stamina resource that refills over real time to a cap; the absence of an overflow system means regeneration past the cap is wasted, so play must happen on the game's energy schedule or value is forfeited - an in-game timer imposing a wait and a schedule obligation.

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
The review is a numbered list of complaints about Candy Crush Soda Saga's economy. Complaint 1 says the game 'charged' premium gold pieces for extra moves at a moment when the player still had moves left, describing an unintended or unneeded charge with no sign the player deliberately consented to it — i.e., a purchase that should not have gone through. Complaint 2 says a paid package failed to deliver its advertised lives; that is a delivery/customer-service failure, not a designed dark pattern. Complaint 3 says timed bonuses keep counting down while the app is closed, so the value of the bonuses is lost unless the player plays inside the window the game's clock defines. Complaint 4 states that gold (Candy Crush's premium currency, bought with real money) cannot be earned in sufficient amounts to keep playing without buying, so continued play is contingent on purchasing currency. Complaints 5 and 6 are price and policy opinions: packages cost too much and should not be timed, restating the timer problem already covered. No term needs an external lookup; the review names the mechanics directly.
```

**Labels assigned**

- `M_EasyToPurchase` - **SPURIOUS**
  - span: "I was charged 10 gold pcs for 5 moves, I had 2 moves left."
  - why: The player was charged premium currency for moves they did not need while moves remained, so the charge went through without their intended consent, implying no confirmation or undo step stood between them and the purchase.
- `M_IntermediateCurrency` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: Gold is the premium currency that the span says must be bought, so real money is being converted into in-game currency to sustain play.
- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: Continued play is stated to be contingent on buying gold because winnings fall short, so progress stops unless payment is made.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone."
  - why: Timed bonuses run on the game's clock and deplete while the player is away, so the player must play within the window the game defines or forfeit the bonuses.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `1da19dbd-f522-43c7-95d7-df59f631cc18` - Total Battle: War Strategy

> They ruined game, there's no more "battle" in total battle with latest update to get rid of open silver. Save your time and money and don't bother. You have to spend to have any meaningful growth and then they go and make it all pointless by getting rid of any player vs player, so it's now just boring farmville. Gotta be the dumbest company i've ever dealt with. They just screwed everyone over who wasted money on this game. Response to developers response..bring back open silver!!!

| | labels |
|---|---|
| gold | `M_PayToProgress` |
| pred | `M_PayToProgress`, `M_PowerCreep` |
| **spurious** | `M_PowerCreep` |

**Model analysis**

```
The reviewer is describing the current state of the game after an update. Two design behaviours come through. First, growth is gated behind payment: 'You have to spend to have any meaningful growth' states that meaningful progression is contingent on spending money, with no free path described — a Pay Wall. Second, the update removed 'open silver' and any player-vs-player play, which the reviewer says made the paid-for growth pointless and 'screwed over' those who spent money; that is an update devaluing purchases players already made, matching how Power Creep treats rebalancing/updates that strip value from acquired investments. The PvP element itself is described only as having been removed, so it is not a currently present mechanic and cannot be coded as Competition under R12. 'Boring farmville' and 'Save your time and money' are evaluations and advice, not mechanics. The term 'open silver' is a removed feature and no label depends on identifying it, so no search is needed.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You have to spend to have any meaningful growth"
  - why: Meaningful progress is stated to be contingent on spending money, with no free alternative described, which is the Pay Wall instance of Pay to Progress.
- `M_PowerCreep` - **SPURIOUS**
  - span: "make it all pointless by getting rid of any player vs player"
  - why: The update removed the game mode that gave paid-for growth its value, so purchases made earlier lose value after acquisition through an update, the devaluation Power Creep describes.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `T_Grinding` | 2 | 2 |
| `T_PlayingByAppointment` | 1 | 2 |
| `S_Competition` | 3 | 0 |
| `M_Gambling` | 2 | 1 |
| `P_RewardMania` | 2 | 1 |
| `M_UIMisdirection` | 2 | 0 |
| `M_DeceptiveLuxury` | 2 | 0 |
| `S_Reciprocity` | 2 | 0 |
| `M_IntermediateCurrency` | 2 | 0 |
| `M_EasyToPurchase` | 0 | 2 |
| `P_IllusionOfControl` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `M_PayToProgress` | 1 | 0 |
| `M_WasteAversion` | 1 | 0 |
| `P_EasyToGetHardToLose` | 1 | 0 |
| `T_MandatoryMarathon` | 1 | 0 |
| `P_AestheticManipulation` | 1 | 0 |
| `M_PowerCreep` | 0 | 1 |
| `S_FriendSpamImpersonation` | 1 | 0 |

