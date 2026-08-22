# Error review - kimi-k3_high_teacher_v2_full

`kimi-k3` / reasoning `high` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `6529a474a2b0`  
micro-F1 **0.811** (P 0.798 / R 0.826) - **21 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 5 | said NONE, gold had labels |
| SWAP | 5 | picked different labels than gold |
| MISSED ONLY | 2 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 9 | found all gold, added extras |

## The diagnostic that matters

Of **15** missed labels, **7** (47%) were named in the model's own analysis and dropped anyway; **8** (53%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `M_Gambling` | 1 | 1 |
| `S_Reciprocity` | 2 | 0 |
| `T_MandatoryMarathon` | 0 | 1 |
| `M_PayToProgress` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `T_Advertisement` | 1 | 0 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `M_UIMisdirection` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `S_Competition` | 1 | 0 |
| `P_AestheticManipulation` | 0 | 1 |
| `P_RewardMania` | 0 | 1 |
| `M_IntermediateCurrency` | 0 | 1 |

## Missed everything (predicted NONE) (5)

### `0853c395-2040-4e0b-a56c-1591484cd35b` - Clash of Clans

> 10/10, but we would like: 1.) Bids & auctions for decorations, skins and sceneries with in-game currency. 2.) Remove the option to remove an obstacle if you've turned it into a decoration. 3.) Widget that can toggle various accounts and see how much time is left for upgrades. 4.) Hidden option for troops' advanced statistics.

| | labels |
|---|---|
| gold | `T_PlayingByAppointment` |
| pred | _NONE_ |
| **missed** | `T_PlayingByAppointment` |

**Did the model consider what it missed?**

- `T_PlayingByAppointment` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer gives a 10/10 rating and then lists four wishes: (1) bids and auctions for decorations, skins and sceneries using in-game currency, (2) removal of the option to remove an obstacle once turned into a decoration, (3) a widget to toggle accounts and see upgrade time remaining, (4) a hidden option for troops' advanced statistics. Every one of these is framed as a request ('we would like'), describing features that do not currently exist in the game. Under R12, requests, suggestions, or hypothetical additions do not trigger tags for the proposed mechanics, so the auction/currency idea cannot be coded as Intermediate Currency or Gambling, and the upgrade-timer widget wish cannot be coded as Playing by Appointment. R2 also blocks coding from tone or the rating alone. No currently present game mechanic is described anywhere in the text.
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

- `S_Competition` - considered and rejected -> **rule interpretation**
- `S_Reciprocity` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The entire review is a bug report about a recent update: the game crashes when opening gifts or trading with friends, lag prevents throwing a pokeball, and PvP and rocket battles suffer from lag, unresponsive charge attacks, and freezes while the opponent keeps attacking. Every mechanic named (gifting, trading, catching, PvP battles) is mentioned only to describe a malfunction, not a design behavior. Under R11, dark patterns are deliberate design choices, and behaviors attributed to bugs, crashes, lag, or freezes are suppressed. Trading with friends could in principle relate to Reciprocity, but the span describes no obligation, donation, or favor mechanism — only that the feature crashes. The PvP mention could relate to Competition, but the span describes the battles purely as lagging and freezing, a technical fault, not the design of competing against other players. No reward or progression penalty from the freezes is described (no forfeited match or lost streak stated as a game rule), so R11's exception does not apply either. Nothing in this review describes a functioning design mechanic.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b98d7e75-73da-4591-b23e-1a2951bfd856` - Township

> I like this game a lot, but recently after seeing the ads, there is no way to close it. No cross mark on the screen , if you try to click anywhere on the screen it takes you to store. If you go back to game it is still stuck in the last sceeen of the ad. You have to kill the game to come out of the ad screen , so frustrating!!!

| | labels |
|---|---|
| gold | `M_UIMisdirection`, `T_Advertisement` |
| pred | _NONE_ |
| **missed** | `M_UIMisdirection`, `T_Advertisement` |

**Did the model consider what it missed?**

- `M_UIMisdirection` - never mentioned -> **attention / recall**
- `T_Advertisement` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer likes the game but describes a problem with ads shown inside it: after an ad finishes, no close (cross) button appears, tapping anywhere redirects to the store, and returning to the game leaves the ad's final screen stuck, forcing the player to kill the app. Two candidate readings: (1) forced ad viewing under T_Advertisement, since the player cannot dismiss the ad and must restart the game; (2) a technical malfunction, since the ad close button failing to render and the screen being 'stuck' is characteristic of a broken ad unit rather than a deliberate design choice. The reviewer frames the whole episode as broken behavior ('No cross mark on the screen', 'still stuck in the last sceeen of the ad', 'You have to kill the game'), i.e., the ad's dismissal control failed. R11 states that behavior attributed to a bug, glitch, or technical fault does not receive a dark pattern label, since dark patterns are deliberate design. The redirect to the store on tap is ordinary ad behavior, and no reward-for-watching or ad-gated progression is described. No other mechanic (timers, currencies, purchases, social features) is described in the review.
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
The reviewer describes a single issue: since an update, they can no longer request troops from their clan, and they ask for it to be fixed. Troop requesting between clan members would ordinarily describe a resource-transfer mechanism between existing players (Reciprocity), but the review does not describe the mechanic functioning as designed. It describes the feature as broken following an update, i.e., a technical fault. Under R11, a behavior attributed to a bug, glitch, or error does not support a label, because dark patterns are deliberate design choices rather than malfunctions. There is no other mechanic described: no timers, no purchases, no daily incentives, no competitive framing. The mention of the clan names a social group but carries no obligation, recruitment, or donation behavior in operation.
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
The reviewer describes returning to the game and finding inventory items gone and both earned and purchased coins consumed. The review does not explain what game rule used those resources while the player was away, so it is unclear whether this is a designed mechanic such as offline consumption or attacks, an accidental expenditure interface, or a malfunction. Without a clearly described mechanic or design behavior, the text cannot support a dark-pattern label under R2 and R4.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (5)

### `fd1230ab-7d12-4aeb-a425-e37ed06bcd5c` - Pokémon GO

> I love this game, just started playing about 2 months ago. Though I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way. I feel taken advantage of. 3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| pred | `M_PayToProgress`, `P_IllusionOfControl`, `S_FriendSpamImpersonation` |
| **missed** | `P_OptimismAndFrequencyBiases` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**

**Model analysis**

```
The review has two layers. The main body describes a monetisation mechanic: after the reviewer started purchasing Poké Balls, captures allegedly began failing more often ('they keep breaking out'), burning through the purchased consumables faster and forcing repeat purchases. This carries two claims: (1) continued play/progress (capturing Pokémon, the core loop) requires buying more balls, and (2) the game secretly manipulates capture outcomes against paying players to accelerate consumption — a concealed-outcome-manipulation allegation, which the reviewer reinforces with 'I feel taken advantage of'. The money here buys items directly, not an in-game currency, so Intermediate Currency does not apply. The second layer is the edit: the reviewer claims the review itself was written and posted under their account without their authorship, and denies the social content attributed to them ('I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE'). Under the Destination of the message rule, a store review written under the player's account counts as the game acting through the player's identity. The impersonation claim does not suppress the in-game mechanics described in the text, which remain codable (per the worked example where the same situation assigned both the impersonation label and the in-game monetary labels).
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "I go through the balls faster so I have to purchase more"
  - why: Capturing Pokémon is the game's core progression; the span states the player must keep purchasing consumable balls to continue it, making continued play contingent on payment.
- `P_IllusionOfControl` - ok
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out"
  - why: The reviewer asserts the game secretly worsens capture outcomes once the player starts paying, i.e., the determination of results is concealed and manipulated to drive purchases, not left to the player's skill or visible odds.
- `S_FriendSpamImpersonation` - ok
  - span: "3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE"
  - why: The reviewer reports a store review published under their account that they did not write, including fabricated social activity attributed to them — content published as the player, which the boundary rule counts as impersonation by the product.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `5e6a5625-5291-4f0e-897c-1b63c1a26494` - MONOPOLY GO!

> I loved this game until the new season started. Suddenly I get no rewards for inviting friends and getting them to join facebook. I am struggling to get dices and when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way... And today. Well, I cannot log in to the game at all. It keeps giving me an internet connection error which is absolute nonsense. I have connected to 3 different wifi connections. BS!!😡

| | labels |
|---|---|
| gold | `M_Gambling`, `P_RewardMania`, `S_ForcedFellowship` |
| pred | `P_CompleteTheCollection`, `P_RewardMania`, `S_ForcedFellowship` |
| **missed** | `M_Gambling` |
| **spurious** | `P_CompleteTheCollection` |

**Did the model consider what it missed?**

- `M_Gambling` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes several mechanics of MONOPOLY GO!. First, an invite-reward system: they invited friends and got them to join Facebook expecting rewards, which is the Social Pyramid Scheme pattern; the complaint is that the rewards stopped, but the mechanic of being rewarded for recruiting new players is described as the game's design (mirroring the codebook's own Forced Fellowship worked example where an invited friend was not credited). Second, the dice rolls: they saved up 500+ dice, played max bet, and got 'NO LUCK' with no shut downs or bank heists — this describes chance-determined outcomes, but no real money stake is mentioned anywhere, so this is variable reward delivery (Reward Mania), not Gambling; nor is it Illusion of Control since no rigging or concealed mechanism is alleged, just an unlucky run. Third, 'Stickers are duplicates all the way' describes a randomised pool of collectible items yielding duplicates, which implies the player is working toward completing sticker sets (the codebook's own Monopoly GO example establishes stickers are collected to complete albums) — this carries both Reward Mania (unwanted duplicate drops from a randomised pool) and Complete the Collection (the collection goal the duplicates frustrate). The inability to log in due to an internet connection error is attributed to a technical fault, and no design penalty (lost streak, forfeited reward) is described, so R11 suppresses any label there. 'Struggling to get dices' names scarcity but describes no wait/regeneration schedule and no purchase, so it codes nothing on its own. No search is needed; all terms (dice, stickers, shut downs, bank heists) are standard MONOPOLY GO! elements and the codebook itself documents the sticker album system.
```

