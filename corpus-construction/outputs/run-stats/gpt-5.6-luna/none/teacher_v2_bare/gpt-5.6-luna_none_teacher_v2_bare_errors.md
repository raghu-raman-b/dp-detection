# Error review - gpt-5.6-luna_none_teacher_v2_bare

`gpt-5.6-luna` / reasoning `` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_bare.txt` sha `ecd3c1810cf2`  
micro-F1 **0.684** (P 0.788 / R 0.605) - **27 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 6 | said NONE, gold had labels |
| SWAP | 8 | picked different labels than gold |
| MISSED ONLY | 9 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 4 | found all gold, added extras |

## The diagnostic that matters

Of **34** missed labels, **6** (18%) were named in the model's own analysis and dropped anyway; **28** (82%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `P_RewardMania` | 0 | 4 |
| `P_IllusionOfControl` | 2 | 1 |
| `S_Reciprocity` | 0 | 3 |
| `S_Competition` | 1 | 2 |
| `M_IntermediateCurrency` | 0 | 3 |
| `P_AestheticManipulation` | 0 | 2 |
| `M_Gambling` | 1 | 1 |
| `M_EasyToPurchase` | 1 | 1 |
| `T_PlayingByAppointment` | 0 | 2 |
| `M_PowerCreep` | 0 | 1 |
| `S_FriendSpamImpersonation` | 0 | 1 |
| `M_PayToProgress` | 1 | 0 |
| `T_MandatoryMarathon` | 0 | 1 |
| `T_Grinding` | 0 | 1 |
| `S_ForcedFellowship` | 0 | 1 |
| `M_WasteAversion` | 0 | 1 |
| `M_DeceptiveLuxury` | 0 | 1 |
| `S_EncouragesAntiSocialBehavior` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |

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
The review consists entirely of requests for hypothetical or additional features: auctions using in-game currency, changing the obstacle-decoration interaction, an account-switching and upgrade-timer widget, and access to advanced troop statistics. It does not describe any currently present game mechanic that matches a codebook label. Under R12, the proposed features are not codable.
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
The reviewer reports technical malfunctions after an update: repeated crashing prevents opening gifts and trading, lag prevents throwing Poké Balls and disrupts battles, switching and charge attacks respond slowly, and the game freezes while the opponent continues attacking. These are bugs, lag, and freezes rather than deliberate game design behaviors. The references to gifts, trading, catching, PvP, and Rocket battles provide context for the malfunctions but do not explicitly describe any codable dark-pattern mechanic.
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
The review describes a technical malfunction after an update: the player can no longer request troops from their clan. The loss of this social interaction is explicitly attributed to something that needs to be fixed, so it is a bug rather than a deliberate game design mechanic. No codebook label applies.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `5e6a5625-5291-4f0e-897c-1b63c1a26494` - MONOPOLY GO!

> I loved this game until the new season started. Suddenly I get no rewards for inviting friends and getting them to join facebook. I am struggling to get dices and when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way... And today. Well, I cannot log in to the game at all. It keeps giving me an internet connection error which is absolute nonsense. I have connected to 3 different wifi connections. BS!!😡

| | labels |
|---|---|
| gold | `M_Gambling`, `P_RewardMania`, `S_ForcedFellowship` |
| pred | _NONE_ |
| **missed** | `M_Gambling`, `P_RewardMania`, `S_ForcedFellowship` |

**Did the model consider what it missed?**

- `M_Gambling` - considered and rejected -> **rule interpretation**
- `P_RewardMania` - never mentioned -> **attention / recall**
- `S_ForcedFellowship` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes several outcomes but does not clearly establish a currently active dark-pattern mechanic. The phrase about inviting friends and getting them to join Facebook refers to a reward mechanic that the reviewer says has stopped working in the new season; under R12, a mechanic described as no longer present is not coded. Difficulty obtaining dice is resource scarcity without an identified coded mechanic. The lack of Shut downs, bank heists, and non-duplicate stickers describes unfavorable or possibly random outcomes, but it does not explicitly establish real-money gambling, a gacha system, collection compulsion, or another listed pattern. The inability to log in is explicitly attributed to an internet connection error, so it is a technical fault and does not trigger a dark-pattern label under R11. Therefore, no label is supported.
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
The review mainly describes misleading advertising for pin-pull and mini-game content, which is out-of-game marketing and therefore out of scope under R13. The reviewer also reports paying for extra coins and experiencing connection problems after updates, but does not describe payment as required for progress or a deliberate purchase mechanic; the connection issue is attributed to a technical fault, which R11 excludes. No codable in-app dark-pattern mechanic is explicitly described.
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
The reviewer describes a resource-loss problem on leaving and returning to the game: a full bag is empty on return, and both earned and purchased coins are gone or spent. The text does not clearly establish that this is an intentional game rule rather than a bug or technical fault, and it does not explicitly say that leaving a session forfeits progress by design. No label is therefore supported under the requirement to code a clear current mechanic.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Swapped labels (8)

### `fd1230ab-7d12-4aeb-a425-e37ed06bcd5c` - Pokémon GO

> I love this game, just started playing about 2 months ago. Though I have noticed since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more. I thought maybe its just me but I've talk to several pokemon players and they feel the same way. I feel taken advantage of. 3 stars editing this Review I DID NOT WRITE THIS REVIEW.....I DIDN'T TALK TO SEVERAL PLAYERS BECAUSE I DO NOT KNOW ANYONE

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| pred | `M_Gambling` |
| **missed** | `P_IllusionOfControl`, `P_OptimismAndFrequencyBiases`, `S_FriendSpamImpersonation` |
| **spurious** | `M_Gambling` |

**Did the model consider what it missed?**

- `P_IllusionOfControl` - never mentioned -> **attention / recall**
- `P_OptimismAndFrequencyBiases` - never mentioned -> **attention / recall**
- `S_FriendSpamImpersonation` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes purchasing Poké Balls, using them for capture attempts, and having Pokémon repeatedly break out so the consumable items are depleted and more must be purchased. The capture outcome is chance-based, and real-money purchases supply repeated attempts for the possibility of obtaining a Pokémon. The later edit disputes authorship and the claim about speaking with other players, but it does not identify a bug or technical fault in the capture mechanic, so the described purchase-and-chance pattern remains codable.
```

