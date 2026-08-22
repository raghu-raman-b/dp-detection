# Error review - claude-sonnet-5_high_teacher_v2_full

`claude-sonnet-5` / reasoning `high` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `6529a474a2b0`  
micro-F1 **0.802** (P 0.827 / R 0.779) - **22 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 5 | said NONE, gold had labels |
| SWAP | 6 | picked different labels than gold |
| MISSED ONLY | 5 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 6 | found all gold, added extras |

## The diagnostic that matters

Of **19** missed labels, **7** (37%) were named in the model's own analysis and dropped anyway; **12** (63%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `S_Competition` | 1 | 2 |
| `P_AestheticManipulation` | 0 | 2 |
| `S_Reciprocity` | 1 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `M_IntermediateCurrency` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `T_Grinding` | 1 | 0 |
| `P_IllusionOfControl` | 1 | 0 |
| `M_Gambling` | 1 | 0 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `T_MandatoryMarathon` | 1 | 0 |
| `P_RewardMania` | 0 | 1 |
| `M_WasteAversion` | 0 | 1 |
| `M_RecurringFee` | 1 | 0 |
| `S_FriendSpamImpersonation` | 0 | 1 |

## Missed everything (predicted NONE) (5)

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
The entire review is a wishlist of four feature requests the player would like added to the game: bidding/auction system for cosmetics, removing an option tied to obstacle-to-decoration conversion, a multi-account widget, and a hidden advanced-stats screen. Per R12, requests, suggestions, or hypothetical additions do not trigger tags for the proposed mechanics themselves, and the review does not describe any existing, currently-active dark pattern mechanic alongside these suggestions -- there is no mention of payment, waiting, grinding, social pressure, or any other codable behaviour the reviewer is currently experiencing in the game. The '10/10' opening is a rating/tone statement (R2) and carries no mechanic. None of the four numbered items describe a mechanic that presently exists in the game; they are all hypothetical additions the reviewer wants implemented. Therefore no label from the codebook applies.
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
The review is an enumerated bug report following an update: gifts and trading crash, throwing pokeballs lags, PvP and Team Rocket battles lag with slow switching, charge attacks fail to respond, and the game freezes while the opponent continues attacking. Every complaint is explicitly attributed to technical malfunction (bugs, crashing, lagging, freezing) rather than to a deliberate game rule or design choice. Under R11, behavior attributed to a bug, glitch, or technical fault is not a dark pattern, and no functional design rule is described as imposing a penalty independent of the malfunction (e.g., the freeze during opponent attacks is presented as a freezing/crashing issue, not a stated design rule that a session-exit or loss condition triggers on freeze). There is no mention of monetary mechanics, schedules, social mechanics, or reward systems here at all, only a request to fix technical problems. R2 and R11 together mean no meso label applies.
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
The reviewer reports that a specific in-game function, requesting troops from their clan, stopped working after an update, and asks for it to be fixed. This is framed entirely as a technical malfunction ('Since 1 of the updates I can no longer... It needs to be fixed'), not as a deliberate design choice or dark pattern. While troop requesting could relate to a resource-donation/reciprocity mechanic in other contexts, here the reviewer is not describing an obligation to reciprocate, a donation mechanic, or any social pressure design; they are simply reporting that a feature broke and want it restored. Per R11, behavior explicitly attributed to a bug or update-caused error is not coded as a dark pattern unless the underlying game rule (not the bug) itself imposes a penalty, which is not the case here since no penalty or design rule is described, only a broken feature.
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
The reviewer opens with general praise ('very addictive', 'upgrades are okay') which under R2 is tone/evaluation and not codable on its own. The first substantive point is a request: 'I think you should have a way to trade sticker with players in the game within the app because everybody is not on Facebook.' This is phrased as a feature the reviewer wishes existed ('you should have a way'), not a mechanic currently operating in the game; under R12, requests or hypothetical additions are not coded, even when they reference an existing constraint (needing Facebook) in passing. There is no description of the game actually sending messages, posting, or using the contact list on the player's behalf, so Friend Spam/Impersonation's messaging requirement is not met either. The second point, 'I believe if i purchase a booster i should be able to use it if another player challenge me to a game,' is also framed as a wish ('I believe... should be able to'), implying a current restriction on using a purchased booster when challenged, but this is presented as a suggestion for a rule change rather than a described dark-pattern mechanic (no pay-to-progress gate, no artificial friction being sold as removed, no scarcity or currency conversion described). Neither passage names or implies an operating mechanic that matches any of the 29 labels' indicators or boundary rules; both are forward-looking requests rather than accounts of present game behavior. Per R2 and R12, no label applies.
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
The review's central complaint is that the game's advertisements misrepresent it as a puzzle game when it is actually a strategy game. Per R13, developer advertising in third-party apps and marketing material is outside the coding unit, even where the behaviour (misrepresented gameplay) would otherwise satisfy a label. So the ad-related content cannot be coded. What remains is the reviewer's description of the actual gameplay: 'making an army from scratch, training, building, gathering resources' and the closing remark that reaching the advertised puzzles requires 'doing chores.' This is a general, genre-level characterization of the game as a resource/army-building strategy title rather than a description of a specific repetitive task tied to progress (no named repeated activity like replaying a level or farming a specific resource is identified as tedious or blocking advancement). Under the Grinding boundary rule, a general characterization of gameplay as chore-like or repetitive without naming the repeated activity and its link to progress does not rise to the level of Grinding; it reads as an evaluation of the game's genre/pace. No monetary, temporal-mechanic, social, psychological, or technical pattern is described with a concrete in-game mechanism (no currency, no timers, no purchase prompts, no social recruitment, no reward delivery system, no scarcity item). Therefore no codable label applies, and the review resolves to NONE per R2/R6.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (6)