**Labels assigned**

- `P_CompleteTheCollection` - **SPURIOUS**
  - span: "Stickers are duplicates all the way"
  - why: Stickers in MONOPOLY GO! are collected to complete albums; the complaint about duplicates implies the player is working toward set completion and the duplicates frustrate that goal.
- `P_RewardMania` - ok
  - span: "played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way"
  - why: Unpredictable outcomes of dice rolls and duplicate drops from a randomised sticker pool describe chance-based reward delivery with no monetary stake described, so Reward Mania alone, not Gambling.
- `S_ForcedFellowship` - ok
  - span: "Suddenly I get no rewards for inviting friends and getting them to join facebook"
  - why: The game rewards the player for pulling new people (Facebook friends) into the game; the complaint that rewards stopped confirms the recruitment-for-reward mechanic is the design.

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

- `M_Gambling` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a deliberate interface behavior in 8 Ball Pool: when the player opens the game or enters the 1v1 section, the UI automatically scrolls to and pre-selects the highest-stakes coin table the player's balance can cover. The reviewer attributes a purpose to this design: inducing accidental entry into high-stakes matches so players lose their accumulated coins and must replenish them by buying coins with real money. This is not an outcome-rigging claim (the 'rigged' language refers to the interface, not match results), so Illusion of Control does not apply. Three mechanics are present: (1) the interface directing the player toward a specific option — the auto-scroll/auto-select of the highest table is attention-and-selection steering by the UI; (2) a default option that removes deliberation and confirmation, making accidental loss of holdings easy and funneling toward a real-money purchase — the accidental-purchase/default-to-purchase mechanism; (3) the explicit conversion of real money into the game's currency, since 'forced to buy real ones' describes buying coins with real money. The Mandatory Marathon worked example (accidental high-stakes match entry) is not matched here because no exit-forfeit is described; the loss mechanism here is the mis-click itself, not a blocked exit.
```

**Labels assigned**

- `M_EasyToPurchase` - **SPURIOUS**
  - span: "This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins and are forced to buy real ones."
  - why: The default selection of the highest bet table removes confirmation and deliberation, making accidental loss easy with the stated purpose of driving players into real-money purchases — an accidental-purchase mechanism via a default option.
- `M_IntermediateCurrency` - ok
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: 'Forced to buy real ones' describes real money being converted into the game's coin currency (the currency is the object acquired), establishing the real-money-to-virtual-currency exchange.
- `M_UIMisdirection` - ok
  - span: "Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins."
  - why: The interface automatically steers the player's selection toward the highest-stakes option, and the span ties this direction to a monetary outcome (losing coins that must then be repurchased), satisfying the attention-direction arm with the required purchase bearing.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `cc714d17-863c-4ebd-b14f-989ba17c71c4` - Dice Dreams™️

> I played this game on a different profile. the only reason I gave it five stars is because if you don't it won't let you write a review. if you want to win anything on this game it will cost hundreds of dollars. on the stickers you will never get the last one or two unless you pay a lot of money to get them. this is not a game you want to get addicted to unless you have a endless bank account. it may let you complete a goal maybe one out of hundred times.dont get your hopes up.

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury`, `M_PayToProgress`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_DeceptiveLuxury`, `M_PayToProgress`, `P_CompleteTheCollection`, `P_IllusionOfControl` |
| **missed** | `P_RewardMania` |
| **spurious** | `P_IllusionOfControl` |

**Did the model consider what it missed?**

- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer played Dice Dreams on another profile and is warning others off. The opening claim that the game 'won't let you write a review' without five stars concerns review solicitation, not a codable in-game mechanic under any label here. The substantive mechanics: (1) winning anything is stated to cost hundreds of dollars — payment as the route to progress/advantage; (2) a sticker collection where the final one or two stickers are made unobtainable except by paying — this is simultaneously a collection-completion structure, a paywall on finishing it, and manufactured scarcity of specific items tied directly to purchase; (3) 'it may let you complete a goal maybe one out of hundred times' — the phrasing 'let you' asserts the game controls whether outcomes occur, a claim that results are determined on a hidden schedule rather than by the player's play. The sticker scarcity is built into the items themselves (the last ones never drop) with payment as the remedy, which fits Deceptive Luxury rather than Gambling, since no wager or chance-purchase is explicitly described — the reviewer says you pay to get them. No search is needed: the sticker album mechanic is clear from the review text itself.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "you will never get the last one or two unless you pay a lot of money to get them"
  - why: The final stickers are made deliberately unobtainable through play and are sold as the remedy, so manufactured scarcity bears directly on the purchase.
- `M_PayToProgress` - ok
  - span: "if you want to win anything on this game it will cost hundreds of dollars"
  - why: Winning is stated to be contingent on spending large amounts of money, i.e., payment purchases in-game success.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: The player is working to complete a sticker set, and the missing final pieces are what drives continued play and payment.
- `P_IllusionOfControl` - **SPURIOUS**
  - span: "it may let you complete a goal maybe one out of hundred times"
  - why: 'It may let you complete' asserts the game determines outcomes on a hidden fixed ratio rather than the player's actions deciding them.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `12267c1e-47ba-4984-97c8-768e820ceb1c` - Bingo Blitz™️ - Bingo Games

> not very user-friendly. no apparent reachable goals within a decent amount of time. I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| pred | `M_DeceptiveLuxury`, `M_EasyToPurchase`, `M_IntermediateCurrency`, `M_PayToProgress`, `P_CompleteTheCollection`, `T_Grinding` |
| **missed** | `P_AestheticManipulation` |
| **spurious** | `M_DeceptiveLuxury`, `M_IntermediateCurrency`, `M_PayToProgress` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes Bingo Blitz's photo-collection meta-game. Several mechanics are present. First, progress requires repetition: they 'play round after round to collect photos', a repeated activity tied to advancement (completing sets). Second, the photos form sets the player is trying to complete, and the reviewer frames the uncompleted set as the harm. Third, after every lost round the game interjects an offer to spend extra coins to claim a missing photo, which is a purchase prompt intercepting play at the moment of loss. Fourth, the photos are effectively unobtainable through play ('no apparent reachable goals'), so the paid claim offer functions as a second, costlier route to an item the game makes scarce. Fifth, coins are the thing being spent, and the reviewer closes with 'I've wasted so much money', implying real money was converted into coins and that paying was the route to progress. The claim that promised photos never arrived despite meeting conditions reads as either a fault or deceptive delivery, but there is no clean label for false offer fulfillment, and the reviewer does not describe outcome manipulation of play itself, so no label is drawn from that portion alone.
```

**Labels assigned**

- `M_DeceptiveLuxury` - **SPURIOUS**
  - span: "after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set"
  - why: Photos are scarce through play and, after the player fails to win one, the game offers a second opportunity to obtain the same item at extra coin cost, the Remedy Consumption structure.
- `M_EasyToPurchase` - ok
  - span: "after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have"
  - why: A buying prompt directly intercepts gameplay, triggered every time the player loses a round, matching the insufficient-funds/spent-resource prompt pattern.
- `M_IntermediateCurrency` - **SPURIOUS**  _[span not verbatim]_
  - span: "I'll spend coins on said offer... I've wasted so much money"
  - why: Coins are the currency spent on offers, and the closing statement that the reviewer wasted real money in this same context implies money was converted into coins to fund those purchases.
- `M_PayToProgress` - **SPURIOUS**  _[span not verbatim]_
  - span: "no apparent reachable goals within a decent amount of time... I'll spend coins on said offer... I've wasted so much money"
  - why: Goals are stated to be unreachable in reasonable time through play, and the reviewer describes paying (money wasted on coin offers) as the attempted route to completing sets.
- `P_CompleteTheCollection` - ok  _[span not verbatim]_
  - span: "collect 'photos'... claim a photo I don't have to complete the set"
  - why: The player is compelled to acquire all photos in a set, and the review frames the missing pieces and incomplete set as the core frustration.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The span names the repeated activity (playing round after round) and links it to progress (collecting photos), satisfying Grinding's repetition-tied-to-progress requirement.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (2)

### `45e3e2f0-4612-4d60-9312-3bff055ec9f3` - Merge Cooking®

> I really enjoyed this game until I got to a higher level. About to quit at level 34. Not enough slots to store and play without spending $$ to buy parts. I have 63 spots, on the board and 37 spots in the refrigerator. 98 spaces total, 72 are taken up by parts of generators or lower generators that I can't merge with higher generators yet or high level items like a corn that I am not going to delete. A lambchop can take up to 9 spaces or more of my 26 spaces and I'm not deleting the chicken pie

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_WasteAversion` |
| pred | `M_WasteAversion` |
| **missed** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_PayToProgress` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes a merge game where board and refrigerator storage is capped (63 board spots, 37 refrigerator spots, 98 total), and most of that capacity is consumed by unmergeable generator parts and high-level items they refuse to delete. The storage cap is actively operating on them: a single item like a lambchop can consume 9+ of their 26 free spaces. They state they cannot continue playing without spending real money to buy parts, and are about to quit at level 34. The core mechanic is a capped inventory that pressures the player to either destroy held items or pay their way out of the space crunch. This maps to Waste Aversion (capped inventory forcing item destruction or inventory upgrades). The payment described is to relieve the storage pressure, not to skip a progression gate like a timer or level wall, and the Pay to Progress boundary rule explicitly excludes paying for inventory space, so Pay to Progress does not apply. No repetitive task, timer, chance mechanic, or currency conversion is described.
```

**Labels assigned**

- `M_WasteAversion` - ok
  - span: "98 spaces total, 72 are taken up by parts of generators or lower generators that I can't merge with higher generators yet or high level items like a corn that I am not going to delete. A lambchop can take up to 9 spaces or more of my 26 spaces and I'm not deleting the chicken pie"
  - why: The span shows the inventory cap operating concretely: 72 of 98 slots are occupied by items the player cannot yet use and refuses to destroy, and single items consume a third of the remaining space, realizing the stranded-value pressure the label requires.

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
The reviewer describes Monopoly GO's sticker album system. Three mechanics are visible. First, stickers arrive with random outcomes: 'always get duplicates' describes repeated draws from a randomised pool yielding unwanted repeats, which is variable reward delivery. Second, the player is working to complete sets — a collection goal the review frames as the objective being withheld. Third, finishing the sets is gated behind payment: 'never lets you finish all the sets unless you pay' makes progress (set completion) contingent on spending. Gambling is not assigned because no monetary stake in a chance mechanic is explicitly described — the payment is stated as the route to finishing, not as buying wagers. Intermediate Currency is not assigned because no real-money-to-currency conversion is described.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: Completing the sets — the player's progression goal — is stated to be impossible without payment.
- `P_CompleteTheCollection` - ok
  - span: "never lets you finish all the sets"
  - why: The player is compelled to complete the full sticker sets, and the review frames the unfinishable collection as the harm.
- `P_RewardMania` - ok
  - span: "frustrating when it comes to getting stickers. always get duplicates"
  - why: Stickers are delivered randomly and the player repeatedly receives duplicates, describing unpredictable reward delivery rather than reward value.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (9)

### `95ddadb3-82cd-4042-8a51-cf8b3ed164c2` - Mech Arena - Shooting Game

> You stuck waiting 30 seconds just to connect to a match. This game makes it seem like they give so many rewards but if all just for show. Its difficult to get weapon upgrades or any percs others you stick battling to win. This kind of games just rob you of your time in my opinion

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `T_Grinding` |
| **spurious** | `T_Grinding` |

**Model analysis**

```
The reviewer describes three things. First, a 30-second wait to connect to a match: this is matchmaking/server connection time, a wait arising from the operation of the service rather than a designed time gate like energy regeneration or build timers, so it does not trigger Playing by Appointment. Second, rewards that appear plentiful but are 'just for show': this describes rewards being illusory or low-value, but names no delivery mechanism, no randomness, no complexity — it is an evaluation of reward value, which the Reward Mania boundary rule (reward described only by its value) excludes, and no other label fits a complaint about rewards being decorative. Third, and most substantive: weapon upgrades and perks are difficult to obtain, so the player is 'stuck battling to win' — the player must run the same battling activity repeatedly to make progress because upgrades are hard to come by. This names the repeated activity (battling) tied to progress, matching Grinding. No payment is mentioned anywhere, so Pay to Progress does not apply; 'rob you of your time' is a general evaluation of time investment, not a mechanic (R2).
```

**Labels assigned**

- `T_Grinding` - **SPURIOUS**
  - span: "Its difficult to get weapon upgrades or any percs others you stick battling to win."
  - why: Progress (weapon upgrades, perks) is gated behind repeatedly battling, which the reviewer describes as being 'stuck' doing — a named repetitive activity required to advance.

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
The reviewer praises Bingo Blitz and explicitly mentions in-app purchases, contrasting this game's pricing with other games. The key mechanical description is: 'If your spend $20 on some item you get less then what your actually hoping for, but on here bingo gives you twice the number of your purchase.' This describes spending real money ($20) and receiving a quantity of something in return — in a bingo game this is the purchase of in-game credits/coins, i.e., real money converted into in-game currency, with a bonus on the conversion. Under the 'Purchases denominated in currency' boundary rule, where the currency is the object acquired and real money is the consideration, the conversion is in the span. This satisfies Intermediate Currency regardless of the reviewer's approval (R7, R8). The mention of 'very different modes an events to get into' names modes and events but describes no schedule, expiry, pressure, or mechanic attached to them, so it does not support Playing by Appointment or FOMO. No timers, waits, ads, grinding, social mechanics, or chance-based purchases are described. No search is needed: the purchase mechanic is clear from the text.
```

**Labels assigned**

- `M_IntermediateCurrency` - **SPURIOUS**
  - span: "If your spend $20 on some item you get less then what your actually hoping for, but on here bingo gives you twice the number of your purchase"
  - why: The span describes spending real money ($20) and receiving a quantity of in-game value (bingo credits) in return, i.e., real money converted into in-game currency, with the game awarding a bonus on the exchange.

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
The reviewer describes a base-builder with two core complaints. First, the gameplay loop is called a 'grinder' — repetitive, tedious tasks performed to progress, which is the canonical Grinding pattern. Second, the game runs competitive events that players cannot win without spending: 'no opportunity for a general player to win an event', 'Zero skill pay to win', and the observation that the last event winner spent 30k. Events where players compete against each other for a win is Competition, and payment being the decisive route to winning the event is Pay to Win, which is a low-level instance of Pay to Progress. The complaint about other players perpetuating the spending problem is social commentary, not a described mechanic, so nothing else follows from it. No term in the review needs external resolution.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "there is absolutely no opportunity for a general player to win an event. Zero skill pay to play. Zero skill pay to win."
  - why: Winning events is stated to be contingent on spending money rather than skill, granting victory to players who pay.
