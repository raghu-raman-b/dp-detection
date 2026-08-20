# MASTER FLOW — CHI Short Paper (≤5,000 words)
**Detecting player-reported deceptive design patterns from app store reviews**
Updated 2026-08-20. This document supersedes prior sprint plans. Frozen decisions are marked FROZEN; violating one is a regression and must be flagged, not silently absorbed.

---

## 0. THE CONTRIBUTION (FROZEN)

One contribution: a validated, scalable pipeline that detects player-REPORTED deceptive design patterns from Google Play reviews, plus a game-level audit, with every claim validated at its own granularity by an independent source.

- Review-level claims → validated against multi-coder human gold.
- Game-level claims → validated against darkpattern.games community labels.
- LLM-vs-LLM agreement is never validation.
- Terminology: "player-reported" (never "player-perceived"), "LLM-annotated corpus" (never "synthetic").
- Out of scope: awareness tool (2 motivation sentences citing Aagaard et al. 2022 only), taxonomy novelty, severity beyond prevalence, interview-derived patterns.
- Label space: Zhang et al. 2025 (Proc. ACM HCI, "First Contact") Table 2 meso-levels verbatim. 29 labels, 5 classes (Monetary 10, Temporal 6, Social 6, Psychological 6, Technical 1). Low-level patterns are codebook examples, not labels. DP Combos are co-occurrences of meso labels only. If any table ever contains "Trapping Starter Kit" as a label, combos have regressed.
- Claims scoped to: player-reported patterns, top-grossing F2P, Google Play, 3 English markets (US/IN/UK), dated snapshot.

---

## 1. DATA MAP (memorize this; every rule below refers to it)

| Set | Size | Labels | Role | May influence decisions? | Reported in paper? |
|---|---|---|---|---|---|
| 200k pool | ~200,000 | teacher (pending) | training corpus + audit corpus | — | prevalence, audit |
| Hand-labeled corpus | 611 | author (single-coder) | source of all sets below | — | corpus stats only |
| Codebook examples | 63 distinct ids | author, embedded in codebook | prompt content | yes (they ARE the prompt) | excluded from every eval |
| Eligible pool | 548 = 611 − 63 | author | sampling frame | — | — |
| **Validation set ("the 75")** | 75 | adjudicated multi-coder gold (pending) | REPORTING set | **NEVER** | teacher-vs-gold, student-vs-gold (headline) |
| **Choosing set ("the 50")** | ~50 from the 473 leftovers | author | ALL tuning: prompt edits, provider pick, examples-mode flag | yes — burn freely | never (selection-only) |
| Remaining leftovers | ~423 | author | secondary student eval (with 611−50) | no | student-vs-author (secondary) |
| Dev slice | carved from teacher-labeled 200k | teacher | student hyperparameters, early stopping, checkpoint pick | yes — burn freely | never |
| Student training set | 200k − 611 − dev slice | teacher | student training | — | — |

**The one rule that generates all others: any set used to make a choice (provider, prompt, flag, hyperparameter, checkpoint, threshold) can never be the source of a reported number.** Tune on cheap labels, report on expensive ones.

75-set composition (built, v0.20, seed 20260812): all 29 labels ≥2; 9 true-None; 17 multi-label; buckets fill 31 / rare 18 / rare-multi 12 / none 9 / combo 5; targeted 53 / random 22; UK 40 / IN 20 / US 15; 63 distinct games, max 3 per game; 17 five-star reviews. Accounting closes exactly: 620 lines = 66 codebook-example lines + 6 repeats + 548 eligible.

---

## 2. IMMEDIATE HYGIENE (before anything ships)

