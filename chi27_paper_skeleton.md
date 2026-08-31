# Paper Skeleton — CHI 2027 Full Paper (~7,500 words)

**Working titles (pick one, refine later):**
1. *Labeling the Store: Automated, Review-Driven Detection of Deceptive Patterns for App Store Disclosure*
2. *From Reviews to Labels: Operationalizing Deceptive-Pattern Disclosure for Mobile Games at Scale*
3. *Leveling the Field, Revisited: A Self-Reliant Pipeline for Game-Level Deceptive Pattern Labels from Player Reviews*

**Legend:** `[KEEP]` = salvage from old paper (light edit) · `[REWRITE]` = old material, new framing · `[NEW]` = write fresh · `[PENDING: step N]` = waiting on experiment · `(~N w)` = word budget

**One-sentence thesis (memorize this, every section serves it):**
> Aagaard et al. proposed disclosure labels for deceptive patterns in app stores; we show, for the first time, that such labels can be generated automatically and reliably from player reviews alone — no gameplay, no experts in the loop, no crowd-sourcing — making disclosure feasible at app-store scale.

---

## Abstract (≤150 words) `[NEW]`

Formula, sentence by sentence:
1. **Problem:** Deceptive patterns pervade mobile games (95% of trending apps — Di Geronimo), yet players have no way to know before installing.
2. **Vision:** Disclosure labels in app stores have been proposed (Aagaard) but never operationalized — expert audits and crowd-sourcing don't scale.
3. **Method:** We present the first automated pipeline that produces game-level deceptive-pattern labels from player reviews, grounded in a peer-reviewed ontology (Zhang et al.) via a rigorously validated codebook (21 iterations, 4-coder agreement, adjudicated gold set).
4. **Results:** LLM labeling reaches micro-F1 `[PENDING: step 8]` against the gold set; we release a 200k-review dataset `[PENDING: step 9]`; game-level labels agree with crowd-sourced ground truth at `[PENDING: step 10/12]`.
5. **Implication:** Disclosure labels are technically feasible today, for any app store, in any review-rich domain.

---

## 1. Introduction (~1,000 w)

**Para 1 — The hook.** `[KEEP — the forum-post/Reddit analogy + Fig. 1 from old paper]` Open with the anonymized forum post describing the Power Creep loop ("just how games work"). Add the scale stats: 8.45B installs in India [old ref 24], Di Geronimo's 95% / 7.4 patterns per app [old ref 7]. End para: the player who wrote that post had no way of knowing before they installed. *(Keep the cycle figure — it was one of the best assets in the old paper.)*

**Para 2 — The regulatory moment.** `[KEEP, tighten]` EU design restrictions to protect children [old ref 9]; loot-box regulation struggles (Belgium ban circumvented — Xiao 2023, take from Zhang et al.'s ref list). Regulators are acting, but regulation moves slower than monetization design evolves. What players need is *point-of-decision* information.

**Para 3 — The proposed solution nobody has built.** `[REWRITE]` Aagaard et al. proposed badge-based disclosure in app stores — like nutrition labels for games. Note honestly: proposed in an Extended Abstract, never operationalized. Why not? Three dead ends: (a) expert audits don't scale (60 games took us weeks — you can say this from experience); (b) crowd-sourcing (darkpattern.games) is accurate but sparse and slow; (c) automated UI detection (UIGuard, AidUI) sees only static screens, but game deception is temporal, layered, experiential [Zagal; old §2 argument — KEEP this reasoning].

**Para 4 — The insight.** `[NEW]` Players already document these experiences, voluntarily, at massive scale: app store reviews. Petrovskaya & Zendle showed reviews surface problematic monetization — but manually, on a sample. Two things have changed since: (1) a rigorous, peer-reviewed ontology of deceptive game design now exists (Zhang et al. 2025), and (2) LLMs have become validated annotation instruments (Gilardi et al.; Törnberg). The missing piece is a pipeline connecting them — with the validation chain to trust its output.

**Para 5 — What we did (RQ + contributions).** `[NEW]` One RQ: *Can player reviews, labeled automatically against an established ontology, produce reliable game-level deceptive-pattern labels suitable for app store disclosure?* Then contributions, exactly four:
- **C1 — Validated annotation method:** codebook operationalizing Zhang et al.'s ontology for review text (21 iterations, IRR study with 4 coders, adjudicated gold set). `[PENDING: step 7 → α value]`
- **C2 — Dataset:** first human-validated, LLM-annotated corpus of deceptive-pattern labels — 200k reviews, 88 games, 3 markets. `[PENDING: step 9]`
- **C3 — Benchmark:** systematic evaluation of prompting strategies and models, plus a distilled 4B model showing the pipeline runs without proprietary APIs. `[PENDING: steps 8, 11 — step 11 is the DESCOPE CANDIDATE; if cut, fold into Discussion as future work]`
- **C4 — Feasibility evidence:** game-level labels validated against crowd-sourced ground truth (darkpattern.games), with a threshold analysis for when a review signal becomes a game label. `[PENDING: steps 10, 12]`

**Para 6 — Roadmap sentence.** `[NEW]` One or two sentences max.

---

## 2. Related Work (~1,400 w)

*Narrative arc of this whole section: "the pieces exist; nobody has assembled them."* Each subsection ends by naming what it contributes to your pipeline and what it lacks alone.

### 2.1 Deceptive Patterns in Games `[KEEP ~60%, restructure]`
- Brignull → Gray et al. 2018 taxonomy → Gray et al. 2024 ontology. `[KEEP from old §2.1]`
- Games as a distinct context: Zagal; Montefiore & Formosa; Hadan (Overwatch); King & Delfabbro predatory monetization; King et al. patents. `[KEEP]`
- Mobile prevalence: Di Geronimo; Niknejad; Petrovskaya & Zendle 35 techniques. `[KEEP]`
- **New anchor paragraph** `[NEW]`: Zhang et al. 2025 — three-level ontology (high/meso/low), integrates Zagal, Sousa & Oliveira, King, Hadan, darkpattern.games; introduces DP Combos and Enhancers; adopts ACM "deceptive patterns" terminology (adopt it throughout your paper too — retire "manipulative patterns"). Close: *this ontology gives us, for the first time, a stable target vocabulary for automated labeling — but it was built from expert gameplay observation, and whether it transfers to player-written text is an open question we answer in §4.*

### 2.2 Automated Detection of Deceptive Patterns `[KEEP ~70%]`
- Keep the old five-category survey (crowd-sourced repos, domain-specific, UI-based, LLM-driven, behavioral simulation): Mathur 11k crawl; Chen UIGuard; Mansur AidUI; Soe cookie banners; Sazid GPT-3; Kocyigit DeceptiLens; Mills & Whittle personas; Chen app exploration; Kollnig & Schäfer mitigation. `[KEEP — this was your strongest old section]`
- **Rewrite the closer** `[NEW]`: end with a positioning paragraph (or small table — this answers old Reviewer 2 directly): static UI methods can't see temporal/experiential deception; simulation uses synthetic personas, not real players; repositories don't scale. None produce *game-level, store-ready* output.

### 2.3 Player Reviews as a Window into Play `[NEW, short]`
- Petrovskaya, Deterding & Zendle CHI'22 — review content analysis for problematic microtransactions (your direct methodological ancestor; manual, sample-scale).
- App review mining lineage (one or two cites: e.g., Maalej et al. on review classification — check what's standard).
- Close: reviews carry the signal; the bottleneck was always labeling cost.

### 2.4 LLMs as Annotation Instruments `[NEW — this was MISSING from the old paper and is now core]`
- Gilardi, Alizadeh & Kubli 2023 (PNAS) — LLMs outperform crowd workers on annotation. **← you did not cite this before; add.**
- Törnberg 2023 `[KEEP ref]`; Ziems et al. 2024, *Can LLMs Transform Computational Social Science?* (Computational Linguistics). **← add.**
- Pangakis et al. 2023, *Automated Annotation with Generative AI Requires Validation.* **← add; it is literally your methodological thesis.**
- Multi-label classification with LLMs `[KEEP old refs 36, 46]`.
- Close: the field's consensus is that LLM annotation is usable *iff validated against human gold data* — which frames your entire §4–5 as best-practice, not convenience.

---

## 3. Study Context & Data (~700 w)

**3.1 Design rationale** `[NEW, 1 para]` Why reviews (voluntary, first-hand, scale, already at the point of decision — the store page); why these three markets (IN/UK/US = English coverage + regional spread); why Android/Play Store. One honest sentence pre-empting the epistemics: reviews are complaint-biased and self-selected — a *feature* for detecting negative experiences, a limitation for absence claims (fully treated in §8).

**3.2 Corpus construction** `[NEW — you have all numbers]`
- Top 50 games × 3 regions → 150 → deduped to **88 games**.
- Scraped **760,839** reviews → filter pipeline: English → ≥10 words → dedupe → **428,241** → random sample to **200,000**.
- **Table 1: filter pipeline** (stage, criterion, count remaining, % retained). Cheap to make, reviewers love it, answers old Reviewer 3's "data collection criteria not described" verbatim.
- Ethics-relevant facts stated here: public reviews, no usernames/PII retained, quotes paraphrased (see §Ethics note).

---

## 4. A Codebook for Deceptive Patterns in Review Text (~1,100 w)
*This section is contribution C1 and your inoculation against the old "fuzzy taxonomy / weak ground truth" criticism. Narrate the transfer problem honestly — it's a finding, not a confession.*

**4.1 Starting point** `[NEW]` Zhang et al.'s ontology as source vocabulary; final label space = **29 labels** — state exactly how you got from their table to 29 (merges? drops? which levels — meso? low?). `[DECISION NEEDED: write the explicit crosswalk; put full table in Appendix A]`

**4.2 Iterative development** `[NEW]` v1 = verbatim literature definitions → hand-label 300 random reviews → refine with examples, counter-examples, boundary rules → 311 targeted reviews (keyword-sampled) to support rare labels → total **611** hand-labeled → **v21**. Give 1–2 concrete evolution examples ("Pattern X, defined by Zhang et al. via UI observation, manifests in reviews as complaint-type Y; we added boundary rule Z"). **Figure 2: codebook evolution timeline** or a worked before/after definition box.

**4.3 Reliability** `[PENDING: step 7 — TODAY'S CRITICAL PATH]`
- 75 reviews sampled evenly across labels; **4 independent coders**; Krippendorff's **α = [PENDING]** (+ MASI for set-valued comparison — cite Passonneau `[KEEP ref 39]`).
- Adjudication by discussion → **gold-75**. Only phrasing changes flowed back into the codebook (state this — it shows the construct was stable).
- Framing if α is moderate: interpretive, multi-label task; compare against IRR reported in Zhang et al. / Petrovskaya & Zendle; the adjudicated gold set, not raw agreement, is the evaluation target.
- **Leakage statement (verbatim, somewhere in 4.3 or 5.1):** *"No review in the gold set appears as an exemplar in any prompt, and all 611 codebook-development reviews were excluded from model training data."*

---

## 5. LLM Labeling: Can Models Apply the Codebook? (~1,100 w)

**5.1 Setup** `[NEW]` Task = 29-label multi-label classification. Codebook → prompt. Four prompt formats × reasoning levels, tested on tuning-50 (sampled from the 611, disjoint from gold-75) against single-coder labels. Result: full prompt (definitions + examples + boundary rules) wins. **Table 2: prompt ablation.** *(Nice narrative beat: the model needs the boundary rules just like human coders did — the codebook is the transferable artifact, not the model.)*

**5.2 Model selection** `[NEW — you have these numbers]` Cost-vs-performance across providers on tuning-50: best model micro-F1 **0.845**, MASI **0.751**, Jaccard **0.815**; 8 models ≥ 0.800 micro-F1. **Figure 3: cost vs. performance scatter.** One sentence on why MASI/Jaccard matter for set-valued labels. `[Model names: check anonymization implications — naming commercial models is fine and normal.]`

**5.3 Gold-set evaluation** `[PENDING: step 8 — THE headline number]` Top-5 models × updated (validated) prompt × gold-75. **Table 3: per-model micro/macro-F1, MASI, Jaccard.** Per-label metrics only where support permits; say so explicitly (29 labels over 75 reviews = thin tails; foreground set-based metrics).

**5.4 Distillation** `[PENDING: step 11 — DESCOPE CANDIDATE]` Fine-tune 4B on the 200k LLM-labeled corpus (611 excluded); evaluate on gold-75. Purpose sentence: proves the pipeline runs open-weight, on-prem, API-free — a store operator could self-host. `[If time fails: one paragraph in Discussion instead; do NOT let this block submission.]`

---

## 6. The Corpus at Scale (~600 w) `[PENDING: steps 9–10]`

- Best model labels 200k − 611 reviews → **the dataset (C2)**.
- **Figure 4: label frequency distribution** across corpus. **Figure 5: co-occurrence matrix/graph** — narrative callback: layering/DP Combos, predicted by Zhang et al. and your old interviews, now visible at corpus scale (e.g., Power Creep × Grinding, or whatever the data shows).
- 2–3 headline observations max; resist writing a second results section here. Market-level differences (IN vs UK vs US) only if the effect is clean — otherwise one sentence + future work.

---

## 7. From Reviews to Store Labels (~800 w) `[PENDING: steps 10, 12]`
*The payoff section — the whole paper has been building here. NOT cuttable.*

**7.1 Aggregation** `[NEW]` A game receives label L if signal(L) ≥ k. Define signal (proportion? count? normalized by review volume?) `[DECISION NEEDED]`. **Sweep k**, plot precision/recall vs. darkpattern.games ground truth — k becomes a *finding* (choose the operating point), not a magic constant.

**7.2 Validation against crowd-sourced ground truth** `[NEW]` Aggregate ALL corpus games; intersect with darkpattern.games coverage (**n = [PENDING] games** — push for every overlapping game, not one). Label crosswalk Zhang-ontology ↔ darkpattern.games in **Appendix B** (mostly exists — Zhang et al. built partly from that site). Report agreement `[PENDING]` + honest divergence analysis: where the pipeline sees patterns the crowd missed (recency! reviews update; crowd labels go stale) and vice versa (patterns invisible in review text).

**7.3 Case study** `[PENDING: step 9-adjacent]` One top game, *all* reviews ever → its store label card. **Figure 6: mock store listing with generated labels** — the money shot; make it look like a real Play Store card. This is the image reviewers remember and tweet.

---

## 8. Discussion (~900 w) `[NEW — the old paper had NO discussion; every reviewer flagged it]`

- **8.1 Feasibility answered.** Loop back to Aagaard: proposal → working pipeline. What a deployment needs (periodic re-labeling, appeal process, multi-model ensembling).
- **8.2 Who acts on this:** stores (labels), regulators (screening/triage at scale — EU context from intro), developers (self-audit pre-launch), researchers (longitudinal pattern tracking — the pipeline is a telescope, not just a label-maker).
- **8.3 What reviews can and cannot see.** The honest epistemics paragraph: presence-evidence strong, absence-evidence weak; complaint bias; patterns players don't articulate (e.g., subtle UI misdirection) → hybrid future (review pipeline + UI methods like UIGuard = complementary, not competing — generous closing move toward the very literature you outperform).
- **8.4 Generalizability.** Nothing is game-specific: any review-rich domain (apps, marketplaces) + a domain ontology + this validation recipe. One paragraph, big-vision, no overclaiming.

---

## 9. Limitations (~350 w) `[NEW — separate section, do NOT bury in conclusion like last time]`
English-only, 3 markets; Play Store only; gold set n=75 with thin per-label support; LLM labels inherit model biases; darkpattern.games as imperfect ground truth (crowd coverage gaps); ontology snapshot in time; k tuned on the same crowd data used for validation (acknowledge; propose held-out split if n permits `[DECISION NEEDED]`).

## 10. Conclusion (~150 w) `[NEW]`
Three sentences: what was proposed (labels), what we showed (feasible, validated, self-reliant), what ships (codebook + dataset + models). End on the player from Figure 1: next time, the store page could have told them.

---

## Back matter — REQUIRED, non-negotiable
- **Ethics note** (CFP hard requirement): public review data, no PII, paraphrased quotes, coder consent/compensation, institutional context statement. ~100 w.
- **AI-use disclosure** (ACM Authorship Policy — mirror Zhang et al.'s note): author produced all content/analysis; LLM used to formalize prose; author verified all output. ~50 w.
- **Data availability:** anonymized OSF link (anonymous view!) — codebook v21, prompts, gold-75, 200k dataset, crosswalk tables. This cashes the "first dataset" claim.
- **Concurrent submission field in PCS:** if the old paper is under review anywhere, disclose per CFP or it's a desk reject. `[CHECK STATUS]`

## Figure & table manifest
| # | Asset | Status |
|---|---|---|
| F1 | Forum-post pattern cycle | `[KEEP from old paper]` |
| F2 | Pipeline overview (scrape→filter→codebook→LLM→aggregate→label) | `[NEW — draw early, anchors §3–7]` |
| F3 | Cost vs. performance scatter | have data |
| F4 | Label frequency | `[PENDING 9]` |
| F5 | Co-occurrence | `[PENDING 10]` |
| F6 | Mock store label card | `[PENDING 12]` — highest-impact figure |
| T1 | Filter pipeline | have data |
| T2 | Prompt ablation | have data |
| T3 | Gold-75 model eval | `[PENDING 8]` |
| T4 | Game-level agreement + k-sweep | `[PENDING 10/12]` |
| A | Appendix: 29-label crosswalk | `[DECISION NEEDED]` |

## New references to add (missed in old paper)
1. Zhang, Wang, Nakajima & Seaborn 2025 — *First Contact…* (PACMHCI) — **the anchor**
2. Gilardi, Alizadeh & Kubli 2023 — ChatGPT outperforms crowd workers (PNAS)
3. Ziems et al. 2024 — LLMs & computational social science (CL)
4. Pangakis et al. 2023 — LLM annotation requires validation (arXiv)
5. Krippendorff — *Content Analysis* (for α)
6. Xiao 2023 — Belgium loot-box ban (Collabra) — via Zhang et al.
7. Petrovskaya, Deterding & Zendle CHI'22 — you had it; promote it to methodological-ancestor status
8. (Optional) Maalej et al. — app review classification, for §2.3
9. (Optional) Joseph 2021 — Battle Pass Capitalism, via Zhang et al., if battle-pass labels feature in results

## Tonight's draft for the prof = 
Abstract (bracketed) + §1 full + §2 rough + §3–5.2 full (all numbers exist) + §5.3–7 as annotated skeletons with table shells + this manifest. That is a credible "working version."
