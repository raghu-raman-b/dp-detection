# Error review - gpt-5.6-luna_xhigh_teacher_v3_full

`gpt-5.6-luna` / reasoning `xhigh` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v3_full.txt` sha `a6ae58246360`  
micro-F1 **0.818** (P 0.800 / R 0.837) - **16 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 2 | said NONE, gold had labels |
| SWAP | 6 | picked different labels than gold |
| MISSED ONLY | 3 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 5 | found all gold, added extras |

## The diagnostic that matters

Of **14** missed labels, **2** (14%) were named in the model's own analysis and dropped anyway; **12** (86%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `M_IntermediateCurrency` | 0 | 2 |
| `M_Gambling` | 0 | 2 |
| `M_WasteAversion` | 0 | 1 |
| `P_AestheticManipulation` | 0 | 1 |
| `S_Competition` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `S_Reciprocity` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `M_EasyToPurchase` | 0 | 1 |
| `P_RewardMania` | 0 | 1 |
| `M_PayToProgress` | 1 | 0 |
| `T_MandatoryMarathon` | 0 | 1 |

## Missed everything (predicted NONE) (2)

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
The review describes a clan troop-request feature, which would ordinarily involve requesting resources from other players. However, the reviewer says the feature no longer works after an update and explicitly asks for it to be fixed. Because the specific behavior is attributed to a technical fault rather than described as a functioning social-transfer mechanic, no dark-pattern label applies.
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
The reviewer reports that leaving the game with a full bag and returning causes the bag contents to be gone, while earned and purchased coins have also been consumed or lost. This describes apparent loss of resources, but it does not identify a deliberate inventory-cap rule, a purchase prompt, a time gate, pressure to keep playing, or an inability to stop a session. No meso label is supported by an explicit game mechanic in the review.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (6)

### `fd1230ab-7d12-4aeb-a425-e37ed06bcd5c` - Pokémon GO

> I love this game, just started playing about 2 months ago. Though I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way. I feel taken advantage of. 3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| pred | `M_Gambling`, `P_IllusionOfControl`, `P_RewardMania`, `S_FriendSpamImpersonation` |
| **missed** | `P_OptimismAndFrequencyBiases` |
| **spurious** | `M_Gambling`, `P_RewardMania` |

**Did the model consider what it missed?**

- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes purchased Poké Balls being consumed when capture attempts fail, with repeated breakouts causing the player to buy more. This is a paid chance-based capture attempt, so it supports Gambling and the variable-reward aspect of Reward Mania. The reviewer also attributes the repeated failures to a rule that consumes balls faster after purchasing, which is an allegation that the game manipulates outcome determination and supports Illusion of Control. I do not add Pay to Progress because purchasing another ball is internal to the chance attempt rather than a separate progression gate. The edit retracts the claim about speaking with other players, so that statement does not support any social recruitment or reciprocity label. However, the statement that the review was not written by the account holder describes impersonation under the destination rule.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out"
  - why: Purchased Poké Balls are used for capture attempts whose success is uncertain, making them a paid stake for a chance at obtaining a Pokémon.
- `P_IllusionOfControl` - ok
  - span: "they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: The reviewer attributes the repeated failures to an outcome rule that consumes balls and drives further purchases, alleging manipulated capture odds.
- `P_RewardMania` - **SPURIOUS**
  - span: "when I tried to make a capture that they keep breaking out"
  - why: The unpredictable success of repeated capture attempts makes the reward-delivery mechanism itself the focus of engagement.
- `S_FriendSpamImpersonation` - ok
  - span: "I DID NOT WRITE THIS REVIEW"
  - why: The edit reports that a review appeared under the player's identity without being authored by them, which fits the codebook's impersonation case.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `5e6a5625-5291-4f0e-897c-1b63c1a26494` - MONOPOLY GO!

> I loved this game until the new season started. Suddenly I get no rewards for inviting friends and getting them to join facebook. I am struggling to get dices and when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way... And today. Well, I cannot log in to the game at all. It keeps giving me an internet connection error which is absolute nonsense. I have connected to 3 different wifi connections. BS!!😡

| | labels |
|---|---|
| gold | `M_Gambling`, `P_RewardMania`, `S_ForcedFellowship` |
| pred | `P_RewardMania`, `S_Competition`, `S_ForcedFellowship`, `S_FriendSpamImpersonation` |
| **missed** | `M_Gambling` |
| **spurious** | `S_Competition`, `S_FriendSpamImpersonation` |

**Did the model consider what it missed?**

- `M_Gambling` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a referral mechanic that is supposed to reward the player for inviting friends and getting them connected through Facebook; the complaint that rewards stopped after the new season still identifies the recruitment mechanic. The wording also describes outgoing invitations through the player's social graph. The dice passage reports a large max-bet run with no Shutdowns or Bank Heists and repeated duplicate stickers, indicating unpredictable or unwanted reward delivery rather than merely a low reward amount. A term check established that Shutdowns and Bank Heists are MONOPOLY GO! player-interaction mini-games involving targeting another player's board or bank, so they support Competition but not Encourages Anti-Social Behavior because no unusually harmful or dishonest targeting is alleged. ([monopolygo.com](https://www.monopolygo.com/news/37?utm_source=openai)) The login failure is explicitly attributed to an internet connection error, so it is a technical malfunction and does not itself support a dark-pattern label. The review does not describe payment, a daily-return reward cycle, a progress grind, or a compulsion to complete the sticker collection.
```

**Labels assigned**

- `P_RewardMania` - ok
  - span: "when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way..."
  - why: The span describes a large run producing absent event outcomes and repeated duplicate sticker drops, showing undesirable and variable reward delivery.
- `S_Competition` - **SPURIOUS**
  - span: "No Shut downs and no bank heists"
  - why: The identified Shutdown and Bank Heist mechanics involve interacting with and targeting other players, which places players in competition. ([monopolygo.com](https://www.monopolygo.com/news/37?utm_source=openai))
- `S_ForcedFellowship` - ok
  - span: "no rewards for inviting friends and getting them to join facebook"
  - why: The game links in-game rewards to bringing new people into the social/game network, even though the reviewer says the rewards have stopped.
- `S_FriendSpamImpersonation` - **SPURIOUS**
  - span: "inviting friends and getting them to join facebook"
  - why: Inviting Facebook friends describes an outgoing message or invitation sent through the player's social graph.

**Search:** `MONOPOLY GO! "Shutdowns" "Bank Heists" meaning` -> The search established that Shutdowns and Bank Heists are player-interaction mini-games involving targeting another player's board or bank and producing rewards. ([monopolygo.com](https://www.monopolygo.com/news/37?utm_source=openai))

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fdef27f2-9a21-4b8e-a04c-7a4753e0fb07` - 8 Ball Pool

> The game is great, but the user interface is completely rigged. Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins and are forced to buy real ones. ​We need a "Default Table Lock" or the game should always open the lowest bet table by default, not the highest! Fix this scammy feature. Giving 1 star

| | labels |
|---|---|
| gold | `M_Gambling`, `M_IntermediateCurrency`, `M_UIMisdirection` |
| pred | `M_IntermediateCurrency`, `M_PayToProgress`, `M_UIMisdirection`, `S_Competition` |
| **missed** | `M_Gambling` |
| **spurious** | `M_PayToProgress`, `S_Competition` |

**Did the model consider what it missed?**

- `M_Gambling` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a player-versus-player mode with tables that require coins to enter. The interface automatically moves the selection to the highest-cost table rather than leaving the player at a neutral or low-cost option, creating a default-selection and accidental-misclick mechanic. The reviewer says this can drain the player's earned coins and leave buying more coins as the route back into play, implying both pay-to-progress and conversion of real money into in-game currency. The request for a Default Table Lock is hypothetical and is not coded.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "players lose all their hard-earned coins and are forced to buy real ones."
  - why: The span implies that real money is used to acquire more in-game coins, making coins the currency obtained through a real-money conversion.
- `M_PayToProgress` - **SPURIOUS**
  - span: "players lose all their hard-earned coins and are forced to buy real ones."
  - why: After the game removes the player's usable coins, purchasing more becomes the stated route for continuing to play.
- `M_UIMisdirection` - ok
  - span: "Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins."
  - why: The interface automatically directs the player to the most expensive available table, steering attention and selection toward a costly option.
- `S_Competition` - **SPURIOUS**
  - span: "go to the 1v1 section"
  - why: A 1v1 section describes player-versus-player competition.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `3c46f5e0-6091-43dc-94a0-e3af3259a63d` - Cashman Casino Slots Games

> Resently cashman had changed it's bingo rewards and daily rewards. However lve found that I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards. The most I can seem to get on the timed rewards is 40,000. I'd not pay just to get my daily rewards. So I'm deleting them.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_WasteAversion`, `T_DailyRewards` |
| pred | `M_Gambling`, `T_DailyRewards` |
| **missed** | `M_PayToProgress`, `M_WasteAversion` |
| **spurious** | `M_Gambling` |

**Did the model consider what it missed?**

- `M_PayToProgress` - considered and rejected -> **rule interpretation**
- `M_WasteAversion` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a daily-reward system that cannot be completed unless the player wagers 50,000 in the casino game. The daily reward is therefore an incentive tied to a recurring daily cycle, while the 50,000 bet is a chance-based wager within the slots mechanic. The statement about not paying is dissatisfaction with the cost of obtaining the reward, but it does not clearly establish a real-money payment or a separate paywall outside the wager, so M_PayToProgress is not assigned. The timed rewards are mentioned as a reward amount, not as an imposed waiting timer, so T_PlayingByAppointment is not assigned.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "unless I bet 50,000"
  - why: In a casino-slots game, betting 50,000 is a wager used within a chance-based mechanic, even though the review does not say the stake was bought with real money.
- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The game provides daily rewards and makes completion of that daily reward track conditional on performing the required activity.

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
The review describes a collection loop rather than only general dissatisfaction. The player repeats bingo rounds to obtain photos and complete a set, which is repetitive progress work and a collection-completion goal. After a loss, the game offers a coin payment for a missing photo, and the reviewer says they spend on that offer and have wasted money; this makes payment a route to collection progress. The failure to receive the promised photo is reported as non-delivery, but the review does not establish a random-reward mechanic, hidden wording, UI friction trick, bug attribution, or a real-money-to-coins conversion. The broad complaints about user-friendliness and unreachable goals do not independently support another label. No web search was needed.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer"
  - why: The game offers a paid coin route to obtain a missing item required to complete the set, and the reviewer says they use that route.
- `P_CompleteTheCollection` - ok
  - span: "a photo I don't have to complete the set"
  - why: The player is pursuing a complete set of in-game photos, directly matching the collection-completion mechanic.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The player describes repeatedly playing the same type of round in order to make collection progress.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `7b564746-b769-4856-b686-529f8717c3ba` - Candy Crush Soda Saga

> I like the game except: 1. I was charged 10 gold pcs for 5 moves, I had 2 moves left. I had 7 moves but only used 1 move. 2. I paid for a pkg unlimited lives ect. I got the etc. but not the lives. 3. The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone. 4. You cannot win enough gold to play without buying sometimes. 5. The packages need to cost less. 6. When I buy pkg should not be timed.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `M_PayToProgress`, `T_PlayingByAppointment` |
| pred | `M_PayToProgress`, `M_WasteAversion`, `T_PlayingByAppointment` |
| **missed** | `M_IntermediateCurrency` |
| **spurious** | `M_WasteAversion` |

**Did the model consider what it missed?**

- `M_IntermediateCurrency` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes spending gold for extra moves and says that earned gold is sometimes insufficient to keep playing, so buying becomes a route to continued play. It also reports being charged for five moves but using only one, which represents concrete paid value being forfeited. Timed bonuses continue expiring while the player is away, making the game's clock govern when rewards remain available. The missing lives from a purchased package is a failure to deliver purchased content rather than a clearly described deliberate design mechanic, and the requests for lower prices or untimed packages are not themselves labels. The timer creates a schedule and loss of rewards, but the review does not describe anticipatory anxiety or pressure to return, so FOMO is not assigned. No external search is needed.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The free route does not provide enough gold to continue playing, so buying is sometimes necessary for continued progress or access.
- `M_WasteAversion` - **SPURIOUS**
  - span: "I was charged 10 gold pcs for 5 moves, I had 2 moves left. I had 7 moves but only used 1 move."
  - why: The player says they paid for five moves but used only one, showing a concrete loss of purchased value rather than a general price complaint.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone."
  - why: Bonuses expire according to real-world time while the player is absent, making the game's schedule determine when the rewards remain available.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (3)

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
The review describes a repetitive base-builder, but "Same old same old grinder" names no specific repeated task or progress loop, so it does not support T_Grinding. The clear mechanic is that spending money rather than skill is presented as the route to winning an event, with 30k cited as the amount spent; this supports Pay to Win under M_PayToProgress. The review does not clearly identify opponents, rankings, or a player-versus-player contest, so S_Competition is not assigned. No other coded mechanic is explicitly described, and no search was needed.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Zero skill pay to win. Calculated total spent on last event was 30k to win."
  - why: The span states that money, including a reported 30k expenditure, is used to obtain victory in an event rather than relying on skill.

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
The review describes a sticker collection in which the final one or two stickers are effectively unavailable through ordinary play and require a large payment, making payment a gate on completing that goal. The same span describes scarcity attached to purchase, so the final stickers are being monetized as rare or exclusive items. The sticker set also supports Complete the Collection because the reviewer is concerned with obtaining the missing final pieces. The forced five-star review condition, addiction warning, and low claim that a goal succeeds about one time in a hundred do not match any listed label: they do not explicitly describe a paid chance mechanic, reward-delivery system, sunk-cost retention, or another coded design behavior. No external search was needed because the review itself identifies the relevant item and payment condition.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them."
  - why: The final stickers are made effectively scarce and obtainable through a costly purchase route, tying scarcity to price.
- `M_PayToProgress` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them."
  - why: Completing the sticker objective is described as unavailable unless the player pays a lot of money.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two"
  - why: The reviewer is describing missing final pieces of a sticker set that the player is trying to complete.

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
The review describes a sticker-collection system. The player is repeatedly receiving duplicate stickers, which implies a reward pool that delivers unwanted repeat items. The goal is to complete all sticker sets, so the collection itself is a motivating objective. The review also states that completing the sets is unavailable unless the player pays, making payment a progression gate. No web search is needed because the mechanics are clear from the review.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: Completion of the sticker sets is stated to be unavailable without payment, so payment gates progress.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: The player is pursuing completion of all sticker sets, which is an in-game collection goal.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: Repeated duplicate stickers describe an unpredictable reward-delivery system that can require multiple attempts to obtain missing items.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (5)

### `95ddadb3-82cd-4042-8a51-cf8b3ed164c2` - Mech Arena - Shooting Game

> You stuck waiting 30 seconds just to connect to a match. This game makes it seem like they give so many rewards but if all just for show. Its difficult to get weapon upgrades or any percs others you stick battling to win. This kind of games just rob you of your time in my opinion

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `P_AestheticManipulation`, `S_Competition`, `T_Grinding` |
| **spurious** | `P_AestheticManipulation`, `S_Competition`, `T_Grinding` |

**Model analysis**

```
The review describes entering a match, so competition against other players is present. The 30-second connection delay is a matchmaking or queue delay rather than an in-game timer or cooldown, so it does not trigger Playing by Appointment. The game is also described as presenting many rewards that are merely for show, which implies deceptive framing of rewards. Finally, weapon upgrades and perks are difficult to obtain and require continued battling to win, implying repeated combat as the route to progress. The complaint that the game wastes time by itself is only an evaluation. No payment mechanic is described, and no web search was needed.
```

**Labels assigned**

- `P_AestheticManipulation` - **SPURIOUS**
  - span: "This game makes it seem like they give so many rewards but if all just for show."
  - why: The game is described as making its reward presentation appear generous while the rewards are merely superficial, which is deceptive framing.
- `S_Competition` - **SPURIOUS**
  - span: "connect to a match"
  - why: Connecting to a match describes the game placing the player into competitive play against other players.
- `T_Grinding` - **SPURIOUS**
  - span: "difficult to get weapon upgrades or any percs others you stick battling to win"
  - why: The span names continued battling as the repeated activity needed to obtain upgrades or perks and win.

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
The review describes a card-collection system in which card packs deliver cards for sets, and completing a set grants a reward. The reviewer says that near the collection's expiration, packs stop providing new cards, leaving the player unable to obtain the remaining cards and causing the completion reward to be missed. The collection goal supports Complete the Collection; the pack-based, unreliable delivery of missing cards supports Reward Mania; and the expiration deadline plus loss of the reward supports Playing by Appointment. No monetary stake is described, so Gambling and Pay to Progress do not apply. I searched only to identify the Royal Match card-pack feature; official materials confirm that cards are obtained from Card Packs, collections contain sets, and pack probabilities can affect access to missing cards. ([dreamgames.helpshift.com](https://dreamgames.helpshift.com/hc/en/3-royal-match/section/55-collection/?utm_source=openai))
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "So after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion"
  - why: The player is pursuing completion of a card set and the reward attached to completing it.
- `P_RewardMania` - **SPURIOUS**
  - span: "include new cards in every card pack because I noticed when one is almost close to completing a set, new cards don't appear again"
  - why: Card packs are the reward-delivery mechanism, but repeated packs allegedly stop yielding the specific new cards needed to finish the set.
- `T_PlayingByAppointment` - ok
  - span: "especially when the set is almost expiring. So after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion"
  - why: The collection has a fixed end date, and failing to obtain the remaining cards before it ends causes the completion reward to be forfeited.

**Search:** `Royal Match card packs collection expiration new cards card collection` -> Official Royal Match materials establish that cards are obtained by opening Card Packs and that collections are organized into sets; the collection page also describes probabilities affecting whether packs provide missing cards. ([dreamgames.helpshift.com](https://dreamgames.helpshift.com/hc/en/3-royal-match/section/55-collection/?utm_source=openai))

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
The review describes low rewards for a long quest, debilitating exploration, disliked character aesthetics, a long play history, and the absence of a Resin overflow system. The low number of Primogems after a seven-hour quest describes poor reward value, not a reward-delivery mechanism, so it does not support Reward Mania. The character-design criticism is an aesthetic evaluation, not evidence that aesthetics are being used to manipulate behavior. Playing since 2021 is only a long history and does not show that accumulated investment is making the player stay. The only codable mechanic is the Resin system: the search established that Resin regenerates naturally and players are advised to avoid reaching its cap to preserve free regeneration, so the lack of overflow imposes a timing schedule on play. ([support.hoyoverse.com](https://support.hoyoverse.com/hc/en-us/articles/50333934832537-Effective-Resin-Management?utm_source=openai))
```

**Labels assigned**

- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "there is no resin overflow system"
  - why: The absence of overflow means regenerating Resin cannot be stored beyond its cap, implying that players must return and spend it before the cap to avoid losing regeneration time. ([support.hoyoverse.com](https://support.hoyoverse.com/hc/en-us/articles/50333934832537-Effective-Resin-Management?utm_source=openai))

**Search:** `Genshin Impact resin overflow system meaning capped resin regeneration` -> The search established that Genshin Impact Resin regenerates over time and that players are advised to use it before reaching its cap to maximize free regeneration. ([support.hoyoverse.com](https://support.hoyoverse.com/hc/en-us/articles/50333934832537-Effective-Resin-Management?utm_source=openai))

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b93c432d-19c0-4c6c-a2d4-bb9b21a436f3` - Dice Dreams™️

> A literal brain-rot game no wonder why they're tryna promote it through Free Cash. Also if you're thinking of making in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates! A real SCAM. Play it if u want but there are games that are actually good also, DON'T GET IN-APP PURCHASES!

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_Gambling`, `M_PayToProgress`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_EasyToGetHardToLose`, `P_RewardMania` |
| **spurious** | `M_Gambling`, `M_PayToProgress`, `P_EasyToGetHardToLose` |

**Model analysis**

```
The review describes an album-collection system in which two missing cards would complete the album and award a grand prize. That near-complete goal led the reviewer to spend on an in-app deal intended to obtain the missing cards, so the purchase was being used for progress. The deal promised NEW cards but delivered duplicates, describing both a misleading purchase claim and a variable card-reward system that can produce unwanted duplicates. Because the deal was purchased and the card outcome was variable, it also supports a paid chance-based reward mechanic. The near-complete album made abandoning the goal less attractive, as shown by the decision to buy the deal. The reference to promotion through Free Cash concerns out-of-game marketing and is excluded under R13; the insults and warnings are not mechanics. A search was used only to resolve the game-specific card/deal mechanic: Dice Dreams identifies album cards as stickers obtained through packs and special offers, with variable odds and documented duplicate outcomes. ([support.dicedreams.com](https://support.dicedreams.com/hc/en-us/articles/24098716134163-I-was-assured-a-Guaranteed-NEW-Sticker-but-I-received-a-duplicate-Why))
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "making in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: The review describes paying for a card deal whose outcome could be one of several cards, making money the stake for a chance-based prize.
- `M_PayToProgress` - **SPURIOUS**
  - span: "so i bought a deal which promised i would get NEW cards"
  - why: The reviewer spent money to obtain missing album cards and advance toward the album's grand prize.
- `P_AestheticManipulation` - ok
  - span: "which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: The purchase offer's stated NEW-card outcome conflicts with the duplicates delivered, so the deception is in the wording of the offer.
- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The reviewer is pursuing the final missing cards to complete an in-game album collection and receive its completion reward.
- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "I had two cards left which would grant me the grand prize for completing an album, so i bought a deal"
  - why: The nearly completed album and its grand prize made the reviewer purchase a deal rather than abandon the partially completed goal.
- `P_RewardMania` - ok
  - span: "promised i would get NEW cards, and all i got were useless duplicates!"
  - why: The card system delivered unwanted duplicate outcomes instead of a new card, describing the reward-delivery mechanism rather than merely its value.

**Search:** `Dice Dreams album card packs duplicate cards deal new cards` -> Official Dice Dreams support identifies album cards as collectible stickers obtained from packs and special offers, with variable odds; it also explains that packs marked NEW can still produce duplicates under type-specific rules. ([support.dicedreams.com](https://support.dicedreams.com/hc/en-us/articles/24098716134163-I-was-assured-a-Guaranteed-NEW-Sticker-but-I-received-a-duplicate-Why))

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
The review describes an update that removed open silver, which the search established is silver left exposed so other players can take it, making it part of the game's PvP attack layer. ([reddit.com](https://www.reddit.com/r/TotalBattle/comments/1lw5at1?utm_source=openai)) The active monetization mechanic is that spending is required for meaningful growth. The reviewer also says that this paid growth was then made pointless by the update, so previously purchased progress or value was devalued over time. I do not assign Competition because PvP is described as removed rather than currently operating, and bringing back open silver is a request for a missing feature under R12. The statement that money was wasted does not by itself show sunk-cost retention or difficulty leaving.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You have to spend to have any meaningful growth"
  - why: The reviewer says spending money is required to achieve meaningful in-game growth.
- `M_PowerCreep` - **SPURIOUS**
  - span: "You have to spend to have any meaningful growth and then they go and make it all pointless"
  - why: The update is described as making previously paid-for growth pointless, devaluing the player's prior investment over time.

**Search:** `Total Battle War Strategy "open silver"` -> The search established that open silver is silver left exposed and available for other players to take, making it a PvP-related resource mechanic. ([reddit.com](https://www.reddit.com/r/TotalBattle/comments/1lw5at1?utm_source=openai))

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_Gambling` | 2 | 3 |
| `S_Competition` | 1 | 3 |
| `M_PayToProgress` | 1 | 3 |
| `P_RewardMania` | 1 | 2 |
| `M_IntermediateCurrency` | 2 | 0 |
| `M_WasteAversion` | 1 | 1 |
| `P_AestheticManipulation` | 1 | 1 |
| `M_PowerCreep` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `T_Grinding` | 0 | 1 |
| `S_FriendSpamImpersonation` | 0 | 1 |
| `S_Reciprocity` | 1 | 0 |
| `M_EasyToPurchase` | 1 | 0 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `T_MandatoryMarathon` | 1 | 0 |