- [ ] Backfill `codebook_version` in all coded rows (currently hardcoded "v1.0") from `saved_at` against the codebook changelog dates.
- [ ] Draw the 50 choosing set with a script + fixed seed, stratified toward rare labels (leftovers contain zero FOMO and zero/near-zero FSI, DeceptiveLuxury, InfiniteTreadmill rows — stratify on what exists; accept that some rare labels are untestable during tuning). **Save the 50 ids permanently**: they are excluded from the reported student eval later.
- [ ] Confirm the 200k pool matches the frozen corpus spec (top-50 top-grossing F2P per market, Sensor Tower snapshot dated, Google Play, ~150 apps after app_id dedup, casino tagged as stratum; filters: English, ≥10 words, exact+near dedup ~0.9, markup-strip only). Record all counts for the PRISMA-style flow figure.
- [ ] Check reviews-per-game distribution in the 200k (Study 2's ≥k-reviewers badge needs volume per game).
- [ ] darkpattern.games overlap check: map ~30 of your titles against DPG's catalog. **If overlap is poor, Study 2 has no comparator — find out before training, not after.**
- [ ] File the IITG ethics exemption. One paragraph in the paper: public review data, no PII retained, quoted reviews paraphrased/anonymized, coders are volunteer colleagues, exemption reference. (2/3 prior reviewers flagged ethics; this is a known rejection vector.)

---

## 3. PHASE A — TEACHER PROMPT (compiled, not written)

**`build_prompt.py`**: renders codebook v0.20 JSON → prompt text. Config variables at top. Store the output's hash; `prompt_version` is tied to `codebook_version`. Hand-edits go into the codebook or the template, never the emitted prompt. Paper sentence earned: "the labeling prompt is compiled mechanically from the released codebook."

Prompt sections, in order:
1. **ROLE**: trained annotator applying a fixed codebook to ONE review.
2. **CONSTRUCT** (stated three ways — definition, rule, examples): label whether this REVIEW REPORTS THE PRESENCE of each mechanic. Presence not sentiment (R2); reviewer's words must describe the mechanic — "cash grab" alone = no labels (R1); you label the review, not the game.
3. **GLOBAL RULES**: R1–R13 condensed.
4. **WEB SEARCH POLICY (FROZEN)**: search ONLY to resolve the referent of a term the reviewer used (e.g., a named game mode). The mechanic itself must be described by the reviewer. Facts learned from search never justify a label on their own. Every search reported in output.
5. **LABELS**: per class; each label = one-line definition + condensed indicators. Counterexamples inline for boundary labels: Reciprocity (named send/gift/request mechanism required; vague "help each other" = none), FSI (game posts on user's behalf or prompts posting; social login alone = none), Competition-vs-ASB (ASB requires asymmetry or real-world-harmful conduct; ordinary PvP = Competition), Grinding-vs-O&FB (single retry after near-miss = O&FB, not Grinding).
6. **OUTPUT SPEC**: strict JSON, no prose. `{"labels": [...], "evidence": {code: "verbatim span"}, "invoked_web_search": bool, "search_query": null|str, "search_result": null|str}`. Enumerate all 29 legal codes; empty array = None (never a "None" string). Plain JSON-in-text (identical prompt across all 5 providers; no provider-specific structured-output modes).
7. **WORKED EXAMPLES**: three global (one positive review WITH labels, one angry review with NONE, one multi-label), drawn from codebook examples.

**EXAMPLES_MODE build flag**: `spans` (one quoted span per label, ~450 tokens) | `boundary` (full examples for boundary labels + the 3 global, ~+1k tokens) | `full` (all 63, ~+5–6k tokens). Start with `boundary`; escalate to `full` only if the 50 shows rare-label errors concentrated where examples were withheld. Prompt budget target 3–5k tokens (`boundary`); every extra 1k tokens = 200M tokens over the mass run.

**Inputs shown to model: review text + game name. NOT the star rating** (R2 protection; a visible 1-star is a shortcut to over-labeling). Apply the same blinding in the coder app.

Per-review calls (decision independence, attributable failures), temperature 0.

---

## 4. PHASE B — BAKE-OFF (on the 50, and only the 50)

Providers: Claude, OpenAI, Gemini, Kimi, DeepSeek. $5 credits each. Web-search capability required.

All prompt drafting, re-runs, examples-mode escalation, and provider comparison happen on the 50. Iterate by reading **disagreement rows**, not the aggregate: bucket errors as R1 violations (labeling the game not the review), valence errors, code hallucinations, span-vs-search violations, JSON non-compliance — each bucket points at the prompt section to tighten. Aggregate F1 is not actionable.

Selection table (never reported as evaluation; may appear as a methods table labeled selection-only):
- macro-F1 vs author labels on the 50
- MASI similarity
- schema compliance rate (failures after 1 retry)
- search invocation rate
- throughput (reviews/min, incl. rate limits)
- cost per 1k reviews (incl. search calls)
- prompt caching support (a criterion, not a footnote — it dominates mass-run cost)
- **performance per dollar**

**Freeze artifacts**: exact prompt text + hash, provider, model version string, temperature, search settings, date. Provider models change silently; the paper and repo need the precise configuration.

**Pre-registered go/no-go** (decide threshold BEFORE looking): abort mass run if winner's macro-F1 on the 50 < [set it now]. One look. Iteration after freeze is forbidden.

---

## 5. PHASE C — MASS LABELING (200k)

Start immediately after freeze — starting is the commitment device; once running, nothing seen later can contaminate the prompt.

- No filtering before base-rate estimation. The old RoBERTa binary filter (recall .849) is only an optional cost-reduction for later audit runs, with recall propagated into estimates — never before prevalence is measured. (FROZEN)
- Log per row: labels, evidence spans, search flag/query/result, model version, prompt hash, timestamp, retry count.
- Rolling QC: schema-failure rate, label-frequency drift over time (provider-side model updates show up here), search invocation rate.
- Teacher labels the 611 rows too (harmless; they are excluded downstream by id).

---

## 6. PHASE D — HUMAN VALIDATION STUDY (parallel with C)

4 external coders + author = 5 coders on the 75. (Adequate: above typical CHI practice of 2–3.)

Protocol (FROZEN):
- Training: 5 practice reviews (not from the 75, not codebook examples), rule-level discussion allowed.
- Then SILENT independent coding of the 75 in the labeling app, `actual_labels` hidden, **star rating hidden**.
- Clarifications during coding answered at rule level only; every clarification logged as a codebook gap.
- No recoding the same 75 after seeing α. If α disappoints: report it, adjudicate, discuss — never retrain-and-rerun.

Analysis:
- Krippendorff's α with MASI distance across 5 coders; report with bootstrap CI.
- Per-class α; per-label only where support permits (support 2 per label is noise).
- Thresholds for framing: ≥0.8 firm, ≥0.667 tentative (Krippendorff). Do not hard-code 0.7 as pass/fail; for a 29-label multi-label construct, ≥0.6 with documented adjudication is defensible.
- ~1hr adjudication meeting → adjudicated labels = review-level gold.

Paper drafting proceeds in parallel with [PENDING] tokens + PENDING.md: [α], [teacher-vs-gold], [student-vs-gold], [DPG agreement], [ethics ref].

---

## 7. PHASE E — TEACHER-VS-GOLD (one number, one look)

Frozen winner runs the 75 once (inference may run anytime after freeze; **scoring happens once, against adjudicated labels, after Phase D**). Report per-label + macro; describe the 75 as "stratified to cover all 29 labels" — never as a random sample; micro-averages over an enriched set are inflated and are not reported as accuracy claims.

Baselines table (FROZEN): zero-shot student, fine-tuned student, teacher-direct ceiling — all end-to-end.

---

## 8. PHASE F — OBSERVABILITY SCOPING (mandatory; do not skip)

Between mass labeling and training:
- Per-label frequency plot over the teacher-labeled 200k.
- Support floor set BEFORE seeing any student results (e.g., ≥N teacher positives).
- Labels below floor = "not review-observable at scale": scoped out of student training and out of audit detection claims; still reported in prevalence with wide uncertainty.
- Reported as a FINDING: players report economy-level manipulation extensively, interaction-level deception rarely (prevalence vs salience; extends Petrovskaya & Zendle). Expected candidates from corpus evidence: UIMisdirection, FSI, AestheticManipulation, FragmentedDownloads (zero random-stratum support), FOMO (3/611).
- Artifacts: one Methods sentence, one frequency figure, one Findings paragraph.

This step protects macro-F1 (prior rejection: low classifier F1) and converts a weakness into a result.

---

## 9. PHASE G — STUDENT

- Architecture (FROZEN): 1+4 multi-label cascade. Stage 1: five classes, None = all-zeros. Stage 2: subclass heads only for classes surviving scoping. Flat multi-label as ablation if time.
- Gemma-class 4B–12B, QLoRA, RTX 5070.
- Training set: 200k − all 611 − dev slice. Dev slice carved from teacher-labeled data BEFORE training; all hyperparameter, early-stopping, and checkpoint decisions happen there and only there.
- Report end-to-end cascade metrics, never per-stage only.
- Evaluation:
  - **Headline: student vs adjudicated 75** (strongest labels in the house).
  - Secondary: student vs author labels on 611 − 50 = 561 ("did it internalize the codebook"), stratified random vs targeted; per-label only where support permits; aggregate over keyword-seeded rows is not a natural-distribution estimate and is labeled as such.
- Student web-search tools: primary reported eval WITHOUT tools (deterministic); tool-enabled mode is the HF demo configuration, reported descriptively.

Cut order under time pressure (FROZEN): ablation → 2nd model size → evaluator agent → per-market splits. NEVER cut observability scoping or the aggregation figure.

---

## 10. PHASE H — STUDY 2 (game-level audit + external validation)

- Run the pipeline over per-game review sets from the 200k.
- Badge rule: game flagged for pattern P if ≥k DISTINCT reviewers report P. Sweep k; sensitivity figure. **Never tune k to maximize DPG agreement** (FROZEN).
- darkpattern.games comparison: vocabulary mapping table (your 29 ↔ DPG categories; shared ancestry — DPG is one of Zhang's ontology sources, say so), agreement stats at game level, 1 page qualitative disagreement analysis (why the crowd and the pipeline diverge is a finding, not an error bar).
- Scoped-out labels (Phase F) carry no badge claims.

---

## 11. PAPER (≤5,000 words)

Structure: Intro (1 contribution, 2 sentences of awareness motivation) → Related work → Study 1: corpus → codebook → validation study → teacher selection (selection-only, on the 50) → mass labeling → scoping → student training → gold eval → Study 2: aggregation + DPG → Discussion (full section) → Limitations (full section) → Ethics paragraph. Methods and results NOT interwoven (prior rejection reason).

Figures carry the load (colorful, high-res, light on text, no em dashes; companion plain-text stats file for each): PRISMA-style flow, agreement/α table, label-frequency + scoping figure, k-sensitivity figure. Supplementary: per-label tables, DPG vocabulary mapping, prompt text, codebook.

Limitations to state: top-grossing frame, English-only, snapshot-dated, search-dependent labels reflect web state at labeling time (logged per row), enriched 75 not a random sample, secondary eval labels single-coder.

Release artifacts (part of the contribution): HF demo (student + tools), repo (codebook v0.20, compiled prompt + hash, stats files, figures, id lists for all set exclusions).

---

## 12. STANDING RULES (recite before every session)

1. Nothing that touched prompt tuning, provider selection, or hyperparameter choice appears in any reported evaluation.
2. The 75 is scored exactly once, against adjudicated labels, by the frozen configuration.
3. Search resolves referents; it never supplies mechanics.
4. Star ratings are hidden from every labeler, human or model.
5. Observability scoping and the aggregation figure are never cut.
6. Combos are co-occurrences of meso labels; atomic combo labels are a regression.
7. Base rates are estimated before any filter touches the pool.
8. Every exclusion is an id list in the repo, not a sentence in prose.

## 13. DEPENDENCY ORDER (today → deadline)

TODAY: hygiene items (§2) + build_prompt.py + bake-off on the 50 + freeze + start 200k + recruit coders + prep coder materials + DPG overlap check + file ethics.
THIS WEEK: coder study runs (D) while 200k labels (C); draft with [PENDING].
THEN: adjudication → α → teacher-vs-gold (E) → scoping (F) → student (G) → Study 2 (H) → fill PENDING → polish.
Calendar check: measure teacher throughput during the bake-off and compute 200k wall-clock TODAY; if it exceeds the window, the RoBERTa pre-filter for the audit corpus (with recall propagated) is the sanctioned lever — never skipping scoping or validation.
