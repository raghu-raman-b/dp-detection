# Error review - kimi-k3_low_teacher_v2_full

`kimi-k3` / reasoning `low` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `aad355174ac4`  
micro-F1 **0.791** (P 0.769 / R 0.814) - **22 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 4 | said NONE, gold had labels |
| SWAP | 7 | picked different labels than gold |
| MISSED ONLY | 2 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 9 | found all gold, added extras |

## The diagnostic that matters

Of **16** missed labels, **5** (31%) were named in the model's own analysis and dropped anyway; **11** (69%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `S_Reciprocity` | 1 | 1 |
| `P_AestheticManipulation` | 0 | 2 |
| `M_Gambling` | 2 | 0 |
| `S_Competition` | 1 | 1 |
| `T_MandatoryMarathon` | 0 | 1 |
| `M_IntermediateCurrency` | 0 | 1 |
| `P_RewardMania` | 1 | 0 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `M_WasteAversion` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `T_Grinding` | 0 | 1 |

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
The review is a wishlist of four feature requests, not a description of current gameplay. R12 excludes requests and suggestions from coding for the proposed mechanics themselves. The only reference to an existing behavior is 'see how much time is left for upgrades,' which mentions that upgrades run on timers. However, the span only asks for a widget to display the timer; it never describes the wait itself operating on the player (no energy refill schedule, no gate on play), unlike reviews where a wait mechanic is actively described alongside a request. Decoration removal, auctions, and advanced statistics are purely hypothetical additions. Nothing here describes a currently present dark pattern.
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
The review reports three technical malfunctions introduced by an update: crashes when opening gifts or trading, lag preventing pokeball throws, and lag/freezing in PvP and rocket battles where the opponent keeps attacking while the reviewer's game is frozen. Everything described is attributed to bugs and performance faults. Gift-opening and trading are mentioned only as features that crash, with no description of any obligation, donation, or reward mechanic behind them. The PvP freeze describes a malfunction causing losses, not a game rule penalising exit or absence, so R11 applies. No dark pattern mechanic is described.
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
The reviewer reports that troop requesting from their clan stopped working after an update and asks for a fix. While troop requesting would normally describe a Reciprocity mechanic (donating/requesting resources among players), the reviewer attributes the behaviour to a malfunction caused by an update: 'It needs to be fixed.' Under R11, behaviour attributed to a bug or technical fault is not coded, since dark patterns are deliberate design choices. No other mechanic is described.
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
The reviewer says they leave the game with a full bag and earned/purchased coins, and return to find the bag empty and the coins used. This describes an unexplained loss of holdings between sessions with no mechanism identified: no attack by other players, no inventory cap, no timer or decay rule, no prompt, no purchase flow. It reads as a report of lost progress or resources, which is most consistent with a malfunction (progress not saved, state not persisting) rather than a stated design rule. Waste Aversion requires realised stranded or forfeited value produced by a design mechanism (inventory limits, misaligned pack pricing, a specific shortfall); nothing here shows such a mechanism operating. Under R2/R3 there is no described game mechanic or design behaviour to attach a label to, and R11 cautions against coding losses that are the fault itself.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (7)

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
The review contains two distinct strands. First, the reviewer describes buying poke balls with real money and then observing that captures fail more often, forcing them to burn through balls faster and repurchase: an allegation that the game tunes outcomes to drive purchases, i.e., concealed manipulation of results. The payment also directly buys the means of continued play, and the paid purchases name an in-game item bought with real money, though no currency conversion is described, so no Intermediate Currency. Second, the edit reveals that the review itself was written and posted under the player's name without their knowledge: the game published content as the player. The boundary rule on Friend Spam / Impersonation explicitly covers a store review written under the player's account.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "so I go through the balls faster so I have to purchase more"
  - why: Continued play depends on repeatedly buying the consumable items that enable captures, which the game is alleged to deplete deliberately.
