# Teacher runs: prompt → labels → stats → comparison

Everything below runs from `corpus-construction/scripts/`. Relative paths resolve against
that directory, not your shell, so the commands work from anywhere.

```bash
cd corpus-construction/scripts
export OPENAI_API_KEY=sk-...        # or put it in scripts/.env (gitignored)
```

Each runner reads only its own key, so you only need the one for the provider you are
running. `scripts/.env` carries a commented template for all of them.

| provider | script | key(s) |
|---|---|---|
| OpenAI | `run_teacher_openai.py` | `OPENAI_API_KEY` |
| Anthropic | `run_teacher_anthropic.py` | `ANTHROPIC_API_KEY` |
| Kimi | `run_teacher_kimi.py` | `MOONSHOT_API_KEY` |
| DeepSeek | `run_teacher_deepseek.py` | `DEEPSEEK_API_KEY` **+** `TAVILY_API_KEY` |

Install once: `pip install -r requirements.txt` (the Anthropic runner needs `anthropic`,
which is not pulled in by the others).

---

## 0. Build the prompts

The prompt is rendered from the codebook. Never hand-edit a built prompt — rebuild it.

```bash
python build_prompt.py              # writes all three ablation modes
```

Produces `../outputs/prompts/teacher_v2_{bare,boundary,full}.txt`, each with a
`.manifest.json` recording the codebook version, the flags, and the SHA. The modes are a
ladder: **bare** (indicators) → **boundary** (+ boundary rules, counterexamples) →
**full** (+ worked examples). Each is the one above it plus one kind of material, so a
score difference is attributable to exactly one addition.

---

## 0b. Which set? — `--eval-set`

Every script below (the four runners, `compute_run_stats.py`, `compare_runs.py`) starts by
asking which review set you mean. Answer at the prompt, or pass `--eval-set` to skip it.

| | `tuning` | `validation` |
|---|---|---|
| reviews | `../tuning/tuning_set_50_blind.jsonl` (50) | `../validation/validation_set_blind.jsonl` (75) |
| gold | `../tuning/tuning_set_50.jsonl` | `../validation/gold_set.jsonl` |
| runs | `../outputs/runs/` | `../outputs/validation/runs/` |
| stats | `../outputs/run-stats/` | `../outputs/validation/run-stats/` |
| comparison | `../outputs/comparison/` | `../outputs/validation/comparison/` |
| role | selection only, **burned** | the reporting set, scored **once** |

One switch moves the review file, the run tree, the gold file, the stats tree and the
comparison tree together. That is the point: a validation run cannot land in the tuning
tree, and a validation run cannot be scored against the tuning gold. Both mistakes produce
a plausible-looking number, which is the kind that survives to a table.

`--reviews`, `--out-root`, `--gold`, `--runs-root` and `--index` still override individually
for a one-off. A non-interactive caller (no tty) that omits `--eval-set` gets `tuning`, so
existing scripts keep doing exactly what they did before.

**Validation gold falls back.** Until `dp_gold.html` has produced `gold_set.jsonl`, the
validation set scores against `validation_set.jsonl` — the author's single-coder labels —
and every script says so on stderr. That is a usable smoke test and is **not** a reportable
agreement number.

## 1. Check the config — no API calls, no cost

```bash
python run_teacher_openai.py --check --prompt ../outputs/prompts/teacher_v2_bare.txt
```

Prints the model, the looked-up pricing, prompt size and SHA, how many legal codes it
parsed out of the prompt, the review count, and where output will land. Run this whenever
you change a flag.

## 2. Dry run — one live call plus a caching probe

```bash
python run_teacher_openai.py --dry --prompt ../outputs/prompts/teacher_v2_bare.txt
```

Two stages: a throwaway call proving the API and web search work, then two identical-prefix
calls proving the cache is being hit. **If it says `CACHING BROKEN`, stop and fix it** —
a cold prefix costs 10× on every call for the rest of the run. It ends with a per-review
cost estimate and the projection at 200k.

## 3. The actual run

```bash
python run_teacher_openai.py --actual --prompt ../outputs/prompts/teacher_v2_bare.txt
```

Defaults: `--model gpt-5.6-luna --effort high`, web search on, and whichever blind set
`--eval-set` resolved to (§0b). Sequential on purpose — the first call writes the cached
prefix, every later call reads it.

Output goes to one directory per `(model, effort, prompt)`, under the tree the eval set
chose — `../outputs/runs/` for tuning, `../outputs/validation/runs/` for validation:

```
../outputs/runs/gpt-5.6-luna/high/teacher_v2_bare/
    <tag>_responses.jsonl   raw text + parsed JSON (+ every re-attempt)
    <tag>_meta.jsonl        usage, cost, latency, status, contract errors
    <tag>_summary.json      scoreboard + run manifest (git sha, codebook version, argv)
    checkpoint.json         progress, for --resume
```

### Running the ablation

Three prompts, three terminals, at the same time. They don't fight over the cache — the
cache key is derived from the prompt SHA, so each warms and reads its own prefix.

```bash
python run_teacher_openai.py --actual --prompt ../outputs/prompts/teacher_v2_bare.txt
python run_teacher_openai.py --actual --prompt ../outputs/prompts/teacher_v2_boundary.txt
python run_teacher_openai.py --actual --prompt ../outputs/prompts/teacher_v2_full.txt
```

### If a run dies

```bash
python run_teacher_openai.py --actual --resume --prompt ../outputs/prompts/teacher_v2_bare.txt
```

Skips every review already labelled, retries the ones that failed, and refuses to resume
if the prompt changed underneath it. **Re-running without `--resume` overwrites the run** —
except for an interrupted one, which stops and makes you choose `--resume` or `--overwrite`.

### Flags worth knowing

| flag | what it does |
|---|---|
| `--model`, `--effort` | pricing is looked up from the model, never configured by hand (Anthropic: `--effort` is rejected on `claude-haiku-4-5`, which has no effort parameter — see `--thinking-budget` below) |
| `--limit 5` | a cheap partial run before committing to all 50 |
| `--only <id>,<id>` | re-run just the reviews a prompt got wrong |
| `--max-spend 2.00` | stop the run once spend passes this many USD |
| `--max-output` | raise if you see `TRUNCATED`; the run auto-bumps on a truncated retry |
| `--parse-retries` | extra attempts when the model won't emit JSON (default 2) |

Provider-specific flags, on top of those:

| flag | runner | what it does |
|---|---|---|
| `--cache-ttl 5m\|1h` | anthropic | a 1h cache write costs 2× a 5m one; only worth it for a run you expect to interrupt |
| `--max-pause-resumes` | anthropic | how many times a `pause_turn` is resumed before taking what's there |
| `--thinking-budget` | anthropic | `budget_tokens` for models with no adaptive thinking / effort parameter (`claude-haiku-4-5`); ignored on `claude-opus-5` / `claude-sonnet-5`. Default 4096, must stay under `--max-output` |
| `--pin-window auto\|peak\|off_peak` | deepseek | `auto` prices each call by the hour it started (exact); pinning declares one rate card for the whole run and records that it is an assumption |
| `--search-backend` | deepseek | `tavily` (default), `brave`, `serper`, `stub` |
| `--search-cache` / `--no-search-cache` | deepseek | where the shared query cache lives, or off |
| `--effort-surface` | deepseek | `thinking` (default, 2 rungs) or `reasoning` (4 rungs, unverified — `--dry` will tell you if it 400s) |

### The four providers

Every runner takes the same flags, writes the same output tree, and resumes the same way,
so an ablation is driven identically whichever one is under test:

```bash
python run_teacher_anthropic.py --actual --prompt ../outputs/prompts/teacher_v2_full.txt
python run_teacher_deepseek.py  --actual --prompt ../outputs/prompts/teacher_v2_full.txt
python run_teacher_kimi.py      --actual --prompt ../outputs/prompts/teacher_v2_full.txt
```

Where they genuinely differ — each runner's module docstring spells its own deltas out
under a `CLAUDE DIFF` / `DEEPSEEK DIFF` / `KIMI DIFF` heading:

| | effort rungs | web search | caching | reasoning tokens |
|---|---|---|---|---|
| **OpenAI** | none…max (6) | server-side builtin | explicit breakpoint + cache key | reported |
| **Anthropic** | low, medium, high, xhigh, max (5) — `claude-opus-5` / `claude-sonnet-5` only; `claude-haiku-4-5` has **no** effort parameter (thinks with `--thinking-budget` instead) | server-side, `max_uses=1` — `web_search_20260209` on Opus 5 / Sonnet 5, `web_search_20250305` on Haiku 4.5 | explicit `cache_control` on the system block | **not reported** |
| **Kimi** | low, high, max (3) | client loop via the Formula API | automatic | reported |
| **DeepSeek** | none, high (2) | client loop via `web_search_tool.py` | automatic | reported |

**The effort ladders are not commensurable across providers.** Only a within-provider
effort sweep is a curve; across providers, `high` is a label, not a quantity.

Two provider-specific things that will bite if you skip them:

- **Anthropic reports no reasoning-token count.** Thinking is billed inside
  `output_tokens` and is not broken out, so `mean_reasoning_tokens` is 0 for `claude-*`.
  That means *not reported*, not *did not think*. `reasoning_tokens_reported: false` is
  in the meta and the summary to say so.
- **`claude-haiku-4-5` has no adaptive thinking and no effort parameter** — both 400 on
  it (verified live against `/v1/models` and a direct probe, 2026-08-22). It thinks with
  an explicit token budget instead (`--thinking-budget`, default 4096), and the output
  tree files it under `effort=none`. Passing `--effort` on it is a hard error, not a
  silent no-op. This is the runner's new **default model**.
- **DeepSeek's price depends on the UTC clock** — see the rule at the bottom.

### Reading the live log

```
[14:22:07] [ 3/50] clean            input=25,013 cached=24,000 (96%) written=0 output=812 (reasoning=602) 7.4s
       $0.001640  running $0.0049  labels=2  searches=1
```

Watch for: a cache percentage that stays low (you're paying 10×), `TRUNCATED`, `CONTRACT:`
lines (illegal code, duplicate label, non-verbatim span), and `x2`/`x3` after the parse
note (the review needed re-attempts — those are billed).

Reading it across providers:

- `written=` appears only where a cache write is actually charged — OpenAI and Anthropic,
  and only on the first call of the run. Kimi and DeepSeek cache automatically with no
  write fee, so their lines omit the field entirely.
- `reasoning=0` on `claude-*` means *not reported* (see the provider table), not *did not
  think*.
- DeepSeek lines end with `[off_peak]` or `[peak]` — the rate card that row was billed at.
- `REFUSAL` on `claude-*` is a model decision, not a transport error. It is counted and
  **not** resampled: resampling a refusal buys the same refusal three times.

---

## 3b. Web search

R10 of the prompt grants every provider **one search per review**, only to resolve what a
term the reviewer used refers to ("welkin", "pity", "battle pass"). Three of the four
providers have their own search; DeepSeek has none, so `web_search_tool.py` supplies it.

### Using it standalone

Debug the search half without spending model budget:

```bash
python web_search_tool.py "what is a welkin pass in Genshin Impact"
python web_search_tool.py --backend stub "anything"      # offline, no key, no cost
python web_search_tool.py --json "gacha pity system"     # full record incl. raw payload
```

It prints exactly the string a model would be handed: a short answer (capped at ~480
chars) plus the hosts it came from.

```
backend   tavily   cached=False   $0.0080   1.2s   results=5

--- what the model would see (233 chars) ---
Welkin Moon (often called the "welkin pass") is a US$4.99 monthly item in Genshin
Impact granting 300 Genesis Crystals immediately and 90 Primogems on each daily
login for 30 days.
(sources: genshin-impact.fandom.com, hoyolab.com)
```

### Backends

`tavily` is the default and the only one that returns a written answer; the others return
raw results which are joined locally. Swap with `--search-backend`.

| backend | key | $/search | answer |
|---|---|---|---|
| `tavily` | `TAVILY_API_KEY` | 0.008 (1000/month free) | written by Tavily |
| `brave` | `BRAVE_API_KEY` | 0.005 | top snippets joined locally |
| `serper` | `SERPER_API_KEY` | 0.001 | knowledge graph, else snippets |
| `stub` | — | 0 | canned; for offline testing |

Tavily's answer is written by *Tavily's* model, not by the teacher and not by us. Disclose
that in the methods section. The raw results are kept in the audit trail either way, so
nothing about what the teacher saw is lost.

### The cache is not (only) about money

Answers are cached on disk at `../outputs/web-search-cache/`, keyed on the **normalised**
query — casing, padding and a trailing question mark all collapse to one key, so
`"What is a Welkin Pass in genshin impact?"` hits the entry written by
`"what is a welkin pass in Genshin Impact"`.

The cost saving is incidental. The point is **replayability**: a live search is a moving
target, so re-running a review next month would otherwise feed the model different
evidence and the run would not reproduce. Entries never expire by default.

```
../outputs/web-search-cache/
    by-hash/<backend>/<hh>/<hash>.json   the full record, including the raw payload
    index.jsonl                          one line per cached query
    audit.jsonl                          one line per search a runner actually made
```

Inspect what the teacher was shown:

```bash
jq -r '[.review_id, .backend, .cached, .query] | @tsv' \
  ../outputs/web-search-cache/audit.jsonl | column -t

jq -r 'select(.cached | not) | .query' \
  ../outputs/web-search-cache/audit.jsonl | sort | uniq -c | sort -rn
```

Refresh one entry with `--force`; disable the cache entirely with `--no-search-cache` on
either the tool or the runner (you lose replayability, so do not do this for a real run).

### Cost accounting

A **cached** search is free and is not billed. Both counts land in the meta, because they
answer different questions: `n_web_searches` is what the teacher *saw* (the search-rate
metric), `n_web_searches_billable` is what you *paid for*. The backend's price and
`PRICING_TABLE`'s `search_per_call` are asserted equal at preflight, so the two can never
drift apart silently.

---

## 4. Compute stats

```bash
python compute_run_stats.py
```

It asks for the eval set (§0b), then scores **every** run in that set's tree against that
set's gold, overwriting what was there before and mirroring the runs tree exactly. For
`tuning` that is `../outputs/runs` against `../tuning/tuning_set_50.jsonl`; for
`validation`, `../outputs/validation/runs` against `../validation/gold_set.jsonl`, written
under `../outputs/validation/run-stats/`:

```
../outputs/run-stats/gpt-5.6-luna/high/teacher_v2_bare/
    <tag>_report.txt        full numeric report
    <tag>_errors.md         every disagreement, for triage
    <tag>_perreview.jsonl   gold vs pred, for the paired bootstrap
    <tag>_metrics.json      the metrics row
../outputs/run-stats/index.jsonl                one row per run
```

`index.jsonl` is rebuilt each pass, so a run you delete drops out automatically (its stats
directory stays on disk, but can't leak into a comparison).

```bash
python compute_run_stats.py --list        # what runs exist
python compute_run_stats.py --run-dir ../outputs/runs/gpt-5.6-luna/high/teacher_v2_bare
```

The single-run form prints the full report and merges its row into the index.

**Read `<tag>_errors.md` before tuning anything.** For each missed label it separates
*considered and rejected* (a rule-interpretation problem — fix the codebook or the prompt)
from *never mentioned* (an attention problem — fix the examples).

---

## 5. Compare

```bash
python compare_runs.py
```

It asks for the eval set (§0b), which picks the index it reads and the tree it writes to,
then asks how many runs to compare. `0` compares everything in the index; a number walks a
menu per run — model, then reasoning level, then prompt — offering only what exists.

```
compare how many models? (0 = all 6 in the index) 2
--- run 1 of 2 ---
model: gpt-5.6-luna  (only option)
reasoning level for gpt-5.6-luna:
  1) high   2) low
> 1
prompt for gpt-5.6-luna [high]:
  1) teacher_v2_bare   2) teacher_v2_boundary   3) teacher_v2_full
> 1
  -> gpt-5.6-luna [high] teacher_v2_bare
--- run 2 of 2 ---
...
tag for this comparison: bare-vs-full
```

Writes `../outputs/comparison/bare-vs-full/` (or `../outputs/validation/comparison/…` for
the validation set) — `comparison_report.txt`, `comparison.csv`,
`selection.json` (what was compared, so the directory is self-describing), and `figures/`
including `6_prompt_sweep.png`, the ablation curve across bare → boundary → full.

Scriptable equivalent:

```bash
python compare_runs.py \
  --select gpt-5.6-luna:high:teacher_v2_bare \
  --select gpt-5.6-luna:high:teacher_v2_full \
  --tag bare-vs-full --yes
```

### Reading the report

- **Compliance is a gate, not a column.** In "compare everything" a run that emits
  unparseable JSON or non-verbatim spans is disqualified whatever it scores. When you name
  runs explicitly it compares them anyway, but flags the failure.
- **The paired bootstrap is the answer, not the leaderboard.** `0.95+` of resamples is a
  real difference; `0.6–0.9` is a lean. At n=50 a gap under ~0.05 micro-F1 is usually noise.
- **`MISSED BY EVERY MODEL`** points at the codebook or the gold, not the model.

---

## Clean worked example

```bash
cd corpus-construction/scripts

# build the three prompts
python build_prompt.py

# sanity, then a 5-review probe on the cheapest setting
python run_teacher_openai.py --check --prompt ../outputs/prompts/teacher_v2_bare.txt
python run_teacher_openai.py --dry   --prompt ../outputs/prompts/teacher_v2_bare.txt
python run_teacher_openai.py --actual --limit 5 --effort low \
       --prompt ../outputs/prompts/teacher_v2_bare.txt

# the real ablation: three prompts at high effort
for p in bare boundary full; do
  python run_teacher_openai.py --actual --prompt ../outputs/prompts/teacher_v2_$p.txt
done

# score everything, then compare the ends of the ladder
python compute_run_stats.py
python compare_runs.py \
  --select gpt-5.6-luna:high:teacher_v2_bare \
  --select gpt-5.6-luna:high:teacher_v2_full \
  --tag bare-vs-full --yes
```

---

## Provider bake-off, end to end

```bash
# offline, then one live probe each (~$0.20 total)
# run_teacher_anthropic.py defaults to claude-haiku-4-5 -- pass --model to check a
# specific one instead
python run_teacher_anthropic.py --check                            # claude-haiku-4-5
python run_teacher_anthropic.py --check --model claude-opus-5
python run_teacher_anthropic.py --check --model claude-sonnet-5
python run_teacher_deepseek.py  --check
python web_search_tool.py "what is a welkin pass in Genshin Impact"
python run_teacher_anthropic.py --dry
python run_teacher_deepseek.py  --dry

# 5 reviews each before committing to the full 50
python run_teacher_anthropic.py --actual --limit 5 --max-spend 1.00
python run_teacher_deepseek.py  --actual --limit 5 --max-spend 0.50

# the real thing (start DeepSeek after 10:00 UTC -- see rule 5)
python run_teacher_anthropic.py --actual --model claude-haiku-4-5 --max-spend 1.00
python run_teacher_anthropic.py --actual --model claude-opus-5    --max-spend 8.00
python run_teacher_anthropic.py --actual --model claude-sonnet-5  --max-spend 4.00
python run_teacher_deepseek.py  --actual --model deepseek-v4-pro  --max-spend 2.00

python compute_run_stats.py
python compare_runs.py \
  --select gpt-5.6-luna:high:teacher_v2_full \
  --select claude-haiku-4-5:none:teacher_v2_full \
  --select claude-opus-5:high:teacher_v2_full \
  --select claude-sonnet-5:high:teacher_v2_full \
  --select deepseek-v4-pro:high:teacher_v2_full \
  --select kimi-k3:high:teacher_v2_full \
  --tag provider-bakeoff --yes
```

The compliance gates in `compare_runs.py` are the real pass/fail: parse rate 1.00, zero
truncated, zero out-of-vocabulary codes, zero API errors, span-verbatim ≥ 0.95. A run that
fails one is named in the report and dropped from the ranking — **one refusal is enough**,
which is why the Anthropic runner shouts about them at run time rather than at scoring
time.

---

## Rules that are easy to break

1. **Never send a built prompt's header to a model.** Use `load_prompt()`; the build log
   above the sentinel contains a timestamp, which would break caching on every call.
2. **The tuning 50 is burned.** It drove prompt tuning and model selection, so its numbers
   are max-over-configs statistics and never appear in the paper. Only the frozen winner
   touches the 75 adjudicated set, exactly once. `--eval-set validation` is not a thing to
   reach for while iterating: the separate tree makes the mistake visible, it does not make
   it harmless. Freeze the configuration first, then run the 75 once.
3. **Check the pricing date.** `PRICING_TABLE` in `runner_common.py` carries an `as_of`
   date. Rates move; the paper needs the ones that were live for the run.
4. **A truncated run is not scorable.** `TRUNCATED` in the log or `truncated > 0` in the
   report means raise `--max-output` and run it again.
5. **DeepSeek's price depends on the UTC clock.** Peak is **01:00–04:00 and 06:00–10:00
   UTC** and costs exactly double; every other hour is half. The runner prices each call
   by the hour it started and prints the current window at preflight, warning you when a
   run is long enough to cross a boundary. **Start DeepSeek runs after 10:00 UTC** so all
   50 sit in one window, and check `pricing_windows_seen` in the summary afterwards — if
   it lists both, the report's single rate card is the *first* row's and the paper has to
   say so.
6. **Anthropic reports no reasoning tokens.** `mean_reasoning_tokens = 0` for `claude-*`
   means "not reported". Never compare that column across providers.
7. **Never enable server-side refusal fallbacks.** A rescued request is answered by a
   different model under the original model's name, which silently invalidates a
   provider comparison. `USE_FALLBACKS = False` in `run_teacher_anthropic.py`, with the
   reasoning in the comment; leave it alone.
8. **Search counts come from usage, never from the model's own JSON.** Every provider is
   asked to self-report `invoked_web_search`, and self-report is not evidence.
   `n_web_searches` is taken from the API's own accounting on every runner.
9. **Don't disable the search cache for a real run.** `--no-search-cache` makes the run
   unreproducible: the evidence the teacher saw stops being recoverable.
