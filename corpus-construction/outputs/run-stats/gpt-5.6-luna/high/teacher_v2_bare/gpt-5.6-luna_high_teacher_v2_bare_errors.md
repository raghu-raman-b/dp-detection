# Error review - gpt-5.6-luna_high_teacher_v2_bare

`gpt-5.6-luna` / reasoning `high` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_bare.txt` sha `ecd3c1810cf2`  
micro-F1 **0.736** (P 0.779 / R 0.698) - **25 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 6 | said NONE, gold had labels |
| SWAP | 4 | picked different labels than gold |
| MISSED ONLY | 6 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 9 | found all gold, added extras |

## The diagnostic that matters

Of **26** missed labels, **0** (0%) were named in the model's own analysis and dropped anyway; **26** (100%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `P_RewardMania` | 0 | 5 |
| `P_IllusionOfControl` | 0 | 3 |
| `S_Reciprocity` | 0 | 2 |
| `P_AestheticManipulation` | 0 | 2 |
| `M_Gambling` | 0 | 2 |
| `M_PayToProgress` | 0 | 2 |
| `M_EasyToPurchase` | 0 | 2 |
| `M_WasteAversion` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `S_FriendSpamImpersonation` | 0 | 1 |
| `S_Competition` | 0 | 1 |
| `T_PlayingByAppointment` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |
| `T_MandatoryMarathon` | 0 | 1 |
| `M_IntermediateCurrency` | 0 | 1 |

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
The review is a list of requested features rather than a description of manipulative mechanics currently operating in the game. The reviewer proposes auctions using in-game currency, removal of an existing option to delete a decorated obstacle, an account-switching widget showing upgrade timers, and access to hidden troop statistics. These requests do not establish any codebook pattern, and the mention of upgrade time remaining does not by itself describe an imposed waiting mechanic or a requirement to play at scheduled times.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `5f3e71b5-200c-45a3-b90e-e08b0dc0e1a3` - Cash Frenzy™ - Casino Slots

> Is a good game, but I will like to place my formal complain about the genie game, in multiple times whe the wheel spin after stopping on a great price the genie move the wheel to a spin tag, and then the prices after the spin are way lower than the original price, from 100 million with 5x multiplier to a 48 million. Is the only part I don't like. There should be a player choice to keep or spin.

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_RewardMania` |
| pred | _NONE_ |
| **missed** | `P_IllusionOfControl`, `P_RewardMania` |

**Did the model consider what it missed?**

- `P_IllusionOfControl` - never mentioned -> **attention / recall**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a genie wheel mechanic in which the wheel appears to stop on a high prize, but the game then forces or redirects it to spin again, producing a substantially lower reward. The reviewer also states that there is no player choice to keep the original result or accept the reroll. This is a deliberate in-game outcome rule, not a technical fault. However, the review does not explicitly describe real-money participation, so M_Gambling cannot be assigned from the text alone. The reroll does not clearly match any other listed label: it is not a purchase gate, timer, daily reward, collection mechanic, or a deception about player skill.
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
The review attributes all described problems to bugs, crashing, lag, slow response, or freezing after an update. Although it mentions existing game activities—opening gifts, trading with friends, throwing Poké Balls, and PvP and Rocket battles—the reported inability to perform them is presented as a technical malfunction rather than an intentional game design behavior. Under R11, these spans do not support dark-pattern labels, and no other qualifying mechanic is described.
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
The reviewer reports a post-update technical malfunction: they can no longer request troops from their clan. This describes a broken social game function, not a deliberate design mechanic, and the text does not describe any qualifying dark-pattern behavior.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `549e5e94-9b59-477d-88c7-ae5e00d62514` - Disney Solitaire

> it was fine at the start but further along into the game the rng is so obviously against you it's crazy.. it's not rewarding playing the game without spending actual money.. at around level 100 it costs 2200 but if you win the level you'll barely make that back.. the rewards need a big revamp for me.. let down by alot of things with this game the further into it you get.. sort it out

| | labels |
|---|---|
| gold | `M_PayToProgress`, `P_IllusionOfControl` |
| pred | _NONE_ |
| **missed** | `M_PayToProgress`, `P_IllusionOfControl` |

**Did the model consider what it missed?**

- `M_PayToProgress` - never mentioned -> **attention / recall**
- `P_IllusionOfControl` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes unfavorable random-number generation and an in-game economy in which a level costs 2200 while winning returns barely that amount. They also say playing without spending real money is not rewarding. However, the review does not explicitly describe a required payment gate, a purchase advantage, chance-based purchases for prizes, repetitive tasks, or a mechanic that deceives the player about their skill. The poor reward balance and suspected unfair RNG do not independently satisfy any listed label.
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
The reviewer reports that items in the bag and both earned and purchased coins disappear after leaving and returning to the game. This is described as unexpected loss of progress or resources, not as an intentional game rule such as a required session, a spending mechanic, or a retention design. Because the text does not establish a deliberate mechanic, no label applies.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (4)

### `fd1230ab-7d12-4aeb-a425-e37ed06bcd5c` - Pokémon GO

> I love this game, just started playing about 2 months ago. Though I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way. I feel taken advantage of. 3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| pred | `M_PayToProgress` |
| **missed** | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `P_IllusionOfControl` - never mentioned -> **attention / recall**
- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**
- `S_FriendSpamImpersonation` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a consumable capture resource: Poké Balls are used during capture attempts, repeated failed attempts deplete them, and the reviewer says this creates a need to purchase more. That is a monetized route for continuing capture-related progress, although the review does not describe a virtual-currency exchange, gambling purchase, or a payment-exclusive wall. The final edit disputes authorship and the claim about speaking with other players, but it does not remove the explicitly described in-game purchasing and ball-depletion behavior from the text being coded.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: Repeated capture failures consume Poké Balls and the reviewer explicitly describes purchasing more as necessary to continue making captures.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a2ece36d-c527-442d-8f18-9a16b63994c8` - War Robots Multiplayer Battles

> Its a p2w game. The only time you enjoy it is when you're new. As you progress, everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game. If you want to progress without paying money, goodluck! Even if you wanted to do f2p, you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it. Plus the only time you benofit by getting f2p rewards is ads... 💩

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `M_PayToProgress`, `M_PowerCreep`, `T_Advertisement` |
| pred | `M_PayToProgress`, `M_PowerCreep`, `S_Competition`, `T_Advertisement` |
| **missed** | `M_EasyToPurchase` |
| **spurious** | `S_Competition` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a monetized competitive progression system. It says progression and competitive viability are tied to spending money, especially purchasing the newest bot rather than earning it. The reference to a shifting meta implies that older bots lose value as newer ones become necessary to remain competitive, which supports power creep. The multiplayer-battle context and the need to keep up with the meta also describe competition against other players. Finally, the review says free-to-play rewards are obtained through ads, indicating incentivized advertisement viewing. The recurring purchase offers shown at login are described as intrusive, but the review does not establish accidental purchases, misleading interface controls, artificial scarcity, or a mandatory payment gate to dismiss them.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "If you want to progress without paying money, goodluck!"
  - why: The review states that progressing without spending money is effectively unavailable, making payment a condition for progress.
- `M_PowerCreep` - ok
  - span: "shifting meta where you have to buy the newest bot with money instead of earning it"
  - why: The shifting meta and required newest bot imply that existing bots lose competitive value over time, driving purchases of newer bots.
- `S_Competition` - **SPURIOUS**
  - span: "keep up with shifting meta"
  - why: In the stated multiplayer-battle context, keeping up with the meta implies competing against other players.
- `T_Advertisement` - ok
  - span: "the only time you benofit by getting f2p rewards is ads"
  - why: The span links free-to-play rewards to watching advertisements, describing incentivized ad viewing.

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
The review describes repeated bingo rounds being used to obtain missing photos for a collection, which is repetitive progress activity. It also describes an in-game offer after a loss that asks the player to spend coins to obtain a missing photo and complete the set, matching payment being promoted as a way to advance. The missing promised photo is reported as a failure of the offer, but the review does not identify a separate coded mechanic such as a bug or chance-based purchase. The search was used only to verify that Bingo Blitz supports real-money purchases of virtual items; it did not establish that the specific coins in this review were purchased with real money.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "spend extra coins to claim a photo I don't have to complete the set"
  - why: The game presents spending currency as a way to obtain a missing collection item and advance toward completion.
- `P_CompleteTheCollection` - ok
  - span: "to complete the set"
  - why: The photos form a set that the player is trying to complete.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The reviewer repeatedly plays bingo rounds to make collection progress.

**Search:** `Bingo Blitz coins purchase real money photos collection` -> The official Bingo Blitz support page confirms that the game allows real-money purchases of virtual items, including random items, but it does not establish that the specific coins mentioned in the review were bought with real money. ([bingoblitz.com](https://www.bingoblitz.com/support/?utm_source=openai))

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b93c432d-19c0-4c6c-a2d4-bb9b21a436f3` - Dice Dreams™️

> A literal brain-rot game no wonder why they're tryna promote it through Free Cash. Also if you're thinking of making in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates! A real SCAM. Play it if u want but there are games that are actually good also, DON'T GET IN-APP PURCHASES!

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_Gambling`, `M_PayToProgress`, `P_CompleteTheCollection`, `P_EasyToGetHardToLose` |
| **missed** | `P_AestheticManipulation`, `P_RewardMania` |
| **spurious** | `M_Gambling`, `M_PayToProgress`, `P_EasyToGetHardToLose` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes an in-game album collection with two missing cards and a grand prize for completion. The player bought an in-app deal specifically to obtain those missing cards, so the purchase functioned as a route toward progress. The near-completed album also appears to have discouraged abandoning the goal and prompted the purchase. The deal promised NEW cards but delivered duplicates; one search was used to confirm that Dice Dreams uses purchasable album-card packs with chance-based outcomes and type-specific “new” guarantees. The mention of promotion through Free Cash is third-party advertising and is excluded under R13. ([support.dicedreams.com](https://support.dicedreams.com/hc/en-us/articles/24098716134163-I-was-assured-a-Guaranteed-NEW-Sticker-but-I-received-a-duplicate-Why))
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates!"
  - why: The player paid for a card-reward deal whose outcome was not the promised missing card and instead produced duplicates.
- `M_PayToProgress` - **SPURIOUS**
  - span: "I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards"
  - why: The reviewer bought an in-app deal to obtain the remaining cards needed to advance toward album completion and its grand prize.
- `P_CompleteTheCollection` - ok
  - span: "completing an album"
  - why: The album is an explicit collection that the player is trying to complete by obtaining its remaining cards.
- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "I had two cards left which would grant me the grand prize for completing an album, so i bought a deal"
  - why: Being only two cards from the completion reward made the partially completed album difficult to abandon and led the reviewer to spend money.

**Search:** `Dice Dreams album card packs duplicates deal new cards` -> Dice Dreams’ official help pages identify album stickers/cards as purchasable packs with variable odds and explain that “NEW” guarantees are type-specific, which can result in duplicates when the relevant type is already complete. ([support.dicedreams.com](https://support.dicedreams.com/hc/en-us/articles/24098716134163-I-was-assured-a-Guaranteed-NEW-Sticker-but-I-received-a-duplicate-Why))

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (6)

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
The review describes a friend-invitation reward mechanic: the player invites friends and gets them to join Facebook in exchange for rewards, although the rewards have stopped appearing after the new season began. It also describes luck-dependent gameplay outcomes, including betting dice for possible shutdowns or bank heists and receiving duplicate stickers, indicating unpredictable reward results. The inability to log in is explicitly attributed to an internet connection error, so it is a technical fault and does not support a dark-pattern label. The review does not explicitly describe repetitive tasks, real-money spending, daily rewards, collection completion pressure, or competition. No external search was needed.
```

**Labels assigned**

- `P_RewardMania` - ok
  - span: "when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way..."
  - why: The span describes luck-dependent, unpredictable outcomes for dice-based events and sticker rewards, including repeated duplicate results.
- `S_ForcedFellowship` - ok
  - span: "no rewards for inviting friends and getting them to join facebook"
  - why: The game uses rewards to motivate the player to bring friends into a connected social activity.

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

- `M_Gambling` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a current interface behavior in which opening the game or entering 1v1 automatically scrolls to and selects the highest-stakes table available from the player's coin balance. This steers the player toward the most expensive wagering option and makes an unintended bet possible. The reviewer also says that losing the coins leaves players needing to purchase replacement coins, which describes real-money acquisition of in-game currency. The requested lowest-table default is only a suggestion and is not coded.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "players lose all their hard-earned coins and are forced to buy real ones."
  - why: The span contrasts earned in-game coins with purchasing replacement coins, implying real-money acquisition of the game's currency.
- `M_UIMisdirection` - ok
  - span: "Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins."
  - why: Automatically steering players to the highest possible bet table directs attention and selection toward the costly option.

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
The review describes a daily-reward system that was changed so players must wager 50,000 in-game currency to complete and collect the daily rewards. It also mentions timed rewards, but does not describe an arbitrary waiting timer or a requirement to play at a particular clock time. The reward requirement is a gate on daily rewards, not evidence of real-money payment, repetitive grinding, or gambling under this codebook because the review does not state that the wager uses real money or that the reward outcome is chance-based.
```

**Labels assigned**

- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The game provides daily rewards and requires the player to complete a daily wagering condition to obtain them, penalizing failure to meet that condition by withholding the rewards.

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
The review describes a monetized progression and collection system. It states that winning rewards requires spending hundreds of dollars, which is a pay-to-progress/pay-to-win mechanic. It also describes sticker collections whose final one or two items are effectively withheld unless the player pays a large amount, which both makes collection completion the objective and indicates manufactured scarcity tied to payment. The comments about addiction, hopes, and the coerced five-star rating are evaluations or out-of-game review behavior, not additional in-game mechanics. No external search was needed because the described mechanics are clear from the review.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "you will never get the last one or two unless you pay a lot of money to get them."
  - why: The game allegedly withholds the final stickers and makes them obtainable only through a large payment, turning artificial scarcity into a reason to spend.
- `M_PayToProgress` - ok
  - span: "if you want to win anything on this game it will cost hundreds of dollars."
  - why: The review explicitly says that winning anything requires spending hundreds of dollars.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two"
  - why: The sticker system is presented as a collection whose final missing items determine whether the set is complete.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `73423b22-395c-49ed-8fc3-488a0b7680df` - MONOPOLY GO!

> I like the game but frustrating when it comes to getting stickers. always get duplicates. never lets you finish all the sets unless you pay

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury`, `M_PayToProgress`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_PayToProgress`, `P_CompleteTheCollection` |
| **missed** | `M_DeceptiveLuxury`, `P_RewardMania` |

**Did the model consider what it missed?**

- `M_DeceptiveLuxury` - never mentioned -> **attention / recall**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a sticker-collection mechanic in which obtaining stickers often produces duplicates, while the goal is to finish all the sets. This supports Complete the Collection because the player is pursuing complete sets. The review also explicitly says that completing the sets is unavailable unless the player pays, which supports Pay to Progress. The duplicate outcome alone does not establish a gacha, gambling, variable-reward, or grinding mechanic because the acquisition method and repetition requirement are not specified.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: Completion of the sticker sets is explicitly presented as unavailable unless the player pays.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: The reviewer describes a goal of acquiring enough stickers to complete every collection set.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `727cc804-9d4b-48ef-8774-2799a2a8de08` - Genshin Impact

> with every incoming patch, we get less and less rewards and for me that wouldn't be a problem but the Meta changes more and more every single day basically forcing us to pull for new characters if we want to actually do damage. the game is getting more and more pay 2 win and the quality of the game is becoming lower. in the new archon quest when we were talking to mavuika, a multi billion dollar company just put an insanely bad picture of Natlans scenery as the background, y'all can do better.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_PowerCreep`, `P_RewardMania` |
| pred | `M_PayToProgress`, `M_PowerCreep` |
| **missed** | `P_RewardMania` |

**Did the model consider what it missed?**

- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes two functional monetization and progression mechanics. First, changing meta balance makes newer characters necessary for effective damage, which implies that older or previously adequate characters lose practical value and players are driven toward new purchases or pulls. This supports Power Creep. Second, the reviewer explicitly characterizes the game as increasingly pay to win, describing paid character acquisition as a route to combat advantage and progress. The complaints about reduced rewards and poor scenery quality are not themselves dark-pattern mechanics.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "the game is getting more and more pay 2 win"
  - why: The review explicitly describes monetization as providing gameplay advantages, linking payment with the ability to perform effectively.
- `M_PowerCreep` - ok
  - span: "the Meta changes more and more every single day basically forcing us to pull for new characters if we want to actually do damage"
  - why: Successive meta changes make newer characters necessary for effective damage, implying that the practical value of existing characters is being diminished to drive new pulls.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (9)

### `95ddadb3-82cd-4042-8a51-cf8b3ed164c2` - Mech Arena - Shooting Game

> You stuck waiting 30 seconds just to connect to a match. This game makes it seem like they give so many rewards but if all just for show. Its difficult to get weapon upgrades or any percs others you stick battling to win. This kind of games just rob you of your time in my opinion

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `S_Competition`, `T_Grinding` |
| **spurious** | `S_Competition`, `T_Grinding` |

**Model analysis**

```
The review describes a 30-second matchmaking connection delay, but this is a service or matchmaking wait rather than a designed timer that forces the player to play at a scheduled time, so it does not support Playing by Appointment. The review also says that obtaining weapon upgrades and perks requires continuing to battle for wins, implying repeated gameplay to make progress, which supports Grinding. The match battles are competitive encounters, supporting Competition. The claim that rewards are merely for show expresses dissatisfaction with the reward presentation but does not explicitly describe an identified dark-pattern mechanic.
```

**Labels assigned**

- `S_Competition` - **SPURIOUS**
  - span: "you stick battling to win"
  - why: Battling to win in a match describes the player competing against other players.
- `T_Grinding` - **SPURIOUS**
  - span: "Its difficult to get weapon upgrades or any percs others you stick battling to win"
  - why: The reviewer links obtaining upgrades and perks to continuing battles for wins, implying repetitive gameplay is required for progress.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `0347fbc7-5c01-452e-ae4b-867f5bd7dd47` - Homescapes

> I really enjoy this (very) addicting and fun game. The levels get harder, but its fun to beat after a while. I only have a few suggestions; maybe only 5-10 minutes for a new life, not as many small and unnecessary tasks like celebrating and just because you miss a day doesnt mean that you need to start over on your daily prizes. But overall, I would recommend this game to anyone and the creators did a very good job on this game.👍

| | labels |
|---|---|
| gold | `T_DailyRewards`, `T_PlayingByAppointment` |
| pred | `S_FearOfMissingOutFOMO`, `T_DailyRewards`, `T_PlayingByAppointment` |
| **spurious** | `S_FearOfMissingOutFOMO` |

**Model analysis**

```
The review describes three active design behaviours. First, the request for a shorter time for a new life implies that lives are replenished through an in-game waiting timer; the requested 5–10 minute duration itself is only a suggestion, not a separate mechanic. Second, the game includes daily prizes that reset when the player misses a day, which both penalizes missed attendance and pressures the player to return daily. The mention of small tasks such as celebrating does not establish repetitive tasks required for progress, so it does not support Grinding.
```

**Labels assigned**

- `S_FearOfMissingOutFOMO` - **SPURIOUS**
  - span: "just because you miss a day doesnt mean that you need to start over on your daily prizes"
  - why: Resetting daily-prize progress when a day is missed pressures the player to keep returning so they do not lose progress and rewards.
- `T_DailyRewards` - ok
  - span: "just because you miss a day doesnt mean that you need to start over on your daily prizes"
  - why: Daily prizes are tied to daily attendance, and missing a day causes the reward sequence to restart.
- `T_PlayingByAppointment` - ok
  - span: "maybe only 5-10 minutes for a new life"
  - why: The request for a shorter time for a new life implies that the existing life system makes the player wait before playing again.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `66698c5c-8577-46fe-b796-8e93ad782166` - Teen Patti GOLD: 3 Patti Rummy

> Finally you forced me to uninstall the game. Forced notifications to give you permission to my contact list, for what? Is this a game or data collecting app?why I am bound to give you that permission? Better to keep you as spam app.

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `S_FriendSpamImpersonation` |
| **spurious** | `S_FriendSpamImpersonation` |

**Model analysis**

```
The review describes the game forcing the player to grant access to their contact list, apparently through a notification or permission prompt. This is an in-game request to access the player's social graph, which matches the Friend Spam / Impersonation indicator for using access to a contact list. The review does not explicitly say that messages were actually sent to contacts, so the label rests on the access behavior rather than confirmed spam transmission. The statement that the app is a spam app is evaluative and does not add another label.
```

**Labels assigned**

- `S_FriendSpamImpersonation` - **SPURIOUS**
  - span: "Forced notifications to give you permission to my contact list"
  - why: The game is described as forcing the player to grant access to their contact list, which is access to the player's social graph.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `21021f9a-e106-4e51-b01d-3fe4a4c941fc` - MONOPOLY GO!

> Deleted the game now. The latest event I was about to get 525 dice as reward, I had 3 left to go and I ran out of dice, it said 2Days left. Now just logged in after sleeping and the event is now changed. Deleting this game and what an absolute waste of time. Never purchased anything coz i have trust issues with F2P model games, and my gutt was right all along. Fun when it lasted, but that was a low blow.

| | labels |
|---|---|
| gold | `T_PlayingByAppointment` |
| pred | `S_FearOfMissingOutFOMO`, `T_PlayingByAppointment` |
| **spurious** | `S_FearOfMissingOutFOMO` |

**Model analysis**

```
The review describes a time-limited event with a reward of 525 dice and a progress goal that was nearly complete. The reviewer ran out of dice while only three steps remained, saw a displayed two-day timer, and then found after sleeping that the event had already changed. This means the game ties access to the reward to its own event schedule and pressures the player to keep playing before the event rotates, creating a fear of missing the reward. The review does not explicitly describe paying to replenish dice, daily rewards, repetitive grinding, or a technical fault.
```

**Labels assigned**

- `S_FearOfMissingOutFOMO` - **SPURIOUS**
  - span: "The latest event I was about to get 525 dice as reward, I had 3 left to go and I ran out of dice, it said 2Days left. Now just logged in after sleeping and the event is now changed."
  - why: The nearly completed 525-dice reward disappeared when the reviewer stopped playing, exemplifying fear of missing out on a limited event reward.
- `T_PlayingByAppointment` - ok
  - span: "it said 2Days left. Now just logged in after sleeping and the event is now changed."
  - why: The event's availability is controlled by the game's schedule, so stopping to sleep results in the event being replaced.

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
The review describes a base-building game with a grind-oriented progression loop, explicitly calling it a "grinder." It also describes an event presented as a competition, where an ordinary player allegedly has no realistic chance to win. The reviewer attributes success in that event to spending rather than skill, explicitly calling the game pay-to-win and reporting a total spend of 30k to win the event. The review does not describe gambling, purchase-interface friction, recurring fees, daily rewards, or a specific time-based appointment mechanic.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Zero skill pay to win"
  - why: The review states that spending money, rather than skill, provides the advantage needed to win.
- `S_Competition` - ok
  - span: "there is absolutely no opportunity for a general player to win an event"
  - why: The span describes an in-game event structured around players competing to win.
- `T_Grinding` - **SPURIOUS**
  - span: "Same old same old grinder"
  - why: The reviewer explicitly characterizes the game's progression as a grinder, describing repetitive gameplay as its defining structure.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b2dc0bc8-8ebe-4c48-bc05-38d0d65acb84` - Last War:Survival Game

