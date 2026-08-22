# Error review - gpt-5.6-luna_low_teacher_v2_bare

`gpt-5.6-luna` / reasoning `low` / search `True`  
prompt `/home/prex_san/Documents/dp-detection/corpus-construction/outputs/prompts/teacher_v2_bare.txt` sha `ecd3c1810cf2`  
micro-F1 **0.662** (P 0.868 / R 0.535) - **27 of 50** reviews disagree

| pattern | n | meaning |
|---|---|---|
| FALSE NONE | 8 | said NONE, gold had labels |
| SWAP | 4 | picked different labels than gold |
| MISSED ONLY | 14 | everything predicted was right, but incomplete |
| SPURIOUS ONLY | 1 | found all gold, added extras |

## The diagnostic that matters

Of **40** missed labels, **7** (18%) were named in the model's own analysis and dropped anyway; **33** (82%) never came up at all.

> Named-then-dropped is **rule interpretation**: fix prompt wording (R9) or the codebook boundary rule.  
> Never-named is **attention**: raise reasoning effort, or split the label list (the 1+4 cascade). Prompt wording will not help.

| label | named then dropped | never named |
|---|---|---|
| `P_RewardMania` | 1 | 5 |
| `P_IllusionOfControl` | 1 | 2 |
| `S_Reciprocity` | 0 | 3 |
| `M_PayToProgress` | 0 | 3 |
| `T_PlayingByAppointment` | 1 | 2 |
| `M_IntermediateCurrency` | 0 | 3 |
| `P_AestheticManipulation` | 0 | 2 |
| `M_Gambling` | 1 | 1 |
| `M_EasyToPurchase` | 1 | 1 |
| `M_DeceptiveLuxury` | 0 | 2 |
| `M_PowerCreep` | 1 | 0 |
| `S_FriendSpamImpersonation` | 0 | 1 |
| `S_Competition` | 0 | 1 |
| `P_EasyToGetHardToLose` | 0 | 1 |
| `T_Advertisement` | 1 | 0 |
| `T_MandatoryMarathon` | 0 | 1 |
| `M_UIMisdirection` | 0 | 1 |
| `T_Grinding` | 0 | 1 |
| `M_WasteAversion` | 0 | 1 |
| `S_EncouragesAntiSocialBehavior` | 0 | 1 |
| `P_OptimismAndFrequencyBiases` | 0 | 1 |

## Missed everything (predicted NONE) (8)

### `0853c395-2040-4e0b-a56c-1591484cd35b` - Clash of Clans

> 10/10, but we would like: 1.) Bids & auctions for decorations, skins and sceneries with in-game currency. 2.) Remove the option to remove an obstacle if you've turned it into a decoration. 3.) Widget that can toggle various accounts and see how much time is left for upgrades. 4.) Hidden option for troops' advanced statistics.

| | labels |
|---|---|
| gold | `T_PlayingByAppointment` |
| pred | _NONE_ |
| **missed** | `T_PlayingByAppointment` |

**Did the model consider what it missed?**

- `T_PlayingByAppointment` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review primarily requests additions or changes: auctions using in-game currency, removing an existing option, a widget showing upgrade timers and account switching, and access to advanced troop statistics. These are suggestions rather than descriptions of manipulative mechanics currently operating in the game. The mention of an option to remove a decorated obstacle and a hidden statistics option does not, by itself, establish a coded dark pattern such as UI misdirection, pay-to-progress, or playing by appointment.
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
The reviewer describes a prize-wheel mechanic in which, after the wheel appears to stop on a valuable reward, the genie forces or changes the outcome to another spin, producing a substantially lower prize. The review also requests a choice to keep the original result or spin again, but that is only a suggestion and not an existing mechanic. Although the game is a casino-themed slots game, the review does not state that real money is used for this wheel, so M_Gambling is not supported. The forced reroll and reduced reward do not clearly satisfy another listed label.
```

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b98d7e75-73da-4591-b23e-1a2951bfd856` - Township

> I like this game a lot, but recently after seeing the ads, there is no way to close it. No cross mark on the screen , if you try to click anywhere on the screen it takes you to store. If you go back to game it is still stuck in the last sceeen of the ad. You have to kill the game to come out of the ad screen , so frustrating!!!

| | labels |
|---|---|
| gold | `M_UIMisdirection`, `T_Advertisement` |
| pred | _NONE_ |
| **missed** | `M_UIMisdirection`, `T_Advertisement` |

**Did the model consider what it missed?**

- `M_UIMisdirection` - never mentioned -> **attention / recall**
- `T_Advertisement` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes an in-game advertisement that lacks a visible close control, redirects any tap to the store, remains on screen after returning to the game, and can only be exited by killing the game. This is an obstructive or malfunctioning ad interface, but the codebook has no label for deceptive ad-dismissal controls. The review does not state that ads are mandatory or reward-incentivized, so T_Advertisement is not supported. The inability to close the ad is presented as the ad screen being stuck, a technical malfunction, which does not trigger a dark-pattern label under R11.
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
The reviewer is requesting a possible save or account-preservation feature for progress and purchases after deleting the game. The concern that deletion would cause loss is framed as a suggestion and supported by what happened in other games, not as an explicitly described current mechanic of MadOut 2. The reviewer also says they would be more willing to spend money if such preservation existed, but this is hypothetical future behavior. Under R12, no current in-game dark pattern is established.
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
The reviewer describes being unable to request troops from their clan after an update, and explicitly says it needs to be fixed. This is attributed to a technical fault rather than a deliberate game design mechanic, so no dark-pattern label applies under R11.
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
- `P_IllusionOfControl` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes perceived unfavorable random outcomes, but it does not clearly establish a deliberate game mechanic that cheats or hides information about the player's skill, so P_IllusionOfControl is not supported. The statement that playing is not rewarding without spending actual money expresses dissatisfaction with the reward economy, but it does not explicitly say that payment is required for progress, that purchases grant an advantage, or that a specific currency obscures prices. The 2200 cost and barely recouped rewards are too unclear to assign a monetary or grinding label. No qualifying mechanic is explicitly described.
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
The reviewer reports that after leaving the game, their full bag is empty upon returning and both earned and purchased coins have been consumed. These are described as lost progress or resources caused by a malfunction or game error, rather than as an intentional mechanic. Under R11, technical faults do not trigger dark-pattern labels, and no separate intentional design behavior is explicitly described.
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
The review describes being stuck on level 195 for almost two months and refusing to pay for power-ups, but it does not explicitly state that payment is required to progress or that the power-ups are the only way forward. The proposed daily login rewards are a request for a feature, not an existing mechanic, so they cannot be coded. No listed label is supported by an explicit current game mechanic.
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
The review describes a consumable-item purchase loop: after purchasing Poké Balls, the reviewer says captures fail more often, causing the balls to be depleted faster and creating a need to purchase additional balls. This explicitly connects spending money on items with continuing capture-related progress. The later statement disputes the authorship of the review and the claimed conversations with other players, but it does not identify a technical malfunction in the game itself, so the described purchase mechanic remains codable.
```

**Labels assigned**

- `M_PayToProgress` - **SPURIOUS**
  - span: "they keep breaking out so I go through the balls faster so I have to purchase more"
  - why: The reviewer describes needing to buy additional Poké Balls to continue making captures, making spending a condition for capture-related progress.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `21021f9a-e106-4e51-b01d-3fe4a4c941fc` - MONOPOLY GO!

> Deleted the game now. The latest event I was about to get 525 dice as reward, I had 3 left to go and I ran out of dice, it said 2Days left. Now just logged in after sleeping and the event is now changed. Deleting this game and what an absolute waste of time. Never purchased anything coz i have trust issues with F2P model games, and my gutt was right all along. Fun when it lasted, but that was a low blow.

| | labels |
|---|---|
| gold | `T_PlayingByAppointment` |
| pred | `M_DeceptiveLuxury`, `S_FearOfMissingOutFOMO` |
| **missed** | `T_PlayingByAppointment` |
| **spurious** | `M_DeceptiveLuxury`, `S_FearOfMissingOutFOMO` |

**Did the model consider what it missed?**

- `T_PlayingByAppointment` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a time-limited event with a promised reward, partial progress toward that reward, and a visible countdown saying there were still two days remaining. After the player stopped playing and logged back in after sleeping, the event had been replaced despite the displayed time. This creates pressure to keep playing or risk missing the reward, supporting Fear of Missing Out. The event’s apparent limited availability and premature replacement also describe manufactured scarcity or urgency, supporting Deceptive Luxury. The review does not explicitly describe daily login rewards, repetitive grinding, payment requirements, or a mandatory session.
```

**Labels assigned**

- `M_DeceptiveLuxury` - **SPURIOUS**
  - span: "it said 2Days left. Now just logged in after sleeping and the event is now changed."
  - why: The game presented the event as available for two more days but replaced it after the player briefly stopped playing, creating manufactured scarcity around the reward.
- `S_FearOfMissingOutFOMO` - **SPURIOUS**
  - span: "The latest event I was about to get 525 dice as reward, I had 3 left to go and I ran out of dice, it said 2Days left. Now just logged in after sleeping and the event is now changed."
  - why: The player had nearly completed a reward-bearing event but feared losing the reward after stopping play, and the event changed before the displayed two-day period ended.

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
The review describes several active game mechanics. The game grants advantages through spending, explicitly framing progression as pay to win. Base upgrades use increasingly long timers, imposing waits on development. Progression continually scales without an apparent endpoint and requires more repetitive grinding. The interface is described as deliberately confusing and overwhelming in order to push purchases, which supports UI Misdirection because the interface is being used to steer players toward buying. Alliance participation is effectively coerced: stronger alliances dictate development choices and players outside alliances are attacked and bullied, making social affiliation necessary for safety and progress. The review does not explicitly describe daily rewards, gambling, a recurring fee, or a technical download deception.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "it's set up in a pay to win way"
  - why: The review explicitly states that spending provides an in-game advantage.
- `M_UIMisdirection` - ok
  - span: "The UI is deliberately confusing and overwhelming to achieve the effect that you need to buy stuff"
  - why: The interface is intentionally made confusing and overwhelming to steer players toward purchases.
- `S_ForcedFellowship` - **SPURIOUS**
  - span: "If you are not in one then you get attacked and bullied"
  - why: Being outside an alliance exposes the player to attacks and bullying, coercing alliance membership as a condition of safe participation.
- `T_Grinding` - **SPURIOUS**
  - span: "just more grind"
  - why: The reviewer explicitly characterizes continued progress as requiring grind.
- `T_InfiniteTreadmill` - ok
  - span: "Everything scales endlessly"
  - why: Endless scaling implies an indefinitely expanding progression system without a meaningful completion point.
- `T_PlayingByAppointment` - ok
  - span: "the update times for your base are becoming ridiculous"
  - why: Base updates are governed by increasingly long timers, requiring the player to wait before development completes.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `32c623b4-0249-469e-968c-94f60c7fe3c2` - Royal Match

> It's an interesting game but the developers should pls try to include new cards in every card pack because I noticed when one is almost close to completing a set, new cards don't appear again especially when the set is almost expiring. So after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion because they don't add new sets to the cards once the collection is about to end.

| | labels |
|---|---|
| gold | `P_CompleteTheCollection`, `T_PlayingByAppointment` |
| pred | `P_CompleteTheCollection`, `S_FearOfMissingOutFOMO` |
| **missed** | `T_PlayingByAppointment` |
| **spurious** | `S_FearOfMissingOutFOMO` |

**Did the model consider what it missed?**

- `T_PlayingByAppointment` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a card-collection system in which players gather cards toward completing sets. Near the end of a set's availability, new cards allegedly stop appearing, so the player can collect many cards yet fail to complete the set and lose its completion reward. The collection goal supports Complete the Collection. The expiring set and the explicitly missed reward also create pressure through fear of missing out. The review does not describe payment, currency, gambling, or a required play schedule beyond the limited collection period.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok  _[span not verbatim]_
  - span: "after one is almost close to completing a set, new cards don't appear again"
  - why: The review explicitly describes collecting cards to complete a set and treats failure to obtain the remaining cards as the central problem.
- `S_FearOfMissingOutFOMO` - **SPURIOUS**
  - span: "especially when the set is almost expiring. So after collecting 125 cards from the beginning of the collection you will miss the reward for the set completion"
  - why: The expiring set creates pressure because the player may miss the completion reward despite substantial progress.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Under-labelled (incomplete, nothing wrong) (14)

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
The review attributes the described problems to bugs, crashing, lag, freezing, and unresponsive controls. The gift opening and trading behavior is not described as a social obligation or unsolicited messaging. The PvP and Team GO Rocket battles explicitly involve fighting an opponent, which describes an in-game competition mechanic; the technical failures themselves do not trigger dark-pattern labels under R11.
```

**Labels assigned**

- `S_Competition` - ok
  - span: "the pvp & rockets battles are also lagging switching out are too slow, charge attacks are not responding well and my game freeze while the opponent keep attacking"
  - why: PvP and battles against an opponent explicitly describe players competing against other players or opponents.

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
The review describes a pass that the player can buy, which is an existing battle-pass mechanic and therefore supports Recurring Fee under the codebook. It also mentions friends, a team, and trading lives, but does not describe inviting friends, an obligation to keep playing for teammates, or feeling required to reciprocate, so no social label is supported. The statement that the player does not have to pay to win explicitly denies a pay-to-win mechanic rather than describing one. The diamonds and the game element are discussed in the context of customer-service resolution and do not establish a qualifying currency, gambling, or other dark-pattern mechanic.
```

**Labels assigned**

- `M_RecurringFee` - ok
  - span: "beyond the pass"
  - why: The review explicitly refers to an in-game pass that can be purchased, which is a battle-pass mechanic.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `5e6a5625-5291-4f0e-897c-1b63c1a26494` - MONOPOLY GO!

> I loved this game until the new season started. Suddenly I get no rewards for inviting friends and getting them to join facebook. I am struggling to get dices and when I finally had more than 500 dices and played max bet, absolutely NO LUCK! No Shut downs and no bank heists. Stickers are duplicates all the way... And today. Well, I cannot log in to the game at all. It keeps giving me an internet connection error which is absolute nonsense. I have connected to 3 different wifi connections. BS!!😡

| | labels |
|---|---|
| gold | `M_Gambling`, `P_RewardMania`, `S_ForcedFellowship` |
| pred | `S_ForcedFellowship` |
| **missed** | `M_Gambling`, `P_RewardMania` |

**Did the model consider what it missed?**

- `M_Gambling` - considered and rejected -> **rule interpretation**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a friend-invitation mechanic tied to rewards: the player invites friends and gets them to join Facebook in exchange for in-game rewards, although the reviewer says those rewards have stopped appearing after the new season. This uses the player's social connections to recruit others, supporting Forced Fellowship. The lack of dice, unsuccessful shut downs and bank heists, duplicate stickers, and the connection error do not by themselves establish another coded mechanic: the latter is explicitly a technical fault, and the review does not clearly state that real money is used for gambling or that the random outcomes come from a defined reward system.
```

**Labels assigned**

- `S_ForcedFellowship` - ok
  - span: "no rewards for inviting friends and getting them to join facebook"
  - why: The game links in-game rewards to recruiting friends and getting them to join Facebook, using the player's social connections as a recruitment mechanism.

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
The review describes an in-game interface that automatically scrolls to and selects the highest-stakes table whenever the game opens or the player enters the 1v1 section. This design directs the player toward the most expensive option and makes an accidental selection more likely, while the reviewer says the consequence is losing coins and then buying more currency with real money. The requested Default Table Lock and lowest-bet default are proposed fixes, not existing mechanics, so they are not coded. The accidental loss is of in-game coins rather than a real-money purchase, so M_EasyToPurchase is not assigned. The clearest supported pattern is UI Misdirection because the interface purposefully steers attention and selection toward the highest-bet table.
```

**Labels assigned**

- `M_UIMisdirection` - ok
  - span: "it automatically scrolls and selects the highest possible bet table based on your coins"
  - why: The interface automatically focuses and defaults the player onto the highest-cost betting option instead of leaving the player at a neutral or low-stakes choice.

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
The review describes an existing daily-reward system that requires the player to bet 50,000 in order to complete and claim the daily rewards. It also mentions timed rewards, but does not describe an arbitrary waiting timer that blocks play. The statement about not paying is the reviewer’s refusal, not evidence that payment is required, so no monetary label applies. The 50,000 betting requirement is a progress task, but the review does not establish repetitive or tedious activity strongly enough for Grinding.
```

**Labels assigned**

- `T_DailyRewards` - ok
  - span: "I can't get my daily rewards unless I bet 50,000"
  - why: The game provides daily rewards tied to completion of a required in-game condition, and the reviewer cannot obtain them without meeting that condition.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `cc714d17-863c-4ebd-b14f-989ba17c71c4` - Dice Dreams™️

> I played this game on a different profile. the only reason I gave it five stars is because if you don't it won't let you write a review. if you want to win anything on this game it will cost hundreds of dollars. on the stickers you will never get the last one or two unless you pay a lot of money to get them. this is not a game you want to get addicted to unless you have a endless bank account. it may let you complete a goal maybe one out of hundred times.dont get your hopes up.

| | labels |
|---|---|
| gold | `M_DeceptiveLuxury`, `M_PayToProgress`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `M_PayToProgress`, `P_CompleteTheCollection` |
| **missed** | `M_DeceptiveLuxury`, `P_RewardMania` |

**Did the model consider what it missed?**

- `M_DeceptiveLuxury` - never mentioned -> **attention / recall**
- `P_RewardMania` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes a sticker-collection progression system in which completing the collection is the player's goal, but the final one or two stickers are effectively withheld unless the player pays a large amount. It also broadly states that winning requires spending hundreds of dollars, indicating a monetary advantage or progression requirement. The statement that a goal succeeds only about one time in a hundred suggests a very low success rate, but it does not clearly identify a chance-based paid mechanic or an unpredictable reward structure, so Gambling and Reward Mania are not assigned. The review's comment about giving five stars concerns the review interface rather than a game mechanic and is out of scope.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "on the stickers you will never get the last one or two unless you pay a lot of money to get them"
  - why: The final stickers, and therefore completion of the collection, are described as unavailable unless the player pays a large amount.
- `P_CompleteTheCollection` - ok
  - span: "you will never get the last one or two"
  - why: The review identifies obtaining the final stickers as the relevant completion goal, showing pursuit of a complete item collection.

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

- `T_Grinding` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes a level-based game with limited lives: the player runs out of lives several times each day while trying to clear levels, and progression is very slow, averaging 5–7 days per level. The central monetization mechanic is that the reviewer says add-ons must be bought to continue through the levels, making payment a condition of progress. The review does not explicitly describe repetitive tasks, scheduled play requirements, a timer-based wait, or a mechanic that makes leaving difficult because of prior investment; statements about frustration, time waste, and dissatisfaction alone do not establish those labels.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You must buy add ons else you can't make it through"
  - why: The reviewer states that purchasing add-ons is necessary to get through the game's levels, making payment a condition of progress.

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
- `M_PowerCreep` - considered and rejected -> **rule interpretation**

**Model analysis**

```
The review describes several current in-game monetization mechanics. Progress is presented as effectively requiring payment, and a newer bot must be bought with money rather than earned, which supports Pay to Progress. The game repeatedly places in-app purchase offers on the screen at login before play, but the review does not describe a specific purchase-by-default, accidental-purchase, or attention-directing interface behavior, so Easy to Purchase and UI Misdirection are not supported. It also says free-to-play rewards are obtained through ads, indicating incentivized advertisements. The reference to a shifting meta and having to buy the newest bot suggests changing competitive viability, but it does not explicitly say that previously purchased items lose value over time, so Power Creep is not assigned.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "If you want to progress without paying money, goodluck! Even if you wanted to do f2p, you would not be able to keep up with shifting meta where you have to buy the newest bot with money instead of earning it."
  - why: The review states that progression and keeping up with the game's meta require purchasing the newest bot with real money rather than earning it.
- `T_Advertisement` - ok
  - span: "the only time you benofit by getting f2p rewards is ads"
  - why: The span links free-to-play rewards to advertisements, implying that ads are viewed or otherwise used as the condition for receiving those rewards.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `12267c1e-47ba-4984-97c8-768e820ceb1c` - Bingo Blitz™️ - Bingo Games

> not very user-friendly. no apparent reachable goals within a decent amount of time. I play round after round to collect 'photos', and after each round that I lose it will ask me if I want to spend extra coins to claim a photo I don't have to complete the set. I'll spend coins on said offer, I GET 2-3 BINGOS BUT STILL DONT GET THE OFFER/PHOTO I WAS PROMISED. What the hell? As of right now, this has happened to me so many times I can't even count. I'm done with the game. I've wasted so much money

| | labels |
|---|---|
| gold | `M_EasyToPurchase`, `P_AestheticManipulation`, `P_CompleteTheCollection`, `T_Grinding` |
| pred | `P_CompleteTheCollection`, `T_Grinding` |
| **missed** | `M_EasyToPurchase`, `P_AestheticManipulation` |

**Did the model consider what it missed?**

- `M_EasyToPurchase` - never mentioned -> **attention / recall**
- `P_AestheticManipulation` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes repeatedly playing bingo rounds to collect photos for a set, which is a collection-completion goal reached through repetitive play. After losing a round, the game presents an offer to spend extra coins to obtain a missing photo; however, the reviewer says that spending the coins does not produce the promised photo. The review does not clearly establish that the coins are bought with real money, that the offer is chance-based, or that the player is required to pay to continue, so monetary labels are not assigned. The failed offer is described as a deceptive or malfunctioning outcome, but no available label directly covers a broken promise of this kind.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "to complete the set"
  - why: The game goal is to acquire missing photos and complete an in-game collection.
- `T_Grinding` - ok
  - span: "I play round after round to collect 'photos'"
  - why: The reviewer describes performing repeated bingo rounds in order to make progress toward collecting photos.

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
The review describes repetitive resource collection as the main route to leveling: the player is “grinding resources” so they can level up and obtain more attempts at another game. It also describes alliances attacking one another, specifically larger alliances attacking smaller ones for resources, which is direct player-versus-player competition. The reference to dedicating time to the game and alliances expresses investment and disappointment, but does not explicitly say that leaving would forfeit accumulated value or let friends down, so it does not independently support Easy to Get, Hard to Lose or Forced Fellowship. The mention of an advertisement is not a clear description of an in-game mechanic and is outside scope if it refers to marketing.
```

**Labels assigned**

- `S_Competition` - ok
  - span: "The bigger alliances all just attack the smaller alliances and take their resources."
  - why: Alliances compete directly by attacking other alliances and taking their resources.
- `T_Grinding` - ok
  - span: "It's just grinding resources trying not to get raided so you can level up"
  - why: The reviewer explicitly describes repeatedly collecting resources to make leveling progress.

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
The review describes a sticker-collection system in which the player repeatedly receives duplicate stickers, making it difficult to complete all sticker sets. It also explicitly states that completing the sets is unavailable without payment, so payment is required for this progress. The duplicate outcome alone does not establish gambling because the review does not explicitly describe paid chance-based purchases or random paid rewards.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "never lets you finish all the sets unless you pay"
  - why: The review explicitly says finishing the sticker sets requires payment.
- `P_CompleteTheCollection` - ok
  - span: "getting stickers. always get duplicates. never lets you finish all the sets"
  - why: The player is pursuing completion of all sticker sets, and duplicate stickers obstruct completing the collection.

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
The review describes several mechanics. Gold is deducted to obtain extra moves, and the reviewer says progress sometimes cannot continue without buying, so spending is used to advance gameplay. A purchased unlimited-lives package failed to deliver the lives, but this is attributed to a missing purchase outcome rather than a deliberate game design, so it is not coded. Timed bonuses continue counting down while the player is asleep and not playing, imposing a game-controlled deadline and requiring play according to the timer. The complaint that packages should not be timed does not by itself establish a separate recurring-fee or limited-offer mechanic.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "You cannot win enough gold to play without buying sometimes."
  - why: The review states that gameplay sometimes cannot continue through earned resources alone and requires buying, making payment necessary for progress.
- `T_PlayingByAppointment` - ok
  - span: "The timed bonuses tick away even though I am not playing. I go to bed with bonuses to wake up with them almost gone or gone."
  - why: Bonuses expire according to an in-game timer while the player is absent, pressuring the player to return and play before the game-defined deadline.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

### `b93c432d-19c0-4c6c-a2d4-bb9b21a436f3` - Dice Dreams™️

> A literal brain-rot game no wonder why they're tryna promote it through Free Cash. Also if you're thinking of making in-app purchases DON'T DO IT. I had two cards left which would grant me the grand prize for completing an album, so i bought a deal which promised i would get NEW cards, and all i got were useless duplicates! A real SCAM. Play it if u want but there are games that are actually good also, DON'T GET IN-APP PURCHASES!

| | labels |
|---|---|
| gold | `P_AestheticManipulation`, `P_CompleteTheCollection`, `P_RewardMania` |
| pred | `P_CompleteTheCollection` |
| **missed** | `P_AestheticManipulation`, `P_RewardMania` |

**Did the model consider what it missed?**

- `P_AestheticManipulation` - never mentioned -> **attention / recall**
- `P_RewardMania` - never mentioned -> **attention / recall**

**Model analysis**

```
The review describes an album-completion system in which the player was two cards short of a grand prize and wanted to obtain those missing cards. It also describes an in-app purchase deal presented as providing new cards, followed by receiving duplicates instead. The album and grand prize support a collection-completion mechanic. The purchase was used in an attempt to advance that collection, but the review does not clearly establish that payment is required for progress or that the deal involves a chance-based draw, so Pay to Progress and Gambling are not assigned. The mention of promoting the game through Free Cash concerns out-of-game advertising and is excluded under R13.
```

**Labels assigned**

- `P_CompleteTheCollection` - ok
  - span: "two cards left which would grant me the grand prize for completing an album"
  - why: The player is pursuing the remaining cards needed to complete an album and receive its completion prize.

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
The review describes a changing competitive balance in which the meta shifts repeatedly and players are effectively pushed to obtain new characters to maintain damage output. This supports Power Creep because newer characters or the changing meta diminish the practical value of existing characters over time. It also explicitly describes the game as increasingly pay to win, meaning spending for characters provides an in-game advantage. The reduced rewards and declining visual quality are complaints, but they do not independently identify another coded mechanic.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "the game is getting more and more pay 2 win"
  - why: The review explicitly states that spending is increasingly tied to gaining an advantage in gameplay.
- `M_PowerCreep` - ok
  - span: "the Meta changes more and more every single day basically forcing us to pull for new characters if we want to actually do damage"
  - why: Repeated meta changes make existing characters less effective for dealing damage and pressure players toward newer character purchases.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## Over-labelled (1)

### `33c422de-1a84-4df9-accd-cdf8bfc96295` - Dark War Survival

> No ingenuity for a base builder. Same old same old grinder. After a few weeks, it became abundantly clear that there is absolutely no opportunity for a general player to win an event. Zero skill pay to play. Zero skill pay to win. Calculated total spent on last event was 30k to win. Wish serious gamers would stop perpetuating the problem by continuing to spend obnoxious amounts of money on a little app that you just want to have a little fun on.

| | labels |
|---|---|
| gold | `M_PayToProgress`, `S_Competition` |
| pred | `M_PayToProgress`, `S_Competition`, `T_Grinding` |
| **spurious** | `T_Grinding` |

**Model analysis**

```
The review describes a repetitive base-building experience, calling it a grinder and saying it is the same old pattern. It also describes an event in which ordinary players cannot win, while players can spend very large amounts of money to win; this is a competitive event whose outcome is influenced by spending. The review does not describe a payment gate required for ordinary progression, only spending for competitive advantage, so the supported monetary label is Pay to Progress through the Pay to Win indicator. No specific timer, daily login requirement, advertisement, collection mechanic, or technical malfunction is described.
```

**Labels assigned**

- `M_PayToProgress` - ok
  - span: "Zero skill pay to win."
  - why: The span explicitly describes spending money to obtain an advantage and win in the game.
- `S_Competition` - ok
  - span: "there is absolutely no opportunity for a general player to win an event"
  - why: The review describes players competing in an event with a winner.
- `T_Grinding` - **SPURIOUS**
  - span: "Same old same old grinder"
  - why: Calling the game a grinder describes repetitive, tedious gameplay used to make progress.

`[ ] under-label`  `[ ] over-label`  `[ ] confusion`  `[ ] codebook gap -> v0.21`  `[ ] gold was wrong`

---

## By label

| label | missed | spurious |
|---|---|---|
| `P_RewardMania` | 6 | 0 |
| `M_PayToProgress` | 3 | 1 |
| `P_IllusionOfControl` | 3 | 0 |
| `S_Reciprocity` | 3 | 0 |
| `T_Grinding` | 1 | 2 |
| `M_DeceptiveLuxury` | 2 | 1 |
| `T_PlayingByAppointment` | 3 | 0 |
| `M_IntermediateCurrency` | 3 | 0 |
| `P_AestheticManipulation` | 2 | 0 |
| `M_Gambling` | 2 | 0 |
| `M_EasyToPurchase` | 2 | 0 |
| `S_FearOfMissingOutFOMO` | 0 | 2 |
| `M_PowerCreep` | 1 | 0 |
| `S_FriendSpamImpersonation` | 1 | 0 |
| `S_Competition` | 1 | 0 |
| `P_EasyToGetHardToLose` | 1 | 0 |
| `T_Advertisement` | 1 | 0 |
| `T_MandatoryMarathon` | 1 | 0 |
| `M_UIMisdirection` | 1 | 0 |
| `M_WasteAversion` | 1 | 0 |
| `S_ForcedFellowship` | 0 | 1 |
| `S_EncouragesAntiSocialBehavior` | 1 | 0 |
| `P_OptimismAndFrequencyBiases` | 1 | 0 |

