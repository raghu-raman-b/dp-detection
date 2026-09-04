# Error review - deepseek-v4-flash_high_teacher_v3_full

`deepseek-v4-flash` / reasoning `high` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v3_full.txt` sha `a6ae58246360`  
micro-F1 **0.826** (P 0.928 / R 0.744) - **21 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 7 | said NONE, gold had labels |
| SWAP | 2 | picked different labels than gold |
| MISSED ONLY | 9 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 3 | found all gold, added extras |

## The diagnostic that matters

Of **22** missed labels, **4** (18%) were named in the model's own analysis and dropped anyway; **18** (82%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `M_IntermediateCurrency` | 0 | 2 |
| `S_Competition` | 0 | 2 |
| `S_Reciprocity` | 1 | 1 |
| `M_Gambling` | 1 | 1 |
| `T_Grinding` | 1 | 1 |
| `P_RewardMania` | 1 | 1 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `P_AestheticManipulation` | 0 | 1 |
| `M_WasteAversion` | 0 | 1 |
| `M_EasyToPurchase` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `M_PayToProgress` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `S_FriendSpamImpersonation` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `T_MandatoryMarathon` | 0 | 1 |

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
The review is a 10/10 rating followed by a short wishlist of four separate ideas. Item 1 asks for a new bidding/auction marketplace; item 2 asks for an option to be removed so decorations cannot be destroyed; item 3 asks for a convenience widget to view upgrade timers across accounts; item 4 asks for a hidden advanced-statistics screen. Every item is phrased as a request or suggestion ('we would like', imperative 'remove', 'widget that can...', 'hidden option for...'), so none of them describes a game mechanic or design behaviour as currently present in the game. Under R12, requests and hypothetical additions for features do not trigger tags for the proposed mechanics, and none of the spans describes an existing dark pattern such as forced timers, wasting value, or misdirection in the live build.
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
The entire review is a bug report. Every complaint is attributed to crashing, lagging, freezing, unresponsive inputs, and slowness caused by an update. The reviewer asks for these problems to be fixed. Under R11, behaviour attributed to bugs, glitches, or technical faults is not a deliberate dark pattern. No span describes a game rule that imposes a penalty: there is no forfeit of progress tied to an exit rule, no schedule the game forces on the player, and no monetary, social, or psychological mechanic. PvP battles are named only as the context where lag occurs, not as a competitive design the reviewer is criticising, so no design label can be lifted from the mention alone (R4).
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

- `P_EasyToGetHardToLose` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer is praising the game and asking the developers to add a feature that saves progress and in-game purchases so they would not be lost if the game is deleted. The core of the review is a suggestion/request for a future capability (cloud/progress saving). Under R12, requests or hypothetical additions for features that are not described as currently present do not trigger tags for the proposed mechanic. The only other content is the reviewer's stated reluctance to delete the game because that would forfeit purchases and effort — but nothing in the text shows a currently operating design mechanism exploiting that investment against the player; the reviewer loves the game, is not describing being trapped or pressured, and frames the concern as a reason they would like a safety net before spending more. No meso label in the codebook covers a missing cloud-save feature, and assigning from general anxiety about data loss would violate R2.
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
The reviewer reports that after an update they lost the ability to request troops from their clan and asks for it to be fixed. Clan troop requests would ordinarily be a social resource-transfer mechanic (Reciprocity), but the text frames the loss as an update-induced malfunction, not as a deliberate game design. Under R11, behaviour attributed to a bug or technical fault is not a dark pattern, since these patterns are deliberate design choices rather than technical malfunctions.
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
The review opens with generic praise ('addictive', 'upgrades are okay') that describes no mechanic. The body contains two feature suggestions. First, the reviewer asks for an in-app way to trade stickers 'because everybody is not on Facebook', which implies current sticker trading runs through Facebook but does not describe any sending, posting, or exchange happening in-game, and the requested in-app trading feature does not exist yet. Second, the reviewer states an opinion that a purchased booster should be usable when another player challenges them, implying that under current rules it cannot be; this is a wish about how a rule should work, not a demonstration of a realised loss, a payment-for-progress gate, or a manipulative design. Under R12, requests and hypothetical additions for features do not trigger tags for the proposed mechanics, and none of the implicitly referenced existing behaviours (stickers, Facebook trading, boosters, challenges) is described in a way that matches any dark-pattern label.
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
The review's central complaint is that the game's advertising presents physics puzzles as the whole game, when the actual product is a deep strategy game with occasional puzzles. Advertising placed outside the installed game is out of scope under R13, so the misleading-ads point codes nothing. Within the game, the reviewer names strategy activities - making an army, training, building, gathering resources - and characterises reaching the occasional puzzle as 'doing chores.' None of this names a concrete mechanism that matches a label: there is no described schedule, payment, social manipulation, psychological trick, or technical deception. 'Doing chores' is a general evaluation of the path to puzzles, not a description of a specific repeated task cycle tied to progress in a way Grinding requires, and the named strategy activities are presented neutrally as what fans of the genre would enjoy.
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
The reviewer complains that progress resets across sessions: leaving with a full bag and returning finds it empty, and both earned and purchased coins are gone or consumed. The complaint centers on the loss of holdings after exiting and re-entering. Although purchased coins are mentioned, the reviewer is not describing how purchases or currency exchange work; the purchase detail only states the value of what was lost. Nothing in the text identifies a deliberate game rule that imposes the loss—no penalty for quitting, no streak reset, no inventory overflow, no designed forfeiture. The described behaviour reads as a save-state or technical failure rather than a designed dark pattern, so under R11 no mechanical label is warranted.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (2)

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
The reviewer is a long-term player at level 8416 describing why they are quitting. Three design behaviours are present. First, the lives system: they run out of lives several times a day while trying to beat levels, which means sessions are cut short and play must resume only after lives regenerate on the game's clock. Second, progress difficulty: levels take days to beat and the reviewer states outright that buying add-ons is required to get through 'with a sane mind', and that the free path is a 'pure time waste' — progress is gated behind payment or excessive time. Third, they sum up time and money already spent as 'wasted' while uninstalling, which describes sunken cost but does not show that investment operating to keep them playing — they are leaving. The review names no currency conversion, no chance mechanics, no ads inside play, and no social features.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying."
  - why: The reviewer states progress is unmanageable without buying add-ons and that the unpaid route merely wastes time, so payment is presented as the dependable way through a roadblock.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "I run out of lives 3-4 times daily to beat every alternate level"
  - why: Running out of lives means play stops until the lives recharge on the game's timer, so sessions are gated by the game's regeneration schedule rather than the player's choice.

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
The reviewer describes the sticker-album loop of a Monopoly Go-style game. They are two cards short of a grand-prize album completion and that goal is what motivates the purchase they describe: an in-app deal bought with real money. The deal's card delivery is chance-based — the review's harm is that it returned useless duplicates rather than the two new cards needed. Warnings against in-app purchases and the mention of promotion through 'Free Cash' are evaluative and out-of-game marketing, which code NONE under R2 and R13. The mechanics present in the span are: a collection-completion goal driving behavior, real money staked on a randomized reward delivery, and duplicate drops from that randomized pool.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "i bought a deal which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: Real money (an in-app purchase) is staked on a chance-based reward: which cards the purchased deal yields is luck, and the outcome was duplicates rather than the needed cards.
- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards"
  - why: The player is two cards from finishing an album set and the near-complete collection is what drives them to purchase, so the album-completion goal is operating on their behavior.
- `P_RewardMania` - ok
  - span: "all i got were useless duplicates!"
  - why: The span shows duplicate drops from a randomised card pool, the variable delivery schedule that sustains repeated pursuit of the missing cards.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (9)

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
The reviewer alleges a causal manipulation: once they started buying Poké Balls with (presumably) real money, Pokémon began breaking out of captures more often, which consumes balls faster and forces further purchases. This is not a description of paywalls, timers, ads, currencies, or social mechanics; it is an assertion that the game secretly alters outcome determination (capture success) in response to purchases in order to drive spending. The appended edit disavowing authorship does not describe any mechanic and does not change what the main body claims about the game's design. The claim matches the alleged-rigging arm of Illusion of Control, which covers spans asserting concealed manipulation of outcomes rather than just an unlucky run.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: The player asserts that capture outcomes were manipulated once they began paying, increasing ball consumption to force more purchases — a claim of concealed manipulation of how results are determined, not merely a bad run.

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

- `M_Gambling` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer is describing a session of MONOPOLY GO! after a season change and venting frustration across several mechanics. The friend-invite sentence names a recruitment design: the game ties rewards to the player inviting friends and getting them to join via Facebook; the complaint is that the reward has stopped since the new season, but the mechanic being described is the friend-invitation incentive itself. The dice sentence reports a bad run of chance events: playing at max bet and getting no shutdowns or bank heists. That is a losing run with no claim that outcomes are rigged, so it does not carry Illusion of Control, and no money is mentioned so it is not Gambling. The sticker sentence describes the randomized sticker-pack delivery: the reviewer keeps receiving duplicates instead of new cards, which is the duplicate-drop delivery experience of a randomised reward pool. The final sentences are a connection/login failure attributed to a technical fault, which R11 treats as a malfunction rather than a deliberate design pattern.
```

