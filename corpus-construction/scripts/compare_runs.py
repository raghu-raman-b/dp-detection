#!/usr/bin/env python3
"""
compare_runs.py -- compare runs scored into run-stats/index.jsonl.

Asks how many runs to compare. 0 compares everything in the index; N walks a guided menu
per run -- model, then reasoning level, then prompt -- each step offering only what
exists given the previous answers, so a typo cannot produce an empty comparison. Every
prompt can be skipped with a flag (--n, --select, --tag) when scripting.

Ranks on micro-F1. Compliance is a GATE, not a column: a run that fails a compliance
threshold is dropped from ranking (or flagged, if named explicitly via --select).

Significance uses a PAIRED bootstrap over review ids, because every run saw the same
review set and pairing removes review difficulty from the comparison.

The report is written in a fixed, machine-parseable style: no prose warnings or verdicts,
coded FLAGS instead, fixed decimal places, a stable run_id per run, and a JSON sidecar
that mirrors every printed table.

You name the output directory, because these become tables in the paper and a wall of
timestamps is unreadable six weeks later:

    outputs/comparison/<tag>/comparison_report.txt
    outputs/comparison/<tag>/comparison.csv
    outputs/comparison/<tag>/comparison.json      every table, machine-readable
    outputs/comparison/<tag>/selection.json       what was compared, and what was picked
    outputs/comparison/<tag>/figures/*.png

It reads run-stats/index.jsonl rather than globbing the run-stats tree: the index is
rebuilt from the runs that currently exist, so stats left behind by a deleted run cannot
leak into a comparison.
"""

from __future__ import annotations
import argparse, csv, json, math, random, re, statistics, sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from runner_common import resolve, show     # shared with the runners
from build_prompt import MODES              # prompt-ablation order: bare, boundary, full

# ============================== CONFIG ==============================
OUT_ROOT        = "../outputs/comparison"
INDEX_FILE      = "../outputs/run-stats/index.jsonl"
PRIMARY         = "micro_f1"        # ranking metric
PROJECT_TO      = 200_000
BOOTSTRAP_N     = 2000
BOOTSTRAP_SEED  = 20260821
MIN_SUPPORT     = 3                 # per-label stats below this are printed flagged, not dropped
CONCURRENCY     = 1                 # the runners are sequential (prompt-cache warmth); wall-clock
                                     # at 200k reflects that, not a hypothetical parallel runner
SIG_THRESHOLD   = 0.95
GREY_ZONE       = (0.05, 0.95)
CONSENSUS_TOP_N = 10
MESO_TOP_N      = 15
MAKE_FIGURES    = True
FIG_WIDTH       = 7.0
DPI             = 600

# compliance gates -- failing any of these disqualifies a run from the ranking
GATE_PARSE_RATE      = 1.00
GATE_MAX_TRUNCATED   = 0
GATE_MAX_BAD_CODES   = 0
GATE_MAX_API_ERRORS  = 0
GATE_SPAN_VERBATIM   = 0.95

CLASS_OF = {"T": "Temporal", "M": "Monetary", "S": "Social",
            "P": "Psychological", "Tech": "Technical"}
CLASS_COLOR = {"T": "#0072B2", "M": "#D55E00", "S": "#009E73",
               "P": "#CC79A7", "Tech": "#E69F00"}
# ====================================================================


def jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def cls_of(code: str) -> str:
    return "Tech" if code.startswith("Tech_") else code.split("_", 1)[0]


def pretty(code: str) -> str:
    """P_IllusionOfControl -> 'Illusion of Control' for axis labels."""
    body = code.split("_", 1)[1] if "_" in code else code
    body = re.sub(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", " ", body)
    body = re.sub(r"\s+", " ", body).strip()
    small = {"Of": "of", "And": "and", "To": "to", "The": "the", "By": "by"}
    return " ".join(small.get(w, w) for w in body.split(" "))


def label_of(r: dict) -> str:
    """Internal dict key for CI / per-review lookups -- unique per configuration. Not used
    as a figure label; figures use readable_label(). Text tables show run_id (== tag)."""
    ws = "" if r.get("web_search") else " no-search"
    stem = r.get("prompt_stem") or Path(r.get("prompt_file") or "").name.rsplit(".txt", 1)[0]
    prompt = f" {stem}" if stem else ""
    return f"{r.get('model')} [{r.get('reasoning_effort')}]{prompt}{ws}"


def rid(r: dict) -> str:
    """Stable run identifier for every printed table and the sidecar."""
    return r.get("tag") or label_of(r)


def gate(r: dict) -> list[str]:
    fails = []
    n = max(r.get("n_requests", 0), 1)
    if r.get("parsed", 0) / n < GATE_PARSE_RATE:
        fails.append(f"parse_rate {r.get('parsed',0)}/{n}")
    if r.get("truncated", 0) > GATE_MAX_TRUNCATED:
        fails.append(f"truncated={r['truncated']}")
    if r.get("bad_codes", 0) > GATE_MAX_BAD_CODES:
        fails.append(f"oov_codes={r['bad_codes']}")
    if r.get("api_errors", 0) > GATE_MAX_API_ERRORS:
        fails.append(f"api_errors={r['api_errors']}")
    if r.get("span_verbatim_rate", 1.0) < GATE_SPAN_VERBATIM:
        fails.append(f"span_verbatim={r.get('span_verbatim_rate'):.3f}")
    return fails


def micro_f1(pairs: list[tuple[set, set]]) -> float:
    tp = sum(len(p & g) for g, p in pairs)
    fp = sum(len(p - g) for g, p in pairs)
    fn = sum(len(g - p) for g, p in pairs)
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    return 2 * prec * rec / (prec + rec) if prec + rec else 0.0


def load_perreview(r: dict) -> dict[str, tuple[set, set]]:
    path = r.get("perreview_file")
    if not path or not Path(path).exists():
        return {}
    return {x["review_id"]: (set(x["gold"]), set(x["pred"])) for x in jsonl(Path(path))}


def paired_bootstrap(a: dict, b: dict, ids: list[str], n: int, seed: int) -> tuple[float, float, float]:
    """Fraction of resamples where a > b, the mean gap, and its sd. Resamples review ids,
    so both runs are scored on the same draw every time."""
    rng = random.Random(seed)
    wins = 0
    gaps = []
    k = len(ids)
    for _ in range(n):
        draw = [ids[rng.randrange(k)] for _ in range(k)]
        fa = micro_f1([a[i] for i in draw])
        fb = micro_f1([b[i] for i in draw])
        wins += fa > fb
        gaps.append(fa - fb)
    sd = statistics.stdev(gaps) if len(gaps) > 1 else 0.0
    return wins / n, statistics.mean(gaps), sd


def bootstrap_ci(pr: dict, ids: list[str], n: int, seed: int) -> tuple[float, float]:
    rng = random.Random(seed)
    vals = []
    k = len(ids)
    for _ in range(n):
        draw = [ids[rng.randrange(k)] for _ in range(k)]
        vals.append(micro_f1([pr[i] for i in draw]))
    vals.sort()
    return vals[int(0.025 * n)], vals[int(0.975 * n) - 1]


def mde_at_n(sd_gap: float, z: float = 1.645) -> float:
    """Smallest true gap that would be expected to clear SIG_THRESHOLD reliably at this n,
    modeling the resampled gap as Normal(delta, sd_gap): Phi(delta/sd_gap)=0.95 -> delta=1.645*sd_gap."""
    return z * sd_gap


def pareto(rows: list[dict], cost_key: str) -> list[dict]:
    """Not dominated on (higher PRIMARY, lower cost_key)."""
    front = []
    for r in rows:
        if not any(o is not r and o[PRIMARY] >= r[PRIMARY] and o[cost_key] <= r[cost_key]
                   and (o[PRIMARY] > r[PRIMARY] or o[cost_key] < r[cost_key]) for o in rows):
            front.append(r)
    return sorted(front, key=lambda r: r[cost_key])


# ---------------------------------------------------------- new metrics

def jaccard(g: set, p: set) -> float:
    u = g | p
    return len(g & p) / len(u) if u else 1.0


def masi(g: set, p: set) -> float:
    """Passonneau MASI: Jaccard scaled by a monotonicity coefficient."""
    j = jaccard(g, p)
    if g == p:
        m = 1.0
    elif (g and p) and (g <= p or p <= g):
        m = 0.67
    elif g & p:
        m = 0.33
    else:
        m = 0.0
    return j * m


def all_label_macro_f1(r: dict) -> float:
    """Macro-F1 over ALL legal labels, unconditioned by support -- distinct from
    meso_macro_f1 (already in the index), which is gated by MIN_SUPPORT."""
    vals = list((r.get("per_label_f1") or {}).values())
    return statistics.mean(vals) if vals else 0.0


def cardinality_stats(pr: dict, ids: list[str]) -> dict:
    sum_p = sum(len(pr[i][1]) for i in ids)
    sum_g = sum(len(pr[i][0]) for i in ids)
    n = len(ids)
    return {
        "labels_per_review_mean": (sum_p / n) if n else None,
        "cardinality_ratio": (sum_p / sum_g) if sum_g else None,
        "label_count_bias": sum_p - sum_g,
        "reviews_with_fp_n": sum(1 for i in ids if pr[i][1] - pr[i][0]),
        "reviews_with_fn_n": sum(1 for i in ids if pr[i][0] - pr[i][1]),
        "reviews_exact_correct_n": sum(1 for i in ids if pr[i][0] == pr[i][1]),
    }


def jaccard_masi_means(pr: dict, ids: list[str]) -> tuple[float | None, float | None]:
    if not ids:
        return None, None
    js = [jaccard(pr[i][0], pr[i][1]) for i in ids]
    ms = [masi(pr[i][0], pr[i][1]) for i in ids]
    return statistics.mean(js), statistics.mean(ms)


def per_label_prf_from_perreview(pr: dict, ids: list[str], labels: list[str]) -> dict[str, tuple]:
    """Sidecar-only cross-check of compute_run_stats.py's own per-label P/R/F1."""
    out = {}
    for c in labels:
        tp = sum(1 for i in ids if c in pr[i][0] and c in pr[i][1])
        fp = sum(1 for i in ids if c in pr[i][1] and c not in pr[i][0])
        fn = sum(1 for i in ids if c in pr[i][0] and c not in pr[i][1])
        p = tp / (tp + fp) if tp + fp else 0.0
        r = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * p * r / (p + r) if p + r else 0.0
        out[c] = {"precision": p, "recall": r, "f1": f1, "support": tp + fn}
    return out


def label_prevalence(per_by_run: dict[str, dict], ids: list[str], labels: list[str]) -> dict:
    names = list(per_by_run.keys())
    gold_by_run = {name: {c: sum(1 for i in ids if c in per_by_run[name][i][0]) for c in labels}
                   for name in names}
    ref = gold_by_run[names[0]] if names else {c: 0 for c in labels}
    consistent = all(gold_by_run[n] == ref for n in names)
    per_run = {}
    for name in names:
        pred_count = {c: sum(1 for i in ids if c in per_by_run[name][i][1]) for c in labels}
        per_run[name] = {c: {"pred_count": pred_count[c],
                             "ratio": (pred_count[c] / ref[c]) if ref[c] else None,
                             "signed_error": pred_count[c] - ref[c]} for c in labels}
    return {"gold_count": ref, "gold_consistent": consistent, "per_run": per_run}


def universal_set(per_by_run: dict[str, dict], ids: list[str], mode: str) -> dict[str, dict]:
    """mode='fn': labels every run missed on a review. mode='fp': labels every run
    spuriously added on a review where gold has none. Keyed by label -> review_ids."""
    per_pair = defaultdict(set)
    for name, pr in per_by_run.items():
        for i in ids:
            g, p = pr[i]
            diff = (g - p) if mode == "fn" else (p - g)
            for c in diff:
                per_pair[(i, c)].add(name)
    n_runs = len(per_by_run)
    bylab = defaultdict(list)
    for (i, c), who in per_pair.items():
        if len(who) == n_runs:
            bylab[c].append(i)
    return {c: {"review_ids": sorted(revs), "n": len(revs)} for c, revs in bylab.items()}


def meso_confusion(per_by_run: dict[str, dict], ids: list[str]) -> tuple[dict, list]:
    """Sibling-label substitutions within a high-level class: gold has A (missed), pred
    has same-class B != A. Aggregated across every ranked run with per-review data."""
    by_class = Counter()
    pairs = Counter()
    for _, pr in per_by_run.items():
        for i in ids:
            g, p = pr[i]
            for a in g - p:
                cls = cls_of(a)
                for b in p:
                    if b != a and cls_of(b) == cls:
                        by_class[cls] += 1
                        pairs[(cls, a, b)] += 1
    top_pairs = [(cls, a, b, n) for (cls, a, b), n in pairs.most_common(MESO_TOP_N)]
    return dict(by_class), top_pairs


def consensus_per_review(per_by_run: dict[str, dict], ids: list[str]) -> dict[str, dict]:
    names = list(per_by_run.keys())
    k = len(names)
    out = {}
    for i in ids:
        gold = per_by_run[names[0]][i][0]
        preds = [per_by_run[name][i][1] for name in names]
        n_match_gold = sum(1 for p in preds if p == gold)
        dist = Counter(frozenset(p) for p in preds)
        ent = -sum((c / k) * math.log2(c / k) for c in dist.values())
        unanimous = len(dist) == 1
        common = next(iter(dist)) if unanimous else None
        agrees = bool(unanimous and common == frozenset(gold))
        out[i] = {"n_exact_match_gold": n_match_gold, "entropy_bits": ent,
                  "unanimous": unanimous, "agrees_with_gold": agrees}
    return out


def consensus_summary(per_review: dict) -> dict:
    ids = list(per_review.keys())
    n = len(ids)
    unanimity_rate = sum(1 for i in ids if per_review[i]["unanimous"]) / n if n else 0.0
    top_entropy = sorted((i for i in ids if per_review[i]["entropy_bits"] > 0),
                        key=lambda i: -per_review[i]["entropy_bits"])[:CONSENSUS_TOP_N]
    unanimous_but_wrong = sorted(i for i in ids
                                 if per_review[i]["unanimous"] and not per_review[i]["agrees_with_gold"])
    return {"unanimity_rate": unanimity_rate, "top_entropy_reviews": top_entropy,
            "unanimous_but_wrong": unanimous_but_wrong}


def cost_per_f1_point(ranked: list[dict], cost_key: str, frontier: list[dict]) -> dict[str, object]:
    if not frontier:
        return {label_of(r): None for r in ranked}
    cheapest = frontier[0]
    out = {}
    for r in ranked:
        if r is cheapest:
            out[label_of(r)] = "ref"
            continue
        d_f1 = r.get(PRIMARY, 0) - cheapest.get(PRIMARY, 0)
        out[label_of(r)] = ((r.get(cost_key, 0) - cheapest.get(cost_key, 0)) / d_f1) if d_f1 > 0 else None
    return out


def n_repeat_groups(rows: list[dict]) -> dict[tuple, list[dict]]:
    groups = defaultdict(list)
    for r in rows:
        groups[(r.get("model"), effort_of(r), r.get("prompt_sha256"))].append(r)
    return {k: v for k, v in groups.items() if len(v) > 1}


def repeatability_stats(groups: dict) -> list[dict]:
    out = []
    for (model, effort, sha), v in groups.items():
        f1s = [r.get(PRIMARY, 0) for r in v]
        out.append({"model": model, "effort": effort, "prompt_sha": (sha or "")[:12],
                    "n_repeats": len(v), "mean": statistics.mean(f1s),
                    "sd": statistics.stdev(f1s) if len(f1s) > 1 else 0.0,
                    "min": min(f1s), "max": max(f1s), "run_ids": [rid(r) for r in v]})
    return out


def wall_clock_hours_at_200k(r: dict) -> float:
    return r.get("latency_mean", 0) * PROJECT_TO / CONCURRENCY / 3600


def oov_label_rate(r: dict) -> float:
    return r.get("bad_codes", 0) / max(r.get("labels_emitted", 0), 1)


def parse_failure_rate(r: dict) -> float:
    return 1 - r.get("parsed", 0) / max(r.get("n_requests", 0), 1)


def truncation_rate(r: dict) -> float:
    return r.get("truncated", 0) / max(r.get("n_requests", 0), 1)


_SUMMARY_CACHE: dict[str, dict] = {}


def load_summary(r: dict) -> dict:
    tag = r.get("tag")
    if tag in _SUMMARY_CACHE:
        return _SUMMARY_CACHE[tag]
    data = {}
    run_dir = r.get("run_dir")
    if run_dir and tag:
        path = Path(run_dir) / f"{tag}_summary.json"
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            data = {}
    _SUMMARY_CACHE[tag] = data
    return data


def run_meta_row(r: dict) -> dict:
    s = load_summary(r)
    codebook_version = ((s.get("manifest") or {}).get("prompt_manifest") or {}).get("codebook_version")
    return {"run_id": rid(r), "model": r.get("model"), "effort": effort_of(r),
            "prompt_name": prompt_of(r), "prompt_sha": (r.get("prompt_sha256") or "")[:12],
            "seed": "n/a", "temperature": s.get("temperature"), "max_tokens": s.get("max_output"),
            "eval_set_n": r.get("n_scored"), "codebook_version": codebook_version,
            "started_at": s.get("started"), "finished_at": s.get("finished")}


# ---------------------------------------------------------------- selection

def effort_of(r: dict) -> str:
    return r.get("reasoning_effort") or "none"


def prompt_of(r: dict) -> str:
    return r.get("prompt_stem") or Path(r.get("prompt_file") or "").name.rsplit(".txt", 1)[0]


EFFORT_ORDER = ["none", "low", "medium", "high", "xhigh", "max"]


def prompt_code(stem: str) -> str:
    """Short code for a prompt stem, used only in compact text tables."""
    tokens = [t for t in stem.split("_") if t]
    if tokens and tokens[0] not in MODES and not re.fullmatch(r"v\d+", tokens[0]):
        tokens = tokens[1:] or tokens
    if tokens and tokens[-1] in MODES:
        mode = {"bare": "bare", "boundary": "bdry", "full": "full"}[tokens[-1]]
        version = "".join(tokens[:-1])
        return f"{version}/{mode}" if version else mode
    return "".join(t[:3] for t in tokens)[:8] or stem[:8]


def ask(prompt: str) -> str:
    try:
        return input(prompt).strip()
    except EOFError:
        sys.exit("\nno more input -- aborted.")


def ask_int(prompt: str, lo: int, hi: int) -> int:
    while True:
        s = ask(prompt)
        if s.isdigit() and lo <= int(s) <= hi:
            return int(s)
        print(f"  enter a number between {lo} and {hi}")


def pick(field: str, options: list[str]) -> str:
    if len(options) == 1:
        print(f"{field}: {options[0]}  (only option)")
        return options[0]
    print(f"{field}:")
    for i, o in enumerate(options, 1):
        print(f"  {i}) {o}")
    while True:
        s = ask("> ")
        if s.isdigit() and 1 <= int(s) <= len(options):
            return options[int(s) - 1]
        if s in options:
            return s
        print(f"  not one of: {', '.join(options)}")


def choose_run(rows: list[dict], taken: list[dict]) -> dict:
    avail = [r for r in rows if r not in taken]
    model = pick("model", sorted({r.get("model", "?") for r in avail}))
    avail = [r for r in avail if r.get("model") == model]
    effort = pick(f"reasoning level for {model}", sorted({effort_of(r) for r in avail}))
    avail = [r for r in avail if effort_of(r) == effort]
    prompt = pick(f"prompt for {model} [{effort}]", prompt_order({prompt_of(r) for r in avail}))
    hit = [r for r in avail if prompt_of(r) == prompt]
    print(f"  -> {rid(hit[0])}\n")
    return hit[0]


def prompt_order(stems) -> list[str]:
    ladder = list(MODES)
    def key(s: str):
        for i, mode in enumerate(ladder):
            if s.endswith("_" + mode) or s == mode:
                return (0, i, s)
        return (1, 0, s)
    return sorted(stems, key=key)


def select_rows(rows: list[dict], a: argparse.Namespace) -> tuple[list[dict], bool]:
    if a.select:
        chosen = []
        for spec in a.select:
            parts = [x.strip() for x in spec.split(":")]
            if len(parts) != 3:
                sys.exit(f"--select wants model:effort:prompt, got {spec!r}")
            m, e, pr = parts
            hit = [r for r in rows if r.get("model") == m and effort_of(r) == e
                   and prompt_of(r) == pr]
            if not hit:
                sys.exit(f"no scored run for {spec!r}.\n  have: "
                         + ", ".join(sorted(f"{r.get('model')}:{effort_of(r)}:{prompt_of(r)}"
                                            for r in rows)))
            chosen.append(hit[0])
        return chosen, True

    n = a.n if a.n is not None else ask_int(
        f"compare how many models? (0 = all {len(rows)} in the index) ", 0, len(rows))
    if n == 0:
        return rows, False
    chosen: list[dict] = []
    for i in range(n):
        print(f"--- run {i + 1} of {n} ---")
        chosen.append(choose_run(rows, chosen))
    return chosen, True


def ask_tag(a: argparse.Namespace) -> str:
    while True:
        tag = a.tag or ask("tag for this comparison: ")
        if re.fullmatch(r"[A-Za-z0-9._-]+", tag or ""):
            return tag
        print("  letters, digits, dot, dash, underscore only")
        a.tag = ""


# ---------------------------------------------------------------- rendering

def fmt_metric(v) -> str:
    return f"{v:.3f}"


fmt_rate = fmt_metric


def fmt_usd_200k(v) -> str:
    return f"${v:,.0f}"


def fmt_usd_rev(v) -> str:
    return f"${v:.5f}"


def fmt_latency(v) -> str:
    return f"{v:.1f}"


def fmt_na(v, fmt_fn=fmt_metric) -> str:
    return "n/a" if v is None else fmt_fn(v)


def fmt_flagged(v, below_floor: bool, fmt_fn=fmt_metric) -> str:
    return fmt_na(v, fmt_fn) + ("*" if below_floor else "")


def render_table(add, headers: list[str], units: list[str], rows: list[list]) -> None:
    cols = list(zip(headers, units))
    widths = []
    for i, (h, u) in enumerate(cols):
        w = max(len(str(h)), len(str(u)), *(len(str(row[i])) for row in rows)) if rows else max(len(h), len(u))
        widths.append(w + 2)
    def line(cells):
        return "  " + "".join(f"{str(c):<{w}}" for c, w in zip(cells, widths))
    add(line(headers))
    add(line(units))
    for row in rows:
        add(line(row))


def display_model(m: str) -> str:
    return m or "unknown"


def display_effort(e: str) -> str:
    return e or "none"


def display_prompt(stem: str) -> str:
    return (stem or "").replace("_", " ")


def readable_label(r: dict, dims: tuple) -> str:
    parts = []
    for d in dims:
        if d == "model":
            parts.append(display_model(r.get("model")))
        elif d == "effort":
            parts.append(display_effort(effort_of(r)))
        elif d == "prompt":
            parts.append(display_prompt(prompt_of(r)))
    return ", ".join(parts) if parts else display_model(r.get("model"))


def varying_dims(rows: list[dict]) -> dict:
    return {"model": len({r.get("model") for r in rows}) > 1,
            "effort": len({effort_of(r) for r in rows}) > 1,
            "prompt": len({prompt_of(r) for r in rows}) > 1}


def rank_key(r: dict, cost_key: str) -> tuple:
    return (-r.get(PRIMARY, 0), 0 if not gate(r) else 1,
            r.get(cost_key, float("inf")), r.get("latency_p95", float("inf")),
            r.get("tag", ""))


# ------------------------------------------------------------------ figures

def style() -> None:
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9,
        "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 8,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.5,
        "figure.facecolor": "white",
    })


def savefig(fig, name: str, fig_dir: Path) -> str:
    import matplotlib.pyplot as plt
    fig.tight_layout()
    fig.savefig(fig_dir / name, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return name


def fig_quality_vs_cost(fig_dir, ranked, cost_key, plt, matplotlib) -> str:
    front = pareto(ranked, cost_key)
    vary = varying_dims(ranked)
    if vary["model"]:
        color_dim, group_of = "model", (lambda r: r.get("model"))
        order = sorted({r.get("model") for r in ranked})
    elif vary["prompt"]:
        color_dim, group_of = "prompt", prompt_of
        order = prompt_order({prompt_of(r) for r in ranked})
    elif vary["effort"]:
        color_dim, group_of = "effort", effort_of
        order = [e for e in EFFORT_ORDER if e in {effort_of(r) for r in ranked}]
    else:
        color_dim, group_of = "run", (lambda r: rid(r))
        order = [rid(r) for r in ranked]
    palette = plt.cm.tab10.colors
    color_of = {g: palette[i % 10] for i, g in enumerate(order)}
    label_dims = tuple(d for d in ("model", "effort", "prompt") if vary[d] and d != color_dim)
    def group_label(g):
        return {"model": display_model, "prompt": display_prompt, "effort": display_effort}.get(
            color_dim, lambda x: x)(g)

    # Only the Pareto-frontier points get a direct label -- with dozens of runs, labeling
    # every point makes the dense/cheap end unreadable; the frontier is the analytically
    # relevant subset, and every run's full identity is already in the LEADERBOARD table.
    front_order = {id(r): i for i, r in enumerate(front)}  # sorted by cost_key already
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    for r in ranked:
        ax.scatter(r[cost_key], r[PRIMARY], s=130, color=color_of[group_of(r)],
                   edgecolor="white", linewidth=1.3, zorder=3)
        fi = front_order.get(id(r))
        txt = readable_label(r, label_dims) if label_dims and fi is not None else ""
        if txt:
            ax.annotate(txt, (r[cost_key], r[PRIMARY]), fontsize=7.5,
                        xytext=(8, 10 if fi % 2 == 0 else -16), textcoords="offset points",
                        bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="0.7", alpha=0.9))
    if len(front) > 1:
        ax.plot([r[cost_key] for r in front], [r[PRIMARY] for r in front],
                "--", color="0.4", linewidth=1.4, zorder=2)
    handles = [matplotlib.lines.Line2D([0], [0], marker="o", linestyle="", markersize=8,
                                       markerfacecolor=color_of[g], markeredgecolor="white",
                                       label=group_label(g)) for g in order]
    if len(front) > 1:
        handles.append(matplotlib.lines.Line2D([0], [0], color="0.4", linestyle="--",
                                                label="Pareto frontier"))
    ax.set_xlabel(f"projected cost at {PROJECT_TO:,} reviews (USD)")
    ax.set_ylabel("micro-F1")
    ax.set_title(f"Quality vs cost (color: {color_dim})")
    ax.legend(handles=handles, fontsize=7.5, loc="best", framealpha=0.9)
    return savefig(fig, "1_quality_vs_cost.png", fig_dir)


def fig_precision_recall(fig_dir, ranked, cis, plt, np) -> str:
    vary = varying_dims(ranked)
    dims = tuple(d for d in ("model", "effort", "prompt") if vary[d]) or ("model",)
    labels = [readable_label(r, dims) for r in ranked]
    fig, ax = plt.subplots(figsize=(max(7, 1.7 * len(ranked)), 4.8))
    x = np.arange(len(ranked)); w = 0.26
    palette = plt.cm.tab10.colors
    ax.bar(x - w, [r["micro_p"] for r in ranked], w, label="precision", color=palette[0])
    ax.bar(x, [r["micro_r"] for r in ranked], w, label="recall", color=palette[1])
    f1s = [r[PRIMARY] for r in ranked]
    err = None
    if cis:
        err = np.array([[f - cis[label_of(r)][0], cis[label_of(r)][1] - f]
                        for r, f in zip(ranked, f1s)]).T
    ax.bar(x + w, f1s, w, yerr=err, capsize=3, label="micro-F1", color=palette[2])
    ax.set_xticks(x); ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.set_ylim(0, 1.02); ax.set_ylabel("score")
    ax.set_title("Precision, recall, micro-F1 (whiskers: 95% paired bootstrap CI)")
    ax.legend(fontsize=8)
    return savefig(fig, "2_precision_recall.png", fig_dir)


def fig_label_heatmap(fig_dir, ranked, heat_cmap, plt, np) -> str | None:
    labels_all = sorted({c for r in ranked for c in (r.get("per_label_support") or {})})
    if not labels_all:
        return None
    below = {c for c in labels_all
             if max((r.get("per_label_support") or {}).get(c, 0) for r in ranked) < MIN_SUPPORT}
    M = np.array([[(r.get("per_label_f1") or {}).get(c, np.nan) for r in ranked]
                  for c in labels_all], dtype=float)
    vary = varying_dims(ranked)
    dims = tuple(d for d in ("model", "effort", "prompt") if vary[d]) or ("model",)
    xlabels = [readable_label(r, dims) for r in ranked]
    ylabels = [pretty(c) + (" *" if c in below else "") for c in labels_all]
    fig, ax = plt.subplots(figsize=(1.5 * len(ranked) + 4.0, 0.32 * len(labels_all) + 2))
    im = ax.imshow(M, cmap=heat_cmap, vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(ranked))); ax.set_xticklabels(xlabels, rotation=25, ha="right")
    ax.set_yticks(range(len(labels_all))); ax.set_yticklabels(ylabels)
    for i in range(len(labels_all)):
        for j in range(len(ranked)):
            if not np.isnan(M[i, j]):
                ax.text(j, i, f"{M[i,j]:.2f}", ha="center", va="center", fontsize=6)
    ax.set_title(f"Per-label F1 (* support below {MIN_SUPPORT})")
    ax.grid(False)
    fig.colorbar(im, ax=ax, shrink=0.7, label="F1")
    return savefig(fig, "3_label_heatmap.png", fig_dir)


def fig_reasoning_sweep(fig_dir, rows, cost_key, plt) -> str | None:
    by_model = defaultdict(list)
    for r in rows:
        by_model[r["model"]].append(r)
    sweeps = {m: sorted([r for r in v if effort_of(r) in EFFORT_ORDER],
                        key=lambda r: EFFORT_ORDER.index(effort_of(r)))
              for m, v in by_model.items()}
    sweeps = {m: v for m, v in sweeps.items() if len(v) > 1}
    if not sweeps:
        return None
    palette = plt.cm.tab10.colors
    order = [e for e in EFFORT_ORDER if any(effort_of(r) == e for v in sweeps.values() for r in v)]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6.2), sharex=True)
    for i, (m, v) in enumerate(sweeps.items()):
        xs = [order.index(effort_of(r)) for r in v]
        c = palette[i % 10]
        ax1.plot(xs, [r[PRIMARY] for r in v], "o-", color=c, label=display_model(m))
        ax2.plot(xs, [r[cost_key] for r in v], "o-", color=c, label=display_model(m))
    ax1.set_ylabel("micro-F1")
    ax2.set_ylabel(f"USD at {PROJECT_TO:,}")
    ax2.set_xticks(range(len(order))); ax2.set_xticklabels([display_effort(e) for e in order])
    ax2.set_xlabel("reasoning effort")
    ax1.set_title("Reasoning effort: quality")
    ax2.set_title("Reasoning effort: cost")
    ax1.legend(fontsize=7, loc="best")
    return savefig(fig, "4_reasoning_sweep.png", fig_dir)


def fig_prompt_sweep(fig_dir, rows, cost_key, plt) -> str | None:
    by_cfg = defaultdict(list)
    for r in rows:
        by_cfg[(r.get("model"), effort_of(r))].append(r)
    order_p = prompt_order({prompt_of(r) for r in rows})
    psweeps = {k: sorted(v, key=lambda r: order_p.index(prompt_of(r)))
               for k, v in by_cfg.items() if len({prompt_of(r) for r in v}) > 1}
    if not psweeps:
        return None
    palette = plt.cm.tab10.colors
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(max(7, 1.9 * len(order_p)), 6.6), sharex=True)
    for i, ((m, eff), v) in enumerate(psweeps.items()):
        xs = [order_p.index(prompt_of(r)) for r in v]
        c = palette[i % 10]
        lab = f"{display_model(m)}, {display_effort(eff)}"
        ax1.plot(xs, [r[PRIMARY] for r in v], "o-", color=c, label=lab)
        ax2.plot(xs, [r[cost_key] for r in v], "o-", color=c, label=lab)
    ax1.set_ylabel("micro-F1")
    ax2.set_ylabel(f"USD at {PROJECT_TO:,}")
    ax2.set_xticks(range(len(order_p)))
    ax2.set_xticklabels([display_prompt(p) for p in order_p], rotation=15, ha="right")
    ax2.set_xlabel("prompt")
    ax1.set_title("Prompt ablation: quality")
    ax2.set_title("Prompt ablation: cost")
    ax1.legend(fontsize=7, loc="best")
    return savefig(fig, "6_prompt_sweep.png", fig_dir)


