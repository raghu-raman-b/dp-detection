# Error review - deepseek-v4-flash_none_teacher_v2_full

`deepseek-v4-flash` / reasoning `none` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `aad355174ac4`  
micro-F1 **0.762** (P 0.780 / R 0.744) - **26 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 8 | said NONE, gold had labels |
| SWAP | 3 | picked different labels than gold |
| MISSED ONLY | 7 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 8 | found all gold, added extras |

## The diagnostic that matters

Of **22** missed labels, **3** (14%) were named in the model's own analysis and dropped anyway; **19** (86%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `S_Competition` | 1 | 2 |
| `P_AestheticManipulation` | 0 | 2 |
| `S_Reciprocity` | 1 | 1 |
| `M_IntermediateCurrency` | 1 | 1 |
| `P_RewardMania` | 0 | 2 |
| `M_Gambling` | 0 | 2 |
| `T_PlayingByAppointment` | 0 | 1 |
| `T_Grinding` | 0 | 1 |
| `T_MandatoryMarathon` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `M_WasteAversion` | 0 | 1 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `M_EasyToPurchase` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `M_RecurringFee` | 0 | 1 |

## Missed everything (predicted NONE) (8)

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
The review is entirely a list of four feature requests phrased as suggestions the reviewer would like the developers to add to the game. The reviewer describes proposed additions — auctions, removing obstacle-deletion option, a widget to toggle accounts and view upgrade times, and hidden troop stats — none of which are presented as currently-existing mechanics or described as negatively operating on the player. Per R12, requests or hypothetical additions do not trigger tags for the proposed mechanics since none of these features are described as already present in the game.
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
The reviewer describes a series of technical faults introduced by an update: crashing when opening gifts or trading, lag preventing pokeball throws, lag in PvP and rocket battles, slow switching, unresponsive charge attacks, and freezing. All of these are attributed to bugs and malfunctions. None of the text describes a deliberate game design mechanic: there is no schedule, payment, social pressure, psychological manipulation, or time-gating. Under R11, behaviors attributed to bugs, glitches, errors, or technical faults are not dark patterns.
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
The review is essentially a request or suggestion: the reviewer expresses love for the game but worries that deleting the game would result in losing in-game purchases and progress. They then ask the developers to implement a feature that saves all progress and purchases. The concern is hypothetical—no loss has actually occurred in this game, and the requested cloud-save feature does not currently exist per the review. No existing game mechanic or design behavior is described as present. Under R12, suggestions or hypothetical additions do not trigger labels for the proposed mechanics, and nothing else in the text names an active design pattern.
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
The review is a purely positive description of the game: immersive experience, graphics, storyline, strategy depth in building an empire, and real-time PvP battles. There is no complaint, no description of any dark pattern mechanic, no time-gating, monetization, social pressure, psychological manipulation, or technical deception. The only concrete mechanics mentioned are empire-building strategy and player-versus-player combat — but the reviewer simply praises them without describing any exploitative design tied to competition. Under R7, approval alone is fine, but no label's indicator is instantiated: real-time combat against other players is ordinary competitive gameplay, and nothing shows the game forcing, incentivizing, or deceiving the player. No mechanic meets a label definition.
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
The review describes a specific malfunction: after an update, the player cannot request troops from their clan, and calls for a fix. This is a bug affecting a social game mechanic (troop requests), but the review attributes the behavior to a technical fault in the update. No dark pattern is described: the player's inability to request troops is a glitch, not a deliberate design choice. There is no mention of recruitment pressure, reciprocity obligations, time manipulation, or monetization. The review describes nothing that meets any codebook label.
```

**Search:** `Clash of Clans request troops clan bug` -> A known bug prevents clan members from seeing or making troop requests, often attributed to network issues or update changes.

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
The reviewer describes two grievances, both framed as requests for features: a sticker trading system that supports players not on Facebook, and boosters being usable in challenge matches. The reviewer implies stickers can currently only be traded with Facebook-connected players, which points to social integration requirements. The booster complaint describes a purchased booster that is blocked in a specific match context. Both statements are largely feature requests or descriptions of limitations rather than active dark patterns involving manipulation of time, money, social ties, or psychology. Sticker trading itself being social doesn't inherently constitute a dark pattern without incentive or obligation pressure described.
```

