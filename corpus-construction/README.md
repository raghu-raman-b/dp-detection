# Play-review research corpus pipeline

Plain-script pipeline that resolves a game list to Google Play `app_id`s,
scrapes English reviews across `us` / `in` / `gb`, applies an ordered,
fully-logged filter cascade (PRISMA-friendly), and draws the labeling pool
plus pilot samples. Every constant lives in `config.py`; every script is
idempotent and resumable.

## Install

```bash
pip install -r requirements.txt
```

## Run order

```bash
python resolve_ids.py   # games.csv -> games_resolved.csv (+ cache/)
# hand-verify rows with needs_review=1, set them to 0, save
python scrape.py        # -> raw/{app_id}_{market}.jsonl, scrape_log.csv
python filter.py        # -> filtered/*.jsonl, filter_log.csv, corpus_stats.json
python sample.py        # -> samples/pool.jsonl, pilot_random.jsonl, pilot_targeted.jsonl
python report.py        # markdown count tables for the paper's data section
```

## Notes

- **Stage 0 never silently guesses.** Low-confidence fuzzy matches
  (`match_score < FUZZY_THRESHOLD`) and rows whose `notes` say `VERIFY`
  are flagged `needs_review=1`, and `scrape.py` refuses to start while
  any remain. Search results are cached in `cache/resolve_cache.json`.
- **Stage 1 resume**: continuation tokens are pickled per app×market in
  `state/`; re-running skips finished pairs and continues partial ones.
  Batches of 200, 1 s sleep, exponential-backoff retries.
- **Stage 2 order is fixed and logged** per app×market in
  `filter_log.csv`: english → ≥10 words → exact dedup (global,
  normalized hash) → near-dedup (global MinHash/LSH, Jaccard ≈ 0.9,
  first occurrence kept) → HTML-only cleaning (emojis / punctuation /
  casing preserved; no stopwords removal, no lemmatization).
- **Stage 3** is deterministic under `RNG_SEED`. `pool.jsonl` rows carry
  `sample_weight` (available/selected per app×market stratum) whenever
  the per-game cap or global scaling truncated a stratum. Pilot sets are
  drawn from the *text-filtered* corpus (no ML filter): 300 uniform
  random + 200 keyword-targeted (round-robin over
  `config.TARGET_KEYWORDS`, deduped against the random set, stamped
  `stratum` and `seed_keyword`).

## Layout

```
config.py  utils.py
resolve_ids.py  scrape.py  filter.py  sample.py  report.py
games.csv -> games_resolved.csv
raw/  filtered/  samples/  state/  cache/
scrape_log.csv  filter_log.csv  corpus_stats.json
```