**Labels assigned**

- `P_RewardMania` - ok
  - span: "Stickers are duplicates all the way..."
  - why: The span describes how sticker rewards are delivered - repeated duplicates from the randomized sticker packs - rather than their value, which is the Variable Rewards arm of the definition.
- `S_ForcedFellowship` - ok
  - span: "Suddenly I get no rewards for inviting friends and getting them to join facebook."
  - why: The game is described as rewarding the player for bringing friends into the game through Facebook, which is the friend-invitation incentive regardless of the reviewer complaining that the reward stopped this season.

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
The reviewer is describing a design behaviour in the 1v1 matchmaking screen: every time the screen opens, the interface itself moves the cursor/selection onto the highest-stakes table the player can afford, instead of leaving the choice neutral or on a low-stakes table. The reviewer names this as a deliberate 'Dark UX' trick whose purpose is to make players accidentally tap and stake coins they did not intend to, so that after losing them they are pushed toward buying coins with real money. The described mechanism is entirely an interface manipulation: auto-scrolling, pre-selection, and a costly default the player must actively undo. The real-money outcome ('forced to buy real ones') is stated as the intended purpose of the interface behaviour, not as a separately described purchase flow, so the monetary lift is carried by the same UI mechanism.
```

**Labels assigned**

- `M_UIMisdirection` - ok
  - span: "Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins and are forced to buy real ones."
  - why: The interface is purposefully designed to steer the player's action onto a costly selected option against their intent, requiring an active opt-out, and the review explicitly states the purpose is to deplete coins and drive real-money top-ups.

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
The reviewer describes a change to the game's daily reward system: previously obtainable daily rewards are now gated behind a 50,000 wager, the free 'timed rewards' only yield up to 40,000, and the resulting shortfall can only be bridged by paying, which the reviewer refuses to do and so is quitting. The named and central mechanic is a daily task/reward system that the player must complete to obtain the day's reward, and failing or being unable to complete it forfeits the reward opportunity. The reviewer also draws the free-vs-paid contrast explicitly, implying the design routes completion of the daily rewards through payment because the free path cannot reach the threshold.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "The most I can seem to get on the timed rewards is 40,000. I'd not pay just to get my daily rewards."
  - why: The reviewer contrasts the free route (timed rewards capping at 40,000) with paying to get the daily rewards, showing the free path falls short of the 50,000 threshold so completion is only smooth when payment is involved.
- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The daily reward is framed as a task (betting 50,000) that must be completed each cycle to obtain the reward, and being unable to complete it forfeits that day's reward opportunity, which is the daily-incentive-with-consequence structure.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `cc714d17-863c-4ebd-b14f-989ba17c71c4` - Dice Dreams™️

> I played this game on a different profile. the only reason I gave it five stars is because if you don't it won't let you write a review. if you want to win anything on this game it will cost hundreds of dollars. on the stickers you will never get the last one or two unless you pay a lot of money to get them. this is not a game you want to get addicted to unless you have a endless bank account. it may let you complete a goal maybe one out of hundred times.dont get your hopes up.

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury`, `M_PayToProgress`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_DeceptiveLuxury`, `M_PayToProgress`, `P_CompleteTheCollection` |
| **missed** | `P_RewardMania` |

**Did the model consider what it missed?**

- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review is about sticker-album collection and event progression in Dice Dreams. Three connected mechanics emerge. First, winning or completing anything meaningful is presented as contingent on large payments: winning 'anything' costs hundreds of dollars, and the last one or two stickers only arrive if you pay. That is progress gated behind money. Second, the sticker album is a completion set whose final pieces are withheld, so the player is held in the collection loop by the missing items. Third, the last stickers are described as never obtainable through normal play and only through payment, which describes an intentionally scarce set with a paid remedy sold to get around the scarcity. The statement about giving five stars only to be allowed to write the review concerns the app-store rating surface, which is outside the game application and not coded. The addiction warning is an evaluation rather than a mechanic description. No web search is needed because 'stickers' and 'goals' in this board-game context are self-explanatory collectible and event terms.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: The final stickers are said never to drop naturally, so their scarcity is built into the design and a paid route is offered to obtain them anyway, compelling an extra outlay for scarce items.
- `M_PayToProgress` - ok
  - span: "if you want to win anything on this game it will cost hundreds of dollars. on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: Winning and completing the sticker set are stated to be unavailable without large payments, so further progress is contingent on spending money.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: The sticker album is a completion set and the withheld final pieces are what keep the player engaged and paying, which is the collection-compulsion pattern.

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
At level 34 the reviewer is blocked by storage pressure: their board has 63 spots plus a 37-slot refrigerator, and 72 of the 98 total spaces are occupied by generator parts, lower generators awaiting merges, and high-value cooked items they refuse to delete. A single lambchop can consume 9 of their remaining 26 working slots. The concrete shortfall means they cannot keep merging/playing unless they spend real money for more parts/capacity. The mechanic described is the capped-inventory monetisation pressure, where continuing to hold items costs either paid slot expansion or sacrificing valuable items.
```

**Labels assigned**

- `M_WasteAversion` - ok
  - span: "Not enough slots to store and play without spending $$ to buy parts. I have 63 spots, on the board and 37 spots in the refrigerator. 98 spaces total, 72 are taken up by parts of generators or lower generators that I can't merge with higher generators yet or high level items like a corn that I am not going to delete."
  - why: The span demonstrates a realised capacity shortfall: 72 of 98 slots are occupied by mergeable generator parts and high-value kept items, so further play requires either paid inventory expansion or destroying items the player refuses to delete.

**Search:** `Merge Cooking refrigerator board slots buying parts` -> The search confirmed that in Merge Cooking 'parts' are mergeable item components used to build generators on the board/refrigerator, not separate storage slots; this supported reading the reviewer as having board space occupied by mergeable parts they cannot clear without buying more of them or more capacity.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `12267c1e-47ba-4984-97c8-768e820ceb1c` - Bingo Blitz™️ - Bingo Games

> not very user-friendly. no apparent reachable goals within a decent amount of time. I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| pred | `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| **missed** | `M_EasyToPurchase` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a collection-completion loop in Bingo Blitz. They play game rounds repeatedly to gather photos, which are parts of collectible sets. After losing a round, the game offers to spend extra coins to claim a specific missing photo needed to finish a set. The reviewer accepts that offer, spends the coins, and reports that the promised photo never arrives, even though they then play several more rounds. Overall they conclude they have wasted money. The repeated round-after-round play tied to collecting photos is a grinding loop; working to complete photo sets is a collection-completion mechanic; and the offer that promises a photo but supposedly does not deliver it is a misleading in-game prompt.
```