> It's a nice game, but it's set up in a pay to win way. I played for 10 days, and the update times for your base are becoming ridiculous. Everything scales endlessly, there is kinda no point to look forward to, just more grind. The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff. Alliances are also weird, with the top ones dictating what to develop, what to rush, etc. If you are not in one then you get attacked and bullied. Not a great experience.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_UIMisdirection`, `S_Competition`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| pred | `M_PayToProgress`, `M_UIMisdirection`, `S_Competition`, `S_ForcedFellowship`, `T_Grinding`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| **spurious** | `S_ForcedFellowship`, `T_Grinding` |

**Model analysis**

```
The review describes several current game mechanics. Progression is framed as pay-to-win, meaning spending money provides gameplay advantages. Base updates use increasingly long timers, imposing waits before progression can continue. The reviewer also describes endlessly scaling progression and continuing grind with no meaningful endpoint, which indicates an infinite treadmill and grinding. The interface is said to be deliberately confusing and overwhelming in order to push purchases, supporting UI misdirection. Finally, alliance membership is practically compelled because players outside alliances are attacked and bullied; the alliance system also creates hostile interaction between players or groups, supporting forced fellowship and competition. No external search was needed because the mechanics are clear from the review.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "set up in a pay to win way"
  - why: The reviewer explicitly describes a design where spending money grants gameplay advantages.
- `M_UIMisdirection` - ok
  - span: "The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff."
  - why: The interface is explicitly described as deliberately confusing and overwhelming to steer players toward purchases.
- `S_Competition` - ok
  - span: "the top ones dictating what to develop, what to rush, etc. If you are not in one then you get attacked and bullied."
  - why: The alliance system places players and groups in hostile opposition, including attacks against players outside alliances.
- `S_ForcedFellowship` - **SPURIOUS**
  - span: "If you are not in one then you get attacked and bullied."
  - why: The threat of being attacked and bullied makes alliance membership practically compulsory.
- `T_Grinding` - **SPURIOUS**
  - span: "just more grind"
  - why: The reviewer characterizes ongoing progression as grind, implying repetitive effort is required to advance.
- `T_InfiniteTreadmill` - ok
  - span: "Everything scales endlessly, there is kinda no point to look forward to, just more grind."
  - why: The reviewer describes endlessly scaling progression with no meaningful completion point.
- `T_PlayingByAppointment` - ok
  - span: "the update times for your base are becoming ridiculous"
  - why: Base updates are governed by increasingly long timers that delay continued progression.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `32c623b4-0249-469e-968c-94f60c7fe3c2` - Royal Match

> It's an interesting game but the developers should pls try to include new cards in every card pack because I noticed when one is almost close to completing a set, new cards don't appear again especially when the set is almost expiring. So after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion because they don't add new sets to the cards once the collection is about to end.

| | labels |
|---|---|
| gold | `P_CompleteTheCollection`, `T_PlayingByAppointment` |
| pred | `P_CompleteTheCollection`, `S_FearOfMissingOutFOMO`, `T_PlayingByAppointment` |
| **spurious** | `S_FearOfMissingOutFOMO` |

**Model analysis**