def fig_compliance(fig_dir, rows, plt, np) -> str:
    vary = varying_dims(rows)
    dims = tuple(d for d in ("model", "effort", "prompt") if vary[d]) or ("model",)
    labels = [readable_label(r, dims) for r in rows]
    fig, ax = plt.subplots(figsize=(max(7, 1.8 * len(rows)), 4.4))
    x = np.arange(len(rows)); w = 0.27
    palette = plt.cm.tab10.colors
    ax.bar(x - w, [r.get("parsed", 0) / max(r.get("n_requests", 1), 1) for r in rows], w,
           label="parse rate", color=palette[0])
    ax.bar(x, [r.get("span_verbatim_rate", 0) for r in rows], w,
           label="span verbatim rate", color=palette[3])
    ax.bar(x + w, [oov_label_rate(r) for r in rows], w,
           label="OOV label rate", color=palette[4])
    ax.axhline(GATE_SPAN_VERBATIM, color="crimson", ls=":", lw=1.2,
               label=f"span gate {GATE_SPAN_VERBATIM}")
    ax.set_xticks(x); ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.set_ylim(0, 1.05); ax.set_title("Compliance rates")
    ax.legend(fontsize=8)
    return savefig(fig, "5_compliance.png", fig_dir)


def fig_prevalence(fig_dir, gold_count: dict, plt, np) -> str | None:
    if not gold_count:
        return None
    order = sorted(gold_count, key=lambda c: (-gold_count[c], c))
    vals = [gold_count[c] for c in order]
    cols = [CLASS_COLOR[cls_of(c)] for c in order]
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, 0.28 * len(order) + 1.5))
    y = np.arange(len(order))
    ax.barh(y, vals, color=cols, edgecolor="white", linewidth=0.4)
    ax.set_yticks(y); ax.set_yticklabels([pretty(c) for c in order])
    ax.invert_yaxis()
    ax.set_xlabel("gold count (shared review set)")
    ax.set_title("Label prevalence")
    handles = [plt.Rectangle((0, 0), 1, 1, color=CLASS_COLOR[k]) for k in CLASS_COLOR]
    ax.legend(handles, [CLASS_OF[k] for k in CLASS_COLOR], fontsize=7, loc="lower right")
    return savefig(fig, "7_prevalence.png", fig_dir)


def fig_meso_confusion(fig_dir, top_pairs: list, plt, np) -> str | None:
    if not top_pairs:
        return None
    labels = [f"{pretty(a)} -> {pretty(b)}" for cls, a, b, n in top_pairs]
    vals = [n for cls, a, b, n in top_pairs]
    cols = [CLASS_COLOR[cls] for cls, a, b, n in top_pairs]
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, 0.32 * len(top_pairs) + 1.5))
    y = np.arange(len(top_pairs))
    ax.barh(y, vals, color=cols, edgecolor="white", linewidth=0.4)
    ax.set_yticks(y); ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel("substitution count (gold missed, same-class label predicted)")
    ax.set_title("Meso confusion: top same-class substitutions")
    return savefig(fig, "8_meso_confusion.png", fig_dir)


def make_figures(fig_dir: Path, rows: list[dict], ranked: list[dict], cost_key: str,
                 cis: dict, gold_count: dict, meso_pairs: list) -> list[str]:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.colors import LinearSegmentedColormap
        import numpy as np
    except ImportError:
        return ["matplotlib not installed - figures skipped (pip install matplotlib)"]

    fig_dir.mkdir(parents=True, exist_ok=True)
    style()
    heat_cmap = LinearSegmentedColormap.from_list(
        "dpheat", ["#FFFFFF", "#BFE3F2", "#4FA8D8", "#2B5FA8", "#1B2E6E"])
    made = []
    if ranked:
        made.append(fig_quality_vs_cost(fig_dir, ranked, cost_key, plt, matplotlib))
        made.append(fig_precision_recall(fig_dir, ranked, cis, plt, np))
        h = fig_label_heatmap(fig_dir, ranked, heat_cmap, plt, np)
        if h:
            made.append(h)
    r = fig_reasoning_sweep(fig_dir, rows, cost_key, plt)
    if r:
        made.append(r)
    p = fig_prompt_sweep(fig_dir, rows, cost_key, plt)
    if p:
        made.append(p)
    if rows:
        made.append(fig_compliance(fig_dir, rows, plt, np))
    pv = fig_prevalence(fig_dir, gold_count, plt, np)
    if pv:
        made.append(pv)
    mc = fig_meso_confusion(fig_dir, meso_pairs, plt, np)
    if mc:
        made.append(mc)
    return made


# --------------------------------------------------------------------- main

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Compare scored runs. Prompts for anything not given as a flag.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--n", type=int, default=None,
                    help="how many runs to compare; 0 = everything in the index")
    ap.add_argument("--select", action="append", default=[], metavar="MODEL:EFFORT:PROMPT",
                    help="pick a run without the menu; repeat once per run")
    ap.add_argument("--tag", default="", help="names the output directory")
    ap.add_argument("--index", default=INDEX_FILE)
    ap.add_argument("--out-root", default=OUT_ROOT)
    ap.add_argument("--yes", action="store_true", help="overwrite an existing tag without asking")
    return ap.parse_args()


