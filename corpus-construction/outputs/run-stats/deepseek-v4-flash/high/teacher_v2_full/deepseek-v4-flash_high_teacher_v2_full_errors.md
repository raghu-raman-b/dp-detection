# Error review - deepseek-v4-flash_high_teacher_v2_full

`deepseek-v4-flash` / reasoning `high` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `6529a474a2b0`  
micro-F1 **0.814** (P 0.814 / R 0.814) - **24 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 4 | said NONE, gold had labels |
| SWAP | 5 | picked different labels than gold |
| MISSED ONLY | 5 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 10 | found all gold, added extras |

## The diagnostic that matters

Of **16** missed labels, **1** (6%) were named in the model's own analysis and dropped anyway; **15** (94%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `S_Competition` | 0 | 3 |
| `M_Gambling` | 1 | 1 |
| `S_Reciprocity` | 0 | 2 |
| `P_RewardMania` | 0 | 2 |
| `M_WasteAversion` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `P_AestheticManipulation` | 0 | 1 |
| `T_Grinding` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `S_FriendSpamImpersonation` | 0 | 1 |

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
The entire review is a list of four feature requests: a bidding/auction system, a change to how decorated obstacles behave, an account-switching widget with upgrade timers, and a hidden statistics menu. Each item is phrased as 'we would like' or 'remove the option', i.e., as wishes or suggestions for changes. R12 states that requests, suggestions, or hypothetical additions do not trigger tags for the proposed mechanics, and the restriction applies to the non-existent feature itself. The only currently present behavior alluded to is that an obstacle can be turned into a decoration and still be removable, but the reviewer is asking to remove that option — a proposed design change, not a description of a present dark pattern operating on the player. Nothing in the text describes an existing mechanic that satisfies any label.
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
The review is entirely a bug report. Each numbered point attributes a failure to technical faults: crashing when opening gifts or trading, lag preventing pokeball throws, lag and unresponsiveness in PvP and rocket battles, and freezes while the opponent keeps attacking. There is no description of a deliberate game rule, schedule, payment gate, social mechanic, or psychological design. Under R11, behavior attributed to bugs, glitches, errors, or technical faults is not coded as a dark pattern because dark patterns are deliberate design choices rather than malfunctions. The review asks for fixes, confirming the faults are seen as malfunctions.
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
The review reports that a previously available feature, requesting troops from one's clan, stopped working after an update. The reviewer asks for the feature to be fixed. This is a description of a malfunction introduced by an update, not a description of a game mechanic or design behaviour operating on the player. Even though troop requesting is a social resource-exchange feature, the review describes its absence due to a technical fault, not its deliberate design. Under R11, behaviours attributed to bugs or technical faults do not trigger dark-pattern labels.
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
The review is essentially two feature requests. The first asks for an in-app way to trade stickers, noting that not everyone uses Facebook — which implies that the game currently ties sticker trading to Facebook. Under the Friend Spam / Impersonation boundary rule, a required social login or connection for a feature describes permission sought or an access gate, not messaging performed, and codes NONE. The second asks that purchased boosters be usable when another player challenges them, implying a current restriction on booster use in challenge matches. Both passages are requests/suggestions for changes rather than descriptions of active dark-pattern mechanics, and R12 says requests for non-existent features do not trigger tags for the proposed mechanics. Nothing in the review describes an existing design behaviour that matches any of the 29 labels: 'addictive' and 'upgrades are okay' are general evaluations, and the two implied current limitations (Facebook-linked trading, booster use restriction) are not described as a spam mechanism, an invitation incentive, a social obligation, stranded value, or a progress gate.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (5)

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
The reviewer describes a belief that after they began purchasing Poké Balls, capture attempts started failing more often — Pokémon keep breaking out — which makes them consume balls faster and therefore forces them to buy more. This is an allegation that the game secretly manipulates catch outcomes in response to the player's spending, i.e., a hidden schedule governing the determination of outcomes (Illusion of Control's alleged-rigging rule). It also describes continued play (catching) as requiring repeated purchases of balls, i.e., payment needed to keep going (Pay to Progress). The second half of the review disclaims authorship and describes no mechanic. No term needs an external lookup: Poké Balls and capture attempts are self-explanatory in context.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "so I go through the balls faster so I have to purchase more"
  - why: The span states the player must purchase more balls to keep capturing, meaning continued play is contingent on spending, and the reviewer says this is deliberately engineered.
- `P_IllusionOfControl` - ok
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: The reviewer asserts the game's capture outcomes were secretly altered once they started paying, engineering failures to drive more purchases — a claimed manipulation of outcome determination, not an unlucky run.

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
The reviewer describes the casino game's reward structure after an update. The daily rewards have been changed so that completing them requires betting 50,000; the reviewer can only accumulate 40,000 from the game's timed rewards, so the daily reward target is unreachable through free play. The reviewer explicitly refuses to pay to obtain the daily rewards and deletes the game. The mechanics being described are: a daily reward track with a task threshold (bet 50,000) that resets daily and is forfeited if unmet; timed rewards that operate on the game's clock and cap how much free value can be earned; and payment implied as the only way to close the gap between the 40,000 ceiling and the 50,000 requirement.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "I'd not pay just to get my daily rewards"
  - why: Free play caps at 40,000 but the daily reward needs a 50,000 bet, and the reviewer's refusal to pay implies payment is the way to complete the daily rewards, i.e., progress contingent on spending.
- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The daily reward system requires completing a daily bet threshold, and failing to do so forfeits the rewards, which is a daily login incentive with an active consequence for not meeting the requirement.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "The most I can seem to get on the timed rewards is 40,000"
  - why: The timed rewards impose a game-clock cap on what the player can earn, forcing the player to keep returning on the game's schedule to accumulate value, and the cap is what blocks completing the daily rewards.

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
The reviewer describes Dice Dreams as a monetized collection game. Three distinct mechanics are being described. First, obtaining any meaningful win is priced in hundreds of dollars of real spending, which is payment gated progression. Second, the sticker album cannot be completed: the last one or two stickers are withheld unless the player pays, which is both a collection-completion drive and a manufactured scarcity tied directly to purchase. Third, the game only lets the player complete a goal about once in a hundred attempts, a claim that the game controls the win ratio rather than the player's skill deciding it.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: The last stickers are deliberately unobtainable through play ('never get') and payment is the only route to them, so the manufactured rarity is tied directly to purchase.
- `M_PayToProgress` - ok
  - span: "if you want to win anything on this game it will cost hundreds of dollars"
  - why: The reviewer states that any winning outcome in the game requires large real-money spending, so advancement is gated behind payment.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: The reviewer is describing a sticker set they are trying to finish, and the harm is that the final one or two items can never be obtained without paying.
- `P_IllusionOfControl` - **SPURIOUS**
  - span: "it may let you complete a goal maybe one out of hundred times"
  - why: The reviewer claims the game decides when a goal is completed at a fixed rate of about 1 in 100, asserting that outcomes are determined by the game rather than by the player.

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
The reviewer is describing end-game progression in Gardenscapes, a match-3 game. Three mechanics are being described. First, the lives system: the reviewer says they run out of lives several times a day, which in a match-3 game means being cut off from play until lives regenerate over real time. Second, progress has become contingent on payment: they say add-ons must be bought to get through levels and that the game is a time waste for non-payers, which contrasts the free route (slow, lives-limited) with the paid shortcut. Third, they mention wasting time and money, but the framing is retrospective and they are uninstalling, so the sunk investment is described as already forfeited rather than as something pulling them back into the game.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying"
  - why: Further progress through levels is stated to require buying add-ons, and the free route is described as an unreasonable time sink, making payment the condition for sane advancement.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "I run out of lives 3-4 times daily to beat every alternate level"
  - why: Running out of lives multiple times a day describes the lives regeneration gate that stops play until the timer refills, forcing the player to adhere to the game's schedule rather than their own.

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
The reviewer describes an album-collection system in Dice Dreams. They were two cards short of completing an album for a grand prize, so they bought a paid deal that promised new cards, but the deal delivered only duplicate cards. The album with a completion prize and a shortfall of the last cards is a collection-completion mechanic. The paid deal whose outcome (new vs. duplicate cards) is not guaranteed is a real-money stake in a chance-based reward delivery: the duplicates come from a randomised card pool. The reference to promoting the game through an external cash-reward app is out-of-game marketing and is not coded. 'Brain-rot' is an evaluation, not a mechanic. No currency conversion is described, so no Intermediate Currency. Nothing describes timers, schedules, or daily-login incentives.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "i bought a deal which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: The reviewer paid real money for a deal whose result was random: it promised new cards but the outcome (new vs. duplicate) was left to chance, so the stake is an explicit monetary purchase feeding a luck-based reward.
- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The reviewer is working toward completing an album set and frames the last two cards as the prize-gating goal, which is the compulsion to acquire all items in a collection.
- `P_RewardMania` - ok
  - span: "all i got were useless duplicates!"
  - why: The span describes an unpredictable reward delivery from a randomised card pool producing duplicate drops, which is the delivery schedule sustaining engagement; Gambling is assigned separately for the monetary stake under R9.

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
The review describes a wheel-spin bonus in Cash Frenzy. The reviewer's complaint is that after the wheel visually stops on a large prize, the genie character moves the wheel to a different (lower) segment, so the player ends up with a much smaller payout (100 million with a 5x multiplier falling to 48 million). This is described as a deliberate, recurring design behavior rather than a bug, and the request for 'a player choice to keep or spin' is a suggestion for a non-existent feature, which is not codable under R12. The active mechanic being described is the game overriding the result the player saw: the wheel appears to land on a great prize and is then moved, which is a claim that the game manipulates the determination of an outcome and deceives the player about what they actually won. No real-money stake, purchase, or wager is mentioned, so Gambling is not triggered; the span is an outcome-manipulation claim, which matches Illusion of Control.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "the genie move the wheel to a spin tag, and then the prices after the spin are way lower than the original price, from 100 million with 5x multiplier to a 48 million"
  - why: The reviewer asserts that the wheel visibly stops on a great prize and the game then moves it to a lower-prize segment, i.e., the game manipulates the outcome after it is revealed, deceiving the player about what they won.

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
The reviewer describes several distinct Monopoly GO experiences across one session. First, they complain that friend-invite rewards stopped after the season change: the sentence reveals the game's design of rewarding players for recruiting friends to join via Facebook, and the complaint is that the reward no longer pays out. Second, they report difficulty obtaining dice and a losing run of no Shut downs or bank heists at max bet: this is a bad-luck streak, not an assertion that the game rigs outcomes, so it does not carry Illusion of Control. Third, 'Stickers are duplicates all the way' describes the sticker pack reward system giving repeated duplicate drops from a randomised pool. Finally, the login/network error is a technical fault and is not a deliberate design pattern, so it is not codable.
```

**Labels assigned**

- `P_RewardMania` - ok
  - span: "Stickers are duplicates all the way"
  - why: The span describes the sticker-pack reward delivery as producing repeated duplicates from a randomised pool, which is the variable-reward delivery mechanic sustaining engagement.
- `S_ForcedFellowship` - ok
  - span: "Suddenly I get no rewards for inviting friends and getting them to join facebook"
  - why: The sentence reveals the game's recruitment mechanic — inviting friends to join via Facebook is rewarded — and the reviewer complains the reward stopped, which still describes the friend-invite incentive design (R7/R8).

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fdef27f2-9a21-4b8e-a04c-7a4753e0fb07` - 8 Ball Pool

> The game is great, but the user interface is completely rigged. Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins and are forced to buy real ones. ​We need a "Default Table Lock" or the game should always open the lowest bet table by default, not the highest! Fix this scammy feature. Giving 1 star

| | labels |
|---|---|
| gold | `M_Gambling`, `M_IntermediateCurrency`, `M_UIMisdirection` |
| pred | `M_IntermediateCurrency`, `M_UIMisdirection` |
| **missed** | `M_Gambling` |

**Did the model consider what it missed?**

- `M_Gambling` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes a UI behaviour in the game: whenever the app is opened or the 1v1 lobby is entered, the interface automatically scrolls to and pre-selects the highest-stakes bet table affordable with the player's coins. The reviewer reads this as a deliberate "Dark UX" trick meant to provoke accidental taps, causing the player to lose accumulated coins and then be pressured into buying more with real money. The complaint is built around the default selection with no opt-out (they ask for a "Default Table Lock" and for the game to open on the lowest table by default). The review also establishes that the in-game coins are purchasable with real money ("forced to buy real ones"), i.e., an intermediate currency. There is no claim about rigged match outcomes or random reward delivery, so Illusion of Control and Gambling are not supported; the mechanics described are the interface's default-selection misdirection and the real-money purchase of the currency.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: The span shows coins (in-game currency) being purchased with real money, establishing the real-money-to-currency conversion that defines Intermediate Currency.
- `M_UIMisdirection` - ok
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins and are forced to buy real ones"
  - why: The auto-scroll/auto-select is a default UI behaviour that steers the player into an unintended high-stakes action and causes accidental mis-clicks, which is exactly the interface directing attention/selection against the player's intent with no opt-out.

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
The reviewer describes the mid-game loop of a survival/strategy title: after the initial city-building phase, play becomes gathering resources while defending against raids, all to level up and unlock more attempts at a side-scrolling minigame. Three candidate mechanics appear. First, the phrase 'grinding resources' names a repetitive resource-gathering activity explicitly tied to progression ('so you can level up'), which matches Grinding. Second, the report that bigger alliances attack smaller ones and take their resources describes asymmetric player-versus-player harm in which the aggressor gains the defender's holdings, which matches Encourages Anti-Social Behavior under its boundary rule for stronger players rewarded for attacking weaker ones. Third, the closing line about having dedicated time and being disappointed reports investment and dissatisfaction, but it does not show the investment operating on a choice to stay or leave, so it is not Easy to Get, Hard to Lose. The garbled sentence about the advertisement is too vague to establish forced or incentivized ad viewing, and no payment or timers are mentioned, so no monetary or appointment labels apply. No term needs external resolution.
```

**Labels assigned**

- `S_EncouragesAntiSocialBehavior` - ok
  - span: "The bigger alliances all just attack the smaller alliances and take their resources."
  - why: The span shows stronger alliances attacking weaker ones and taking their resources, an asymmetric harmful act whose gain (plunder) flows to the aggressor.
- `T_Grinding` - ok
  - span: "It's just grinding resources trying not to get raided so you can level up"
  - why: The reviewer names 'grinding resources' as the repetitive activity required to advance ('so you can level up'), which is repetitive tasking tied directly to progress.

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
The reviewer is describing sticker collection in MONOPOLY GO!. They say they enjoy the game but are frustrated with the sticker system: they keep getting duplicate stickers, and completing sticker sets is not possible unless they pay. Three mechanics sit in this short account. First, the player is engaged in completing sticker sets, and the review's frustration is that the sets cannot be finished, which is the collection-completion compulsion operating on the player. Second, the completion of those sets is gated behind payment, which is progress contingent on spending. Third, the duplicate drops come from a randomised reward pool: receiving repeats instead of missing stickers describes the delivery mechanism of the reward system, not merely its value.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: Finishing the sticker sets, the player's goal, is stated to be impossible without payment, so progress is contingent on spending money.
- `P_CompleteTheCollection` - ok
  - span: "never lets you finish all the sets"
  - why: The player is working toward completing the sticker set collection and the review's complaint is that the game blocks that completion, showing the collection drive operating on the player.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: Receiving duplicate stickers instead of missing ones describes the randomised delivery mechanism of the reward system that sustains repeated play, not just the reward's size or value.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (10)

### `95ddadb3-82cd-4042-8a51-cf8b3ed164c2` - Mech Arena - Shooting Game

> You stuck waiting 30 seconds just to connect to a match. This game makes it seem like they give so many rewards but if all just for show. Its difficult to get weapon upgrades or any percs others you stick battling to win. This kind of games just rob you of your time in my opinion

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `T_Grinding` |
| **spurious** | `T_Grinding` |

**Model analysis**

```
The reviewer describes three distinct experiences. First, a 30-second wait to connect to a match, which is matchmaking/queue time rather than a designed game gate, and the codebook explicitly excludes queue and matchmaking waits from Playing by Appointment. Second, rewards that 'seem' generous but are 'just for show,' which is a complaint about the value of rewards, not about how rewards are delivered, so Reward Mania does not apply. Third, difficulty obtaining weapon upgrades or perks, which leaves the player 'stuck battling to win' — this names the repeated activity (battling) that the player must perform to make progress. The closing line is a general evaluation that the game wastes the player's time, which by itself is not a mechanic.
```

**Labels assigned**

- `T_Grinding` - **SPURIOUS**
  - span: "Its difficult to get weapon upgrades or any percs others you stick battling to win"
  - why: The span says upgrades/perks are hard to obtain and implies the player must keep battling repeatedly to earn them, describing the repetitive task cycle required to advance.

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
The review is a positive recommendation praising the game and, most concretely, its in-app purchase value. The only game mechanic actually described is monetization: the reviewer compares spending real money in other games (where $20 yields less than hoped) with Bingo Blitz, where the same purchase returns twice the quantity. That describes the transaction of real money being converted into an in-game quantity (packs of credits/items) at an exchange rate the reviewer approves of. Everything else — being fun, energizing, having modes and events — is generic praise with no specific mechanic, schedule, competition, or social design named. The 'modes and events' mention is too vague to code as Playing by Appointment or Competition. The only codable mechanic is the real-money-to-in-game-goods conversion.
```

**Labels assigned**

- `M_IntermediateCurrency` - **SPURIOUS**
  - span: "If your spend $20 on some item you get less then what your actually hoping for, but on here bingo gives you twice the number of your purchase"
  - why: The span describes spending $20 (real money) and receiving twice the number of the purchased in-game quantity, i.e., the exchange rate between real-world money and in-game currency/goods; the reviewer's approval does not suppress the mechanic (R7).

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
The reviewer is describing a base-builder war game after a few weeks of play. Three things stand out in what they describe. First, they call the game a 'grinder' — naming the repeated task-cycle required to get anywhere, a statement about how progress is produced rather than just an evaluation. Second, they describe events as unwinnable for a general (non-paying) player: winning is contingent on spending, and skill is explicitly said to play no part ('Zero skill pay to play. Zero skill pay to win.'). This is the pay-to-win/pay wall structure, with the 30k figure showing the scale of spending that wins an event. Third, 'win an event' implies competitive events in which players are pitted against each other and ranked by spending, though the review's focus is on the pay gate rather than the rivalry itself. The review is largely negative in tone, but R7 and R8 require coding the mechanics described regardless of approval.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "there is absolutely no opportunity for a general player to win an event. Zero skill pay to play. Zero skill pay to win."
  - why: The span states that winning events is impossible for a general player and that outcomes are determined by spending, not skill — payment grants the decisive advantage and gates event success.
- `S_Competition` - ok
  - span: "there is absolutely no opportunity for a general player to win an event"
  - why: 'Win an event' describes competitive events in which players are pitted against each other for placement, with spenders dominating the outcome; the competition mechanic is implied by the event-winner framing.
- `T_Grinding` - **SPURIOUS**
  - span: "Same old same old grinder."
  - why: 'Grinder' directly names the repetitive task cycle the game requires for progress, meeting the Grinding definition rather than being a mere quality complaint.

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
The reviewer describes the core loop of a base-building survival game. Three clear design behaviors are named: a pay-to-win economy, base upgrade timers that grow long (an arbitrary wait imposed by the game), and endless scaling that produces only more grind with no goal to aim at. The UI is described as deliberately confusing and overwhelming with the explicit purpose of pushing purchases, which is an interface designed against the player's intent. Finally, the alliance system punishes non-members: unallied players get attacked and bullied by others, which is player-versus-player predation rather than any described social obligation to keep playing.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "it's set up in a pay to win way"
  - why: The reviewer states outright that the game is arranged so that paying players gain an advantage.
- `M_UIMisdirection` - ok
  - span: "The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff"
  - why: The reviewer states the UI is designed to be confusing and overwhelming precisely to steer the player toward purchases.
- `S_Competition` - ok
  - span: "If you are not in one then you get attacked and bullied"
  - why: The alliance system pits players against each other: those outside an alliance are attacked by other players, a player-versus-player competition mechanic.
- `T_Grinding` - **SPURIOUS**
  - span: "just more grind"
  - why: The reviewer explicitly names the required activity as grinding, tied to the endless scaling of the game.
- `T_InfiniteTreadmill` - ok
  - span: "Everything scales endlessly, there is kinda no point to look forward to"
  - why: The span asserts the game expands endlessly with nothing to aim for, i.e., no attainable end state rather than a mere complaint about difficulty.
- `T_PlayingByAppointment` - ok
  - span: "the update times for your base are becoming ridiculous"
  - why: Base upgrade timers impose waits set by the game's clock, and since upgrades gate progression the appointment is required for progress.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `176aaa1f-d8f9-4a1a-9f29-64902f13be5c` - All in Hole: Black Hole Games

> I would give 5 stars, but I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used.🤨😒🙄😥

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `T_MandatoryMarathon` |
| pred | `M_IntermediateCurrency`, `P_EasyToGetHardToLose`, `T_MandatoryMarathon` |
| **spurious** | `P_EasyToGetHardToLose` |

**Model analysis**

```
The reviewer describes what happens between two play sessions: they stop playing ('leave the game') while holding accumulated value ('my bag full' and coins), and when they return that value is gone ('come back with it empty' and coins 'used'). The mechanics being described are, first, a forfeit-on-exit rule: stopping play costs the player everything they had gathered, so the session cannot be ended without losing accumulated progress. Second, that same forfeiture operates as a sunk-cost retention hook: the bag is easy to fill, but leaving is costly because the accumulated holdings are lost. Third, the phrase 'coins that I earned and purchased' states that the in-game coin currency is something the player can buy with real money, which establishes a real-money-to-virtual-currency conversion. No schedule, timer, reward calendar, ad, or gambling element is described, and the reviewer does not attribute the loss to a bug.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "coins that I earned and purchased"
  - why: The reviewer states the coins were purchased, showing real money converted into the in-game coin currency.
- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used"
  - why: The bag and coins are accumulated holdings that are easy to acquire but are forfeited when the player leaves, raising the cost of stopping.
- `T_MandatoryMarathon` - ok
  - span: "I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used"
  - why: Stopping the session and returning forfeits the accumulated bag contents and coins, so the player cannot exit at a moment of their choosing without losing progress.

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
The reviewer is describing a time-limited card collection event inside the game. Cards come from card packs; the player works toward completing themed sets, and completing a set grants a reward. The reviewer's account of their own play shows the event runs on the game's clock: the collection is 'about to expire', and finishing sets within that window is required to get the completion reward. Their concrete complaint is that the card-pack delivery stops yielding new cards precisely when a set is nearly complete, so after collecting 125 cards the set stays unfinished and the completion reward is lost at expiry. Three mechanics are present: a collection-completion system that exploits the drive to finish the set, a game-defined expiry that turns the collection into an obligation to complete by a deadline, and a random delivery system described as withholding the needed cards near completion.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "So after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion because they don't add new sets to the cards once the collection is about to end."
  - why: The player is working to complete card sets and the game is described as blocking completion of the set, exploiting the drive to finish the collection and claim its reward.
- `P_RewardMania` - **SPURIOUS**
  - span: "when one is almost close to completing a set, new cards don't appear again especially when the set is almost expiring"
  - why: The span describes the card-pack reward delivery withholding the needed new cards near completion, so continued draws yield no progress toward the specific missing items.
- `T_PlayingByAppointment` - ok
  - span: "you will miss the reward for the set completion because they don't add new sets to the cards once the collection is about to end"
  - why: The collection has a game-defined expiry and the span describes the reward being forfeited when the deadline arrives, imposing the game's schedule on the player.

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
The reviewer describes a storage bottleneck in a merge game at higher levels. Produced items accumulate: most of the 98 available board/refrigerator slots are occupied by generator parts that cannot yet be merged and by high-level finished items the player refuses to delete. The consequence is that there is not enough free space to continue playing, and the only relief described is spending real money for more capacity ("buy parts"). Three design mechanics are being described at once: payment as the way to remove a barrier that blocks continued play; a capped inventory that strands unusable holdings and leaves a realized shortfall of space, prompting the purchase; and the sunk value of the accumulated high-level items, which the player is unwilling to abandon, making exit costly.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Not enough slots to store and play without spending $$ to buy parts."
  - why: Continuing to store items and play is stated to be contingent on payment, so the storage cap acts as a barrier whose removal requires spending money.
- `M_WasteAversion` - ok
  - span: "98 spaces total, 72 are taken up by parts of generators or lower generators that I can't merge with higher generators yet or high level items like a corn that I am not going to delete"
  - why: The inventory cap is shown operating: most capacity is occupied by items that cannot be used or merged yet, leaving a realized shortfall of space and forcing the player to either spend money or sacrifice holdings.
- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "high level items like a corn that I am not going to delete"
  - why: The reviewer's refusal to discard the high-level items they have built shows accumulated investment making it hard to abandon those gains, which is what locks them into the storage problem.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `12267c1e-47ba-4984-97c8-768e820ceb1c` - Bingo Blitz™️ - Bingo Games

> not very user-friendly. no apparent reachable goals within a decent amount of time. I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| pred | `M_EasyToPurchase`, `M_IntermediateCurrency`, `M_PayToProgress`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| **spurious** | `M_IntermediateCurrency`, `M_PayToProgress` |

**Model analysis**

```
The reviewer describes a bingo collection game. They play repeatedly ('round after round') to collect photos for completing sets, which is repetitive play in service of a progress goal. After every lost round the game intercepts the session with a paid offer: spend coins to claim a missing photo so the set can be completed. The reviewer takes the offer, spends coins, and does not receive the promised photo, which they present as the game's recurring deceptive behaviour rather than a one-off fault. The closing statement that they have wasted so much money indicates the coins were funded with real money, making them an intermediate currency. Together this describes: grinding for collectibles, paying to advance the collection, a purchase prompt that interrupts gameplay, a collection-completion compulsion being exploited, a currency layer funded by real money, and an offer whose claim ('claim a photo... to complete the set') is deceitful because the item is not delivered.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set"
  - why: The purchase prompt fires after every lost round, interrupting the session and soliciting a spend at the point of frustration, reducing the friction before purchase.