```
The review describes a card-collection system in which players collect cards from packs to complete sets and earn a completion reward. It explicitly describes substantial partial collection progress—125 cards—but says that new cards stop appearing when a set is close to expiring, making completion impossible and causing the reward to be missed. The expiration creates a game-defined deadline that pressures completion before the collection ends and produces fear of missing the reward. The review does not describe payment, paid chance, daily login requirements, or abandoning an investment, so those patterns are not assigned.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion"
  - why: The review describes collecting cards toward completion of a set and pursuing the reward for completing the collection.
- `S_FearOfMissingOutFOMO` - **SPURIOUS**
  - span: "you will miss the reward for the set completion"
  - why: The expiring collection creates the possibility of missing an important in-game reward, pressuring players to keep trying to complete it.
- `T_PlayingByAppointment` - ok
  - span: "when the set is almost expiring"
  - why: The set has a game-imposed expiration point, so players must complete it before the scheduled end or lose the completion opportunity.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `7b564746-b769-4856-b686-529f8717c3ba` - Candy Crush Soda Saga

> I like the game except: 1. I was charged 10 gold pcs for 5 moves, I had 2 moves left. I had 7 moves but only used 1 move. 2. I paid for a pkg unlimited lives ect. I got the etc. but not the lives. 3. The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone. 4. You cannot win enough gold to play without buying sometimes. 5. The packages need to cost less. 6. When I buy pkg should not be timed.

| | labels |
|---|---|
| gold | `M_IntermediateCurrency`, `M_PayToProgress`, `T_PlayingByAppointment` |
| pred | `M_IntermediateCurrency`, `M_PayToProgress`, `S_FearOfMissingOutFOMO`, `T_PlayingByAppointment` |
| **spurious** | `S_FearOfMissingOutFOMO` |

**Model analysis**

```
The review describes several current mechanics. Gold is an in-game currency that can be earned or bought, and the reviewer says purchasing is sometimes necessary to keep playing; spending gold also buys extra moves, so progression/play is monetized. Timed bonuses continue expiring while the player is away, and paid packages are also described as timed, creating a schedule-based pressure to use them before they disappear and a risk of missing rewards. The missing lives after purchasing a package is described as a delivery or technical fault, so it does not independently trigger a dark-pattern label under R11. The request for cheaper packages is only an evaluation of price.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: Gold is described as an in-game currency that can be won or acquired through buying, indicating real-world spending to obtain currency used for play.
- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The reviewer states that continuing to play sometimes requires buying rather than earning enough gold through gameplay.
- `S_FearOfMissingOutFOMO` - **SPURIOUS**
  - span: "I go to bed with bonuses to wake up with them almost gone or gone."
  - why: The player loses rewards by stopping play and risks missing out because the bonuses expire during the absence.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing."
  - why: The bonuses run on a real-time game timer, requiring the player to use them according to the game's schedule rather than whenever they choose.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `440bffdc-ba8d-42d3-b7fc-af289deb1e22` - Last Z: Survival Shooter

> I read a couple of good jokes in the review summaries: "not a deceptive game", "free-to-play friendly". Incredible. First off, this game is nothing like what's advertised: it's a base growth simulator teeming with micro transaction menus. I still decided to play for a couple months, since the game does look good, which takes us to the second lie. Look: very soon, after a certain point, players are encouraged to attack each other, and there's a huge gap between p2w and f2p. Extremely frustrating.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `S_Competition` |
| pred | `M_PayToProgress`, `P_AestheticManipulation`, `S_Competition` |
| **spurious** | `P_AestheticManipulation` |

**Model analysis**

```
The review mentions misleading advertising and promotional claims, but those are outside the game application and are excluded by R13. Within the game, the reviewer describes a base-growth design with microtransaction menus, but does not provide enough detail to assign a specific currency, purchase-friction, payment-gating, or grinding label. The reviewer says the game's appearance kept them playing for months, which indicates an aesthetically appealing design influencing continued engagement. The game later encourages players to attack one another, establishing player-versus-player competition. The stated gap between pay-to-win and free-to-play players indicates that spending money provides gameplay advantages, matching Pay to Progress. No web search was needed.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "there's a huge gap between p2w and f2p"
  - why: The contrast between pay-to-win and free-to-play players implies that spending provides an in-game advantage.
- `P_AestheticManipulation` - **SPURIOUS**
  - span: "I still decided to play for a couple months, since the game does look good"
  - why: The game's appealing appearance is described as the reason the reviewer continued playing.
- `S_Competition` - ok
  - span: "players are encouraged to attack each other"
  - why: The game encourages direct conflict between players.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `P_RewardMania` | 5 | 0 |
| `M_PayToProgress` | 2 | 3 |
| `S_FearOfMissingOutFOMO` | 0 | 4 |
| `P_IllusionOfControl` | 3 | 0 |
| `S_Competition` | 1 | 2 |
| `P_AestheticManipulation` | 2 | 1 |
| `M_Gambling` | 2 | 1 |
| `T_Grinding` | 0 | 3 |
| `S_Reciprocity` | 2 | 0 |
| `S_FriendSpamImpersonation` | 1 | 1 |
| `M_EasyToPurchase` | 2 | 0 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `T_MandatoryMarathon` | 1 | 0 |
| `M_WasteAversion` | 1 | 0 |
| `S_ForcedFellowship` | 0 | 1 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `T_PlayingByAppointment` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |
| `M_IntermediateCurrency` | 1 | 0 |

