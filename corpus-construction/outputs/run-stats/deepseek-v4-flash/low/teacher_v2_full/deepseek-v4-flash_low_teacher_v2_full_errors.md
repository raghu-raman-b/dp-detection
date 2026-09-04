# Error review - deepseek-v4-flash_low_teacher_v2_full

`deepseek-v4-flash` / reasoning `low` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `aad355174ac4`  
micro-F1 **0.800** (P 0.865 / R 0.744) - **23 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 6 | said NONE, gold had labels |
| SWAP | 4 | picked different labels than gold |
| MISSED ONLY | 9 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 4 | found all gold, added extras |

## The diagnostic that matters

Of **22** missed labels, **3** (14%) were named in the model's own analysis and dropped anyway; **19** (86%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `M_Gambling` | 0 | 2 |
| `S_Competition` | 0 | 2 |
| `P_RewardMania` | 0 | 2 |
| `S_Reciprocity` | 0 | 2 |
| `P_AestheticManipulation` | 0 | 1 |
| `M_UIMisdirection` | 0 | 1 |
| `M_EasyToPurchase` | 0 | 1 |
| `M_IntermediateCurrency` | 0 | 1 |
| `S_EncouragesAntiSocialBehavior` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `T_Grinding` | 1 | 0 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `M_RecurringFee` | 1 | 0 |
| `T_DailyRewards` | 1 | 0 |
| `T_MandatoryMarathon` | 0 | 1 |
| `M_WasteAversion` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |

## Missed everything (predicted NONE) (6)

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
The review is a feature-request list. Each numbered item asks the developer to add a capability (auctions, a widget, hidden statistics) or to change an existing behaviour (stop letting players remove an obstacle that has become a decoration). Under R12, requests, suggestions, and hypothetical additions do not trigger tags for the proposed mechanics. The passing reference to 'time is left for upgrades' implies build timers exist, but the review does not describe them as an imposed schedule or obstacle to the player; it merely asks for a widget to view them. No currently-present design behaviour is described as exploitative, and none of the proposed mechanics is asserted to already operate in the game.
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
The reviewer describes only technical malfunctions throughout: crashes when opening gifts or trading, lag preventing pokeball throws, PvP and rocket battles lagging, slow switching, unresponsive charge attacks, and a game freeze during opponent attacks. Every issue is attributed to bugs introduced by a new update and the reviewer asks only for fixes. There is no game rule, schedule, monetization, social, psychological, or download-size mechanic described that would satisfy a dark-pattern label.
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
The reviewer praises the game, then states that deleting the app would forfeit their purchases and progress, and asks the developers to add a save/cloud-progress feature so they would feel safe spending money. What is being described is a hypothetical about what would happen if they uninstalled, used to motivate a feature request. The actual loss is not occurring in the review; no in-game mechanic is described as currently operating on them. The request itself — add a way to save all progress and purchases — is a proposed, non-existent feature, which per R12 cannot trigger any label for that proposed mechanic. The stated reluctance to uninstall because of sunk purchases and effort is a worry and an appeal, not a demonstration of an active design forcing continued play or spending within the game as it is.
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
The reviewer reports that a specific feature, requesting troops from their clan, has stopped working after an update and asks for it to be fixed. The loss of the function is attributed to a technical fault introduced by an update, not to a deliberate design rule. Under R11, behavior attributed to a bug or technical fault should not be coded as a dark pattern. Even though troop requesting is a social resource mechanism, the review frames its absence as a malfunction, and there is no description of a game rule penalizing the player or manipulating them.
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
The review is almost entirely a set of suggestions and a grievance about how purchased items behave. The first request, an in-app way to trade stickers because not everyone is on Facebook, proposes a feature that does not exist in-app; R12 excludes suggestions from coding, and the Facebook reference describes only where trading currently happens, not any active recruitment, spam, or obligation. The booster remark reports that a purchased booster cannot be used when another player issues a challenge; this describes a restriction on using a purchased item, but it does not establish that the purchase is required for progress, that money must be wagered, or that any value is stranded in the currency sense. No review span describes a design behaviour matching any meso label; the complaints and requests concern feature availability rather than a currently operating dark pattern.
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
The reviewer's main complaint is that the game's external advertisements misrepresent the actual gameplay, showing physics puzzles when the real game is a strategy game. Under R13, out-of-game store advertising and marketing material is outside the unit, so the misleading-ads claim is not codeable. The rest of the review describes the game neutrally as an 'extremely involved strategy game' with army training, building, and resource gathering, and tells puzzle-expecting players they will be 'doing chores in order to get to them.' That phrase is vague and conditional, naming no specific repetitive activity and describing no design that forces repetition for progress; it functions as a cautionary characterization rather than an account of a grinding mechanic. No dark pattern is clearly instantiated.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (4)

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
The reviewer reports several distinct frustrations in MONOPOLY GO!. First, that the game stopped rewarding them for inviting friends to join through Facebook, which names the game's friend-invitation incentive even as the reviewer complains it is no longer paying out. Second, a shortage of dice, and an unlucky stretch at maximum bet with no shutdowns or bank heists, which reads as a losing run rather than a mechanistic claim about rigging. Third, sticker packs delivering duplicates, which describes a randomized reward delivery that prevents completing the sticker collection. Finally, a login/connection failure, which the reviewer attributes to a technical fault and is therefore not coded as a dark pattern.
```

**Labels assigned**

- `P_CompleteTheCollection` - **SPURIOUS**
  - span: "Stickers are duplicates all the way"
  - why: The reviewer is working toward a sticker set and frames the repeated duplicates as blocking collection, which capitalizes on the drive to complete collections.
- `P_RewardMania` - ok
  - span: "Stickers are duplicates all the way"
  - why: Duplicate sticker drops from a randomized pack pool describe unpredictable reward delivery that withholds the wanted item across repeated attempts.
- `S_ForcedFellowship` - ok
  - span: "I get no rewards for inviting friends and getting them to join facebook"
  - why: The game incentivizes the player to invite friends to join through Facebook in exchange for rewards; the reviewer's complaint that the reward stopped confirms the invitation-recruitment mechanic exists.

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
The reviewer describes a UI behaviour in the 1v1 betting lobby: every time the player opens the game or the 1v1 section, the interface automatically scrolls to and pre-selects the highest-stakes table the player can afford. The stated purpose is to induce accidental mis-clicks, drain the player's coins, and force them to buy more with real money. The core mechanic is an interface that defaults the player onto a harmful option with no opt-out, framed explicitly as a 'Dark UX' trick. The coins themselves are the player's in-game holdings, and losing them is described as forcing a real-money purchase of coins to keep going. I will not code Mandatory Marathon because the review describes the pre-selection causing the loss, not an inability to exit a session.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "so players lose all their hard-earned coins and are forced to buy real ones"
  - why: The span shows the in-game coins being lost and then replenished by buying them with real money, establishing coins as a purchased intermediate currency.
- `M_PayToProgress` - **SPURIOUS**
  - span: "so players lose all their hard-earned coins and are forced to buy real ones"
  - why: Being drained of all coins through the trick leaves the player unable to keep playing and 'forced to buy' coins, making continued play contingent on payment.
- `M_UIMisdirection` - ok
  - span: "Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins"
  - why: The interface pre-selects and auto-scrolls to the highest bet as a default, an opt-in arrangement the player must actively fight to avoid, which is an interface element directing the player toward a damaging selection.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `176aaa1f-d8f9-4a1a-9f29-64902f13be5c` - All in Hole: Black Hole Games

> I would give 5 stars, but I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used.🤨😒🙄😥

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `T_MandatoryMarathon` |
| pred | `P_EasyToGetHardToLose` |
| **missed** | `M_IntermediateCurrency`, `T_MandatoryMarathon` |
| **spurious** | `P_EasyToGetHardToLose` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**
- `T_MandatoryMarathon` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes arriving at the game with a full bag and coins earned and purchased, only to return after being away and find the bag empty and the coins consumed. The mechanic implied is an offline or absence-based loss system: holdings accumulated during play are vulnerable to being taken or spent during the time the player is not in the game. This makes disengagement the moment of loss and raises the cost of leaving the game for any length of time. The underlying design appears to be one where the player must return in order to protect what they hold.
```

**Labels assigned**

- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "I leave the game with my bag full only to come back with it empty and coins that I earned and purchased used"
  - why: The span implies that accumulated coins and bag contents are held as value that is forfeited when the player is away, so the cost of not playing is measured in holdings already gained, which is the endorse-value mechanism.

**Search:** `"All in Hole" mobile game what happens to coins when offline` -> Coins in All in Hole are used for continuing play and do not accumulate passively; they are gained in gameplay. Search did not fully clarify the specific offline-loss mechanic, so the analysis relies on the reviewer's own description.

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
The reviewer is describing a collection mechanic: completing an album for a grand prize, needing the last two cards. To finish, they bought a paid deal that was represented as guaranteeing NEW (previously unowned) cards, but the deal delivered duplicates instead. That failure is what they call a scam. Reading through it, the purchase is a stake paid into a reward delivery whose outcome is random: the deal could produce cards the player already owns rather than the missing ones. So the paid deal is a chance mechanic (Gambling), the delivery of cards from a randomized pool producing duplicates is Reward Mania, and the whole effort is framed around completing a set (Complete the Collection). The purchase does not unlock content outside the wager; it is itself a wager on a random draw, so Pay to Progress does not attach under the Gambling boundary rule.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: Real money was spent on a deal whose outcome is chance-based: it could return duplicate cards already owned rather than the promised missing ones, so the wager decided the reward.
- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The player is pursuing completion of an album set for its grand prize, and the missing cards are what drive the purchase attempt.
- `P_RewardMania` - ok
  - span: "so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: The reward is delivered from a random pool and produced repeated duplicate drops, requiring further attempts to obtain the specific missing cards.

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
The reviewer describes a wheel-spin feature (the 'genie game') inside this casino-slot game. The wheel visibly stops on a large prize, but then a genie animation moves the wheel onward to a 'spin' tag, and the final payout is much lower than what the wheel appeared to land on (100 million with a 5x multiplier drops to 48 million). The core complaint is that the shown outcome is overridden by an animation the player cannot control, so the displayed result is not the real result. This is a claim that the game conceals or manipulates how an outcome is determined rather than a matter of ordinary unlucky spins. The request that the player be given a choice to keep or spin is a suggestion for an absent feature and codes nothing. No real-money wager is described, so Gambling does not apply.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "whe the wheel spin after stopping on a great price the genie move the wheel to a spin tag, and then the prices after the spin are way lower than the original price, from 100 million with 5x multiplier to a 48 million"
  - why: The wheel visibly stops on a high prize only for the genie to move it to a lower one; the reviewer asserts the game manipulates the outcome after the fact, hiding the true result from the player.

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
The review has three distinct threads. First, a customer-service complaint: 9 diamonds were spent but a game element did not appear within the original 5 moves plus 5 purchased additional moves, and support would not refund. This describes a lost purchase and a support refusal; it does not clearly describe a designed dark pattern behind it, so I will not assign from it. Second, a monetization remark: 'you don't have to pay to win' explicitly negates pay-to-win, and 'don't buy from this game beyond the pass' names a pass as the only purchase the reviewer still tolerates but does not describe what the pass does or how it operates, so no Recurring Fee mechanic is carried by the span. Third, a social feature: 'Get friends and a team and trade lives' describes exchanging lives with people already in the player's friend and team circle, which is a resource-transfer mechanism between current players.
```

**Labels assigned**

- `S_Reciprocity` - ok
  - span: "Get friends and a team and trade lives."
  - why: Trading lives with friends and team members already playing is an in-game resource-exchange mechanic between existing players, not recruitment of new players, so it codes Reciprocity.

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
The reviewer is describing what happens inside the game when an advertisement plays. They report that after seeing an ad there is no way to close it: no close (cross) control is provided, tapping anywhere on the screen navigates to an app store, and pressing back leaves the ad stuck on screen so the only exit is killing the game process. This is an in-game ad-viewing experience that the player cannot dismiss, i.e., the player is compelled to watch or endure the ad and cannot end the session at a moment of their choosing through ordinary means. The review attributes this to the ad's design (missing close control), not to a crash or technical fault.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "there is no way to close it. No cross mark on the screen , if you try to click anywhere on the screen it takes you to store. If you go back to game it is still stuck in the last sceeen of the ad. You have to kill the game to come out of the ad screen"
  - why: The ad shown in the game cannot be dismissed through any in-ad control, back navigation leaves it stuck, and only killing the game exits it, so the player is compelled to view the advertisement.

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
The review has two distinct parts. The first describes purchasing Poké Balls and then finding that Pokémon 'keep breaking out' of them, so the player consumes balls faster and must buy more, ending with 'I feel taken advantage of.' This is an accusation that the game manipulates catch outcomes (higher break-out rates after spending) to drive continued purchases. The second part, added as an edit, denies authorship entirely: 'I DID NOT WRITE THIS REVIEW... I DO NOT KNOW ANYONE' - a claim that a review appeared under the player's account that they did not author, which is the impersonation pattern of a review written under the player's identity.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: The reviewer asserts that captures began failing more often once they started purchasing, a manipulation of the outcome determination engineered to consume purchased balls and drive further spending.
- `S_FriendSpamImpersonation` - ok
  - span: "editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE"
  - why: The player states a review is attributed to them that they did not write and could not have written, i.e., content published under the player's identity without their authorship.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `3c46f5e0-6091-43dc-94a0-e3af3259a63d` - Cashman Casino Slots Games

> Resently cashman had changed it's bingo rewards and daily rewards. However lve found that I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards. The most I can seem to get on the timed rewards is 40,000. I'd not pay just to get my daily rewards. So I'm deleting them.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_WasteAversion`, `T_DailyRewards` |
| pred | `M_PayToProgress` |
| **missed** | `M_WasteAversion`, `T_DailyRewards` |

**Did the model consider what it missed?**

- `M_WasteAversion` - never mentioned -> **attention / recall**
- `T_DailyRewards` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes a change to the game's bingo and daily rewards. The core complaint is that the daily reward is now only obtainable by wagering 50,000 in the casino, while the free route ('timed rewards') tops out at 40,000. The reviewer states they will not pay just to obtain the daily reward and will delete the game. Reading the implied design: the daily-reward goal sets a wager threshold above what free play can deliver, leaving payment (buying more coins to bet with) as the only way to close the gap. The reviewer does not describe missing a day or a login-calendar penalty, so the daily-return/streak mechanic of Daily Rewards is not what is being described; the mechanic at issue is a reward goal that cannot be met without spending money.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards. The most I can seem to get on the timed rewards is 40,000. I'd not pay just to get my daily rewards."
  - why: The daily-reward goal requires a 50,000 wager that the free timed-reward path (40,000) cannot reach, and the reviewer explicitly frames payment as the only way to get it ('I'd not pay just to get my daily rewards'), showing the reward is effectively contingent on spending money.

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
The reviewer describes a pay-walled progression experience in Dice Dreams, a dice-and-sticker-collection game. Two intertwined problems are named. First, winning or getting anywhere requires spending a lot of real money ('hundreds of dollars'), which is payment gating advancement. Second, the sticker album system never hands out its final one or two pieces unless the player pays to obtain them, which is simultaneously a collection-completion compulsion and a manufactured scarcity of the rare remaining pieces tied directly to purchase. The closing line about completing a goal 'one out of hundred times' is a frustration about rare success, but it does not describe any concealed mechanism or delivery-schedule mechanic clearly enough to tag on its own.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "you will never get the last one or two unless you pay a lot of money to get them"
  - why: The scarce final stickers are made unobtainable through play and offered back through paid purchase, which is manufactured scarcity tied directly to price.
- `M_PayToProgress` - ok
  - span: "if you want to win anything on this game it will cost hundreds of dollars"
  - why: The span states plainly that winning in the game is contingent on spending large sums of real money.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two"
  - why: The reviewer describes being unable to finish the sticker set because its final pieces are withheld, the core frustration of an incomplete collection.

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
The reviewer is playing Bingo Blitz and is trying to complete photo collections. Their account describes three distinct things: repeatedly playing round after round to collect photos, which is a repetitive activity pursued to gather collection items; the goal of assembling complete sets of photos, which is a collection-completion loop; and an in-game offer presented after each lost round that promises, for a coin payment, a photo the player does not yet have to finish the set, but which the reviewer says never actually delivers that promised photo. The final complaint is that this deceptive offer has caused them to waste money repeatedly.
```

**Labels assigned**

- `P_AestheticManipulation` - ok
  - span: "I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED"
  - why: The offer's wording promises a specific photo in exchange for coins but the player does not receive it; the deception lies in what the offer claims versus what is delivered.
- `P_CompleteTheCollection` - ok
  - span: "to claim a photo I don't have to complete the set"
  - why: The player is collecting photos to assemble complete sets, and the missing item needed to finish a set is what the offer is aimed at, a collection-completion compulsion.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The reviewer describes performing the same play activity repeatedly ('round after round') in order to acquire collection items, which is the repetitive-task pattern.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `84bbc363-d55a-4cf1-a557-c61ed7ab82bc` - Last War:Survival Game

> Once you get past building the city block stage, it gets kinda boring. It's just grinding resources trying not to get raided so you can level up to have a few more attempts at the left right scroller game. The advertisement that's really becomes not that great. The bigger alliances all just attack the smaller alliances and take their resources. I dedicated some time to this game and to my alliances and am disappointed with current status.

| | labels |
|---|---|
| gold | `S_Competition`, `S_EncouragesAntiSocialBehavior`, `T_Grinding` |
| pred | `S_Competition`, `T_Grinding` |
| **missed** | `S_EncouragesAntiSocialBehavior` |

**Did the model consider what it missed?**

- `S_EncouragesAntiSocialBehavior` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer is describing the mid-game state of a survival/base-building PvP game. Three things stand out. First, the core progression loop is named directly as grinding resources to avoid raids while levelling up — a repetitive task performed to advance. Second, the PvP layer is described as stronger alliances preying on weaker ones and seizing their resources; this is players set against each other in the game's sanctioned raiding/competition system. Third, the reviewer notes having dedicated time to the game and its alliances and expresses disappointment, which reads as sunk-investment regret rather than a demonstrated pull keeping them playing, so it does not meet the Easy-to-Get-Hard-to-Lose threshold. The garbled sentence about an advertisement does not clearly describe forced ad views or rewarded ads, so it does not support Advertisement.
```

**Labels assigned**

- `S_Competition` - ok
  - span: "The bigger alliances all just attack the smaller alliances and take their resources"
  - why: Alliances raiding one another for resources is ordinary competitive PvP design where players are set against each other; the reviewer reports the sanctioned raiding mechanic rather than an incentive to dishonest or bullying conduct beyond sanctioned play.
- `T_Grinding` - ok
  - span: "It's just grinding resources trying not to get raided so you can level up"
  - why: The reviewer names the repetitive activity ('grinding resources') performed to make progress (level up), which is the canonical Grinding pattern.

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
The reviewer is describing Monopoly GO's sticker album collection system. Stickers come from reward packs and fill themed album sets; the reviewer reports three intertwined frustrations: draws keep producing duplicates rather than needed cards, the full sets therefore cannot be completed, and completing them is stated to be impossible without paying. The collection drive (finishing the sets), the randomised reward delivery (duplicates), and the payment wall on completion are each being described.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: Completing the collection is stated to be contingent on payment, with the free path unable to reach completion.
- `P_CompleteTheCollection` - ok
  - span: "never lets you finish all the sets"
  - why: Finishing the full sticker albums is the goal the review treats as blocked, describing the urge to complete the set.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: Duplicate drops describe a variable reward delivery system in which repeated attempts keep yielding unwanted items, sustaining engagement rather than completing value.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (4)

### `ab2097d3-2f9b-4a87-885c-25dfcddb5a70` - Gardenscapes

> Have been playing this game since COVID 19 lockdown. It was fun back then. Currently at 8416 and it gets frustratingly annoying after level 8000. I run out of lives 3-4 times daily to beat every alternate level, avg 5-7 days per level. You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying. Now I'm not interested anymore. Unistalling this game to invest some quality time in a real life. Wasted too much of money and time into this game.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `T_Grinding` |
| pred | `M_PayToProgress`, `T_Grinding`, `T_PlayingByAppointment` |
| **spurious** | `T_PlayingByAppointment` |

**Model analysis**

```
The reviewer is describing the end-game difficulty wall of a match-3 game. Several mechanics are being described together. First, lives are a consumable resource that is exhausted multiple times a day, which forces the player to stop and wait before more attempts are possible. Second, progressing through each level takes days of repeated attempts (5-7 days per level, beating every alternate level), which is a grind of replaying the same stages. Third, the alternative to that slow repeated play is spending money on add-ons, framed as the only way to get through sanely. The reviewer's closing statement that they wasted too much money and time expresses regret and an intent to quit, not a retention mechanism, so it does not trigger Easy-to-Get/Hard-to-Lose. No term in the review is obscure enough to require a web search.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying."
  - why: The span states outright that buying add-ons is required to get through, and that without paying the game is a time waste, tying payment to the ability to make progress.
- `T_Grinding` - ok
  - span: "I run out of lives 3-4 times daily to beat every alternate level, avg 5-7 days per level"
  - why: Spending 5-7 days and exhausting lives 3-4 times per day to clear a single level describes repeated attempts at the same stage as the required path forward.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "I run out of lives 3-4 times daily to beat every alternate level"
  - why: Running out of lives multiple times daily describes a consumable resource whose exhaustion forces the player to wait for regeneration before they can continue, gating play on the game's clock.

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
The reviewer describes an inventory-capacity wall. At level 34 they run out of board and refrigerator slots. Many of the occupied slots hold generator parts, lower-level generators awaiting merge, or high-level items (corn, lambchop, chicken pie) they refuse to discard. Their only stated way to keep playing without deleting invested items is spending real money on more storage slots. Three mechanics show up: (a) progress is gated behind buying capacity, i.e., paying to progress; (b) the capped board forces the player to either sacrifice invested items or buy space, i.e., waste from inventory limits; (c) accumulated high-level items and partially merged generators make leaving costly because that investment would be abandoned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Not enough slots to store and play without spending $$ to buy parts"
  - why: The span ties continuing to play to purchasing storage slots; without buying the slots the player is blocked from effective play.
- `M_WasteAversion` - ok
  - span: "72 are taken up by parts of generators or lower generators that I can't merge with higher generators yet or high level items like a corn that I am not going to delete. A lambchop can take up to 9 spaces or more of my 26 spaces"
  - why: The capped inventory holds invested items that cannot currently be used, forcing a choice between deleting them and paying to expand capacity.
- `P_EasyToGetHardToLose` - **SPURIOUS**  _[span not verbatim]_
  - span: "I'm not deleting the chicken pie... A lambchop can take up to 9 spaces or more of my 26 spaces"
  - why: The player refuses to delete high-level items and half-built generators, so accumulated in-game assets raise the cost of continuing to need more space or of leaving.

**Search:** `Merge Cooking game buy board slots parts storage` -> The game lets players expand board/inventory slots using gems and resources, and inventory management is a normal part of progressing, confirming capacity expansion is a core game design element.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `ae3b6309-101e-4320-99b1-aa6795602787` - Genshin Impact

> The rewarding system is just DIABOLICAL, I just finished a 7 hour quest and I barely got any primogems. exploration is debilitating. the character design is as almost lame... especially for the female characters, they all have the same bare legs curse that makes the design uninteresting. it's just a horrible game, this game used to be fine by the ways. for context I've been playing since 2021, 5 years have passed can you imagine ? and there is no resin overflow system. 😭

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `M_IntermediateCurrency`, `T_Grinding`, `T_PlayingByAppointment` |
| **spurious** | `M_IntermediateCurrency`, `T_Grinding`, `T_PlayingByAppointment` |

**Model analysis**

```
The reviewer describes several problems with the game. 'The rewarding system is just DIABOLICAL, I just finished a 7 hour quest and I barely got any primogems' describes completing a long quest yet earning insufficient in-game currency, meaning the reward does not match the time invested, and the reward is the premium currency. 'no resin overflow system' describes an absent mechanic where the energy resource's regeneration cap is reached, and the player cannot accumulate a reserve beyond the cap, so the resource is wasted if the cap fills, which implicitly punishes not playing within the game's schedule. The reviewer has played for 5 years, which describes long tenure, not a treadmill. The quote about 5 years passing and not having overflow is about the resource cap, not about content extending beyond completion.
```

**Labels assigned**

- `M_IntermediateCurrency` - **SPURIOUS**
  - span: "I just finished a 7 hour quest and I barely got any primogems"
  - why: Primogems is the game's premium currency; the reviewer states the quest yielded very few of them, implying a real-money conversion exists in-game.
- `T_Grinding` - **SPURIOUS**
  - span: "7 hour quest"
  - why: A 7-hour quest is described as long and yielding little, framed as a tedious task required to progress.
- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "there is no resin overflow system"
  - why: The absence of an overflow system means resin regeneration stops at the cap, forcing the player to log in on the game's schedule to use resin before it is wasted.

**Search:** `Genshin Impact resin overflow system meaning` -> Resin is the game's energy resource that regenerates over time to a cap of 200; without an overflow system, resin beyond the cap is not accumulated and is wasted.

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
The review's core complaint is that a recent update removed a player-versus-player element called 'open silver' (a PvP mode for raiding silver), leaving the game as farming only. Within that account, the reviewer states that meaningful growth (game progression) is contingent on spending money, and then describes that paid growth as retroactively pointless because the update stripped out the PvP that gave it purpose. The removal of a feature is itself a design change rather than a dark pattern, but the spent-money-for-progress made worthless by the update shows value of purchases declining after acquisition is the Power Creep pattern.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You have to spend to have any meaningful growth"
  - why: The span states that further meaningful progress is contingent on making a payment, meeting the Pay Wall indicator.
- `M_PowerCreep` - **SPURIOUS**
  - span: "You have to spend to have any meaningful growth and then they go and make it all pointless by getting rid of any player vs player"
  - why: Spending yields in-game growth, then an update removes the PvP that gave it meaning, so the value of what was purchased is lost after acquisition, satisfying Power Creep.

**Search:** `Total Battle War Strategy "open silver" what is it` -> Silver is the primary in-game currency for upgrades; 'open silver' from community context refers to a PvP mode/event allowing raids on other players' silver, confirmation that its removal is tied to the disappearance of player-versus-player gameplay.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_Gambling` | 2 | 1 |
| `P_EasyToGetHardToLose` | 1 | 2 |
| `T_PlayingByAppointment` | 1 | 2 |
| `M_IntermediateCurrency` | 1 | 1 |
| `T_Grinding` | 1 | 1 |
| `S_Competition` | 2 | 0 |
| `P_RewardMania` | 2 | 0 |
| `S_Reciprocity` | 2 | 0 |
| `P_AestheticManipulation` | 1 | 0 |
| `M_UIMisdirection` | 1 | 0 |
| `M_EasyToPurchase` | 1 | 0 |
| `S_EncouragesAntiSocialBehavior` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `P_CompleteTheCollection` | 0 | 1 |
| `M_PowerCreep` | 0 | 1 |
| `M_RecurringFee` | 1 | 0 |
| `M_PayToProgress` | 0 | 1 |
| `T_DailyRewards` | 1 | 0 |
| `T_MandatoryMarathon` | 1 | 0 |
| `M_WasteAversion` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |

