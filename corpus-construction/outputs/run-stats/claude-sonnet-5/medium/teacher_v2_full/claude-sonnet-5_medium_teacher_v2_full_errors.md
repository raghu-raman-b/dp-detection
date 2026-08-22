# Error review - claude-sonnet-5_medium_teacher_v2_full

`claude-sonnet-5` / reasoning `medium` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `6529a474a2b0`  
micro-F1 **0.761** (P 0.805 / R 0.721) - **25 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 7 | said NONE, gold had labels |
| SWAP | 6 | picked different labels than gold |
| MISSED ONLY | 6 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 6 | found all gold, added extras |

## The diagnostic that matters

Of **24** missed labels, **6** (25%) were named in the model's own analysis and dropped anyway; **18** (75%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `S_Competition` | 2 | 2 |
| `T_Grinding` | 0 | 2 |
| `P_AestheticManipulation` | 0 | 2 |
| `S_Reciprocity` | 1 | 1 |
| `P_RewardMania` | 1 | 1 |
| `M_Gambling` | 1 | 1 |
| `M_IntermediateCurrency` | 0 | 2 |
| `S_FriendSpamImpersonation` | 0 | 1 |
| `T_MandatoryMarathon` | 0 | 1 |
| `M_RecurringFee` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `M_EasyToPurchase` | 0 | 1 |
| `M_WasteAversion` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |

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
The entire review is a wishlist of four hypothetical feature requests directed at the developers: an auction system for cosmetics, a change to obstacle/decoration interaction, a widget for tracking upgrade timers across accounts, and a hidden advanced-stats screen for troops. None of these describe mechanics currently present in the game; they are all explicitly proposed additions ('we would like'). Per R12, requests or suggestions for non-existent features do not trigger tags for the proposed mechanics, and R2 requires an actual described game mechanic or design behaviour, not a wish. There is no mention of any existing dark pattern, monetization behaviour, social mechanic, or temporal mechanic currently operating in the game — even the mention of 'in-game currency' is only in the context of a suggested bidding/auction system that doesn't exist. No boundary rule salvages any of this content as describing a present mechanic.
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
The review is a list of technical complaints following an update: crashes when opening gifts or trading, lag when throwing pokeballs, lag and freezing during PVP and Team Rocket battles. Every issue named is explicitly attributed to bugs, lag, or crashes rather than to a deliberate game rule or mechanic. There is no mention of an underlying design rule that imposes a penalty independent of the malfunction (e.g., no statement that losing due to a freeze forfeits progress by design, no mention of monetization, currency, scheduling, social pressure, or reward structures). Per R11, behavior attributed to a bug, glitch, or technical fault does not trigger dark pattern labels unless the game's underlying rule itself would impose the same penalty regardless of the malfunction, and no such rule is described here. This review is a general bug report and does not describe any deliberate game mechanic or design behaviour under R2.
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
This review is a generic, enthusiastic endorsement of the game's graphics, storyline, strategy depth, and real-time combat. It mentions building an empire and battling other players, but does not describe any specific dark pattern mechanic such as payment requirements, timers, currencies, social pressure, or reward delivery systems. Real-time combat against other players could suggest competition, but the review frames it purely as an enjoyable feature without describing any manipulative design (e.g., no mention of pay-to-win, matchmaking unfairness, or forced participation). Per R2, a label requires description of a game mechanic or design behaviour, not just general praise or feature-naming. Mentioning 'battling other players in real-time combat' alone, without any indication of exploitation, competitive pressure, or monetization tied to it, does not meet the bar for S_Competition since the codebook example for Competition ties it to monetization or pressure context, and R2 warns against assigning from tone or general enjoyment alone. There is no concrete mechanic described here that maps to any of the 29 labels.
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
The reviewer reports that a specific feature, requesting troops from their clan, stopped working after an update, and asks for it to be fixed. While troop requesting is itself a Reciprocity-style resource exchange mechanic between clan members, the review does not describe the mechanic's operation, obligation, or any dark-pattern behavior around it. It only reports that the feature is broken due to an update, which is a technical malfunction complaint. Per R11, behavior attributed to a bug or technical fault does not get coded as a deliberate dark pattern, and there is no underlying game rule or penalty described here that would survive the bug attribution (unlike the daily-rewards worked example where a demotion penalty was still enforced by design). There is no mention of any monetary, temporal, social, psychological, or technical dark pattern actually functioning as intended. Therefore no label applies.
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
The reviewer opens with general praise and then makes two requests. The first, wanting an in-app way to trade stickers with other players because not everyone uses Facebook, is explicitly framed as a wish ('I think you should have a way to trade stickers') rather than a description of an existing mechanic; per R12, requests or suggestions for features that do not currently exist are not codable, even though the underlying game (sticker collection, Facebook-linked trading) might otherwise touch on collection or social mechanics. The second statement, about wanting to use a purchased booster when challenged by another player, is also phrased as a wish ('I believe if i purchase a booster i should be able to use it'), implying the current game does not allow this, again a suggestion for a hypothetical improvement rather than a description of a present dark pattern (e.g., no wasted currency, no scarcity, no forced purchase is described). Neither span describes a mechanic currently operating on the player in a way that fits any codebook definition; both are proposals for change. There is no description of trading actually happening, no resource forfeiture shown, no purchase-flow friction described, and no penalty tied to an existing rule. Consequently, no label in the codebook is satisfied by the text as written.
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
The review centers entirely on advertising that misrepresents the gameplay: the reviewer states the ads emphasize puzzles as if that's the core game, while the actual game is a strategy title with occasional puzzles. Per R13, out-of-game marketing and store-front advertising are outside the coding unit, even where the behaviour (misleading gameplay representation) would otherwise satisfy a label like Advertisement. The T_Advertisement label specifically requires ads encountered within the installed game (forced views, ad-gated content, reward-for-watching), not misleading marketing that prompted install. The closing line 'you'll be doing chores in order to get to them' gestures at repetitive activity required to reach the puzzle content, but it names no specific repeated task (no farming, no replaying levels, no identified grind loop) — it's a vague, evaluative characterization comparable to the boundary rule example where general repetitiveness without a named activity codes NONE. No other mechanic (currency, payment, social, psychological, technical) is described anywhere in the text.
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
The reviewer describes leaving the game with accumulated coins (both earned through play and purchased with real money) only to find them gone upon return. This is a complaint about resources vanishing between sessions, but the review does not describe any of the specific mechanisms in the codebook: it doesn't describe a currency exchange rate, a wager or gambling mechanic, an inventory cap forcing disposal, a schedule or timer causing forfeiture, or any deliberate design rule tying the loss to a missed login window or session exit. There's no naming of what causes the coins to disappear (no timer, no cap, no competitor raid, no expiration), and no indication this is a deliberate design choice rather than a bug/glitch in tracking currency. Without a described mechanism connecting the loss to a specific dark pattern (e.g., a daily reset, an inventory limit, a raid mechanic, an expiring pass), this reads as an unexplained resource loss that could well be a technical malfunction, which per R11 would not be codable unless the underlying game rule itself is described as imposing this penalty. No such rule is named here.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (6)

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
The reviewer describes purchasing Poke Balls with real money to catch Pokémon, and notices that after they began purchasing, the balls 'keep breaking out' during capture attempts, causing them to burn through the balls faster and need to buy more. This is a two-part mechanic: first, real-money purchases are tied to the core catching activity, meaning that running out of balls interrupts continued play unless more are bought, which is a progress-gating purchase. Second, and more specifically, the reviewer alleges a change in behavior correlated with paying, i.e., a suspicion that the catch/break-out odds are being manipulated to induce more spending rather than being a stable, transparent mechanic, and this suspicion is corroborated by other players they claim to have spoken to. That is a claim about the game concealing or tuning the determination of outcomes (capture success) to encourage continued purchasing, which fits the Illusion of Control pattern rather than a simple losing streak. The retracted portion about not writing the review and not talking to other players is a meta-comment about review authenticity and does not itself describe a game mechanic, so it is disregarded under R2.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: Running out of Poke Balls halts the player's ability to continue capturing Pokémon, and the review frames purchasing more balls as the way to keep progressing, satisfying the pay-to-progress pattern.
- `P_IllusionOfControl` - ok
  - span: "when I tried to make a capture that they keep breaking out so I go through the balls faster"
  - why: The reviewer perceives a change in the game's determination of catch success correlated with their purchasing behavior, implying the game conceals or tunes outcomes to encourage further purchases rather than this being a normal losing streak.

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

- `M_Gambling` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes several distinct mechanics. First, they note that inviting friends and having them join via Facebook used to yield rewards, implying an in-game invite-for-reward system (Social Pyramid Scheme) that is now not paying out after a season change. Second, they describe dice as a resource used to 'play max bet' hoping to trigger chance-based bonus events ('Shut downs' and 'bank heists'), and lament getting no luck, which describes a variable/unpredictable reward delivery system rather than a purchased wager (no money is mentioned entering the dice pool here). Third, they mention stickers coming as duplicates, which ties to the sticker-album collection mechanic in this game and also reflects the randomized, duplicate-heavy nature of the reward drops. Finally, the login/connection error appears to be a technical fault (R11) with no described penalty beyond being locked out, so it does not code as a dark pattern under this codebook.
```

**Labels assigned**

- `P_CompleteTheCollection` - **SPURIOUS**
  - span: "Stickers are duplicates all the way"
  - why: References the sticker album collection system where the reviewer is frustrated by receiving duplicates instead of progressing toward completing the set, reflecting the compulsion to complete the collection.
- `P_RewardMania` - ok
  - span: "Stickers are duplicates all the way"
  - why: Repeated duplicate sticker drops from a randomized pool is a named indicator of Reward Mania's delivery-mechanism-driven engagement (already assigned once per R1, listed here to show the supporting span).
- `S_ForcedFellowship` - ok
  - span: "Suddenly I get no rewards for inviting friends and getting them to join facebook"
  - why: The span implies an existing mechanic that rewards the player for recruiting friends into the game, matching the Social Pyramid Scheme indicator of Forced Fellowship.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fdef27f2-9a21-4b8e-a04c-7a4753e0fb07` - 8 Ball Pool

> The game is great, but the user interface is completely rigged. Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins and are forced to buy real ones. ​We need a "Default Table Lock" or the game should always open the lowest bet table by default, not the highest! Fix this scammy feature. Giving 1 star

| | labels |
|---|---|
| gold | `M_Gambling`, `M_IntermediateCurrency`, `M_UIMisdirection` |
| pred | `M_EasyToPurchase`, `M_IntermediateCurrency`, `M_PayToProgress`, `M_UIMisdirection` |
| **missed** | `M_Gambling` |
| **spurious** | `M_EasyToPurchase`, `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_Gambling` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes a specific interface behavior in the 1v1 betting menu: the UI automatically scrolls to and highlights the highest-stake table whenever the section is opened, rather than defaulting to a neutral or lowest option. The reviewer explicitly frames this as a 'Dark UX' trick designed to cause accidental mis-clicks, which then costs the player their accumulated coins and pushes them toward purchasing more. This is a description of a purposeful default-selection mechanism in the interface (UI Misdirection / Accidental Purchases), and the consequence described, losing coins and being 'forced to buy real ones', implies both a purchase-friction reduction mechanism and a real-money-to-currency conversion the game relies on to keep the player spending. No gambling wager, grinding, or social mechanic is described; the review is narrowly about the interface's default behavior and its monetary consequence.
```

**Labels assigned**

- `M_EasyToPurchase` - **SPURIOUS**
  - span: "This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins"
  - why: The default selection is described as engineered to cause mis-clicks that cost the player currency without confirmation or an easy way to avoid it, reducing the friction that would normally prevent an unintended loss of value.
- `M_IntermediateCurrency` - ok
  - span: "lose all their hard-earned coins and are forced to buy real ones"
  - why: The span shows coins as an in-game currency that must be replenished with real money purchases, establishing the money-to-currency conversion direction required for this label.
- `M_PayToProgress` - **SPURIOUS**
  - span: "are forced to buy real ones"
  - why: Once coins are lost through the engineered mis-click, the reviewer states the player is compelled to purchase more to continue playing, describing a payment requirement to keep progressing in the game.
- `M_UIMisdirection` - ok
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins"
  - why: The interface actively directs the player's selection toward the highest-stake option by default rather than leaving it neutral, matching the pattern of UI elements engineered to steer choice toward the option that benefits the developer.

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
The reviewer describes a sticker/collection-based dice game. First, they state that winning anything requires substantial real-money spending, which is a direct Pay to Progress/Pay to Win claim tied to overall game outcomes. Second, they describe a sticker album where the final one or two items are deliberately withheld unless the player pays extra money to obtain them, which both invokes the collection-completion compulsion (naming the album as something the player is trying to finish) and describes manufactured scarcity on specific items whose acquisition is gated by payment (Remedy Consumption pattern of Deceptive Luxury). Third, the reviewer states that completing a goal succeeds only 'one out of hundred times,' which frames the game as controlling/limiting the odds of success at a fixed, low rate rather than merely describing an unlucky personal run — this fits the Illusion of Control's fixed win-ratio indicator, since the reviewer is asserting a near-fixed low success rate baked into the game rather than reporting a one-off loss streak.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "you will never get the last one or two unless you pay a lot of money to get them"
  - why: The last items are made artificially unobtainable through normal play, with a costly payment offered as the remedy route to acquire them, tying the manufactured scarcity directly to price.
- `M_PayToProgress` - ok
  - span: "if you want to win anything on this game it will cost hundreds of dollars"
  - why: States that winning in the game is contingent on substantial real-money payment, directly matching the pay-to-win/pay-wall pattern.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: Names a sticker set the player is trying to finish, with the final pieces framed as the goal the reviewer cannot reach, matching the collection-completion compulsion.
- `P_IllusionOfControl` - **SPURIOUS**
  - span: "it may let you complete a goal maybe one out of hundred times"
  - why: Asserts the game itself permits success only at a near-fixed, extremely low rate, implying the outcome is controlled by the game rather than genuine random chance or skill, rather than describing a single unlucky run.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `12267c1e-47ba-4984-97c8-768e820ceb1c` - Bingo Blitz™️ - Bingo Games

> not very user-friendly. no apparent reachable goals within a decent amount of time. I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| pred | `M_IntermediateCurrency`, `M_PayToProgress`, `P_CompleteTheCollection` |
| **missed** | `M_EasyToPurchase`, `P_AestheticManipulation`, `T_Grinding` |
| **spurious** | `M_IntermediateCurrency`, `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - never mentioned -> **attention / recall**
- `P_AestheticManipulation` - never mentioned -> **attention / recall**
- `T_Grinding` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes collecting 'photos' to complete a set across rounds, which is the collection-completion compulsion. After losing a round, the game repeatedly offers to spend extra coins to claim a missing photo needed to complete the set, which ties spending an in-game currency directly to progress toward that goal (Pay to Progress). The review also states 'I've wasted so much money,' which, combined with 'spend extra coins,' implies the coins are purchased with real money, satisfying Intermediate Currency as the funding chain even though the exchange itself isn't detailed. The complaint that the offer/photo was 'promised' but not delivered after paying reads as a broken promise/bug in the transaction rather than a described design rule (no stated penalty structure), so per R11 this specific failure-to-deliver is not coded as a separate dark pattern; it's a malfunction, not a designed mechanic.
```

**Labels assigned**

- `M_IntermediateCurrency` - **SPURIOUS**
  - span: "I'll spend coins on said offer"
  - why: Coins are the in-game currency spent on offers; combined with the reviewer's statement of having 'wasted so much money,' this implies real money was converted into coins used for these purchases.
- `M_PayToProgress` - **SPURIOUS**
  - span: "it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set"
  - why: Payment (coins) is offered as the route to obtain a missing item needed for progress toward completing the set, directly linking spend to advancement.
- `P_CompleteTheCollection` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The reviewer is engaged in repeated play specifically to acquire a set of photos, the core compulsion this label covers.

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
The reviewer describes a collection mechanic (an album needing specific cards) with a 'grand prize' for completion. Needing only two more cards, they made an in-app purchase advertised as delivering 'NEW cards' toward that goal, but instead received 'useless duplicates.' This is a paid, chance-based transaction: real money was spent for an uncertain, randomized outcome (which specific cards would be delivered), fitting a loot-box style gamble. The collection-completion framing (needing specific cards to finish an album for a grand prize) also implicates the compulsion to complete a set. The fact that the paid draw yielded duplicates rather than the needed items shows the delivery mechanism itself, an unpredictable, randomized pool that can yield unwanted duplicates, is what drove the spend, independent of the value of what was received. No other mechanics (ads, daily logins, social pressure, UI tricks, etc.) are described in the review.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "i bought a deal which promised i would get NEW cards, and all i got were useless duplicates"
  - why: Real money was spent on a deal with an uncertain, randomized outcome (which cards would be received), a chance-based wager for a prize.
- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The reviewer is driven by the need to finish an album (a full set) to obtain the grand prize, the core collection-completion compulsion.
- `P_RewardMania` - ok
  - span: "promised i would get NEW cards, and all i got were useless duplicates"
  - why: The purchase yielded duplicate items from a randomized delivery pool rather than the promised specific cards, showing the unpredictable delivery mechanism itself is what sustains repeated spending/engagement.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (6)

### `5f3e71b5-200c-45a3-b90e-e08b0dc0e1a3` - Cash Frenzy™ - Casino Slots

> Is a good game, but I will like to place my formal complain about the genie game, in multiple times whe the wheel spin after stopping on a great price the genie move the wheel to a spin tag, and then the prices after the spin are way lower than the original price, from 100 million with 5x multiplier to a 48 million. Is the only part I don't like. There should be a player choice to keep or spin.

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_RewardMania` |
| pred | `P_IllusionOfControl` |
| **missed** | `P_RewardMania` |

**Did the model consider what it missed?**

- `P_RewardMania` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes a bonus 'genie' wheel mini-game within a slots app. The core complaint is that after the wheel visibly stops on a high prize, the game then moves it to land on a lower prize tag, so the displayed outcome is not honored and the actual payout is deliberately reduced ('the genie move the wheel to a spin tag, and then the prices after the spin are way lower than the original price'). This is an explicit allegation that the game manipulates or overrides the determination of the outcome after it appears settled, which is a claim about concealed/manipulated result determination rather than simply an unlucky spin or a general unfairness complaint. This matches the 'alleged rigging' pattern under Illusion of Control, since a mechanism is specifically described (the wheel being moved after stopping on a good result) rather than just a losing streak. There is no mention of real money being wagered on this wheel, so Gambling does not apply, and the complaint is about the mechanism misrepresenting the outcome rather than about the reward's random delivery schedule itself, so Reward Mania is not clearly supported either. The reviewer's request for a 'choice to keep or spin' is a suggestion for a feature that does not currently exist, which per R12 is not codable.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "in multiple times whe the wheel spin after stopping on a great price the genie move the wheel to a spin tag, and then the prices after the spin are way lower than the original price"
  - why: The review describes the game moving the wheel away from an already-displayed high prize to a lower one, which is a specific claim that the outcome determination is manipulated after the result appears settled, rather than a general complaint about bad luck.

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

- `M_RecurringFee` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review opens with a customer service complaint: diamonds (an in-game currency) were not refunded or honored when a game element failed to appear within the allotted moves. This reads as a service/support failure tied to a specific in-game event mechanic rather than a description of a deliberate monetization or scarcity design, and no clear dark pattern mechanism (conversion rate, scarcity, wager) is described in that span, so per R2/R4 it does not support a label on its own. The reviewer explicitly states the game does not require payment to win, which is a denial of Pay to Progress, not a description of the mechanic being present, so R12/R7 do not license assigning it. The reviewer advises against buying anything 'beyond the pass,' naming a pass purchase, but no schedule, expiry, task-completion pressure, or playtime-maximizing incentive is described for it, so this alone does not meet Recurring Fee's definition (R4). Finally, the review recommends getting 'friends and a team' to 'trade lives,' which explicitly names a resource-donation/exchange mechanic between players — this matches the Reciprocity pattern of feeling obligated to share resources like lives with other players.
```

**Labels assigned**

- `S_Reciprocity` - ok
  - span: "Get friends and a team and trade lives."
  - why: The review names an explicit resource-transfer mechanism between players (trading lives) facilitated through joining a team, which is the core indicator for Reciprocity.

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
The reviewer describes a daily reward system that recently changed: completing the daily reward now requires betting 50,000 in-game currency, but through normal timed play (the free path) they can only accumulate up to 40,000. This is a daily task/reward mechanism with a threshold that resets and cannot be met through unpaid play. The reviewer explicitly states 'I'd not pay just to get my daily rewards,' establishing that the shortfall between the free ceiling (40,000) and the requirement (50,000) can only be closed by spending money, i.e., the daily reward task itself is a progress gate contingent on payment. This satisfies both the Daily Rewards pattern (a resetting daily task tied to reward completion) and Pay to Progress (a free alternative that falls short, forcing a paid route to complete the daily task).
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "The most I can seem to get on the timed rewards is 40,000. I'd not pay just to get my daily rewards."
  - why: The free/timed path caps out below the 50,000 threshold needed to complete the daily reward, and the reviewer's refusal to pay implies payment is the only route to close that 10,000 gap, satisfying the free-alternative-falls-short condition for Pay to Progress.
- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: Describes a daily reward task with a completion requirement (betting 50,000) that must be met to claim the reward, consistent with a daily task list tied to reward delivery.

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
The reviewer describes a city-building/alliance game that becomes tedious after an initial phase. The core activity described is repetitive: 'grinding resources trying not to get raided so you can level up to have a few more attempts' names an explicit repeated task (grinding resources) undertaken to progress, which is Grinding. The alliance PvP is described not as ordinary sanctioned competition but as an asymmetric predation dynamic: bigger alliances attacking smaller ones and taking their resources, i.e., stronger players preying on weaker ones who presumably cannot respond in kind, which per the boundary rule shifts this from ordinary Competition into Encourages Anti-Social Behavior since the gain (resources taken) flows to the aggressor from the asymmetric act. The mention of 'the advertisement' is too garbled and lacks any description of forced viewing or reward-for-watching, so it does not meet the Advertisement indicator. The closing statement about dedicating time and being disappointed expresses regret/sentiment without describing a mechanic that pressures continued play or forfeiture of investment, so it does not rise to Easy to Get, Hard to Lose under R2/R3.
```

**Labels assigned**

- `S_EncouragesAntiSocialBehavior` - ok
  - span: "The bigger alliances all just attack the smaller alliances and take their resources."
  - why: Describes an asymmetric predation mechanic where stronger groups take resources from weaker ones who cannot respond in kind, with the gain flowing to the aggressor, which the codebook routes to Anti-Social Behavior rather than plain Competition.
- `T_Grinding` - ok
  - span: "It's just grinding resources trying not to get raided so you can level up to have a few more attempts at the left right scroller game."
  - why: Names a repetitive activity, grinding resources, that must be repeated to level up and gain further attempts, which is exactly the repeated-task-for-progress pattern.

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
The reviewer describes Monopoly GO's sticker album system: collecting stickers to complete sets, but repeatedly receiving duplicates and being unable to finish sets without paying. This names the collection-completion compulsion directly (working toward finishing all sets), a payment gate on that completion (the game never lets you finish unless you pay), and a randomized/duplicate-heavy delivery mechanism (always getting duplicates) that reflects an unpredictable reward pool rather than a fixed earn-rate.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: Completing the sticker sets, the core progression goal, is stated to require payment; without paying, progress is blocked.
- `P_CompleteTheCollection` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: The reviewer is driven by the compulsion to finish all sticker sets, naming the collection-completion goal directly.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: Getting duplicate stickers describes an unpredictable, randomized delivery of rewards from a pool, where repeated attempts are needed to obtain a specific missing item rather than the value of the reward itself.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `7b564746-b769-4856-b686-529f8717c3ba` - Candy Crush Soda Saga

> I like the game except: 1. I was charged 10 gold pcs for 5 moves, I had 2 moves left. I had 7 moves but only used 1 move. 2. I paid for a pkg unlimited lives ect. I got the etc. but not the lives. 3. The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone. 4. You cannot win enough gold to play without buying sometimes. 5. The packages need to cost less. 6. When I buy pkg should not be timed.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `M_PayToProgress`, `T_PlayingByAppointment` |
| pred | `M_PayToProgress`, `T_PlayingByAppointment` |
| **missed** | `M_IntermediateCurrency` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**

**Model analysis**

```
The review lists several complaints. Points 1 and 2 describe being charged gold incorrectly for moves and paying for a 'unlimited lives' package but not receiving the lives - these read as billing/delivery failures (technical faults) rather than deliberate design mechanics, so under R11 they are not codable as dark patterns. Point 3 describes a purchased timed bonus that continues to count down in real time whether or not the player is actively playing, meaning the player loses value simply by sleeping or being away - this is a real-world clock imposed on the player that forfeits value if not used within the window, matching Playing by Appointment (especially via its Recurring Fee boundary rule about a pass's clock operating on the player). Point 6 reinforces this same timed-package complaint. Point 4 explicitly states that the gold currency cannot be earned in sufficient quantity to keep playing without buying more, which is a narrative-obligation style Pay to Progress pattern. Point 5 ('packages need to cost less') is a pure price/value complaint with no mechanic described, so it does not trigger any label under R2.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The reviewer states that in-game earned gold is insufficient to continue playing, implying purchase is required to progress, which is a Pay to Progress pattern.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone."
  - why: The timed bonus depletes on a real-world clock regardless of play, forcing the player to be online during the game's schedule or lose the reward, which is the core of Playing by Appointment.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (6)

### `95ddadb3-82cd-4042-8a51-cf8b3ed164c2` - Mech Arena - Shooting Game

> You stuck waiting 30 seconds just to connect to a match. This game makes it seem like they give so many rewards but if all just for show. Its difficult to get weapon upgrades or any percs others you stick battling to win. This kind of games just rob you of your time in my opinion

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `S_Competition`, `T_Grinding` |
| **spurious** | `S_Competition`, `T_Grinding` |

**Model analysis**

```
The review complains about three things: a matchmaking wait ('waiting 30 seconds just to connect to a match'), a vague claim that advertised rewards are hollow ('makes it seem like they give so many rewards but if all just for show'), and difficulty obtaining weapon upgrades or perks that requires repeated battling to win. The matchmaking wait is a service/queue delay, not a designed timer gate like energy or cooldowns, so per the worked NONE example it does not qualify as Playing by Appointment or Wait to Play. The 'rewards are just for show' remark is too vague and unspecific to tie to any concrete mechanism (no chance mechanic, no specific reward delivery system, no purchase or scarcity described), so it does not satisfy any Psychological or Monetary indicator and codes NONE. The remaining complaint, however, names a repeated activity, battling, as the means by which the player must try to obtain weapon upgrades and perks ('difficult to get weapon upgrades or any percs others you stick battling to win'), which satisfies Grinding: repetitive combat sessions are the mechanism through which progress toward upgrades is made. This same span also shows the game structured around player-vs-player combat as the route to advancement, which satisfies Competition since the reviewer is describing having to fight/battle other players ('win') to get ahead.
```

**Labels assigned**

- `S_Competition` - **SPURIOUS**
  - span: "others you stick battling to win"
  - why: The player must battle other players to win, indicating the game structures progress around player-vs-player competition.
- `T_Grinding` - **SPURIOUS**
  - span: "Its difficult to get weapon upgrades or any percs others you stick battling to win"
  - why: Repeated battling is named as the activity the player must perform to obtain weapon upgrades and perks, i.e., a repetitive task required for progress.

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
The reviewer is largely praising the game and explicitly contrasts it favorably against other games' monetization. They mention 'in app purchases in the game but their being very reasonable about the price unlike other games' and then describe a specific mechanic: when you spend money on a purchase, 'bingo gives you twice the number of your purchase.' This describes a real-money-to-virtual-currency conversion where the purchase yields in-game credits/coins at a bonus rate — the direction of the transaction (money converted into an acquired quantity of something used in-game) satisfies the Intermediate Currency pattern (R5's boundary rule on direction of transaction), regardless of the reviewer's positive framing (R7/R8: code the mechanic, not the evaluation). Beyond that, the review is otherwise a general positive endorsement ('very fun game,' 'different modes an events to get into') without naming a specific repetitive task, schedule, wager, or UI mechanism, so no other label's indicators are satisfied under R2/R3. The general mention of 'in app purchases... being very reasonable' alone, without a mechanism, does not independently trigger any monetary label per the worked NONE example in R2.
```

**Labels assigned**

- `M_IntermediateCurrency` - **SPURIOUS**  _[span loose match]_
  - span: "if your spend $20 on some item you get less then what your actually hoping for, but on here bingo gives you twice the number of your purchase"
  - why: The span describes real money being spent and converted into a quantity of in-game currency/credits at a bonus multiplier, which is the money-to-virtual-currency conversion relation that defines Intermediate Currency, independent of whether the reviewer views the rate favorably.

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
The review describes a base-building game with repetitive resource/building tasks ('Same old same old grinder'), which is a grinding complaint. The core complaint is that events cannot be won by skill or effort alone; winning requires massive real-money spending ('Zero skill pay to play. Zero skill pay to win. Calculated total spent on last event was 30k to win'). This ties spending directly to winning an in-game competitive event, which is Pay to Progress (specifically the Pay to Win variant) combined with Competition since the event is against other players. There is no mention of currency conversion, UI tricks, collections, or other mechanics - just grinding, pay-to-win events, and competitive structure.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Zero skill pay to play. Zero skill pay to win. Calculated total spent on last event was 30k to win."
  - why: Winning the event is explicitly stated to require spending a large sum of money rather than skill, directly satisfying Pay to Win.
- `S_Competition` - ok
  - span: "there is absolutely no opportunity for a general player to win an event"
  - why: The event described is a competitive contest between players where only the top spender can win, indicating a player-vs-player competitive structure.
- `T_Grinding` - **SPURIOUS**
  - span: "Same old same old grinder"
  - why: The reviewer names the game's core loop as repetitive grinding ('grinder'), describing the base-building activity as tedious and repetitive.

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
The reviewer names pay-to-win directly. They then describe base upgrade timers ('update times for your base') growing worse, and content that 'scales endlessly' with 'no point to look forward to, just more grind' -- this is both a repetitive-task complaint (Grinding) and a description of the game extending goals beyond completion (Infinite Treadmill), while the timer growth itself is a Wait-to-Play style schedule (Playing by Appointment). The UI complaint is not a generic quality gripe: the reviewer explicitly attributes a purpose to the confusing design -- 'deliberately confusing and overwhelming to achieve the effect that you need to buy stuff' -- which matches the boundary rule that lifts a UI complaint into UI Misdirection when the reviewer states the manipulative purpose. Finally, the alliance description shows inter-player conflict: being outside an alliance leads to being 'attacked and bullied', which is competitive PvP pressure (Competition). There is no explicit reward described flowing to the aggressors beyond the attack itself, and no obligation to teammates is described (the alliance pressure is about hierarchy dictating strategy, and being outside means becoming a target, which is coerced-grouping-for-protection territory rather than Forced Fellowship, per the boundary rule excluding pure protection-motivated grouping).
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "it's set up in a pay to win way"
  - why: Reviewer directly labels the game's monetization as pay-to-win, granting advantage/progress to paying players.
- `M_UIMisdirection` - ok
  - span: "The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff"
  - why: Reviewer attributes the confusing UI design to a purpose against the player's intent -- inducing purchases -- which lifts it from a generic quality complaint to UI Misdirection.
- `S_Competition` - ok
  - span: "If you are not in one then you get attacked and bullied"
  - why: Being outside an alliance results in being targeted by other players, showing the game structures player-vs-player conflict.
- `T_Grinding` - **SPURIOUS**
  - span: "there is kinda no point to look forward to, just more grind"
  - why: Reviewer explicitly names the repetitive activity required to progress as 'grind'.
- `T_InfiniteTreadmill` - ok
  - span: "Everything scales endlessly"
  - why: Describes the game's content/requirements expanding without an attainable end state, preventing completion.
- `T_PlayingByAppointment` - ok
  - span: "the update times for your base are becoming ridiculous"
  - why: Describes an escalating build/upgrade timer imposed by the game that the player must wait out, matching the wait-to-play schedule pattern.

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
The reviewer describes long-term play since COVID, now stuck around level 8000+ with steep difficulty. Two mechanics are described concretely: running out of lives multiple times a day, which forces waiting before continuing (a resource-depletion wait gate), and needing to buy 'add ons' to get through levels, framed as the alternative to wasting time. The '5-7 days per level' figure describes repeated attempts to beat the same level, which is a repetitive grind rather than just a statement of slowness, since it's tied to the daily life-depletion cycle described just before it. No named currency, collection, or gambling mechanic is present, so those labels don't apply.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying."
  - why: The review states purchase of add-ons is required to progress, with the free path framed as an unreasonable time waste, satisfying the paid-vs-free progress contrast.
- `T_Grinding` - ok
  - span: "avg 5-7 days per level"
  - why: Taking multiple days per level, driven by the repeated life-depletion cycle just described, indicates the player must repeat attempts at the same level to progress, not merely that progress is slow.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "I run out of lives 3-4 times daily to beat every alternate level"
  - why: Running out of lives multiple times a day describes a resource that depletes and must be waited out on the game's regeneration schedule before continuing.

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
The reviewer levels several complaints. The claim that the reward system is 'DIABOLICAL' because a 7-hour quest yielded few primogems is a complaint about the value/quantity of a reward, not about how it is delivered (no unpredictability, complexity, or out-of-game activity is described), so it does not meet Reward Mania or Pay to Progress on its own. 'Exploration is debilitating' and criticism of character design are general quality evaluations with no specific repeated task or monetization mechanism named, so they code NONE under R2. The final line, 'there is no resin overflow system,' references Genshin's resin mechanic: a stamina-like resource that regenerates on a timer and caps at a maximum, meaning unused regeneration is lost once the cap is hit unless the player returns to spend it. The reviewer's complaint about the absence of an 'overflow system' presupposes and describes this capped, timer-driven resource, which is a designed wait/regeneration schedule that pressures the player to log in periodically to avoid wasting potential resin. This matches the Wait to Play indicator under Playing by Appointment.
```

**Labels assigned**

- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "there is no resin overflow system"
  - why: Resin is a capped, timer-based regenerating resource; the complaint that it lacks an overflow system implies the resource caps on the game's schedule and is wasted if the player doesn't log in to spend it, pressuring play according to the game's timer rather than the player's own schedule.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `S_Competition` | 4 | 1 |
| `T_Grinding` | 2 | 3 |
| `M_IntermediateCurrency` | 2 | 2 |
| `M_PayToProgress` | 0 | 3 |
| `M_Gambling` | 2 | 1 |
| `T_PlayingByAppointment` | 1 | 2 |
| `P_AestheticManipulation` | 2 | 0 |
| `S_Reciprocity` | 2 | 0 |
| `M_EasyToPurchase` | 1 | 1 |
| `P_RewardMania` | 2 | 0 |
| `S_FriendSpamImpersonation` | 1 | 0 |
| `P_IllusionOfControl` | 0 | 1 |
| `T_MandatoryMarathon` | 1 | 0 |
| `M_RecurringFee` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `P_CompleteTheCollection` | 0 | 1 |
| `M_WasteAversion` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |

