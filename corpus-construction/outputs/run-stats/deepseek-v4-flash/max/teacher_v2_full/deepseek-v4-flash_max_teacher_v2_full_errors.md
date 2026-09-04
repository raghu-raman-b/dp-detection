# Error review - deepseek-v4-flash_max_teacher_v2_full

`deepseek-v4-flash` / reasoning `max` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `aad355174ac4`  
micro-F1 **0.829** (P 0.872 / R 0.791) - **21 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 4 | said NONE, gold had labels |
| SWAP | 5 | picked different labels than gold |
| MISSED ONLY | 7 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 5 | found all gold, added extras |

## The diagnostic that matters

Of **18** missed labels, **3** (17%) were named in the model's own analysis and dropped anyway; **15** (83%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `S_Competition` | 1 | 2 |
| `S_Reciprocity` | 1 | 1 |
| `P_RewardMania` | 0 | 2 |
| `M_Gambling` | 0 | 2 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `M_PayToProgress` | 0 | 1 |
| `M_RecurringFee` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `P_AestheticManipulation` | 0 | 1 |
| `M_WasteAversion` | 0 | 1 |
| `S_ForcedFellowship` | 0 | 1 |
| `T_Grinding` | 1 | 0 |
| `T_PlayingByAppointment` | 0 | 1 |

## Missed everything (predicted NONE) (4)

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
The review is a short feature-request list. Every numbered item asks the developers to add or change something: auctions for cosmetics paid in in-game currency, removal of the delete option for decorated obstacles, an account-toggling widget that displays remaining upgrade time, and hidden advanced statistics for troops. Under R12, requests, suggestions, and hypothetical additions do not trigger tags for the proposed mechanics, even where the surrounding game context (e.g., upgrade timers, an in-game currency) makes the request intelligible. The review never describes a currently present design behaviour that fits any label: no complaint about imposed wait schedules or timers, no real-money-to-currency conversion described, no deceptive or manipulative mechanic named. It is a positive rating with suggestions, so nothing is codable.
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
The review is a bug report for the latest update. Every complaint is attributed to technical malfunction: crashes when opening gifts or trading, lag when throwing Pokéballs, and lag, freezing, and unresponsive controls in PvP and Team Rocket battles, with the opponent continuing to attack while the player's game is frozen. There is no description of any deliberate design rule or game mechanic operating on the player — no timers, payment, social obligation, reward schedule, or forfeiture rule. Under R11, behavior attributed to bugs, glitches, lag, or crashes is not coded as a dark pattern because dark patterns are deliberate design choices rather than technical faults. The freeze during battle does not describe an explicit exit rule (e.g., leaving forfeits progress); the loss of combat responsiveness is itself the malfunction, not a designed penalty that a malfunction merely triggered. No label satisfies R2 and R3.
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
The review reports a regression: after one of the updates, the reviewer can no longer request troops from their clan and asks for it to be fixed. Requesting troops from clanmates could ordinarily relate to a social resource-transfer mechanic (Reciprocity), but the review describes the feature as broken by a technical fault, not as a functioning design that imposes an obligation or exchange. R11 suppresses dark-pattern labels when the text attributes a specific behaviour to a bug, glitch, or technical fault, because dark patterns are deliberate design choices rather than malfunctions. Nothing in the text describes any other game mechanic or design behaviour.
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
The reviewer makes two points, both framed as requests or opinions rather than reports of existing mechanics. First, they ask for an in-app way to trade stickers, noting that not everyone is on Facebook. The Facebook mention implies some social/account integration exists, but the text describes nothing the game currently does with it: no messages sent, no contacts accessed, no invitation posted, and the request is explicitly for a feature that does not exist. Under R12, requests for proposed mechanics do not trigger tags. Second, they argue that a purchased booster should be usable when challenged by another player, implying the booster is currently unusable in challenged matches. This describes a usage restriction on a purchased item, but no listed pattern matches: it is not a loss of value over time (Power Creep), not stranded leftover currency or a shortfall (Waste Aversion), and not a payment wall on progress. It reads as a dissatisfaction with a mode restriction, not a dark pattern described by the codebook. The 'addictive' comment is a general evaluation and codes NONE under R2.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (5)

### `5e6a5625-5291-4f0e-897c-1b63c1a26494` - MONOPOLY GO!

> I loved this game until the new season started. Suddenly I get no rewards for inviting friends and getting them to join facebook. I am struggling to get dices and when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way... And today. Well, I cannot log in to the game at all. It keeps giving me an internet connection error which is absolute nonsense. I have connected to 3 different wifi connections. BS!!😡

| | labels |
|---|---|
| gold | `M_Gambling`, `P_RewardMania`, `S_ForcedFellowship` |
| pred | `P_CompleteTheCollection`, `P_RewardMania` |
| **missed** | `M_Gambling`, `S_ForcedFellowship` |
| **spurious** | `P_CompleteTheCollection` |

**Did the model consider what it missed?**

- `M_Gambling` - never mentioned -> **attention / recall**
- `S_ForcedFellowship` - never mentioned -> **attention / recall**

**Model analysis**

```
The review lists four separate grievances at the start of a new season: (1) the referral incentive that previously rewarded inviting Facebook friends now pays nothing — a mechanic the reviewer describes as having been removed, not one active in the game, so under R12 it cannot be coded; (2) having accumulated over 500 dice and played at max bet, the reviewer experienced no shutdowns or bank heists — a losing/unlucky run framed as frustration, without any claim that the game conceals or fixes outcomes, so this is not Illusion of Control; (3) sticker packs keep producing duplicates, which in MONOPOLY GO blocks progress toward completing collectible sticker albums; and (4) a login failure attributed to an internet connection error, which is a technical fault suppressed by R11. The sticker complaint carries two dimensions: the random drop mechanism delivering unwanted duplicates (Reward Mania) and the underlying drive to complete the sticker album collection (Complete the Collection). A web search was used to confirm what stickers are for in the game.
```

**Labels assigned**

- `P_CompleteTheCollection` - **SPURIOUS**
  - span: "Stickers are duplicates all the way..."
  - why: The reviewer is gathering stickers toward an album collection, and the frustration with duplicate drops implies the drive to obtain every unique sticker; the search confirms stickers feed album-completion rewards.
- `P_RewardMania` - ok
  - span: "Stickers are duplicates all the way..."
  - why: The span describes the sticker-pack reward delivery as producing repeat duplicates from a randomised pool, sustaining play through the unpredictable draw of the missing items.

**Search:** `MONOPOLY GO what are stickers and sticker albums used for` -> Stickers in MONOPOLY GO are collectible items used to complete sticker albums, and completing an album grants significant bonus rewards; duplicate stickers do not fill album slots.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

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
The reviewer describes one continuous design behaviour in the 1v1 lobby of 8 Ball Pool: the interface automatically scrolls to and pre-selects the highest-stakes table the player can afford whenever the game opens or the section is entered. Because the highest bet is already selected by default, an ordinary tap or mis-tap commits the player to a match that can drain all of their coins. The reviewer names the purpose explicitly: to force accidental mis-clicks, strip players of earned coins, and drive them to buy coins with real money. Three distinct mechanics sit in this account. First, an interface whose defaults steer the player toward the most expensive option and make a mis-tap costly — that is attention/selection manipulation by UI design, connected by the reviewer to spending. Second, the outcome that losing all coins compels buying more to keep playing — payment restoring the ability to play is pay-to-continue. Third, the purchase itself: coins are the object bought with real money, which is the real-money-to-currency conversion. The 'Default Table Lock' request is a proposed fix for the existing behaviour and does not itself add a label.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "are forced to buy real ones"
  - why: 'Real ones' refers to coins purchased with real money, describing the exchange of real currency for the in-game coin currency — the conversion relation that defines Intermediate Currency.
- `M_PayToProgress` - **SPURIOUS**
  - span: "so players lose all their hard-earned coins and are forced to buy real ones"
  - why: Losing all coins through the rigged default leaves the player unable to keep playing at their level, and the only way back is buying coins with real money, i.e., continued play becomes contingent on payment.
- `M_UIMisdirection` - ok
  - span: "Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins and are forced to buy real ones"
  - why: The interface pre-selects and centres the most expensive table so a routine tap becomes an unintended high-stakes wager; the span explicitly frames this as a deliberate dark-UX device whose payoff is a coerced real-money purchase, satisfying UI Misdirection's purchase-bearing arm.

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
The reviewer is describing Dice Dreams as a game where winning and completing goals requires heavy spending, and where a sticker collection exists whose final items are never obtained through normal play, only through paying. The sticker mechanic is a completion set: the last one or two pieces are withheld from natural acquisition and the purchase is the only route to finish, which simultaneously describes a pay gate on progress, the compulsion to complete a collection, and a deliberately manufactured scarcity used to monetize completion. The final sentence, 'it may let you complete a goal maybe one out of hundred times', attributes the near-total failure to complete goals to the game's own determination of outcomes, i.e., a fixed, engineered success ratio rather than player skill or ordinary bad luck. The rating-gating complaint ('if you don't it won't let you write a review') is a store-listing behaviour, not an in-game mechanic, so it is not coded.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: The span asserts the final stickers categorically never drop through normal play ('never get') — a scarcity invented by the developer — and that paying is the only remedy, tying manufactured rarity directly to purchase.
- `M_PayToProgress` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: Finishing the sticker collection is stated to be impossible through play and contingent on payment, blocking completion unless money is spent.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: The sticker set is a collection whose final items are withheld from the player; the review's framing shows the drive to complete the set being exploited to extract payment for the last pieces.
- `P_IllusionOfControl` - **SPURIOUS**
  - span: "it may let you complete a goal maybe one out of hundred times"
  - why: 'Let you' attributes the decision of whether goals get completed to the game, asserting an engineered success ratio of roughly one in a hundred rather than outcomes determined by the player's own play.

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

- `T_Grinding` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes late-game Gardenscapes difficulty. Three design behaviours surface. First, a lives system: they run out of lives several times a day and take 5–7 days per level, which means each level attempt is throttled by life regeneration timers that force the player to wait or return later. Second, payment as the escape from that friction: 'must buy add ons' or the game is not passable, with an explicit free-vs-paying contrast ('pure time waste if you're not paying'), so purchases are framed as the route through level roadblocks. Third, a closing reflection on sunk time and money; however, the reviewer is actively disengaging and frames the investment as wasted rather than as something that made quitting hard, so no sunk-cost retention mechanic is being described as operating on them. The high level number and per-level slowness are progress complaints, not descriptions of repetitive activity or endless content expansion, so Grinding and Infinite Treadmill are not supported.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying."
  - why: The reviewer states levels cannot be passed without buying add-ons and that not paying makes the game a time sink, describing payment as the route through the roadblock.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "I run out of lives 3-4 times daily to beat every alternate level"
  - why: Running out of lives multiple times a day implies each attempt is gated by a timer-based refill, so play must follow the game's life-regeneration schedule rather than the player's own.

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
The review's substance is a failed attempt to finish a card album. The reviewer was two cards short of the grand prize awarded for completing the album, so they spent real money on a deal that was presented as delivering NEW cards; instead the deal returned duplicate cards, which are useless toward completing the album. The mechanics this reveals: an album-completion goal that collects cards toward a grand prize (Complete the Collection), and card deals bought with real money whose contents are drawn from a randomized pool, producing duplicates rather than the missing pieces (a chance-based paid reward). The 'Free Cash' promotion is external marketing and outside the app, so it is not coded. The scam complaint is an evaluation of the purchase outcome, not itself a mechanic, but the underlying design it describes — paid card packs with random, duplicating contents blocking the final collection goal — is what the labels capture.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "i bought a deal which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: Real money is spent on a card deal whose contents are drawn at random, evidenced by the reviewer receiving useless duplicates instead of the specific missing cards they needed.
- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The reviewer is positioned two items short of completing an album set, and the duplicate cards keep the collection unfinished, showing a collection-completion structure driving the player's spending.
- `P_RewardMania` - ok
  - span: "all i got were useless duplicates!"
  - why: The complaint describes the delivery of duplicate drops from a randomized card pool, the variable-reward delivery mechanism that sustains continued engagement rather than the reward's value.

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
The reviewer describes a wheel feature inside a casino slot game: after the wheel stops on a high prize (100 million with a 5x multiplier), the genie character moves the wheel again to a 'spin tag' and the resulting prize is lower (48 million). The complaint is that the game overrides the result the player had already won, and the reviewer asks for a choice to keep the prize or spin. Nothing about real money, purchases, schedules, waiting, or social features is described, so monetary, social, and temporal classes do not apply. The core described behavior is the game itself altering the outcome of a spin after the fact, repeatedly ('in multiple times') and by design (a wish for a keep-or-spin choice), which asserts that the displayed result is not the final outcome and the wheel's determination is manipulated by the game rather than left to the player.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "in multiple times whe the wheel spin after stopping on a great price the genie move the wheel to a spin tag, and then the prices after the spin are way lower than the original price, from 100 million with 5x multiplier to a 48 million"
  - why: The genie overriding a landed winning result with a lower one asserts that the game manipulates the outcome of the wheel, deceiving the player about the value of the result they actually receive.

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
The reviewer describes several distinct mechanics: a customer service failure over purchased diamonds and a missing game element, the general free-to-play friendliness of the game, an advisory against buying a pass, and a recommendation to source lives through friends and team membership. The customer-service issue describes a fault in the delivery of a purchased item and does not clearly describe a dark pattern design. The absence of needing to pay to win shows that progress is not gated. The admonition about the pass describes a purchasable pass but does not describe its clock, price, or value. The friend/team/trade-lives recommendation, however, implies a resource donation feature for gaining lives, which matches Reciprocity's indicator that the text explicitly names the transfer: asking for and donating lives is an instance of a support mechanism for playing on. The reviewer is not describing being obligated to reciprocate, but the explicit mention of a send/request lives mechanic is what Reciprocity's indicator requires.
```

**Labels assigned**

- `S_Reciprocity` - ok
  - span: "Get friends and a team and trade lives."
  - why: The span names the actual resource transfer between players—donating or trading lives—which establishes the presence of a social resource-donation feature in the game.

**Search:** `Fishdom mobile game "pass" purchase what is it` -> Fishdom's mobile game pass offers extra rewards and features for a fee. It is optional and not required to play.

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
The review splits into two distinct parts. First, the writer (or someone writing under the account) claims that after the player began purchasing Poké Balls, capture attempts began failing more often — "they keep breaking out" — so balls are consumed faster and more must be bought. That is an assertion that the game secretly alters the outcome determination (catch odds) based on purchase behaviour to drive further spending; no free alternative or paywall is described, and no currency conversion is named, so the monetary reading is the alleged rigging itself. Second, the closing edit states the review was posted under the account without the account holder's authorship and that its quoted conversations never happened — content published as the player that the player disclaims, which the Friend Spam / Impersonation destination rule treats as impersonation performed through the player's identity. No search is needed: Poké Balls and the capture mechanic are clear from the review and the supplied game name.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: The reviewer asserts the game secretly lowers capture success once the player buys balls, engineering faster consumption to force more purchases — concealed manipulation of outcomes to encourage continued spending.
- `S_FriendSpamImpersonation` - ok
  - span: "I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE"
  - why: The account holder states a review was posted under their name that they did not write and whose claims they disavow, implying the game published fabricated content through the player's identity.

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
The reviewer is describing Cashman Casino's revised daily reward system. They describe three linked things: daily rewards that can only be completed by wagering a very high amount (bet 50,000); a free source of coins ("timed rewards") that caps out at 40,000 — below that wager requirement; and their refusal to spend real money to bridge the gap, leading them to uninstall. The daily reward is a resetting daily task whose reward is forfeited when the required wager cannot be met. The 40,000-vs-50,000 gap plus "I'd not pay" implies that completing the daily reward is contingent on buying coins with real money, since the free route falls short of the threshold. No chance-mechanic, social, or scheduling elements beyond the daily cycle are described in enough detail to code.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "The most I can seem to get on the timed rewards is 40,000. I'd not pay just to get my daily rewards"
  - why: The reviewer's free coin income cannot reach the required wager, and payment is the only way to close the gap and complete the daily rewards, so reaching that reward milestone is contingent on spending money.
- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The daily reward is gated behind a resetting daily task (a 50,000 wager), and failing to meet it means the day's reward cannot be claimed — an active consequence for not completing the daily requirement.

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
The reviewer describes hitting a storage ceiling high in the game. They count the slots they own (63 on the board plus 37 in the refrigerator), report that 72 of those 98 spaces are taken by merge components they cannot currently merge, and say they will not delete high-level food items such as the corn or the chicken pie. The complaint is that the capped inventory blocks continued play unless the player spends money. The search clarified that 'parts' in this game are mergeable item components rather than an unrelated term, so the span about parts occupying slots is about inventory being consumed by merge materials. The mechanic described is a capacity limit that pressures the player to destroy items or pay to expand storage.
```

**Labels assigned**

- `M_WasteAversion` - ok
  - span: "Not enough slots to store and play without spending $$ to buy parts. I have 63 spots, on the board and 37 spots in the refrigerator. 98 spaces total, 72 are taken up by parts of generators or lower generators that I can't merge with higher generators yet or high level items like a corn that I am not going to delete."
  - why: The player's storage is nearly full with valuable merge components and high-level items they refuse to delete, so the only acceptable route to keep playing is paying to expand the capped inventory; the capacity limit forces the destroy-or-expand choice.

**Search:** `Merge Cooking game "parts" storage slots buy - what does parts mean` -> In Merge Cooking, parts refer to mergeable item components used to upgrade generators; they are normal in-game items, not a separate fee, and they fill the player's storage slots.

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
The reviewer describes the mid-game loop in Last War: repeatedly gathering resources while defending against raids, all to gain levels that unlock more attempts at a side mini-game. The word 'grinding' names the repetitive resource-collection task directly and ties it to progression ('so you can level up'), which is Grinding. The sentence about bigger alliances attacking smaller ones and taking their resources describes an asymmetric player-versus-player structure: stronger groups are rewarded with the defender's resources for raiding weaker groups. That matches the Encourages Anti-Social Behavior boundary rule about stronger players rewarded for attacking weaker ones, not merely ordinary sanctioned raid competition. The vague comment about advertisement becoming 'not that great' describes no forced or rewarded ad mechanic and codes nothing. The closing statement of dedication and disappointment reports time invested and dissatisfaction, but shows no mechanism raising the cost of leaving, so it does not reach Easy to Get, Hard to Lose. No currency, timers, daily incentives, or payment are described.
```

**Labels assigned**

- `S_EncouragesAntiSocialBehavior` - ok
  - span: "The bigger alliances all just attack the smaller alliances and take their resources"
  - why: The design lets larger alliances raid smaller ones and directly take their resources, so the harmful act and the aggressor's gain appear in the same span, with the asymmetry between strong and weak made explicit.
- `T_Grinding` - ok
  - span: "It's just grinding resources trying not to get raided so you can level up"
  - why: The reviewer names the repetitive task ('grinding resources') and links it to advancement ('so you can level up'), describing the activity required for progress rather than just slow progress in the abstract.

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
The reviewer is talking about the sticker album collection mechanic in MONOPOLY GO!. Sticker packs come from a randomised reward pool and produce duplicate stickers, which the reviewer experiences as the reason the collection stays incomplete. The game is described as blocking completion of the full set of albums unless the player pays. Three mechanics sit in this short text: a random delivery system whose duplicates deny the desired items, a collection completion goal the player is being pulled toward, and a pay gate placed on finishing that collection.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: Finishing the sticker sets is stated to be contingent on payment, so further progress in the collection is gated behind spending money.
- `P_CompleteTheCollection` - ok
  - span: "never lets you finish all the sets"
  - why: The reviewer is pursuing the full sticker album sets, and the game is framed as withholding completion of the collection, capitalising on the drive to collect all items.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: The span describes how rewards are delivered from a randomised pool, with repeated unwanted duplicate drops rather than the items wanted, which is the delivery-schedule mechanism Reward Mania covers.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (5)

### `33c422de-1a84-4df9-accd-cdf8bfc96295` - Dark War Survival

> No ingenuity for a base builder. Same old same old grinder. After a few weeks, it became abundantly clear that there is absolutely no opportunity for a general player to win an event. Zero skill pay to play. Zero skill pay to win. Calculated total spent on last event was 30k to win. Wish serious gamers would stop perpetuating the problem by continuing to spend obnoxious amounts of money on a little app that you just want to have a little fun on.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `S_Competition` |
| pred | `M_PayToProgress`, `S_Competition`, `T_Grinding` |
| **spurious** | `T_Grinding` |

**Model analysis**

```
The reviewer describes a base-builder war game across three mechanics. First, they characterise the game itself as an unoriginal 'grinder', meaning progress runs on repetitive task play rather than design ingenuity. Second, they describe the event system: after weeks of play it became clear that a general (non-spending) player cannot win an event, and that winning is determined by money rather than skill — 'zero skill pay to play, zero skill pay to win' is a pay-to-win formulation, and the $30k figure for the last event shows victory priced, not earned. Third, that account implies events pit players against each other in competition where big spenders dominate and ordinary players are locked out. The closing sentence about serious gamers spending money is a plea about other players' conduct, not a game mechanic, so it codes nothing.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "there is absolutely no opportunity for a general player to win an event. Zero skill pay to play. Zero skill pay to win."
  - why: Event victory is closed to non-paying players ('no opportunity for a general player') and outcomes are decided by spending rather than skill ('zero skill pay to win'), both forms of paying to progress/win.
- `S_Competition` - ok
  - span: "there is absolutely no opportunity for a general player to win an event"
  - why: Winning events implies ranked competition among players; the review describes that competition as dominated by spenders (with the last event costing 30k to win), so ordinary players are pitted against paying rivals.
- `T_Grinding` - **SPURIOUS**
  - span: "Same old same old grinder."
  - why: The reviewer names the game a 'grinder', describing a design whose progress model is repetitive grinding rather than anything inventive.

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
The reviewer is describing the structural design of a base-building war game after ten days of play. Four separate mechanics come through. First, the game is explicitly labelled pay-to-win, i.e., spending grants advantage. Second, base upgrade timers get longer as the player progresses, which is an in-game timer gate on progress. Third, the progression system scales endlessly with no reachable goal in sight, and the only thing ahead is more of the same repetitive advancement work, which is grind without an attainable end. Fourth, the UI is described as deliberately confusing and overwhelming with the stated purpose of driving purchases, which is an interface design working against the player's intent rather than a mere quality complaint. Finally, the social layer forces players into alliances for protection: top alliances steer development, and unattached players are attacked and bullied, which describes the game pitting players against each other. Nothing in the text is opaque enough to need a search.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "it's set up in a pay to win way"
  - why: The reviewer names the monetization model directly: the game grants advantages to players who spend, i.e., paying is the route to winning.
- `M_UIMisdirection` - ok
  - span: "The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff."
  - why: Rather than a bare quality complaint, the span attributes a purpose to the confusing interface: directing the player toward buying, which matches the boundary rule that 'confusing so you buy stuff' assigns the label.
- `S_Competition` - ok
  - span: "If you are not in one then you get attacked and bullied."
  - why: The design pits players against each other: unattached players are attacked by those in alliances, mirroring the worked example where higher-level players attacking others codes Competition. No attacker reward or incentive is described, so Encourages Anti-Social Behavior does not apply.
- `T_Grinding` - **SPURIOUS**
  - span: "just more grind"
  - why: The reviewer names what the endless scaling reduces to: continued repetitive advancement work required to progress.
- `T_InfiniteTreadmill` - ok
  - span: "Everything scales endlessly, there is kinda no point to look forward to"
  - why: The reviewer states that the game's requirements scale without end and that no goal lies ahead, i.e., the progression system has no attainable end state.
- `T_PlayingByAppointment` - ok
  - span: "the update times for your base are becoming ridiculous"
  - why: Base upgrade timers impose arbitrary waits that the player must sit through, and since upgrades gate progression, the game's schedule dictates when the player can advance.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `32c623b4-0249-469e-968c-94f60c7fe3c2` - Royal Match

> It's an interesting game but the developers should pls try to include new cards in every card pack because I noticed when one is almost close to completing a set, new cards don't appear again especially when the set is almost expiring. So after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion because they don't add new sets to the cards once the collection is about to end.

| | labels |
|---|---|
| gold | `P_CompleteTheCollection`, `T_PlayingByAppointment` |
| pred | `P_CompleteTheCollection`, `P_IllusionOfControl`, `T_PlayingByAppointment` |
| **spurious** | `P_IllusionOfControl` |

**Model analysis**

```
The reviewer is describing a limited-time card-collection event in the game: card packs are expected to deliver new cards toward themed sets, but the reviewer claims the drop system withholds new cards precisely as a set nears completion and as its deadline approaches. The collection then expires, and after gathering around 125 cards the player forfeits the set-completion reward because the event ended before the set was finished. Three distinct design behaviours are present: a collection-completion goal with a forfeited completion reward, a game-defined deadline that costs the reward when it passes, and an asserted manipulation of which cards appear to keep completion out of reach. No purchases or currencies are mentioned, so no monetary labels apply.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion"
  - why: The player is working toward completing card sets and the harm is framed as forfeiting the reward for completing the set at 125 cards, showing the design's hold on finishing the collection.
- `P_IllusionOfControl` - **SPURIOUS**
  - span: "when one is almost close to completing a set, new cards don't appear again especially when the set is almost expiring"
  - why: The reviewer asserts that the game withholds new card drops as a set nears completion, i.e., an engineered, concealed manipulation of which outcomes the player receives, rather than mere bad luck.
- `T_PlayingByAppointment` - ok
  - span: "you will miss the reward for the set completion because they don't add new sets to the cards once the collection is about to end"
  - why: The card collection ends on the game's schedule and the completion reward is lost when it does, forcing the player to finish within the event window or forfeit the reward.

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
The reviewer lists six separate grievances, all about purchases and timers. #1 describes being charged 10 gold pieces for five extra moves at a moment when they still had moves left (2 left, or 7 moves with only 1 used): the charge is framed as unwanted and automatic, implying an accidental/unconfirmed purchase rather than a deliberate buy. #2 says a paid package with unlimited lives delivered everything except the lives: this is a failed delivery, with no design mechanic described, so nothing is coded from it. #3 and #6 describe purchased or earned bonuses and packages whose real-time clocks keep ticking while the player is not playing, so their value erodes overnight on the game's schedule. #4 says free gold winnings are insufficient to keep playing, so the player must buy gold: this shows a premium currency purchasable with real money standing between the player and continued play. #5 is a pure price complaint with no mechanic and codes nothing.
```

**Labels assigned**

- `M_EasyToPurchase` - **SPURIOUS**
  - span: "I was charged 10 gold pcs for 5 moves, I had 2 moves left. I had 7 moves but only used 1 move."
  - why: The reviewer was charged for extra moves despite still having moves available, describing a deduction they did not intend or need, with no confirmation or reversal mentioned.
- `M_IntermediateCurrency` - ok
  - span: "You cannot win enough gold to play without buying sometimes"
  - why: Gold pieces are the in-game premium currency; the contrast between winning it and 'buying' it implies the currency is acquired with real money.
- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes"
  - why: Free gold winnings are insufficient, so the player must purchase gold to keep playing, making payment the route to continued progress.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone."
  - why: Bonuses have a real-time countdown set by the game that runs whether or not the player is playing, so using them requires playing on the game's clock and the reviewer describes the loss that follows from not doing so.

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
The reviewer is describing the game's long-term progression economy. They name several things at once: rewards shrinking with each patch; the meta shifting so that only newly released characters can still deal damage, which forces players to keep pulling new characters; and the game becoming pay to win. 'Pull' is Genshin's gacha mechanic — the chance-based draw that delivers characters — and the reviewer treats pulling as mandatory for staying competitive, which means older owned characters lose their damage value over time. The art-quality complaint about the archon quest background is an evaluation of production quality, not a game mechanic.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "forcing us to pull for new characters if we want to actually do damage. the game is getting more and more pay 2 win"
  - why: Pulling characters is a chance-based gacha draw whose outcome is not guaranteed, and the pay-to-win framing places real money behind those draws, making this spending on luck-based acquisition of prizes.
- `M_PayToProgress` - ok
  - span: "forcing us to pull for new characters if we want to actually do damage. the game is getting more and more pay 2 win"
  - why: Acquiring new characters through pulls is presented as the requirement for dealing damage, and the reviewer explicitly frames the game as increasingly pay to win, i.e., spending money buys the competitive advantage.
- `M_PowerCreep` - ok
  - span: "the Meta changes more and more every single day basically forcing us to pull for new characters if we want to actually do damage"
  - why: The ever-shifting meta means only newly pulled characters can still deal damage, asserting that older purchased characters lose their value over time through new releases, which drives further pulls.
- `P_RewardMania` - ok
  - span: "forcing us to pull for new characters"
  - why: The span names the gacha pull mechanic as the game's mandated route for obtaining new characters; naming pulls instantiates the Reward Mania pattern regardless of the reviewer's disapproval, and no monetary stake needs to be stated for this label.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_Gambling` | 2 | 2 |
| `T_Grinding` | 1 | 2 |
| `S_Competition` | 3 | 0 |
| `M_PayToProgress` | 1 | 1 |
| `P_RewardMania` | 2 | 0 |
| `P_IllusionOfControl` | 0 | 2 |
| `S_Reciprocity` | 2 | 0 |
| `T_PlayingByAppointment` | 1 | 1 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `M_EasyToPurchase` | 0 | 1 |
| `S_ForcedFellowship` | 1 | 0 |
| `M_RecurringFee` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `P_AestheticManipulation` | 1 | 0 |
| `P_CompleteTheCollection` | 0 | 1 |
| `M_WasteAversion` | 1 | 0 |