- `M_IntermediateCurrency` - **SPURIOUS**
  - span: "spend extra coins to claim a photo I don't have to complete the set"
  - why: Coins are the in-game currency used as the means of payment, and the reviewer's closing 'I've wasted so much money' shows the coins were funded by real money, establishing the conversion.
- `M_PayToProgress` - **SPURIOUS**
  - span: "it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set"
  - why: Spending coins claims a missing photo and directly advances completion of the set, a paid shortcut to progress that the reviewer contrasts with unreachable goals in reasonable time.
- `P_AestheticManipulation` - ok
  - span: "I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED"
  - why: The offer promises a photo needed to complete the set, but the player does not receive it after paying; the recurring, unfulfilled promise is a deceitful claim used to extract coin spend.
- `P_CompleteTheCollection` - ok
  - span: "to claim a photo I don't have to complete the set"
  - why: The game exploits the player's drive to finish the photo set by offering the missing piece for coins, using the incomplete collection as the hook.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: Playing round after round to collect photos describes the repetitive, task-based grind required to advance the collection.

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
The review is a frustrated account of long-term play in Genshin Impact. The first complaint, that a 7-hour quest yields few primogems, is about reward size and value, not about the delivery mechanism, so it does not satisfy Reward Mania, and no real-money conversion is described, so Intermediate Currency does not apply. 'Exploration is debilitating' and the character-design criticism are evaluations with no mechanic named. The one mechanic the reviewer actually references is resin: in Genshin, resin is an energy resource that regenerates over time up to a hard cap and is consumed to claim rewards. The lament that 'there is no resin overflow system' only makes sense against that existing design — regeneration beyond the cap is wasted, so the player must log in and spend resin on the game's clock to avoid losing value. That is a time-based energy regeneration schedule imposing play on the game's schedule rather than the player's, i.e., Wait to Play / Playing by Appointment.
```

**Labels assigned**

- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "there is no resin overflow system"
  - why: The span implies the existing resin system regenerates over time to a fixed cap; without an overflow bank, the player must return on the game's schedule to spend resin before regeneration is forfeited, so the game's timer dictates when the player plays.

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
The review is about a Total Battle update that removed the open-silver PvP activity. The reviewer says two real things are happening now: meaningful growth requires spending money, and the removal of player-versus-player combat has made previously purchased growth pointless. A search was needed to pin down what 'open silver' refers to; it is the silver currency used in the game, and in context it names the open-world PvP looting activity that the update removed. Because the review explicitly says the PvP mode was taken away, the competition mechanic is no longer currently present and does not trigger S_Competition under R12. The paywall on growth is currently present, and the update's removal of PvP devalues money already spent on advancement, matching the devaluation-after-update test for Power Creep.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You have to spend to have any meaningful growth"
  - why: Meaningful growth in the game is stated to require spending money, so progress is contingent on payment.
- `M_PowerCreep` - **SPURIOUS**
  - span: "They just screwed everyone over who wasted money on this game"
  - why: The update removed PvP, making the progress players paid for worthless; previously purchased value is diminished through an update, per the boundary rule.

**Search:** `Total Battle game "open silver" what is it` -> Silver is the game's in-game currency used for upgrades; in context 'open silver' refers to the open-world PvP activity of looting silver from other players that the update removed.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `T_PlayingByAppointment` | 1 | 3 |
| `T_Grinding` | 1 | 3 |
| `M_Gambling` | 2 | 1 |
| `P_RewardMania` | 2 | 1 |
| `S_Competition` | 3 | 0 |
| `P_EasyToGetHardToLose` | 0 | 2 |
| `M_PayToProgress` | 0 | 2 |
| `S_Reciprocity` | 2 | 0 |
| `M_IntermediateCurrency` | 0 | 2 |
| `M_WasteAversion` | 1 | 0 |
| `P_IllusionOfControl` | 0 | 1 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `M_PowerCreep` | 0 | 1 |
| `P_AestheticManipulation` | 1 | 0 |
| `S_FriendSpamImpersonation` | 1 | 0 |