**Search:** `Match Masters game stickers trade` -> Sticker trading requires a Facebook-based group, suggesting a social dependency but this search result doesn't establish a dark pattern; it confirms stickers are collectible items.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a5bfa159-1783-40a8-8852-ce39d7962398` - Homescapes

> They advertise many, many pin pull levels and games, but they are so few and far between, it's like false advertising. I'm over level 4000, so it's not like I haven't given it time. The "mini" games are foolish and also rare. I have also paid a lot for extra coins and things to see if pin pulls would happen, and they don't. Also, nearly everytime I do the required update, it takes days before it connects correctly again. I've tried on Gardenscapes too, same thing, false pin pulling advertising.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency` |
| pred | _NONE_ |
| **missed** | `M_IntermediateCurrency` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer makes two distinct complaints about Homescapes. First, the game's pin-pull levels and other mini-games are heavily advertised but appear 'so few and far between,' which the reviewer calls false advertising. Second, after performing required updates the game often fails to reconnect to the server for days, and the same happens in the developer's other title, Gardenscapes. The false-advertising complaint is aimed largely at marketing material promising these pin-pull levels, which under R13 falls outside the game application. To the extent pin-pull levels within the game are merely uncommon, rarity of a mode itself does not match a dark-pattern definition; no price, urgency, schedule, or manipulative mechanic is attached to it. The repeated-update connectivity failure is a technical malfunction — days before the game connects — which under R11 is not a deliberate design pattern. There is no span describing a functional design behaviour that satisfies any of the 29 labels.
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

- `M_IntermediateCurrency` - considered and rejected -> **rule interpretation**
- `T_MandatoryMarathon` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes leaving the game with inventory full ("bag full") and returning to find the inventory empty and coins (earned and purchased) spent. The account is brief and does not identify which game rule produced the loss. It reads most plausibly as a save or session-recovery problem: the player's holdings were not carried over between sessions. Per R11, a loss that follows from faulty progress retention is a technical malfunction, not a deliberate dark pattern. No time-gated schedule, payment requirement, advertised storefront download, social manipulation, or psychological reward loop is described. The mention of coins having been purchased could gesture at Intermediate Currency, but the review never states that real money is being converted into coins at the moment of purchase; it only notes some coins were previously bought. Without a described design behaviour, no label meets the standard of coding an explicit mechanic under R2.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (3)

### `fdef27f2-9a21-4b8e-a04c-7a4753e0fb07` - 8 Ball Pool

> The game is great, but the user interface is completely rigged. Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins and are forced to buy real ones. ​We need a "Default Table Lock" or the game should always open the lowest bet table by default, not the highest! Fix this scammy feature. Giving 1 star

| | labels |
|---|---|
| gold | `M_Gambling`, `M_IntermediateCurrency`, `M_UIMisdirection` |
| pred | `M_IntermediateCurrency`, `M_PayToProgress`, `M_UIMisdirection` |
| **missed** | `M_Gambling` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_Gambling` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a single interlocking design behaviour in the billiards UI. On opening the game or entering the 1v1 area, the interface automatically scrolls to and pre-selects the highest-stakes table the player can afford, so a routine tap lands the player in a match that drains their coins. The reviewer reads that selection as deliberate: a 'Dark UX' trick to produce accidental mis-clicks and coin loss, after which the player is forced to buy coins with real money. The pre-selection is an active, functional interface rule (auto-scroll + default-to-highest), not a malfunction, so it is codeable as a designed behaviour. Three mechanic strands stand out: (1) an interface that directs the player's action toward a harmful option and gives no safe default, which matches UI Misdirection; (2) loss of coins leaving the player required to buy more to keep playing, which matches Pay to Progress; and (3) that purchase is made with real money in exchange for the virtual coin currency, matching Intermediate Currency. The request for a 'Default Table Lock' is a proposed fix, not an existing mechanic, and is not coded (R12).
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "forced to buy real ones"
  - why: The reviewer describes needing to acquire the in-game coin currency by paying real money, showing the conversion of real money into virtual currency to continue play.