**Labels assigned**

- `M_Gambling` - **SPURIOUS**
  - span: "since I started purchasing, items "poke" balls that when I tried to make a capture that they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: The player purchases consumable Poké Balls to make repeated chance-based capture attempts, with the possibility of receiving a Pokémon as the reward.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `fdef27f2-9a21-4b8e-a04c-7a4753e0fb07` - 8 Ball Pool

> The game is great, but the user interface is completely rigged. Every time you open the game or go to the 1v1 section, it automatically scrolls and selects the highest possible bet table based on your coins. This is a cheap "Dark UX" trick to force accidental mis-clicks so players lose all their hard-earned coins and are forced to buy real ones. ​We need a "Default Table Lock" or the game should always open the lowest bet table by default, not the highest! Fix this scammy feature. Giving 1 star

| | labels |
|---|---|
| gold | `M_Gambling`, `M_IntermediateCurrency`, `M_UIMisdirection` |
| pred | `M_IntermediateCurrency`, `M_UIMisdirection`, `S_Competition` |
| **missed** | `M_Gambling` |
| **spurious** | `S_Competition` |

**Did the model consider what it missed?**

- `M_Gambling` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a UI behavior in which opening the game or entering the 1v1 area automatically scrolls to and selects the highest-stakes table available. This directs the player toward the most expensive betting option and can cause accidental high wagers that deplete their coins. The reviewer also says that, after losing those coins, players are forced to buy more with real money, which describes conversion of real money into in-game currency. The 1v1 section is a competitive game mode, but the review does not describe social pressure or manipulation between players. The requested lowest-table default is hypothetical and is not coded.
```

**Labels assigned**

- `M_IntermediateCurrency` - ok
  - span: "are forced to buy real ones"
  - why: After the in-game coins are lost, the review describes acquiring replacement coins through real-world spending.
- `M_UIMisdirection` - ok
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins"
  - why: The interface purposefully directs the player toward the highest-stakes option instead of a neutral or safer default.
- `S_Competition` - **SPURIOUS**
  - span: "go to the 1v1 section"
  - why: A 1v1 section explicitly places players in competition against one another.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `33c422de-1a84-4df9-accd-cdf8bfc96295` - Dark War Survival

> No ingenuity for a base builder. Same old same old grinder. After a few weeks, it became abundantly clear that there is absolutely no opportunity for a general player to win an event. Zero skill pay to play. Zero skill pay to win. Calculated total spent on last event was 30k to win. Wish serious gamers would stop perpetuating the problem by continuing to spend obnoxious amounts of money on a little app that you just want to have a little fun on.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `S_Competition` |
| pred | `M_PayToProgress`, `T_Grinding` |
| **missed** | `S_Competition` |
| **spurious** | `T_Grinding` |

**Did the model consider what it missed?**

- `S_Competition` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a repetitive base-building experience, explicitly calling it a grinder. It also describes an event whose outcome is effectively inaccessible to ordinary players unless they spend money, with the reviewer claiming that 30k was spent to win the last event. The event framing implies competitive progression, but the review does not explicitly state that players compete against one another, so Competition is not assigned. The phrases about pay to play and pay to win are treated as the described monetized access and advantage mechanic, with the concrete event-spending account supporting Pay to Progress.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "there is absolutely no opportunity for a general player to win an event. Zero skill pay to play. Zero skill pay to win. Calculated total spent on last event was 30k to win."
  - why: Winning the event is portrayed as requiring or being determined by substantial spending, giving paying players the decisive advantage.
- `T_Grinding` - **SPURIOUS**
  - span: "Same old same old grinder"
  - why: The reviewer explicitly characterizes the game as a grinder, describing repetitive gameplay rather than skill-based progression.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b2dc0bc8-8ebe-4c48-bc05-38d0d65acb84` - Last War:Survival Game

> It's a nice game, but it's set up in a pay to win way. I played for 10 days, and the update times for your base are becoming ridiculous. Everything scales endlessly, there is kinda no point to look forward to, just more grind. The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff. Alliances are also weird, with the top ones dictating what to develop, what to rush, etc. If you are not in one then you get attacked and bullied. Not a great experience.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `M_UIMisdirection`, `S_Competition`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| pred | `M_PayToProgress`, `M_UIMisdirection`, `S_ForcedFellowship`, `T_Grinding`, `T_InfiniteTreadmill`, `T_PlayingByAppointment` |
| **missed** | `S_Competition` |
| **spurious** | `S_ForcedFellowship`, `T_Grinding` |

**Did the model consider what it missed?**

- `S_Competition` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes several current game mechanics. It explicitly characterizes the game as pay-to-win, indicating that spending money grants gameplay advantages. Base upgrades use increasingly long or excessive update timers, imposing waits on progress. The reviewer also describes endlessly scaling content and continuing grind with no meaningful endpoint, which indicates an infinite treadmill and repetitive progression work. The UI is described as deliberately confusing and overwhelming in order to push purchases; this is UI misdirection because the interface is being used to steer player attention and decision-making toward buying. Finally, alliance participation appears socially enforced: top alliances dictate development choices, while players outside alliances are attacked and bullied. This makes alliance membership a condition for avoiding in-game harm and supports Forced Fellowship. No web search was needed because all referenced mechanics are identifiable from the review itself.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "it's set up in a pay to win way"
  - why: The review explicitly states that the game grants gameplay advantages through spending, which is the Pay to Win instance of Pay to Progress.
- `M_UIMisdirection` - ok
  - span: "The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff"
  - why: The interface is intentionally made confusing and overwhelming to steer players toward purchasing.
- `S_ForcedFellowship` - **SPURIOUS**
  - span: "If you are not in one then you get attacked and bullied"
  - why: Players are pressured to join an alliance because remaining outside one exposes them to attacks and bullying.
- `T_Grinding` - **SPURIOUS**
  - span: "just more grind"
  - why: The reviewer identifies ongoing progression as grind, indicating repetitive work required to advance.
- `T_InfiniteTreadmill` - ok
  - span: "Everything scales endlessly, there is kinda no point to look forward to, just more grind"
  - why: Endlessly scaling progression with no meaningful endpoint describes a game structure that continually extends rather than allows completion.
- `T_PlayingByAppointment` - ok
  - span: "the update times for your base are becoming ridiculous"
  - why: Base development is gated by increasingly excessive in-game update timers, requiring the player to wait before progress can continue.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `ab2097d3-2f9b-4a87-885c-25dfcddb5a70` - Gardenscapes

> Have been playing this game since COVID 19 lockdown. It was fun back then. Currently at 8416 and it gets frustratingly annoying after level 8000. I run out of lives 3-4 times daily to beat every alternate level, avg 5-7 days per level. You must buy add ons else you can't make it through a sane mind. it's pure time waste if you're not paying. Now I'm not interested anymore. Unistalling this game to invest some quality time in a real life. Wasted too much of money and time into this game.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `T_Grinding` |
| pred | `M_PayToProgress`, `P_EasyToGetHardToLose` |
| **missed** | `T_Grinding` |
| **spurious** | `P_EasyToGetHardToLose` |

**Did the model consider what it missed?**

- `T_Grinding` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a level-based progression system in which advancing becomes difficult and slow at high levels: they report taking an average of 5–7 days per level and repeatedly running out of lives. They explicitly state that buying add-ons is necessary to get through the game, so payment is being used to progress. The reviewer also says they have invested substantial money and time and now finds uninstalling difficult or regrettable, which supports the invested-value form of Easy to Get, Hard to Lose. The text does not clearly describe repetitive tasks, timers, daily rewards, or an impossible-to-complete game, so those labels are not assigned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through"
  - why: The review explicitly says purchasing add-ons is required to make progress through the game.
- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "Wasted too much of money and time into this game."
  - why: The reviewer identifies substantial accumulated time and money investment, which makes abandoning the game costly or difficult.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `32c623b4-0249-469e-968c-94f60c7fe3c2` - Royal Match

> It's an interesting game but the developers should pls try to include new cards in every card pack because I noticed when one is almost close to completing a set, new cards don't appear again especially when the set is almost expiring. So after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion because they don't add new sets to the cards once the collection is about to end.

| | labels |
|---|---|
| gold | `P_CompleteTheCollection`, `T_PlayingByAppointment` |
| pred | `P_CompleteTheCollection`, `P_EasyToGetHardToLose`, `S_FearOfMissingOutFOMO` |
| **missed** | `T_PlayingByAppointment` |
| **spurious** | `P_EasyToGetHardToLose`, `S_FearOfMissingOutFOMO` |

**Did the model consider what it missed?**

- `T_PlayingByAppointment` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a card-collection mechanic in which the player tries to complete a set and earn its completion reward. Near the end of the collection period, card packs stop providing needed new cards, leaving the player with an incomplete set despite having collected 125 cards. The expiring collection creates a risk of missing the reward, which pressures completion before the event ends. The text does not explicitly describe payment, gambling, ads, daily login requirements, or a deliberate scarcity tactic tied to purchases.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok  _[span not verbatim]_
  - span: "after one is almost close to completing a set, new cards don't appear again"
  - why: The mechanic centers on acquiring all cards needed to complete a collection set.
- `P_EasyToGetHardToLose` - **SPURIOUS**
  - span: "after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion"
  - why: The player has accumulated substantial progress toward a partially completed goal, making the lost completion reward and prior investment salient.
- `S_FearOfMissingOutFOMO` - **SPURIOUS**
  - span: "you will miss the reward for the set completion"
  - why: The expiring collection creates pressure through the possibility of missing an important completion reward.

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
The review describes a collection goal involving photos and a set that the player wants to complete. Progress requires playing repetitive bingo rounds, described as playing round after round. After losing a round, the game prompts the player to spend extra coins to obtain a missing photo, making payment a route to progress toward completing the set. Although the reviewer says the promised photo is not delivered, the text does not clearly establish that this is a chance-based paid reward, a currency exchange purchased with real money, or a technical bug, so those labels are not assigned.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "spend extra coins to claim a photo I don't have to complete the set"
  - why: The game offers spending coins as a way to obtain a missing collection item and advance toward completing the set.
- `P_CompleteTheCollection` - ok
  - span: "a photo I don't have to complete the set"
  - why: The game presents a collection set with a missing photo, and the player is pursuing completion of that set.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The player describes repeating bingo rounds to make progress toward collecting photos.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b93c432d-19c0-4c6c-a2d4-bb9b21a436f3` - Dice Dreams™️

> A literal brain-rot game no wonder why they're tryna promote it through Free Cash. Also if you're thinking of making in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates! A real SCAM. Play it if u want but there are games that are actually good also, DON'T GET IN-APP PURCHASES!

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_PayToProgress`, `P_CompleteTheCollection` |
| **missed** | `P_AestheticManipulation`, `P_RewardMania` |
| **spurious** | `M_PayToProgress` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes an album-collection system in which the player was two cards short of completing an album and receiving its grand prize. The player then purchased a deal specifically to obtain new cards, making payment a means of advancing toward completion. The deal promised new cards but delivered duplicates instead; this is a deceptive purchase outcome, but the codebook has no general label for false item guarantees without an explicit chance mechanic, artificial scarcity, or misleading purchase interface. The mention of promotion through Free Cash concerns out-of-game advertising and is excluded by R13.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "so i bought a deal which promised i would get NEW cards"
  - why: The player spent money to obtain missing cards and advance toward completing the album.
- `P_CompleteTheCollection` - ok
  - span: "I had two cards left which would grant me the grand prize for completing an album"
  - why: The player is pursuing the remaining cards needed to complete an album and obtain its completion reward.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (9)

### `5f3e71b5-200c-45a3-b90e-e08b0dc0e1a3` - Cash Frenzy™ - Casino Slots

> Is a good game, but I will like to place my formal complain about the genie game, in multiple times whe the wheel spin after stopping on a great price the genie move the wheel to a spin tag, and then the prices after the spin are way lower than the original price, from 100 million with 5x multiplier to a 48 million. Is the only part I don't like. There should be a player choice to keep or spin.

| | labels |
|---|---|
| gold | `P_IllusionOfControl`, `P_RewardMania` |
| pred | `P_RewardMania` |
| **missed** | `P_IllusionOfControl` |

**Did the model consider what it missed?**

- `P_IllusionOfControl` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a wheel-based reward mechanic in the Genie game. After the wheel appears to stop on a high-value prize, the game overrides that result by moving the wheel to a second spin, which can produce a substantially lower reward. This is an unpredictable reward sequence and therefore supports Reward Mania through variable rewards. The review does not state that real money is used for the wheel, so Gambling is not assigned. The override is unfair, but it does not clearly meet Illusion of Control because the review does not say the mechanic misrepresents the player's skill.
```

**Labels assigned**

- `P_RewardMania` - ok
  - span: "in multiple times whe the wheel spin after stopping on a great price the genie move the wheel to a spin tag, and then the prices after the spin are way lower than the original price"
  - why: The wheel produces an apparently favorable outcome and then forces another unpredictable spin that can replace it with a much lower reward.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `0bc09fc3-6436-4a24-855e-0fdc56887918` - Fishdom

> EDIT 1/17/2023: Customer Service can't make good on 9 diamonds when game element doesn't appear within 5 original moves and 5 additional moves. It is a fun game, you don't have to pay to win. I suggest after this cust. svc experience that you don't buy from this game beyond the pass.Get friends and a team and trade lives.

| | labels |
|---|---|
| gold | `M_RecurringFee`, `S_Reciprocity` |
| pred | `M_RecurringFee` |
| **missed** | `S_Reciprocity` |

**Did the model consider what it missed?**

- `S_Reciprocity` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a conditional diamond compensation involving a game element that fails to appear within 5 original moves plus 5 additional moves, but it attributes the failure to a game element not appearing and focuses on customer-service handling, so no dark-pattern label follows from that incident. The reviewer also explicitly refers to purchasing a pass; the search established that Fishdom uses a time-limited Gold Pass, which is a battle-pass mechanic covered by Recurring Fee. The mention of friends, a team, and trading lives describes social interaction and resource exchange, but does not state an obligation to reciprocate, recruitment rewards, or pressure from teammates.
```

**Labels assigned**

- `M_RecurringFee` - ok
  - span: "you don't buy from this game beyond the pass"
  - why: The reviewer identifies Fishdom's pass as a purchasable battle-pass product, which is explicitly included under Recurring Fee.

**Search:** `Fishdom game "the pass" diamonds customer service` -> The search established that Fishdom's pass refers to its Gold Pass, a time-limited pass with additional rewards.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `549e5e94-9b59-477d-88c7-ae5e00d62514` - Disney Solitaire

> it was fine at the start but further along into the game the rng is so obviously against you it's crazy.. it's not rewarding playing the game without spending actual money.. at around level 100 it costs 2200 but if you win the level you'll barely make that back.. the rewards need a big revamp for me.. let down by alot of things with this game the further into it you get.. sort it out

| | labels |
|---|---|
| gold | `M_PayToProgress`, `P_IllusionOfControl` |
| pred | `M_PayToProgress` |
| **missed** | `P_IllusionOfControl` |

**Did the model consider what it missed?**

- `P_IllusionOfControl` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a progression economy that becomes unfavorable later in the game. Around level 100, completing a level costs 2200 while the reward barely replenishes that cost, and the reviewer says playing without spending real money is not rewarding. This implies that continued progress is made easier or effectively sustained through monetary spending, supporting Pay to Progress. The complaint that RNG is against the player describes perceived unfair randomness, but it does not explicitly establish that the game hides information or manipulates the player's sense of skill, so Illusion of Control is not assigned. No gambling mechanic, recurring fee, currency exchange, grinding task, or explicit completion-ending treadmill is described.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "it's not rewarding playing the game without spending actual money"
  - why: The review links continued play or progression to spending real money, implying that monetary payment is needed to make later progress viable.

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

- `M_PayToProgress` - considered and rejected -> **rule interpretation**
- `M_WasteAversion` - never mentioned -> **attention / recall**

**Model analysis**

```
The reviewer describes a daily-reward system that was changed so the rewards cannot be completed unless the player places a 50,000 bet. The game also has timed rewards, but the review does not clearly describe their reset schedule or a requirement to watch advertisements. The explicit daily schedule and the inability to obtain the daily rewards without performing the required activity support Daily Rewards. The betting requirement does not establish Gambling because the review does not say that real money is used, and it does not establish Pay to Progress because the 50,000 appears to be an in-game bet rather than a payment.
```

**Labels assigned**

- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000 with out it I can't complete my daily rewards"
  - why: The game provides daily rewards but makes obtaining or completing them contingent on performing a required in-game activity.

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
The review describes monetized progression and collection completion. Winning or obtaining the final stickers is portrayed as requiring very large real-money payments, including hundreds of dollars, so progress is gated or substantially enabled by spending. The sticker album also creates a completion goal centered on obtaining the last missing items. The statement that the last one or two stickers will never be obtained unless the player pays a lot suggests manufactured scarcity tied to payment, supporting Deceptive Luxury through the artificial-scarcity indicator. The low chance of completing a goal does not by itself establish grinding, gambling, or an infinite treadmill because the underlying mechanic is not specified.
```

**Labels assigned**

- `M_DeceptiveLuxury` - ok
  - span: "you will never get the last one or two unless you pay a lot of money to get them"
  - why: The final stickers are portrayed as deliberately unavailable through ordinary play and obtainable only through expensive payment, implying manufactured scarcity used to drive spending.
- `M_PayToProgress` - ok
  - span: "if you want to win anything on this game it will cost hundreds of dollars"
  - why: The review says that achieving wins requires spending substantial real-world money, describing paid advantage or progress.
- `P_CompleteTheCollection` - ok
  - span: "on the stickers you will never get the last one or two"
  - why: The reviewer describes pursuing completion of a sticker collection, specifically the final missing items.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `a2ece36d-c527-442d-8f18-9a16b63994c8` - War Robots Multiplayer Battles

> Its a p2w game. The only time you enjoy it is when you're new. As you progress, everytime you log in, your screen has spam of so called "good deals" in which I mean in app purchases before you can actually play your game. If you want to progress without paying money, goodluck! Even if you wanted to do f2p, you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it. Plus the only time you benofit by getting f2p rewards is ads... 💩

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `M_PayToProgress`, `M_PowerCreep`, `T_Advertisement` |
| pred | `M_PayToProgress`, `T_Advertisement` |
| **missed** | `M_EasyToPurchase`, `M_PowerCreep` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - considered and rejected -> **rule interpretation**
- `M_PowerCreep` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes monetized progression: the reviewer says progress without paying is effectively unavailable, and that keeping up with the game's changing competitive meta requires buying the newest bot rather than earning it. The newest bot purchase also grants a gameplay advantage, supporting pay-to-progress through the codebook's combined pay-to-skip/pay-to-win definition. The game repeatedly presents in-app purchase offers on login before play, but the review does not describe a specific purchase-default, accidental-purchase, or attention-directing UI behavior, so Easy to Purchase and UI Misdirection are not assigned. It also states that free-to-play rewards are obtained through ads, which describes incentivized advertising. I am not assigning Competition or FOMO merely from the game's multiplayer context or the phrase 'keep up,' because the review does not explicitly describe competing players or fear of missing rewards.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it"
  - why: The reviewer describes needing to purchase the newest bot with real money to maintain gameplay-relevant progress and competitive viability.
- `T_Advertisement` - ok
  - span: "the only time you benofit by getting f2p rewards is ads"
  - why: The span links free-to-play rewards to watching advertisements, describing rewarded or incentivized ad viewing.

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
The review describes repetitive resource gathering as the main route to leveling up, which directly supports Grinding. It also describes alliances attacking one another and taking resources, an explicit player-versus-player competitive mechanic supporting Competition. The reference to an advertisement concerns external marketing rather than gameplay, so it is out of scope under R13. The reviewer’s investment of time in the game and alliances does not by itself establish that the design makes quitting difficult, and the review does not describe daily rewards, forced social obligations, payment mechanics, or mandatory play sessions.
```

**Labels assigned**

- `S_Competition` - ok
  - span: "The bigger alliances all just attack the smaller alliances and take their resources"
  - why: The game places alliances against one another in direct competition over resources.
- `T_Grinding` - ok
  - span: "It's just grinding resources trying not to get raided so you can level up"
  - why: The player must repeatedly gather resources to make progress and level up, which is performing repetitive tasks for advancement.

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
The review describes a sticker-collection system in which the player receives duplicate stickers and cannot complete all sticker sets without paying. The duplicates indicate difficulty completing the collection, but do not by themselves establish gambling or a random-reward mechanic. The explicit payment gate supports Pay to Progress, and the goal of finishing all sets supports Complete the Collection.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: The review explicitly states that completing the game's sets requires payment, making progress contingent on spending money.
- `P_CompleteTheCollection` - ok
  - span: "finish all the sets"
  - why: The player is pursuing completion of a collection of sticker sets.

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
The review describes three actionable game mechanics. First, the player must buy or spend paid resources to obtain extra moves and sometimes to keep playing, which is Pay to Progress. Second, timed bonuses continue expiring while the player is offline, forcing the player to organize play around the game's countdown schedule, which is Playing by Appointment. The missing lives from a purchased package is described as a fulfillment problem rather than a deliberate design choice, so it is excluded under R11. The requests for cheaper packages and untimed purchases do not label hypothetical changes; only the existing timed package behavior is considered, but its timing alone does not establish a separate listed monetary pattern.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The review states that continuing to play sometimes requires buying, making payment a condition for progress or continued play.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing."
  - why: Bonuses expire according to an in-game timer while the player is absent, pressuring the player to play within the game's time window.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (4)

### `95ddadb3-82cd-4042-8a51-cf8b3ed164c2` - Mech Arena - Shooting Game

> You stuck waiting 30 seconds just to connect to a match. This game makes it seem like they give so many rewards but if all just for show. Its difficult to get weapon upgrades or any percs others you stick battling to win. This kind of games just rob you of your time in my opinion

| | labels |
|---|---|
| gold | _NONE_ |
| pred | `T_Grinding` |
| **spurious** | `T_Grinding` |

**Model analysis**

```
The review describes a 30-second matchmaking connection delay, but this is an operational matchmaking wait rather than an in-game timer or scheduled play requirement, so it does not trigger Playing by Appointment. The reviewer also says weapon upgrades and perks are difficult to obtain and that the player must keep battling to win them. This implies repeated gameplay is required to make progression toward those upgrades, which supports Grinding. The claims that rewards are “just for show” and that the game wastes time are evaluative and do not independently identify another coded mechanic.
```

**Labels assigned**

- `T_Grinding` - **SPURIOUS**
  - span: "Its difficult to get weapon upgrades or any percs others you stick battling to win."
  - why: The span indicates that the player must continue battling repeatedly to obtain weapon upgrades or perks, making repetitive gameplay the route to progress.

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
The review describes the game forcing the player to grant access to their contact list, apparently as a condition associated with notifications. It does not explicitly say that the game actually sends messages or invitations to those contacts, so the supported mechanic is the game's attempt to obtain access to the player's contact list. The statement that it is a spam app is an evaluation and does not add another label.
```

**Labels assigned**

- `S_FriendSpamImpersonation` - **SPURIOUS**
  - span: "give you permission to my contact list"
  - why: The game is described as requiring access to the player's contact list, which is an explicit contact-list access behavior covered by this label.

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
The reviewer describes a time-limited event with a reward of 525 dice. They were three objectives short, had no dice left, and expected to have two more days to finish, but after sleeping and logging in again the event had changed. This indicates that access to the event and its reward is governed by the game's schedule rather than the player's preferred stopping and returning time, supporting Playing by Appointment. It also creates a fear of missing the reward or falling behind when the event changes unexpectedly. The review does not explicitly describe buying dice, a purchase prompt, repetitive grinding, daily rewards, or a technical bug, so those are not coded.
```

**Labels assigned**

- `S_FearOfMissingOutFOMO` - **SPURIOUS**
  - span: "I had 3 left to go and I ran out of dice, it said 2Days left. Now just logged in after sleeping and the event is now changed."
  - why: The player was close to earning a large reward but risked losing it by stopping, and the event's change meant the reward opportunity was missed.
- `T_PlayingByAppointment` - ok
  - span: "it said 2Days left. Now just logged in after sleeping and the event is now changed."
  - why: The reviewer expected to return within the displayed two-day period, but the game changed the event after the player stopped and slept, making the game's schedule determine when the event could be played.

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
The review describes a very long quest that provides almost no primogem reward, but this is a complaint about poor reward quantity rather than a clearly described repetitive task, unpredictable reward structure, or progression gate. The character-design criticism is aesthetic opinion and does not describe psychological manipulation. The concrete game mechanic is the absence of resin overflow: Original Resin is a capped, regenerating resource, so without an overflow or reserve it must be spent before reaching the cap or later regeneration is wasted. That makes players return according to the resource timer rather than solely according to their own schedule. The five years of play establishes tenure but does not explicitly say that accumulated investment makes quitting difficult.
```

**Labels assigned**

- `T_PlayingByAppointment` - **SPURIOUS**
  - span: "there is no resin overflow system"
  - why: The lack of overflow makes resource use time-sensitive and encourages players to return and spend Resin according to the game's regeneration schedule.

**Search:** `Genshin Impact resin overflow system` -> The search established that Original Resin is a capped resource that regenerates over time, while an overflow or reserve system would store excess Resin beyond the cap; therefore, the review's statement describes a time-sensitive resource design.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `S_Competition` | 3 | 1 |
| `P_RewardMania` | 4 | 0 |
| `T_Grinding` | 1 | 3 |
| `P_IllusionOfControl` | 3 | 0 |
| `S_Reciprocity` | 3 | 0 |
| `M_PayToProgress` | 1 | 2 |
| `M_Gambling` | 2 | 1 |
| `T_PlayingByAppointment` | 2 | 1 |
| `M_IntermediateCurrency` | 3 | 0 |
| `S_FriendSpamImpersonation` | 1 | 1 |
| `P_AestheticManipulation` | 2 | 0 |
| `P_EasyToGetHardToLose` | 0 | 2 |
| `M_EasyToPurchase` | 2 | 0 |
| `S_FearOfMissingOutFOMO` | 0 | 2 |
| `S_ForcedFellowship` | 1 | 1 |
| `M_PowerCreep` | 1 | 0 |
| `T_MandatoryMarathon` | 1 | 0 |
| `M_WasteAversion` | 1 | 0 |
| `M_DeceptiveLuxury` | 1 | 0 |
| `S_EncouragesAntiSocialBehavior` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |

