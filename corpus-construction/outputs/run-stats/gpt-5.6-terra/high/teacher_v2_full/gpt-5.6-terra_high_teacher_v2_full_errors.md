# Error review - gpt-5.6-terra_high_teacher_v2_full

`gpt-5.6-terra` / reasoning `high` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_full.txt` sha `6529a474a2b0`  
micro-F1 **0.800** (P 0.865 / R 0.744) - **22 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 6 | said NONE, gold had labels |
| SWAP | 5 | picked different labels than gold |
| MISSED ONLY | 6 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 5 | found all gold, added extras |

## The diagnostic that matters

Of **22** missed labels, **2** (9%) were named in the model's own analysis and dropped anyway; **20** (91%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `S_Competition` | 1 | 2 |
| `M_IntermediateCurrency` | 0 | 2 |
| `P_AestheticManipulation` | 0 | 2 |
| `M_DeceptiveLuxury` | 0 | 2 |
| `M_WasteAversion` | 1 | 1 |
| `S_Reciprocity` | 0 | 2 |
| `M_Gambling` | 0 | 2 |
| `P_RewardMania` | 0 | 1 |
| `M_EasyToPurchase` | 0 | 1 |
| `M_UIMisdirection` | 0 | 1 |
| `T_MandatoryMarathon` | 0 | 1 |
| `M_PayToProgress` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |

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
The review is primarily a feature request list. It asks for auctions using in-game currency, a way to prevent removal of decorative obstacles, an account-switching upgrade timer widget, and a hidden advanced-statistics option. Although it refers to upgrade time and an existing option to remove obstacles, it does not describe a dark-pattern mechanic: no imposed wait, payment shortcut, forced purchase, deceptive interface behavior, or progress penalty is stated. Requested features do not code under R12.
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
The reviewer attributes all described problems to bugs, crashes, lag, freezing, and unresponsive controls after an update. They mention gifts, trading with friends, catching Pokémon, and PvP/Rocket battles, but do not describe a deliberate game mechanic that pressures spending, time, social obligations, or cognition. Under R11, technical faults themselves do not receive dark-pattern labels.
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
The reviewer reports that a clan troop-request function stopped working after an update and asks for it to be fixed. Requesting troops could ordinarily describe an existing resource-transfer feature, but here the only described behavior is its unavailability due to a technical fault. Under R11, a specific behavior attributed to a bug, error, or technical fault is not coded as a deliberate dark-pattern mechanic.
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
The reviewer asks for a sticker-trading feature inside the app because some players are not on Facebook; this is a requested, not explicitly existing, mechanic, so R12 prevents coding it. They also say a purchased booster cannot be used when another player challenges them, describing a restriction on an item’s usability in a particular match context. That does not establish that payment is required for progress, that the item lost value over time, or another listed pattern. Calling the game addictive is a general evaluation rather than a described reward mechanic.
```

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
The reviewer primarily describes misleading advertising outside the installed game: pin-pull levels are advertised but seldom appear in the actual game. Under R13, store-listing or third-party advertising does not code as an in-game Advertisement mechanic. They also report having paid for extra coins and items in hopes that pin-pull content would appear, but the text does not establish that payment unlocks, skips, or advances normal in-game progression; it describes a disappointed expectation about advertised content. Finally, updates taking days to reconnect are attributed to a technical connection problem rather than a deliberate game design behavior (R11).
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
The reviewer says that items in their bag and coins, including coins they bought, are gone after leaving and returning to the game. This reports lost inventory/currency, but does not describe an intentional game mechanic that makes quitting costly, a capacity limit that strands value, or a purchase design. It may be a persistence or technical-loss problem, and no dark-pattern label is supported by the stated behavior.
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
The review has two distinct accounts. First, it alleges that once the player began buying Poké Balls, capture outcomes became worse: Pokémon repeatedly break out, depleting Balls and making further purchases necessary. This describes a paid route needed to keep catching Pokémon, as well as an alleged hidden tuning of capture outcomes to drive that spending. Second, the edit states that the reviewer did not author the displayed review and that it was posted under their identity, which describes in-app impersonation. Poké Balls are items rather than a stated real-money-to-virtual-currency conversion, so Intermediate Currency is not supported.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: The reviewer says extra purchases of capture items become necessary to continue making captures, which is progression through core gameplay.
- `P_IllusionOfControl` - ok
  - span: "when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: The span alleges that capture outcomes are covertly manipulated after purchasing in order to cause further spending.
- `S_FriendSpamImpersonation` - ok
  - span: "I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE"
  - why: The reviewer states that a review was posted under their identity even though they did not write it.

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
The reviewer describes a monetary user-interface default that automatically focuses the 1v1 menu on the highest-stake table available, rather than the lowest table. They say this design causes accidental taps that wager and lose their accumulated coins. The review then states that, after losing those coins, players must buy more coins with real money to keep playing. This supports UI Misdirection, an intermediate-currency purchase mechanism, and payment as the route past a gameplay-access barrier.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: The span describes players buying more in-game coins after their existing coin balance is lost.
- `M_PayToProgress` - **SPURIOUS**
  - span: "players lose all their hard-earned coins and are forced to buy real ones"
  - why: The reviewer says losing coins through the default high-stakes selection forces players to purchase more in order to continue playing.
- `M_UIMisdirection` - ok
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks"
  - why: The game automatically selects the highest wager table, steering players into an unintended high-cost choice.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `cc714d17-863c-4ebd-b14f-989ba17c71c4` - Dice Dreams™️

> I played this game on a different profile. the only reason I gave it five stars is because if you don't it won't let you write a review. if you want to win anything on this game it will cost hundreds of dollars. on the stickers you will never get the last one or two unless you pay a lot of money to get them. this is not a game you want to get addicted to unless you have a endless bank account. it may let you complete a goal maybe one out of hundred times.dont get your hopes up.

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury`, `M_PayToProgress`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_PayToProgress`, `P_CompleteTheCollection`, `P_IllusionOfControl` |
| **missed** | `M_DeceptiveLuxury`, `P_RewardMania` |
| **spurious** | `P_IllusionOfControl` |

**Did the model consider what it missed?**

- `M_DeceptiveLuxury` - never mentioned -> **attention / recall**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes several separate mechanics. Winning or completing goals is portrayed as effectively dependent on spending substantial real money, so payment is tied to competitive success and progression. The reviewer is also trying to finish a sticker set, with the final one or two stickers described as unobtainable without paying, which invokes the drive to complete a collection. Finally, the wording that the game may allow a goal to be completed only "one out of hundred times" alleges that the game covertly controls outcome rates rather than outcomes being determined transparently by play. The forced five-star rating to submit a review is not among the available in-game labels.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "if you want to win anything on this game it will cost hundreds of dollars."
  - why: The span directly states that real-money spending is required to win, granting an advantage to paying players.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them."
  - why: The reviewer describes being unable to acquire the remaining items needed to finish a sticker collection.
- `P_IllusionOfControl` - **SPURIOUS**
  - span: "it may let you complete a goal maybe one out of hundred times."
  - why: Saying the game only "lets" the player complete a goal at an asserted one-in-one-hundred rate alleges a concealed, game-controlled outcome schedule.

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
The review describes a collection-progress loop: the player repeatedly plays bingo rounds to obtain photos needed to complete a set. This is repetitive activity tied directly to advancement in the collection. After losing a round, the game presents an offer to spend coins for a missing photo, and the reviewer states that they have spent money pursuing these offers; this makes payment the route offered to advance the collection. The review does not clearly establish that coins are bought with real money as a currency conversion, nor does it clearly describe a random reward mechanic rather than a failed promised delivery. A search was used because the meaning of “photos” in this game was unclear; it established that Pics are collection items shown in an Adventure Book alongside missing items and duplicates.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer"
  - why: A paid coin expenditure is offered after a loss as the means to obtain a missing collection item and advance toward completing the set.
- `P_CompleteTheCollection` - ok
  - span: "claim a photo I don't have to complete the set"
  - why: The missing photo is framed as a required piece of a set the player is trying to complete.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The reviewer identifies repeatedly playing the same rounds as the activity required to obtain collection progress.

**Search:** `Bingo Blitz photos extra coins claim photo feature` -> Bingo Blitz’s official support describes Pics as collection items in an Adventure Book, which displays missing items and duplicates.

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
The reviewer is trying to complete a card album, with only two cards missing before a grand prize is awarded. They purchased a deal specifically to obtain cards described as new, but received duplicates instead. The search establishes that Dice Dreams sticker/card packs contain multiple cards and use rarity odds for additional stickers, so the paid deal is a monetary stake in a chance-based card-pack outcome rather than a straightforward purchase of the two missing cards. The album objective also directly invokes a completionist collection mechanic. Pay to Progress is not assigned separately because the payment described operates within the chance-based card-pack mechanism itself.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: The reviewer spent money on a card deal whose card results could include unwanted duplicates, making the purchase a paid chance-based reward attempt.
- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The reviewer describes pursuing the final missing cards needed to complete an album and receive its grand prize.
- `P_RewardMania` - ok
  - span: "so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: The card-pack reward delivery produced duplicate cards rather than the needed cards, describing an unpredictable reward pool.

**Search:** `Dice Dreams cards album card packs new cards duplicates` -> Dice Dreams support states that sticker packs award multiple cards, additional stickers have stated rarity odds, and packs marked “new” guarantee only a missing sticker of the relevant type; duplicate cards can still occur. ([support.dicedreams.com](https://support.dicedreams.com/hc/en-us/articles/24098716134163-I-was-assured-a-Guaranteed-NEW-Sticker-but-I-received-a-duplicate-Why?utm_source=openai))

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (6)

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
The reviewer describes an in-game advertisement that cannot be dismissed: there is no close control, tapping the screen opens the store, and returning leaves the ad screen in place until the app is force-closed. This makes viewing or remaining in the advertisement compulsory. The text does not describe an in-game purchase prompt, a payment, or a deliberate monetary UI element, so no monetary label is supported.
```

**Labels assigned**

- `T_Advertisement` - ok
  - span: "recently after seeing the ads, there is no way to close it. No cross mark on the screen , if you try to click anywhere on the screen it takes you to store. If you go back to game it is still stuck in the last sceeen of the ad. You have to kill the game to come out of the ad screen"
  - why: The advertisement has no dismissal control and prevents return to gameplay, compelling the player to remain in or force-exit the ad.

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
The reviewer describes a referral mechanic in which inviting friends and having them join through Facebook is supposed to yield in-game rewards; the complaint is that the reward credit no longer arrives after the season change. This is still evidence of recruitment being tied to incentives, rather than merely a social connection. The reviewer also describes random in-game outcomes: spending over 500 dice at the maximum multiplier yielded neither shutdowns nor bank heists, and sticker drops were duplicates. I checked the meaning of the sticker reference because the review does not itself name packs or random delivery; Monopoly GO!'s help material establishes that duplicate stickers occur because sticker content is random. The connection-error complaint is attributed to a technical fault, so it does not supply a dark-pattern label.
```

**Labels assigned**

- `P_RewardMania` - ok
  - span: "Stickers are duplicates all the way..."
  - why: The sticker system delivers random contents, and the reviewer describes repeatedly receiving duplicate outcomes rather than needed rewards.
- `S_ForcedFellowship` - ok
  - span: "I get no rewards for inviting friends and getting them to join facebook."
  - why: The span describes rewards being contingent on recruiting friends, even though the reviewer says the reward credit has stopped arriving.

**Search:** `MONOPOLY GO stickers duplicates sticker packs random rewards` -> Monopoly GO!'s official help center states that players receive many duplicate stickers over time because sticker content is random, establishing that the duplicate-sticker complaint refers to a randomized reward pool.

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
The reviewer describes a base-building game with events that ordinary players cannot realistically win because spending large amounts of real money provides the decisive advantage. "Pay to play" and "pay to win" explicitly connect payment to participating effectively and winning. Although the reviewer calls it a "grinder," they do not identify a repeated task or explain how repetition is required to progress, so Grinding is not supported. The reference to winning an event does not explicitly establish player-versus-player competition.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Zero skill pay to play. Zero skill pay to win."
  - why: The reviewer explicitly states that real-money spending, rather than skill, determines the ability to play effectively and win.

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
The review describes a daily-reward system that now requires the player to wager 50,000 before the daily rewards can be completed. The player also describes a timed reward source that only supplies 40,000, leaving them short of the required wager. This is an active daily task/reward requirement, not merely a complaint about reward value. The review does not explicitly establish that real money is exchanged for chips or that payment is required to progress, so monetary labels are not assigned.
```

**Labels assigned**

- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards."
  - why: The daily rewards are contingent on completing a required wager, describing an active daily-reward task mechanism.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `45e3e2f0-4612-4d60-9312-3bff055ec9f3` - Merge Cooking®

> I really enjoyed this game until I got to a higher level. About to quit at level 34. Not enough slots to store and play without spending $$ to buy parts. I have 63 spots, on the board and 37 spots in the refrigerator. 98 spaces total, 72 are taken up by parts of generators or lower generators that I can't merge with higher generators yet or high level items like a corn that I am not going to delete. A lambchop can take up to 9 spaces or more of my 26 spaces and I'm not deleting the chicken pie

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_WasteAversion` |
| pred | `M_PayToProgress` |
| **missed** | `M_WasteAversion` |

**Did the model consider what it missed?**

- `M_WasteAversion` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The reviewer describes an inventory-capacity constraint: most of the board and refrigerator slots are occupied by generator parts and high-level items that cannot yet be merged or safely deleted. They state that this lack of space prevents continued play unless real money is spent to buy parts. This is a payment-based route around a barrier to ongoing play, so it supports Pay to Progress. Although the reviewer details crowded storage and items they do not want to delete, they do not state that items were actually forfeited, that paid capacity was required, or that a concrete currency remainder was stranded; therefore Waste Aversion is not supported.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Not enough slots to store and play without spending $$ to buy parts."
  - why: The reviewer explicitly says insufficient storage prevents them from playing without spending real money on parts.

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
The reviewer describes a sticker-collection system in which duplicate sticker drops prevent completion of full sets. They say completing the sets is effectively gated by payment. The duplicates also imply that stickers are delivered from a randomized reward pool rather than reliably awarded, creating repeated unwanted outcomes while the player pursues missing stickers.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: Finishing the sticker sets is described as unavailable unless the player spends money.
- `P_CompleteTheCollection` - ok
  - span: "getting stickers. always get duplicates. never lets you finish all the sets"
  - why: The review describes pursuing completion of sticker sets, with missing items and duplicates obstructing the complete collection.
- `P_RewardMania` - ok
  - span: "always get duplicates"
  - why: Repeated duplicate stickers imply an unpredictable sticker-reward pool that delivers unwanted drops while the player seeks missing ones.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (5)

### `95ddadb3-82cd-4042-8a51-cf8b3ed164c2` - Mech Arena - Shooting Game

> You stuck waiting 30 seconds just to connect to a match. This game makes it seem like they give so many rewards but if all just for show. Its difficult to get weapon upgrades or any percs others you stick battling to win. This kind of games just rob you of your time in my opinion

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `T_Grinding` |
| **spurious** | `T_Grinding` |

**Model analysis**

```
The reviewer first describes a 30-second connection wait before a match, which is a matchmaking/service delay rather than an in-game timer or scheduled gate, so it does not meet Playing by Appointment. They also say rewards are "just for show," but do not identify a reward-delivery mechanism such as random drops, gacha, or a paid stake. The concrete progression complaint is that weapon upgrades and perks are difficult to obtain and the player is left repeatedly battling in order to win; this describes repeated combat activity as the route toward advancement and upgrades.
```

**Labels assigned**

- `T_Grinding` - **SPURIOUS**
  - span: "Its difficult to get weapon upgrades or any percs others you stick battling to win."
  - why: The span describes being stuck repeatedly battling as the way to obtain upgrades/perks and progress toward winning, rather than merely saying progression is slow.

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
The reviewer describes several active systems. The game is stated to be pay-to-win, meaning spending provides an advantage over non-spenders. Base update/upgrade times become increasingly long, imposing timers on advancement. Progress is portrayed as endlessly scaling with no attainable point to look forward to, while requiring continued grinding. The reviewer also says the UI is deliberately confusing and overwhelming so that players feel they need to buy items, describing purchase-oriented interface misdirection. Alliances create PvP pressure, since players outside strong alliances are attacked and bullied; this establishes player-versus-player competition, but it does not establish that harmful conduct is specifically rewarded beyond ordinary competitive play.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "it's set up in a pay to win way"
  - why: The reviewer explicitly describes a pay-to-win structure, in which spending grants an in-game advantage.
- `M_UIMisdirection` - ok
  - span: "The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff."
  - why: The reviewer attributes deliberately confusing and overwhelming UI design to making players feel compelled to purchase.
- `S_Competition` - ok
  - span: "If you are not in one then you get attacked and bullied."
  - why: Being attacked by other players when outside an alliance describes a player-versus-player competitive structure.
- `T_Grinding` - **SPURIOUS**
  - span: "just more grind"
  - why: The reviewer explicitly characterizes continued progress as requiring grinding.
- `T_InfiniteTreadmill` - ok
  - span: "Everything scales endlessly, there is kinda no point to look forward to"
  - why: The game is described as scaling endlessly with no attainable endpoint to work toward.
- `T_PlayingByAppointment` - ok
  - span: "the update times for your base are becoming ridiculous"
  - why: The base update/upgrade times describe increasingly burdensome in-game timers that delay advancement.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a2ece36d-c527-442d-8f18-9a16b63994c8` - War Robots Multiplayer Battles

> Its a p2w game. The only time you enjoy it is when you're new. As you progress, everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game. If you want to progress without paying money, goodluck! Even if you wanted to do f2p, you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it. Plus the only time you benofit by getting f2p rewards is ads... 💩

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `M_PayToProgress`, `M_PowerCreep`, `T_Advertisement` |
| pred | `M_EasyToPurchase`, `M_PayToProgress`, `M_PowerCreep`, `M_UIMisdirection`, `T_Advertisement` |
| **spurious** | `M_UIMisdirection` |

**Model analysis**

```
The review describes several active monetization mechanics. Purchase offers appear every login and block access to play until the player gets past them, which both interrupts gameplay with buying prompts and obstructs the opt-out path. Progress is described as effectively unavailable to free players because new bots must be bought with real money rather than earned. The reviewer also describes a shifting meta in which newer bots are necessary to remain viable, implying that older bots lose practical value as new releases arrive. Finally, free-to-play rewards are obtained through ads, describing rewarded advertising.
```

**Labels assigned**

- `M_EasyToPurchase` - ok
  - span: "everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game."
  - why: In-app purchase offers intercept the player on each login before gameplay can begin, requiring them to deal with buying prompts.
- `M_PayToProgress` - ok
  - span: "If you want to progress without paying money, goodluck! Even if you wanted to do f2p, you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it."
  - why: The reviewer states that progression and keeping up require purchasing the newest bot with real money rather than earning it.
- `M_PowerCreep` - ok
  - span: "you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it."
  - why: A shifting meta requiring the newest bots implies that older bots lose competitive value as new ones are released.
- `M_UIMisdirection` - **SPURIOUS**
  - span: "everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game."
  - why: The purchase-offer screen obstructs access to play until it is dismissed, directing the player through monetized UI before gameplay.
- `T_Advertisement` - ok
  - span: "the only time you benofit by getting f2p rewards is ads... 💩"
  - why: The reviewer describes ads as the route through which free-to-play rewards are obtained.

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
The reviewer describes a time-limited card-collection system: cards come through packs, but near the end of a collection period the packs allegedly stop yielding new cards. This leaves the player unable to finish the set and forfeiting its completion reward when the collection expires. The card packs therefore describe a randomised reward delivery mechanism with unwanted/duplicate outcomes, while the stated aim is completing the full set. The expiring collection and missed reward describe a game-clock deadline and loss, but the review does not describe anxiety or continued play specifically to avoid falling behind.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "when one is almost close to completing a set"
  - why: The reviewer describes pursuing completion of a card set, with the missing cards preventing the collection from being finished.
- `P_RewardMania` - **SPURIOUS**
  - span: "include new cards in every card pack because I noticed when one is almost close to completing a set, new cards don't appear again"
  - why: Card packs are described as repeatedly delivering no new cards when specific missing cards are needed, making the reward-delivery mechanism the obstacle.
- `T_PlayingByAppointment` - ok
  - span: "especially when the set is almost expiring. So after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion"
  - why: The collection reward expires on the game's clock and is lost if the set is not completed before that deadline.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `84bbc363-d55a-4cf1-a557-c61ed7ab82bc` - Last War:Survival Game

> Once you get past building the city block stage, it gets kinda boring. It's just grinding resources trying not to get raided so you can level up to have a few more attempts at the left right scroller game. The advertisement that's really becomes not that great. The bigger alliances all just attack the smaller alliances and take their resources. I dedicated some time to this game and to my alliances and am disappointed with current status.

| | labels |
|---|---|
| gold | `S_Competition`, `S_EncouragesAntiSocialBehavior`, `T_Grinding` |
| pred | `P_EasyToGetHardToLose`, `S_Competition`, `S_EncouragesAntiSocialBehavior`, `T_Grinding` |
| **spurious** | `P_EasyToGetHardToLose` |

**Model analysis**

```
The reviewer describes a resource-progression loop: they repeatedly gather resources in order to level up, and leveling up provides additional attempts at a separate left-right scroller mode. They also describe alliance-versus-alliance raiding, specifically larger alliances attacking smaller ones and taking their resources. This is both direct player competition and an asymmetric harmful incentive because the attackers gain the defenders' resources. The need to keep gathering resources while avoiding raids also means accumulated resources are put at risk, making disengagement costly in terms of value already earned. The sentence about advertising appears to criticize the advertised gameplay or quality, not advertisements that the player is forced or rewarded to watch inside the app.
```

**Labels assigned**

- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "It's just grinding resources trying not to get raided"
  - why: Resources earned through grinding are portrayed as value the player must actively protect from being taken, raising the cost of stopping or disengaging.
- `S_Competition` - ok
  - span: "The bigger alliances all just attack the smaller alliances and take their resources."
  - why: The game is described as placing alliances against one another through attacks and resource-taking.
- `S_EncouragesAntiSocialBehavior` - ok
  - span: "The bigger alliances all just attack the smaller alliances and take their resources."
  - why: The span describes stronger groups gaining resources by repeatedly harming weaker groups, combining asymmetric aggression with a concrete benefit for the aggressor.
- `T_Grinding` - ok
  - span: "It's just grinding resources trying not to get raided so you can level up"
  - why: The reviewer explicitly identifies repeatedly gathering resources as the activity required to level up.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `M_PayToProgress` | 1 | 3 |
| `S_Competition` | 3 | 0 |
| `M_Gambling` | 2 | 1 |
| `T_Grinding` | 0 | 2 |
| `P_RewardMania` | 1 | 1 |
| `M_IntermediateCurrency` | 2 | 0 |
| `M_UIMisdirection` | 1 | 1 |
| `P_AestheticManipulation` | 2 | 0 |
| `M_DeceptiveLuxury` | 2 | 0 |
| `M_WasteAversion` | 2 | 0 |
| `S_Reciprocity` | 2 | 0 |
| `M_EasyToPurchase` | 1 | 0 |
| `T_MandatoryMarathon` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `P_IllusionOfControl` | 0 | 1 |
| `T_PlayingByAppointment` | 1 | 0 |