- `S_Competition` - ok
  - span: "no opportunity for a general player to win an event"
  - why: Events pit players against each other for a win, with one winner outspending the rest (30k) to take the event.
- `T_Grinding` - **SPURIOUS**
  - span: "Same old same old grinder."
  - why: The reviewer characterises the core loop as a 'grinder' — repetitive, tedious tasks performed in order to progress, emphasizing time invested over skill.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `3c46f5e0-6091-43dc-94a0-e3af3259a63d` - Cashman Casino Slots Games

> Resently cashman had changed it's bingo rewards and daily rewards. However lve found that I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards. The most I can seem to get on the timed rewards is 40,000. I'd not pay just to get my daily rewards. So I'm deleting them.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_WasteAversion`, `T_DailyRewards` |
| pred | `M_IntermediateCurrency`, `M_PayToProgress`, `M_WasteAversion`, `T_DailyRewards`, `T_PlayingByAppointment` |
| **spurious** | `M_IntermediateCurrency`, `T_PlayingByAppointment` |

**Model analysis**

```
The reviewer describes a slots casino economy built around coins. The game recently changed its daily reward system so that completing the daily rewards now requires betting 50,000 coins. The free route, the 'timed rewards' (free coin drops on an in-game timer), caps out around 40,000, leaving the player permanently short of the threshold. The reviewer reads the design as engineered so that the only way to complete the daily rewards is to pay for coins, and refuses, deleting the game. This carries several mechanics: a daily reward system with tasks that must be completed (Daily Rewards); timed free-coin rewards on a schedule that gate progress (Playing by Appointment); a paid route that fills the gap the free route cannot (Pay to Progress); real money implied as converting into the bettable coin currency (Intermediate Currency, via 'I'd not pay just to get my daily rewards'); and a concrete, realized shortfall of 10,000 coins below the target, the small-gap design that prompts a top-up purchase (Waste Aversion).
```

**Labels assigned**

- `M_IntermediateCurrency` - **SPURIOUS**
  - span: "I can't get my daily rewards unless I bet 50,000"
  - why: Progress is denominated in a bettable coin currency, and 'I'd not pay just to get my daily rewards' implies real money converts into those coins to reach the threshold.
- `M_PayToProgress` - ok
  - span: "I'd not pay just to get my daily rewards"
  - why: The free timed rewards cap below the required bet, so completing the daily rewards is contingent on paying; the reviewer's refusal to pay confirms the paid route exists.
- `M_WasteAversion` - ok
  - span: "unless I bet 50,000 with out it I can't complete my daily rewards. The most I can seem to get on the timed rewards is 40,000"
  - why: The span shows the concrete gap: 40,000 obtainable free against a 50,000 requirement, a small engineered difference that pushes the player toward buying coins.
- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The game runs a daily reward system with completion requirements; failing to meet the requirement forfeits that day's rewards.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "The most I can seem to get on the timed rewards is 40,000"
  - why: Free coins arrive on the game's timer ('timed rewards'), and this schedule gates how much the player can bet toward the daily target.

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
The reviewer describes late-game Gardenscapes match-3 play. Three mechanics are described. First, a lives system gates play: lives run out multiple times a day, implying a regeneration schedule that forces the player to stop and return later rather than play when they want. Second, progress is described as requiring payment: add-ons must be bought to get through levels, and playing without paying is called a waste of time. Third, the activity required for progress is repetitive: 5-7 days spent retrying the same level, beating every alternate level only after repeated attempts. The closing remark about wasted money and time reports investment already written off while the reviewer is actively uninstalling, which per the counterexample for Easy to Get Hard to Lose does not qualify, since the span shows disengagement rather than accumulated value operating on the choice to stay. The high level number (8416) alone does not establish Infinite Treadmill, since nothing says the game extends beyond completion. No currency conversion, chance mechanics, or social features are described.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying"
  - why: Further progress is stated to require purchasing add-ons, with the free path described as futile.
- `T_Grinding` - ok
  - span: "avg 5-7 days per level"
  - why: Progress requires repeated attempts at the same level over many days, identifying the repetitive activity required to advance.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "I run out of lives 3-4 times daily to beat every alternate level"
  - why: Lives deplete several times a day and must regenerate before play can resume, imposing a game-defined schedule on sessions.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `32c623b4-0249-469e-968c-94f60c7fe3c2` - Royal Match

