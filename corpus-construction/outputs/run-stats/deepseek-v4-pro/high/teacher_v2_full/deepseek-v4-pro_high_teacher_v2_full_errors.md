# Error review - deepseek-v4-pro_high_teacher_v2_full

`deepseek-v4-pro` / reasoning `high` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `6529a474a2b0`  
micro-F1 **0.807** (P 0.789 / R 0.826) - **24 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 4 | said NONE, gold had labels |
| SWAP | 6 | picked different labels than gold |
| MISSED ONLY | 3 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 11 | found all gold, added extras |

## The diagnostic that matters

Of **15** missed labels, **3** (20%) were named in the model's own analysis and dropped anyway; **12** (80%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `M_Gambling` | 1 | 1 |
| `S_Competition` | 1 | 1 |
| `P_AestheticManipulation` | 0 | 2 |
| `S_Reciprocity` | 1 | 1 |
| `P_RewardMania` | 0 | 2 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `M_EasyToPurchase` | 0 | 1 |

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
The review is a list of feature requests and quality-of-life suggestions. The reviewer asks for auctions, removal of a decoration option, a widget, and a hidden statistics toggle. Under R12, only mechanics explicitly described as currently present in the game are codable; requests and hypothetical additions do not trigger labels for the proposed mechanics. None of the spans describe a present dark pattern mechanic. The mention of an existing option to remove an obstacle turned into a decoration references current behavior but is itself a request for its removal, and no listed label fits it.
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
- `S_Reciprocity` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review is entirely a bug report: opening gifts or trading with friends crashes the game, tapping a Pokémon causes lag so the player cannot throw a pokeball, and PvP/rocket battles lag with slow switching, unresponsive charge attacks, and freezes while the opponent keeps attacking. Every described behaviour is attributed to bugs, lag, or freezing, i.e., technical malfunctions, not to deliberate game design. Under R11 these do not assign dark-pattern labels. The mention of gifts and trading with friends describes the crash context, not a social dark pattern such as an obligation, spam, or a reciprocity incentive.
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
The reviewer is expressing affection for the game but raising a concern about progress and in-game purchases being lost if the game is deleted. Their message is framed as a request or suggestion: they ask whether the developers can implement saving for progress and purchases, and they conditionally say they would spend money if such saving existed. The loss-on-deletion fear is attributed to their experience with other games and to the apparent absence of a save/account feature in this game. There is no described deliberate game mechanic that manipulates time, money, social ties, or psychology. The save feature itself is a proposal, not an existing mechanic, so under R12 it cannot be tagged. The mention of in-game purchases is only about what would be lost, not about how purchases are solicited, priced, or used to gate progress. No label is satisfied.
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
The reviewer reports that a clan troop-request feature stopped working after a game update and asks the developer to fix it. The text names a clan/team request mechanic but frames it entirely as a malfunction: the feature is no longer usable and 'needs to be fixed.' No dark-pattern mechanic is being described as a deliberate design behavior. Under R11, a specific behavior attributed to a bug or technical fault is not coded, and the clan request feature is mentioned only as a broken function, not as an obligation, reciprocation, or recruitment mechanism.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (6)

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
The review has two distinct parts. The first part describes a mechanic the reviewer noticed after they began buying Poké Balls: captured Pokémon 'keep breaking out', which consumes the purchased balls faster and forces the player to buy more. That is both a claim that the game tunes catch outcomes to drain paid items (hidden manipulation of the outcome), and a structure where continuing the core catching loop requires repeated payment. The second part is an edit disclaiming the review: the reviewer says they did not write it and do not know any other players, which implies the review was posted under their account without their authorship. That matches the impersonation pattern of content published as the player.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "so I go through the balls faster so I have to purchase more"
  - why: Continuing to capture Pokémon requires the player to keep buying balls because the purchased balls are consumed faster, making further play contingent on payment.
- `P_IllusionOfControl` - ok
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster"
  - why: The span claims catch outcomes (breakouts) are manipulated after purchases begin, draining paid balls faster and concealing the real odds.
- `S_FriendSpamImpersonation` - ok
  - span: "I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE"
  - why: The reviewer disclaims authorship of the review, implying it was posted under their account without their writing, which is content published as the player.

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
The reviewer describes three distinct things after the new season started. First, friend invitations were previously tied to rewards and now are not credited: the review names inviting friends and getting them to join Facebook as something the player did in expectation of rewards, which is a social recruitment incentive. Second, the player describes struggling to get dice and then a losing run at max bet with no shutdowns or bank heists; this is a chance-based outcome whose stake is earned dice, and no real-money purchase is mentioned anywhere in the review, so the gambling/monetary labels do not reach it, nor does a bare losing run code Illusion of Control. Third, sticker packs keep yielding duplicates, which shows both a collection-completion drive and randomized, unwanted drops from the sticker pool. Finally, the inability to log in due to an internet connection error is a technical fault and is suppressed under R11, not a design pattern.
```

**Labels assigned**

- `P_CompleteTheCollection` - **SPURIOUS**
  - span: "Stickers are duplicates all the way"
  - why: The player is working toward completing sticker sets and is blocked by receiving only duplicates, which is the collection-completion compulsion.
- `P_RewardMania` - ok
  - span: "Stickers are duplicates all the way"
  - why: The sticker packs deliver randomized duplicates rather than the missing items, which is a variable-reward delivery mechanic rather than a complaint about reward value.
- `S_ForcedFellowship` - ok
  - span: "I get no rewards for inviting friends and getting them to join facebook"
  - why: The player invited friends to join and expected rewards, describing the game's incentive to bring new people into its social circle even though the reward stopped being credited.

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
The reviewer is describing a UI dark pattern in the bet-table selection. On opening the game or the 1v1 section, the interface automatically scrolls to and selects the highest possible bet table based on the player's coin balance, which the reviewer says causes accidental mis-clicks. Those mis-clicks lose the player's hard-earned coins, and the player is then forced to buy coins with real money to keep playing. Three mechanics are present: the interface steering the player toward the highest bet (attention-direction against the player's intent), the loss of coins forcing a real-money coin purchase to continue, and the conversion of real money into in-game coins ('real ones' clearly refers to coins as opposed to 'hard-earned' coins).
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "forced to buy real ones"
  - why: 'Real ones' refers to coins purchased with real money as opposed to hard-earned coins, showing real money being converted into in-game currency.
- `M_PayToProgress` - **SPURIOUS**
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: Losing all coins blocks further play, and the player is forced to buy coins with real money to continue, which is payment required to progress/keep playing.
- `M_UIMisdirection` - ok
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins"
  - why: The interface steers the player to the highest-stakes option by default, directing attention/selection away from the player's intended choice and toward a costly option.

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
The reviewer is describing a monetised collection-and-goal game (Dice Dreams). Several mechanics are present. First, they say they only rated five stars because the app will not let them write a review otherwise, which is a review-gating behaviour, but none of the codebook labels directly covers a rating prompt that suppresses low-star reviews, so I set that aside. Second, winning is described as costing hundreds of dollars, which is pay-to-win progress gating. Third, the sticker album cannot be finished because the last one or two stickers are effectively withheld unless the player pays a lot, which combines the compulsion to complete a collection with developer-manufactured scarcity of the final items. Fourth, the reviewer states the game 'lets' you complete a goal only about one time in a hundred, which asserts that goal outcomes are determined by the game on a fixed, hidden ratio rather than by the player.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: The final stickers are made artificially unobtainable through normal play, and payment is the only route to them, so the scarcity directly drives the purchase.
- `M_PayToProgress` - ok
  - span: "if you want to win anything on this game it will cost hundreds of dollars"
  - why: Winning is stated to require spending hundreds of dollars, establishing that advantage is purchased.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: The reviewer is working to finish a sticker set and frames the missing final stickers as the pain point, showing the collection-completion pull.
- `P_IllusionOfControl` - **SPURIOUS**
  - span: "it may let you complete a goal maybe one out of hundred times"
  - why: The span asserts the game itself grants goal completion on a fixed, hidden ratio rather than the player's skill deciding it.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `12267c1e-47ba-4984-97c8-768e820ceb1c` - Bingo Blitz™️ - Bingo Games

> not very user-friendly. no apparent reachable goals within a decent amount of time. I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| pred | `M_Gambling`, `M_PayToProgress`, `P_CompleteTheCollection`, `P_RewardMania`, `T_Grinding` |
| **missed** | `M_EasyToPurchase`, `P_AestheticManipulation` |
| **spurious** | `M_Gambling`, `M_PayToProgress`, `P_RewardMania` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - never mentioned -> **attention / recall**
- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer is describing the loop of playing Bingo Blitz rounds to collect photos for a set. After a loss, the game presents an offer to spend extra coins to claim a missing photo and complete the set. The reviewer accepts this repeatedly, gets several bingos, but says the promised photo still does not drop, and they have wasted real money. A web search confirms that Bingo Blitz has a post-loss Challenge Round where coins are spent for a chance at a missing photo. This is both a paid-progress mechanic and a chance-based paid reward mechanic, wrapped around a collection goal.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money"
  - why: The player pays coins, funded by real money, for a chance-based challenge to win a photo; the repeated failures and wasted money make the paid wager explicit.
- `M_PayToProgress` - **SPURIOUS**
  - span: "spend extra coins to claim a photo I don't have to complete the set"
  - why: Paying coins is the offered route to obtain a needed photo and progress set completion after losing.
- `P_CompleteTheCollection` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The photos are collectibles needed to complete a set, and the reviewer is playing repeatedly to acquire them.
- `P_RewardMania` - **SPURIOUS**
  - span: "I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED"
  - why: Even after meeting the apparent bingo requirement, the promised photo reward is not delivered, showing an unpredictable chance-based reward schedule that fuels repeated attempts.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The reviewer performs the same bingo round repeatedly to obtain collectible photos, which is the repetitive activity needed to progress the set.

**Search:** `Bingo Blitz spend coins after losing round to claim a photo complete the set` -> After losing a Bingo Blitz round, players can spend coins on a Challenge Round for a chance to claim a missing photo; photos complete sets.

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
The reviewer describes a card album in Dice Dreams: completing an album awards a grand prize, and the player was two cards short. To finish, they bought an in-app purchase 'deal' that was advertised as giving new cards, but the cards it actually delivered were duplicates. Three mechanics are visible. First, the album itself is a collection the player is driven to complete. Second, the purchased deal delivers cards through a chance-based draw: real money was spent and the result (new vs. duplicate) was a matter of luck, not the guaranteed new card the deal promised. Third, the delivery produced unwanted duplicate drops from a randomised pool, which is a variable-reward structure rather than a guaranteed payoff. The 'Free Cash' mention is third-party/out-of-game promotion and is not codable under R13. The review does not describe a currency conversion, a pay-to-progress gate on the core game, or a scarcity tied to price beyond the general difficulty of finishing the album.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "i bought a deal which promised i would get NEW cards, and all i got were useless duplicates"
  - why: Real money was spent on a card deal whose outcome (new card vs. duplicate) was determined by chance rather than the guaranteed new cards promised.
- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The player is working to complete a full card album and the missing two cards drive the purchase; this is the compulsion to acquire all collection items.
- `P_RewardMania` - ok
  - span: "all i got were useless duplicates"
  - why: The purchased deal delivered unpredictable, unwanted duplicate drops from a randomised pool instead of a fixed reward.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (3)

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
The reviewer is describing a bonus 'genie game' inside a casino slots app. They describe a wheel that spins, appears to stop on a great prize (100 million with a 5x multiplier), but then the genie moves the wheel to a 'spin tag' and the resulting prize is much lower (48 million). This is a claim that the game manipulates or rigs the outcome of the wheel after it has appeared to land on a good prize. The closing request for a 'player choice to keep or spin' is a suggestion for a feature that does not exist, so it does not itself trigger a label. The wheel is a chance mechanic, but no monetary stake or real-money currency purchase is described in this span, so Gambling and Intermediate Currency do not apply.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "the wheel spin after stopping on a great price the genie move the wheel to a spin tag, and then the prices after the spin are way lower than the original price, from 100 million with 5x multiplier to a 48 million"
  - why: The reviewer describes the wheel appearing to land on a great prize and then being moved by the genie to yield a lower prize, asserting the outcome is manipulated rather than left to genuine chance.

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
The reviewer describes the core loop after the early building stage: gathering resources to level up, which gates access to attempts at a side mini-game. The activity required for that progress is explicitly called 'grinding resources,' which is the repetitive task the player must perform to advance. Separately, the reviewer describes the PvP raiding system: larger alliances attacking smaller alliances and taking their resources. That is asymmetric predation, with the stronger side gaining resources at the weaker side's expense, which fits the anti-social behavior pattern rather than ordinary sanctioned competition. The sentence about 'advertisement' is vague and does not describe forced or incentivized ad viewing, so it does not trigger T_Advertisement. The closing line about dedicating time to the game and alliances reports investment but shows the player disengaging in disappointment, not being held by sunk cost or social obligation, so no Easy-to-Get-Hard-to-Lose or Forced Fellowship label applies.
```

**Labels assigned**

- `S_EncouragesAntiSocialBehavior` - ok
  - span: "The bigger alliances all just attack the smaller alliances and take their resources"
  - why: The span shows stronger alliances attacking weaker ones and taking their resources, which is asymmetric predation where the aggressor gains at the expense of players who cannot respond, matching the 'stronger players rewarded for attacking weaker ones' example.
- `T_Grinding` - ok
  - span: "It's just grinding resources trying not to get raided so you can level up"
  - why: The span names the specific repetitive activity (grinding resources) required to make progress (level up), which satisfies Grinding.

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
The reviewer is describing the sticker album system in MONOPOLY GO. Stickers arrive in a way that produces constant duplicates, which frustrates the goal of completing the sets. The reviewer then states that finishing all sets is impossible without paying, framing payment as the gate to completing the collection. The text describes three things at once: the compulsion to complete the sticker sets, the random/duplicate delivery of sticker rewards, and a progress gate that is contingent on payment. No obscure term needs external resolution; stickers, sets, and duplicates are understandable from the review itself.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: Completing the sticker sets is contingent on making a payment, which is a progress gate.
- `P_CompleteTheCollection` - ok
  - span: "never lets you finish all the sets"
  - why: The reviewer is driven to acquire all stickers and complete every set, and the inability to finish is the stated harm.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: The reward delivery is random and produces unwanted duplicate stickers, sustaining engagement through the delivery rather than the reward's value.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (11)

### `8da35d79-a1e5-46ef-b545-cc2cc3c4d671` - Cash Frenzy™ - Casino Slots

> Do not buy from this game!!! Constant "display" issues as the developer states when you tell them you are missing coins lost of 161Billion. The just disappeared. When you complain to them the send a graph that they expect you to know how to read.

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `M_IntermediateCurrency` |
| **spurious** | `M_IntermediateCurrency` |

**Model analysis**

```
The reviewer is warning others not to make purchases in this casino slots game. In a slots game, the thing you buy is the game's coins/chips. The reviewer reports that 161 billion coins vanished and that the developer attributed the disappearance to 'display issues' — a technical fault. The loss of coins is therefore being explained as a malfunction, not as a deliberate design rule, so the disappearance itself does not support a dark-pattern label under R11. What remains is the purchase mechanism itself: real money converted into the in-game currency (coins). That exchange is implied by 'Do not buy from this game' alongside 'missing coins lost of 161Billion.'
```

**Labels assigned**

- `M_IntermediateCurrency` - **SPURIOUS**
  - span: "Do not buy from this game!!! Constant "display" issues as the developer states when you tell them you are missing coins lost of 161Billion."
  - why: The warning 'Do not buy' together with 'missing coins' implies the reviewer purchased the in-game currency (coins) with real money, satisfying the real-money-to-virtual-currency exchange; the direction is money -> coins.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `95ddadb3-82cd-4042-8a51-cf8b3ed164c2` - Mech Arena - Shooting Game

> You stuck waiting 30 seconds just to connect to a match. This game makes it seem like they give so many rewards but if all just for show. Its difficult to get weapon upgrades or any percs others you stick battling to win. This kind of games just rob you of your time in my opinion

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `T_Grinding` |
| **spurious** | `T_Grinding` |

**Model analysis**

```
The reviewer makes three observations. First, there is a 30-second wait to connect to a match, which is a matchmaking/queue delay rather than a designed in-game timer gate (no energy, build timer, or cooldown is described). Second, the game presents rewards that feel substantial but the reviewer says they are mostly for show, which is a complaint about reward value, not about how rewards are delivered. Third, obtaining weapon upgrades or perks is difficult and requires the player to keep battling to win, naming the repeated activity through which progress is earned. No spending or payment alternative is mentioned anywhere in the review.
```

**Labels assigned**

- `T_Grinding` - **SPURIOUS**
  - span: "Its difficult to get weapon upgrades or any percs others you stick battling to win"
  - why: The span names the repeated activity (battling to win) that the player must keep doing in order to obtain weapon upgrades and perks, so progress is earned through repetitive play rather than merely described as slow.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `0347fbc7-5c01-452e-ae4b-867f5bd7dd47` - Homescapes

> I really enjoy this (very) addicting and fun game. The levels get harder, but its fun to beat after a while. I only have a few suggestions; maybe only 5-10 minutes for a new life, not as many small and unnecessary tasks like celebrating and just because you miss a day doesnt mean that you need to start over on your daily prizes. But overall, I would recommend this game to anyone and the creators did a very good job on this game.👍

| | labels |
|---|---|
| gold | `T_DailyRewards`, `T_PlayingByAppointment` |
| pred | `T_DailyRewards`, `T_Grinding`, `T_PlayingByAppointment` |
| **spurious** | `T_Grinding` |

**Model analysis**

```
The reviewer is mostly positive and frames their complaints as suggestions, but the suggestions reveal existing mechanics in the game. First, lives regenerate on a timer and the player wishes new lives came every 5-10 minutes, which implies the current regeneration wait is longer than that. Second, the game presents many small renovation tasks such as celebrating, which the player describes as unnecessary. Third, daily prizes reset when a day is missed, which the player wishes did not happen. Under R12, the proposed changes do not get tagged, but the existing behaviours they describe alongside the suggestions remain codable.
```

**Labels assigned**

- `T_DailyRewards` - ok
  - span: "just because you miss a day doesnt mean that you need to start over on your daily prizes"
  - why: Daily prizes exist and resetting them after a missed day is a penalty for not logging in daily, which is Daily Rewards.
- `T_Grinding` - **SPURIOUS**
  - span: "not as many small and unnecessary tasks like celebrating"
  - why: The reviewer names the task type (celebrating) and describes the tasks as small and unnecessary, implying the game requires many such tedious tasks to progress.
- `T_PlayingByAppointment` - ok
  - span: "maybe only 5-10 minutes for a new life"
  - why: The suggestion implies lives currently regenerate on a timer longer than 5-10 minutes, which is a life refill wait the game imposes.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b98d7e75-73da-4591-b23e-1a2951bfd856` - Township

> I like this game a lot, but recently after seeing the ads, there is no way to close it. No cross mark on the screen , if you try to click anywhere on the screen it takes you to store. If you go back to game it is still stuck in the last sceeen of the ad. You have to kill the game to come out of the ad screen , so frustrating!!!

| | labels |
|---|---|
| gold | `M_UIMisdirection`, `T_Advertisement` |
| pred | `M_EasyToPurchase`, `M_UIMisdirection`, `T_Advertisement` |
| **spurious** | `M_EasyToPurchase` |

**Model analysis**

```
The reviewer is describing an in-game ad that cannot be closed: after the ad plays there is no close button, tapping anywhere on the screen routes the player to the store, returning to the game leaves the ad screen stuck, and the only way out is to force-quit the app. Three mechanics are present at once. The ad itself is compulsory viewing with no skip or close (Advertisement). The interface removes the exit control entirely and makes any tap select the store instead of dismissing the ad (UI Misdirection's obstructed-opt-out arm). And the player is directed to the purchase screen as a default action with no way to decline or dismiss it (Easy to Purchase's Low Barrier / Prompted-to-Buy behaviour). No web search is needed because the mechanics are described directly.
```

**Labels assigned**

- `M_EasyToPurchase` - **SPURIOUS**
  - span: "if you try to click anywhere on the screen it takes you to store"
  - why: The player is directed to the store as a default action with no way to opt out, which reduces friction before spending.
- `M_UIMisdirection` - ok
  - span: "No cross mark on the screen , if you try to click anywhere on the screen it takes you to store"
  - why: The close control is absent and any tap routes the player to the store, obstructing the opt-out from the ad and the purchase surface.
- `T_Advertisement` - ok
  - span: "after seeing the ads, there is no way to close it"
  - why: The reviewer is compelled to view an ad with no way to close it, which is forced ad viewing.

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
The reviewer describes a base-building game as an unoriginal, repetitive grinder. The core complaint is that events cannot be won by ordinary players: winning is described as requiring large real-money spending with no skill involved, and the reviewer calculates that someone spent $30k to win the last event. This points to a pay-to-win structure (payment required for victory/progression), a competitive event framework in which players vie against one another to win, and a repetitive grind-based core loop. No currency, chance, subscription, or scheduling mechanics are described, and the final sentence about other spenders is a wish about player behaviour, not a game mechanic.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Zero skill pay to play. Zero skill pay to win. Calculated total spent on last event was 30k to win"
  - why: Winning the event is presented as requiring large money spend with zero skill, which is the Pay to Win indicator.
- `S_Competition` - ok
  - span: "there is absolutely no opportunity for a general player to win an event"
  - why: The game runs events that players compete to win, pitting players against each other for the top outcome.
- `T_Grinding` - **SPURIOUS**
  - span: "Same old same old grinder"
  - why: Calling the game a 'grinder' implies the player must perform repetitive, tedious tasks to make progress.

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
The reviewer is describing a base-building war game and identifies several mechanics at once. They name the game as pay-to-win, which is a paid advantage. They describe base upgrade timers that grow unreasonable, which is a wait the game imposes on the player's schedule. They say everything scales endlessly with no point to look forward to, only more grind: an unending treadmill plus repetitive progress work. They state the UI is deliberately confusing and overwhelming in order to push purchases, which is interface-driven monetization. Finally, they describe alliance dynamics: top alliances dictate how members develop, and players outside one get attacked and bullied, which is player-versus-player competition. The bullying is harm by stronger players but the span does not show what the aggressor gains, so the anti-social-behavior label does not apply under the permitted-harm rule. No web search is needed because the terms are self-explanatory.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "set up in a pay to win way"
  - why: The reviewer states the game grants advantage to players who pay.
- `M_UIMisdirection` - ok
  - span: "The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff"
  - why: The reviewer attributes the interface's confusing design to the deliberate purpose of driving purchases.
- `S_Competition` - ok
  - span: "If you are not in one then you get attacked and bullied"
  - why: Being attacked by other players and alliances describes the game pitting players against one another.
- `T_Grinding` - **SPURIOUS**
  - span: "just more grind"
  - why: The word 'grind' names repetitive, tedious activity as the means of progress.
- `T_InfiniteTreadmill` - ok
  - span: "Everything scales endlessly, there is kinda no point to look forward to"
  - why: The game's scaling never terminates, so the player describes no attainable end state.
- `T_PlayingByAppointment` - ok
  - span: "the update times for your base are becoming ridiculous"
  - why: Base upgrade timers impose a wait the player must schedule around rather than choosing when to progress.

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
The reviewer is describing the late-game experience in a match-3 game. They name a lives system that runs out repeatedly, which implies timed regeneration gating play. They describe having to attempt levels over and over ('beat every alternate level', 'avg 5-7 days per level'), which is grinding. They also state explicitly that buying add-ons is the only way to progress without wasting enormous time, and contrast the paid path against the free path ('pure time waste if you're not paying'), which is pay-to-progress. The closing line about wasted money and time is regret over past investment, not a mechanic keeping them in the game, so it does not trigger Endowed Value.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying."
  - why: The review states that paying is required to progress without an unreasonable time investment, contrasting the paid shortcut against the tedious free path.
- `T_Grinding` - ok
  - span: "I run out of lives 3-4 times daily to beat every alternate level, avg 5-7 days per level"
  - why: The span describes repeated attempts at levels over days as the activity required to advance, which is grinding rather than mere slow progress.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "I run out of lives 3-4 times daily"
  - why: Running out of lives multiple times daily implies a timer-based life regeneration gate: the player must stop and wait for lives to refill before continuing.

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
The reviewer is describing a time-limited card collection feature inside Royal Match. Three mechanics are present at once. First, the player is working to complete card sets, and completing a set yields a reward; missing that reward is framed as the harm. Second, cards come from card packs, and the reviewer reports that new cards stop appearing as the collection nears its end, meaning the pack delivery produces duplicates and the desired drops dry up. Third, the collection itself has an expiry window: the set is 'almost expiring' and the collection is 'about to end', so the completion reward is forfeited unless the player finishes before the game's deadline. No real-money purchase or currency conversion is mentioned, so no monetary label applies. No web search is needed; the card pack, set completion, and collection expiry are all described plainly in the review.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion"
  - why: The player is collecting cards to complete sets and the loss of the set-completion reward is the stated harm, which is the collection-completion compulsion.
- `P_RewardMania` - **SPURIOUS**
  - span: "new cards don't appear again especially when the set is almost expiring"
  - why: Card packs are a chance-based delivery system, and the span describes the drop of new cards drying up near the end, i.e., the variable/duplicate reward delivery rather than the reward's value.
- `T_PlayingByAppointment` - ok
  - span: "you will miss the reward for the set completion because they don't add new sets to the cards once the collection is about to end"
  - why: The collection runs on the game's clock and the reward is forfeited if the set is not completed before the window closes, so the schedule and the loss are both described.

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
The review is mostly dissatisfaction: a stingy reward system (a 7-hour quest yielding few primogems), exploration described as debilitating, and character design critiqued as uninteresting. Those are value/aesthetic evaluations, not game mechanics, so they do not assign labels on their own. The one functional design behaviour described is the resin system: the reviewer states there is no resin overflow system, which implies resin regenerates over time and caps, forcing players to log in and spend it before it stops accumulating or be left with wasted potential resin. No payment, gacha, or social mechanics are described.
```

**Labels assigned**

- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "there is no resin overflow system"
  - why: The complaint about no overflow implies resin regenerates over time and caps, so players must adhere to the game's schedule to spend it before it stops accumulating.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `8d13a3c1-1982-45db-a2b4-07c61c41ba2a` - Pixel Flow!

> this WAS a favorite game and WAS fun until it became unplayable. stuck on level 195 for almost 2 months. getting ready to uninstall it. I refuse to pay for power ups. should be daily login rewards to help with these harder levels.

| | labels |
|---|---|
| gold | `M_PayToProgress` |
| pred | `M_PayToProgress`, `T_Grinding` |
| **spurious** | `T_Grinding` |

**Model analysis**

```
The reviewer describes being blocked on a single level for a long period, which implies repeatedly attempting the same level to make progress. They then frame paid power ups as the way the game offers to get past these harder levels, while explicitly refusing to pay. The final clause about daily login rewards is a wish for a feature that does not currently exist, so it does not trigger Daily Rewards under R12. No out-of-game terminology needs resolving.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "I refuse to pay for power ups"
  - why: Power ups are purchasable and are the paid way past the hard level blocking the player's progress; the reviewer's refusal to pay leaves them stuck.
- `T_Grinding` - **SPURIOUS**
  - span: "stuck on level 195 for almost 2 months"
  - why: Being stuck on a single named level for two months implies the player must repeatedly attempt the same level in order to progress.

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
The reviewer is describing an update to a war strategy game that removed the player-vs-player element (referred to as 'open silver'), leaving only farming-style play. Two design mechanics are described. First, meaningful growth is gated behind spending, which is Pay to Progress. Second, the update then devalues that paid growth by removing the PvP context that gave it purpose, which is the purchased-value-loss pattern of Power Creep. 'Open silver' is explained within the review itself as the PvP feature, so no external search is needed. The removal of PvP means Competition is not currently present, and 'boring farmville' reads as a quality evaluation rather than a named grinding loop tied to progress.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You have to spend to have any meaningful growth"
  - why: The reviewer states that spending money is required for meaningful in-game progress.
- `M_PowerCreep` - **SPURIOUS**
  - span: "You have to spend to have any meaningful growth and then they go and make it all pointless"
  - why: Money spent on growth is rendered worthless by the update that removed the PvP feature, devaluing the prior investment.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `T_Grinding` | 0 | 5 |
| `M_Gambling` | 2 | 2 |
| `P_RewardMania` | 2 | 2 |
| `T_PlayingByAppointment` | 1 | 2 |
| `M_PayToProgress` | 0 | 3 |
| `P_AestheticManipulation` | 2 | 0 |
| `S_Reciprocity` | 2 | 0 |
| `S_Competition` | 2 | 0 |
| `M_EasyToPurchase` | 1 | 1 |
| `M_IntermediateCurrency` | 0 | 1 |
| `P_EasyToGetHardToLose` | 1 | 0 |
| `P_CompleteTheCollection` | 0 | 1 |
| `M_PowerCreep` | 0 | 1 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `P_IllusionOfControl` | 0 | 1 |