- `M_PayToProgress` - **SPURIOUS**
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: Once coins are drained by the mis-directed match entry, continued play is contingent on buying back coins, i.e. the game reaches a state where money is needed to keep playing.
- `M_UIMisdirection` - ok
  - span: "Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins"
  - why: The interface actively moves the player's selection to the highest-stakes table with no safe default, forcing the player to locate and select a lower table themselves — an interface behaviour operating against the player's intent.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `12267c1e-47ba-4984-97c8-768e820ceb1c` - Bingo Blitz™️ - Bingo Games

> not very user-friendly. no apparent reachable goals within a decent amount of time. I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| pred | `M_Gambling`, `M_IntermediateCurrency`, `P_CompleteTheCollection`, `P_RewardMania` |
| **missed** | `M_EasyToPurchase`, `P_AestheticManipulation`, `T_Grinding` |
| **spurious** | `M_Gambling`, `M_IntermediateCurrency`, `P_RewardMania` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - never mentioned -> **attention / recall**
- `P_AestheticManipulation` - never mentioned -> **attention / recall**
- `T_Grinding` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a collection game played by completing photo sets through bingo rounds. Three mechanisms are intertwined: (1) the game runs rounds whose purpose is gathering photos to complete a set, and a specific missing photo is offered for purchase right after a losing round; (2) the purchase offer resolves by chance rather than delivering the promised photo ('I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED'); (3) coins are the paying medium and the reviewer calls the whole repeated expenditure 'wasted so much money', implying coins were obtained with real money. The collection objective, the chance-based delivery, and the real-money funding chain are all active in the text.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED"
  - why: The reviewer stakes coins (funded by real money) on an offer that resolves by chance, receiving 2-3 bingos instead of the specific promised photo, i.e., paying for a chance-based draw.
- `M_IntermediateCurrency` - **SPURIOUS**
  - span: "spend extra coins"
  - why: Coins are the in-game currency repeatedly spent on the offer, and the reviewer's closing 'I've wasted so much money' establishes that this currency expenditure was funded with real-world money.
- `P_CompleteTheCollection` - ok
  - span: "I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set"
  - why: The reviewer repeatedly plays to collect photos specifically to complete a set, and the missing member of that set drives the repeated attempts and spending.
- `P_RewardMania` - **SPURIOUS**
  - span: "I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED"
  - why: Beyond the stake, the delivery itself is random and unpredictable: repeated attempts yield unrelated bingos rather than the desired photo, keeping the player trying on an unreliable reward schedule.

**Search:** `Bingo Blitz album photos collect sets mechanic what are bingo blitz photo collections` -> Photo collections in Bingo Blitz involve collecting pictures from destinations to complete sets in an Adventure Book, each completed collection offering rewards.

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
The reviewer describes purchasing a deal promised to grant new cards toward completing an album, but receiving duplicates. This reveals: (1) album completion mechanics tied to card collection where progress is blocked by missing specific cards, (2) a purchase directly marketed as solving that gap but failing, creating a cycle where payment is the advancement route but the random delivery undermines it, (3) money spent on a chance-based reward system labeled as guaranteed new content, which is then revealed as duplicates. The reviewer frames the whole experience as a scam, but the underlying design is what is described. Web search establishes that Dice Dreams has an album/sticker collection feature where cards are obtained through purchases and packs, and duplicates are a known complaint.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**  _[span loose match]_
  - span: "I bought a deal which promised i would get NEW cards, and all i got were useless duplicates"
  - why: The purchase is for reward delivery that is not guaranteed—the outcome (new vs duplicates) is randomized, making the sale a wager on chance.
- `M_PayToProgress` - **SPURIOUS**
  - span: "I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards"
  - why: The player is specifically buying to complete an album and advance, showing the game's progress is contingent on purchases.
- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The span shows the player pursuing a full album collection, with the remaining cards as the focus of their effort.
- `P_RewardMania` - ok  _[span loose match]_
  - span: "I bought a deal which promised i would get NEW cards, and all i got were useless duplicates"
  - why: The unpredictable, duplicate-heavy card delivery from a randomized pool sustains engagement through repeated attempts rather than value, which is the variable rewards pattern.

**Search:** `Dice Dreams album cards duplicates deal new cards scam` -> Dice Dreams has an album/sticker collection feature sold through purchases and packs; players frequently report duplicate cards and the random delivery undermines collection progress, consistent with the review.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (7)

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
The reviewer focuses on one specific slot mode, the "genie game", describing an alleged rigged wheel bonus. When the wheel lands on a good prize (100 million with a 5x multiplier), the genie moves the wheel to a spin tag, after which the prizes are lower (48 million). This is a claim that the game overrides the wheel's genuine result to redirect the player to a worse outcome. No real money is described as funding the spin, so no monetary stake is shown; the complaint is purely about the outcome-determination being manipulated. The reviewer also requests that the player be given agency to keep or spin again, which describes a denial of control over the outcome.
```

**Labels assigned**

- `P_IllusionOfControl` - ok  _[span not verbatim]_
  - span: "when the wheel spin after stopping on a great price the genie move the wheel to a spin tag, and then the prices after the spin are way lower than the original price"
  - why: The span asserts the game manipulates the determination of the outcome by moving the wheel off a winning result onto a worse one, which is concealing the true outcome determination rather than a mere unlucky run.

**Search:** `genie game wheel spin Cash Frenzy Casino Slots` -> Cash Frenzy is an app with slot games whose 'genie' slot features a wheel bonus with prizes and free spins; the review describes this wheel being moved from a higher to a lower prize.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

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
The review is short and mostly describes a customer-service grievance: the reviewer spent 9 diamonds on a game element that failed to appear within the first 5 moves and the 5 bonus moves, and support would not refund. That failure is framed as a technical/product fault, not a designed mechanic, so it does not trigger a dark pattern under R11. The reviewer also states the game does not require paying to win (an absence of a mechanic, not its presence). Two remaining content threads: an advice to limit spending to 'the pass,' naming a purchasable season pass without describing how it operates, and an instruction to get friends and a team to trade lives, which describes a reciprocal resource-exchange feature between existing players.
```

**Labels assigned**

- `S_Reciprocity` - ok
  - span: "Get friends and a team and trade lives."
  - why: The span describes exchanging lives with friends and teammates already playing: a favour/resource transfer between existing players, which is Reciprocity, not recruitment of new players (Forced Fellowship).

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
The review splits into two distinct claims. The first describes the player purchasing Poké Balls, then observing that captures increasingly fail ('they keep breaking out'), which drains the purchased balls faster and forces repeat purchases. The reviewer frames this as the developer manipulating capture outcomes in response to spending ('I feel taken advantage of'), i.e., a hidden, rigged mechanic tied to payment. The second part, appended as an edit, asserts that a review was posted under the reviewer's identity that they did not write, because they know no other players and talked to no one — an act of the game publishing content in the player's name.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way"
  - why: The reviewer asserts that the game covertly changes capture outcomes after purchase so balls are consumed faster and more purchases are required, concealing how results are determined to drive further play and spending.
- `S_FriendSpamImpersonation` - ok
  - span: "I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE"
  - why: The reviewer states that text they did not author was published in the game's review under their identity, i.e., content posted as the player by the game/account, which is impersonation.

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
The reviewer describes a run of grievances in MONOPOLY GO! after a new season began. First, they expected rewards for recruiting friends onto Facebook-play, which implies a friend-invite-for-reward recruitment loop inside the game design. Second, they describe needing dice and, with 500+ dice wagered at max multiplier, getting no shutdown or bank-heist events — a complaint about a bad streak in chance-based minigames, with no money or paid stake described. Third, sticker rewards keep arriving as duplicates, which describes random reward delivery repeatedly producing unwanted repeats from a collection pool. Finally, they report being unable to log in due to an internet connection error; this is attributed to a technical fault and, per R11, is not a design pattern.
```

**Labels assigned**

- `P_RewardMania` - ok
  - span: "Stickers are duplicates all the way"
  - why: The sticker cards arrive through a random drop system and keep repeating, so the reward delivery schedule repeatedly produces useless repeats — a variable/duplicate reward delivery complaint.
- `S_ForcedFellowship` - ok
  - span: "I get no rewards for inviting friends and getting them to join facebook"
  - why: The reviewer's expectation of a reward for recruiting friends to the game names the friend-invite-for-incentive recruitment loop; the complaint that the reward stopped does not remove the mechanic from the design.

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
The reviewer describes a recent change to the game's daily rewards. The core mechanic: the daily reward can only be claimed when the player bets 50,000 across play, and the player reports they cannot complete that daily target because the most they can obtain from the timed rewards is 40,000. The shortfall between what play can generate (40,000) and the daily-reward threshold (50,000) is what forces paying; the reviewer explicitly refuses to pay just to collect the daily rewards and deletes the game. So two mechanics are being described together: a daily log-in task that must be fulfilled to earn its reward, and a de facto monetary barrier created by setting that task's target above what free play can realistically fund.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "The most I can seem to get on the timed rewards is 40,000. I'd not pay just to get my daily rewards"
  - why: The daily-reward target (50,000) exceeds the maximum free play can fund (40,000), and paying is presented as the route to close the gap; the free route falls short of completing the daily reward, implying payment is required to keep earning them.
- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The reviewer describes a daily reward that is only earned by completing a daily betting task, with the day's reward forfeited when the task cannot be fulfilled.

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
The reviewer warns that winning in Dice Dreams costs hundreds of dollars, that sticker collections can never be finished without paying, and that goals rarely complete without payment. The reviewer also describes being required to give five stars to post a review, which is outside the installed game scope. The central mechanics: pay walls are the route to victory and to completing sticker albums; the last one or two stickers are made unattainable then sold; and goal completion happens only rarely, framing the reward structure as gated behind spending. The sticker album is a finite collection goal the game withholds completion of until payment.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: The last stickers are deliberately withheld from normal play, and the only route to them is spending, which is artificial scarcity with a purchase remedy.
- `M_PayToProgress` - ok
  - span: "it may let you complete a goal maybe one out of hundred times"
  - why: Goal completion is reported as near-impossible without spending, describing progress blocked unless the player pays, per the earlier price claim.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two"
  - why: The sticker album is a finite collection the game never lets the player finish; the withheld last items are the hook that keeps the collection active.

**Search:** `Dice Dreams stickers album goal mechanic` -> Dice Dreams has a sticker album collection where completing sets yields rewards; stickers drop from packs. This confirms the sticker album is the collection goal referenced.

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
The reviewer describes the sticker collection mechanic in MONOPOLY GO!. They express frustration about always getting duplicate stickers, which prevents them from completing sets. They additionally state that the game never lets them finish all sets unless they pay money. The reviewer begins saying they like the game but finds the sticker acquisition mechanics frustrating. The core gameplay described involves collecting stickers to complete themed sets, where duplicates are frequent and completing sets requires payment. I must determine which mechanics are described: a game that rewards completing collections, duplicates from a random reward system, and progress gated behind payment.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: Completion of the sticker sets is stated to be impossible without payment, showing a direct payment gate on progress.
- `P_CompleteTheCollection` - ok
  - span: "frustrating when it comes to getting stickers. always get duplicates. never lets you finish all the sets"
  - why: The player is working to complete a collection of sticker sets, and the frustration is tied to inability to finish that collection.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: The random delivery of stickers from a reward pool results in repeated unwanted duplicates, indicating an unpredictable reward delivery system.

**Search:** `Monopoly GO stickers sets finishing albums` -> Sticker albums in MONOPOLY GO! are collections of themed sets that reward completion with in-game currency and other items. Stickers are obtained through gameplay and purchases.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (8)

### `95ddadb3-82cd-4042-8a51-cf8b3ed164c2` - Mech Arena - Shooting Game

> You stuck waiting 30 seconds just to connect to a match. This game makes it seem like they give so many rewards but if all just for show. Its difficult to get weapon upgrades or any percs others you stick battling to win. This kind of games just rob you of your time in my opinion

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `T_Grinding` |
| **spurious** | `T_Grinding` |

**Model analysis**

```
The reviewer describes three things. First, waiting roughly 30 seconds to connect to a match; this is matchmaking and queue latency, which per the Wait to Play boundary is a service-side wait rather than a designed in-game gate, so it does not code Playing by Appointment. Second, rewards that are 'just for show', which is a vague value complaint with no delivery mechanic (unpredictability or complexity) named, so it does not code Reward Mania. Third, difficulty obtaining weapon upgrades and perks unless the player keeps 'battling to win', which describes repeated combat as the activity required to make progress, pointing to Grinding. The final line 'rob you of your time' is an evaluation of the experience rather than a mechanic itself.
```

**Labels assigned**

- `T_Grinding` - **SPURIOUS**
  - span: "Its difficult to get weapon upgrades or any percs others you stick battling to win."
  - why: The reviewer states upgrades and perks only come after continued battling, implying repeated matches are the activity required to advance, which matches the grinding pattern of repetitive tasks required for progress.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `91e3872b-4443-43de-b4e5-508456ea6706` - Mystery Town: Merge Games

> Good game but greedy. I am level 113 and there is no extra energy. it's getting annoying now, to have any change at progressing you need to purchase.

| | labels |
|---|---|
| gold | `M_PayToProgress` |
| pred | `M_PayToProgress`, `T_PlayingByAppointment` |
| **spurious** | `T_PlayingByAppointment` |

**Model analysis**

```
The reviewer describes reaching level 113 and finding that there is 'no extra energy,' before connecting the energy shortage to the need to pay for progression. The core mechanic being described is an energy system that gates continued play, and the reviewer states that the only way around that gate is purchase. I need to determine which labels apply given the search on the energy system.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "it's getting annoying now, to have any change at progressing you need to purchase."
  - why: The reviewer states that further progress is contingent on purchasing, which is the Pay to Progress definition.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "I am level 113 and there is no extra energy."
  - why: The energy system imposes a throttled resource limit: the reviewer's play is gated by a finite energy pool, which represents the schedule-imposed wait between sessions. The search confirms energy refills slowly and caps, indicating a timer-gated resource.