### `0bc09fc3-6436-4a24-855e-0fdc56887918` - Fishdom

> EDIT 1/17/2023: Customer Service can't make good on 9 diamonds when game element doesn't appear within 5 original moves and 5 additional moves. It is a fun game, you don't have to pay to win. I suggest after this cust. svc experience that you don't buy from this game beyond the pass.Get friends and a team and trade lives.

| | labels |
|---|---|
| gold | `M_RecurringFee`, `S_Reciprocity` |
| pred | `M_PayToProgress`, `S_Reciprocity` |
| **missed** | `M_RecurringFee` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_RecurringFee` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review centers on a customer-service dispute over a specific Fishdom mechanic: the reviewer spent 9 diamonds (the game's premium currency) to buy additional moves ('5 additional moves' beyond the '5 original moves') hoping a particular game element would appear, and it did not, with customer service refusing to compensate the diamonds. This describes a real design mechanic, not a malfunction: diamonds are spent to bypass the move-limit obstacle in order to keep attempting to obtain the item, which is a Pay-to-Skip instance of Pay to Progress. The reviewer explicitly denies pay-to-win is required ('you don't have to pay to win'), which is a disclaimer, not a mechanic to code. The mention of 'the pass' is a bare reference with no described schedule, clock, or forfeiture attached, so it does not meet the Recurring Fee or Playing by Appointment bars on its own. Finally, the closing advice 'Get friends and a team and trade lives' names an explicit resource-transfer mechanism (trading lives) with existing teammates, which is the Reciprocity pattern; there is no description of recruiting new players into the game itself, so Forced Fellowship is not supported.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "Customer Service can't make good on 9 diamonds when game element doesn't appear within 5 original moves and 5 additional moves"
  - why: Diamonds were spent to purchase additional moves beyond the level's built-in move limit in order to keep attempting to obtain a needed item, which is paying to bypass an obstacle that directly blocks continued progress.
- `S_Reciprocity` - ok
  - span: "Get friends and a team and trade lives"
  - why: Names an explicit resource-transfer mechanism, trading lives with teammates, which instills the obligation-to-reciprocate pattern with players already in the game.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fd1230ab-7d12-4aeb-a425-e37ed06bcd5c` - Pokémon GO

> I love this game, just started playing about 2 months ago. Though I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way. I feel taken advantage of. 3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| pred | `M_PayToProgress`, `P_IllusionOfControl` |
| **missed** | `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**
- `S_FriendSpamImpersonation` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a specific pay mechanic tied to Pokémon GO's core capture loop: after they began purchasing Poké Balls, they noticed captures 'breaking out' more often, which burns through their ball supply faster and pushes them to buy more balls. Two things are being described together. First, the consumable resource (Poké Balls) is positioned as something the player must keep buying to keep playing/catching, i.e., purchase is framed as necessary to keep the capture loop going. Second, and more pointedly, the reviewer alleges a causal link between purchasing and worsened outcomes (higher break-out rates), i.e., a claim that the game's determination of catch success is being manipulated in a way that incentivizes continued spending rather than being a fair/random mechanic — this is a claim about the game concealing or tuning outcomes against the player, which the reviewer frames as feeling exploited ('I feel taken advantage of'). This is not simply an unlucky streak; the reviewer explicitly ties the pattern to the act of purchasing and corroborates it with other players' experiences (in the original text). The final edited addendum about not having written the review or spoken to other players is an account/authorship dispute, not a game mechanic, and is not codable. There is no explicit real-money-to-virtual-currency conversion described (no mention of PokeCoins), so Intermediate Currency is not supported by the text as written. No wager or chance-based delivery system beyond the capture mechanic itself is described, so Gambling and Reward Mania do not apply. No collection, social, temporal, or UI-based mechanic is described.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: The capture loop consumes the purchased balls faster than expected, pushing the player into a repeated cycle of buying more balls just to continue catching Pokémon, i.e., payment is required to keep progressing through the core loop.
- `P_IllusionOfControl` - ok
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster"
  - why: The reviewer alleges that capture success rates worsened specifically after they began paying, implying the game manipulates catch odds around purchase behavior to drive further spending, corroborated by their statement of feeling 'taken advantage of.'

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fdef27f2-9a21-4b8e-a04c-7a4753e0fb07` - 8 Ball Pool

> The game is great, but the user interface is completely rigged. Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins and are forced to buy real ones. ​We need a "Default Table Lock" or the game should always open the lowest bet table by default, not the highest! Fix this scammy feature. Giving 1 star

| | labels |
|---|---|
| gold | `M_Gambling`, `M_IntermediateCurrency`, `M_UIMisdirection` |
| pred | `M_EasyToPurchase`, `M_IntermediateCurrency`, `M_UIMisdirection` |
| **missed** | `M_Gambling` |
| **spurious** | `M_EasyToPurchase` |

**Did the model consider what it missed?**

- `M_Gambling` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes a specific UI behavior in 8 Ball Pool's table-selection screen: opening the game or the 1v1 menu causes the interface to automatically scroll to and select the highest-stake table available for the player's coin balance. The reviewer explicitly frames this as a manipulative default that causes 'accidental mis-clicks,' i.e., a mis-tap on the auto-selected high-bet option rather than a deliberately chosen low-stake table. This matches the UI Misdirection pattern where placement/default routing causes a mis-tap to select an unintended, costly option, and it also matches the Accidental Purchases/Low Barrier pattern of Easy to Purchase, where a default option (rather than an explicit opt-in) results in unintended spending with no confirmation step. The consequence described is loss of the player's accumulated coins, and the reviewer states this then forces players to 'buy real ones,' i.e., spend real money to replenish the in-game coin currency — this is the money-to-virtual-currency conversion described by Intermediate Currency. The review does not describe a gambling wager (no chance mechanic named beyond the bet-table selection itself as a UI trap), nor does it describe grinding, dailies, or social mechanics, so those classes are not implicated.
```

**Labels assigned**

- `M_EasyToPurchase` - **SPURIOUS**
  - span: "force accidental mis-clicks so players lose all their hard-earned coins"
  - why: A default option (the auto-selected high-bet table) is used to induce unintended spending of the player's coins with no confirmation step, matching the Accidental Purchases indicator of reducing friction/deliberation before spend.
- `M_IntermediateCurrency` - ok
  - span: "are forced to buy real ones"
  - why: The span describes coins as the object being purchased with real money after they are lost, which is the money-to-virtual-currency conversion direction that defines Intermediate Currency.
- `M_UIMisdirection` - ok
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks"
  - why: The interface defaults attention and selection onto the highest-cost option so that a normal tap lands on the costly choice rather than the player's intended one, matching the 'mis-tap selects the opposite action' boundary for UI Misdirection.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `176aaa1f-d8f9-4a1a-9f29-64902f13be5c` - All in Hole: Black Hole Games

> I would give 5 stars, but I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used.🤨😒🙄😥

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `T_MandatoryMarathon` |
| pred | `M_WasteAversion` |
| **missed** | `M_IntermediateCurrency`, `T_MandatoryMarathon` |
| **spurious** | `M_WasteAversion` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**
- `T_MandatoryMarathon` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer's core complaint is a between-session loss of accumulated holdings: they close the game with their 'bag' (an in-game storage/inventory) full, and when they return the bag is empty, with coins they had both earned through play and purchased with real money already 'used' up. No bug, crash, or error is named, so R11 does not apply; the reviewer is describing what reads as a designed consequence of returning to the game rather than a malfunction. The pattern most directly matches Waste Aversion's boundary rule, which explicitly covers 'lost holdings due to inventory limits' as a form of realized, stranded/forfeited value: a full bag (implying a capacity cap) that empties itself, and coins (both earned and paid-for) that are consumed without the player's own spending action, are both instances of value the player held but could not retain or use, matching the darkpattern.games alt-definition of capped inventory forcing loss and leftover/unusable premium currency. This is not a case of being trapped in an active session and forced to forfeit progress on exit (Mandatory Marathon), since the reviewer describes ordinary leaving and returning, not being prevented from stopping a session; nor is it reluctance to abandon investment (Easy to Get, Hard to Lose), since the loss is described as already realized rather than as a psychological pull to keep playing. The single sentence therefore best supports one label: Waste Aversion, covering both the emptied bag and the consumed coins as forfeited value.
```

**Labels assigned**

- `M_WasteAversion` - **SPURIOUS**
  - span: "I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used"
  - why: The bag reaching full and then being found empty on return shows realized, forfeited value tied to an inventory cap, and the earned-and-purchased coins being 'used' up without the player's own action shows currency the player held but could not retain, both matching Waste Aversion's requirement of demonstrated stranded or forfeited value.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `12267c1e-47ba-4984-97c8-768e820ceb1c` - Bingo Blitz™️ - Bingo Games

> not very user-friendly. no apparent reachable goals within a decent amount of time. I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| pred | `M_EasyToPurchase`, `M_Gambling`, `M_PayToProgress`, `P_CompleteTheCollection`, `T_Grinding` |
| **missed** | `P_AestheticManipulation` |
| **spurious** | `M_Gambling`, `M_PayToProgress` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a photo-collection mechanic layered on top of the core bingo gameplay: they play round after round specifically to collect 'photos' toward completing a set, which is a named collection-completion goal. When a round is lost, the game inserts a purchase prompt asking the player to spend coins to claim a missing photo needed for the set, an interception of the natural play flow with a monetized offer. The reviewer paid coins on this offer repeatedly but reports receiving other rewards (bingos) instead of the specific promised photo, and states this has happened to them 'so many times I can't even count' - framing it as a systemic, repeated outcome rather than a one-off technical glitch, which supports reading it as the game's variable/uncertain reward delivery on a paid offer rather than a bug under R11. The closing line about having 'wasted so much money' ties real-world spending to this coin-based offer loop, though the text never explicitly states the money-to-coin conversion, so Intermediate Currency is not confidently supported. The opening complaint about 'no apparent reachable goals' is a general quality evaluation without a named mechanic and does not meet R2's threshold on its own.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "after each round that I lose it will ask me if I want to spend extra coins to claim a photo"
  - why: A spend prompt is triggered at a fixed point in the gameplay loop (immediately after losing a round), intercepting the session to solicit a purchase.
- `M_Gambling` - **SPURIOUS**
  - span: "I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED"
  - why: Despite paying coins for a specific promised photo, the outcome received differs (other bingo rewards), and this occurs repeatedly ('so many times'), implying the payment buys an uncertain chance at the item rather than a guaranteed one.
- `M_PayToProgress` - **SPURIOUS**
  - span: "it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set"
  - why: Payment (in coins) is offered as the route to obtain a specific item needed to advance the collection goal.
- `P_CompleteTheCollection` - ok
  - span: "claim a photo I don't have to complete the set"
  - why: The player is pursuing photos to complete a defined set, matching the compulsion to acquire all items in a collection.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The reviewer names a repeated activity (playing round after round) as the means of advancing the photo-collection goal.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b93c432d-19c0-4c6c-a2d4-bb9b21a436f3` - Dice Dreams™️

> A literal brain-rot game no wonder why they're tryna promote it through Free Cash. Also if you're thinking of making in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates! A real SCAM. Play it if u want but there are games that are actually good also, DON'T GET IN-APP PURCHASES!

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_Gambling`, `M_PayToProgress`, `P_CompleteTheCollection`, `P_RewardMania` |
| **missed** | `P_AestheticManipulation` |
| **spurious** | `M_Gambling`, `M_PayToProgress` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes two things. First, they mention the game is promoted through 'Free Cash', which is an external advertising/rewards platform, i.e., marketing outside the installed app; under R13 this is out of scope regardless of any dark-pattern flavor. Second, and centrally, they describe an in-app purchase made to close out a sticker/card album: they were two cards short of the grand prize for completing the album, so they paid for a 'deal' explicitly promising new cards, but the outcome was random and delivered only duplicates they already had. This is the same structural pattern as the canonical Monopoly Go card-set example: a real-money purchase made specifically to progress toward finishing a collection (Pay to Progress), where the purchased content is delivered through a chance-based mechanism with no guarantee of the needed item (Gambling), the collection-completion drive itself (Complete the Collection), and the unpredictable/duplicate-heavy delivery of the reward (Reward Mania). No leftover-currency shortfall, UI trickery, or social mechanic is described, so no other labels apply.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "i bought a deal which promised i would get NEW cards, and all i got were useless duplicates"
  - why: Real money was spent on a purchase whose outcome (which cards would be received) was governed by chance rather than guaranteed, with the player instead receiving unwanted duplicates.
- `M_PayToProgress` - **SPURIOUS**
  - span: "I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards"
  - why: The player spent real money specifically to obtain the final cards needed to unlock the grand prize, i.e., to progress toward completing the album.
- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The reviewer's entire motivation is finishing a card album/collection, the compulsion the label targets.
- `P_RewardMania` - ok
  - span: "promised i would get NEW cards, and all i got were useless duplicates"
  - why: Describes the delivery mechanism as unpredictable, yielding unwanted duplicate drops from a randomized pool rather than the specific reward sought.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (5)

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
The reviewer describes a bonus wheel feature ('the genie game') inside a slots title. The core complaint is not that rewards are simply random or small, but that the wheel appears to land on a high prize and then the game's 'genie' character moves the pointer further to a different, lower-value segment before the spin resolves, converting a would-be 100 million (5x multiplier) result into 48 million. This is a specific claim that the game intervenes in or manipulates the determination of the outcome after it has ostensibly landed, rather than letting the stopped result stand — i.e., the reviewer is alleging the outcome-determination mechanism is not what it appears to be (a non-random, post-hoc adjustment dressed up as a spin animation). That matches the Illusion of Control pattern's boundary on alleged rigging/manipulation of outcome determination. The final line, asking for a 'player choice to keep or spin,' is a request for a feature that doesn't currently exist, so per R12 it is not itself codable. There is no explicit mention of real money being wagered on this specific feature within the span, so Gambling is not supported here (R4), and no other mechanic (currency conversion, purchase prompts, collection, social features) is described in this text.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "in multiple times whe the wheel spin after stopping on a great price the genie move the wheel to a spin tag, and then the prices after the spin are way lower than the original price, from 100 million with 5x multiplier to a 48 million"
  - why: The reviewer describes the wheel appearing to stop on a large prize, after which the game moves it further to a lower prize, implying the true outcome is manipulated after the fact rather than genuinely determined by the visible stop, which is a claim about concealed/altered outcome determination.

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

- `P_IllusionOfControl` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes a solitaire-style game where progression through numbered levels depends on an in-game economy. Two things are being reported together: first, a general statement that playing without spending real money is unrewarding, using the explicit contrast phrase 'without spending actual money'; second, a concrete illustration of that unrewarding economy — at level 100 the entry cost is 2200 (game currency), and even a win barely returns that amount, meaning the free/earned loop cannot sustain play and pushes the player toward spending. This is the Narrative Obligation shape of Pay to Progress: currency earned in-game trickles back at a rate that barely covers the cost of continuing, so payment becomes the practical way to keep progressing. The 'rng is so obviously against you' line is a bare, mechanism-free accusation of bad luck/unfairness — it doesn't describe a concealed or manipulated outcome-determination system (no fixed ratio, no rigged deal, no hidden schedule named), so per the Illusion of Control boundary rule this reads as an unlucky-run complaint rather than an instance of that pattern, and gets no label. 'The rewards need a big revamp' is an evaluative complaint about reward value, not a description of a delivery mechanism (variable rewards, gacha, complexity), so it does not support Reward Mania either. No currency name, social mechanic, ad, timer, or collection element is described, so no other labels apply.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "it's not rewarding playing the game without spending actual money.. at around level 100 it costs 2200 but if you win the level you'll barely make that back"
  - why: The review explicitly contrasts playing 'without spending actual money' as unrewarding, then illustrates it: the level's currency cost (2200) is barely recovered even by winning, so the earned/free loop cannot sustain play and payment becomes the practical route to progress.

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
The reviewer describes a change to the game's daily reward system in a casino/slots app. The core complaint is that daily rewards are now gated behind a wagering threshold: the player must bet 50,000 (in-game currency, presumably) to complete the daily reward, but the free/timed rewards only ever supply up to 40,000, leaving a 10,000 shortfall that can only be closed by paying real money. Two mechanics are implied here. First, this is a daily reward structure with a resetting task requirement tied to real-world daily cycles ('daily rewards'), where failure to meet the bet threshold means the reward is not completed that day. Second, because the free/earned path (timed rewards, capped at 40,000) falls short of the amount needed to complete the daily task, and the reviewer explicitly refuses to pay to close that gap ('I'd not pay just to get my daily rewards'), the daily reward has effectively become a pay-gated objective: money is the only way to bridge the shortfall to progress/complete it. This fits the Pay to Progress boundary rule about a free alternative falling short of smooth completion, forcing a paid shortcut. There is no clear repetitive-task description beyond the bet volume itself, no currency-conversion span, and no other mechanic named or implied strongly enough to warrant additional labels.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "The most I can seem to get on the timed rewards is 40,000. I'd not pay just to get my daily rewards."
  - why: The free, earned route (timed rewards) is capped below the amount needed (40,000 vs required 50,000), so completing the daily reward requires paying real money to close the gap; the reviewer names this paid alternative and refuses it, showing the free path falls short of completion without payment.
- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: Describes a daily reward system with a completion requirement (a wagering threshold) that must be met each day, and failing to meet it means the daily reward is not obtained, which is the daily-return incentive/penalty pattern.

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

- `S_Competition` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes a resource-grinding loop as the core late-game activity: collecting resources while trying to avoid being raided, in order to level up for more attempts at a mini-game. This is a repetitive, tedious task tied directly to progress, matching Grinding. The reviewer also names alliance combat: bigger alliances attacking smaller ones and taking their resources. This is not framed as symmetric, sanctioned PvP but as an asymmetric power dynamic where stronger groups prey on weaker ones and profit from it, which the boundary rules place under Encourages Anti-Social Behavior rather than ordinary Competition. The line about advertisement is vague and does not describe being forced to watch ads or being rewarded for watching them, nor does it describe an in-game ad mechanic with enough specificity to satisfy the Advertisement label's requirements; it reads as a general quality complaint and is excluded under R2. No payment, currency, scarcity, social recruitment, or reward-delivery mechanics are described, so no monetary or reward-mania labels apply.
```

**Labels assigned**

- `S_EncouragesAntiSocialBehavior` - ok
  - span: "The bigger alliances all just attack the smaller alliances and take their resources."
  - why: The span describes an explicitly asymmetric predatory dynamic where stronger groups attack and plunder weaker ones, gaining resources from the imbalance, which the boundary rule places under this label rather than ordinary Competition.
- `T_Grinding` - ok
  - span: "It's just grinding resources trying not to get raided so you can level up to have a few more attempts at the left right scroller game."
  - why: The reviewer explicitly names the repeated resource-collection loop as 'grinding' and ties it directly to leveling up, i.e., progress, satisfying the repetitive-task-for-progress requirement.

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
The reviewer describes the Monopoly Go sticker collection system. Two things are named: getting duplicate stickers repeatedly ('always get duplicates'), and being unable to complete sticker sets/albums without paying ('never lets you finish all the sets unless you pay'). The duplicates complaint describes the delivery mechanism of the reward pool, unwanted duplicate drops from a randomized pool, rather than the value of the reward itself, which matches Reward Mania. The inability to finish sets without payment is a direct pay-wall on completing a collection, which supports both Pay to Progress (payment required to advance/complete) and Complete the Collection (the compulsion to finish the full set of items is the stated goal being blocked). No monetary stake on a specific chance mechanic is described, so Gambling does not apply. No leftover currency or capacity shortfall is shown, so Waste Aversion does not apply.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: Completing the collection, the stated progress goal, is described as contingent on payment, matching the Pay Wall indicator where further progress requires spending money.
- `P_CompleteTheCollection` - ok
  - span: "never lets you finish all the sets"
  - why: The reviewer frames the goal explicitly as finishing all the sticker sets, and describes the game as preventing that completion, which is the collection compulsion being thwarted.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: Repeatedly receiving duplicate stickers describes the delivery mechanism of a randomized reward pool sustaining engagement/frustration rather than the value of any single sticker, matching the duplicate-drops indicator for Reward Mania.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (6)

### `14e87cfb-665b-4239-863d-2175f401d894` - Clash Royale

> this game is so annoying all you play against after 8k trophies is mega knight,pekka, and golem they need to rebuffed them they are so annoying to play against and when spammed down its annoying to defend this game is not fun for that reason its also pay to win and usually doesn't let you get higher from just using skill you have to go out of your way to be annoying to actually win in a game this game is getting more and more pay to win with each update and they buff cards people hate

| | labels |
|---|---|
| gold | `M_PayToProgress`, `S_Competition` |
| pred | `M_PayToProgress`, `M_PowerCreep`, `S_Competition` |
| **spurious** | `M_PowerCreep` |

**Model analysis**

```
The reviewer is complaining about the ranked ladder meta in Clash Royale. They describe facing the same over-represented, over-strong cards (mega knight, pekka, golem) once past 8k trophies, competitive ladder play against other players. They explicitly label the game 'pay to win,' stating skill alone does not let you climb and framing paying/using annoying strategies as necessary to win. They also state the game is 'getting more and more pay to win with each update' because the developers 'buff cards people hate,' which describes cards being rebalanced upward over time, degrading the relative value/viability of cards the player already has and forcing adaptation to new metas driven by updates. There is no mention of loot boxes, currencies, ads, timers, or social mechanics, so those classes do not apply. The 'skill vs annoying playstyle' complaint is a balance/meta grievance rather than an assertion that the game conceals or manipulates match outcomes/matchmaking, so it does not rise to Illusion of Control.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "its also pay to win"
  - why: The reviewer directly characterizes the game as pay to win, indicating spending money confers a competitive advantage needed to progress on the ladder.
- `M_PowerCreep` - **SPURIOUS**
  - span: "this game is getting more and more pay to win with each update and they buff cards people hate"
  - why: Repeated buffing of specific cards with each update devalues the player's existing card investments and strategies relative to the newly strengthened meta, matching the update-driven devaluation pattern.
- `S_Competition` - ok
  - span: "all you play against after 8k trophies is mega knight,pekka, and golem"
  - why: The trophy-based matchmaking described puts the reviewer directly against other players' decks, which is the game's competitive PvP structure.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `2528f51b-7c4c-4a27-ac30-09bbef267e0f` - Bingo Blitz™️ - Bingo Games

> A very fun game to play, when your bored an looking for something to hype up your engery, an their may be in app purchases in the game but their being very reasonable about the price unlike other games that I play. If your spend $20 on some item you get less then what your actually hoping for, but on here bingo gives you twice the number of your purchase, an has very different modes an events to get into... what Im saying is... try this game an give it try an see if you like it 😁

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `M_IntermediateCurrency` |
| **spurious** | `M_IntermediateCurrency` |

**Model analysis**

```
The review is overwhelmingly positive and describes the game's in-app purchase pricing as reasonable. The key mechanic described is a purchase mechanic: the reviewer contrasts spending $20 on 'some item' in other games (getting less than hoped for) with this game, where a purchase yields 'twice the number' of whatever was bought. This describes real money being converted into an in-game quantity (coins, credits, or similar) with a bonus multiplier applied, which is the real-money-to-virtual-currency conversion at the heart of Intermediate Currency, even though the reviewer frames it favorably (R7/R8 require coding the mechanic regardless of the reviewer's positive evaluation). The remainder of the review ('very different modes an events to get into') names game content generically without describing any specific mechanic (schedule, reward structure, competition, etc.), so it does not support any codebook label on its own. No other mechanic (grinding, ads, social pressure, gambling stakes, etc.) is described anywhere in the text.
```

**Labels assigned**

- `M_IntermediateCurrency` - **SPURIOUS**
  - span: "If your spend $20 on some item you get less then what your actually hoping for, but on here bingo gives you twice the number of your purchase"
  - why: The span describes spending real money ($20) on an in-game item/quantity and receiving a multiplied amount in return, which is the real-money-to-in-game-currency conversion pattern, coded regardless of the reviewer's positive framing of it (R7/R8).

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `5e6a5625-5291-4f0e-897c-1b63c1a26494` - MONOPOLY GO!

> I loved this game until the new season started. Suddenly I get no rewards for inviting friends and getting them to join facebook. I am struggling to get dices and when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way... And today. Well, I cannot log in to the game at all. It keeps giving me an internet connection error which is absolute nonsense. I have connected to 3 different wifi connections. BS!!😡

| | labels |
|---|---|
| gold | `M_Gambling`, `P_RewardMania`, `S_ForcedFellowship` |
| pred | `M_Gambling`, `P_CompleteTheCollection`, `P_RewardMania`, `S_ForcedFellowship` |
| **spurious** | `P_CompleteTheCollection` |

**Model analysis**

```
The reviewer names several Monopoly Go mechanics in sequence. First, they describe having previously received rewards for inviting friends and getting them to join via Facebook, and that this reward has now stopped ('Suddenly I get no rewards for inviting friends and getting them to join facebook'). This names the recruitment-for-reward mechanic itself (Social Pyramid Scheme), even though the reviewer is complaining the payout broke; the underlying design of rewarding friend invitations is what is being described. Second, the reviewer describes accumulating over 500 dice (an in-game currency used for board moves) and then 'playing max bet' on a chance-based event, hoping to trigger Shutdowns or Bank Heists, but getting none. This is a wager of an in-game currency (dice, whether earned or purchased) on an outcome governed by chance, which is a gambling mechanic per the codebook's boundary language allowing wagers of 'paid or earned intermediate currency,' and the unpredictable delivery of the special event outcomes (Shutdowns/Heists never landing) is also a variable-reward delivery schedule. Third, the reviewer complains that stickers are duplicates 'all the way,' which describes a randomized collection-item pool yielding repeated, unwanted drops rather than new items needed to complete sticker sets, implicating both the collection-completion compulsion and the reward-delivery mechanism. Finally, the reviewer describes being locked out of the game entirely by a persistent internet connection error across three different wifi networks. This is explicitly attributed to a technical fault (an 'internet connection error') with no stated in-game penalty tied to a design rule (e.g., no forfeited streak or progress described), so per R11 this does not support any dark-pattern label on its own.
```

**Labels assigned**

- `M_Gambling` - ok
  - span: "when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists"
  - why: The player wagers a stockpile of an intermediate currency (dice) in a 'max bet' for a chance at a rewarded outcome (Shutdowns/Bank Heists), which is a chance mechanic staked with intermediate currency.
- `P_CompleteTheCollection` - **SPURIOUS**
  - span: "Stickers are duplicates all the way"
  - why: Describes the frustration of a randomized sticker pool yielding repeat items instead of the missing pieces needed to complete sticker sets, reflecting the collection-completion compulsion being thwarted.
- `P_RewardMania` - ok
  - span: "played max bet, absolutely NO LUCK! No Shut downs and no bank heists"
  - why: Describes an unpredictable delivery schedule for the special reward events (sometimes triggered, sometimes not), which is the variable-reward mechanism sustaining repeated bets rather than a guaranteed payout.
- `S_ForcedFellowship` - ok
  - span: "Suddenly I get no rewards for inviting friends and getting them to join facebook"
  - why: Names a mechanic that rewards the player for recruiting friends into the game via Facebook; the complaint that the reward stopped does not erase that the underlying design incentivizes friend recruitment.