**Labels assigned**

- `P_AestheticManipulation` - ok
  - span: "I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED"
  - why: The in-game offer is worded as if paying coins will yield the promised missing photo, but the reviewer reports the reward repeatedly does not arrive, making the prompt's claim deceptive rather than merely a bad deal.
- `P_CompleteTheCollection` - ok
  - span: "to claim a photo I don't have to complete the set"
  - why: The goal the player pursues is completing a set of photos, and the offer specifically targets the single missing item in that collection, an exploitation of the urge to complete sets.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The player names the repeated activity (playing rounds over and over) and ties it to progress through the game (collecting photos), which is repetitive tasking for advancement.

**Search:** `Bingo Blitz offer after losing a round spend coins to claim a photo to complete collection` -> Bingo Blitz presents an offer after a losing round to spend coins on a collection tool that is meant to let the player claim a missing photo and complete the set. The review describes this offer and its failure to deliver.

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
The reviewer is describing MONOPOLY GO!'s sticker album system. Three design behaviours are present. First, the sticker packs deliver duplicates ('always get duplicates'): the player keeps engaging with a random delivery system that produces repeated unwanted copies, which is a chance-based delivery outcome rather than a complaint about reward size. Second, the player is trying to complete sticker sets and frames the inability to finish them as the frustration ('never lets you finish all the sets'), which is collection-completion pressure. Third, finishing the sets is stated to be contingent on payment ('unless you pay'), which makes payment the gate to that goal. The review is short but each clause names a distinct mechanic.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: Completing the sticker sets is stated to be unavailable without payment, which is the pay wall instance of Pay to Progress.
- `P_CompleteTheCollection` - ok
  - span: "never lets you finish all the sets"
  - why: The player is working toward completing all the sticker sets and frames not being able to finish the collection as the harm.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: Duplicates from the sticker packs describe how the randomised reward system delivers repeated unwanted copies, which sustains the chase rather than the reward's value.

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

- `P_RewardMania` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer is talking about Genshin Impact's update cadence and its consequence for their account. They name three things: reward payouts shrinking patch over patch; a fast-moving meta that makes previously sufficient characters inadequate, so the player feels compelled to pull new characters to keep dealing damage; and a slide toward pay-to-win, plus a separate quality complaint about a quest background image. The reward shrink is only about the amount of reward, not its delivery mechanism, so it does not sustain Reward Mania on its own. The meta shift is the core mechanic: content updates are described as devaluing what the player already has and forcing new purchases/pulls to stay effective. The 'pay 2 win' statement explicitly names paid advantage. The background-art complaint is an aesthetic quality evaluation and codes NONE.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "the game is getting more and more pay 2 win"
  - why: The reviewer explicitly states the game increasingly grants advantages to players who spend money, which is the Pay to Win instance.
- `M_PowerCreep` - ok
  - span: "the Meta changes more and more every single day basically forcing us to pull for new characters if we want to actually do damage"
  - why: Rapid meta shifts mean the characters the player already acquired no longer suffice and new pulls are required to keep doing damage, so existing purchases lose value over time through updates, driving new spending.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (3)

### `95ddadb3-82cd-4042-8a51-cf8b3ed164c2` - Mech Arena - Shooting Game

> You stuck waiting 30 seconds just to connect to a match. This game makes it seem like they give so many rewards but if all just for show. Its difficult to get weapon upgrades or any percs others you stick battling to win. This kind of games just rob you of your time in my opinion

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `T_Grinding` |
| **spurious** | `T_Grinding` |

**Model analysis**

```
The review is mostly a general complaint about time being wasted. The 30-second matchmaking wait is a service/queue time, which the codebook explicitly excludes from Playing by Appointment. The claim that rewards are 'all just for show' is a complaint about reward value, not about the delivery mechanism (no unpredictability, complexity, or collection pressure is described), so Reward Mania does not apply. The only concrete design behaviour described is that weapon upgrades and perks are difficult to obtain and the player must keep battling to win them, which is progression tied to sustained, repeated play. No payment, social, or collection mechanics are mentioned.
```

**Labels assigned**

