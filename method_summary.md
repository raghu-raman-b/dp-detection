# Automated Detection of Player-Reported Deceptive Game Design Patterns from App Store Reviews

## Master Method Document & Task List — CHI Submission Cycle

---

## 0. Framing (FROZEN — do not reopen)

**Contribution sentence:** A validated, scalable pipeline that detects player-reported deceptive design patterns in mobile games from app store reviews, applied as a game-level audit across the top-grossing mobile game corpus, with review-level claims validated against expert human coding and game-level labels benchmarked against community-curated ground truth (darkpattern.games).

**Construct definition:** A label means _"this review reports the presence of this mechanic"_ — valence-independent. "I love the daily rewards" → `T: Daily Rewards`. Detection target is player-REPORTED patterns, not player-perceived (we did not measure perception) and not complaints (we are not Petrovskaya's construct).

**Explicitly OUT of scope (do not let these creep back in):**

- Awareness tool / player-facing system (motivation only, 2 sentences in intro citing Aagaard et al. 2022 + our prior interview finding)
- Taxonomy contribution (we adopt Zhang et al. 2025 verbatim)
- Severity beyond prevalence (severity = prevalence statistics only)
- Novel patterns from interviews (saved for future short paper)
- Interviews / thematic analysis

**Core validation logic (state explicitly in the paper):** Every claim is validated at its own granularity by an independent source.

- Review-level claims → human expert coders (gold set, month 2)
- Game-level claims → darkpattern.games community labels
- Teacher (LLM annotator) trustworthiness → pilot agreement on sequestered test split
- NO claim rests on LLM-agreeing-with-LLM. The evaluator agent is pipeline QC, never validation.

**Paper structure (Reviewer 1's skeleton + Reviewer 2's two-study prescription):**

- Intro → Related Work → **Study 1: Validated Detection Pipeline** (corpus, pilot, teacher, classifiers, gold-set eval) → **Study 2: Game-Level Audit & External Validation** (aggregation, darkpattern.games comparison, disagreement analysis) → Discussion (must exist — Reviewer 2 flagged its absence) → Limitations → Conclusion.
- Study 2 consumes Study 1's outputs; the relationship is explicit.

---

## 1. Label Space (FROZEN)

- **Canonical vocabulary:** Zhang et al. (2025) Table 2 meso-level patterns, verbatim, uneven counts per class (Monetary has 10; Temporal/Social/Psychological have ~6 each; Technical has 1).
- **High-level classes:** Temporal, Monetary, Social, Psychological, Technical (+ None as all-zeros).
- **Low-level patterns** (Evil Battle Pass, Premium Currency, etc.) = codebook indicators/examples under their meso parent, NOT labels.
- **DP Combos** = co-occurrences of meso labels, NEVER atomic labels. Zhang's own dataset codes "Trapping Starter Kit" as a label — we do not. A trapping-starter-kit review = Daily Rewards + Playing by Appointment (+ others as present). Combos are recovered analytically from co-occurrence → this is the "empirical validation of DP Combos at scale" secondary finding.
- **Multi-label throughout.** Both stages. Forced by DP Combos; single-label softmax would erase the phenomenon.
- **None rule (R1):** None unless a _specific mechanic_ is identifiable. "Cash grab, uninstalled" → None. "Cash grab, $20 for one skin" → Monetary.
- Vocabulary discrepancies exist in Zhang's own published data ("Fool's Gold Free", "Play Now or Pay Later" not in Table 2) → Table 2 is canonical; budget a mapping table for any cross-walk against their data or darkpattern.games.
- Label format convention: `HighLevel: MesoLevel` prefix scheme (mirrors Zhang's dataset; makes future cross-walks trivial).

---

## 2. Corpus Construction (Step 1)

**Sampling frame (executed):** Top-50 top-grossing F2P games per market from Sensor Tower, markets = US, India, UK, snapshot dated [JULY 11, 2026]. Precedent: Petrovskaya & Zendle (2022) used top-50 grossing; Zhang et al. scoped to F2P. DECISION: keep top-grossing (not genre-stratified top-free). See changes file for full rationale + limitation sentence.

**Store:** Google Play only (`gl=us/in/gb`, `hl=en`). Precedent: Petrovskaya.

**List hygiene (before scraping):**

- Resolve every title to Play Store `app_id`; dedupe by app_id, not name. Expect ~150 distinct apps after cross-market dedup.
- Fix known typos: "Toral Battle"→Total Battle, "Royal Kingdowm"→Royal Kingdom, "Garden Scapes"→Gardenscapes.
- Verify same-vs-different: Travel Town variants (same), Coin Master vs Coin Master Board Adventure (check), Free Fire "9th Anniversary" (seasonal title of Free Fire), Free Fire MAX vs Free Fire (India ban context — decide one entity or two, document).
- **Casino stratum:** slots/bingo/Teen Patti apps are kept (precedent: Zendle sampled casino; Petrovskaya found highest technique density there) but TAGGED `casino=1` so results can be reported with/without.

**Per-game pull:** up to ~5,000 most recent reviews per game per market. Keep: rating, date, helpful votes, market.

**Filter pipeline (in order), with counts logged at every stage (PRISMA-style flow figure — answers Reviewer 3's "data collection criteria not described"):**

1. Language ID (fastText/langdetect) → English only
2. Length floor: ≥10 words (NOT median — median discards half the corpus incl. short-but-codable reviews)
3. Exact-duplicate removal
4. Near-duplicate removal (normalize case/whitespace → MinHash or difflib ~0.9)
5. Strip markup only. KEEP emojis, punctuation, casing. No stopword removal, no lemmatization — LLM annotator needs raw phrasing.

**Labeling pool:** stratified sample to ~200k with per-game cap (~800) so mega-titles don't dominate.

**Binary filter placement (DECIDED):** Pilot sampling and all base-rate estimation run on UNFILTERED random samples. The legacy RoBERTa binary filter (0.849 recall) is optionally repositioned as a cost-reduction stage for the mass audit only, with recall propagated explicitly ("game-level estimates are lower bounds given filter recall of X"). Recompute whether it is needed at all given current API prices.

**Documentation:** snapshot source/date/chart-type verbatim; every filter's survival count; final pool size.

---

## 3. Pilot Study (Step 2) — instrument development, single-coder, reported as such

**Structure: 500 = 300 random + 200 targeted.**

- Random stratum → unbiased base rates (from these rows ONLY).
- Targeted stratum → keyword-seeded coverage of suspected-rare patterns (seeds: "battle pass", "pity", "energy", "VIP", "storage", "download more data", "guild", "invite friends", "gacha", ...). Zhang's own per-game counts confirm Social is sparse → seeding matters most there. Document seeding openly; strata analyzed separately.

**Why 500 (three converging constraints):**

- Statistical: ~200-review test split gives ±6–7pt 95% CI on agreement; ≥30–50 positives per high-level class needed for per-class metrics (engineered by the targeted stratum). Krippendorff: required n scales with rarity of rarest category.
- Precedent: Petrovskaya iterated codebook on 100 + 60 IRR reviews; Iyer et al. did 4,595 total with one coder; LLM-annotator lit (Gilardi et al. PNAS; Törnberg; Ziems et al.) validates on hundreds–low thousands. [Search for 2024–25 additions when writing.]
- Practical: ~1.5–2 min/review × 500 ≈ 13–17 hrs ≈ 3 evenings.

**Four outputs (nothing else produces these):**

1. Codebook v1 (rules emerge from real borderline cases)
2. Base-rate estimates (random stratum)
3. Prompt-engineering dev set
4. Teacher-trust number on sequestered test split

**Dev/test split:** ~300 dev / 200 test, stratified so both contain rare-pattern positives. Assign AFTER labeling completes, BEFORE any prompt work. FREEZE. Tune on dev only; one frozen-prompt run on test; report per-class F1 + chance-corrected agreement (per-label kappa; Krippendorff's alpha with MASI distance for multi-label). Calibration: human-human on adjacent tasks lands κ/α ≈ 0.6–0.8 (Petrovskaya: 0.36 first pass → 0.81 after codebook revision — expect a rough first pass).

**Process notes:** codebook drafted DURING labeling (running rules file); re-code first ~50 rows after codebook stabilizes (`pass` column tracks this; reportable as intra-coder drift if asked).

---

## 4. Codebook (living document, versioned)

**Section A — Global rules (ID'd so the sheet can cite them):**

- R1: None rule (no identifiable mechanic → None, regardless of sentiment intensity)
- R2: Presence is valence-independent
- R3: Past/removed mechanics ("they removed the energy system") → presence-at-time-of-writing = No (log it) [confirm on first real case]
- R4: Sarcasm/irony handling
- R5: Combos = co-occurrences, never labels
- R6: Review about a different game / ads for other games — coding rule
- (+Rn grown as encountered; each = ID + one-line statement + one worked example with review_id)

**Section B — Per-meso-label entries, five fields:**

1. Canonical definition — VERBATIM from Zhang (Table 2 + §4.1.x prose for novel patterns), with citation. Never paraphrase (this is the "we did not modify the taxonomy" defense made literal).
2. Review-text indicators — player vocabulary, complaint framings; low-level patterns live here as examples.
3. Boundary rules — disambiguation vs adjacent labels (Daily Rewards vs Playing by Appointment; Gambling vs Intermediate Currency for "pulls with gems"; Pay to Progress vs generic cash-grab-None).
4. Counterexamples — superficially-similar reviews that are NOT this label.
5. Worked examples — 2–4 review_ids from the pilot.

**Section C — Changelog:** version, date, change, whether it invalidates earlier coding ("v0.4: tightened X boundary; rows 1–112 re-checked"). Sheet's `codebook_version` column + this log = audit trail.

**Acceptance test:** a labmate who has never discussed the project can read the codebook, code 20 practice reviews, and land near your labels. That property IS the month-2 IRR number, which IS the answer to Reviewer 1.

---

## 5. Annotation Spreadsheet Schema

Identity: `review_id, app_id, game_name, market, review_date, star_rating, review_text` (immutable — fix pipeline, re-import; never edit cells).
Sampling: `stratum` (random/targeted), `seed_keyword`, `split` (dev/test, frozen post-labeling), `casino` tag inherited from game.
Labels: one binary column per meso label (exact canonical spellings, dropdown-validated); `labels_str` (formula-generated, never hand-typed); `none` (formula-checked against binaries).
Judgment metadata: `confidence` (H/M/L), `rule_applied` (rule ID), `borderline` (0/1), `rationale` (1–2 sentences for non-obvious calls — these become few-shot CoT exemplars in the teacher prompt), `pass` (1/2), `codebook_version`.
Mechanics: hidden validation sheet with label list / rule IDs / confidence values; dropdowns everywhere; no free-typed labels ever.

---

## 6. Teacher (LLM Annotator) — Step 3

- Terminology: **"LLM-assisted annotation" / "LLM-annotated corpus"** — never "synthetic" (reviews are real; only labels are model-produced; the old paper's terminology made the method sound weaker than it was).
- Prompt: full Zhang meso definitions + global rules + few-shot exemplars drawn from pilot rationales + CoT. Multi-label JSON output using the `HighLevel: MesoLevel` convention + rationale field. Prompt is an appendix artifact.
- Iterate on dev split only. Freeze. One run on test split → the reported validation number.
- If specific classes crater: targeted prompt revision on dev; fresh test run only if unavoidable; report honestly.
- **Evaluator agent:** second LLM pass with game context (store pages, wikis, gameplay summaries — do NOT play ~150 games) outputs plausible/implausible per label. Framed as label quality control in the pipeline. Never framed as validation.

---

## 7. Mass Labeling + Observability Scoping (Step 4 — reported as its own step)

- Frozen prompt → ~200k pool → per-pattern frequency plots.
- Patterns below floor → declared **not review-observable** → scoped out of classifier training → reported as a FINDING (which DPs are player-salient; extends Petrovskaya's prevalence-vs-salience to a structured ontology). Expected non-observable: Aesthetic Manipulation, Overloading, Polymorphic Currency, kawaii enhancers (visually-defined patterns).
- Pilot license: the pilot's validated prompt is what lets us distinguish "players never mention X" from "our prompt can't detect X." Ordering is pilot → freeze → mass label → scope. Never scope from unvalidated labels.
- This step decides which subclass heads exist. Never train a head on classes with a dozen real positives (the source of last cycle's F1 disaster).

---

## 8. Classifier Training + Evaluation (Step 5)

- **Architecture:** 1 + 4 cascade over Zhang hierarchy. Stage 1: multi-label over {T, M, S, P, Tech} (None = all zeros). Stage 2: four multi-label subclass heads (T/M/S/P), each invoked only when parent fires. Technical (single subclass: Fragmented Downloads) handled by stage 1 alone or a rule.
- **Ablation row:** flat multi-label (old architecture) vs cascade — know by week 3, not from a reviewer.
- **Models:** 4B–12B band (Gemma lightweight tier; whatever QLoRA fits on the 5070). Train 2–3 sizes → size-vs-performance curve (this curve + teacher ceiling = the entire "why distillation" argument, visually).
- **Imbalance as design input:** targeted-pilot rarity measurement → observability scoping → keyword-seeded oversampling for rare-but-observable classes → focal loss / per-class thresholds. Per-class support becomes a finding, not an apology.
- **Baselines table:** zero-shot base model; fine-tuned model(s); **teacher-direct on the gold set** (the ceiling row — essentially free, mandatory); optional keyword/regex floor.
- **Metrics:** per-class + macro F1, multi-label metrics, and **end-to-end cascade metrics** (stage-1 misses must not be hidden). Cost math: $/million reviews API vs local — one paragraph.
- Delete everywhere: top-3 label truncation (old paper's silent agreement-killer).

---

## 9. Month 2 — Gold Set (Step 6)

- 2–3 coders (labmates / teacher's students; ~15 hrs each), trained on the codebook, independently code 300–500 stratified reviews (stratified to include rare-pattern positives).
- Report IRR: Krippendorff's alpha (MASI distance) + per-label kappa. Adjudicate disagreements by discussion → adjudicated set = review-level ground truth for ALL model rows (fine-tuned, zero-shot, teacher-direct).
- **Design the protocol THIS month** (sampling plan, training procedure, practice set, adjudication rules) so month 2 is a two-week execution.
- Non-negotiable. darkpattern.games CANNOT substitute: unit mismatch (game-level labels vs review-level predictions → every unmentioned-but-present pattern scores as a false negative → garbage metrics + visible methodological confusion). Short paper lowers the scale bar (~300, 2 coders), not the existence bar.

## 10. Month 2 — Game-Level Aggregation + External Validation (Steps 7–8)

- **Aggregation rule stated in advance:** game badged for pattern P if ≥ k distinct reviewers report it (or proportion threshold). Sweep k → sensitivity curve figure → pick + justify. Do NOT tune k to maximize agreement with darkpattern.games (overfitting the validation target). Doubles as the severity-as-prevalence story.
- **darkpattern.games comparison:** overlap games only; vocabulary mapping table (shared ancestry with Zhang helps — the site is literally one of Zhang's ontology sources; say so, it preempts "why are these comparable"); agreement stats; **qualitative disagreement analysis** (a page of "games we flagged that the community didn't, and what the reviews said" = Reviewer 1's interpretive depth).
- **THIS WEEK:** check ~30 corpus titles against the site's catalog. If overlap < ~50 games, add the site's most-reviewed games as a documented supplementary stratum. Only fixable if caught now.

---

## 11. Literature-Justification Checklist (write these sections deliberately)

1. **Why reviews?** Ecologically valid, unsolicited, no demand effects, scale (Petrovskaya & Zendle 2022; Zagal et al. 2009; Iyer et al. 2026; review-mining lit in SE/HCI). Honest scope: we detect _player-reported_ patterns; observability analysis quantifies the gap.
2. **Why LLMs as annotators?** Scale (200k × 1 min ≈ 2 person-years); LLM-annotation literature (Gilardi PNAS; Törnberg; Ziems; search 2024–25); anchored by OUR pilot agreement number, not citations alone.
3. **Why this taxonomy?** Peer-reviewed, current, hierarchical, built partly from darkpattern.games (wires the step-8 comparison into the lineage); verbatim adoption = the response to last cycle's taxonomy critiques.
4. **Why detection/badges matter?** Aagaard's badge concept; players recognize mechanics but can't name patterns (Aagaard; Keleher et al.); regulatory momentum (EU action). Motivation layer only.
5. **Why distill vs. just prompting a frontier model?** Cost, deployability (continuous catalog-scale audits), reproducibility/auditability (open fine-tuned model vs drifting API). One short section; the size-vs-performance curve carries it.

## 12. Reviewer Critique → Answer Map (keep visible while writing)

| Last cycle's critique                                       | This cycle's answer                                                                                                                                                      |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Too many contributions, each underdeveloped                 | One contribution sentence; awareness/taxonomy/severity explicitly out                                                                                                    |
| Classifier performance very low                             | Observability scoping; no heads on starved classes; 4B–12B models; imbalance as design input; end-to-end metrics                                                         |
| Ground truth unreliable; needs trained experts              | Pilot (instrument) + month-2 gold set with IRR + adjudication (validation), at the right granularity                                                                     |
| Taxonomy fuzzy / not reproducible / "Others" too vague      | Zhang verbatim; canonical Table 2 label space; no Others bucket; combos as co-occurrences                                                                                |
| Layered patterns unsupported                                | Multi-label throughout → DP Combo co-occurrence stats at scale                                                                                                           |
| Ethics missing                                              | Exemption/waiver filed early; data-handling statement; Petrovskaya precedent for scraped-review ethics reporting                                                         |
| Structure confusing, methods/results interwoven             | Study 1 / Study 2, each design→validation→results                                                                                                                        |
| No discussion; no "so what"; no comparison to prior methods | Discussion section; baselines table incl. teacher ceiling; detection-methods related work (§2.2 salvaged) answers "what's missing in other methods vs ours" with numbers |
| Dataset/sampling undocumented                               | Sensor Tower snapshot doc; PRISMA-style filter flow; per-game caps; all counts logged                                                                                    |
| Unclear how system is used                                  | Badge pipeline explicit: review labels → k-threshold aggregation → game badges → store integration (Aagaard)                                                             |

## 13. Task List (sequenced)

**Week 1 (now):**

- [x] Game lists pulled (Sensor Tower, 3 markets, top-grossing F2P, dated)
- [ ] Resolve to app_ids; dedupe; fix typos; tag casino stratum; document snapshot
- [ ] darkpattern.games overlap check (~30 titles)
- [ ] File ethics exemption (IITG; check Mphasis if internship data policy applies)
- [ ] Build scraper; run; log all filter counts; assemble 200k pool (per-game cap)
- [ ] Build labeling web app + codebook app (prompts in prompts.txt)
- [ ] Codebook v0: verbatim Zhang definitions + seeded indicators for high-traffic labels

**Weeks 1–2:**

- [ ] Pilot sampling: 300 random (UNFILTERED) + 200 keyword-targeted
- [ ] Hand-label 500 (~3 evenings); grow codebook rules during; re-code first ~50; codebook v1
- [ ] Freeze dev/test split (300/200, stratified)
- [ ] Base-rate plots from random stratum

**Weeks 2–3:**

- [ ] Teacher prompt engineering on dev (few-shot from pilot rationales + CoT)
- [ ] Freeze prompt → one test-split run → per-class F1 + alpha/MASI (the reported number)
- [ ] Evaluator-agent QC pass built (game descriptions from store/wikis)
- [ ] Mass-label 200k; observability plots; scope label set; decide subclass heads
- [ ] Decide binary-filter inclusion for audit runs (with recall propagation) or drop

**Weeks 3–4:**

- [ ] Train cascade (2–3 model sizes) + flat ablation; oversample/focal loss for rare classes
- [ ] Baselines: zero-shot, fine-tuned, teacher-direct; end-to-end metrics; cost math
- [ ] Short-vs-full decision (~week 3; write toward full)
- [ ] Gold-set protocol doc (sampling, coder training, practice set, IRR + adjudication rules)
- [ ] Repro package skeleton (OSF/repo: codebook, prompts, code, counts)

**Month 2:**

- [ ] Recruit + train 2–3 coders; gold set 300–500; IRR; adjudication
- [ ] Evaluate all models on gold set (incl. teacher-direct ceiling)
- [ ] Aggregation rule + k-sensitivity sweep figure
- [ ] darkpattern.games mapping table + agreement + qualitative disagreement analysis
- [ ] Write: Study 1 / Study 2 structure; Discussion; Limitations (top-grossing frame; English-only; review-observable scope; temporal snapshot; filter recall bounds)

## 14. Salvage Manifest (from previous submission)

Keep: scraper stack; QLoRA/PEFT pipeline; JSON label format w/ rationale; 6k binary-filter dataset (repositioned); GPT labeling prompt as v0 seed; MASI; Related Work §2.2 nearly intact.
Drop: Player-Facing Awareness System + interviews + archetypes + 5 novel patterns; 31-pattern taxonomy + 11-way consolidation + "Others"; 2-expert gameplay validation; "validated against 400k" claim; top-3 truncation; "synthetic dataset" terminology.
Re-do: re-label old 26,832 reviews with new Zhang-targeted prompt (reviews fine, labels dead); 92% agreement number (proper split, per-class metrics, frozen prompt).
