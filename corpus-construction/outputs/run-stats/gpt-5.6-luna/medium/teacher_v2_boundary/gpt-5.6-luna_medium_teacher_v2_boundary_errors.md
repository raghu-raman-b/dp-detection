# Error review - gpt-5.6-luna_medium_teacher_v2_boundary

`gpt-5.6-luna` / reasoning `medium` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_boundary.txt` sha `013bb31c5857`  
micro-F1 **0.821** (P 0.954 / R 0.721) - **19 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 5 | said NONE, gold had labels |
| SWAP | 2 | picked different labels than gold |
| MISSED ONLY | 11 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 1 | found all gold, added extras |

## The diagnostic that matters

Of **24** missed labels, **6** (25%) were named in the model's own analysis and dropped anyway; **18** (75%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `M_PayToProgress` | 0 | 3 |
| `S_Reciprocity` | 0 | 2 |
| `S_Competition` | 1 | 1 |
| `P_AestheticManipulation` | 0 | 2 |
| `M_IntermediateCurrency` | 0 | 2 |
| `M_PowerCreep` | 1 | 0 |
| `S_FriendSpamImpersonation` | 0 | 1 |
| `M_RecurringFee` | 1 | 0 |
| `P_RewardMania` | 0 | 1 |
| `T_Advertisement` | 1 | 0 |
| `M_Gambling` | 0 | 1 |
| `T_MandatoryMarathon` | 0 | 1 |
| `M_EasyToPurchase` | 0 | 1 |
| `T_Grinding` | 1 | 0 |
| `M_WasteAversion` | 0 | 1 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `T_PlayingByAppointment` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |

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
The review is primarily a list of requested features rather than descriptions of current game mechanics. It asks for auctions using in-game currency, preventing removal of converted decorations, an account-switching upgrade-timer widget, and access to advanced troop statistics. Because these are proposed additions or changes, they do not trigger labels under R12. The phrase about removing an obstacle after turning it into a decoration describes a requested restriction, not a dark-pattern mechanic currently operating in the game.
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
The reviewer describes an inability to request troops from their clan, but explicitly attributes it to an update-related problem and asks for it to be fixed. This is a reported technical malfunction rather than a deliberate social resource-sharing mechanic, so no label applies under R11.
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
The reviewer describes existing upgrades, stickers, player challenges, and purchased boosters, but the two potentially relevant mechanics are requests rather than current game behavior: they want sticker trading within the app because not everyone uses Facebook, and they want a purchased booster to remain usable when another player challenges them. These proposed features cannot be coded under R12. The statement that a booster was purchased does not describe a progress gate, advantage mechanism, currency conversion, or other qualifying dark pattern. The review therefore supports no labels.
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
The reviewer reports that after leaving the game, their full bag is empty on return and coins they had earned or purchased have been consumed. This describes a loss of inventory and currency, but the text does not identify a deliberate game rule such as an inventory-capacity penalty, a purchase mechanism, a progression gate, or pressure to keep playing. It may imply a malfunction or unintended state change, but no dark-pattern mechanic is explicitly described, so no label applies.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `8d13a3c1-1982-45db-a2b4-07c61c41ba2a` - Pixel Flow!

> this WAS a favorite game and WAS fun until it became unplayable. stuck on level 195 for almost 2 months. getting ready to uninstall it. I refuse to pay for power ups. should be daily login rewards to help with these harder levels.

| | labels |
|---|---|
| gold | `M_PayToProgress` |
| pred | _NONE_ |
| **missed** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_PayToProgress` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes being unable to advance past level 195 for almost two months and refusing to buy power-ups. This reports stalled progress and a declined possible purchase, but does not explicitly describe repetitive tasks, a payment requirement, or a paywall. The request for daily login rewards is hypothetical and therefore does not establish an existing Daily Rewards mechanic.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (2)

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
The review describes Poké Balls being consumed more quickly because Pokémon repeatedly break out during capture attempts, leaving the player needing to buy more to continue catching Pokémon. This supports Pay to Progress because payment is presented as necessary to overcome depletion of a gameplay resource and continue the core activity. The reviewer also alleges that capture outcomes worsen after purchases, implying that the game manipulates or tunes outcome determination rather than merely producing an unlucky streak, which supports Illusion of Control. The later claim that the reviewer did not write the review describes possible account misuse, not an in-game messaging or posting mechanic, so Friend Spam / Impersonation is not assigned.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "so I go through the balls faster so I have to purchase more"
  - why: The rapid depletion of Poké Balls makes purchasing more necessary to continue making captures, a core progression activity.
- `P_IllusionOfControl` - ok
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out"
  - why: The reviewer implies that capture success is deliberately worsened after purchasing, alleging hidden manipulation of the capture outcomes.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `12267c1e-47ba-4984-97c8-768e820ceb1c` - Bingo Blitz™️ - Bingo Games

> not very user-friendly. no apparent reachable goals within a decent amount of time. I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| pred | `M_PayToProgress`, `P_CompleteTheCollection`, `T_Grinding` |
| **missed** | `M_EasyToPurchase`, `P_AestheticManipulation` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - never mentioned -> **attention / recall**
- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a collection goal involving photos and repeatedly playing bingo rounds to obtain them. The repeated rounds are a grinding activity tied to progress, and the photo set is an explicitly described collection objective. After losing a round, the game presents an offer to spend extra coins for a missing photo, which is a paid shortcut toward completing the set; however, the review does not explicitly establish that the coins were purchased with real money, so Intermediate Currency is not assigned. The reviewer says the promised photo is not delivered, but does not attribute this to a bug or technical fault, so the described purchase/progression mechanic remains codable. No chance-based reward delivery is clearly described for the photo offer itself.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "spend extra coins to claim a photo I don't have to complete the set"
  - why: The game offers spending coins to bypass the ordinary effort needed to acquire a missing photo and complete the set.
- `P_CompleteTheCollection` - ok
  - span: "collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set"
  - why: The reviewer is pursuing missing photos specifically to complete an in-game set.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The reviewer repeatedly plays bingo rounds as the activity needed to obtain photos.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (11)

### `b580a4c7-3c75-493e-ad3b-03b4f2bde6a5` - Pokémon GO

> This new update have many bugs. 1)I can't open any gifts or trade with friends without the keep on crashing, 2) when click on a pokemon I can't even throw the pokeball with all the lagging, 3) the pvp & rockets battles are also lagging switching out are too slow, charge attacks are not responding well and my game freeze while the opponent keep attacking. Please fix these problems!

| | labels |
|---|---|
| gold | `S_Competition`, `S_Reciprocity` |
| pred | `S_Competition` |
| **missed** | `S_Reciprocity` |

**Did the model consider what it missed?**

- `S_Reciprocity` - never mentioned -> **attention / recall**

**Model analysis**

```
The review primarily attributes the inability to open gifts, trade, catch Pokémon, and conduct battles to technical faults: crashing, lag, unresponsive controls, and freezing. These malfunction descriptions do not trigger dark-pattern labels under R11. It also explicitly describes PvP battles in which an opponent attacks, which is an in-game competitive mechanic independent of the reported lag, so Competition applies. Gifts and trading with friends are mentioned, but no obligation to reciprocate is described.
```

**Labels assigned**

- `S_Competition` - ok
  - span: "the opponent keep attacking"
  - why: The span explicitly describes a competitive battle involving the reviewer and an opponent.

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
The review describes a pass as an in-game purchase, but does not explain its duration, renewal, or any pressure to play enough to justify it, so the pass reference alone does not establish Recurring Fee. The statement that a game element failed to appear within the move limits is attributed to a game-element failure and customer-service compensation issue, not a deliberate dark-pattern mechanic. The reviewer explicitly says payment is not required to win, which does not support Pay to Progress. The review does explicitly describe exchanging lives with existing friends or teammates, which is a resource-transfer mechanism creating reciprocity.
```

**Labels assigned**

- `S_Reciprocity` - ok
  - span: "Get friends and a team and trade lives"
  - why: The reviewer explicitly describes trading lives with friends and teammates, which is an in-game resource exchange.

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
The review describes an interface behavior in which opening the game or entering the 1v1 area automatically scrolls to and selects the highest-bet table available from the player's coin balance. This directs the player's attention and default selection toward the costly option, while the reviewer says mis-clicks can cause unintended coin losses. The request for a Default Table Lock and for the lowest-bet table to open by default is hypothetical and is not coded. The claim that players are forced to buy real currency is not sufficiently specific to establish a separate currency-conversion or pay-to-progress mechanic.
```

**Labels assigned**

- `M_UIMisdirection` - ok
  - span: "Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins"
  - why: The interface automatically focuses and defaults to the highest-cost betting option, directing the player's selection away from safer lower-bet choices and facilitating accidental spending of coins.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `549e5e94-9b59-477d-88c7-ae5e00d62514` - Disney Solitaire

> it was fine at the start but further along into the game the rng is so obviously against you it's crazy.. it's not rewarding playing the game without spending actual money.. at around level 100 it costs 2200 but if you win the level you'll barely make that back.. the rewards need a big revamp for me.. let down by alot of things with this game the further into it you get.. sort it out

| | labels |
|---|---|
| gold | `M_PayToProgress`, `P_IllusionOfControl` |
| pred | `P_IllusionOfControl` |
| **missed** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `M_PayToProgress` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a claimed hidden manipulation of random outcomes: the RNG is said to be obviously biased against the player. Under the Illusion of Control boundary, this is an assertion that the game determines or tunes outcomes rather than leaving them genuinely random. The review also describes poor reward economics and a level costing 2200 while returning barely that amount, but it does not explicitly state that payment is required to continue or progress, nor does it describe stranded currency or a specific purchase-to-currency conversion. Therefore those monetary labels are not supported.
```

**Labels assigned**

- `P_IllusionOfControl` - ok
  - span: "the rng is so obviously against you"
  - why: The reviewer alleges that the game's random-number outcomes are deliberately biased against the player, implying manipulated rather than genuine randomness.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `33c422de-1a84-4df9-accd-cdf8bfc96295` - Dark War Survival

> No ingenuity for a base builder. Same old same old grinder. After a few weeks, it became abundantly clear that there is absolutely no opportunity for a general player to win an event. Zero skill pay to play. Zero skill pay to win. Calculated total spent on last event was 30k to win. Wish serious gamers would stop perpetuating the problem by continuing to spend obnoxious amounts of money on a little app that you just want to have a little fun on.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `S_Competition` |
| pred | `M_PayToProgress` |
| **missed** | `S_Competition` |

**Did the model consider what it missed?**

- `S_Competition` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a game characterized as repetitive, but it does not name a repeated activity required for progress, so the general complaint that it is a grinder does not satisfy T_Grinding. The reviewer states that winning an event is effectively determined by spending money, including a reported total of 30k spent to win. This describes a monetary advantage purchased for competitive success, satisfying Pay to Win under M_PayToProgress. The review does not explicitly state that players compete against other players, nor that payment is required merely to continue progressing through the game, so S_Competition and a separate pay wall label are not assigned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Zero skill pay to win."
  - why: The reviewer explicitly attributes winning to payment rather than skill, describing money as the source of an in-game advantage.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `3c46f5e0-6091-43dc-94a0-e3af3259a63d` - Cashman Casino Slots Games

> Resently cashman had changed it's bingo rewards and daily rewards. However lve found that I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards. The most I can seem to get on the timed rewards is 40,000. I'd not pay just to get my daily rewards. So I'm deleting them.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_WasteAversion`, `T_DailyRewards` |
| pred | `T_DailyRewards` |
| **missed** | `M_PayToProgress`, `M_WasteAversion` |

**Did the model consider what it missed?**

- `M_PayToProgress` - never mentioned -> **attention / recall**
- `M_WasteAversion` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a daily-reward system that now requires completing a betting threshold: they cannot complete the daily rewards unless they bet 50,000. This directly matches Daily Rewards because the game provides a daily reward objective and withholds completion of that reward unless the player performs the required daily activity. The required activity is a bet, but the review does not explicitly establish that the 50,000 is purchased with real money; it is therefore not enough for Gambling under the stated monetary-stake rule. The timed rewards and their maximum amount are mentioned as resource values, not as a distinct dark-pattern mechanic.
```

**Labels assigned**

- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The game offers daily rewards but requires the player to complete a betting requirement to obtain or complete them.

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
The review describes a sticker-collection goal in which the final one or two stickers are effectively unavailable through ordinary play and require spending a large amount of money. That makes collection completion payment-dependent, so it supports Pay to Progress. The sticker album also supports Complete the Collection because the reviewer is pursuing the final missing items. The wording that the last stickers will never be obtained unless the player pays describes deliberate scarcity tied to purchase, supporting Deceptive Luxury. The statements about spending hundreds of dollars and completing a goal only rarely do not by themselves establish a chance-based gambling mechanic, a hidden rigging mechanism, or a reward-delivery system. The review-gating complaint concerns writing an app-store review and does not match any listed in-game label.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "you will never get the last one or two unless you pay a lot of money to get them"
  - why: The final stickers are presented as artificially scarce and obtainable only through a costly purchase.
- `M_PayToProgress` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: The final collection items are described as unattainable through ordinary play unless the player pays substantially.
- `P_CompleteTheCollection` - ok
  - span: "you will never get the last one or two"
  - why: The reviewer describes pursuing the last missing stickers needed to complete an in-game collection.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `ab2097d3-2f9b-4a87-885c-25dfcddb5a70` - Gardenscapes

> Have been playing this game since COVID 19 lockdown. It was fun back then. Currently at 8416 and it gets frustratingly annoying after level 8000. I run out of lives 3-4 times daily to beat every alternate level, avg 5-7 days per level. You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying. Now I'm not interested anymore. Unistalling this game to invest some quality time in a real life. Wasted too much of money and time into this game.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `T_Grinding` |
| pred | `M_PayToProgress` |
| **missed** | `T_Grinding` |

**Did the model consider what it missed?**

- `T_Grinding` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes difficult and slow level progression, with the player taking an average of 5–7 days per level and repeatedly running out of lives. However, it does not describe a specific repetitive task required for progress, so this is not Grinding. The key monetization mechanic is that buying add-ons is presented as necessary to get through the levels; the non-paying route is described as excessively time-consuming. The reviewer also mentions having wasted money and time, but does not describe those investments making it difficult to leave—instead, they are uninstalling—so Easy to Get, Hard to Lose does not apply. Running out of lives is not enough for Playing by Appointment because no regeneration wait or cooldown schedule is stated.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying."
  - why: The review states that payment is necessary to get through the game and that the free route makes progress excessively time-consuming.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a2ece36d-c527-442d-8f18-9a16b63994c8` - War Robots Multiplayer Battles

> Its a p2w game. The only time you enjoy it is when you're new. As you progress, everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game. If you want to progress without paying money, goodluck! Even if you wanted to do f2p, you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it. Plus the only time you benofit by getting f2p rewards is ads... 💩

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `M_PayToProgress`, `M_PowerCreep`, `T_Advertisement` |
| pred | `M_EasyToPurchase`, `M_PayToProgress` |
| **missed** | `M_PowerCreep`, `T_Advertisement` |

**Did the model consider what it missed?**

- `M_PowerCreep` - considered and rejected -> **rule interpretation**
- `T_Advertisement` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes two current in-game mechanics. First, purchase offers appear every time the player logs in and block access to gameplay until they are dealt with, which is an active buying prompt that intercepts play. Second, progressing or keeping up with the shifting competitive meta requires buying the newest bot with money rather than earning it, making payment a condition for advancement or competitive progress. The statements that the game is pay-to-win and that it is only enjoyable when new are evaluations or summaries, not separate mechanics. The mention of ads does not clearly state that the player is forced or rewarded to watch them, so it does not support Advertisement. The shifting meta also does not explicitly say that an already purchased bot loses value, so Power Creep is not assigned.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game"
  - why: Purchase offers appear at login and directly intercept access to gameplay before the player can play.
- `M_PayToProgress` - ok
  - span: "where you have to buy the newest bot with money instead of earning it"
  - why: The review states that keeping up with progress requires purchasing the newest bot instead of using the free earning route.

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

- `M_DeceptiveLuxury` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes a sticker-collection system in which attempts to obtain stickers repeatedly produce duplicates, making the reward delivery produce unwanted repeated items. They are trying to complete all sticker sets, which supports collection compulsion. They also state that completing the sets is unavailable unless they pay, directly tying payment to progress. No specific limited-time scarcity or random mechanism beyond the duplicate outcomes is explicitly described, so Deceptive Luxury and Gambling are not assigned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: The review explicitly states that completing the sets requires payment.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: The reviewer is pursuing completion of all in-game sticker sets.
- `P_RewardMania` - ok
  - span: "getting stickers. always get duplicates"
  - why: The sticker reward process repeatedly delivers unwanted duplicate items rather than needed collection pieces.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b93c432d-19c0-4c6c-a2d4-bb9b21a436f3` - Dice Dreams™️

> A literal brain-rot game no wonder why they're tryna promote it through Free Cash. Also if you're thinking of making in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates! A real SCAM. Play it if u want but there are games that are actually good also, DON'T GET IN-APP PURCHASES!

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `P_CompleteTheCollection`, `P_RewardMania` |
| **missed** | `P_AestheticManipulation` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes an album-collection mechanic: the player was two cards short of completing an album and earning its grand prize. It also describes a paid card deal whose delivery produced duplicate cards rather than the promised new cards. The album completion supports Complete the Collection. The unwanted duplicate result supports Reward Mania because the reward-delivery system gives duplicate items from a card pool. The review does not establish that payment is required for progress, only that the reviewer voluntarily bought a deal, so Pay to Progress is not assigned. The mention of promotion through Free Cash concerns external advertising and is out of scope.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The reviewer is pursuing the final items needed to complete an in-game album and receive its completion reward.
- `P_RewardMania` - ok
  - span: "i bought a deal which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: The paid card deal delivers unwanted duplicate cards instead of the desired new ones, describing a reward system whose delivery sustains pursuit of collection items.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (1)

### `95ddadb3-82cd-4042-8a51-cf8b3ed164c2` - Mech Arena - Shooting Game

> You stuck waiting 30 seconds just to connect to a match. This game makes it seem like they give so many rewards but if all just for show. Its difficult to get weapon upgrades or any percs others you stick battling to win. This kind of games just rob you of your time in my opinion

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `S_Competition` |
| **spurious** | `S_Competition` |

**Model analysis**

```
The review describes a 30-second connection delay before entering a match, but this is a matchmaking or service wait rather than an in-game timer, cooldown, or other designed wait-to-play mechanic. The reviewer also says rewards are merely for show and that weapon upgrades or perks are difficult to obtain, but does not describe a specific reward-delivery system, payment gate, repetitive activity, or concrete shortfall. The phrase "battling to win" explicitly describes player-versus-player competition, although the review does not describe harmful or deceptive competitive conduct. The complaint about losing time is an evaluation, not a separate mechanic.
```

**Labels assigned**

- `S_Competition` - **SPURIOUS**
  - span: "you stick battling to win"
  - why: The span describes battling other players to achieve victory, which is a competitive game mechanic.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_PayToProgress` | 3 | 2 |
| `S_Competition` | 2 | 1 |
| `S_Reciprocity` | 2 | 0 |
| `P_AestheticManipulation` | 2 | 0 |
| `M_IntermediateCurrency` | 2 | 0 |
| `M_PowerCreep` | 1 | 0 |
| `S_FriendSpamImpersonation` | 1 | 0 |
| `M_RecurringFee` | 1 | 0 |
| `P_RewardMania` | 1 | 0 |
| `T_Advertisement` | 1 | 0 |
| `M_Gambling` | 1 | 0 |
| `T_MandatoryMarathon` | 1 | 0 |
| `M_EasyToPurchase` | 1 | 0 |
| `T_Grinding` | 1 | 0 |
| `M_WasteAversion` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |

