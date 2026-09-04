# Prompt v3 — adjudicated worked examples

**Status: approved and built.** These 58 examples are now `codebook_versions/codebook_adjudicated.json` (v0.21) and render into `outputs/prompts/teacher_v3_full.txt`. This document is the review record; the machine-readable source is `codebook_versions/adjudicated_examples.json`.

Source: `corpus-construction/gold_set/gold_set.jsonl` (75 reviews, adjudicated panel labels, codebook v0.20) with spans and coder reasoning from the sidecar `gold_provenance_2026-09-04-06-38-46.json`.

58 examples: two per meso label, for all 29 labels. Each is shown in the shape the teacher model must emit, so an approved entry drops into `worked_examples[]` in the codebook and renders straight into the v3 prompt.

> **Revision 2.** `rule_applied` corrected on ten entries after review — see [Changes in this revision](#changes-in-this-revision). One gold-set label was added as a result; the gold files have been updated and the edit is logged in `gold_set/post_adjudication_edits.md`.

---

## How to read an entry

Each label gets two examples:

- **Apt** — the cleanest instance of the pattern in the gold set. Usually the canonical definition or a named indicator, high coder agreement, minimal inference. This is what the model should learn the label *is*.
- **Coverage** — an instance that extends the label somewhere the apt example does not reach: a second arm of the definition, a different indicator, a boundary rule that settled a near miss, an implied rather than stated mechanic, or an interaction with a global rule (R7/R8 valence, R11 bugs, R12 suggestions, R9 co-assignment). This is what the model should learn the label's *edges* are.

Every entry carries:

| field | meaning |
| --- | --- |
| **span** | Verbatim substring of the review text. All 58 verified programmatically against `review_text`. |
| **rule_applied** | The codebook material the label rests on. See the vocabulary below. |
| **rationale** | One line: why this span satisfies this label. Written to be reproducible by a model, not to cite literature. |
| **Also on this review** | The other codes the panel assigned. Included so the example does not teach under-labelling; the model still sees that the review is multi-label. |
| **Why this example** | Editorial note for you. This does **not** go into the prompt. |
| **Provenance** | Where the span came from and how many of the three coders assigned this label before adjudication. |

## The `rule_applied` vocabulary

Three forms only, matching the v2 output contract (`teacher_v2_full.txt`, OUTPUT section):

1. `definition` — the span meets the label's canonical definition directly.
2. An **indicator name**, copied verbatim from that label's own `indicators` list — e.g. `Wait to Play`, `Artificial Scarcity`, `First Charge Discount`, `Accidental Purchases`, `Exciting UI Effect`, `Social Pyramid Scheme`, `Invested (Endowed) Value`, `Gacha mechanics`, `Pay Wall`. Two indicators may combine (`Remedy Consumption + Artificial Scarcity`). Entries tagged `[dp-enhancer]` in the codebook, such as `Rarity Level`, sharpen a pattern but do not assign it on their own, so they never stand alone here.
3. A **boundary rule**, written `vs <vs_label>` exactly as the codebook names it — e.g. `vs Slow Progress`, `vs Alleged rigging`, `vs Free alternative`, `vs Purchase solicitation`.

**Two constraints on form 3,** both applied in this revision:

- A boundary rule may only be cited if it is listed under **this** label in the codebook. Rules are written from one side, so `vs Fear of missing out` belongs to Playing by Appointment and cannot be cited from FOMO's entry; `vs Optimism and Frequency Biases` belongs to Illusion of Control and cannot be cited from O&FB's entry.
- A boundary rule is cited only where it is what **settled a genuine near miss**. Most boundary rules say when *not* to apply a label; where the definition reaches the span directly, `rule_applied` is `definition` and the boundary is simply not in play.

Distribution across the 58: `definition` 24 · indicator 18 · boundary rule 16.

### A note on R10

One example rests on a web search: `M_IntermediateCurrency` coverage, where "top up" is not resolvable from the review text alone. Because `invoked_web_search` / `search_query` / `search_result` are review-level rather than label-level fields, that entry shows them in a second block below its label object. A draft query and result are supplied; swap in a real one from the cache if you would rather the prompt quote an actual search.

---

## Support summary

Pre-adjudication coder support for each chosen example. Low numbers are not errors — the panel ruled the label in — but they mark examples where the reading was contested.

| label | apt | coverage |
| --- | --- | --- |
| `T_PlayingByAppointment` | 3/3 | 3/3 |
| `T_DailyRewards` | 3/3 | 3/3 |
| `T_Grinding` | 3/3 | 2/3 |
| `T_Advertisement` | 3/3 | 3/3 |
| `T_InfiniteTreadmill` | 2/3 | 1/3 ⚠️ |
| `T_MandatoryMarathon` | 3/3 | 2/3 |
| `M_PayToProgress` | 3/3 | 3/3 |
| `M_IntermediateCurrency` | 3/3 | 2/3 |
| `M_DeceptiveLuxury` | 2/3 | 2/3 |
| `M_RecurringFee` | 3/3 | 3/3 |
| `M_Gambling` | 3/3 | 3/3 |
| `M_PowerCreep` | 3/3 | 3/3 |
| `M_WasteAversion` | 3/3 | 3/3 |
| `M_EasyToPurchase` | 3/3 | 2/3 |
| `M_UIMisdirection` | 3/3 | 3/3 |
| `M_NeverEndingLure` | 3/3 | 3/3 |
| `S_ForcedFellowship` | 3/3 | 3/3 |
| `S_FriendSpamImpersonation` | 3/3 | 2/3 |
| `S_Reciprocity` | 3/3 | 3/3 |
| `S_EncouragesAntiSocialBehavior` | 3/3 | 2/3 |
| `S_FearOfMissingOutFOMO` | 1/3 ⚠️ | 1/3 ⚠️ |
| `S_Competition` | 3/3 | 3/3 |
| `P_EasyToGetHardToLose` | 3/3 | 2/3 |
| `P_CompleteTheCollection` | 2/3 | 2/3 |
| `P_IllusionOfControl` | 3/3 | 2/3 |
| `P_AestheticManipulation` | 2/3 | 1/3 ⚠️ |
| `P_OptimismAndFrequencyBiases` | 3/3 | 3/3 |
| `P_RewardMania` | 2/3 | 2/3 |
| `Tech_FragmentedDownloads` | 3/3 | 3/3 |

⚠️ marks an example that only one of the three coders assigned before adjudication: `T_InfiniteTreadmill` coverage, `S_FearOfMissingOutFOMO` apt, `S_FearOfMissingOutFOMO` coverage, `P_AestheticManipulation` coverage. These sit on the labels with the thinnest gold-set support overall (2 instances each), so there was no higher-agreement alternative available. Worth a second look before approval.

---

## Temporal

### `T_PlayingByAppointment` — Playing by Appointment

> **Definition (codebook).** Requires players play at specific times (and or dates) as defined by the game, rather than the players. When mechanics result in player playing according to the schedules the game offers, rather than their personal desires (an obligation).

#### Apt — Last War:Survival Game

`f9424404-513f-41a9-a3b9-a97670e89512` · UK · 1★ · 2024-10-07

> This game demands constant attention and is definitely falsely advertised, though they just added some new screenshots to try and avoid chargebacks. They lure you in and then the pressure to login every 2-3 hours 24/7 is constant with Arms Race or keep it open all day long so you don't miss treasure digs. Competing=who spends the most. This is a gacha game and 4x. You've been warned.

```json
{
  "label": "T_PlayingByAppointment",
  "span": "login every 2-3 hours 24/7",
  "rule_applied": "definition",
  "rationale": "The game sets a 2-3 hour login cycle the player must keep to, so play happens on the game's schedule rather than the player's."
}
```

- **Also on this review:** `M_PayToProgress`, `S_FearOfMissingOutFOMO`, `S_Competition`, `P_RewardMania`
- **Why this example:** Cleanest reading of the canonical definition: an explicit clock the player must obey. No indicator or boundary needed.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

#### Coverage — Carrom Pool: Disc Game

`ab9a6418-85dc-4e82-a279-bab6e1e5e148` · IN · 1★ · 2025-02-24

> (1) The shooting time is too short. (2) The foul thing is unfair because if I put a chip into a pocket and I have a foul, it takes out 2 chips, not just the one I put inside. (3) The openning time for the chests is too long, 1 or 2 hours is fine, but 8 and 12 hours?!...come on! (4) The Practice option disappears when the game detects a network connection, should be available with it. (5) It's impossible to play when other players are using cheats, they do perfect shots in impossible situations.

```json
{
  "label": "T_PlayingByAppointment",
  "span": "The openning time for the chests is too long, 1 or 2 hours is fine, but 8 and 12 hours?!...come on!",
  "rule_applied": "Wait to Play",
  "rationale": "The span names an in-game timer and its length, which is the Wait to Play instance of this pattern."
}
```

- **Also on this review:** `S_Competition`
- **Why this example:** Reaches the same label through an indicator instead of the definition, and via a timer rather than a login schedule. Clears the 'vs Resource depletion without stated wait' boundary because the wait's duration is stated.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

### `T_DailyRewards` — Daily Rewards

> **Definition (codebook).** Motivates players to log in daily by providing incentives, while also penalising them for failing to do so.

#### Apt — Township

`50be85ac-f98c-4d2c-a70c-4465974027c0` · UK · 4★ · 2026-05-03

> Awesome game; one issue though. I had a login streak of 53 that I just lost today for no reason. I did not miss yesterday's login.

```json
{
  "label": "T_DailyRewards",
  "span": "I had a login streak of 53 that I just lost today for no reason. I did not miss yesterday's login.",
  "rule_applied": "definition",
  "rationale": "A login streak that resets on a missed day is a daily incentive with a penalty attached, which is the definition."
}
```

- **Also on this review:** _none — single-label_
- **Why this example:** Single-label, unanimous, and the mechanic is stated outright. Also shows R11's second half: the reviewer disputes missing a day, but the reset is the game's own rule, so the label stands whatever triggered it.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: unanimous.

#### Coverage — Kingshot

`c63003ef-dcdd-4ef2-a54e-0c9b0dfe931a` · UK · 2★ · 2026-03-02

> The game is very meh. The ads are much more fun than the actual game, and make up only a tiny portion of it. Still, I decided to persist for a few days to see how it went, and all the game ever had me do what click to upgrade this or research that or go there. Even after such a short time, there were already so many things that it wad impossible to keep track of them without relying on the daily quests and such. It's really not my cup of tea

```json
{
  "label": "T_DailyRewards",
  "span": "wad impossible to keep track of them without relying on the daily quests and such.",
  "rule_applied": "Daily task lists with resetting rewards",
  "rationale": "The span names a daily quest system that governs what the player does each session, which is the resetting task-list indicator."
}
```

- **Also on this review:** `T_PlayingByAppointment`, `T_Grinding`
- **Why this example:** The non-streak arm of the label: a daily task list counts with no streak, no calendar and no stated penalty. It is also the review that turned up the gold-set gap — the 'vs Playing by Appointment' boundary requires both labels here, because the daily quest cycle is what the player relies on to advance rather than a standalone reward. `T_PlayingByAppointment` has been added to the gold set (see `gold_set/post_adjudication_edits.md`), so this example now teaches the R9 co-assignment too.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

### `T_Grinding` — Grinding

> **Definition (codebook).** “Performing repetitive and tedious tasks” in order to make progress in a game. Emphasizes time invested over skill and in worst cases could be conducted unattended by the player.

#### Apt — Shadow Fight 4: Arena

`e92fc4f7-bdda-4f54-a8e2-aa591fbc7945` · IN · 3★ · 2023-01-07

> It's a fun game, but takes quite a long time to unlock new heros...I have done close to 100 fights and still have the first two heros you get when you start the game. Also the "share to unlock this hero" won't unlock the hero for me. So I'm thinking about installing the app.

```json
{
  "label": "T_Grinding",
  "span": "takes quite a long time to unlock new heros...I have done close to 100 fights and still have the first two heros",
  "rule_applied": "vs Slow Progress",
  "rationale": "The span names the repeated activity (fights) and ties it to progress (unlocking heroes), not merely that progress is slow."
}
```

- **Also on this review:** `S_FriendSpamImpersonation`
- **Why this example:** The exact discrimination the label needs: a repeated activity is named. Without the '100 fights' this would be slow progress and code nothing.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

#### Coverage — Total Battle: War Strategy

`042ee18e-d78e-4a0f-9cc2-2b1e10cc46e6` · UK · 3★ · 2025-05-14

> Sometimes, it feels like 'Groundhog Day', meaning that I show up, complete tasks, spend gold and potion, spend real money, then come back tomorrow and do it all over again. It's a way to get you drawn in and invested in the game, so you feel obligated to keep playing. There is no real progress or advancement; there is no pot of gold at the end of this rainbow.

```json
{
  "label": "T_Grinding",
  "span": "'Groundhog Day', meaning that I show up, complete tasks, spend gold and potion, spend real money, then come back tomorrow and do it all over again.",
  "rule_applied": "vs Gameplay described as repetitive",
  "rationale": "The span sets out the actual task cycle the player runs each day, so it is the repeated activity and not a general complaint that the game is repetitive."
}
```

- **Also on this review:** `T_InfiniteTreadmill`, `P_EasyToGetHardToLose`
- **Why this example:** The other Grinding boundary. 'Groundhog Day' alone would be an evaluation of quality under R2; the enumerated cycle is what lifts it to the label.
- **Provenance:** adjudicated note; 2/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

### `T_Advertisement` — Advertisement

> **Definition (codebook).** Compelled to view advertisements or incentivized to do so through the promise of rewards.

#### Apt — Real Cricket™

`86de0e5d-8187-4dfd-b8c3-05e5b271d89e` · IN · 1★ · 2023-07-02

> I would have given negative ratings if possible. Too much ads are shown after every over and every wicket fell. Opponent takes catches very easily while our team drops all the catches except one or two. Worst game, totally wasting of Data and time. Please don't go for it.

```json
{
  "label": "T_Advertisement",
  "span": "Too much ads are shown after every over and every wicket fell",
  "rule_applied": "definition",
  "rationale": "Ads are forced at fixed in-game events, so the player is compelled to view them to keep playing."
}
```

- **Also on this review:** `P_IllusionOfControl`
- **Why this example:** The compelled-viewing arm of the definition, stated plainly and coded unanimously.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: unanimous.

#### Coverage — 8 Ball Pool

`ce92d6ba-cc5f-40a1-bc8e-27a82fa0a8f8` · IN · 1★ · 2026-06-03

> way too many ads and paid popups. I've never seen a game ask u to watch an ad just to claim a daily reward

```json
{
  "label": "T_Advertisement",
  "span": "way too many ads and paid popups. I've never seen a game ask u to watch an ad just to claim a daily reward",
  "rule_applied": "definition",
  "rationale": "The ad is the price of a reward, which is the incentivised-viewing arm of the definition."
}
```

- **Also on this review:** _none — single-label_
- **Why this example:** The second arm of the same definition: rewarded ads rather than forced ads. Also shows that ad volume alone is not the trigger - the reward gate is.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

### `T_InfiniteTreadmill` — Infinite Treadmill

> **Definition (codebook).** Patterns that continually expand the game to never allow players to complete.

#### Apt — Toon Blast

`f62c8a1f-91fc-4866-b267-977172fa2db3` · UK · 1★ · 2026-03-03

> I don't leave reviews at all, but I'm beyond angry. Im in the 11000 level area. No new levels for 2 weeks and get a champions league. Its a money grab and I fell for it. Get new levels on 3/2/26 only to go maybe 50 levels and no more levels. Come to 3/3, another champions league & have to wait another 2 weeks for levels. This is BS for so many reasons. You dont have levels but have levels for a champions league?! Not going through that again. You've lost my bankroll & me as a player. Way to go!

```json
{
  "label": "T_InfiniteTreadmill",
  "span": "No new levels for 2 weeks and get a champions league. Its a money grab and I fell for it. Get new levels on 3/2/26 only to go maybe 50 levels and no more levels. Come to 3/3, another champions league",
  "rule_applied": "definition",
  "rationale": "The player clears everything available and is cycled back into a repeating league while more levels are added, so completion keeps receding."
}
```

- **Also on this review:** `S_Competition`
- **Why this example:** The definition in its most concrete form: content is added as fast as it is cleared, with dates given.
- **Provenance:** adjudicated note; 2/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

#### Coverage — Total Battle: War Strategy

`042ee18e-d78e-4a0f-9cc2-2b1e10cc46e6` · UK · 3★ · 2025-05-14

> Sometimes, it feels like 'Groundhog Day', meaning that I show up, complete tasks, spend gold and potion, spend real money, then come back tomorrow and do it all over again. It's a way to get you drawn in and invested in the game, so you feel obligated to keep playing. There is no real progress or advancement; there is no pot of gold at the end of this rainbow.

```json
{
  "label": "T_InfiniteTreadmill",
  "span": "There is no real progress or advancement; there is no pot of gold at the end of this rainbow.",
  "rule_applied": "vs High level number or long play history",
  "rationale": "The span asserts there is no attainable end state, which is what the boundary requires, rather than reporting a high level or a long tenure."
}
```

- **Also on this review:** `T_Grinding`, `P_EasyToGetHardToLose`
- **Why this example:** Guards the label's most common false positive. The same review's level counts and long play history would not qualify; the stated absence of an end state does.
- **Provenance:** adjudicated note; 1/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

### `T_MandatoryMarathon` — Mandatory Marathon

> **Definition (codebook).** Design that prevents the player from stopping at a moment of their choosing, requiring continuation to a stopping point defined by the game. Includes absent or restricted saving, checkpoint-only progress, and sessions or matches that cannot be exited without forfeiting progress.

#### Apt — Call of Duty®: Mobile

`443ba104-8abc-48c7-b8a7-b875ec52b05b` · IN · 5★ · 2020-04-19

> I'm actually super impressed. It really is the next best thing to playing on the console! I see a lot of reviews about it lagging and glitching...I would recommend it, but I am so angry. Literally at least once every day, the game just force quits itself in the middle of a match and it has cost me so many wins, and to add insult to injury....I get penalized for leaving matches early on top of that and I wasn't even the one who quit the match!

```json
{
  "label": "T_MandatoryMarathon",
  "span": "I get penalized for leaving matches early on top of that and I wasn't even the one who quit the match!",
  "rule_applied": "vs Loss caused by malfunction",
  "rationale": "Being penalised for leaving a match early is the game's own exit rule, so the label holds even though a crash is what triggered it here."
}
```

- **Also on this review:** _none — single-label_
- **Why this example:** The definition plus the R11 interaction in one span. The forfeit would follow a deliberate exit identically, which is exactly what the boundary tests.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: unanimous.

#### Coverage — Township

`fe4ad63c-0bee-4c2e-814f-1e4f46f14d3d` · UK · 4★ · 2026-05-26

> Please have a feature where you can edit plans for your town and then if you're not finished yet, you can temporarily save it as a draft so you can continue editing it later. It doesn't have to be usable. Just a draft design that you can continue editing later. Editing the plan of the town is very time consuming and it's unfortunate that you have to put all buildings in place first before you can save it and continue. I want to edit my town like Im an urban planner and it takes time of planning.

```json
{
  "label": "T_MandatoryMarathon",
  "span": "you have to put all buildings in place first before you can save it and continue",
  "rule_applied": "Can’t Pause or Save",
  "rationale": "The player cannot save partway and must carry the edit through to a state the game defines, which is the Can't Pause or Save instance."
}
```

- **Also on this review:** _none — single-label_
- **Why this example:** Coverage on three fronts: the saving arm rather than the session arm, no malfunction anywhere near it, and R12 - the review is mostly a feature request, but this clause describes a mechanic that exists today, so it codes.
- **Provenance:** adjudicated note; 2/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

---

## Monetary

### `M_PayToProgress` — Pay to Progress

> **Definition (codebook).** Patterns that require the players to spend money to progress in-game.

#### Apt — Mystery Town: Merge Games

`da13d098-3944-4e0b-aa94-c064a56edd83` · UK · 2★ · 2026-04-27

> the game is fun at first but it's so boring later on, you can't do anything without using in app purchases. you will never be able to complete the card packs and other mini games without being forced to pay real money for it. the energy cap will barely get you midway through an order unless you use all your gems. like everything just feels like a trap to get you to spend real money and it's so dumb.

```json
{
  "label": "M_PayToProgress",
  "span": "you can't do anything without using in app purchases",
  "rule_applied": "Pay Wall",
  "rationale": "Progress is stated to be unavailable without payment, which is the Pay Wall instance."
}
```

- **Also on this review:** `M_IntermediateCurrency`, `P_CompleteTheCollection`
- **Why this example:** The label at its most direct: payment named, progress named, no inference required.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

#### Coverage — Match Factory!

`07dd542b-2a71-4772-8a68-538115f1f826` · UK · 5★ · 2025-08-29

> I used to scoff at this game, but there's no dialogue or cheesy mascot animations. It's basically a digital version of 'pick up sticks.' And it's addicting. I have 1 complaint- level boosters can only be earned by beating levels, which I find ironic. Unless you're willing to pay for them, & lmk tell you, I'm not. At least not $10, I spent $2- I shouldn't have spent it & it was gone like 🫰. Ppl can gift lives to each other but not boosters. I *have* made it to lvl 639 but... now I'm stuck.

```json
{
  "label": "M_PayToProgress",
  "span": "Unless you're willing to pay for them",
  "rule_applied": "vs Free alternative",
  "rationale": "The span sets a paid route against a free one for the boosters progress requires, so the free path falls short of smooth advancement."
}
```

- **Also on this review:** `S_Reciprocity`
- **Why this example:** The implied case. Five words, no mechanic named, and the label rests entirely on the free/paid contrast the boundary rule licenses.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: unanimous.

### `M_IntermediateCurrency` — Intermediate Currency

> **Definition (codebook).** Pattern where players use real-world money to acquire in-game currency for purchases or trades within the game world

#### Apt — Travel Town - Merge Adventure

`b6745663-5486-4e5b-9066-8a889055d8bc` · UK · 4★ · 2026-03-21

> it's a good hook. the completionist in me wants to get every level, and the matching is satisfying enough to really tempt me into buying gems/energy to play more. I wish there was a way to disable all the event pop-ups. opening the app and then having to click away ten different challenges is very annoying. at least there are no outside ad pop-ups but I would rather have more optional outside ads than the unskippable events. please consider having a dismiss option for the events! good game.

```json
{
  "label": "M_IntermediateCurrency",
  "span": "buying gems",
  "rule_applied": "vs Purchases denominated in currency",
  "rationale": "The currency is the object being acquired, so real money is the consideration and the conversion sits inside the span."
}
```

- **Also on this review:** `M_PayToProgress`, `M_UIMisdirection`
- **Why this example:** The direction-of-transaction test in its simplest form. Two words, and they settle it because gems are what is bought, not what is spent.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

#### Coverage — Free Fire: 9th Anniversary

`fb70e577-e644-4af9-88a1-773476a5b805` · US · 1★ · 2021-09-07

> I use to love this game is was my best game I ever played, until now. It's difficult to play if you are using a low ram end device why?,It lag alot.When I approach a enemy it starts to lag like crazy.Enemies are hard to kill now. I never top up not even once. They were always keeping away free stuffs I was hype for the update but now, it just want you to top up to get this or that. They just want your money. I want the old free fire back where you can Play worldwide etc etc please fix bigs n etc

```json
{
  "label": "M_IntermediateCurrency",
  "span": "it just want you to top up to get this or that.",
  "rule_applied": "definition",
  "rationale": "A search establishes that 'top up' is the game's term for buying diamonds with real money, so the span describes money converted into in-game currency."
}
```

Review-level search fields for this example:

```json
{
  "invoked_web_search": true,
  "search_query": "Free Fire what does top up mean diamonds",
  "search_result": "\"Top up\" is Free Fire's term for buying diamonds, the game's premium currency, with real money."
}
```

- **Also on this review:** _none — single-label_
- **Why this example:** Requires R10. 'Top up' is not resolvable from the review text alone, so the label depends on a search resolving the term. The search is shown with the entry below.
- **Provenance:** adjudicated note; 2/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

### `M_DeceptiveLuxury` — Deceptive Luxury

> **Definition (codebook).** Deceptive Luxury is a game design tactic that makes an item feel rare and exclusive so players will pay more for it, when the rarity was invented by the developer rather than being a real limit. The item's price reflects manufactured scarcity, not genuine value.

#### Apt — RAID: Shadow Legends

`57add346-8b93-4249-be50-1a39331cf79b` · UK · 2★ · 2020-06-25

> These are my views of the game after playing for almost a day. I didnt make a single purchase but got a free champion and silver from a referral. Pros: Easy to learn the controls and layout of the game, nice story line, easy combat system, no lag, nice champion designs and gameplay. Cons: Every single time you log in you are bombarded with pop ads advertising "special" or "limited time" deals, once your champions hit level 30 it becomes a horrible grind, p2p is the best way to win this game.

```json
{
  "label": "M_DeceptiveLuxury",
  "span": "advertising \"special\" or \"limited time\" deals",
  "rule_applied": "Artificial Scarcity",
  "rationale": "Time-limited offers create urgency the developer invented, and the scarcity is attached to a purchase, which is Artificial Scarcity."
}
```

- **Also on this review:** `M_PayToProgress`, `S_ForcedFellowship`
- **Why this example:** The commonest instance of the label, and it clears the 'vs Scarcity without monetization' boundary because the scarcity is on an offer.
- **Provenance:** adjudicated note; 2/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

#### Coverage — GODDESS OF VICTORY: NIKKE

`71d54398-28c7-4f4a-a67d-0914206f59c6` · US · 1★ · 2026-04-30

> Gacha is quite scummy. If you started with no currency and wanted a guaranteed unit, it's 200 tickets. You get about 20 tickets with $80 so even being generous it's still $600-$800 just to guarantee the unit you want. 4% chance to pull any SSR at any time. In a 10-pull that's around a 33% chance give or take. I failed that 15 times in a row, so 150 pulls with no SSR (supposedly 1/456 chance of happening) . Great system. Really makes players not want to quit or anything.

```json
{
  "label": "M_DeceptiveLuxury",
  "span": "still $600-$800 just to guarantee the unit you want. 4% chance to pull any SSR at any time",
  "rule_applied": "Remedy Consumption + Artificial Scarcity",
  "rationale": "Pulls are made scarce at a 4% rate, and a guaranteed unit is then sold as a second, far more expensive route to the same item, so the player pays extra to escape the scarcity."
}
```

- **Also on this review:** `M_IntermediateCurrency`, `M_Gambling`, `P_RewardMania`
- **Why this example:** Two indicators combining, which is how this label usually presents at the top end. Rarity Level is tagged [dp-enhancer] in the codebook, not a standalone assigning indicator — it prices the SSR tier, but what assigns the label is the manufactured scarcity plus the paid remedy.
- **Provenance:** adjudicated note; 2/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

### `M_RecurringFee` — Recurring Fee

> **Definition (codebook).** Patterns that encourages players to maximize playtime to justify their spending.

#### Apt — Cash Frenzy™ - Casino Slots

`6088dbf1-7d56-4302-945e-72fd73832609` · US · 2★ · 2020-09-27

> Great games. Horrible customer support. I stopped playing the game for about a year. I came and didnt realize they unlinked my facebook. I started over, joined a clan, and bought season pass. They wont delete my old account so I can link my facebook, and wont transfer purchases to the one linked. They said I have to rebuy everyrhing

```json
{
  "label": "M_RecurringFee",
  "span": "season pass",
  "rule_applied": "Battle passes, MMO-subscriptions",
  "rationale": "A paid seasonal pass is named as bought and present, which is the listed indicator."
}
```

- **Also on this review:** _none — single-label_
- **Why this example:** Unanimous, single-label, and the indicator is named outright.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: unanimous.

#### Coverage — Fishdom

`d96bbc2c-73bb-4af5-9597-34a44117c7f5` · US · 1★ · 2022-11-05

> Changed and not for the better, the season pass is a total rip off with far less rewards. Too many hard levels so you get stuck for weeks and lose interest. Should be able to opt out of the he challenge levels. And the additional side tasks don't earn the same boosters that they used to. It was pretty well balanced in the past but just got too difficult and developers too greedy now. Revert it back to how it was.

```json
{
  "label": "M_RecurringFee",
  "span": "season pass",
  "rule_applied": "Battle passes, MMO-subscriptions",
  "rationale": "A season pass is a recurring paid subscription; the reviewer's poor opinion of its value does not change what the mechanic is."
}
```

- **Also on this review:** _none — single-label_
- **Why this example:** R8 in action. Same indicator, but the surrounding text calls it 'a total rip off' - the mechanic is coded, the evaluation is not.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

### `M_Gambling` — Gambling

> **Definition (codebook).** Using real money to participate in a game that involves an element of luck, with the possibility of receiving a prize as a reward.

#### Apt — Fate/Grand Order (English)

`a59f5319-a1b7-4991-8c6b-d2d2ca56265c` · UK · 1★ · 2020-04-24

> It's an unregulated casino. Every part of the game is set up to direct you towards the slot machine summoning system. Story? Free buffet and show to keep you interested. Plus, you like this character? Well, either hope you have godly luck, or fork over some cash (~$140 for 50% to get a 'rate up' character), because the majority of them are limited time only. Gameplay is mostly just grind to build sunk cost. That, and an incentive to roll the slots for things to reduce the amount of grind.

```json
{
  "label": "M_Gambling",
  "span": "(~$140 for 50% to get a 'rate up' character)",
  "rule_applied": "definition",
  "rationale": "Real money is staked against a stated probability with a character as the prize, which is the definition exactly."
}
```

- **Also on this review:** `M_PayToProgress`, `M_DeceptiveLuxury`, `M_UIMisdirection`, `P_EasyToGetHardToLose`, `P_RewardMania`
- **Why this example:** Money, chance and prize all inside one span. Nothing has to be inferred.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

#### Coverage — Lotsa Slots - Casino Games

`c1a9f304-9cc1-4eb5-84f0-7988297fe423` · US · 2★ · 2024-06-05

> The game has gone downhill. The wins are not as big, or as often. The bonus when buying is smaller. If you are considering slot games there are less costly options with more wins

```json
{
  "label": "M_Gambling",
  "span": "slot games there are less costly options",
  "rule_applied": "definition",
  "rationale": "Slots are a chance mechanic and the span sets their real-money cost against cheaper alternatives, so real money is being spent for luck-based prizes."
}
```

- **Also on this review:** `M_IntermediateCurrency`, `P_RewardMania`
- **Why this example:** The label read straight off the definition where the reviewer never says 'I gambled'. The whole of it is carried by 'slot games' plus 'less costly' — a chance mechanic and a real cost.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

### `M_PowerCreep` — Power Creep

> **Definition (codebook).** Patterns that diminishing the value of purchased items over time to drive new purchases.

#### Apt — Clash of Clans

`2471db11-2c61-415a-8af4-33b80a05c759` · UK · 1★ · 2026-05-06

> The balancing makes this game have no point. So many bugs, to many sales, support is non existent. You will spend months upgrading troops and defenses just to be nerfed. I have a maxed out account and anyone can destroy me. The more you play the game the more it penalizes you. Reduced times for people that don't play as much. Every account recieves different reward amounts. I've played over 10 years, it's just a chore at this point, not fun. They ruin COC more with every update and event.

```json
{
  "label": "M_PowerCreep",
  "span": "You will spend months upgrading troops and defenses just to be nerfed",
  "rule_applied": "definition",
  "rationale": "Investment the player already made is devalued afterwards by rebalancing, which is the definition."
}
```

- **Also on this review:** `T_Grinding`
- **Why this example:** Loss strictly after acquisition, caused by a developer change. Unanimous.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

#### Coverage — Genshin Impact

`b0a2aece-2b3e-4026-966b-7836e3cfc6bc` · IN · 1★ · 2026-05-22

> I love the game, I invested so much time and effort in it. I genuinely love the art and designs but recently ever since Fontaine arrived the characters started becoming expensive because of premium team comps and some being locked and good for a specific team. old characters started falling off which I hope they could climb back up. And now the Meta shifts now are extremely fast.. and another issue is how much rewards we get.. it's so low each patch barely gives us enough to hit hard pity.

```json
{
  "label": "M_PowerCreep",
  "span": "old characters started falling off which I hope they could climb back up. And now the Meta shifts now are extremely fast..",
  "rule_applied": "definition",
  "rationale": "Characters the player already owns are described as having fallen off as the meta moved, which is purchased value diminishing over time."
}
```

- **Also on this review:** `M_DeceptiveLuxury`, `P_EasyToGetHardToLose`, `P_RewardMania`
- **Why this example:** Devaluation by drift rather than by an explicit nerf, and no purchase named in the span — the definition still reaches it. Contrast with the apt example, where a developer nerf is stated.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

### `M_WasteAversion` — Waste Aversion

> **Definition (codebook).** Patterns set small differences between in-game currency and item costs, prompting additional currency purchases.

#### Apt — Travel Town - Merge Adventure

`bc0d6ee6-1f01-4101-8c25-fc4da5a1ef7c` · UK · 3★ · 2022-05-13

> This game is good but I dislike the limited space on the board and especially the potterwheel. I spent so much energy just trying to get the items I need and after a while the potterwheel isn't even needed. The limited space is bothersome too and you have to use diamonds to buy more storage with each purchase the price gets higher.

```json
{
  "label": "M_WasteAversion",
  "span": "The limited space is bothersome too and you have to use diamonds to buy more storage",
  "rule_applied": "definition",
  "rationale": "The board is full and capacity has to be bought, so the shortfall is realised rather than merely possible."
}
```

- **Also on this review:** _none — single-label_
- **Why this example:** The capped-inventory arm with the loss actually realised: the board is full and capacity has to be bought.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

#### Coverage — Merge Cooking®

`31c8de21-5262-4e88-9d3c-feaffe08ec14` · UK · 3★ · 2023-07-05

> I would love to be able to play this game more because I quite enjoy it, but the time it takes to recharge items and how long it takes to 'cook' is frustrating! I have to watch adds for a measly recharge only to run out again quickly. I run out of space on the board and have to delete items I spent time on. It's fun when you can play, but otherwise is just a huge money grab

```json
{
  "label": "M_WasteAversion",
  "span": "I run out of space on the board and have to delete items I spent time on.",
  "rule_applied": "definition",
  "rationale": "Items the player invested time in are destroyed to make room, so value is forfeited outright rather than repurchased."
}
```

- **Also on this review:** `T_PlayingByAppointment`, `T_Advertisement`
- **Why this example:** The forfeiture arm rather than the purchase arm — nothing is bought, value is simply destroyed. Same definition, opposite resolution, which is why both examples cite it.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: unanimous.

### `M_EasyToPurchase` — Easy to Purchase

> **Definition (codebook).** Interface design that reduces the friction or deliberation involved in spending real money, through purchase-by-default options, absent confirmation or refund steps, prompts triggered at the point of insufficient funds, or price presentation that makes an amount appear smaller than it is.

#### Apt — Dark War Survival

`2b915fb2-6ff4-4351-9b2f-e8db5661e0a5` · UK · 1★ · 2025-09-28

> accidentally brought a pack when I double tapped the screen got a refund for the pack through Google play and now my game has been locked and they are holding my account to ransom until I pay the equivalent of the refund I got, thanks ffs, respond promptly my a**, I explained the problem and after what would be considered not very promptly was told you would continue to hold my account ransom, I explained further and you don't bother to respond at all

```json
{
  "label": "M_EasyToPurchase",
  "span": "accidentally brought a pack when I double tapped the screen",
  "rule_applied": "Accidental Purchases",
  "rationale": "A purchase completed on a stray double tap means no confirmation step stood between the player and spending."
}
```

- **Also on this review:** _none — single-label_
- **Why this example:** Friction removed at the moment of payment, stated plainly. Unanimous.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: unanimous.

#### Coverage — Mech Arena - Shooting Game

`cbcde992-08aa-4bfb-a653-a944e4b733aa` · IN · 3★ · 2022-05-18

> Every time you open the main menu you get a minimum of 10 pop up ads to buy gear/equipment with small x buttons in the corner. Edit: the developer responded to this review. It would be great if the frequency of offers was reduced: 2 or 3 max. My concern is if i did purchase something, Id get even more pop-ups! I didn't want to buy the first 9 items, I certainly dont want the last one any more.

```json
{
  "label": "M_EasyToPurchase",
  "span": "Every time you open the main menu you get a minimum of 10 pop up ads to buy gear/equipment",
  "rule_applied": "vs Purchase solicitation",
  "rationale": "The offers intercept the session on every menu open and each must be dismissed to continue, which is interception rather than ad volume."
}
```

- **Also on this review:** `M_UIMisdirection`
- **Why this example:** Guards the label's main false positive. High ad volume alone codes NONE under R2; it is the interception and the forced dismissal that qualify.
- **Provenance:** adjudicated note; 2/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

### `M_UIMisdirection` — UI Misdirection

> **Definition (codebook).** The user interface (i.e., not the NPC) contains elements designed to purposefully focus attention on specific options, or away from opportunities to opt-out.

#### Apt — Whiteout Survival

`d8278e85-b5f2-45ef-88ad-ea3370a5195d` · UK · 1★ · 2024-09-25

> There is basically no real time gameplay. No gameplay at all really. Loaded it up for the first time in a week to a flashing button I didn't recognise. Clicked the button "DO YOU WANT TO PAY US $8?!" lol... No whiteout survival, I don't.

```json
{
  "label": "M_UIMisdirection",
  "span": "Loaded it up for the first time in a week to a flashing button I didn't recognise. Clicked the button \"DO YOU WANT TO PAY US $8?!\"",
  "rule_applied": "Exciting UI Effect",
  "rationale": "Animation is used to pull the player onto a button, and what it opens is a purchase prompt."
}
```

- **Also on this review:** _none — single-label_
- **Why this example:** The attention-directing arm, with the animation and the purchase destination both in the span.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

#### Coverage — Mech Arena - Shooting Game

`cbcde992-08aa-4bfb-a653-a944e4b733aa` · IN · 3★ · 2022-05-18

> Every time you open the main menu you get a minimum of 10 pop up ads to buy gear/equipment with small x buttons in the corner. Edit: the developer responded to this review. It would be great if the frequency of offers was reduced: 2 or 3 max. My concern is if i did purchase something, Id get even more pop-ups! I didn't want to buy the first 9 items, I certainly dont want the last one any more.

```json
{
  "label": "M_UIMisdirection",
  "span": "with small x buttons in the corner.",
  "rule_applied": "vs Attention-directing without an opt-out",
  "rationale": "The close control is undersized and pushed to the corner, so the opt-out is obstructed by its size and placement."
}
```

- **Also on this review:** `M_EasyToPurchase`
- **Why this example:** The second arm of the same boundary: obstructing the exit rather than highlighting the option. Six words carry it.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

### `M_NeverEndingLure` — Never-Ending Lure

> **Definition (codebook).** The “Never-Ending Lure” pattern is designed to convert non-paying players into paying ones (“First Charge Discount”) and encourage consistent long-term payments (“Accumulating Rewards”).

#### Apt — Match Masters

`4a9d42d6-ad1d-4d3e-9cd1-5b16339524b0` · UK · 1★ · 2022-01-27

> This app was made to make money, not a fun game. It uses pretty much has made the entire game around the most profitable industry tricks for making whales. It has pop up to sell you in game assets constantly, it discounts first time buyers, it makes you feel like you've earned prizes, but you've earned the right to buy the prizes. You can spend money to gain a competitive advantage. The game itself is heavily determined by luck, basically it's just one big slot machine.

```json
{
  "label": "M_NeverEndingLure",
  "span": "it discounts first time buyers",
  "rule_applied": "First Charge Discount",
  "rationale": "A discount reserved for a player's first purchase is the First Charge Discount instance, aimed at converting a non-payer into a payer."
}
```

- **Also on this review:** `M_PayToProgress`, `M_EasyToPurchase`, `S_Competition`, `P_AestheticManipulation`, `P_RewardMania`
- **Why this example:** The indicator named almost word for word.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

#### Coverage — Dice Dreams™️

`97c23c8d-b858-4afa-83b1-ebd08d56badc` · UK · 5★ · 2026-05-31

> awesome the beginner packs really help get you started so you can see what can game offers in terms of gameplay, no surprises

```json
{
  "label": "M_NeverEndingLure",
  "span": "awesome the beginner packs really help get you started",
  "rule_applied": "First Charge Discount",
  "rationale": "Beginner packs are the cheap entry bundle that converts a new player into a paying one, whatever the reviewer thinks of them."
}
```

- **Also on this review:** _none — single-label_
- **Why this example:** A five-star review praising the mechanic. R7 and R8 both apply: presence is coded independently of approval, and this is the only positive-valence example in the set.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: unanimous.

---

## Social

### `S_ForcedFellowship` — Forced Fellowship

> **Definition (codebook).** Forced Fellowship is a game design tactic that turns real friendships into leverage: the game rewards you for pulling friends in, then makes it costly to stop playing because quitting would let those friends down.Design that uses the player's social ties, real or in-game, as the mechanism of recruitment or retention: rewarding the player for bringing others into the game, or making disengagement costly because absence burdens teammates, guildmates, or friends.

#### Apt — RAID: Shadow Legends

`57add346-8b93-4249-be50-1a39331cf79b` · UK · 2★ · 2020-06-25

> These are my views of the game after playing for almost a day. I didnt make a single purchase but got a free champion and silver from a referral. Pros: Easy to learn the controls and layout of the game, nice story line, easy combat system, no lag, nice champion designs and gameplay. Cons: Every single time you log in you are bombarded with pop ads advertising "special" or "limited time" deals, once your champions hit level 30 it becomes a horrible grind, p2p is the best way to win this game.

```json
{
  "label": "S_ForcedFellowship",
  "span": "got a free champion and silver from a referral",
  "rule_applied": "Social Pyramid Scheme",
  "rationale": "The game pays in-game rewards for bringing a new person in, which is the Social Pyramid Scheme instance."
}
```

- **Also on this review:** `M_PayToProgress`, `M_DeceptiveLuxury`
- **Why this example:** Recruitment rewarded, stated directly. Clears the 'vs Reciprocity' boundary because the person is new to the game.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

#### Coverage — Match Masters

`b4d6e64c-bd0c-49aa-9023-ed3f59bc63bf` · UK · 3★ · 2021-04-10

> Seems like FOREVER since my last enjoyable gaming experience, until I downloaded this colorful, graphic & challenging app! Only one issue & it's a rather strange one. Played a bit this week.Really enjoyed it! I decided 2 form a team, so invites were sent 2 gaming friends fr other apps, FB friends etc. 12 hrs later I'd a chat room filled w/48 strangers on my team?? My real friends downlded & "joined" my team, but no success on their end or mine & NO coins rewarded!

```json
{
  "label": "S_ForcedFellowship",
  "span": "My real friends downlded & \"joined\" my team, but no success on their end or mine & NO coins rewarded!",
  "rule_applied": "vs Reciprocity",
  "rationale": "Coins are the stated reward for getting friends to download and join, so the mechanic recruits new players rather than trading favours with existing ones."
}
```

- **Also on this review:** `S_FriendSpamImpersonation`
- **Why this example:** The boundary that separates this from Reciprocity, and the reward is established by the reviewer complaining it did not arrive - the mechanic is still described.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: unanimous.

### `S_FriendSpamImpersonation` — Friend Spam / Impersonation

> **Definition (codebook).** The game employs unsolicited messaging to a player's contact list or social media account.

#### Apt — Match Masters

`b4d6e64c-bd0c-49aa-9023-ed3f59bc63bf` · UK · 3★ · 2021-04-10

> Seems like FOREVER since my last enjoyable gaming experience, until I downloaded this colorful, graphic & challenging app! Only one issue & it's a rather strange one. Played a bit this week.Really enjoyed it! I decided 2 form a team, so invites were sent 2 gaming friends fr other apps, FB friends etc. 12 hrs later I'd a chat room filled w/48 strangers on my team?? My real friends downlded & "joined" my team, but no success on their end or mine & NO coins rewarded!

```json
{
  "label": "S_FriendSpamImpersonation",
  "span": "I decided 2 form a team, so invites were sent 2 gaming friends fr other apps, FB friends etc.",
  "rule_applied": "vs Destination of the message",
  "rationale": "Invitations go out through the player's own contacts and Facebook account, so the game acts under the player's identity and something is actually sent."
}
```

- **Also on this review:** `S_ForcedFellowship`
- **Why this example:** Messaging performed, not permission requested. R13 does not exclude it because the installed game is what sends.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: unanimous.

#### Coverage — Shadow Fight 4: Arena

`e92fc4f7-bdda-4f54-a8e2-aa591fbc7945` · IN · 3★ · 2023-01-07

> It's a fun game, but takes quite a long time to unlock new heros...I have done close to 100 fights and still have the first two heros you get when you start the game. Also the "share to unlock this hero" won't unlock the hero for me. So I'm thinking about installing the app.

```json
{
  "label": "S_FriendSpamImpersonation",
  "span": "\"share to unlock this hero\" won't unlock the hero for me",
  "rule_applied": "definition",
  "rationale": "The game posts under the player's own account as the condition for an unlock, which is unsolicited messaging sent through the player's social account."
}
```

- **Also on this review:** `T_Grinding`
- **Why this example:** The prompted-to-post case rather than the already-sent case. R11 does not suppress it: the share-to-unlock mechanic is designed, only its execution failed.
- **Provenance:** adjudicated note; 2/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

### `S_Reciprocity` — Reciprocity

> **Definition (codebook).** Patterns that instill a sense of obligation to reciprocate by donating resources to other players.

#### Apt — Match Factory!

`07dd542b-2a71-4772-8a68-538115f1f826` · UK · 5★ · 2025-08-29

> I used to scoff at this game, but there's no dialogue or cheesy mascot animations. It's basically a digital version of 'pick up sticks.' And it's addicting. I have 1 complaint- level boosters can only be earned by beating levels, which I find ironic. Unless you're willing to pay for them, & lmk tell you, I'm not. At least not $10, I spent $2- I shouldn't have spent it & it was gone like 🫰. Ppl can gift lives to each other but not boosters. I *have* made it to lvl 639 but... now I'm stuck.

```json
{
  "label": "S_Reciprocity",
  "span": "Ppl can gift lives to each other",
  "rule_applied": "definition",
  "rationale": "Players send resources to one another, which is the donation-and-return mechanic the definition describes."
}
```

- **Also on this review:** `M_PayToProgress`
- **Why this example:** Unanimous and unambiguous: resources move between players.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: unanimous.

#### Coverage — Pokémon GO

`681563e1-227c-4af2-8a1f-a145f3a795ca` · US · 2★ · 2020-10-30

> This game has been good for years. But lately... My god. So glitchy. Can barely log into the game these days. Gift exchange screens are ridiculously slow. If you leave your phone for a few minutes, it's probably going to crash and require a restart. Get it together, folks...

```json
{
  "label": "S_Reciprocity",
  "span": "Gift exchange screens",
  "rule_applied": "definition",
  "rationale": "A gift exchange between players is named as a present feature; the complaint is that its screens are slow, not that it does not exist."
}
```

- **Also on this review:** _none — single-label_
- **Why this example:** R11 discrimination. The review is largely about glitches, but the exchange system itself is functioning design, so the label survives.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: unanimous.

### `S_EncouragesAntiSocialBehavior` — Encourages Anti-Social Behavior

> **Definition (codebook).** Patterns that incentivize players to engage in dishonest or harmful actions to gain an advantage.

#### Apt — Tiles Survive!

`ee8d0008-1f3c-400d-bbbe-d29e8a7c0405` · IN · 1★ · 2025-10-22

> Extremely pay2win bundled with a bunch of game modes where strong players steal from weaker players, furthering a divide that only more money can bridge.

```json
{
  "label": "S_EncouragesAntiSocialBehavior",
  "span": "game modes where strong players steal from weaker players",
  "rule_applied": "definition",
  "rationale": "The reviewer describes game modes built so that strong players take from weak ones, so the harmful behaviour is what the design is for rather than a side effect of it."
}
```

- **Also on this review:** `M_PayToProgress`, `S_Competition`
- **Why this example:** Deliberate design read straight from the definition: a mode exists whose purpose is predation. The developer's intent is what carries it, not a reward the span has to name.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

#### Coverage — Yalla Ludo - Ludo&Jackaroo

`64e4aba6-ce6d-420a-b5cb-4422c11c4186` · IN · 5★ · 2022-08-23

> Hello, I recommend improving the "Auto Playing" feature through "Bot". If the first player isn't responding or playing, the second player at the end have to exit and lose his credits because there are no limitations are for the Bot. Some players can also misuse this feature to grab the credits of the corresponding players. I think you must consider it, next it's up to your development team :-) Regards

```json
{
  "label": "S_EncouragesAntiSocialBehavior",
  "span": "Some players can also misuse this feature to grab the credits of the corresponding players.",
  "rule_applied": "vs Permitted harm",
  "rationale": "The span carries both the harmful act and the gain it produces for the aggressor, who ends up with the other player's credits."
}
```

- **Also on this review:** `T_MandatoryMarathon`, `S_Competition`
- **Why this example:** The other boundary. Design that merely permits harm codes NONE; here the aggressor's gain is stated, which is what makes it an incentive.
- **Provenance:** coder span (no adjudicated note entry); 2/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

### `S_FearOfMissingOutFOMO` — Fear of Missing Out (FOMO)

> **Definition (codebook).** Players are pressured to continue playing the game by the fear of missing out on rewards or falling behind other players.

#### Apt — Last War:Survival Game

`f9424404-513f-41a9-a3b9-a97670e89512` · UK · 1★ · 2024-10-07

> This game demands constant attention and is definitely falsely advertised, though they just added some new screenshots to try and avoid chargebacks. They lure you in and then the pressure to login every 2-3 hours 24/7 is constant with Arms Race or keep it open all day long so you don't miss treasure digs. Competing=who spends the most. This is a gacha game and 4x. You've been warned.

```json
{
  "label": "S_FearOfMissingOutFOMO",
  "span": "pressure to login every 2-3 hours 24/7 is constant with Arms Race or keep it open all day long so you don't miss treasure digs",
  "rule_applied": "definition",
  "rationale": "The player is pressured to stay in the game so as not to miss timed events, which is the anticipatory pressure the definition describes."
}
```

- **Also on this review:** `T_PlayingByAppointment`, `M_PayToProgress`, `S_Competition`, `P_RewardMania`
- **Why this example:** The clearest split against Playing by Appointment: the same review yields both labels from different spans. Note the discriminating boundary rule is written on Playing by Appointment's side, so from here it is the definition that applies.
- **Provenance:** adjudicated note; 1/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

#### Coverage — Homescapes

`f09401aa-1aef-4c8b-ac3a-92eec49af44d` · UK · 3★ · 2019-04-15

> I like the satisfaction of finishing the puzzles and renovating rooms a lot, but I hate how the game tries to force you to be competitive. every time you lose the game reminds you that unless you pay up, you're going to go down on the leaderboard and will lose all your winning streak rewards. it makes you feel bad for not winning every level on the first attempt. I just want to enjoy playing a casual puzzle game, and I think there should be opt out of the leaderboard system.

```json
{
  "label": "S_FearOfMissingOutFOMO",
  "span": "and will lose all your winning streak rewards",
  "rule_applied": "definition",
  "rationale": "The player is pressured to keep winning so as not to forfeit accumulated rewards and fall behind on the leaderboard."
}
```

- **Also on this review:** `M_PayToProgress`, `S_Competition`, `P_EasyToGetHardToLose`
- **Why this example:** The falling-behind arm rather than the missing-an-event arm, and the pressure is social (leaderboard position) rather than scheduled.
- **Provenance:** coder span (no adjudicated note entry); 1/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

### `S_Competition` — Competition

> **Definition (codebook).** Patterns that make players against each other in competition.

#### Apt — War Robots Multiplayer Battles

`ce1c6456-5d34-4001-a1a8-8b5991ef8ffb` · IN · 1★ · 2024-01-17

> Too much greed by the game devs. You are not just bombarded with tons of advertisements but after you progress up through the rankings, you notice you are always competing with gamers way above your paygrade. The strategy is to make you spend and spend to reach to upper levels. Toxic pity, I would say. Better to spend £50 in a Console game and play for ages, than spend £50 in this game just to get a lame account. The more you pay, more the prices start to increase as well. Run!!

```json
{
  "label": "S_Competition",
  "span": "you notice you are always competing with gamers way above your paygrade",
  "rule_applied": "definition",
  "rationale": "The game puts the player against other players, which is the definition."
}
```

- **Also on this review:** `T_Advertisement`, `M_PayToProgress`
- **Why this example:** Competition stated in the reviewer's own words.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

#### Coverage — Moba Legends: 5v5!

`a12fb168-3791-4d93-8cee-9b38fceb3059` · IN · 1★ · 2026-02-03

> If you want to get some serious anger issues and frustration,the game is for you.This game simply don't care about you at all,they only need money and frame(Obv it's a complete copy of league of legends). The match making, completely illogical,if you play good,game will give you bad teammates expecting you to carry and if you play bad,game will give you more bad teammates saying that it's so called "skill based matching". The only thing game will provide you is waste of time and energy

```json
{
  "label": "S_Competition",
  "span": "The match making",
  "rule_applied": "definition",
  "rationale": "Matchmaking exists to pair the player against other players, so competition is implied by the mechanic being named."
}
```

- **Also on this review:** `P_IllusionOfControl`
- **Why this example:** The implied case. Two words, no competitive language at all, and the label rests on what matchmaking necessarily is.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

---

## Psychological

### `P_EasyToGetHardToLose` — Easy to Get, Hard to Lose

> **Definition (codebook).** Design in which accumulated investment, time played, money spent, progress attained, or partially completed goals, raises the cost of leaving. Entry is low-friction; exit entails forfeiting value the player already holds.

#### Apt — Bingo Blitz™️ - Bingo Games

`12105fcc-1fe5-46c6-8d77-d0bd2a11d6f1` · US · 1★ · 2025-03-11

> Once again it will not load. I have tried everything. I have uninstalled & reinstalled the app.i have updated everything and still ho luck. This is not the first time this has happened. If I didnt have so much time invested I would not continue playing. 3-10Update: 4days post issue the app came back. Having something fun playing another once again an update to the new version and now I cannot open the app again . Crazy!Do not waste your time telling to do all the fixes.

```json
{
  "label": "P_EasyToGetHardToLose",
  "span": "If I didnt have so much time invested I would not continue playing.",
  "rule_applied": "Invested (Endowed) Value",
  "rationale": "The player states directly that accumulated time is the only reason they have not left, which is the raised cost of leaving."
}
```

- **Also on this review:** _none — single-label_
- **Why this example:** The player names the mechanism on themselves. Unanimous, single-label.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: unanimous.

#### Coverage — Total Battle: War Strategy

`042ee18e-d78e-4a0f-9cc2-2b1e10cc46e6` · UK · 3★ · 2025-05-14

> Sometimes, it feels like 'Groundhog Day', meaning that I show up, complete tasks, spend gold and potion, spend real money, then come back tomorrow and do it all over again. It's a way to get you drawn in and invested in the game, so you feel obligated to keep playing. There is no real progress or advancement; there is no pot of gold at the end of this rainbow.

```json
{
  "label": "P_EasyToGetHardToLose",
  "span": "It's a way to get you drawn in and invested in the game, so you feel obligated to keep playing.",
  "rule_applied": "Invested (Endowed) Value",
  "rationale": "The review attributes the retention to design: investment is built up so that leaving feels costly."
}
```

- **Also on this review:** `T_Grinding`, `T_InfiniteTreadmill`
- **Why this example:** Same indicator reached from the design side rather than the self-report side, and inside a three-label review where it must be separated from Grinding and Infinite Treadmill.
- **Provenance:** adjudicated note; 2/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

### `P_CompleteTheCollection` — Complete the Collection

> **Definition (codebook).** The compulsion to acquire all the items, achievements, or hidden features in a game.

#### Apt — MONOPOLY GO!

`49a53e7c-0564-46c6-995f-1d8bc418c80a` · US · 1★ · 2024-09-08

> I used to love this game but the new sticker album has been made to be to difficult to get the non tradable gold cards, I have been needing only gold cards for two months now and have only been awarded one new card in that time, and the golden blitz has never been a card that I am in need of. After this album I will no longer be playing the game due to this and the fact that events are just too hard to finish with the small amount of dice you get in the game. It just is no longer fun anymore

```json
{
  "label": "P_CompleteTheCollection",
  "span": "but the new sticker album has been made to be to difficult to get the non tradable gold cards",
  "rule_applied": "definition",
  "rationale": "Album completion is what is driving the player, and the missing cards are what keeps them playing."
}
```

- **Also on this review:** `S_Reciprocity`, `P_RewardMania`
- **Why this example:** A named collection with the missing pieces framed as the hook.
- **Provenance:** adjudicated note; 2/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

#### Coverage — Mystery Town: Merge Games

`da13d098-3944-4e0b-aa94-c064a56edd83` · UK · 2★ · 2026-04-27

> the game is fun at first but it's so boring later on, you can't do anything without using in app purchases. you will never be able to complete the card packs and other mini games without being forced to pay real money for it. the energy cap will barely get you midway through an order unless you use all your gems. like everything just feels like a trap to get you to spend real money and it's so dumb.

```json
{
  "label": "P_CompleteTheCollection",
  "span": "never be able to complete the card packs",
  "rule_applied": "definition",
  "rationale": "The player is working toward a complete set of card packs and frames not finishing it as the harm."
}
```

- **Also on this review:** `M_PayToProgress`, `M_IntermediateCurrency`
- **Why this example:** The collection drive with payment gating it, so the example also shows Complete the Collection and Pay to Progress coexisting on separate spans under R9.
- **Provenance:** adjudicated note; 2/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

### `P_IllusionOfControl` — Illusion of Control

> **Definition (codebook).** Patterns that deceive players about their skill level to encourage more gameplay.

#### Apt — Ludo King®

`2fd4ef32-a33b-44ed-a921-2889ba6e0375` · IN · 1★ · 2020-08-27

> Dice rolls are not random at all, they are preplanned. Game randomly decides at the start of the play that which player has to win and dice rolls according to it. You also will know at the beginning of the game that who is going to win. One player will get more and more 6s and another one will get 1 or 2 mostly. The rolls have gone predictable. That's why I have uninstalled the game today. It's frustrating.

```json
{
  "label": "P_IllusionOfControl",
  "span": "Dice rolls are not random at all, they are preplanned",
  "rule_applied": "vs Alleged rigging",
  "rationale": "The span names a mechanism - a winner fixed at the start with the dice fed to match - so it is a claim about concealed determination, not a bad run."
}
```

- **Also on this review:** `S_Competition`, `P_OptimismAndFrequencyBiases`
- **Why this example:** The boundary satisfied at its cleanest: a specific mechanism is described.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

#### Coverage — Moba Legends: 5v5!

`a12fb168-3791-4d93-8cee-9b38fceb3059` · IN · 1★ · 2026-02-03

> If you want to get some serious anger issues and frustration,the game is for you.This game simply don't care about you at all,they only need money and frame(Obv it's a complete copy of league of legends). The match making, completely illogical,if you play good,game will give you bad teammates expecting you to carry and if you play bad,game will give you more bad teammates saying that it's so called "skill based matching". The only thing game will provide you is waste of time and energy

```json
{
  "label": "P_IllusionOfControl",
  "span": "The match making, completely illogical,if you play good,game will give you bad teammates expecting you to carry and if you play bad,game will give you more bad teammates saying that it's so called \"skill based matching\"",
  "rule_applied": "vs Alleged rigging",
  "rationale": "Matchmaking is described as tuned to the player's performance rather than to a fair pairing, which is difficulty on a hidden schedule."
}
```

- **Also on this review:** `S_Competition`
- **Why this example:** Rigging without randomness. The mechanism is matchmaking rather than an RNG, which the boundary lists but which is easy to miss.
- **Provenance:** adjudicated note; 2/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

### `P_AestheticManipulation` — Aesthetic Manipulation

> **Definition (codebook).** The use of deceitful questions or manipulation of emotions and subconscious desires, mainly based on aesthetical game elements.

#### Apt — Match Masters

`4a9d42d6-ad1d-4d3e-9cd1-5b16339524b0` · UK · 1★ · 2022-01-27

> This app was made to make money, not a fun game. It uses pretty much has made the entire game around the most profitable industry tricks for making whales. It has pop up to sell you in game assets constantly, it discounts first time buyers, it makes you feel like you've earned prizes, but you've earned the right to buy the prizes. You can spend money to gain a competitive advantage. The game itself is heavily determined by luck, basically it's just one big slot machine.

```json
{
  "label": "P_AestheticManipulation",
  "span": "it makes you feel like you've earned prizes, but you've earned the right to buy the prizes",
  "rule_applied": "vs UI Misdirection",
  "rationale": "The deception is in what the offer says - a prize presented as won when it is actually an offer to buy - so it is misleading wording, not placement."
}
```

- **Also on this review:** `M_PayToProgress`, `M_EasyToPurchase`, `M_NeverEndingLure`, `S_Competition`, `P_RewardMania`
- **Why this example:** The wording/placement split that separates this label from UI Misdirection, with both labels live in the same review.
- **Provenance:** adjudicated note; 2/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

#### Coverage — Chess - Play and Learn Online

`c2c60604-401f-416e-9489-a53cbaa6a968` · IN · 3★ · 2026-05-29

> I'm having a very good experience with the game but whenever I end a game it sometimes show that i played brilliant moves but when I review it it doesn't show any brilliant move this wastes my free review I'm so disappointed with this please fix this and there should also be a system to cancel friend requests cause sometimes someone don't accept or decline so I can't send request to anyone else

```json
{
  "label": "P_AestheticManipulation",
  "span": "I end a game it sometimes show that i played brilliant moves but when I review it it doesn't show any brilliant move this wastes my free review",
  "rule_applied": "vs UI Misdirection",
  "rationale": "The game tells the player they played brilliantly and then does not bear it out, so flattering feedback is used against what the player is actually shown."
}
```

- **Also on this review:** _none — single-label_
- **Why this example:** The emotional arm rather than the purchase arm - no money anywhere in the span. The lowest-support example in the set; see the support table.
- **Provenance:** adjudicated note; 1/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

### `P_OptimismAndFrequencyBiases` — Optimism and Frequency Biases

> **Definition (codebook).** Patterns that exploit cognitive biases and clustering illusions to overestimate event frequencies (e.g., winning streaks).

#### Apt — Jackpot Party Casino Slots

`41a6813f-af68-497a-ac7b-2532b4659186` · US · 2★ · 2026-02-28

> this game isn't that great! it's IMPOSSIBLE to win ANYTHING jackpot party! you come close, but NOTHING is won or any game with REAL MONEY or prizes are always just a few points or coins away from a jackpot

```json
{
  "label": "P_OptimismAndFrequencyBiases",
  "span": "you come close, but NOTHING is won or any game with REAL MONEY or prizes are always just a few points or coins away from a jackpot",
  "rule_applied": "definition",
  "rationale": "The span reports repeated near-wins as the player perceives them, with no claim that the game fixes outcomes."
}
```

- **Also on this review:** _none — single-label_
- **Why this example:** O&FB alone. The absence of a manipulation claim is what keeps Illusion of Control off, which is the boundary working in the negative direction.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

#### Coverage — Disney Solitaire

`03e1dcd5-9c13-4b7f-a9e1-d2ebdc8f5773` · UK · 1★ · 2026-03-18

> This is incredibly rigged; designed to get you hooked early to develop into impossibility, to suck you into paying money. You can be down to one card and have 10 cards left in your deck and end up going through those 10 cards and still have one card left. Even if you pay the astronomical coins to get another handful of cards, you still have the same card left. If you were to take an actual deck of cards, your chances would be significantly higher. Don't install this game. It's a money scam.

```json
{
  "label": "P_OptimismAndFrequencyBiases",
  "span": "You can be down to one card and have 10 cards left in your deck and end up going through those 10 cards and still have one card left. Even if you pay the astronomical coins to get another handful of cards, you still have the same card left.",
  "rule_applied": "definition",
  "rationale": "The one-card-away situation repeating is the player overestimating how close a win is, which is the clustering illusion the definition names."
}
```

- **Also on this review:** `M_Gambling`, `P_IllusionOfControl`, `P_RewardMania`
- **Why this example:** The paired case: contrast directly with the apt example. Same near-miss perception, but this review also claims the deal is rigged, so Illusion of Control is assigned alongside under R9. The rule that pairs them is written on Illusion of Control's side, so from here it is the definition.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

### `P_RewardMania` — Reward Mania

> **Definition (codebook).** Reward structures in which the mechanism of delivery, its complexity, its unpredictability, or the out-of-game activity it demands, is what sustains engagement, rather than the value of the reward itself. The player invests disproportionate cognitive effort, repeated attempts, or external activity in pursuit of the reward system.

#### Apt — Last War:Survival Game

`f9424404-513f-41a9-a3b9-a97670e89512` · UK · 1★ · 2024-10-07

> This game demands constant attention and is definitely falsely advertised, though they just added some new screenshots to try and avoid chargebacks. They lure you in and then the pressure to login every 2-3 hours 24/7 is constant with Arms Race or keep it open all day long so you don't miss treasure digs. Competing=who spends the most. This is a gacha game and 4x. You've been warned.

```json
{
  "label": "P_RewardMania",
  "span": "This is a gacha game and 4x",
  "rule_applied": "Gacha mechanics",
  "rationale": "Gacha is a chance-based delivery system, and no stake is described in the span, so the label applies without Gambling."
}
```

- **Also on this review:** `T_PlayingByAppointment`, `M_PayToProgress`, `S_FearOfMissingOutFOMO`, `S_Competition`
- **Why this example:** The indicator alone, and the 'vs Gambling' boundary resolving to Reward Mania by itself because no wager is named.
- **Provenance:** adjudicated note; 2/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

#### Coverage — Genshin Impact

`b0a2aece-2b3e-4026-966b-7836e3cfc6bc` · IN · 1★ · 2026-05-22

> I love the game, I invested so much time and effort in it. I genuinely love the art and designs but recently ever since Fontaine arrived the characters started becoming expensive because of premium team comps and some being locked and good for a specific team. old characters started falling off which I hope they could climb back up. And now the Meta shifts now are extremely fast.. and another issue is how much rewards we get.. it's so low each patch barely gives us enough to hit hard pity.

```json
{
  "label": "P_RewardMania",
  "span": "how much rewards we get.. it's so low each patch barely gives us enough to hit hard pity.",
  "rule_applied": "vs Reward described only by its value",
  "rationale": "Hard pity is the pull-count mechanism, so the span describes how rewards are delivered even though the reviewer's complaint is about their size."
}
```

- **Also on this review:** `M_DeceptiveLuxury`, `M_PowerCreep`, `P_EasyToGetHardToLose`
- **Why this example:** The hardest call for this label. The surface complaint is value, which alone would code nothing; naming the pity system is what makes it delivery.
- **Provenance:** adjudicated note; 2/3 coders assigned this label pre-adjudication; review-level coder agreement: split (the count above is for this label; the flag covers the whole review).

---

## Technical

### `Tech_FragmentedDownloads` — Fragmented Downloads

> **Definition (codebook).** “Fragmented Downloads” are characterized by designs that obscure the true storage requirements of the game until the game starts. This is deceptive because it targets mobile users who are cautious about their device’s storage capacity and foments a space monopoly by the app against competitors.

#### Apt — Shadow Fight 4: Arena

`a4d925c0-1248-4d12-ad93-5b8b1ced3b8d` · IN · 4★ · 2022-04-02

> This is probably the first fighting game I liked in my opinion I like the characters the moves but the downloading system sucks I thought I already download the file but I still get an additional download and when that happens the matchmaking is broken it doesn't works anymore cause there's a problem on my wifi but my wifi is good pls fix this😿

```json
{
  "label": "Tech_FragmentedDownloads",
  "span": "I thought I already download the file but I still get an additional download",
  "rule_applied": "Small advertised App Store size vs. large mandatory in-game download",
  "rationale": "The install appeared complete and the game then demanded more downloading, so the true requirement was not what was shown up front."
}
```

- **Also on this review:** _none — single-label_
- **Why this example:** The core deception - hidden storage cost - stated in one clause. Unanimous.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: unanimous.

#### Coverage — BGMI: FPS Battle Royale

`2d118652-5693-499a-8f3f-d02d0b405cd4` · IN · 5★ · 2026-06-15

> Dear BGMI Support Team, I am facing a persistent bug regarding the resource download system in the game. Maps, outfits, and other resource packs are downloading automatically in the background. The main issue is that even when I manually go to the settings and turn OFF the "Auto-Download" feature, the game ignores the setting and continues to download files automatically. This is consuming a lot of my internet data and causing storage issues on my device. Please fix this bug as soon as possible

```json
{
  "label": "Tech_FragmentedDownloads",
  "span": "Maps, outfits, and other resource packs are downloading automatically in the background. The main issue is that even when I manually go to the settings and turn OFF the \"Auto-Download\" feature",
  "rule_applied": "Missing animations / assets with in-place “downloading” prompts when packages are declined",
  "rationale": "The real storage and data cost is spread across resource packs pulled after install, and declining them does not stop the download."
}
```

- **Also on this review:** _none — single-label_
- **Why this example:** R11 discrimination. The reviewer files it as a bug, but the fragmented resource-pack architecture is the design; only the ignored setting would be the fault.
- **Provenance:** adjudicated note; 3/3 coders assigned this label pre-adjudication; review-level coder agreement: unanimous.

---

## Changes in this revision

`rule_applied` corrected on ten entries, all in the same two directions.

**Boundary rule cited from the wrong side** — the rule exists, but on the other label:

| entry | was | now |
| --- | --- | --- |
| `S_FearOfMissingOutFOMO` apt | `vs Fear of missing out` (lives on `T_PlayingByAppointment`) | `definition` |
| `P_OptimismAndFrequencyBiases` coverage | `vs Optimism and Frequency Biases` (lives on `P_IllusionOfControl`) | `definition` |

An audit of all 58 found no other instance of this.

**Boundary cited where the definition applies directly** — the rule says when *not* to assign, so it is not what carries these spans:

| entry | was | now |
| --- | --- | --- |
| `M_Gambling` coverage | `vs Intermediate Currency` | `definition` |
| `M_PowerCreep` coverage | `vs Incomplete on purchase` | `definition` |
| `M_WasteAversion` apt | `vs NONE` | `definition` |
| `M_WasteAversion` coverage | `vs NONE` | `definition` |
| `S_FriendSpamImpersonation` coverage | `vs Access Requests` | `definition` |
| `S_EncouragesAntiSocialBehavior` apt | `vs Reward for gameplay elements` | `definition` |

**Indicator corrected:**

| entry | was | now |
| --- | --- | --- |
| `M_DeceptiveLuxury` coverage | `Rarity Level` (a `[dp-enhancer]`, not an assigning indicator) | `Remedy Consumption + Artificial Scarcity` |

**Also:** `M_IntermediateCurrency` coverage now shows its R10 search; `M_Gambling` coverage no longer claims to need one, since the definition reading does not depend on resolving a term. Two indicator strings (`Can’t Pause or Save`, the Fragmented Downloads in-place-prompt indicator) were repunctuated to match the codebook byte for byte.

### Gold-set change

Checking `T_DailyRewards` coverage against its own boundary rules surfaced a gap in the gold set. The Daily Rewards `vs Playing by Appointment` rule requires **both** labels where the daily cycle gates progression rather than delivering a standalone reward, which is what the Kingshot review describes. `T_PlayingByAppointment` has been added to `c63003ef-dcdd-4ef2-a54e-0c9b0dfe931a`, sharing the `T_DailyRewards` span under R9.

Updated: `gold_set/gold_set.jsonl`, `validation/gold_set.jsonl` (kept byte-identical), `gold_set/gold_provenance_*.json`, `gold_set/gold_changes_*.csv`. Full rationale, the files deliberately left alone, and the downstream impact are in **`gold_set/post_adjudication_edits.md`**.

Gold label instances 136 → 137; `T_PlayingByAppointment` support 6 → 7; `counts.changed` 27 → 28. Coder votes and the display-only agreement block are untouched.

Both `gpt-5.6-luna` validation runs have been rescored against the corrected gold (stale stats deleted, `index.jsonl` rebuilt, raw run outputs untouched): micro-F1 high 0.7769 → 0.7737, xhigh 0.8031 → 0.8000. Precision and exact match unchanged; the whole delta is one added false negative per run on this review, which neither run had ever labelled correctly. Numbers in `gold_set/post_adjudication_edits.md`.

---

## Appendix A — NONE examples

Not requested, but v2's prompt carries a NONE exemplar (the `331c695a` matchmaking-wait counterexample) and v3 will need one too. The gold set has 7 true-None reviews. These two are the most instructive; say the word and I will work them up to the same standard, or leave v2's exemplar in place.

#### Lightning Link Casino Slots

`6ccb26a7-01e3-41a3-ba1a-bddba2063257` · US · 1★ · 2018-09-13

> Dont even waste you time with this app. I dont understand why you guys make these things so fun to play but impossible to ever win. I mean I know your trying to make money on the app but why would I ever come back and spend more money when it is impossible to when. Because of that this app is garbage!!!!!!!

```json
{
  "labels": []
}
```

- **Why this example:** Pure dissatisfaction with no mechanic named. 'Impossible to ever win' on a slots app is exactly the review a model will want to code `M_Gambling` or `P_IllusionOfControl` from prior knowledge of the genre — R4 forbids it, and R2 leaves nothing to attach. The strongest available guard against genre-priming.
- **Provenance:** ruled NONE on adjudication; the coders were split.

#### Flambé®: Merge & Cook

`3db5f780-e8e1-44a1-b538-63120ac046a6` · UK · 4★ · 2025-10-03

> Love this game, I would have given it 5 stars but as you go up in levels you start to run out of space on the board when making more complicated recipes. A storage option would be fab please developers. Also when winning items you have to move them onto the board in the order won, it would be really nice if we could select which ones we want to play in our own play order. Lastly, what is the inventory? I can't do anything with mine, lots of empty slots. Still the best Merge game in my opinion!

```json
{
  "labels": []
}
```

- **Why this example:** A minimal pair against the `M_WasteAversion` examples above. The board fills up, but nothing is bought and nothing is destroyed, and the storage option is a request rather than a feature — so no value is actually forfeited and R12 excludes the proposed mechanic. Same surface vocabulary as a positive, opposite answer.
- **Provenance:** ruled NONE on adjudication; the coders were split.

The other five true-Nones (`366f36fc`, `01d62acd`, `ef1623a3`, `340ca9ea`, `e2a95947`) are mostly short praise or bug reports; `e2a95947` is a usable minimal pair against `Tech_FragmentedDownloads` if you want a third.

---

## Appendix B — reviews consumed, for the record

`corpus-construction/validation/gold_set.jsonl` is byte-identical to the gold set. `guides/teacher-runs.md` describes the validation set as the reporting set, scored once, and `chi_sprint_plan.md` requires few-shot exemplars to be excluded from every eval set. Promoting these reviews into the v3 prompt consumes them for that purpose. The list below is what v3 would contain, so a disjoint eval set can be built against it later.

**45 distinct reviews** of the 75, carrying 58 label instances:

| review_id | game | labels used as examples |
| --- | --- | --- |
| `03e1dcd5-9c13-4b7f-a9e1-d2ebdc8f5773` | Disney Solitaire | P_OptimismAndFrequencyBiases (cov) |
| `042ee18e-d78e-4a0f-9cc2-2b1e10cc46e6` | Total Battle: War Strategy | P_EasyToGetHardToLose (cov); T_Grinding (cov); T_InfiniteTreadmill (cov) |
| `07dd542b-2a71-4772-8a68-538115f1f826` | Match Factory! | M_PayToProgress (cov); S_Reciprocity (apt) |
| `12105fcc-1fe5-46c6-8d77-d0bd2a11d6f1` | Bingo Blitz™️ - Bingo Games | P_EasyToGetHardToLose (apt) |
| `2471db11-2c61-415a-8af4-33b80a05c759` | Clash of Clans | M_PowerCreep (apt) |
| `2b915fb2-6ff4-4351-9b2f-e8db5661e0a5` | Dark War Survival | M_EasyToPurchase (apt) |
| `2d118652-5693-499a-8f3f-d02d0b405cd4` | BGMI: FPS Battle Royale | Tech_FragmentedDownloads (cov) |
| `2fd4ef32-a33b-44ed-a921-2889ba6e0375` | Ludo King® | P_IllusionOfControl (apt) |
| `31c8de21-5262-4e88-9d3c-feaffe08ec14` | Merge Cooking® | M_WasteAversion (cov) |
| `41a6813f-af68-497a-ac7b-2532b4659186` | Jackpot Party Casino Slots | P_OptimismAndFrequencyBiases (apt) |
| `443ba104-8abc-48c7-b8a7-b875ec52b05b` | Call of Duty®: Mobile | T_MandatoryMarathon (apt) |
| `49a53e7c-0564-46c6-995f-1d8bc418c80a` | MONOPOLY GO! | P_CompleteTheCollection (apt) |
| `4a9d42d6-ad1d-4d3e-9cd1-5b16339524b0` | Match Masters | M_NeverEndingLure (apt); P_AestheticManipulation (apt) |
| `50be85ac-f98c-4d2c-a70c-4465974027c0` | Township | T_DailyRewards (apt) |
| `57add346-8b93-4249-be50-1a39331cf79b` | RAID: Shadow Legends | M_DeceptiveLuxury (apt); S_ForcedFellowship (apt) |
| `6088dbf1-7d56-4302-945e-72fd73832609` | Cash Frenzy™ - Casino Slots | M_RecurringFee (apt) |
| `64e4aba6-ce6d-420a-b5cb-4422c11c4186` | Yalla Ludo - Ludo&Jackaroo | S_EncouragesAntiSocialBehavior (cov) |
| `681563e1-227c-4af2-8a1f-a145f3a795ca` | Pokémon GO | S_Reciprocity (cov) |
| `71d54398-28c7-4f4a-a67d-0914206f59c6` | GODDESS OF VICTORY: NIKKE | M_DeceptiveLuxury (cov) |
| `86de0e5d-8187-4dfd-b8c3-05e5b271d89e` | Real Cricket™ | T_Advertisement (apt) |
| `97c23c8d-b858-4afa-83b1-ebd08d56badc` | Dice Dreams™️ | M_NeverEndingLure (cov) |
| `a12fb168-3791-4d93-8cee-9b38fceb3059` | Moba Legends: 5v5! | P_IllusionOfControl (cov); S_Competition (cov) |
| `a4d925c0-1248-4d12-ad93-5b8b1ced3b8d` | Shadow Fight 4: Arena | Tech_FragmentedDownloads (apt) |
| `a59f5319-a1b7-4991-8c6b-d2d2ca56265c` | Fate/Grand Order (English) | M_Gambling (apt) |
| `ab9a6418-85dc-4e82-a279-bab6e1e5e148` | Carrom Pool: Disc Game | T_PlayingByAppointment (cov) |
| `b0a2aece-2b3e-4026-966b-7836e3cfc6bc` | Genshin Impact | M_PowerCreep (cov); P_RewardMania (cov) |
| `b4d6e64c-bd0c-49aa-9023-ed3f59bc63bf` | Match Masters | S_ForcedFellowship (cov); S_FriendSpamImpersonation (apt) |
| `b6745663-5486-4e5b-9066-8a889055d8bc` | Travel Town - Merge Adventure | M_IntermediateCurrency (apt) |
| `bc0d6ee6-1f01-4101-8c25-fc4da5a1ef7c` | Travel Town - Merge Adventure | M_WasteAversion (apt) |
| `c1a9f304-9cc1-4eb5-84f0-7988297fe423` | Lotsa Slots - Casino Games | M_Gambling (cov) |
| `c2c60604-401f-416e-9489-a53cbaa6a968` | Chess - Play and Learn Online | P_AestheticManipulation (cov) |
| `c63003ef-dcdd-4ef2-a54e-0c9b0dfe931a` | Kingshot | T_DailyRewards (cov) |
| `cbcde992-08aa-4bfb-a653-a944e4b733aa` | Mech Arena - Shooting Game | M_EasyToPurchase (cov); M_UIMisdirection (cov) |
| `ce1c6456-5d34-4001-a1a8-8b5991ef8ffb` | War Robots Multiplayer Battles | S_Competition (apt) |
| `ce92d6ba-cc5f-40a1-bc8e-27a82fa0a8f8` | 8 Ball Pool | T_Advertisement (cov) |
| `d8278e85-b5f2-45ef-88ad-ea3370a5195d` | Whiteout Survival | M_UIMisdirection (apt) |
| `d96bbc2c-73bb-4af5-9597-34a44117c7f5` | Fishdom | M_RecurringFee (cov) |
| `da13d098-3944-4e0b-aa94-c064a56edd83` | Mystery Town: Merge Games | M_PayToProgress (apt); P_CompleteTheCollection (cov) |
| `e92fc4f7-bdda-4f54-a8e2-aa591fbc7945` | Shadow Fight 4: Arena | S_FriendSpamImpersonation (cov); T_Grinding (apt) |
| `ee8d0008-1f3c-400d-bbbe-d29e8a7c0405` | Tiles Survive! | S_EncouragesAntiSocialBehavior (apt) |
| `f09401aa-1aef-4c8b-ac3a-92eec49af44d` | Homescapes | S_FearOfMissingOutFOMO (cov) |
| `f62c8a1f-91fc-4866-b267-977172fa2db3` | Toon Blast | T_InfiniteTreadmill (apt) |
| `f9424404-513f-41a9-a3b9-a97670e89512` | Last War:Survival Game | P_RewardMania (apt); S_FearOfMissingOutFOMO (apt); T_PlayingByAppointment (apt) |
| `fb70e577-e644-4af9-88a1-773476a5b805` | Free Fire: 9th Anniversary | M_IntermediateCurrency (cov) |
| `fe4ad63c-0bee-4c2e-814f-1e4f46f14d3d` | Township | T_MandatoryMarathon (cov) |

Plus 2 NONE reviews in Appendix A: `6ccb26a7-01e3-41a3-ba1a-bddba2063257`, `3db5f780-e8e1-44a1-b538-63120ac046a6`.

---

## What was built

1. `codebook_versions/adjudicated_examples.json` — these 58 examples as data (anchor label, role,
   review_id, span, rule_applied, rationale, plus the editorial note from this document).
2. `codebook_versions/codebook_adjudicated.json` — **v0.21**. Only `worked_examples` changed: 40
   uneven entries became 58, two per label across all 29. Every definition, indicator, boundary
   rule, counterexample and global rule is copied through byte for byte, so the label vocabulary is
   identical to v0.20 and the other scripts that read the codebook for its vocabulary stay on
   `codebook_final.json`.
3. `scripts/post-label/build_adjudicated_codebook.py` — builds (2) from (1), and re-asserts on every
   run that spans are verbatim, that each `rule_applied` names material listed under *that* label,
   that every label has exactly one apt and one coverage example, and that both pinned exemplars are
   still reachable.
4. `outputs/prompts/teacher_v3_{bare,boundary,full}.txt` — rebuilt, with manifests and SHAs.

**The pinned exemplars stay**, as you asked. That needed one accommodation: `build_prompt.py` pulls
the positive exemplar's review text out of the codebook by id, and `9d76ef06` lived only in Deceptive
Luxury's `worked_examples`. Replacing that list wholesale would have made `find_review()` exit and
taken the build with it. So Deceptive Luxury keeps three entries — the retained `9d76ef06` first,
then its apt and coverage examples. The retained one is never rendered (`render_label()` skips
anything in `used_ids`, which holds both pinned exemplars), so it costs nothing in the prompt and
every label still shows exactly two. It is flagged `retained_for` / `rendered_in_prompt: false`.

**The ablation is intact, and cheaper than expected.** Worked examples are gated on `full`, so
`teacher_v3_bare` and `teacher_v3_boundary` are **byte-identical** to their v2 counterparts — same
body SHA, same cache prefix. Only `full` moved: 24,066 → 29,947 tokens (+24%), about +$24 on cached
input across 200k reviews. Any existing v2 bare/boundary run is still valid for v3.
