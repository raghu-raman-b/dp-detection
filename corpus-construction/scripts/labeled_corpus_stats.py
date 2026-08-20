#!/usr/bin/env python3
"""
corpus_stats.py — descriptive statistics and paper figures for the
hand-labeled dark-pattern review corpus.

Reads every *.jsonl in INPUT_DIR, quarantines any record whose label
representations disagree, computes stats on the clean remainder, and writes:

    OUTPUT_DIR/corpus_stats.txt     all numbers, copy-paste ready
    OUTPUT_DIR/figures/*.png        600 dpi, double-column width

Dependencies: matplotlib, numpy. Nothing else.

Records are EXCLUDED (not silently repaired) when any of these hold:
  - the binary columns, the `labels` array and `labels_str` do not agree
  - none=1 but labels are present, or none=0 but no labels are present
  - a required field is missing or empty
  - an unrecognised label code appears
  - the same review_id appears twice with different label sets
Every exclusion is listed by review_id at the end of the text report.
"""

import json
import math
import re
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# ─────────────────────────── CONFIG ───────────────────────────

INPUT_DIR = "../labeled_data"
OUTPUT_DIR = "../outputs/labeled_data_stats"

SIZE_OF_POOL = 200_000        # post-filter pool the sample was drawn from

FIG_WIDTH = 7.0               # inches, double column
DPI = 600

TOP_N_GAMES = 15
TOP_N_PAIRS = 15

# ──────────────────────────────────────────────────────────────

LABELS = [
    "T_PlayingByAppointment", "T_DailyRewards", "T_Grinding", "T_Advertisement",
    "T_InfiniteTreadmill", "T_MandatoryMarathon",
    "M_PayToProgress", "M_IntermediateCurrency", "M_DeceptiveLuxury",
    "M_RecurringFee", "M_Gambling", "M_PowerCreep", "M_WasteAversion",
    "M_EasyToPurchase", "M_UIMisdirection", "M_NeverEndingLure",
    "S_ForcedFellowship", "S_FriendSpamImpersonation", "S_Reciprocity",
    "S_EncouragesAntiSocialBehavior", "S_FearOfMissingOutFOMO", "S_Competition",
    "P_EasyToGetHardToLose", "P_CompleteTheCollection", "P_IllusionOfControl",
    "P_AestheticManipulation", "P_OptimismAndFrequencyBiases", "P_RewardMania",
    "Tech_FragmentedDownloads",
]

CLASS_OF = {c: (c.split("_", 1)[0]) for c in LABELS}
CLASSES = ["T", "M", "S", "P", "Tech"]
CLASS_NAME = {
    "T": "Temporal", "M": "Monetary", "S": "Social",
    "P": "Psychological", "Tech": "Technical",
}

# Okabe-Ito, colorblind safe and still saturated in print.
CLASS_COLOR = {
    "T": "#0072B2",
    "M": "#D55E00",
    "S": "#009E73",
    "P": "#CC79A7",
    "Tech": "#E69F00",
}

HEAT_CMAP = LinearSegmentedColormap.from_list(
    "dpheat", ["#FFFFFF", "#BFE3F2", "#4FA8D8", "#2B5FA8", "#1B2E6E"]
)

REQUIRED_FIELDS = ["review_id", "app_id", "game_name", "market",
                   "review_date", "star_rating", "review_text", "stratum"]


def pretty(code):
    """P_IllusionOfControl -> 'Illusion of Control' for axis labels."""
    body = code.split("_", 1)[1]
    # split lower-to-upper and upper-to-upperlower, so UI and FOMO survive
    body = re.sub(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", " ", body)
    body = re.sub(r"\s+", " ", body).strip()
    small = {"Of": "of", "And": "and", "To": "to", "The": "the", "By": "by"}
    parts = [small.get(w, w) for w in body.split(" ")]
    return " ".join(parts)


def norm(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


NORM_CODE = {c: norm(c) for c in LABELS}


def truthy(v):
    return str(v).strip() in ("1", "1.0", "True", "true", "yes")


# ──────────────────────── load and validate ────────────────────────

def parse_labels_str(s):
    """
    labels_str looks like 'P: Illusion of Control' or several joined by a
    separator. Rather than guessing the separator, match each known code
    against the normalised string. No code is a substring of another, so
    this is unambiguous.
    """
    if not s or not str(s).strip():
        return set()
    n = norm(s)
    return {c for c in LABELS if NORM_CODE[c] in n}


def validate(rec):
    """Return (label_set, list_of_problems)."""
    problems = []

    for f in REQUIRED_FIELDS:
        v = rec.get(f)
        if v is None or (isinstance(v, str) and not v.strip()):
            problems.append(f"missing field '{f}'")

    arr_raw = rec.get("labels")
    arr = set(arr_raw) if isinstance(arr_raw, list) else set()
    if arr_raw is None:
        problems.append("no 'labels' array")

    unknown = arr - set(LABELS)
    if unknown:
        problems.append("unknown label code(s): " + ", ".join(sorted(unknown)))
    arr &= set(LABELS)

    cols = {c for c in LABELS if truthy(rec.get(c))}
    strs = parse_labels_str(rec.get("labels_str", ""))

    if cols != arr:
        d1 = ", ".join(sorted(cols - arr)) or "-"
        d2 = ", ".join(sorted(arr - cols)) or "-"
        problems.append(f"binary columns vs labels array (col only: {d1}; array only: {d2})")
    if strs != arr:
        d1 = ", ".join(sorted(strs - arr)) or "-"
        d2 = ", ".join(sorted(arr - strs)) or "-"
        problems.append(f"labels_str vs labels array (str only: {d1}; array only: {d2})")

    none_flag = truthy(rec.get("none"))
    if none_flag and arr:
        problems.append("none=1 but labels present")
    if not none_flag and not arr:
        problems.append("none=0 but no labels")

    return arr, problems


def load(input_dir):
    paths = sorted(Path(input_dir).glob("*.jsonl"))
    if not paths:
        raise SystemExit(f"no .jsonl files found in {input_dir}/")

    rows, excluded = [], []
    malformed = 0
    lines_parsed = 0

    for p in paths:
        with open(p, "r", encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, 1):
                line = line.strip()
                if not line:
                    continue
                lines_parsed += 1
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError as e:
                    malformed += 1
                    excluded.append({
                        "review_id": "(unparseable)", "src": p.name,
                        "line": lineno, "problems": [f"bad JSON: {e.msg}"],
                    })
                    continue
                labels, problems = validate(rec)
                entry = {"rec": rec, "labels": labels, "src": p.name,
                         "line": lineno,
                         "review_id": rec.get("review_id", "(no id)")}
                if problems:
                    excluded.append({"review_id": entry["review_id"],
                                     "src": p.name, "line": lineno,
                                     "problems": problems})
                else:
                    rows.append(entry)

    # duplicate handling on the records that passed validation
    by_id = defaultdict(list)
    for e in rows:
        by_id[e["review_id"]].append(e)

    clean, dup_identical, dup_conflict = [], [], []
    for rid, group in by_id.items():
        if len(group) == 1:
            clean.append(group[0])
            continue
        label_sets = {frozenset(g["labels"]) for g in group}
        if len(label_sets) == 1:
            clean.append(group[0])
            dup_identical.append((rid, [f"{g['src']}:{g['line']}" for g in group]))
        else:
            dup_conflict.append((rid, group))
            excluded.append({
                "review_id": rid,
                "src": ", ".join(f"{g['src']}:{g['line']}" for g in group),
                "line": "",
                "problems": ["duplicate review_id with conflicting labels: "
                             + " | ".join(
                                 ", ".join(sorted(g["labels"])) or "(none)"
                                 for g in group)],
            })

    clean.sort(key=lambda e: (e["src"], e["line"]))
    return (paths, clean, excluded, dup_identical, dup_conflict, malformed,
            lines_parsed)


# ──────────────────────────── helpers ────────────────────────────

def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def stratum_of(e):
    s = str(e["rec"].get("stratum", "")).strip().lower()
    return "random" if s.startswith("random") else "targeted"


def wordcount(t):
    return len(re.findall(r"\b[\w']+\b", str(t)))


def year_of(e):
    d = str(e["rec"].get("review_date", ""))
    return d[:4] if len(d) >= 4 and d[:4].isdigit() else "unknown"


def fig(height, name, outdir):
    """Save and close. Called as fig(...) after plotting."""
    plt.tight_layout()
    plt.savefig(outdir / name, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close()


def style():
    plt.rcParams.update({
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linewidth": 0.5,
        "figure.facecolor": "white",
    })


# ──────────────────────────── figures ────────────────────────────

def make_figures(clean, outdir):
    style()
    n = len(clean)
    labels_of = [e["labels"] for e in clean]
    support = Counter()
    for s in labels_of:
        support.update(s)

    # F1 label support, colored by class
    order = [c for c in LABELS]
    order.sort(key=lambda c: (-support.get(c, 0), c))
    vals = [support.get(c, 0) for c in order]
    cols = [CLASS_COLOR[CLASS_OF[c]] for c in order]
    plt.figure(figsize=(FIG_WIDTH, 5.2))
    y = np.arange(len(order))
    plt.barh(y, vals, color=cols, edgecolor="white", linewidth=0.4)
    plt.yticks(y, [pretty(c) for c in order])
    plt.gca().invert_yaxis()
    plt.xlabel("Reviews")
    for i, v in enumerate(vals):
        plt.text(v + max(vals) * 0.01, i, str(v), va="center", fontsize=7)
    handles = [plt.Rectangle((0, 0), 1, 1, color=CLASS_COLOR[k]) for k in CLASSES]
    plt.legend(handles, [CLASS_NAME[k] for k in CLASSES],
               loc="lower right", frameon=False, ncol=1)
    plt.xlim(0, max(vals) * 1.12 if vals and max(vals) else 1)
    fig(5.2, "f01_label_support.png", outdir)

    # F2 class support
    cls_support = Counter()
    for s in labels_of:
        for c in s:
            cls_support[CLASS_OF[c]] += 1
    plt.figure(figsize=(FIG_WIDTH, 2.6))
    xs = np.arange(len(CLASSES))
    v = [cls_support.get(k, 0) for k in CLASSES]
    plt.bar(xs, v, color=[CLASS_COLOR[k] for k in CLASSES],
            edgecolor="white", linewidth=0.6)
    plt.xticks(xs, [CLASS_NAME[k] for k in CLASSES])
    plt.ylabel("Label instances")
    for i, vv in enumerate(v):
        plt.text(i, vv + max(v) * 0.02 if v and max(v) else 0.1, str(vv),
                 ha="center", fontsize=8)
    fig(2.6, "f02_class_support.png", outdir)

    # F3 random-only prevalence vs combined
    rnd = [e for e in clean if stratum_of(e) == "random"]
    n_r = len(rnd)
    sup_r = Counter()
    for e in rnd:
        sup_r.update(e["labels"])
    plt.figure(figsize=(FIG_WIDTH, 5.2))
    y = np.arange(len(order))
    comb_pct = [100 * support.get(c, 0) / n if n else 0 for c in order]
    rnd_pct = [100 * sup_r.get(c, 0) / n_r if n_r else 0 for c in order]
    h = 0.4
    plt.barh(y - h / 2, comb_pct, height=h, color="#9AA5B1",
             label=f"All hand-labeled (n={n})", edgecolor="white", linewidth=0.3)
    plt.barh(y + h / 2, rnd_pct, height=h,
             color=[CLASS_COLOR[CLASS_OF[c]] for c in order],
             label=f"Random stratum only (n={n_r})",
             edgecolor="white", linewidth=0.3)
    plt.yticks(y, [pretty(c) for c in order])
    plt.gca().invert_yaxis()
    plt.xlabel("Percent of reviews")
    plt.legend(loc="lower right", frameon=False)
    fig(5.2, "f03_prevalence_random_vs_all.png", outdir)

    # F4 labels per review
    counts = Counter(min(len(s), 4) for s in labels_of)
    keys = [0, 1, 2, 3, 4]
    lab = ["0", "1", "2", "3", "4+"]
    plt.figure(figsize=(FIG_WIDTH * 0.62, 2.6))
    v = [counts.get(k, 0) for k in keys]
    plt.bar(range(len(keys)), v, color="#2B5FA8", edgecolor="white", linewidth=0.6)
    plt.xticks(range(len(keys)), lab)
    plt.xlabel("Labels per review")
    plt.ylabel("Reviews")
    for i, vv in enumerate(v):
        plt.text(i, vv + max(v) * 0.02 if v and max(v) else 0.1, str(vv),
                 ha="center", fontsize=8)
    fig(2.6, "f04_labels_per_review.png", outdir)

    # F5 class co-occurrence 5x5
    M = np.zeros((len(CLASSES), len(CLASSES)))
    for s in labels_of:
        cs = sorted({CLASS_OF[c] for c in s}, key=CLASSES.index)
        for a in cs:
            M[CLASSES.index(a), CLASSES.index(a)] += 1
        for a, b in combinations(cs, 2):
            M[CLASSES.index(a), CLASSES.index(b)] += 1
            M[CLASSES.index(b), CLASSES.index(a)] += 1
    plt.figure(figsize=(FIG_WIDTH * 0.62, 3.4))
    plt.imshow(M, cmap=HEAT_CMAP)
    plt.xticks(range(len(CLASSES)), [CLASS_NAME[k] for k in CLASSES],
               rotation=35, ha="right")
    plt.yticks(range(len(CLASSES)), [CLASS_NAME[k] for k in CLASSES])
    mx = M.max() if M.size else 1
    for i in range(len(CLASSES)):
        for j in range(len(CLASSES)):
            if M[i, j] > 0:
                plt.text(j, i, int(M[i, j]), ha="center", va="center",
                         fontsize=7,
                         color="white" if M[i, j] > mx * 0.55 else "#1B2E6E")
    plt.grid(False)
    plt.colorbar(shrink=0.8, label="Reviews")
    fig(3.4, "f05_class_cooccurrence.png", outdir)

    # F5b top co-occurring label pairs
    pair = Counter()
    for s in labels_of:
        for a, b in combinations(sorted(s), 2):
            pair[(a, b)] += 1
    top = pair.most_common(TOP_N_PAIRS)
    if top:
        plt.figure(figsize=(FIG_WIDTH, max(2.4, 0.28 * len(top) + 1.0)))
        y = np.arange(len(top))
        v = [c for _, c in top]
        colr = [CLASS_COLOR[CLASS_OF[a]] for (a, b), _ in top]
        plt.barh(y, v, color=colr, edgecolor="white", linewidth=0.4)
        plt.yticks(y, [f"{pretty(a)} + {pretty(b)}" for (a, b), _ in top])
        plt.gca().invert_yaxis()
        plt.xlabel("Reviews carrying both labels")
        for i, vv in enumerate(v):
            plt.text(vv + max(v) * 0.01, i, str(vv), va="center", fontsize=7)
        fig(3.0, "f05b_top_label_pairs.png", outdir)

    # F6 star rating, labeled vs none
    stars = [1, 2, 3, 4, 5]
    lab_c = Counter()
    non_c = Counter()
    for e in clean:
        try:
            s = int(e["rec"].get("star_rating"))
        except (TypeError, ValueError):
            continue
        (lab_c if e["labels"] else non_c)[s] += 1
    plt.figure(figsize=(FIG_WIDTH * 0.62, 2.8))
    w = 0.4
    xs = np.arange(len(stars))
    plt.bar(xs - w / 2, [lab_c.get(s, 0) for s in stars], width=w,
            color="#D55E00", label="At least one label", edgecolor="white", linewidth=0.5)
    plt.bar(xs + w / 2, [non_c.get(s, 0) for s in stars], width=w,
            color="#9AA5B1", label="No label", edgecolor="white", linewidth=0.5)
    plt.xticks(xs, [str(s) for s in stars])
    plt.xlabel("Star rating")
    plt.ylabel("Reviews")
    plt.legend(frameon=False)
    fig(2.8, "f06_star_rating.png", outdir)

    # F7 market distribution
    mk = Counter(str(e["rec"].get("market", "")).upper() for e in clean)
    items = mk.most_common()
    plt.figure(figsize=(FIG_WIDTH * 0.62, 2.8))
    xs = np.arange(len(items))
    v = [c for _, c in items]
    plt.bar(xs, v, color="#009E73", edgecolor="white", linewidth=0.6)
    plt.xticks(xs, [k for k, _ in items], rotation=0)
    plt.ylabel("Reviews")
    plt.xlabel("Market")
    for i, vv in enumerate(v):
        plt.text(i, vv + max(v) * 0.02 if v and max(v) else 0.1, str(vv),
                 ha="center", fontsize=8)
    fig(2.8, "f07_market.png", outdir)

    # F8 review year
    yr = Counter(year_of(e) for e in clean)
    ys = sorted(yr)
    plt.figure(figsize=(FIG_WIDTH * 0.62, 2.6))
    xs = np.arange(len(ys))
    v = [yr[k] for k in ys]
    plt.bar(xs, v, color="#0072B2", edgecolor="white", linewidth=0.6)
    plt.xticks(xs, ys, rotation=0)
    plt.ylabel("Reviews")
    plt.xlabel("Review year")
    fig(2.6, "f08_year.png", outdir)

    # F10 top games
    gm = Counter(str(e["rec"].get("game_name", "")) for e in clean)
    top_g = gm.most_common(TOP_N_GAMES)
    plt.figure(figsize=(FIG_WIDTH, max(2.6, 0.26 * len(top_g) + 1.0)))
    y = np.arange(len(top_g))
    v = [c for _, c in top_g]
    plt.barh(y, v, color="#E69F00", edgecolor="white", linewidth=0.4)
    plt.yticks(y, [g[:42] for g, _ in top_g])
    plt.gca().invert_yaxis()
    plt.xlabel("Hand-labeled reviews")
    for i, vv in enumerate(v):
        plt.text(vv + max(v) * 0.01, i, str(vv), va="center", fontsize=7)
    fig(3.0, "f10_top_games.png", outdir)

    # F11 review length, labeled vs none
    wl = [wordcount(e["rec"].get("review_text")) for e in clean if e["labels"]]
    wn = [wordcount(e["rec"].get("review_text")) for e in clean if not e["labels"]]
    plt.figure(figsize=(FIG_WIDTH * 0.62, 2.8))
    hi = int(np.percentile(wl + wn, 97)) if (wl or wn) else 100
    bins = np.linspace(0, max(hi, 10), 26)
    plt.hist([wl, wn], bins=bins, color=["#D55E00", "#9AA5B1"],
             label=["At least one label", "No label"], edgecolor="white",
             linewidth=0.3)
    plt.xlabel("Review length in words")
    plt.ylabel("Reviews")
    plt.legend(frameon=False)
    fig(2.8, "f11_review_length.png", outdir)

    # F12 class prevalence by market, row normalised
    mkts = [k for k, _ in mk.most_common()]
    if len(mkts) > 1:
        Mm = np.zeros((len(mkts), len(CLASSES)))
        tot = np.zeros(len(mkts))
        for e in clean:
            mi = mkts.index(str(e["rec"].get("market", "")).upper())
            tot[mi] += 1
            for c in {CLASS_OF[x] for x in e["labels"]}:
                Mm[mi, CLASSES.index(c)] += 1
        with np.errstate(invalid="ignore", divide="ignore"):
            Mp = np.where(tot[:, None] > 0, 100 * Mm / tot[:, None], 0)
        plt.figure(figsize=(FIG_WIDTH * 0.72, max(2.4, 0.32 * len(mkts) + 1.4)))
        plt.imshow(Mp, cmap=HEAT_CMAP, aspect="auto")
        plt.xticks(range(len(CLASSES)), [CLASS_NAME[k] for k in CLASSES],
                   rotation=35, ha="right")
        plt.yticks(range(len(mkts)), [f"{m} (n={int(tot[i])})"
                                      for i, m in enumerate(mkts)])
        mx = Mp.max() if Mp.size else 1
        for i in range(len(mkts)):
            for j in range(len(CLASSES)):
                plt.text(j, i, f"{Mp[i, j]:.0f}", ha="center", va="center",
                         fontsize=7,
                         color="white" if Mp[i, j] > mx * 0.55 else "#1B2E6E")
        plt.grid(False)
        plt.colorbar(shrink=0.8, label="Percent of market's reviews")
        fig(3.0, "f12_class_by_market.png", outdir)

    # F13 supplementary, full 29x29 co-occurrence
    idx = {c: i for i, c in enumerate(LABELS)}
    F = np.zeros((len(LABELS), len(LABELS)))
    for s in labels_of:
        ss = sorted(s, key=lambda c: idx[c])
        for a in ss:
            F[idx[a], idx[a]] += 1
        for a, b in combinations(ss, 2):
            F[idx[a], idx[b]] += 1
            F[idx[b], idx[a]] += 1
    plt.figure(figsize=(9.5, 9.0))
    plt.imshow(F, cmap=HEAT_CMAP)
    names = [pretty(c) for c in LABELS]
    plt.xticks(range(len(LABELS)), names, rotation=90, fontsize=6)
    plt.yticks(range(len(LABELS)), names, fontsize=6)
    plt.grid(False)
    plt.colorbar(shrink=0.7, label="Reviews")
    fig(9.0, "f13_supp_full_cooccurrence.png", outdir)


# ──────────────────────────── report ────────────────────────────

def write_report(paths, clean, excluded, dup_identical, dup_conflict,
                 malformed, lines_parsed, outdir):
    n = len(clean)
    L = []
    w = L.append

    def sec(t):
        w("")
        w("=" * 72)
        w(t.upper())
        w("=" * 72)

    def pct(k, d):
        return f"{100 * k / d:.1f}%" if d else "n/a"

    w("CORPUS STATISTICS: hand-labeled dark-pattern review set")
    w(f"Source files: {', '.join(p.name for p in paths)}")

    sec("1. corpus")
    dup_lines_collapsed = sum(len(locs) - 1 for _, locs in dup_identical)
    dup_lines_conflict = sum(len(g) for _, g in dup_conflict)
    excluded_rows = len(excluded) - len(dup_conflict) + dup_lines_conflict
    total = n + dup_lines_collapsed + excluded_rows

    def kv(label, value):
        w(f"  {label:<38}{value:>12}")

    kv("Post-filter review pool", f"{SIZE_OF_POOL:,}")
    kv("Lines read", f"{lines_parsed:,}")
    kv("  redundant copies of repeated ids", dup_lines_collapsed)
    kv("  excluded, see section 10", excluded_rows)
    kv("  unparseable", malformed)
    kv("Hand-labeled reviews", f"{n:,}")
    kv("Sampling fraction of pool", f"{100 * n / SIZE_OF_POOL:.3f}%")
    if total != lines_parsed:
        w(f"  WARNING: outcomes sum to {total}, lines read {lines_parsed}")
    w("")
    kv("Repeated review_ids", len(dup_identical) + len(dup_conflict))
    kv("  copies agreed, one kept", len(dup_identical))
    kv("  copies disagreed, all quarantined", len(dup_conflict))

    w("")
    w("  Stratum")
    for k, v in Counter(stratum_of(e) for e in clean).most_common():
        w(f"    {k:<36}{v:>8}{pct(v, n):>9}")
    w("")
    w("  Source file")
    for k, v in Counter(e["src"] for e in clean).most_common():
        w(f"    {k:<36}{v:>8}{pct(v, n):>9}")

    sec("2. apps and games")
    apps = Counter(e["rec"].get("app_id") for e in clean)
    games = Counter(e["rec"].get("game_name") for e in clean)
    w(f"Unique app ids   : {len(apps)}")
    w(f"Unique game names: {len(games)}")
    if games:
        top5 = sum(c for _, c in games.most_common(5))
        w(f"Share held by top 5 games: {pct(top5, n)}")
        w(f"Games contributing a single review: "
          f"{sum(1 for _, c in games.items() if c == 1)}")
        w("")
        w(f"Top {TOP_N_GAMES} games:")
        for g, c in games.most_common(TOP_N_GAMES):
            w(f"  {str(g)[:44]:<46} {c:>5}  ({pct(c, n)})")

    sec("3. markets, dates, ratings, length")
    w("Market:")
    for k, v in Counter(str(e["rec"].get("market", "")).upper()
                        for e in clean).most_common():
        w(f"  {k:<8} {v:>6}  ({pct(v, n)})")
    dates = sorted(str(e["rec"].get("review_date", "")) for e in clean
                   if e["rec"].get("review_date"))
    if dates:
        w("")
        w(f"Review date range: {dates[0]} to {dates[-1]}")
    w("")
    w("Reviews per year:")
    for k in sorted(Counter(year_of(e) for e in clean)):
        v = Counter(year_of(e) for e in clean)[k]
        w(f"  {k:<8} {v:>6}  ({pct(v, n)})")

    w("")
    w("Star rating, overall and by stratum:")
    w(f"  {'star':<6}{'all':>8}{'random':>10}{'targeted':>10}")
    for s in [1, 2, 3, 4, 5]:
        a = sum(1 for e in clean if str(e["rec"].get("star_rating")) == str(s))
        r = sum(1 for e in clean if str(e["rec"].get("star_rating")) == str(s)
                and stratum_of(e) == "random")
        t = a - r
        w(f"  {s:<6}{a:>8}{r:>10}{t:>10}")
    rat = [int(e["rec"]["star_rating"]) for e in clean
           if str(e["rec"].get("star_rating", "")).strip().isdigit()]
    if rat:
        w(f"  mean star rating: {np.mean(rat):.2f}   median: {np.median(rat):.0f}")

    wl = [wordcount(e["rec"].get("review_text")) for e in clean if e["labels"]]
    wn = [wordcount(e["rec"].get("review_text")) for e in clean if not e["labels"]]
    w("")
    w("Review length in words:")
    for nm, arr in (("all", wl + wn), ("labeled", wl), ("no label", wn)):
        if arr:
            w(f"  {nm:<10} mean {np.mean(arr):6.1f}   median {np.median(arr):5.0f}"
              f"   p25 {np.percentile(arr, 25):5.0f}   p75 {np.percentile(arr, 75):5.0f}"
              f"   max {max(arr):5.0f}")

    sec("4. label distribution")
    support = Counter()
    for e in clean:
        support.update(e["labels"])
    total_inst = sum(support.values())
    w(f"Total label instances: {total_inst}")
    w(f"Reviews with at least one label: {sum(1 for e in clean if e['labels'])}"
      f"  ({pct(sum(1 for e in clean if e['labels']), n)})")
    w(f"Reviews with no label: {sum(1 for e in clean if not e['labels'])}"
      f"  ({pct(sum(1 for e in clean if not e['labels']), n)})")
    w("")
    w(f"  {'label':<34}{'n':>6}{'% of reviews':>14}{'% of instances':>16}")
    for c in sorted(LABELS, key=lambda c: (-support.get(c, 0), c)):
        k = support.get(c, 0)
        w(f"  {c:<34}{k:>6}{pct(k, n):>14}{pct(k, total_inst):>16}")

    zero = [c for c in LABELS if support.get(c, 0) == 0]
    low = [c for c in LABELS if 0 < support.get(c, 0) < 3]
    w("")
    w(f"Zero support ({len(zero)}): {', '.join(zero) if zero else 'none'}")
    w(f"Support below 3 ({len(low)}): {', '.join(low) if low else 'none'}")

    w("")
    w("By class:")
    cls = Counter()
    cls_rev = Counter()
    for e in clean:
        for c in e["labels"]:
            cls[CLASS_OF[c]] += 1
        for c in {CLASS_OF[x] for x in e["labels"]}:
            cls_rev[c] += 1
    for k in CLASSES:
        w(f"  {CLASS_NAME[k]:<16} instances {cls.get(k, 0):>5}   "
          f"reviews {cls_rev.get(k, 0):>5}  ({pct(cls_rev.get(k, 0), n)})")

    sec("5. prevalence in the random stratum only")
    rnd = [e for e in clean if stratum_of(e) == "random"]
    nr = len(rnd)
    w(f"Random stratum size: {nr}")
    if nr:
        sr = Counter()
        for e in rnd:
            sr.update(e["labels"])
        none_r = sum(1 for e in rnd if not e["labels"])
        lo, hi = wilson(nr - none_r, nr)
        w(f"Reviews with at least one label: {nr - none_r} ({pct(nr - none_r, nr)}), "
          f"95% CI [{100*lo:.1f}%, {100*hi:.1f}%]")
        w("")
        w(f"  {'label':<34}{'n':>6}{'prev':>9}{'95% CI':>20}")
        for c in sorted(LABELS, key=lambda c: (-sr.get(c, 0), c)):
            k = sr.get(c, 0)
            lo, hi = wilson(k, nr)
            w(f"  {c:<34}{k:>6}{pct(k, nr):>9}"
              f"{'[' + f'{100*lo:.1f}, {100*hi:.1f}' + ']':>20}")

    sec("6. labels per review")
    per = [len(e["labels"]) for e in clean]
    if per:
        w(f"Mean {np.mean(per):.2f}   median {np.median(per):.0f}   max {max(per)}")
        lp = [x for x in per if x > 0]
        if lp:
            w(f"Mean among labeled reviews only: {np.mean(lp):.2f}")
        w(f"Multi-label reviews (2 or more): {sum(1 for x in per if x >= 2)}"
          f"  ({pct(sum(1 for x in per if x >= 2), n)})")
        w("")
        dist = Counter(per)
        for k in sorted(dist):
            w(f"  {k} label(s): {dist[k]:>5}  ({pct(dist[k], n)})")

    sec("7. co-occurrence")
    pair = Counter()
    for e in clean:
        for a, b in combinations(sorted(e["labels"]), 2):
            pair[(a, b)] += 1
    w(f"Distinct co-occurring pairs observed: {len(pair)}")
    w("")
    w(f"Top {TOP_N_PAIRS} pairs by count, with lift:")
    w(f"  {'pair':<62}{'n':>5}{'lift':>8}")
    for (a, b), c in pair.most_common(TOP_N_PAIRS):
        exp = support[a] * support[b] / n if n else 0
        lift = c / exp if exp else float("inf")
        w(f"  {a + ' + ' + b:<62}{c:>5}{lift:>8.1f}")

    sec("8. seed keywords")
    kw_tot, kw_hit = Counter(), Counter()
    for e in clean:
        if stratum_of(e) != "targeted":
            continue
        k = str(e["rec"].get("seed_keyword", "")).strip().lower()
        if not k:
            k = "(no keyword)"
        kw_tot[k] += 1
        if e["labels"]:
            kw_hit[k] += 1
    real = [k for k in kw_tot if k != "(no keyword)"]
    productive = sorted(k for k in real if kw_hit[k] > 0)
    dead = sorted(k for k in real if kw_hit[k] == 0)

    def wrap(items, indent="    "):
        if not items:
            w(indent + "none")
            return
        buf = indent
        for i, k in enumerate(items):
            piece = k + ("," if i < len(items) - 1 else "")
            if len(buf) + len(piece) + 1 > 76:
                w(buf.rstrip())
                buf = indent
            buf += piece + " "
        w(buf.rstrip())

    w(f"  {'Targeted reviews':<38}{sum(kw_tot.values()):>12}")
    w(f"  {'Distinct seed keywords':<38}{len(real):>12}")
    w("")
    w(f"  Produced at least one label ({len(productive)})")
    wrap(productive)
    w("")
    w(f"  Produced no label ({len(dead)})")
    wrap(dead)

    sr = Counter()
    for e in rnd:
        sr.update(e["labels"])
    only_t = [c for c in LABELS
              if support.get(c, 0) > 0 and sr.get(c, 0) == 0]
    w("")
    w(f"  Labels with support only in the targeted stratum ({len(only_t)})")
    wrap(only_t)

    sec("9. star rating against labeling")
    w(f"  {'star':<6}{'labeled':>10}{'no label':>11}{'labeled %':>12}")
    for s in [1, 2, 3, 4, 5]:
        a = [e for e in clean if str(e["rec"].get("star_rating")) == str(s)]
        lb = sum(1 for e in a if e["labels"])
        w(f"  {s:<6}{lb:>10}{len(a) - lb:>11}{pct(lb, len(a)):>12}")

    sec("10. excluded records")
    w(f"Total excluded: {len(excluded)}")
    if not excluded:
        w("None. Every record passed validation.")
    else:
        reason_count = Counter()
        for x in excluded:
            for p in x["problems"]:
                reason_count[p.split("(")[0].split(":")[0].strip()] += 1
        w("")
        w("By reason:")
        for r, c in reason_count.most_common():
            w(f"  {c:>5}  {r}")
        w("")
        w("Detail:")
        for x in excluded:
            loc = f"{x['src']}:{x['line']}" if x["line"] != "" else x["src"]
            w(f"  {x['review_id']}   [{loc}]")
            for p in x["problems"]:
                w(f"      - {p}")

    if dup_identical:
        w("")
        w(f"Identical duplicate review_ids collapsed to one ({len(dup_identical)}), "
          "no action needed:")
        for rid, locs in dup_identical:
            w(f"  {rid}   {' , '.join(locs)}")

    (outdir / "corpus_stats.txt").write_text("\n".join(L), encoding="utf-8")


def main():
    outdir = Path(OUTPUT_DIR)
    figdir = outdir / "figures"
    figdir.mkdir(parents=True, exist_ok=True)

    (paths, clean, excluded, dup_id, dup_cf, malformed,
     lines_parsed) = load(INPUT_DIR)
    if not clean:
        raise SystemExit("no clean records survived validation, see the report")

    make_figures(clean, figdir)
    write_report(paths, clean, excluded, dup_id, dup_cf, malformed,
                 lines_parsed, outdir)

    print(f"clean reviews : {len(clean)}")
    print(f"excluded      : {len(excluded)}")
    print(f"report        : {outdir / 'corpus_stats.txt'}")
    print(f"figures       : {figdir}/  ({len(list(figdir.glob('*.png')))} png)")


if __name__ == "__main__":
    main()