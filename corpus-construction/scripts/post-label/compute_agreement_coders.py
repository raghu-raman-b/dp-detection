#!/usr/bin/env python3
"""
compute_agreement_coders.py — inter-coder agreement AMONG THE CODERS ONLY.

This is compute_agreement.py with the author dropped from the rater pool.
The author file is still read, but only for the universe of review_ids and
their metadata (game_name, market, codebook_version); the author's own
`actual_labels` never enter the ballots. Every metric here is IAA computed
over the *.jsonl coder exports in CODERS_DIR and nothing else.

Edit the CONFIG block, then:  python3 compute_agreement_coders.py

Unit of analysis is one review; the value a coder contributes is the SET of
meso labels they assigned. NONE is the empty set, not a code.

Three states are distinguished and only the first is a ballot:
    coded     row present, saved == 1                -> counts
    abstain   row present, saved == 0                -> excluded
    absent    review_id not in that coder's file     -> excluded
An abstention is not a vote for NONE. Collapsing the two would dilute every
majority and inflate agreement on exactly the rows nobody finished.

Krippendorff's alpha is computed for an arbitrary distance function as

    Do = (1/n)      * SUM_u [ SUM_{i!=j} d(c_ui, c_uj) / (m_u - 1) ]
    De = (1/n(n-1)) * SUM over ordered pairs of the pooled values of d
    alpha = 1 - Do/De

with n = SUM_u m_u over units having m_u >= 2 raters.
"""

from __future__ import annotations

import json
import random
import re
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

# ═══════════════════════════════ CONFIG ═══════════════════════════════

CODERS_DIR = "../../coders"                 # every *.jsonl here is a coder
AUTHOR_FILE = "../../validation/validation_set.jsonl"   # review_id universe + metadata only
CODEBOOK = "../../../codebook_versions/codebook_v0.20.json"

OUT_DIR = "../../outputs/agreement"
REPORT = "agreement_report_coders.txt"
METRICS_JSON = "agreement_coders.json"      # None to skip

AUTHOR_ID = "author"
INCLUDE_AUTHOR = False       # author is excluded from IAA; file used only for the review universe

BOOTSTRAP_N = 2000           # resamples for the alpha CI; 0 to skip
BOOTSTRAP_CI = 0.95
SEED = 20260831

MIN_SUPPORT = 3              # per-label metrics below this are starred, not suppressed
TOP_CONTESTED = 15           # most-disagreed reviews to list

# ══════════════════════════════════════════════════════════════════════

SCRIPT_DIR = Path(__file__).resolve().parent

CLASS_PREFIX = {
    "Temporal": "T", "Monetary": "M", "Social": "S",
    "Psychological": "P", "Technical": "Tech",
}
CLASS_NAME = {v: k for k, v in CLASS_PREFIX.items()}


def rel(p: str) -> Path:
    return (SCRIPT_DIR / p).resolve()


def label_key(high_level: str, meso_label: str) -> str:
    """'Social' + 'Fear of Missing Out (FOMO)' -> 'S_FearOfMissingOutFOMO'."""
    words = re.split(r"[^0-9A-Za-z]+", meso_label)
    camel = "".join(w[:1].upper() + w[1:] for w in words if w)
    return f"{CLASS_PREFIX[high_level]}_{camel}"


def load_codebook(path: Path) -> list[str]:
    """The full codebook vocabulary, in codebook order."""
    labels = json.loads(path.read_text(encoding="utf-8"))["labels"]
    out = []
    for lab in labels:
        hl = lab.get("high_level")
        meso = lab.get("meso_label")
        if hl and meso:
            out.append(label_key(hl, meso))
    return out


def jsonl(path: Path):
    with open(path, encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            s = line.strip()
            if not s:
                continue
            try:
                yield json.loads(s)
            except json.JSONDecodeError:
                print(f"  ! {path.name}:{i} unparseable, skipped", file=sys.stderr)


# ─────────────────────────── distances ────────────────────────────────

def jaccard(a: frozenset, b: frozenset) -> float:
    if not a and not b:
        return 1.0
    u = len(a | b)
    return len(a & b) / u if u else 1.0


def masi_sim(a: frozenset, b: frozenset) -> float:
    """Passonneau's MASI: Jaccard scaled by a monotonicity term."""
    if not a and not b:
        return 1.0
    inter = len(a & b)
    if inter == len(a) and inter == len(b):
        m = 1.0
    elif inter == len(a) or inter == len(b):
        m = 2 / 3          # one set contains the other
    elif inter > 0:
        m = 1 / 3          # they intersect
    else:
        m = 0.0            # disjoint
    return jaccard(a, b) * m


def d_masi(a, b):
    return 1.0 - masi_sim(a, b)


def d_jaccard(a, b):
    return 1.0 - jaccard(a, b)


def d_nominal(a, b):
    return 0.0 if a == b else 1.0


# ──────────────────────── Krippendorff's alpha ────────────────────────

class Alpha:
    """Alpha over set-valued units, with the pieces cached so a bootstrap
    over units is cheap: per-unit disagreement never changes, and the
    expected term is a quadratic form over counts of distinct values."""

    def __init__(self, units: list[list], dist):
        self.units = [u for u in units if len(u) >= 2]
        self.dist = dist
        vals = sorted({v for u in self.units for v in u}, key=lambda s: (len(s), sorted(s)))
        self.index = {v: i for i, v in enumerate(vals)}
        k = len(vals)
        self.D = [[0.0] * k for _ in range(k)]
        for i in range(k):
            for j in range(i + 1, k):
                d = dist(vals[i], vals[j])
                self.D[i][j] = self.D[j][i] = d
        # per unit: the observed term, and the count vector of its values
        self.unit_do = []
        self.unit_counts = []
        self.unit_m = []
        for u in self.units:
            ids = [self.index[v] for v in u]
            m = len(ids)
            s = 0.0
            for a in range(m):
                for b in range(m):
                    if a != b:
                        s += self.D[ids[a]][ids[b]]
            self.unit_do.append(s / (m - 1))
            c = Counter(ids)
            self.unit_counts.append(c)
            self.unit_m.append(m)

    def _alpha(self, idxs):
        if not idxs:
            return None
        n = sum(self.unit_m[i] for i in idxs)
        if n < 2:
            return None
        do = sum(self.unit_do[i] for i in idxs) / n
        pool = Counter()
        for i in idxs:
            pool.update(self.unit_counts[i])
        de = 0.0
        items = list(pool.items())
        for a, (ia, ca) in enumerate(items):
            for ib, cb in items[a + 1:]:
                de += 2.0 * ca * cb * self.D[ia][ib]
        de /= n * (n - 1)
        if de == 0:
            return 1.0 if do == 0 else None
        return 1.0 - do / de

    def value(self):
        return self._alpha(list(range(len(self.units))))

    def bootstrap(self, n_resamples, ci, rng):
        if not self.units or n_resamples <= 0:
            return None, None
        N = len(self.units)
        out = []
        for _ in range(n_resamples):
            a = self._alpha([rng.randrange(N) for _ in range(N)])
            if a is not None:
                out.append(a)
        if not out:
            return None, None
        out.sort()
        lo = out[int((1 - ci) / 2 * len(out))]
        hi = out[min(len(out) - 1, int((1 + ci) / 2 * len(out)))]
        return lo, hi


def alpha_of(units, dist):
    a = Alpha(units, dist)
    return a.value(), a


# ─────────────────────────── loading ──────────────────────────────────

def coder_labels(o: dict, legal: list[str]):
    """dp_coder's own tolerance: labels, else assigned_labels, else the
    29 binary columns. Booleans arrive as 0/1 or as true/false."""
    if isinstance(o.get("labels"), list):
        labs = o["labels"]
    elif isinstance(o.get("assigned_labels"), list):
        labs = o["assigned_labels"]
    else:
        labs = [c for c in legal if o.get(c) in (1, "1", True)]
    known = [c for c in labs if c in legal]
    unknown = [c for c in labs if c and c not in legal]
    return known, unknown


def is_saved(o: dict) -> bool:
    return o.get("saved") in (1, "1", True)


def load_coders(folder: Path, legal: list[str], known_ids: set[str]):
    """-> ordered [(coder_id, {review_id: frozenset}), ...], plus per-coder notes.

    Ballots are restricted to review_ids that exist in the author file. A
    coder file carrying ids from somewhere else must not silently inflate
    that coder's coverage."""
    files = sorted(p for p in folder.glob("*.jsonl"))
    coders, notes = [], {}
    for p in files:
        rows = list(jsonl(p))
        if not rows:
            continue
        names = Counter(str(r.get("coder_name", "")).strip()
                        for r in rows if str(r.get("coder_name", "")).strip())
        base = names.most_common(1)[0][0] if names else re.sub(
            r"^coder[_-]|[_-]\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}$", "", p.stem)
        cid, n = base, 2
        while any(cid == c for c, _ in coders) or cid == AUTHOR_ID:
            cid, n = f"{base}#{n}", n + 1

        ballots, abstain, foreign, unknown = {}, 0, 0, Counter()
        for r in rows:
            rid = str(r.get("review_id", ""))
            if not rid:
                continue
            if rid not in known_ids:
                foreign += 1
                continue
            if not is_saved(r):
                abstain += 1
                continue
            known, unk = coder_labels(r, legal)
            unknown.update(unk)
            ballots[rid] = frozenset(known)
        coders.append((cid, ballots))
        notes[cid] = {
            "file": p.name, "rows": len(rows), "coded": len(ballots),
            "abstain": abstain, "foreign": foreign, "unknown_codes": dict(unknown),
            "renamed_from": base if cid != base else None,
            "name_variants": [k for k, _ in names.most_common()[1:]],
        }
    return coders, notes


def load_author(path: Path, legal: list[str]):
    """Only `order` and `meta` are consumed downstream; ballots/unknown are
    returned for parity with compute_agreement.py but never enter the pool."""
    ballots, order, meta, unknown = {}, [], {}, Counter()
    for o in jsonl(path):
        rid = str(o.get("review_id", ""))
        if not rid:
            continue
        labs = o.get("actual_labels")
        if labs is None:
            labs = [s.strip() for s in str(o.get("actual_labels_str", "")).split(";")]
        known = [c for c in labs if c in legal]
        unknown.update(c for c in labs if c and c not in legal)
        if rid in ballots:
            continue
        ballots[rid] = frozenset(known)
        order.append(rid)
        meta[rid] = {"game_name": o.get("game_name", ""), "market": o.get("market", ""),
                     "codebook_version": o.get("codebook_version", "")}
    return ballots, order, meta, dict(unknown)


# ─────────────────────────── formatting ───────────────────────────────

def bar(ch="=", n=92):
    return ch * n


def head(title, ch="="):
    return f"{bar(ch)}\n{title}\n{bar(ch)}"


def f3(x):
    return "n/a" if x is None else f"{x:.3f}"


def table(rows, headers, aligns=None):
    if not rows:
        return "  (none)"
    cols = len(headers)
    w = [len(str(h)) for h in headers]
    for r in rows:
        for i in range(cols):
            w[i] = max(w[i], len(str(r[i])))
    aligns = aligns or ["<"] + [">"] * (cols - 1)
    out = ["  " + "  ".join(f"{headers[i]:{aligns[i]}{w[i]}}" for i in range(cols))]
    for r in rows:
        out.append("  " + "  ".join(f"{str(r[i]):{aligns[i]}{w[i]}}" for i in range(cols)))
    return "\n".join(out)


def interpret(a):
    if a is None:
        return "undefined"
    if a >= 0.800:
        return "firm (Krippendorff >= .800)"
    if a >= 0.667:
        return "tentative (>= .667)"
    if a >= 0.600:
        return "below tentative; defensible for a 29-label multi-label construct only with documented adjudication"
    return "below .600"


# ─────────────────────────────── main ─────────────────────────────────

def main() -> int:
    rng = random.Random(SEED)
    cod_dir, auth_path = rel(CODERS_DIR), rel(AUTHOR_FILE)
    if not auth_path.exists():
        print(f"ERROR: author file not found: {auth_path}", file=sys.stderr)
        return 1
    if not cod_dir.is_dir():
        print(f"ERROR: coders folder not found: {cod_dir}", file=sys.stderr)
        return 1

    legal = load_codebook(rel(CODEBOOK))
    if not legal:
        print("ERROR: no labels parsed from the codebook", file=sys.stderr)
        return 1

    author_b, order, meta, author_unknown = load_author(auth_path, legal)
    coders, notes = load_coders(cod_dir, legal, set(order))
    if not coders:
        print(f"ERROR: no *.jsonl coder files in {cod_dir}", file=sys.stderr)
        return 1

    raters = ([(AUTHOR_ID, author_b)] if INCLUDE_AUTHOR else []) + coders
    rater_ids = [c for c, _ in raters]
    if len(raters) < 2:
        print(f"ERROR: need >=2 coders for IAA, found {len(raters)}", file=sys.stderr)
        return 1

    # ballots per unit, in author file order
    units, unit_ids = [], []
    for rid in order:
        b = [(c, m[rid]) for c, m in raters if rid in m]
        units.append(b)
        unit_ids.append(rid)
    pairable = [i for i, u in enumerate(units) if len(u) >= 2]

    L = [
        head("INTER-CODER AGREEMENT  (CODERS ONLY, author excluded)"),
        f"generated={__import__('datetime').datetime.now().isoformat(timespec='seconds')}",
        f"author_file={AUTHOR_FILE}  (review universe + metadata only)",
        f"coders_dir={CODERS_DIR}",
        f"codebook={CODEBOOK}  labels={len(legal)}",
        f"units={len(order)}  pairable_units={len(pairable)}  raters={len(raters)}"
        f"  include_author={INCLUDE_AUTHOR}",
        f"BOOTSTRAP_N={BOOTSTRAP_N} CI={BOOTSTRAP_CI} SEED={SEED} MIN_SUPPORT={MIN_SUPPORT}",
        "",
        head("RATERS", "-"),
    ]

    rrows = []
    for cid, b in raters:
        nt = notes.get(cid)
        cov = len(b)
        nl = sum(len(s) for s in b.values())
        none_n = sum(1 for s in b.values() if not s)
        rrows.append([
            cid,
            nt["file"] if nt else Path(AUTHOR_FILE).name,
            cov, len(order) - cov,
            nt["abstain"] if nt else 0,
            nl, f"{nl / cov:.2f}" if cov else "n/a",
            none_n, f"{none_n / cov:.3f}" if cov else "n/a",
        ])
    L += [table(rrows, ["rater", "file", "coded", "absent", "abstain",
                        "labels", "lab/rev", "NONE", "NONE rate"]), ""]

    warn = []
    for cid, nt in notes.items():
        if nt["renamed_from"]:
            warn.append(f"{cid}: duplicate coder_name, renamed from {nt['renamed_from']}")
        if nt["name_variants"]:
            warn.append(f"{cid}: coder_name varies in-file, also saw {', '.join(nt['name_variants'])}")
        if nt["unknown_codes"]:
            warn.append(f"{cid}: codes not in the codebook: "
                        + ", ".join(f"{k} x{v}" for k, v in nt["unknown_codes"].items()))
        if nt["abstain"]:
            warn.append(f"{cid}: {nt['abstain']} row(s) exported unsaved, excluded as abstentions")
        if nt["foreign"]:
            warn.append(f"{cid}: {nt['foreign']} review_id(s) not in the author file, excluded")
        gap = len(order) - nt["coded"] - nt["abstain"]
        if gap > 0:
            warn.append(f"{cid}: {gap} review(s) of {len(order)} missing from the file entirely")
    missing = [unit_ids[i] for i, u in enumerate(units) if len(u) < 2]
    if missing:
        warn.append(f"{len(missing)} unit(s) with <2 ballots, excluded from alpha")
    if warn:
        L += [head("DATA NOTES", "-")] + [f"  {w}" for w in warn] + [""]

    # ── overall alpha ─────────────────────────────────────────────────
    vals = [[s for _, s in u] for u in units]
    a_masi, A = alpha_of(vals, d_masi)
    a_jac, _ = alpha_of(vals, d_jaccard)
    a_exact, _ = alpha_of(vals, d_nominal)
    lo, hi = A.bootstrap(BOOTSTRAP_N, BOOTSTRAP_CI, rng)

    n_ballots = sum(len(u) for u in units if len(u) >= 2)
    L += [
        head("KRIPPENDORFF'S ALPHA"),
        table([
            ["MASI (set-valued, primary)", f3(a_masi),
             f"[{f3(lo)}, {f3(hi)}]" if lo is not None else "n/a", interpret(a_masi)],
            ["Jaccard (set-valued)", f3(a_jac), "", ""],
            ["nominal (exact set match)", f3(a_exact), "", ""],
        ], ["distance", "alpha", f"{int(BOOTSTRAP_CI*100)}% CI", "reading"],
            ["<", ">", ">", "<"]),
        "",
        f"  units={len(A.units)}  ballots={n_ballots}  distinct_value_sets={len(A.index)}",
        "",
        head("PER-CLASS ALPHA (MASI, label set restricted to the class)", "-"),
    ]

    crows = []
    for pre in ["T", "M", "S", "P", "Tech"]:
        sub = [[frozenset(x for x in s if x.startswith(pre + "_")) for _, s in u] for u in units]
        a, _ = alpha_of(sub, d_masi)
        sup = sum(1 for u in units for _, s in u if any(x.startswith(pre + "_") for x in s))
        crows.append([f"{pre}  {CLASS_NAME[pre]}", f3(a), sup])
    L += [table(crows, ["class", "alpha", "positive ballots"]), ""]

    # ── pairwise ──────────────────────────────────────────────────────
    L += [head("PAIRWISE (units both raters coded)", "-")]
    prows = []
    for (c1, b1), (c2, b2) in combinations(raters, 2):
        both = [rid for rid in order if rid in b1 and rid in b2]
        if not both:
            prows.append([f"{c1} / {c2}", 0, "n/a", "n/a", "n/a", "n/a"])
            continue
        ex = sum(1 for r in both if b1[r] == b2[r]) / len(both)
        jc = sum(jaccard(b1[r], b2[r]) for r in both) / len(both)
        ms = sum(masi_sim(b1[r], b2[r]) for r in both) / len(both)
        a, _ = alpha_of([[b1[r], b2[r]] for r in both], d_masi)
        prows.append([f"{c1} / {c2}", len(both), f"{ex:.3f}", f"{jc:.3f}", f"{ms:.3f}", f3(a)])
    L += [table(prows, ["pair", "n", "exact", "Jaccard", "MASI", "alpha(MASI)"]), ""]

    # ── observed agreement summary ────────────────────────────────────
    unan = sum(1 for u in units if len(u) >= 2 and len({s for _, s in u}) == 1)
    pair_ex, pair_ms, pair_jc, npair = 0, 0.0, 0.0, 0
    for u in units:
        for (_, s1), (_, s2) in combinations(u, 2):
            npair += 1
            pair_ex += 1 if s1 == s2 else 0
            pair_ms += masi_sim(s1, s2)
            pair_jc += jaccard(s1, s2)
    L += [
        head("OBSERVED AGREEMENT", "-"),
        table([
            ["unanimous units (all raters identical)", unan,
             f"{unan/len(pairable):.3f}" if pairable else "n/a"],
            ["rater pairs compared", npair, ""],
            ["pairwise exact set match", pair_ex,
             f"{pair_ex/npair:.3f}" if npair else "n/a"],
            ["mean pairwise MASI similarity", "",
             f"{pair_ms/npair:.3f}" if npair else "n/a"],
            ["mean pairwise Jaccard similarity", "",
             f"{pair_jc/npair:.3f}" if npair else "n/a"],
        ], ["measure", "n", "rate"]),
        "",
    ]

    # ── per label ─────────────────────────────────────────────────────
    L += [head("PER-LABEL AGREEMENT  (binary presence, one column per rater)")]
    lrows = []
    for col in legal:
        bin_units, kk, mm = [], [], []
        for u in units:
            v = [(1 if col in s else 0) for _, s in u]
            bin_units.append([frozenset([x]) for x in v])
            kk.append(sum(v))
            mm.append(len(v))
        a, _ = alpha_of(bin_units, d_nominal)
        # Fleiss' kappa, variable raters per unit
        idx = [i for i in range(len(units)) if mm[i] >= 2]
        if idx:
            pbar = sum((kk[i] * (kk[i] - 1) + (mm[i] - kk[i]) * (mm[i] - kk[i] - 1))
                       / (mm[i] * (mm[i] - 1)) for i in idx) / len(idx)
            p = sum(kk[i] for i in idx) / sum(mm[i] for i in idx)
            pe = p * p + (1 - p) * (1 - p)
            kap = (pbar - pe) / (1 - pe) if pe < 1 else None
        else:
            kap = None
        support = sum(1 for i in idx if kk[i] > 0)          # units any rater assigned it
        full = sum(1 for i in idx if kk[i] == mm[i])        # units every rater assigned it
        star = "*" if support < MIN_SUPPORT else " "
        lrows.append([col + star, support, full, sum(kk), f3(a), f3(kap)])
    L += [table(lrows, ["label", "units", "unanim", "assigns", "alpha", "Fleiss k"]),
          f"  (* support < MIN_SUPPORT={MIN_SUPPORT}; alpha/kappa on a handful of units is noise, not a measurement)",
          ""]

    # ── prevalence per rater ──────────────────────────────────────────
    L += [head("LABEL PREVALENCE BY RATER  (assignments, over units that rater coded)", "-")]
    prow = []
    for col in legal:
        cells = []
        for cid, b in raters:
            cells.append(sum(1 for s in b.values() if col in s))
        prow.append([col] + cells + [sum(cells)])
    L += [table(prow, ["label"] + rater_ids + ["total"]), ""]

    # ── most contested units ──────────────────────────────────────────
    L += [head(f"MOST CONTESTED REVIEWS (top {TOP_CONTESTED} by mean pairwise MASI distance)", "-")]
    scored = []
    for i, u in enumerate(units):
        if len(u) < 2:
            continue
        ps = list(combinations(u, 2))
        d = sum(1 - masi_sim(s1, s2) for (_, s1), (_, s2) in ps) / len(ps)
        allc = sorted({x for _, s in u for x in s}, key=lambda c: legal.index(c) if c in legal else 999)
        scored.append([unit_ids[i], meta[unit_ids[i]]["game_name"][:24], len(u), f"{d:.3f}",
                       ", ".join(allc) if allc else "(all NONE)"])
    scored.sort(key=lambda r: -float(r[3]))
    L += [table(scored[:TOP_CONTESTED],
                ["review_id", "game", "n", "MASI dist", "union of assigned labels"],
                ["<", "<", ">", ">", "<"]), ""]

    # ── NONE ──────────────────────────────────────────────────────────
    none_all = sum(1 for u in units if len(u) >= 2 and all(not s for _, s in u))
    none_any = sum(1 for u in units if len(u) >= 2 and any(not s for _, s in u))
    L += [
        head("NONE (the empty label set)", "-"),
        table([
            ["units where every rater said NONE", none_all],
            ["units where at least one rater said NONE", none_any],
            ["units where raters split on NONE", none_any - none_all],
        ], ["measure", "n"]),
        "",
        bar(),
    ]

    out_dir = rel(OUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    report = "\n".join(L) + "\n"
    (out_dir / REPORT).write_text(report, encoding="utf-8")

    if METRICS_JSON:
        (out_dir / METRICS_JSON).write_text(json.dumps({
            "generated": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
            "author_file": AUTHOR_FILE, "coders_dir": CODERS_DIR,
            "include_author": INCLUDE_AUTHOR,
            "raters": rater_ids, "n_units": len(order), "n_pairable": len(pairable),
            "alpha_masi": a_masi, "alpha_masi_ci": [lo, hi],
            "alpha_jaccard": a_jac, "alpha_nominal": a_exact,
            "bootstrap_n": BOOTSTRAP_N, "ci": BOOTSTRAP_CI, "seed": SEED,
            "per_class_alpha": {r[0].split()[0]: (None if r[1] == "n/a" else float(r[1]))
                                for r in crows},
            "per_label": {r[0].rstrip("*"): {
                "units": r[1], "unanimous": r[2], "assignments": r[3],
                "alpha": None if r[4] == "n/a" else float(r[4]),
                "fleiss_kappa": None if r[5] == "n/a" else float(r[5])} for r in lrows},
            "observed": {
                "unanimous_units": unan, "rater_pairs": npair,
                "pairwise_exact": pair_ex,
                "mean_pairwise_masi": pair_ms / npair if npair else None,
                "mean_pairwise_jaccard": pair_jc / npair if npair else None},
            "notes": notes,
        }, indent=2), encoding="utf-8")

    print(report)
    print(f"wrote {out_dir / REPORT}"
          + (f" and {out_dir / METRICS_JSON}" if METRICS_JSON else ""), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