def main() -> None:
    a = parse_args()
    idx = resolve(a.index)
    if not idx.exists():
        sys.exit(f"no index at {show(idx)} -- run compute_run_stats.py first")
    all_rows = jsonl(idx)
    if not all_rows:
        sys.exit(f"{show(idx)} is empty -- run compute_run_stats.py first")

    selected, explicit = select_rows(all_rows, a)
    tag = ask_tag(a)
    out_dir = resolve(a.out_root) / tag
    if out_dir.exists() and not a.yes:
        if ask(f"{show(out_dir)} exists. overwrite? [y/N] ").lower() not in ("y", "yes"):
            sys.exit("aborted.")

    cost_key = f"projected_usd_at_{PROJECT_TO}"
    for r in selected:
        r["wall_clock_hours_at_200k"] = wall_clock_hours_at_200k(r)
    rows = sorted(selected, key=lambda r: rank_key(r, cost_key))

    L, add = [], None
    add = L.append
    sidecar: dict = {}

    # ---- HEADER ----
    add("=" * 92)
    add("PROVIDER / MODEL COMPARISON")
    add("=" * 92)
    add(f"generated={datetime.now().isoformat(timespec='seconds')}")
    add(f"tag={tag}")
    add(f"index={show(idx)}")
    add(f"runs={len(rows)}"
        + (f" of_{len(all_rows)}_in_index" if explicit else " (all_in_index)"))
    add(f"ranked_on={PRIMARY}")
    add(f"CONCURRENCY={CONCURRENCY} PROJECT_TO={PROJECT_TO} BOOTSTRAP_N={BOOTSTRAP_N} "
        f"MIN_SUPPORT={MIN_SUPPORT}")
    add("")
    sidecar["meta"] = {"generated": datetime.now().isoformat(timespec="seconds"), "tag": tag,
                       "index": str(idx), "n_runs": len(rows), "n_index_total": len(all_rows),
                       "explicit": explicit, "ranked_on": PRIMARY, "concurrency": CONCURRENCY,
                       "project_to": PROJECT_TO, "bootstrap_n": BOOTSTRAP_N,
                       "min_support": MIN_SUPPORT}

    # ---- comparability / FLAGS ----
    golds = {r.get("gold_file") for r in rows}
    shas = {r.get("prompt_sha256") for r in rows}
    if len(golds) > 1 and explicit is False:
        pass  # handled below via hard exit for explicit; "all" mode still compares, flagged
    if len(golds) > 1 and explicit:
        sys.exit("ERROR: runs used DIFFERENT gold files -- not comparable:\n"
                 + "\n".join(f"  {g}" for g in sorted(golds) if g))

    passed, failed = [], []
    for r in rows:
        f = gate(r)
        (failed if f else passed).append((r, f))
    ranked = rows if explicit else [r for r, _ in passed]

    flags = {
        "GOLD_UNIFORM": str(len(golds) <= 1).lower(),
        "PROMPT_UNIFORM": str(len(shas) <= 1).lower(),
        "GATE_MODE": "explicit" if explicit else "all",
        "N_GATE_FAILURES": str(len(failed)),
        "N_DISQUALIFIED": str(0 if explicit else len(failed)),
        "GATE": "pass" if not failed else ("warn" if explicit else "fail"),
    }
    add("-" * 92)
    add("FLAGS")
    add("-" * 92)
    for line in [f"{k}={v}" for k, v in sorted(flags.items())]:
        add(line)
    add("")
    sidecar["flags"] = flags

    if not ranked:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "comparison_report.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return

    # ---- RUN METADATA ----
    meta_rows = [run_meta_row(r) for r in ranked]
    add("-" * 92)
    add("RUN METADATA")
    add("-" * 92)
    render_table(add,
        ["run_id", "model", "effort", "prompt_name", "prompt_sha", "seed", "temperature",
         "max_tokens", "eval_set_n", "codebook_version", "started_at", "finished_at"],
        ["", "", "", "", "", "", "", "", "n", "", "", ""],
        [[m["run_id"], m["model"], m["effort"], m["prompt_name"], m["prompt_sha"], m["seed"],
          fmt_na(m["temperature"], lambda v: f"{v}"), fmt_na(m["max_tokens"], lambda v: f"{v}"),
          m["eval_set_n"], fmt_na(m["codebook_version"], str), fmt_na(m["started_at"], str),
          fmt_na(m["finished_at"], str)] for m in meta_rows])
    add("")
    sidecar["run_metadata"] = meta_rows

    # ---- COMPLIANCE GATE FAILURES ----
    add("-" * 92)
    add("COMPLIANCE GATE FAILURES")
    add("-" * 92)
    if failed:
        render_table(add, ["run_id", "failed_checks"], ["", ""],
                    [[rid(r), "; ".join(f)] for r, f in failed])
    else:
        add("  (none)")
    add("")

    # ---- per-review data ----
    per = {label_of(r): load_perreview(r) for r in ranked}
    have = {k: v for k, v in per.items() if v}
    ids: list[str] = []
    cis: dict[str, tuple] = {}
    win_ru_stats = None  # (win_frac, mean_gap, sd_gap) for the top-2 pair, computed once

    repeat_groups = n_repeat_groups(rows)
    variant_tags = {rr.get("tag") for grp in repeat_groups.values() for rr in grp}

    # ---- LEADERBOARD ----
    top_f1 = ranked[0].get(PRIMARY, 0)
    lb_rows = []
    for i, r in enumerate(ranked, 1):
        pr = per.get(label_of(r)) or {}
        own_ids = sorted(pr.keys())
        card = cardinality_stats(pr, own_ids) if own_ids else {}
        jm, ms = jaccard_masi_means(pr, own_ids)
        tokens = r.get("tokens") or {}
        n_scored = max(r.get("n_scored", 1), 1)
        lb_rows.append({
            "rank": i, "run_id": rid(r), "delta_from_top": r.get(PRIMARY, 0) - top_f1,
            "micro_f1": r.get(PRIMARY, 0), "micro_p": r.get("micro_p", 0),
            "micro_r": r.get("micro_r", 0), "class_macro_f1": r.get("class_macro_f1", 0),
            "meso_macro_f1": r.get("meso_macro_f1", 0),
            "all_label_macro_f1": all_label_macro_f1(r), "exact_match": r.get("exact_match", 0),
            "jaccard_mean": jm, "masi_mean": ms, "none_p": r.get("none_p", 0),
            "none_r": r.get("none_r", 0), "none_f1": r.get("none_f1", 0),
            "labels_per_review_mean": card.get("labels_per_review_mean"),
            "cardinality_ratio": card.get("cardinality_ratio"),
            "label_count_bias": card.get("label_count_bias"),
            "reviews_with_fp_n": card.get("reviews_with_fp_n"),
            "reviews_with_fn_n": card.get("reviews_with_fn_n"),
            "reviews_exact_correct_n": card.get("reviews_exact_correct_n"),
            "latency_p50": r.get("latency_p50", 0), "latency_p95": r.get("latency_p95", 0),
            "wall_clock_hours_at_200k": r.get("wall_clock_hours_at_200k", 0),
            "tokens_in_per_review": tokens.get("input_tokens", 0) / n_scored,
            "tokens_out_per_review": tokens.get("output_tokens", 0) / n_scored,
            "usd_per_review": r.get("usd_per_review", 0), cost_key: r.get(cost_key, 0),
            "run_variance": r.get("tag") in variant_tags,
        })
    add("-" * 92)
    add("LEADERBOARD")
    add("-" * 92)
    render_table(add,
        ["rank", "run_id", "d_top", "microF1", "P", "R", "clsMac", "mesoMac", "allMac",
         "exact", "Jaccard", "MASI", "NoneP", "NoneR", "$/rev", "$/200k", "p50", "p95",
         "wallclk_h", "tok_in", "tok_out", "var"],
        ["", "", "F1", "F1", "F1", "F1", "F1", "F1", "F1", "rate", "0-1", "0-1", "0-1",
         "0-1", "USD", "USD", "s", "s", "h@200k", "n/rev", "n/rev", ""],
        [[r["rank"], r["run_id"], f"{r['delta_from_top']:+.3f}", fmt_metric(r["micro_f1"]),
          fmt_metric(r["micro_p"]), fmt_metric(r["micro_r"]), fmt_metric(r["class_macro_f1"]),
          fmt_metric(r["meso_macro_f1"]), fmt_metric(r["all_label_macro_f1"]),
          fmt_metric(r["exact_match"]), fmt_na(r["jaccard_mean"]), fmt_na(r["masi_mean"]),
          fmt_metric(r["none_p"]), fmt_metric(r["none_r"]), fmt_usd_rev(r["usd_per_review"]),
          fmt_usd_200k(r[cost_key]), fmt_latency(r["latency_p50"]), fmt_latency(r["latency_p95"]),
          f"{r['wall_clock_hours_at_200k']:.1f}", f"{r['tokens_in_per_review']:.0f}",
          f"{r['tokens_out_per_review']:.0f}", str(r["run_variance"]).lower()]
         for r in lb_rows])
    add("")
    sidecar["leaderboard"] = lb_rows

    # ---- PARETO x2 ----
    front_cost = pareto(ranked, cost_key)
    front_wall = pareto(ranked, "wall_clock_hours_at_200k")
    add("-" * 92)
    add(f"PARETO -- {PRIMARY} vs {cost_key}")
    add("-" * 92)
    render_table(add, ["run_id", PRIMARY, cost_key], ["", "F1", "USD"],
                [[rid(r), fmt_metric(r[PRIMARY]), fmt_usd_200k(r[cost_key])] for r in front_cost])
    dominated_cost = [rid(r) for r in ranked if r not in front_cost]
    if dominated_cost:
        add(f"  dominated={','.join(dominated_cost)}")
    add("")
    add("-" * 92)
    add(f"PARETO -- {PRIMARY} vs wall_clock_hours_at_200k")
    add("-" * 92)
    render_table(add, ["run_id", PRIMARY, "wall_clock_hours_at_200k"], ["", "F1", "h@200k"],
                [[rid(r), fmt_metric(r[PRIMARY]), f"{r['wall_clock_hours_at_200k']:.1f}"]
                 for r in front_wall])
    dominated_wall = [rid(r) for r in ranked if r not in front_wall]
    if dominated_wall:
        add(f"  dominated={','.join(dominated_wall)}")
    add("")
    sidecar["pareto"] = {
        "quality_vs_cost": [{"run_id": rid(r), PRIMARY: r[PRIMARY], cost_key: r[cost_key]} for r in front_cost],
        "quality_vs_wallclock": [{"run_id": rid(r), PRIMARY: r[PRIMARY],
                                  "wall_clock_hours_at_200k": r["wall_clock_hours_at_200k"]}
                                 for r in front_wall],
    }

    # ---- SIGNIFICANCE ----
    if len(have) >= 1:
        common = set.intersection(*[set(v) for v in have.values()])
        ids = sorted(common)
        add("-" * 92)
        add(f"SIGNIFICANCE  n_resamples={BOOTSTRAP_N} shared_n={len(ids)}")
        add(f"SIG_THRESHOLD={SIG_THRESHOLD} GREY_ZONE=[{GREY_ZONE[0]},{GREY_ZONE[1]}]")
        ci_rows = []
        for name, pr in have.items():
            lo, hi = bootstrap_ci(pr, ids, BOOTSTRAP_N, BOOTSTRAP_SEED)
            cis[name] = (lo, hi)
            r = next(rr for rr in ranked if label_of(rr) == name)
            ci_rows.append({"run_id": rid(r), "ci_lo": lo, "ci_hi": hi, "ci_width": hi - lo})
        add("-" * 92)
        render_table(add, ["run_id", "ci_lo", "ci_hi", "ci_width"], ["", "F1", "F1", "F1"],
                    [[c["run_id"], fmt_metric(c["ci_lo"]), fmt_metric(c["ci_hi"]),
                      fmt_metric(c["ci_width"])] for c in ci_rows])
        add("")
        sig_sidecar = {"n_resamples": BOOTSTRAP_N, "shared_n": len(ids),
                      "sig_threshold": SIG_THRESHOLD, "grey_zone": list(GREY_ZONE), "ci": ci_rows}

        pairwise = []
        if len(have) >= 2:
            names = [label_of(r) for r in ranked if label_of(r) in have]
            add("  pairwise: P(row beats column) over resamples")
            id_of = {label_of(r): rid(r) for r in ranked}
            add("    " + "".ljust(20) + "".join(id_of[n][:16].ljust(18) for n in names))
            for a in names:
                cells = []
                for b in names:
                    if a == b:
                        cells.append("-".ljust(18))
                    else:
                        w, gap, sd = paired_bootstrap(have[a], have[b], ids, BOOTSTRAP_N, BOOTSTRAP_SEED)
                        cells.append(f"{w:.2f} ({gap:+.3f})".ljust(18))
                        pairwise.append({"run_a": id_of[a], "run_b": id_of[b], "p_win": w,
                                        "mean_gap": gap, "sd_gap": sd})
                add("    " + id_of[a][:18].ljust(20) + "".join(cells))
            add("")
            if len(ranked) > 1 and label_of(ranked[0]) in have and label_of(ranked[1]) in have:
                win_ru_stats = paired_bootstrap(have[label_of(ranked[0])], have[label_of(ranked[1])],
                                                ids, BOOTSTRAP_N, BOOTSTRAP_SEED)
                add(f"MDE_AT_N={mde_at_n(win_ru_stats[2]):.3f}")
            add("")
        sig_sidecar["pairwise"] = pairwise
        sidecar["significance"] = sig_sidecar

        # ---- UNIVERSAL FALSE NEGATIVES / POSITIVES ----
        if len(have) >= 2:
            for mode, title, sidecar_key in [("fn", "UNIVERSAL FALSE NEGATIVES", "universal_false_negatives"),
                                             ("fp", "UNIVERSAL FALSE POSITIVES", "universal_false_positives")]:
                uset = universal_set(have, ids, mode)
                add("-" * 92)
                add(title)
                add("-" * 92)
                if uset:
                    for c, d in sorted(uset.items(), key=lambda kv: -kv[1]["n"]):
                        add(f"  {c:<36} n={d['n']} review_ids={','.join(d['review_ids'])}")
                else:
                    add("  (none)")
                add("")
                sidecar[sidecar_key] = uset

            # ---- CROSS-RUN CONSENSUS ----
            per_review = consensus_per_review(have, ids)
            summary = consensus_summary(per_review)
            add("-" * 92)
            add("CROSS-RUN CONSENSUS")
            add("-" * 92)
            add(f"unanimity_rate={summary['unanimity_rate']:.3f} "
                f"n_unanimous_but_wrong={len(summary['unanimous_but_wrong'])}")
            add(f"unanimous_but_wrong_review_ids={','.join(summary['unanimous_but_wrong']) or '(none)'}")
            add("top_entropy_reviews:")
            render_table(add, ["review_id", "entropy_bits", "n_exact_match_gold"], ["", "bits", "n_runs"],
                        [[i, f"{per_review[i]['entropy_bits']:.3f}", per_review[i]["n_exact_match_gold"]]
                         for i in summary["top_entropy_reviews"]])
            add("")
            sidecar["cross_run_consensus"] = {"unanimity_rate": summary["unanimity_rate"],
                                              "top_entropy_reviews": summary["top_entropy_reviews"],
                                              "unanimous_but_wrong": summary["unanimous_but_wrong"],
                                              "per_review": per_review}

            # ---- MESO CONFUSION ----
            by_class, top_pairs = meso_confusion(have, ids)
            add("-" * 92)
            add("MESO CONFUSION")
            add("-" * 92)
            render_table(add, ["class", "swap_count"], ["", "n"],
                        [[c, n] for c, n in sorted(by_class.items(), key=lambda kv: -kv[1])])
            add("top substitutions:")
            render_table(add, ["class", "gold_label", "pred_label", "n"], ["", "", "", ""],
                        [[cls, a, b, n] for cls, a, b, n in top_pairs])
            add("")
            sidecar["meso_confusion"] = {"by_class": by_class,
                                         "top_pairs": [{"class": c, "gold_label": a, "pred_label": b, "n": n}
                                                       for c, a, b, n in top_pairs]}

            # ---- PREVALENCE ----
            labels_all = sorted({c for r in ranked for c in (r.get("per_label_support") or {})})
            prev = label_prevalence(have, ids, labels_all)
            add("-" * 92)
            add(f"PREVALENCE  gold_consistent={str(prev['gold_consistent']).lower()}")
            add("-" * 92)
            id_of = {label_of(r): rid(r) for r in ranked}
            prow = []
            for c in sorted(labels_all, key=lambda c: -prev["gold_count"][c]):
                cells = [c, prev["gold_count"][c]]
                for name in have:
                    d = prev["per_run"][name][c]
                    cells.append(f"{id_of[name]}:{d['pred_count']}/"
                                 f"{fmt_na(d['ratio'])}/{d['signed_error']:+d}")
                prow.append(cells)
            render_table(add, ["label", "gold_n"] + [f"run_{i+1}" for i in range(len(have))],
                        [""] * (2 + len(have)), prow)
            add("  (per run cell: pred_count/ratio/signed_error)")
            add("")
            sidecar["prevalence"] = prev
        else:
            for key in ("universal_false_negatives", "universal_false_positives",
                       "cross_run_consensus", "meso_confusion", "prevalence"):
                sidecar[key] = {}
    else:
        sidecar["significance"] = {}
        for key in ("universal_false_negatives", "universal_false_positives",
                   "cross_run_consensus", "meso_confusion", "prevalence"):
            sidecar[key] = {}

    # ---- PER-LABEL FULL TABLE ----
    labels_all = sorted({c for r in ranked for c in (r.get("per_label_support") or {})})
    pl_rows = []
    for c in labels_all:
        support = next((r["per_label_support"][c] for r in ranked
                        if c in (r.get("per_label_support") or {})), 0)
        scores = [(r.get("per_label_f1", {}).get(c, 0.0), rid(r)) for r in ranked]
        best_f1, best_run = max(scores)
        f1_vals = [f for f, _ in scores]
        pl_rows.append({"label": c, "support": support, "best_f1": best_f1, "best_run_id": best_run,
                        "median_f1": statistics.median(f1_vals), "spread": max(f1_vals) - min(f1_vals),
                        "below_support_floor": support < MIN_SUPPORT})
    add("-" * 92)
    add("PER-LABEL FULL TABLE  (per-run precision/recall in sidecar only)")
    add("-" * 92)
    render_table(add, ["label", "support", "best_f1", "best_run_id", "median_f1", "spread"],
                ["", "n", "F1", "", "F1", "F1"],
                [[r["label"], r["support"], fmt_flagged(r["best_f1"], r["below_support_floor"]),
                  r["best_run_id"], fmt_flagged(r["median_f1"], r["below_support_floor"]),
                  fmt_flagged(r["spread"], r["below_support_floor"])] for r in pl_rows])
    add("  (* support < MIN_SUPPORT)")
    add("")
    per_label_sidecar = {r["label"]: r for r in pl_rows}
    if have:
        id_of_name = {label_of(r): rid(r) for r in ranked}
        for name, pr in have.items():
            own_ids = sorted(pr.keys())
            prf = per_label_prf_from_perreview(pr, own_ids, labels_all)
            for c, d in prf.items():
                per_label_sidecar[c].setdefault("per_run", {})[id_of_name[name]] = d
    sidecar["per_label"] = per_label_sidecar

    # ---- REPEATABILITY ----
    repeat_stats = repeatability_stats(repeat_groups)
    between_config_gap = ranked[0].get(PRIMARY, 0) - ranked[-1].get(PRIMARY, 0)
    add("-" * 92)
    add(f"REPEATABILITY  N_REPEAT_GROUPS={len(repeat_stats)} between_config_gap={between_config_gap:.3f}")
    add("-" * 92)
    if repeat_stats:
        render_table(add, ["model", "effort", "prompt_sha", "n_repeats", "mean", "sd", "min", "max"],
                    ["", "", "", "n", "F1", "F1", "F1", "F1"],
                    [[s["model"], s["effort"], s["prompt_sha"], s["n_repeats"], fmt_metric(s["mean"]),
                      fmt_metric(s["sd"]), fmt_metric(s["min"]), fmt_metric(s["max"])]
                     for s in repeat_stats])
    else:
        add("  (no config has more than one run)")
    add("")
    sidecar["repeatability"] = {"n_repeat_groups": len(repeat_stats), "between_config_gap": between_config_gap,
                                "groups": repeat_stats}

    # ---- COMPLIANCE ----
    comp_rows = []
    for r in ranked:
        s = load_summary(r)
        comp_rows.append({"run_id": rid(r), "span_verbatim_rate": r.get("span_verbatim_rate", 0),
                          "oov_label_rate": oov_label_rate(r), "parse_failure_rate": parse_failure_rate(r),
                          "truncation_rate": truncation_rate(r), "retry_count": s.get("extra_attempts"),
                          "empty_analysis_rate": None, "gate_pass": not gate(r)})
    add("-" * 92)
    add("COMPLIANCE")
    add("-" * 92)
    render_table(add,
        ["run_id", "span_verbatim", "oov_rate", "parse_fail", "truncation", "retry_n",
         "empty_analysis", "gate_pass"],
        ["", "rate", "rate", "rate", "rate", "n", "rate", "bool"],
        [[c["run_id"], fmt_rate(c["span_verbatim_rate"]), fmt_rate(c["oov_label_rate"]),
          fmt_rate(c["parse_failure_rate"]), fmt_rate(c["truncation_rate"]),
          fmt_na(c["retry_count"], lambda v: f"{v}"), fmt_na(c["empty_analysis_rate"]),
          str(c["gate_pass"]).lower()] for c in comp_rows])
    add("")
    sidecar["compliance"] = comp_rows

    # ---- COST ----
    cpf = cost_per_f1_point(ranked, cost_key, front_cost)
    cost_rows = []
    for r in ranked:
        tokens = r.get("tokens") or {}
        n_scored = max(r.get("n_scored", 1), 1)
        c = cpf.get(label_of(r))
        cost_rows.append({"run_id": rid(r), "usd_per_review": r.get("usd_per_review", 0),
                          cost_key: r.get(cost_key, 0),
                          "tokens_in_per_review": tokens.get("input_tokens", 0) / n_scored,
                          "tokens_out_per_review": tokens.get("output_tokens", 0) / n_scored,
                          "cost_per_f1_point": c})
    add("-" * 92)
    add("COST")
    add("-" * 92)
    render_table(add, ["run_id", "$/rev", "$/200k", "tok_in/rev", "tok_out/rev", "$/F1_point"],
                ["", "USD", "USD", "n", "n", "USD"],
                [[c["run_id"], fmt_usd_rev(c["usd_per_review"]), fmt_usd_200k(c[cost_key]),
                  f"{c['tokens_in_per_review']:.0f}", f"{c['tokens_out_per_review']:.0f}",
                  c["cost_per_f1_point"] if isinstance(c["cost_per_f1_point"], str)
                  else fmt_na(c["cost_per_f1_point"], fmt_usd_200k)] for c in cost_rows])
    add("  ($/F1_point relative to the cheapest run on the quality-vs-cost frontier; "
        "'ref' = that run itself)")
    add("")
    sidecar["cost"] = cost_rows

    # ---- SELECTION ----
    win = ranked[0]
    runner_up = ranked[1] if len(ranked) > 1 else None
    selection = {"run_id": rid(win), "selection_criterion": "max micro_f1 among "
                + ("named runs" if explicit else "gate-passing runs"),
                "ranked_on": PRIMARY,
                "tie_break_rule": "gate_pass > lower $/200k > lower latency_p95 > lexical run_id",
                "margin": None, "p_win_vs_runner_up": None,
                "runner_up_run_id": rid(runner_up) if runner_up is not None else None}
    if win_ru_stats is not None:
        selection["p_win_vs_runner_up"], selection["margin"], _ = win_ru_stats
    add("=" * 92)
    add("SELECTION")
    add("=" * 92)
    for k in ["run_id", "selection_criterion", "ranked_on", "tie_break_rule", "margin",
             "p_win_vs_runner_up", "runner_up_run_id"]:
        v = selection[k]
        add(f"{k}=" + (fmt_metric(v) if isinstance(v, float) else str(v)))
    add("=" * 92)
    sidecar["selection"] = selection

    # ---- write ----
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "comparison_report.txt").write_text("\n".join(L) + "\n", encoding="utf-8")

    csv_rows = []
    for lb, cm, cost, meta in zip(lb_rows, comp_rows, cost_rows, meta_rows):
        row = {**lb, **{f"compliance_{k}": v for k, v in cm.items() if k != "run_id"},
              "cost_per_f1_point": cost["cost_per_f1_point"], "model": meta["model"],
              "effort": meta["effort"], "prompt_name": meta["prompt_name"],
              "prompt_sha": meta["prompt_sha"], "temperature": meta["temperature"]}
        csv_rows.append(row)
    cols = (["rank", "run_id", "model", "effort", "prompt_name", "prompt_sha", "temperature",
            "delta_from_top", "micro_f1", "micro_p", "micro_r", "class_macro_f1",
            "meso_macro_f1", "all_label_macro_f1", "exact_match", "jaccard_mean", "masi_mean",
            "none_p", "none_r", "none_f1", "labels_per_review_mean", "cardinality_ratio",
            "label_count_bias", "reviews_with_fp_n", "reviews_with_fn_n",
            "reviews_exact_correct_n", "latency_p50", "latency_p95",
            "wall_clock_hours_at_200k", "tokens_in_per_review", "tokens_out_per_review",
            "usd_per_review", cost_key, "cost_per_f1_point", "run_variance"]
           + [f"compliance_{k}" for k in ("span_verbatim_rate", "oov_label_rate",
                                          "parse_failure_rate", "truncation_rate",
                                          "retry_count", "gate_pass")])
    with open(out_dir / "comparison.csv", "w", newline="", encoding="utf-8") as f:
        wcsv = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        wcsv.writeheader()
        for row in csv_rows:
            wcsv.writerow(row)

    (out_dir / "comparison.json").write_text(json.dumps(sidecar, indent=2, default=str) + "\n",
                                             encoding="utf-8")

    notes = []
    if MAKE_FIGURES:
        gold_count_for_fig = sidecar.get("prevalence", {}).get("gold_count", {})
        meso_pairs_for_fig = sidecar.get("meso_confusion", {}).get("top_pairs", [])
        meso_pairs_for_fig = [(p["class"], p["gold_label"], p["pred_label"], p["n"])
                              for p in meso_pairs_for_fig]
        notes = make_figures(out_dir / "figures", rows, ranked, cost_key, cis,
                             gold_count_for_fig, meso_pairs_for_fig)

    (out_dir / "selection.json").write_text(json.dumps({
        "tag": tag, "generated": datetime.now().isoformat(timespec="seconds"),
        "mode": "explicit" if explicit else "all", "index": str(idx), "primary_metric": PRIMARY,
        "flags": flags, "selection": selection,
        "runs": [{"run_id": rid(r), "model": r.get("model"), "reasoning_effort": r.get("reasoning_effort"),
                 "prompt_stem": prompt_of(r), "prompt_sha256": r.get("prompt_sha256"),
                 "gold_file": r.get("gold_file"), "run_dir": r.get("run_dir"),
                 PRIMARY: r.get(PRIMARY), "gate_failures": gate(r)} for r in rows],
    }, indent=2) + "\n", encoding="utf-8")

    print("\n".join(L))
    print(f"\nwrote {show(out_dir / 'comparison_report.txt')}")
    print(f"wrote {show(out_dir / 'comparison.csv')}")
    print(f"wrote {show(out_dir / 'comparison.json')}")
    print(f"wrote {show(out_dir / 'selection.json')}")
    for n in notes:
        print(f"  {n}")


if __name__ == "__main__":
    main()