- `P_IllusionOfControl` - ok
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: The reviewer asserts the game engineers capture failures once purchases begin, i.e., outcomes manipulated on a hidden schedule to drive more purchases.
- `S_FriendSpamImpersonation` - ok
  - span: "I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE"
  - why: A review was published under the player's name without their authorship, an act performed through the player's own account identity.

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
The reviewer describes a deliberate interface behaviour in 8 Ball Pool: on opening the game or the 1v1 section, the UI auto-scrolls to and pre-selects the highest-stakes table the player's coin balance allows. They call it a 'Dark UX' trick designed to cause accidental mis-clicks so players lose their coin balance and then have to buy more. Three mechanics follow: (1) a purchase action defaulted by the interface with accidental-spend intent, which is Easy to Purchase (Default To Purchase / Accidental Purchases); (2) the interface directing the player toward a selected option against their intent, which is UI Misdirection; (3) the implied real-money purchase of replacement coins ('forced to buy real ones'), where coins are the object bought with money, which is Intermediate Currency. The betting itself is ordinary 8 Ball Pool match wagering, not a chance-based purchase, so Gambling does not apply. The 'rigged' accusation is about the UI defaults, not about manipulated match outcomes, so Illusion of Control does not apply.
```

**Labels assigned**

- `M_EasyToPurchase` - **SPURIOUS**
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins"
  - why: The game pre-selects the highest-stakes table as the default action, engineering accidental entry into a large spend with no opt-out step; the player must actively change the selection to avoid it.
- `M_IntermediateCurrency` - ok
  - span: "so players lose all their hard-earned coins and are forced to buy real ones"
  - why: Coins are bought as replacements for lost ones, i.e. real money converted into the in-game currency, establishing the conversion relation.
- `M_UIMisdirection` - ok
  - span: "the user interface is completely rigged. Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table"
  - why: Auto-scrolling to and highlighting the highest-bet table is the interface directing attention and selection toward the option that benefits the game at the player's expense.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b2dc0bc8-8ebe-4c48-bc05-38d0d65acb84` - Last War:Survival Game

> It's a nice game, but it's set up in a pay to win way. I played for 10 days, and the update times for your base are becoming ridiculous. Everything scales endlessly, there is kinda no point to look forward to, just more grind. The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff. Alliances are also weird, with the top ones dictating what to develop, what to rush, etc. If you are not in one then you get attacked and bullied. Not a great experience.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_UIMisdirection`, `S_Competition`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| pred | `M_PayToProgress`, `M_UIMisdirection`, `S_EncouragesAntiSocialBehavior`, `T_Grinding`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| **missed** | `S_Competition` |
| **spurious** | `S_EncouragesAntiSocialBehavior`, `T_Grinding` |

**Did the model consider what it missed?**

- `S_Competition` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes several mechanics. (1) The game is 'set up in a pay to win way' — spending grants advantage, which is Pay to Win under Pay to Progress. (2) Base upgrade times become 'ridiculous' — in-game timers imposing waits, Wait to Play under Playing by Appointment. (3) 'Everything scales endlessly, there is kinda no point to look forward to' — the game extends beyond any attainable end state, Infinite Treadmill, combined with 'just more grind' describing repetitive effort for progress. (4) 'The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff' — the reviewer attributes a purpose to the interface design working against the player's intent and bearing on purchases; this fits UI Misdirection (attention/obstruction bearing on spending; the reviewer's UI Misdirection counterexample was excluded because it lacked a spending connection, which is present here). (5) Players outside top alliances 'get attacked and bullied' — asymmetric predation of weaker players, where the aggressor gains from sanctioned raids; the bullying framing fits Encourages Anti-Social Behavior (stronger players rewarded for attacking weaker ones). The alliance dictating development is social organization, not recruitment or obligation to play when one would rather not, so no Forced Fellowship. Competition alone doesn't fully capture the bullying span; the predation carries the anti-social label.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "it's set up in a pay to win way"
  - why: The reviewer states spending money grants advantage in the game, the Pay to Win indicator.
- `M_UIMisdirection` - ok
  - span: "The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff"
  - why: The reviewer attributes the confusing interface to a purpose against the player's intent — driving purchases — which lifts it above a mere quality complaint.
- `S_EncouragesAntiSocialBehavior` - **SPURIOUS**
  - span: "If you are not in one then you get attacked and bullied"
  - why: The design enables stronger allied players to attack and bully unaffiliated weaker players, asymmetric predation beyond ordinary competition.
- `T_Grinding` - **SPURIOUS**
  - span: "just more grind"
  - why: Progress is described as continued repetitive effort with no meaningful goal, the activity being the grind itself.
- `T_InfiniteTreadmill` - ok
  - span: "Everything scales endlessly, there is kinda no point to look forward to"
  - why: The game continually expands its targets so there is no attainable end state or completion point.
- `T_PlayingByAppointment` - ok
  - span: "the update times for your base are becoming ridiculous"
  - why: Base upgrades run on in-game timers that impose arbitrary waits, the Wait to Play indicator.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `3c46f5e0-6091-43dc-94a0-e3af3259a63d` - Cashman Casino Slots Games

> Resently cashman had changed it's bingo rewards and daily rewards. However lve found that I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards. The most I can seem to get on the timed rewards is 40,000. I'd not pay just to get my daily rewards. So I'm deleting them.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_WasteAversion`, `T_DailyRewards` |
| pred | `M_PayToProgress`, `T_DailyRewards`, `T_PlayingByAppointment` |
| **missed** | `M_WasteAversion` |
| **spurious** | `T_PlayingByAppointment` |

**Did the model consider what it missed?**

- `M_WasteAversion` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a slots game's daily rewards system that was recently changed so that completing daily rewards requires betting 50,000 coins. They also mention 'timed rewards' with a cap around 40,000, meaning the free/timed income falls short of the bet requirement, so the daily rewards become unreachable without paying. This carries three mechanics: a daily return incentive with a penalty for not completing it (Daily Rewards); rewards delivered on the game's clock via timers (Playing by Appointment / timed rewards); and a free-versus-paid contrast where the free route cannot reach the requirement, implying payment is the way to complete daily progression (Pay to Progress). No real-money wager is described, so Gambling does not apply; the coins are in-game currency but no conversion of real money into coins is explicitly described, only 'pay to get my daily rewards', which supports Pay to Progress rather than Intermediate Currency.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "I'd not pay just to get my daily rewards"
  - why: The free route (timed rewards capped at 40,000) falls short of the 50,000 requirement, so payment is implied as the alternative path to completing the daily rewards.
- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The game provides daily rewards and missing the requirement forfeits that day's reward opportunity, an incentive to return daily with a consequence for failing.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "The most I can seem to get on the timed rewards is 40,000"
  - why: Rewards are delivered on in-game timers with a fixed amount per interval, a schedule imposed by the game that gates the player's progress toward the daily requirement.

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

- `P_RewardMania` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes a dice game with a sticker collection mechanic. Several mechanics surface: winning anything costs 'hundreds of dollars,' which states payment is required for progress. Sticker sets cannot be finished because the last one or two stickers are withheld unless the player pays a lot, which is both a collection completion driver and manufactured scarcity bearing on price. Finally, 'it may let you complete a goal maybe one out of hundred times' asserts that outcomes are on a hidden, engineered ratio rather than determined by the player's play, an outcome-manipulation claim. No randomised reward delivery mechanic is explicitly named (no packs, chests, or pulls described), so Reward Mania is not clearly established; the withheld last stickers function as a direct scarcity/payment gate rather than odds. No monetary stake on a chance mechanic is described, so Gambling does not apply.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "you will never get the last one or two unless you pay a lot of money to get them"
  - why: The final stickers are deliberately made unobtainable through play so their price reflects manufactured scarcity, compelling payment to acquire them.
- `M_PayToProgress` - ok
  - span: "if you want to win anything on this game it will cost hundreds of dollars"
  - why: Payment is described as granting what free play cannot obtain, i.e., spending money is required to progress or win.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: The player is working to complete a sticker set, and the missing final pieces are framed as the compulsion driving further play and payment.
- `P_IllusionOfControl` - **SPURIOUS**
  - span: "it may let you complete a goal maybe one out of hundred times"
  - why: The reviewer asserts the game controls whether goals can be completed on a fixed ratio ('let you'), a claim that outcomes are manipulated rather than determined by the player's skill.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `12267c1e-47ba-4984-97c8-768e820ceb1c` - Bingo Blitz™️ - Bingo Games

> not very user-friendly. no apparent reachable goals within a decent amount of time. I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| pred | `M_EasyToPurchase`, `M_Gambling`, `M_IntermediateCurrency`, `P_CompleteTheCollection`, `P_RewardMania` |
| **missed** | `P_AestheticManipulation`, `T_Grinding` |
| **spurious** | `M_Gambling`, `M_IntermediateCurrency`, `P_RewardMania` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**
- `T_Grinding` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a bingo game where each round yields 'photos' toward completing sets. Three mechanics are described. First, a collection system: photos are collected to complete sets, and the reviewer frames the unfinishable set as the central frustration. Second, after every lost round the game prompts the player to spend extra coins to claim a photo they don't have — a purchase prompt that intercepts gameplay at the point of failure. Third, even after paying the coins and getting 2-3 bingos, the promised photo doesn't materialise — the reward delivery is chance-based and unpredictable despite the payment. The closing line 'I've wasted so much money' shows real money was converted into the coins being spent, establishing the intermediate currency layer, and the coins are effectively being wagered on a chance-based outcome (the photo drop).
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have"
  - why: A purchase prompt intercepts gameplay automatically after every lost round, catching the player at the point of a spent resource.
- `M_Gambling` - **SPURIOUS**
  - span: "I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED"
  - why: Purchased coins are spent on an offer whose payout (the photo) is luck-dependent and frequently fails to arrive — a wager on a chance outcome.
- `M_IntermediateCurrency` - **SPURIOUS**
  - span: "it will ask me if I want to spend extra coins to claim a photo"
  - why: Coins are the stake the game demands, and 'I've wasted so much money' shows real money entering the coin economy, establishing the money-to-currency conversion.
- `P_CompleteTheCollection` - ok  _[span not verbatim]_
  - span: "I play round after round to collect 'photos'... to complete the set"
  - why: The player is driven to acquire all photos in a set, and the uncompleted set is what sustains repeated play and spending.
- `P_RewardMania` - **SPURIOUS**
  - span: "I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times"
  - why: Photo drops are unpredictable — repeated attempts and even successful bingos fail to yield the item, keeping the player chasing the next attempt.

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
The reviewer is describing a sticker/card album mechanic in Dice Dreams. They were two cards short of completing an album for a grand prize, bought a paid deal that 'promised' new cards, and received duplicates instead. This carries several mechanics: the album is a collection the player is compelled to complete; completing it is tied to spending money on card deals; the deal delivers cards from a randomised pool (duplicates possible), which is a chance-based delivery with a real-money stake; and the low drop rate of needed cards is what sustains the purchase loop. The 'Free Cash' promotion is out-of-game marketing and excluded under R13. No wait timers, daily mechanics, or social mechanics are described.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "i bought a deal which promised i would get NEW cards, and all i got were useless duplicates"
  - why: Real money was spent on a card deal whose contents were chance-based, yielding duplicates rather than the needed cards.
- `M_PayToProgress` - **SPURIOUS**
  - span: "I had two cards left which would grant me the grand prize for completing an album, so i bought a deal"
  - why: Progress toward completing the album is pursued through a real-money purchase of a card deal.
- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The player is driven to complete a full card album, with the missing pieces framed as the goal pulling them toward purchase.
- `P_RewardMania` - ok
  - span: "all i got were useless duplicates"
  - why: Duplicate drops from a randomised card pool describe unpredictable reward delivery, sustaining repeated attempts at the needed cards.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (2)

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
The reviewer describes three mechanics. First, the game rewards inviting friends and getting them to join via Facebook — recruitment of new players for in-game rewards, even though the reviewer complains the rewards stopped; the mechanic is still described as present in the game's design (R7/R8 code the mechanic, not the evaluation of its payout). Second, dice are the stake in a chance-based loop: the reviewer played max bet and got no shut downs or bank heists, describing a randomized outcome system — but no real money is mentioned, so this codes the variable reward delivery, not Gambling. Third, sticker drops are all duplicates, i.e., repeated unwanted drops from a randomised pool, which is Reward Mania delivery language; the reviewer does not describe compulsion to complete the album itself, so Complete the Collection is not assigned. The login failure is a technical fault (R11/R2) and codes nothing.
```

**Labels assigned**

- `P_RewardMania` - ok
  - span: "when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way"
  - why: Unpredictable outcomes from dice betting and duplicate drops from a randomised sticker pool describe chance-based reward delivery sustaining repeated attempts; no monetary stake is described, so Gambling does not apply.
- `S_ForcedFellowship` - ok
  - span: "Suddenly I get no rewards for inviting friends and getting them to join facebook"
  - why: The game rewards players for inviting friends to join, which instantiates the Social Pyramid Scheme indicator; the complaint is that the reward stopped, but the recruitment mechanic is described.

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
The reviewer describes Monopoly GO's sticker collection system: stickers come from randomized packs, the player keeps getting duplicates, and completing the full sets is presented as impossible without paying. Three mechanics are named or implied: (1) completing sets, which is a collection mechanic; (2) finishing is gated behind payment, which is Pay to Progress; (3) the duplicate-heavy random delivery of stickers is a variable-reward delivery mechanism (duplicate drops from a randomized pool is explicitly named as a Reward Mania indicator). No explicit monetary stake in the chance mechanic itself is stated, so Gambling is not assigned; the payment is tied to finishing the sets, i.e., progression.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: Completing the sets is stated to be contingent on payment; progress toward completion is blocked without paying.
- `P_CompleteTheCollection` - ok  _[span not verbatim]_
  - span: "frustrating when it comes to getting stickers... never lets you finish all the sets"
  - why: The player is compelled to acquire all stickers to complete the sets, and the unfinished collection is framed as the central frustration.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: Duplicate drops from a randomized sticker pool describe the unpredictability of the reward delivery mechanism, not the reward's value.

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
The reviewer complains about three things. First, a 30-second wait to connect to a match: this is matchmaking/queue time arising from the operation of the service, not an in-game timer gating play, so it does not meet Wait to Play. Second, rewards that look generous but are 'just for show': no mechanism of delivery is described, so this is an evaluation of reward value, not Reward Mania. Third, weapon upgrades and perks are difficult to get and the player is 'stick battling to win': the reviewer describes having to keep battling repeatedly as the route to progress, which names the repeated activity (battling) tied to advancement, satisfying Grinding. 'Rob you of your time' is a general evaluation and codes nothing on its own.
```

**Labels assigned**

- `T_Grinding` - **SPURIOUS**
  - span: "Its difficult to get weapon upgrades or any percs others you stick battling to win"
  - why: The span names the repeated activity (battling to win) as what the player must keep doing to obtain upgrades, i.e., repetitive play as the means of progress.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `0bc09fc3-6436-4a24-855e-0fdc56887918` - Fishdom

> EDIT 1/17/2023: Customer Service can't make good on 9 diamonds when game element doesn't appear within 5 original moves and 5 additional moves. It is a fun game, you don't have to pay to win. I suggest after this cust. svc experience that you don't buy from this game beyond the pass.Get friends and a team and trade lives.

| | labels |
|---|---|
| gold | `M_RecurringFee`, `S_Reciprocity` |
| pred | `M_PayToProgress`, `M_RecurringFee`, `S_Reciprocity` |
| **spurious** | `M_PayToProgress` |

**Model analysis**

```
The reviewer describes several mechanics. First, 'diamonds' are named as a premium-style in-game currency, but the span concerns customer service failing to compensate diamonds lost to a game element not appearing — a bug complaint, and no real-money conversion is described, so Intermediate Currency does not apply. Second, 'you don't have to pay to win' explicitly invokes pay-to-win: the reviewer frames paying as the route to winning while noting it is not mandatory, which establishes a paid advantage contrast. Third, 'don't buy from this game beyond the pass' names a purchasable pass, which under R5 is a battle pass / recurring fee instance. Fourth, 'Get friends and a team and trade lives' describes an existing resource-exchange mechanism between players already in the game, which is Reciprocity (not Forced Fellowship, since no recruitment of new players is described). The customer service complaint about the missing game element is attributed to a malfunction and codes nothing under R11.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "It is a fun game, you don't have to pay to win."
  - why: The phrase 'pay to win' explicitly describes spending money as a route to winning; the free/paid contrast establishes the paid advantage exists even though the reviewer says it is optional.
- `M_RecurringFee` - ok
  - span: "I suggest after this cust. svc experience that you don't buy from this game beyond the pass."
  - why: The game contains a purchasable pass, which is an explicit instance of a recurring fee under R5.
- `S_Reciprocity` - ok
  - span: "Get friends and a team and trade lives."
  - why: Players already in the game exchange lives with teammates, a resource-transfer favour mechanism between existing players.

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
The reviewer praises the game and compares its monetization favorably to other games. The key mechanic described is spending real money ($20) on items/purchases in the game, with bingo giving 'twice the number of your purchase' — this describes real money being converted into in-game currency/credits whose exchange rate obscures the true cost, which is Intermediate Currency (Premium Currency). The mention of 'different modes and events' names events but describes no schedule, expiry, or pressure operating on the player, so no temporal or FOMO label. Payment is never tied to progression being blocked or slowed, so Pay to Progress does not apply. The comparison about getting more for your money is a value judgment on pricing, not anchoring or a purchase-friction mechanism, so no Easy to Purchase.
```

**Labels assigned**

- `M_IntermediateCurrency` - **SPURIOUS**
  - span: "If your spend $20 on some item you get less then what your actually hoping for, but on here bingo gives you twice the number of your purchase"
  - why: Real money ($20) is exchanged for in-game purchase credit whose amount ('twice the number of your purchase') is expressed through the game's own conversion rather than a direct price, establishing the money-to-currency conversion.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `21021f9a-e106-4e51-b01d-3fe4a4c941fc` - MONOPOLY GO!

> Deleted the game now. The latest event I was about to get 525 dice as reward, I had 3 left to go and I ran out of dice, it said 2Days left. Now just logged in after sleeping and the event is now changed. Deleting this game and what an absolute waste of time. Never purchased anything coz i have trust issues with F2P model games, and my gutt was right all along. Fun when it lasted, but that was a low blow.

| | labels |
|---|---|
| gold | `T_PlayingByAppointment` |
| pred | `P_EasyToGetHardToLose`, `T_PlayingByAppointment` |
| **spurious** | `P_EasyToGetHardToLose` |

**Model analysis**

```
The reviewer describes a limited-time event in MONOPOLY GO! They were close to completing it (3 tasks left toward a 525-dice reward), ran out of dice, and saw the event carried a '2 Days left' timer. When they logged back in after sleeping, the event had changed and their progress toward the reward was gone. Two mechanics are active: (1) a game-set clock governing when the event and its rewards are available, with rewards forfeited when the window closes — the schedule operates on the player and is tied to reward loss, which is Playing by Appointment. (2) A partially completed goal whose near-completion kept the player engaged and whose loss is the felt harm — Endowed Progress, the partially-completed-goal arm of Easy to Get, Hard to Lose. The F2P/trust comments express general dissatisfaction with monetization but describe no specific purchase mechanic, so no monetary label. Running out of dice is a resource constraint but no regeneration timer or wait is described, so no Wait to Play beyond the event clock already coded.
```

**Labels assigned**

- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "The latest event I was about to get 525 dice as reward, I had 3 left to go and I ran out of dice"
  - why: The reviewer was three tasks from the reward and frames the near-complete progress as the wasted investment, the partially completed goal the design uses to hold engagement.
- `T_PlayingByAppointment` - ok
  - span: "it said 2Days left. Now just logged in after sleeping and the event is now changed."
  - why: The event runs on a countdown set by the game and the reward was forfeited when the window closed, forcing play within the game's schedule or losing the reward.

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
The reviewer describes a match-3 style progression wall after level 8000. Three mechanics are described. First, a lives system: they run out of lives multiple times daily, which means lives deplete and must regenerate or be replenished, gating play sessions. Second, progress is effectively payment-gated: 'You must buy add ons else you can't make it through', and the free path is called a waste of time, so payment is framed as the required route past levels. Third, the path to each level requires many repeated attempts: 'avg 5-7 days per level' spent trying to beat every alternate level, which is repetitive task repetition to advance. The closing 'Wasted too much of money and time' is investment already written off while the player is actively uninstalling; per the Easy to Get Hard to Lose counterexample, reporting a sum spent while disengaging does not code that label, and there is no described pull keeping them in. No currencies are named, no chance mechanics, no social mechanics.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying"
  - why: Progress past levels is stated to require purchasing add-ons; the unpaid path is framed as not viable, so payment is the route to advancement.
- `T_Grinding` - ok
  - span: "I run out of lives 3-4 times daily to beat every alternate level, avg 5-7 days per level"
  - why: The repeated activity is identified: replaying each level over many attempts for 5-7 days to advance, which is repetitive effort substituting for progress rather than a bare slowness complaint.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "I run out of lives 3-4 times daily to beat every alternate level"
  - why: A lives system that depletes and refills over time gates play: running out of lives repeatedly imposes waits until lives regenerate, per the lives/energy regeneration boundary rule.

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
The reviewer describes Royal Match's card collection feature: card packs yield random cards toward completing sets, each set is time-limited ('almost expiring', 'about to end'), and completing a set within the window earns a reward. Three mechanics are described. First, the collection compulsion itself: gathering all cards in a set for the completion reward. Second, the delivery mechanism: cards come from packs with new cards allegedly stopping near completion, i.e., duplicate-heavy randomised drops. Third, the deadline: sets expire and the reward is forfeited if the set is not completed in the game's window, which is a schedule imposed by the game. The reviewer also asserts the game deliberately withholds new cards as the deadline nears, a claim that outcomes are manipulated by a hidden schedule. No money or purchase is mentioned anywhere, so monetary labels like Gambling or Deceptive Luxury do not apply.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "when one is almost close to completing a set, new cards don't appear again"
  - why: The player is engaged in collecting all cards of a set to obtain the set-completion reward, which is the collection-completion compulsion.
- `P_IllusionOfControl` - **SPURIOUS**
  - span: "I noticed when one is almost close to completing a set, new cards don't appear again especially when the set is almost expiring"
  - why: The reviewer asserts the game manipulates drop outcomes on a hidden schedule, withholding new cards precisely when completion is near, a claim of concealed outcome determination.
- `P_RewardMania` - **SPURIOUS**
  - span: "the developers should pls try to include new cards in every card pack because I noticed when one is almost close to completing a set, new cards don't appear again"
  - why: Cards are delivered through randomised packs yielding repeats instead of needed new cards, sustaining engagement through unpredictable drops rather than reward value.
- `T_PlayingByAppointment` - ok
  - span: "you will miss the reward for the set completion because they don't add new sets to the cards once the collection is about to end"
  - why: The reward expires on the game's clock: the collection has an end date and the completion reward is forfeited when the window closes, a schedule imposed by the game rather than felt anxiety.

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
The reviewer complains about four things. First, a 7-hour quest yielding very few primogems: this is a complaint about reward value for a single long quest, not about a repeated activity, a randomised delivery mechanism, or a payment alternative, so it does not lift to Grinding, Reward Mania, or Pay to Progress. Second, exploration described as debilitating and female character designs criticised as samey: evaluations of quality with no mechanic described (the aesthetic complaint reports the reviewer's own preference, per the Aesthetic Manipulation counterexample). Third, the absence of a resin overflow system: this only makes sense if the game has a capped energy resource (resin) that regenerates over real time, so that regeneration beyond the cap is wasted. The span thus implies an in-game energy timer governing when the player can use stamina-gated content, which is the Wait to Play indicator of Playing by Appointment. No purchases, no social mechanics, no chance mechanics are described.
```

**Labels assigned**

- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "there is no resin overflow system"
  - why: Complaining that resin cannot overflow implies a capped energy resource that regenerates on a real-world timer, an in-game timer that makes players wait or return on the game's schedule to use stamina-gated content.

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
The reviewer describes a gacha game where each patch reduces free rewards and shifts the meta so frequently that players are effectively forced to pull for new characters to deal damage. Pulls are the gacha draw mechanic, which is Reward Mania. The pull pressure is monetized: 'forcing us to pull for new characters' combined with 'the game is getting more and more pay 2 win' ties real money to chance-based character acquisition and to in-game advantage. The meta constantly shifting so older characters no longer suffice is the recency-qualifier form of Power Creep: value of already-owned characters diminishes as new ones become necessary. The complaint about a bad background picture is a quality gripe, not a mechanic. 'Less rewards per patch' describes reward value, not delivery, so it adds nothing beyond what's coded.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "basically forcing us to pull for new characters if we want to actually do damage. the game is getting more and more pay 2 win"
  - why: The pull is a chance-based mechanic and the 'pay 2 win' framing supplies the monetary stake in the same span.
- `M_PayToProgress` - ok
  - span: "basically forcing us to pull for new characters if we want to actually do damage. the game is getting more and more pay 2 win"
  - why: Spending (pulling) is described as granting combat advantage, and the reviewer explicitly calls it pay to win.
- `M_PowerCreep` - ok
  - span: "the Meta changes more and more every single day basically forcing us to pull for new characters if we want to actually do damage"
  - why: Constant meta shifts mean only new characters deal adequate damage, devaluing characters the player already owns, mirroring the 'new enough to deal damage' worked example.
- `P_RewardMania` - ok
  - span: "forcing us to pull for new characters"
  - why: Pulls are named outright, which is an indicator instance of Reward Mania regardless of the stake.

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
The reviewer describes an update that removed 'open silver' and player-vs-player combat from Total Battle. Two mechanics are coded as currently present. First, meaningful growth requires spending: 'You have to spend to have any meaningful growth' is a direct pay-to-progress statement. Second, the update devalued what players had already bought: spending is described as made 'pointless' by the update and players 'screwed... who wasted money on this game', which is a purchased investment losing value through a game update, i.e., Power Creep. The PvP removal itself is the removal of Competition, not its presence, so Competition is not coded (R12). Easy to Get, Hard to Lose does not apply: the reviewer reports investment lost and advises others not to play; there is no reluctance to leave or investment pulling the player back (per the counterexample). No search needed.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You have to spend to have any meaningful growth"
  - why: Progress in the game is stated to require spending money.
- `M_PowerCreep` - **SPURIOUS**
  - span: "You have to spend to have any meaningful growth and then they go and make it all pointless by getting rid of any player vs player"
  - why: Value purchased with real money was rendered pointless by an update, i.e., acquired investment devalued after purchase through a game change.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_Gambling` | 2 | 3 |
| `T_PlayingByAppointment` | 1 | 3 |
| `M_IntermediateCurrency` | 1 | 2 |
| `P_RewardMania` | 1 | 2 |
| `M_PayToProgress` | 0 | 3 |
| `T_Grinding` | 1 | 2 |
| `S_Reciprocity` | 2 | 0 |
| `P_AestheticManipulation` | 2 | 0 |
| `P_IllusionOfControl` | 0 | 2 |
| `S_Competition` | 2 | 0 |
| `M_PowerCreep` | 0 | 1 |
| `S_EncouragesAntiSocialBehavior` | 0 | 1 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `M_WasteAversion` | 1 | 0 |
| `M_EasyToPurchase` | 0 | 1 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `T_MandatoryMarathon` | 1 | 0 |

