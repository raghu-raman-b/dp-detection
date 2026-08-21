#!/usr/bin/env python3
"""
compare_runs.py -- compare every run in run-stats/index.jsonl.

Ranks on micro-F1 (stable at n=50; the meso macro moves several points on one
decision because it averages over ~13 labels). Compliance is a GATE, not a column:
a model that scores well but emits unparseable JSON is unusable at 200k.

Significance uses a PAIRED bootstrap over review ids. Every model saw the same 50
reviews, so pairing removes review difficulty from the comparison and is far more
sensitive than independent confidence intervals. A 0.03 micro-F1 gap at n=50 is
usually noise, and this is what tells you so.

Outputs:
    <OUT_ROOT>/comparison/<stamp>/comparison_report.txt
    <OUT_ROOT>/comparison/<stamp>/comparison.csv
    <OUT_ROOT>/comparison/<stamp>/figures/*.png
"""

from __future__ import annotations
import csv, json, random, statistics, sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# ============================== CONFIG ==============================
OUT_ROOT       = "../outputs/run-stats"
INDEX_FILE     = "../outputs/run-stats/index.jsonl"
PRIMARY        = "micro_f1"        # ranking metric
PROJECT_TO     = 200_000
BOOTSTRAP_N    = 2000
BOOTSTRAP_SEED = 20260821
MIN_SUPPORT    = 3                 # labels shown in the heatmap
MAKE_FIGURES   = True
DPI            = 200

# compliance gates -- failing any of these disqualifies a run from the ranking
GATE_PARSE_RATE      = 1.00
GATE_MAX_TRUNCATED   = 0
GATE_MAX_BAD_CODES   = 0
GATE_MAX_API_ERRORS  = 0
GATE_SPAN_VERBATIM   = 0.95
# ====================================================================


def jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def config_key(r: dict) -> tuple:
    return (r.get("provider"), r.get("model"), r.get("reasoning_effort"),
            r.get("web_search"), r.get("prompt_sha256"))


def label_of(r: dict) -> str:
    ws = "" if r.get("web_search") else " no-search"
    return f"{r.get('model')} [{r.get('reasoning_effort')}]{ws}"


def gate(r: dict) -> list[str]:
    fails = []
    n = max(r.get("n_requests", 0), 1)
    if r.get("parsed", 0) / n < GATE_PARSE_RATE:
        fails.append(f"parse rate {r.get('parsed',0)}/{n}")
    if r.get("truncated", 0) > GATE_MAX_TRUNCATED:
        fails.append(f"{r['truncated']} truncated")
    if r.get("bad_codes", 0) > GATE_MAX_BAD_CODES:
        fails.append(f"{r['bad_codes']} out-of-vocab codes")
    if r.get("api_errors", 0) > GATE_MAX_API_ERRORS:
        fails.append(f"{r['api_errors']} api errors")
    if r.get("span_verbatim_rate", 1.0) < GATE_SPAN_VERBATIM:
        fails.append(f"span verbatim {r.get('span_verbatim_rate'):.3f}")
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


def paired_bootstrap(a: dict, b: dict, ids: list[str], n: int, seed: int) -> tuple[float, float]:
    """Fraction of resamples where a > b, and the mean gap. Resamples review ids,
    so both models are scored on the same draw every time."""
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
    return wins / n, statistics.mean(gaps)


def bootstrap_ci(pr: dict, ids: list[str], n: int, seed: int) -> tuple[float, float]:
    rng = random.Random(seed)
    vals = []
    k = len(ids)
    for _ in range(n):
        draw = [ids[rng.randrange(k)] for _ in range(k)]
        vals.append(micro_f1([pr[i] for i in draw]))
    vals.sort()
    return vals[int(0.025 * n)], vals[int(0.975 * n) - 1]


def pareto(rows: list[dict], cost_key: str) -> list[dict]:
    """Not dominated on (higher PRIMARY, lower cost)."""
    front = []
    for r in rows:
        if not any(o is not r and o[PRIMARY] >= r[PRIMARY] and o[cost_key] <= r[cost_key]
                   and (o[PRIMARY] > r[PRIMARY] or o[cost_key] < r[cost_key]) for o in rows):
            front.append(r)
    return sorted(front, key=lambda r: r[cost_key])