- `T_Grinding` - **SPURIOUS**
  - span: "Its difficult to get weapon upgrades or any percs others you stick battling to win"
  - why: The span names continued battling ('stick battling to win') as the required route to weapon upgrades and perks, so progress is gated behind sustained repeated play rather than merely described as slow.

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
The reviewer describes four separate design behaviours after ten days of play. First, they name the monetisation model directly as pay-to-win. Second, base upgrade times growing to 'ridiculous' lengths is a build-timer gate: the player must wait on the game's clock to advance. Third, endless scaling of upgrade requirements with nothing to look forward to beyond more of the same work describes both an unattainable end state (treadmill) and the repetitive grind the path consists of. Fourth, they attribute the confusing, overwhelming interface to a deliberate purpose of pushing purchases, which is the interface working against the player's intent rather than a mere quality complaint. Finally, the alliance system is described as leaving players who do not join exposed to being attacked and bullied by other players, which pits players against each other in PvP; no reward or advantage flowing to the aggressor is described, so the stronger Encourages Anti-Social Behavior reading is not supported. No term in the review needs an external lookup.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "it's set up in a pay to win way"
  - why: The reviewer explicitly names the model as pay-to-win, meaning paying grants an advantage over non-payers.
- `M_UIMisdirection` - ok
  - span: "The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff"
  - why: The interface is described as intentionally confusing and overwhelming in order to steer the player into buying, which is UI serving a manipulative purpose rather than a quality flaw.
- `S_Competition` - ok
  - span: "If you are not in one then you get attacked and bullied"
  - why: The game sets players against each other: those outside an alliance are preyed on by other players in PvP, so competition is the mechanic being described.
- `T_Grinding` - **SPURIOUS**
  - span: "just more grind"
  - why: The reviewer names the repetitive task work that endless scaling requires as the only thing awaiting them, tying grind to progression.
- `T_InfiniteTreadmill` - ok
  - span: "Everything scales endlessly, there is kinda no point to look forward to"
  - why: Endless scaling with nothing ahead to aim for means the game continually extends beyond any possible completion.
- `T_PlayingByAppointment` - ok
  - span: "the update times for your base are becoming ridiculous"
  - why: Base upgrade/build timers force the player to wait on in-game timers, so play happens on the game's schedule rather than the player's.

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
The review is a long-tenure player's complaint about the game's economy and quality. The 7-hour quest returning few primogems is a statement about reward value relative to effort, not about how rewards are delivered. 'Exploration is debilitating' is a qualitative evaluation, not a repeatable activity tied to progress. The character-design complaint is aesthetic taste, not the game using aesthetics to steer behaviour. 'There is no resin overflow system' names a system I cannot fully interpret from the review alone; in Genshin, resin is the energy resource that regenerates in real time up to a hard cap, and without overflow the regen timer stalls while the player is at cap, forcing them to spend resin on the game's schedule to avoid forfeiting regeneration. That makes the missing overflow an implicit complaint about the game's appointment-based energy cycle, which is a present design behaviour rather than a purely hypothetical feature.
```

**Labels assigned**

- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "there is no resin overflow system"
  - why: Resin is an energy resource that refills on a real-time timer up to a cap; the absence of overflow means regeneration is forfeited if the player does not log in and spend on the game's schedule, which is the wait-to-play instance of the pattern.

**Search:** `what is resin and resin overflow system in Genshin Impact` -> Resin is Genshin Impact's energy resource that regenerates over time up to a cap of 200; an overflow system is not implemented, so regeneration stops once the cap is reached.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `T_Grinding` | 2 | 2 |
| `T_PlayingByAppointment` | 1 | 2 |
| `M_Gambling` | 2 | 1 |
| `M_IntermediateCurrency` | 2 | 0 |
| `S_Competition` | 2 | 0 |
| `S_Reciprocity` | 2 | 0 |
| `P_RewardMania` | 2 | 0 |
| `P_EasyToGetHardToLose` | 1 | 0 |
| `P_AestheticManipulation` | 1 | 0 |
| `M_WasteAversion` | 1 | 0 |
| `M_EasyToPurchase` | 1 | 0 |
| `M_PayToProgress` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `S_FriendSpamImpersonation` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `T_MandatoryMarathon` | 1 | 0 |