> It's an interesting game but the developers should pls try to include new cards in every card pack because I noticed when one is almost close to completing a set, new cards don't appear again especially when the set is almost expiring. So after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion because they don't add new sets to the cards once the collection is about to end.

| | labels |
|---|---|
| gold | `P_CompleteTheCollection`, `T_PlayingByAppointment` |
| pred | `P_CompleteTheCollection`, `P_RewardMania`, `T_PlayingByAppointment` |
| **spurious** | `P_RewardMania` |

**Model analysis**

```
The reviewer describes Royal Match's card collection feature: players open card packs to collect cards and complete themed sets, and completing a set before it expires yields a reward. Three mechanics are described. First, the collection compulsion itself: the player is working to complete sets of 125 cards and frames missing the completion reward as the harm. Second, the pack delivery system: cards arrive in packs, and near set completion new cards stop appearing, meaning the player keeps receiving duplicate or unwanted cards from a randomised pool while chasing the last missing ones. This describes how rewards are delivered, i.e. repeated attempts and duplicate drops, which is Reward Mania's territory. Third, the sets are time-limited: the reviewer says the set is 'almost expiring' and that the player misses the completion reward when the collection ends. This is a reward expiring on the game's clock, with the span describing the schedule and the loss, which the codebook assigns to Playing by Appointment rather than FOMO (no anticipatory anxiety or pressure-to-return is described). No monetary stake is mentioned anywhere, so Gambling, Pay to Progress, and Deceptive Luxury do not apply: the scarcity of new cards is never tied to a price or purchase in the span. No purchase prompts, ads, social mechanics, or downloads are described.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "when one is almost close to completing a set"
  - why: The player is pursuing completion of card sets and the review frames the unobtainable final cards and lost completion reward as the central harm.
- `P_RewardMania` - **SPURIOUS**
  - span: "I noticed when one is almost close to completing a set, new cards don't appear again"
  - why: Describes the delivery of cards from packs: repeated openings yield duplicates and the needed new cards stop dropping, i.e. unpredictable delivery and repeated attempts to obtain specific items from a randomised pool.
- `T_PlayingByAppointment` - ok
  - span: "especially when the set is almost expiring. So after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion"
  - why: The completion reward expires on the game's clock and the span describes the schedule and the forfeited reward, with no felt pressure described, so it codes Playing by Appointment rather than FOMO.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b93c432d-19c0-4c6c-a2d4-bb9b21a436f3` - Dice Dreams™️

> A literal brain-rot game no wonder why they're tryna promote it through Free Cash. Also if you're thinking of making in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates! A real SCAM. Play it if u want but there are games that are actually good also, DON'T GET IN-APP PURCHASES!

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_Gambling`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_EasyToGetHardToLose`, `P_RewardMania` |
| **spurious** | `M_Gambling`, `P_EasyToGetHardToLose` |

**Model analysis**

```
The reviewer is describing a sticker/card album system in Dice Dreams. First, there is a collection mechanic: they were two cards short of completing an album that pays a grand prize, which is a partially completed goal with a reward attached. Second, they spent real money on a 'deal' whose outcome was chance-based: the pack was supposed to deliver needed new cards but instead returned duplicates from a randomised pool. That is simultaneously a real-money stake on a chance outcome (Gambling) and an unpredictable reward delivery that yields duplicate/unwanted drops (Reward Mania). Third, the deal's wording is described as deceptive: it 'promised NEW cards' and delivered duplicates, which is misleading copy on a purchase offer. The near-complete album also operated as endowed progress, pulling the reviewer into the purchase because they were only two cards away. The 'Free Cash' promotion is out-of-game/third-party marketing, which R13 excludes. No currency conversion is described (the deal is bought directly), so Intermediate Currency does not apply.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "i bought a deal which promised i would get NEW cards, and all i got were useless duplicates"
  - why: Real money was spent on a card deal with a chance-based outcome: the needed cards or worthless duplicates.
- `P_AestheticManipulation` - ok
  - span: "a deal which promised i would get NEW cards"
  - why: The deception is in what the offer says: the deal's copy promised new cards but delivered duplicates, misleading wording on a purchase.
- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The player is working to complete a full card album for a prize, and the missing pieces are framed as the driver of their behaviour.
- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "I had two cards left which would grant me the grand prize for completing an album, so i bought a deal"
  - why: The nearly complete album (only two cards left) is what pushed the reviewer into spending, a partially completed goal they could not abandon.
- `P_RewardMania` - ok
  - span: "all i got were useless duplicates"
  - why: Card delivery is unpredictable and yields duplicate, unwanted drops from a randomised pool; assigned alongside Gambling per the Gambling vs Reward Mania boundary rule.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `727cc804-9d4b-48ef-8774-2799a2a8de08` - Genshin Impact

> with every incoming patch, we get less and less rewards and for me that wouldn't be a problem but the Meta changes more and more every single day basically forcing us to pull for new characters if we want to actually do damage. the game is getting more and more pay 2 win and the quality of the game is becoming lower. in the new archon quest when we were talking to mavuika, a multi billion dollar company just put an insanely bad picture of Natlans scenery as the background, y'all can do better.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_PowerCreep`, `P_RewardMania` |
| pred | `M_Gambling`, `M_PayToProgress`, `M_PowerCreep`, `P_RewardMania` |
| **spurious** | `M_Gambling` |