# ------------------------------------------------------------------ figures

def make_figures(fig_dir: Path, rows: list[dict], ranked: list[dict],
                 cost_key: str, cis: dict, per: dict, ids: list[str]) -> list[str]:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        return ["matplotlib not installed - figures skipped (pip install matplotlib)"]

    fig_dir.mkdir(parents=True, exist_ok=True)
    made = []
    plt.rcParams.update({"figure.dpi": DPI, "font.size": 9, "axes.grid": True,
                         "grid.alpha": 0.25, "axes.spines.top": False,
                         "axes.spines.right": False})
    palette = plt.cm.tab10.colors

    # 1. quality vs cost, with the pareto frontier
    front = pareto(ranked, cost_key)
    fig, ax = plt.subplots(figsize=(7.5, 5))
    for i, r in enumerate(ranked):
        ax.scatter(r[cost_key], r[PRIMARY], s=160, color=palette[i % 10],
                   edgecolor="white", linewidth=1.5, zorder=3, label=label_of(r))
        ax.annotate(label_of(r), (r[cost_key], r[PRIMARY]), fontsize=7,
                    xytext=(6, 6), textcoords="offset points")
    if len(front) > 1:
        ax.plot([r[cost_key] for r in front], [r[PRIMARY] for r in front],
                "--", color="0.4", linewidth=1.4, zorder=2, label="Pareto frontier")
    ax.set_xlabel(f"projected cost at {PROJECT_TO:,} reviews (USD)")
    ax.set_ylabel(PRIMARY.replace("_", "-"))
    ax.set_title("Quality vs cost")
    ax.legend(fontsize=7, loc="lower right")
    fig.tight_layout(); fig.savefig(fig_dir / "1_quality_vs_cost.png"); plt.close(fig)
    made.append("1_quality_vs_cost.png")

    # 2. precision / recall / f1 with bootstrap CI on f1
    fig, ax = plt.subplots(figsize=(max(7, 1.6 * len(ranked)), 4.6))
    x = np.arange(len(ranked)); w = 0.26
    ax.bar(x - w, [r["micro_p"] for r in ranked], w, label="precision", color=palette[0])
    ax.bar(x, [r["micro_r"] for r in ranked], w, label="recall", color=palette[1])
    f1s = [r[PRIMARY] for r in ranked]
    err = np.array([[f - cis[label_of(r)][0], cis[label_of(r)][1] - f]
                    for r, f in zip(ranked, f1s)]).T if cis else None
    ax.bar(x + w, f1s, w, yerr=err, capsize=3, label="micro-F1", color=palette[2])
    ax.set_xticks(x); ax.set_xticklabels([label_of(r) for r in ranked], rotation=20, ha="right")
    ax.set_ylim(0, 1.02); ax.set_ylabel("score")
    ax.set_title("Precision vs recall (whiskers: 95% paired bootstrap CI on F1)")
    ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(fig_dir / "2_precision_recall.png"); plt.close(fig)
    made.append("2_precision_recall.png")

    # 3. label x model heatmap, labels with enough support
    labels = sorted({c for r in ranked for c, s in (r.get("per_label_support") or {}).items()
                     if s >= MIN_SUPPORT})
    if labels:
        M = np.array([[(r.get("per_label_f1") or {}).get(c, np.nan) for r in ranked]
                      for c in labels], dtype=float)
        fig, ax = plt.subplots(figsize=(1.4 * len(ranked) + 3.5, 0.32 * len(labels) + 2))
        im = ax.imshow(M, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
        ax.set_xticks(range(len(ranked)))
        ax.set_xticklabels([label_of(r) for r in ranked], rotation=20, ha="right", fontsize=7)
        ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels, fontsize=7)
        for i in range(len(labels)):
            for j in range(len(ranked)):
                if not np.isnan(M[i, j]):
                    ax.text(j, i, f"{M[i,j]:.2f}", ha="center", va="center", fontsize=6)
        ax.set_title(f"Per-label F1 (support >= {MIN_SUPPORT})")
        ax.grid(False)
        fig.colorbar(im, ax=ax, shrink=0.7)
        fig.tight_layout(); fig.savefig(fig_dir / "3_label_heatmap.png"); plt.close(fig)
        made.append("3_label_heatmap.png")

    # 4. reasoning effort sweep
    order = ["none", "low", "medium", "high", "xhigh", "max"]
    by_model = defaultdict(list)
    for r in rows:
        by_model[r["model"]].append(r)
    sweeps = {m: sorted([r for r in v if r.get("reasoning_effort") in order],
                        key=lambda r: order.index(r["reasoning_effort"]))
              for m, v in by_model.items()}
    sweeps = {m: v for m, v in sweeps.items() if len(v) > 1}
    if sweeps:
        fig, ax = plt.subplots(figsize=(7, 4.6))
        ax2 = ax.twinx()
        for i, (m, v) in enumerate(sweeps.items()):
            xs = [order.index(r["reasoning_effort"]) for r in v]
            ax.plot(xs, [r[PRIMARY] for r in v], "o-", color=palette[i % 10], label=f"{m} F1")
            ax2.plot(xs, [r[cost_key] for r in v], "s--", color=palette[i % 10],
                     alpha=0.45, label=f"{m} cost")
        ax.set_xticks(range(len(order))); ax.set_xticklabels(order)
        ax.set_xlabel("reasoning effort"); ax.set_ylabel(PRIMARY.replace("_", "-"))
        ax2.set_ylabel(f"USD at {PROJECT_TO:,}"); ax2.grid(False)
        ax.set_title("Reasoning effort: quality (solid) vs cost (dashed)")
        ax.legend(fontsize=7, loc="lower right")
        fig.tight_layout(); fig.savefig(fig_dir / "4_reasoning_sweep.png"); plt.close(fig)
        made.append("4_reasoning_sweep.png")

    # 5. compliance
    fig, ax = plt.subplots(figsize=(max(7, 1.6 * len(rows)), 4.2))
    x = np.arange(len(rows)); w = 0.38
    ax.bar(x - w/2, [r.get("parsed", 0)/max(r.get("n_requests", 1), 1) for r in rows], w,
           label="parse rate", color=palette[0])
    ax.bar(x + w/2, [r.get("span_verbatim_rate", 0) for r in rows], w,
           label="span verbatim rate", color=palette[3])
    ax.axhline(GATE_SPAN_VERBATIM, color="crimson", ls=":", lw=1.2,
               label=f"span gate {GATE_SPAN_VERBATIM}")
    ax.set_xticks(x); ax.set_xticklabels([label_of(r) for r in rows], rotation=20, ha="right")
    ax.set_ylim(0, 1.05); ax.set_title("Compliance gates")
    ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(fig_dir / "5_compliance.png"); plt.close(fig)
    made.append("5_compliance.png")
    return made


# --------------------------------------------------------------------- main

def main() -> None:
    idx = Path(INDEX_FILE)
    if not idx.exists():
        sys.exit(f"no index at {idx} -- run compute_stats.py first")
    all_rows = jsonl(idx)

    # keep the latest row per config
    latest, dupes = {}, 0
    for r in all_rows:
        k = config_key(r)
        if k in latest:
            dupes += 1
        latest[k] = r
    rows = sorted(latest.values(), key=lambda r: -r.get(PRIMARY, 0))
    cost_key = f"projected_usd_at_{PROJECT_TO}"

    L, add = [], None
    add = L.append
    add("=" * 86)
    add("PROVIDER / MODEL COMPARISON")
    add("=" * 86)
    add(f"generated     {datetime.now().isoformat(timespec='seconds')}")
    add(f"index         {INDEX_FILE}")
    add(f"runs          {len(rows)} configs from {len(all_rows)} rows"
        + (f" ({dupes} superseded by later runs)" if dupes else ""))
    add(f"ranked on     {PRIMARY}")
    add("")

    # comparability
    golds = {r.get("gold_file") for r in rows}
    shas = {(r.get("prompt_sha256") or "")[:12] for r in rows}
    if len(golds) > 1:
        add("!! runs used DIFFERENT gold files -- not comparable:")
        for g in sorted(golds):
            add(f"     {g}")
        add("")
    if len(shas) > 1:
        add("!! runs used DIFFERENT prompts. Fine when comparing prompt versions,")
        add("   NOT fine when comparing providers. Prompt shas present:")
        for r in rows:
            add(f"     {(r.get('prompt_sha256') or '')[:12]}  {label_of(r)}")
        add("")

    # gates
    passed, failed = [], []
    for r in rows:
        f = gate(r)
        (failed if f else passed).append((r, f))
    if failed:
        add("-" * 86)
        add("DISQUALIFIED (compliance gate)")
        add("-" * 86)
        for r, f in failed:
            add(f"  {label_of(r):<42} {'; '.join(f)}")
        add("  A model that cannot emit valid output is unusable at 200k, whatever it scores.")
        add("")
    ranked = [r for r, _ in passed]
    if not ranked:
        add("no run passed the gates.")
        Path(OUT_ROOT).mkdir(parents=True, exist_ok=True)
        print("\n".join(L))
        return

    # leaderboard
    add("-" * 86)
    add("LEADERBOARD")
    add("-" * 86)
    add(f"  {'model [effort]':<34} {'microF1':>8} {'P':>7} {'R':>7} {'clsMac':>7} "
        f"{'None F1':>8} {'$/rev':>9} {'$/200k':>9}")
    for r in ranked:
        add(f"  {label_of(r):<34} {r.get(PRIMARY,0):8.3f} {r.get('micro_p',0):7.3f} "
            f"{r.get('micro_r',0):7.3f} {r.get('class_macro_f1',0):7.3f} "
            f"{r.get('none_f1',0):8.3f} {r.get('usd_per_review',0):9.5f} "
            f"{r.get(cost_key,0):9.0f}")
    add("")

    # pareto
    front = pareto(ranked, cost_key)
    add("-" * 86)
    add("PARETO FRONTIER (not beaten on both quality and cost)")
    add("-" * 86)
    for r in front:
        add(f"  {label_of(r):<42} {r.get(PRIMARY,0):.3f} @ ${r.get(cost_key,0):,.0f}")
    dominated = [r for r in ranked if r not in front]
    if dominated:
        add("  dominated (something is both better and cheaper):")
        for r in dominated:
            add(f"    {label_of(r)}")
    add("")

    # paired bootstrap
    per = {label_of(r): load_perreview(r) for r in ranked}
    have = {k: v for k, v in per.items() if v}
    cis = {}
    if len(have) >= 1:
        common = set.intersection(*[set(v) for v in have.values()])
        ids = sorted(common)
        add("-" * 86)
        add(f"SIGNIFICANCE  paired bootstrap, {BOOTSTRAP_N} resamples over {len(ids)} shared reviews")
        add("-" * 86)
        for name, pr in have.items():
            lo, hi = bootstrap_ci(pr, ids, BOOTSTRAP_N, BOOTSTRAP_SEED)
            cis[name] = (lo, hi)
            add(f"  {name:<42} 95% CI [{lo:.3f}, {hi:.3f}]")
        add("")
        if len(have) >= 2:
            add("  pairwise: P(row beats column) over resamples")
            names = [label_of(r) for r in ranked if label_of(r) in have]
            add("    " + "".ljust(30) + "".join(n[:14].ljust(16) for n in names))
            for a in names:
                cells = []
                for b in names:
                    if a == b:
                        cells.append("-".ljust(16))
                    else:
                        w, gap = paired_bootstrap(have[a], have[b], ids,
                                                  BOOTSTRAP_N, BOOTSTRAP_SEED)
                        cells.append(f"{w:.2f} ({gap:+.3f})".ljust(16))
                add("    " + a[:28].ljust(30) + "".join(cells))
            add("")
            add("  Read: 0.95+ is a real difference. 0.6-0.9 is a lean, not a result.")
            add("  At n=50 a gap under ~0.05 micro-F1 will usually land in the grey zone.")
        add("")

        # reviews everyone got wrong -> codebook, not model
        if len(have) >= 2:
            allmiss = defaultdict(set)
            for name, pr in have.items():
                for i in ids:
                    g, p = pr[i]
                    for c in g - p:
                        allmiss[(i, c)].add(name)
            universal = [(i, c) for (i, c), who in allmiss.items() if len(who) == len(have)]
            if universal:
                add("-" * 86)
                add("MISSED BY EVERY MODEL  (suspect the codebook or the gold, not the model)")
                add("-" * 86)
                bylab = defaultdict(list)
                for i, c in universal:
                    bylab[c].append(i)
                for c, revs in sorted(bylab.items(), key=lambda kv: -len(kv[1])):
                    add(f"  {c:<36} {len(revs)} reviews")
                add("")

    # per-label winners
    add("-" * 86)
    add(f"PER-LABEL BEST (support >= {MIN_SUPPORT} in that run)")
    add("-" * 86)
    labels = sorted({c for r in ranked for c, s in (r.get("per_label_support") or {}).items()
                     if s >= MIN_SUPPORT})
    for c in labels:
        scores = [(r.get("per_label_f1", {}).get(c), label_of(r)) for r in ranked
                  if (r.get("per_label_support") or {}).get(c, 0) >= MIN_SUPPORT]
        scores = [(f, n) for f, n in scores if f is not None]
        if scores:
            best = max(scores)
            spread = best[0] - min(scores)[0]
            add(f"  {c:<36} {best[0]:.3f}  {best[1]:<32} (spread {spread:.3f})")
    add("")

    # recommendation
    win = ranked[0]
    add("=" * 86)
    add("RECOMMENDATION")
    add("=" * 86)
    add(f"  {label_of(win)}   {PRIMARY} {win.get(PRIMARY,0):.3f}  "
        f"${win.get(cost_key,0):,.0f} at {PROJECT_TO:,}")
    if len(ranked) > 1 and label_of(win) in cis and label_of(ranked[1]) in cis:
        w, gap = paired_bootstrap(have[label_of(win)], have[label_of(ranked[1])],
                                  ids, BOOTSTRAP_N, BOOTSTRAP_SEED)
        verdict = ("a real margin" if w >= 0.95 else
                   "a lean, not a result -- pick on cost or compliance instead")
        add(f"  vs {label_of(ranked[1])}: wins {w:.0%} of resamples ({gap:+.3f}) -> {verdict}")
    if win.get("micro_r", 1) < win.get("micro_p", 0) - 0.1:
        add(f"  NOTE: recall {win.get('micro_r',0):.3f} well below precision "
            f"{win.get('micro_p',0):.3f} -- it under-labels. Check the errors.md split "
            f"between 'named then dropped' and 'never named' before tuning.")
    add("")
    add("  This set is BURNED. It drove prompt tuning and this selection, so the number")
    add("  above is a max-over-configs statistic and never appears in the paper. Only the")
    add("  frozen winner touches the 75 adjudicated set, exactly once.")
    add("=" * 86)

    # ---- write ----
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = Path(OUT_ROOT) / "comparison" / stamp
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "comparison_report.txt").write_text("\n".join(L) + "\n", encoding="utf-8")

    cols = ["provider", "model", "reasoning_effort", "web_search", "micro_f1", "micro_p",
            "micro_r", "example_f1", "class_macro_f1", "meso_macro_f1", "none_p", "none_r",
            "none_f1", "exact_match", "tp", "fp", "fn", "missed_but_named_in_analysis",
            "parsed", "truncated", "bad_codes", "span_verbatim_rate", "cache_hit_rate",
            "mean_output_tokens", "mean_reasoning_tokens", "usd_per_review", cost_key,
            "latency_p50", "search_rate", "prompt_sha256", "tag"]
    with open(out_dir / "comparison.csv", "w", newline="", encoding="utf-8") as f:
        wcsv = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        wcsv.writeheader()
        for r in rows:
            wcsv.writerow(r)

    notes = []
    if MAKE_FIGURES:
        notes = make_figures(out_dir / "figures", rows, ranked, cost_key, cis, per,
                             sorted(set.intersection(*[set(v) for v in have.values()]))
                             if have else [])

    print("\n".join(L))
    print(f"\nwrote {out_dir / 'comparison_report.txt'}")
    print(f"wrote {out_dir / 'comparison.csv'}")
    for n in notes:
        print(f"  {n}")


if __name__ == "__main__":
    main()