**Search:** `Mystery Town Merge Games energy mechanic` -> Energy is earned daily and refills slowly over time, constraining how much the player can do before waiting for regeneration or paying.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `66698c5c-8577-46fe-b796-8e93ad782166` - Teen Patti GOLD: 3 Patti Rummy

> Finally you forced me to uninstall the game. Forced notifications to give you permission to my contact list, for what? Is this a game or data collecting app?why I am bound to give you that permission? Better to keep you as spam app.

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `M_EasyToPurchase`, `S_FriendSpamImpersonation` |
| **spurious** | `M_EasyToPurchase`, `S_FriendSpamImpersonation` |

**Model analysis**

```
The review describes being forced to grant contact-list access and pressured by notifications. Two movements are present. The first: the game will not let the reviewer proceed or use the game unless they grant the contact-list permission, expressed as being "forced" and "bound" to give it. The second: the game sends unsolicited notifications as a pressure mechanism. The reviewer's question 'Is this a game or data collecting app?' implies the contact permission is not needed for the gameplay itself but for the developer's data exploitation. The external search clarifies the contact permission is used for push notifications, i.e., for sending messages to the player's own device, not for messaging the contact list itself.
```

**Labels assigned**

- `M_EasyToPurchase` - **SPURIOUS**
  - span: "Forced notifications to give you permission"
  - why: The notification is described as forcing the user toward a designated action (granting permission) through a prompt that must be dismissed to continue. This is a deliberate UI/UX pressure mechanism, though not strictly purchase-related.
- `S_FriendSpamImpersonation` - **SPURIOUS**  _[span not verbatim]_
  - span: "Better to keep you as spam app"
  - why: The reviewer calls the app spammy, attributing the behavior of sending notifications to the developer. However, notifications sent to the player's own device are not messages to the player's contact list, so this general description of notification spam does not establish the label.

**Search:** `Teen Patti GOLD contact permission notifications what for` -> The app uses contact-list permission for push notifications and general app functionality; no game mechanic requires it, so granting it serves the developer's data and notification purposes.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `21021f9a-e106-4e51-b01d-3fe4a4c941fc` - MONOPOLY GO!

> Deleted the game now. The latest event I was about to get 525 dice as reward, I had 3 left to go and I ran out of dice, it said 2Days left. Now just logged in after sleeping and the event is now changed. Deleting this game and what an absolute waste of time. Never purchased anything coz i have trust issues with F2P model games, and my gutt was right all along. Fun when it lasted, but that was a low blow.

| | labels |
|---|---|
| gold | `T_PlayingByAppointment` |
| pred | `M_PayToProgress`, `P_CompleteTheCollection`, `P_EasyToGetHardToLose`, `T_DailyRewards`, `T_PlayingByAppointment` |
| **spurious** | `M_PayToProgress`, `P_CompleteTheCollection`, `P_EasyToGetHardToLose`, `T_DailyRewards` |

**Model analysis**

```
The review describes the player being close to winning a limited-time event reward (525 dice), running out of dice with 2 days remaining, and, after a night's sleep, discovering that the event has disappeared; the player lost the opportunity to obtain a reward they were about to earn. The mechanics being described are an event with a timer that drives the player to keep playing to get the reward, a loss of the reward if missed, and an underlying pay-to-keep-playing element (running out of dice likely forcing payment or waiting to continue). Since the player was near completion and lost the chance when the event expired while asleep, this touches on both the scheduling and the loss of an almost-completed goal.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "I had 3 left to go and I ran out of dice"
  - why: Running out of dice is a resource gate; continuing the event without dice requires spending money or waiting a long time. The player was unable to progress further and lost the reward as a result.
- `P_CompleteTheCollection` - **SPURIOUS**
  - span: "I had 3 left to go"
  - why: The player had nearly completed the event goal (three steps missing to gain dice) and losing this almost-finished objective is framed as the key harm, showing investment in finishing.
- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "I had 3 left to go and I ran out of dice, it said 2Days left. Now just logged in after sleeping and the event is now changed."
  - why: The player's nearly completed progress (3 out of something) is lost if they step away; the cost of leaving is giving up what they had already almost finished, making exit costly.
- `T_DailyRewards` - **SPURIOUS**
  - span: "The latest event I was about to get 525 dice as reward, I had 3 left to go and I ran out of dice, it said 2Days left. Now just logged in after sleeping and the event is now changed."
  - why: The event resets or expires with the passage of real time; by logging in after sleeping, the player misses the event and loses the near-complete reward. The daily time-gated return determines whether the reward is obtained.
- `T_PlayingByAppointment` - ok
  - span: "The latest event I was about to get 525 dice as reward, I had 3 left to go and I ran out of dice, it said 2Days left. Now just logged in after sleeping and the event is now changed."
  - why: The event operates on a two-day countdown; the player must play within that window to claim the reward, and sleeping (not playing) caused the event to disappear. The game's clock dictates when the reward can be earned.

**Search:** `MONOPOLY GO dice event reward expires 2 days` -> Monopoly GO dice events typically last a limited time (often 2 days), driving players to claim rewards within the window; missing the deadline forfeits the reward.

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
The review describes a survival/base-building game. Several distinct mechanics: (1) base update/build timers that scale endlessly and become ridiculous, forcing waiting — Playing by Appointment / Wait to Play. (2) endless scaling and grind with no attainable goal — Grinding, and possibly Infinite Treadmill ('no point to look forward to, just more grind' carries tedium but the endless scaling is described as an endless treadmill of upgrades). (3) deliberately confusing/overwhelming UI pushing purchases — UI Misdirection (attention/obstructing opt-out toward buying). (4) alliances dictating development and attacking/bullying non-members — this describes coercion into a group and being attacked; bullied players are not in the top alliance. I'll consider the social labels. 'Alliances are weird, top ones dictating what to develop, what to rush' describes being compelled by group leaders, not by the game reward structure. 'If you are not in one then you get attacked and bullied' describes harm by other players without an incentive attributed... The review doesn't show a design reward flow clearly enough for Encourages Anti-Social. However ordinary competitive plunder/attack design where the aggressor takes from weaker players... The pay-to-win framing describes money giving advantage, which is Pay to Win low-level.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "it's set up in a pay to win way"
  - why: Explicit statement that spending money grants advantages over non-paying players.
- `M_UIMisdirection` - ok
  - span: "The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff."
  - why: UI is described as designed to push purchases by being confusing/overwhelming.
- `S_Competition` - ok
  - span: "If you are not in one then you get attacked and bullied."
  - why: Players within the game attack one another for resources/standing.
- `T_Grinding` - **SPURIOUS**
  - span: "Everything scales endlessly, there is kinda no point to look forward to, just more grind"
  - why: Adjust: the scaling/grind here ties to endless upgrades; though the repetitive activity is not literally named, it reads as crafted tedium loop.
- `T_InfiniteTreadmill` - ok
  - span: "Everything scales endlessly, there is kinda no point to look forward to"
  - why: The game continually extends content (endless scaling upgrades) so there is no attainable endpoint.
- `T_PlayingByAppointment` - ok
  - span: "the update times for your base are becoming ridiculous. Everything scales endlessly"
  - why: Build/update timers that impose wait times directly gate base progression and scale endlessly.

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
The reviewer is recounting their long-term experience near the end-game (level 8416). Several mechanics are being described through their own play. Running out of lives several times a day, and taking 5-7 days per level, shows an energy/lives system that regenerates on a real-world timer and gates when further attempts can be made. Spending 5-7 days and repeated daily sessions to clear a single level describes the repetitive, time-intensive task the player must perform to keep advancing. The statement that add-ons must be bought or the player cannot make it through is a direct pay wall on progress. The closing regret about wasted money and time is the player disengaging, not an investment holding them in, so it does not form an Easy-to-Get-Hard-to-Lose span.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through a sane mind."
  - why: The reviewer asserts continued progress is contingent on buying add-ons, matching a pay wall on advancement with a paid alternative to a tedious free path.
- `T_Grinding` - ok
  - span: "I run out of lives 3-4 times daily to beat every alternate level, avg 5-7 days per level."
  - why: Repeatedly replaying levels over multiple days to clear each one describes repetitive tasks required to make progress.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "I run out of lives 3-4 times daily to beat every alternate level"
  - why: Running out of lives repeatedly across a day shows the lives regeneration schedule imposing wait times on when the player can attempt levels again.

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
The reviewer complains about three things: poor rewards (primogems) for a 7-hour quest, exploration being tiring, and the absence of a resin overflow system after five years of play. The resin system is Genshin's stamina resource that regenerates over time and caps at 200; without an overflow system, excess regeneration is wasted if the player doesn't log in to spend it. The reviewer's complaint about no overflow indicates that the game imposes a schedule where the player must return when the cap fills or lose the value of further regeneration. The character-design complaint is subjective and does not describe a manipulation mechanic. The quest reward complaint describes low reward value, not a particular dark pattern. The resin issue points to the Wait to Play mechanic: a timer/cap that dictates when the player must return.
```

**Labels assigned**

- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "there is no resin overflow system"
  - why: The absence of an overflow system implies the resin cap forces the player to play on the game's regeneration schedule; excess resin is wasted, obligating regular returns to avoid loss.

**Search:** `what is resin in Genshin Impact and resin overflow system` -> Resin is a stamina-like resource used for farming and challenges that regenerates over time up to a daily cap of 200; an overflow system would allow regeneration beyond the cap.

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
The reviewer is describing a single trajectory: players must spend money to achieve meaningful progress or growth, and a recent update then removed the game's player-versus-player mode ('open silver'), which the reviewer says makes all that paid-for growth pointless and deceives whoever already spent money. The stated requirement to spend for growth is explicit and current. The devaluation of that growth after the update is stated as having already happened to paying players. There is no description of timers, schedules, ads, loot, social mechanics, or interfaces.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You have to spend to have any meaningful growth"
  - why: The reviewer states directly that attaining any meaningful progress/growth is contingent on spending money.
- `M_PowerCreep` - **SPURIOUS**
  - span: "they go and make it all pointless by getting rid of any player vs player"
  - why: The growth the reviewer paid for is devalued after acquisition when the update removes PvP, making the purchased progress worthless to those who already spent.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `T_PlayingByAppointment` | 1 | 3 |
| `M_Gambling` | 2 | 2 |
| `T_Grinding` | 1 | 2 |
| `M_PayToProgress` | 0 | 3 |
| `M_IntermediateCurrency` | 2 | 1 |
| `P_RewardMania` | 2 | 1 |
| `S_Competition` | 3 | 0 |
| `P_AestheticManipulation` | 2 | 0 |
| `S_Reciprocity` | 2 | 0 |
| `P_EasyToGetHardToLose` | 1 | 1 |
| `M_EasyToPurchase` | 1 | 1 |
| `T_MandatoryMarathon` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `M_WasteAversion` | 1 | 0 |
| `T_DailyRewards` | 0 | 1 |
| `S_FriendSpamImpersonation` | 0 | 1 |
| `M_PowerCreep` | 0 | 1 |
| `P_CompleteTheCollection` | 0 | 1 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `M_RecurringFee` | 1 | 0 |