**Model analysis**

```
The reviewer describes several mechanics in Genshin Impact. First, a shifting meta that makes older characters inadequate: 'Meta changes more and more every single day basically forcing us to pull for new characters if we want to actually do damage' — this is the subtle Power Creep form where the recency qualifier (newer characters needed to deal damage) implies older, already-obtained characters have lost value through new releases. Second, the mechanism used to obtain those new characters is 'pulls', i.e., gacha draws, a chance-based reward delivery system — Reward Mania. Third, the reviewer states the game is 'pay 2 win', describing money spent for in-game advantage, which is Pay to Win under Pay to Progress. Fourth, the combination of pulls (a chance mechanic) and the stated monetary stake (pay to win) means real money is being spent on a game of chance for a reward, which supports Gambling under the R9/Gambling vs Reward Mania rule — the stake is described via 'pay 2 win' and the chance mechanic via 'pull'. No intermediate currency is named (no primogems, wishes, or genesis crystals), so Intermediate Currency is not assigned. The complaint about the bad background picture in the archon quest is an evaluation of art quality, not a manipulative design mechanic, and codes NONE under R2. 'Less and less rewards' describes reward value shrinking, not delivery mechanics, and does not lift to Reward Mania on its own.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "basically forcing us to pull for new characters if we want to actually do damage. the game is getting more and more pay 2 win"
  - why: The monetary stake ('pay 2 win') funds the chance mechanic ('pull'), so real money is spent on a game of chance for a reward; analogous to the gacha-costs-money worked example.
- `M_PayToProgress` - ok
  - span: "the game is getting more and more pay 2 win"
  - why: The reviewer explicitly describes spending money as conferring in-game advantage (damage via new characters), which is Pay to Win.
- `M_PowerCreep` - ok
  - span: "the Meta changes more and more every single day basically forcing us to pull for new characters if we want to actually do damage"
  - why: Stating that newer characters are needed to deal damage asserts that older, already-obtained characters no longer do — value lost after acquisition through new releases, per the subtle-form worked example.
- `P_RewardMania` - ok
  - span: "forcing us to pull for new characters"
  - why: 'Pull' names the gacha draw mechanic, a chance-based reward delivery system, regardless of the reviewer's disapproval (R7/R8).

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
The reviewer is a former paying player reacting to an update in Total Battle: War Strategy. Three things are described. First, growth in the game requires spending: 'You have to spend to have any meaningful growth,' which is a direct statement that progress is contingent on payment. Second, the update devalued what players had already bought: removing player-versus-player combat (framed as 'get rid of open silver') rendered prior purchases pointless — 'they go and make it all pointless' and 'They just screwed everyone over who wasted money on this game.' That is purchased value destroyed by a design change after acquisition, which fits Power Creep's definition of diminishing the value of purchased items over time. Third, the reviewer calls the current state 'boring farmville,' but this is a general characterisation of gameplay quality with no specific repetitive activity named and no explicit link to a progress loop, so it does not satisfy Grinding under R2. Competition is not assigned: the span describes PvP as removed, i.e., not currently present (R12). Easy to Get, Hard to Lose is not assigned: the investment is described as already forfeited and the reviewer is disengaging and warning others away, per that label's counterexample.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You have to spend to have any meaningful growth"
  - why: Progress ('meaningful growth') is stated to require spending money, meeting the canonical Pay to Progress definition directly.
- `M_PowerCreep` - **SPURIOUS**
  - span: "they go and make it all pointless by getting rid of any player vs player, so it's now just boring farmville. Gotta be the dumbest company i've ever dealt with. They just screwed everyone over who wasted money on this game."
  - why: An update removed the PvP context that gave purchased progress its value, so money previously spent became pointless — value of purchased items diminished after acquisition by a design change.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_Gambling` | 2 | 2 |
| `M_IntermediateCurrency` | 1 | 3 |
| `T_PlayingByAppointment` | 1 | 2 |
| `M_PayToProgress` | 1 | 2 |
| `P_RewardMania` | 1 | 1 |
| `T_Grinding` | 0 | 2 |
| `M_DeceptiveLuxury` | 1 | 1 |
| `S_Reciprocity` | 2 | 0 |
| `T_MandatoryMarathon` | 1 | 0 |
| `M_PowerCreep` | 0 | 1 |
| `P_CompleteTheCollection` | 0 | 1 |
| `M_UIMisdirection` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `M_EasyToPurchase` | 0 | 1 |
| `S_Competition` | 1 | 0 |
| `P_AestheticManipulation` | 1 | 0 |
| `T_Advertisement` | 1 | 0 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `P_IllusionOfControl` | 0 | 1 |