**Search:** `Monopoly Go max bet dice shutdown bank heist high roller` -> Search attempts failed due to a tool availability error (server tool use limit exceeded); no external result was obtained. Coding for M_Gambling relied instead on the codebook's own boundary rule permitting a wager of 'earned' intermediate currency, and general knowledge that Shutdowns/Bank Heists are chance-triggered board events in Monopoly Go, without needing external confirmation of a real-money exchange rate.

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
The reviewer describes a long-tenured player of a level-based match game hitting a wall past level 8000. Two mechanics are described concretely: running out of lives multiple times a day while trying to clear each level, which is the lives/energy regeneration wait gate (Wait to Play, lifts to Playing by Appointment), and the fact that clearing a single level now takes 5-7 days on average, which describes the same level being repeatedly attempted rather than simply being hard or slow in the abstract - a repetitive task tied to progress, satisfying Grinding. The reviewer then states payment is required to get through without frustration ('You must buy add ons else you can't make it through a sane mind') and that the free path is 'pure time waste if you're not paying', which is a direct statement that progress without payment is a slog while payment removes the barrier - Pay to Progress. The closing lines about wasted money and time and quitting to invest in 'real life' are evaluative/tone statements with no mechanic named (R2) and do not independently support Easy to Get Hard to Lose, since no reluctance to abandon accumulated investment operating on the decision to keep playing is described - the reviewer is instead reporting sums spent while disengaging, which the codebook explicitly treats as insufficient.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying."
  - why: The span states payment is effectively required to advance without frustration, and explicitly frames the unpaid route as wasted time, establishing a paid shortcut against a tedious free path.
- `T_Grinding` - ok
  - span: "avg 5-7 days per level"
  - why: Taking several days to clear a single level, combined with repeatedly running out of lives on it, describes the same level being attempted over and over as the means of advancing, which is repetitive task performance tied to progress rather than mere slowness.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "I run out of lives 3-4 times daily to beat every alternate level"
  - why: Running out of lives repeatedly and having to wait for them to regenerate is the lives-refill wait mechanic that gates continued play on the game's clock.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a5bfa159-1783-40a8-8852-ce39d7962398` - Homescapes

> They advertise many, many pin pull levels and games, but they are so few and far between, it's like false advertising. I'm over level 4000, so it's not like I haven't given it time. The "mini" games are foolish and also rare. I have also paid a lot for extra coins and things to see if pin pulls would happen, and they don't. Also, nearly everytime I do the required update, it takes days before it connects correctly again. I've tried on Gardenscapes too, same thing, false pin pulling advertising.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency` |
| pred | `M_Gambling`, `M_IntermediateCurrency` |
| **spurious** | `M_Gambling` |

**Model analysis**

```
The review opens with a complaint that the game's advertising overstates how often 'pin pull' levels occur, and that these are rare compared to what is shown in ads. This is a claim about marketing/advertising content, which per R13 is out of scope when it concerns the promotional material rather than an in-game mechanic (matches the counterexample about ads not reflecting actual gameplay). The reviewer's mention of being 'over level 4000' is used only to establish credibility/tenure, not to describe an unending or repetitive task, so it does not support Grinding or Infinite Treadmill on its own. The reviewer then describes having 'paid a lot for extra coins and things to see if pin pulls would happen, and they don't' — this shows real money being converted into an in-game currency (coins), which is the direction-of-transaction pattern for Intermediate Currency. The stated purpose of that spending — hoping that paying for coins would cause the rare, luck-dependent pin-pull levels to occur — describes using real-money-derived currency to chase an uncertain, luck-based outcome, which aligns with Gambling's definition of spending real money (via the intervening currency) for a chance at a desired outcome. Finally, the complaint about updates taking 'days before it connects correctly again' describes a technical/connectivity fault rather than a deliberate design penalty, so under R11 it does not support any dark-pattern label.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "paid a lot for extra coins and things to see if pin pulls would happen, and they don't"
  - why: The coins purchased with real money are then used in hopes of triggering the rare, luck-dependent pin-pull levels, i.e. money funneled through currency into a chance-based attempt at a desired outcome that fails to materialize.
- `M_IntermediateCurrency` - ok
  - span: "I have also paid a lot for extra coins and things to see if pin pulls would happen"
  - why: Real money is described as being spent to acquire coins, the in-game currency, matching the pattern where money is converted into a virtual currency.

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
The reviewer describes several complaints about Genshin Impact. First, they criticize the reward-to-effort ratio of a long quest ('finished a 7 hour quest and I barely got any primogems'), which is a value complaint about a reward's size rather than a description of how the reward is delivered (unpredictable, gacha-like, etc.), so it does not satisfy Reward Mania's requirement that the delivery mechanism itself be the driver of engagement. 'Exploration is debilitating' is a vague evaluative complaint about the open-world gameplay with no specific repeated task named, so it does not rise to Grinding under the boundary rule distinguishing a general 'repetitive/tedious' characterization from an actual described repeated activity. The complaint about character design and 'bare legs curse' is an aesthetic critique of art direction, not a description of the game using aesthetics to manipulate player behavior or spending, so it does not satisfy Aesthetic Manipulation. The final and most codable line is 'there is no resin overflow system.' Resin is Genshin's well-known stamina/energy resource that regenerates slowly over real time and is capped at a maximum; without an overflow mechanism, any resin generated past the cap while the player is away is lost, which pressures players to log in and spend resin on a schedule dictated by the game's regeneration timer rather than their own preference. This is the classic 'Wait to Play' indicator that underlies Playing by Appointment: an in-game timer (resin regeneration) that gates play and creates pressure to return periodically. While the reviewer frames it as a missing feature (a suggestion for an overflow system), the underlying active mechanic being complained about, resin capping on a real-time regeneration schedule with no way to bank overage, is itself an existing, described mechanic (per R12, the suggestion for the fix does not get coded, but the active resin-cap/regen system it responds to does).
```

**Labels assigned**

- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "there is no resin overflow system"
  - why: Resin is a capped stamina resource that regenerates on a real-time timer; the absence of an overflow system means resin generated beyond the cap while not playing is forfeited, which implies the player is pressured to log in and spend resin on the game's regeneration schedule rather than their own, the canonical Wait to Play pattern underlying Playing by Appointment.

**Search:** `Genshin Impact resin overflow system stamina cap` -> Confirmed Resin is a stamina/energy system that regenerates slowly over real time (about 1 per 8 minutes) and is capped at a maximum, with no mechanism to bank or exceed the cap, meaning regeneration beyond the cap is wasted if not spent.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_Gambling` | 1 | 3 |
| `M_PayToProgress` | 0 | 4 |
| `T_PlayingByAppointment` | 1 | 2 |
| `S_Competition` | 3 | 0 |
| `M_IntermediateCurrency` | 1 | 1 |
| `P_AestheticManipulation` | 2 | 0 |
| `S_Reciprocity` | 2 | 0 |
| `M_WasteAversion` | 1 | 1 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `T_Grinding` | 1 | 0 |
| `P_IllusionOfControl` | 1 | 0 |
| `P_CompleteTheCollection` | 0 | 1 |
| `P_RewardMania` | 1 | 0 |
| `T_MandatoryMarathon` | 1 | 0 |
| `M_EasyToPurchase` | 0 | 1 |
| `M_RecurringFee` | 1 | 0 |
| `S_FriendSpamImpersonation` | 1 | 0 |
| `M_PowerCreep` | 0 | 1 |

