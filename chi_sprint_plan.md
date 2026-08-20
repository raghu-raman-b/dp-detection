# CHI Sprint — 4-Day Execution Plan + Paper Rewrite Map
### Reference document · frozen as of Aug 16, 2026 · companion to method_summary.md

---

# PART 1 — THE FOUR DAYS

## Day 1 — Launch everything with external latency

### Block A (morning) — Validation study out the door [HIGHEST PRIORITY — its clock runs ~1 week]
- [ ] Sample validation set (~60–70 reviews) from the pilot pool:
  - every meso label ≥2 where pilot support allows
  - + 8–10 true-None reviews (coders must practice withholding labels)
  - + 4–5 multi-label combo reviews (combos are the hard agreement case)
  - EXCLUDE any review used as a few-shot exemplar in ANY prompt draft
  - EXCLUDE the blind-50 (they don't exist yet — keep the pools disjoint)
- [ ] Strip labels; load into labeling app in blind mode; verify export schema works end-to-end with a 2-review dry run
- [ ] Export codebook v0.16 → PDF
- [ ] Write 1-page coder instruction sheet:
  - task definition (multi-label; presence = valence-independent)
  - key rules verbatim: R1 (None unless a specific mechanic is identifiable), R2 (valence-independent), R5 (combos = multiple labels, never one)
  - 3 worked examples (one single-label, one combo, one None)
  - expected time ~2 hrs; how to save/export; who to ask what (nothing — they must not discuss reviews with each other or with you beyond codebook clarifications; log any clarification you give, it's a codebook gap)
- [ ] SEND to all 4 coders TODAY with soft deadline (+5 days) and schedule a 20–30 min sync (today/tomorrow): walk the codebook, do 5 practice reviews together (practice reviews ≠ validation reviews)
- [ ] Log: date sent, codebook version, set composition (goes in the paper's validation subsection)

### Block B (midday) — Bureaucracy + freezes
- [ ] Ethics exemption: file at IITG today if not filed (30 min form; multi-week latency; the paper needs the sentence). Note Petrovskaya cited a formal approval for scraped reviews — match that pattern in the writeup.
- [ ] Codebook freeze: changelog entry "v0.16 — frozen for validation study + teacher labeling." Coders and teacher use the SAME version. Any change after this = new version + documented impact.
- [ ] Snapshot documentation check: Sensor Tower source, chart type, 3 markets, exact date recorded verbatim in corpus log.

### Block C (afternoon/evening) — Blind-50 + prompt finalization
- [ ] Sample 50 fresh reviews: stratified across high-level classes, NOT in pilot, NOT in validation set, NOT few-shot exemplars.
- [ ] Code them cold (~1.5 hrs). ROLE: provider-selection ONLY. This set is never a reported number and dies after Day 2.
- [ ] Finalize teacher prompt template:
  - codebook definitions (verbatim Zhang) + global rules R1–Rn
  - few-shot exemplars w/ CoT drawn from pilot `rationale` column (log which review_ids — they're excluded from every eval set)
  - strict JSON output schema: labels as "HighLevel: MesoLevel" + per-label rationale
  - one template across providers; per-provider deltas only where API syntax forces it (log deltas)

## Day 2 — Provider bake-off → launch 200k

### Block A (morning) — Bake-off
- [ ] Run frozen prompt on blind-50 across: Claude, OpenAI, Gemini, DeepSeek, Kimi
- [ ] Log per provider (this becomes the "annotator model selection" table):
  - macro-F1, per-class F1 (only where n≥5), MASI
  - JSON parse/compliance rate (matters at 200k scale)
  - cost per 1k reviews, latency
  - NOT accuracy (multi-label + imbalance → None-spam scores high)
- [ ] Pick winner: quality-per-dollar, compliance as a hard gate. Save all raw outputs.
- [ ] DO NOT iterate the prompt per-provider against the 50 and then report the 50 anywhere. Selection set ≠ test set.

### Block B (afternoon) — Launch mass labeling
- [ ] 200k run on winner via batch API (~50% cost, hours-to-a-day turnaround)
- [ ] Chunked submission; resumable state; validate every response against schema; quarantine parse failures → one retry pass → log final failure count (reportable)
- [ ] Evaluator-agent decision (make it consciously, today):
  - BUILD: descriptions from store pages/wikis (never gameplay), plausible/implausible per label, runs over batches as they return, framed as pipeline label-QC in the paper
  - OR CUT: delete from method text entirely. A half-built component described in the paper is worse than an absent one.

### Block C (evening) — Pre-write the analysis
- [ ] Scripts ready before data lands: per-pattern frequency, co-occurrence (combo) matrix, per-game label profiles, per-market splits
- [ ] Table shells + figure stubs for tomorrow

## Day 3 — Observability → freeze → train → aggregate

### Block A (morning) — On returned labels (partial is fine)
- [ ] Frequency plots → OBSERVABILITY SCOPING: pick + record a floor (e.g., <0.1% of reviews or <200 positives) → patterns below = "not review-observable" → out of training, IN the paper as a finding
- [ ] Write down the scoped label list — it defines every downstream table
- [ ] Combo co-occurrence matrix → the DP-Combos-at-scale figure (nearly free, genuinely novel evidence for Zhang's claim)
- [ ] Eyeball 30–50 random teacher labels. Systematic breakage found now costs 2 hours; found after training costs the schedule.

### Block B (afternoon) — Training
- [ ] Build training data from scoped label set (teacher labels; oversample rare-but-observable classes; focal loss / per-class thresholds)
- [ ] Fine-tune priority order (cut from the bottom if GPU time runs out):
  1. Stage-1 multi-label (load-bearing)
  2. Subclass heads for classes that survived scoping
  3. Second model size (curve point)
  4. Flat multi-label ablation
- [ ] Evaluate vs HELD-OUT TEACHER LABELS (distillation fidelity) with end-to-end cascade metrics (never per-stage only)
- [ ] Human-truth evaluation slots in next week (adjudicated set) — leave the table row pending

### Block C (evening) — Study 2 spine + skeleton
- [ ] Game-level aggregation script: badge if ≥k distinct reviewers report pattern P; sweep k; sensitivity curve figure. DO NOT let this slide out of the draft — it is Study 2's spine and one script.
- [ ] Paper skeleton: all section headers, figure list, table shells with final column headers

## Day 4 — Write (nothing else)

Writing order (most-settled first):
1. Method / Study 1 — corpus (snapshot + PRISMA-style filter-count figure), pilot + codebook, annotator-selection table, mass labeling, observability scoping, architecture, training. Every number exists.
2. Results / Study 1 — observability findings, combo co-occurrence, model-vs-teacher table WITH teacher-direct ceiling row.
3. Study 2 — aggregation rule + k-sweep figure now; darkpattern.games section written structurally with mapping-table stub (execution next week).
4. Intro + Related Work — salvage old §2.2 nearly intact; new framing spine on top (see Part 2).
5. Discussion + Limitations — FULLY WRITTEN, not stubs. Their absence was an explicit rejection reason.

### Placeholder discipline
Every pending number = visible token + one sentence of committed method:
> "Inter-coder agreement across five coders (Krippendorff's α, MASI distance) = **[α-PENDING]**; disagreements were adjudicated by discussion."

Maintain PENDING.md: token → script that fills it → input it needs. Tokens:
- [α-PENDING] — 5-coder Krippendorff (you + 4), MASI
- [PER-CLASS-AGREEMENT-PENDING] — only where n permits; aggregate rest at high-level
- [TEACHER-VS-GOLD-PENDING] — frozen prompt, one run, adjudicated set
- [STUDENT-VS-GOLD-PENDING] — fine-tuned model on adjudicated set
- [DPG-AGREEMENT-PENDING] — darkpattern.games game-level stats + mapping table
- [ETHICS-REF-PENDING] — exemption reference number

---

# PART 2 — PAPER REWRITE MAP (old submission → new)

## KEEP (light edits only)
| Old part | Action |
|---|---|
| §2.2 Detection-methods related work | Keep nearly intact; it directly answers "what's missing in other methods vs ours" — now backed by the baselines table |
| Related-work citations generally | Keep; add Zhang 2025, Gray 2024 ontology framing at the top |
| Motivation: manipulative loop figure (Fig 1), freemium evolution, EU regulation paragraph | Keep with trims; this was praised |
| Scraper/fine-tuning infrastructure descriptions | Keep mechanics; update models/params |
| MASI as multi-label agreement metric | Keep; now alongside per-class F1 + Krippendorff |

## REWRITE (same slot, new content)
| Old part | New content |
|---|---|
| Title + abstract | New contribution sentence; claims scoped to what gold set + community comparison establish. Kill "validated against 400,000 reviews" phrasing — 400k application is deployment, not validation |
| Intro contribution list | ONE contribution + secondary findings (observability/salience, DP combos at scale). Awareness = 2 motivation sentences citing Aagaard + prior interviews |
| §3 taxonomy/groundwork | Replace 31-pattern custom taxonomy with verbatim Zhang adoption ¶ + label-space table + combo-as-co-occurrence rule. "We adopt without modification" is the whole defense |
| §4 method | Full new pipeline: corpus → pilot → teacher (selection + validation) → mass labeling → scoping → cascade training. Structured as Study 1 |
| Binary classifier subsection | Reposition: optional cost-reduction stage for audit runs w/ recall propagated ("lower-bound estimates given filter recall 0.849") — or cut if unused |
| §5 results | New tables: annotator selection; model-vs-teacher + teacher ceiling; observability; combos; k-sweep; gold-set rows pending |
| Expert validation (old 2-expert gameplay study) | Replace with: (a) 5-coder blind validation + adjudication [review-level], (b) darkpattern.games comparison [game-level]. One sentence may note the granularity lesson learned |
| Terminology (global sweep) | "LLM-annotated corpus" never "synthetic"; "player-reported" never "player-perceived"; "annotation" never "generation" |

## DELETE (do not migrate)
- Player-Facing Awareness System: architecture, 4 agents, Figs 2–3, interaction pipeline
- §4.2 interviews, archetypes (Veterans/Grinders/Watchers/Casuals), survey instrument
- 5 novel patterns from interviews (future short paper)
- 11-category consolidation + "Others" bucket
- Top-3 label truncation (everywhere, silently poisoned old agreement stats)
- 2-expert × 10-game agreement tables (Table 3, Fig 10)
- Any DeepSeek-agent-as-validator framing

## ADD (new sections that didn't exist)
- Study 1 / Study 2 explicit structure
- Annotator model selection subsection + table
- Observability scoping as method step + finding
- Aggregation rule + sensitivity analysis (Study 2)
- darkpattern.games comparison + qualitative disagreement analysis (Study 2)
- Discussion (full section: implications for badges/stores, salience vs prevalence, taxonomy operationalizability, deployment cost math)
- Limitations: top-grossing frame; English-only; review-observable scope; teacher-labeled training data; snapshot timing; filter recall bound (if filter used)
- Ethics + data statement; repro package pointer (codebook PDF, prompts, code, count logs)

---

# PART 3 — VALIDATION WEEK (parallel, after Day 4)

1. Coders return → compute α (all FIVE coders — your pilot labels on those rows count) → per-label agreement where n permits
2. Adjudication meeting (~1 hr): resolve disagreements by discussion; log rule clarifications → codebook changelog (reportable as "rules refined during adjudication: ...")
3. Adjudicated set = review-level gold
4. Run FROZEN teacher prompt once on gold → [TEACHER-VS-GOLD-PENDING]
5. Evaluate fine-tuned student(s) on gold → [STUDENT-VS-GOLD-PENDING] (same table as teacher ceiling)
6. darkpattern.games: overlap list → vocabulary mapping table (site ↔ Zhang meso; note shared ancestry — the site is one of Zhang's ontology sources) → game-level agreement stats → 1 page qualitative disagreement analysis ("games we flag that the community doesn't, and what reviews said")
7. Fill every token in PENDING.md; delete PENDING.md; final terminology sweep; submit-shape pass

---

# PART 4 — STANDING RULES (read when tired)

1. Nothing that touched prompt tuning appears in any reported evaluation. Blind-50 dies after Day 2. Few-shot exemplar reviews are excluded from every eval set.
2. If time forces cuts, cut in this order: ablation → second model size → evaluator agent → per-market analyses. NEVER cut observability scoping or the aggregation figure — they are the difference from last year.
3. Validation claims at the right granularity: review-level ↔ human coders; game-level ↔ darkpattern.games; never crossed.
4. Every count logged the moment it exists (filter survivors, parse failures, label frequencies). The flow figure writes itself or it never gets written.
5. Combos are co-occurrences. If a table cell ever says "Trapping Starter Kit," something regressed.
6. Codebook version stamped on everything: coder packets, teacher prompt, adjudication notes.
7. Any coder clarification you give during validation week = a codebook gap → changelog, don't hide it.
8. The paper claims what the data shows: player-REPORTED patterns in TOP-GROSSING F2P games on Google Play in three English-language markets, at a dated snapshot. Every widening of that sentence needs a defense you don't have time to build.
