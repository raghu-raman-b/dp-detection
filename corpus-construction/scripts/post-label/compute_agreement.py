#!/usr/bin/env python3
"""
compute_agreement.py — multi-angle agreement over the validation set.

    python3 compute_agreement.py                 # all discovered raters
    python3 compute_agreement.py --list-llms     # what LLM runs are available
    python3 compute_agreement.py --llm gpt-5.6-luna_xhigh_teacher_v2_full
    python3 compute_agreement.py --only AUTHOR,HUMAN-A,HUMAN-B,HUMAN-C

Four kinds of rater are pooled onto one ballot sheet, one row per review:

    AUTHOR    the author's own independent labels        (validation_set.jsonl)
    GOLD      the adjudicated panel consensus            (gold_set.jsonl)
    HUMAN-*   the trained coders' dp_coder.html exports  (coders/*.jsonl)
    LLM-*     one model x reasoning effort x prompt      (validation/runs/**)

GOLD is *not* independent of the humans: it was adjudicated from their ballots
and the author's. It is carried through every table because it is the reference
the LLM runs were scored against, but it is excluded from the headline panel and
flagged everywhere it appears. Alpha over a panel containing GOLD is a measure of
distance-to-consensus, not of inter-rater reliability, and must not be reported
as the latter.

Unit of analysis is one review; the value a rater contributes is the SET of meso
labels they assigned. NONE is the empty set, not a code.

Three states are distinguished and only the first is a ballot:
    coded     row present and finished (saved==1 / parsed cleanly)  -> counts
    abstain   row present but unfinished (saved==0 / parse failure) -> excluded
    absent    review_id not in that rater's file                    -> excluded
An abstention is not a vote for NONE. Collapsing the two would dilute every
majority and inflate agreement on exactly the rows nobody finished.

Krippendorff's alpha is computed for an arbitrary distance function as

    Do = (1/n)      * SUM_u [ SUM_{i!=j} d(c_ui, c_uj) / (m_u - 1) ]
    De = (1/n(n-1)) * SUM over ordered pairs of the pooled values of d
    alpha = 1 - Do/De

with n = SUM_u m_u over units having m_u >= 2 raters.
"""

from __future__ import annotations

import argparse
import datetime
import fnmatch
import json
import random
import re
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

try:
    import numpy as _np
except ImportError:
    _np = None

# ═══════════════════════════════ CONFIG ═══════════════════════════════

CODERS_DIR = "../../coders"                  # every *.jsonl here is a human coder
AUTHOR_FILE = "../../validation/validation_set.jsonl"
GOLD_FILE = "../../gold_set/gold_set.jsonl"  # adjudicated consensus; None to skip
LLM_RUNS_DIR = "../../outputs/validation/runs"
CODEBOOK = "../../../codebook_versions/codebook_v0.20.json"

OUT_DIR = "../../outputs/agreement"
REPORT = "agreement_report.txt"
METRICS_JSON = "agreement.json"              # None to skip

INCLUDE_AUTHOR = True
INCLUDE_GOLD = True

# Which discovered LLM runs to admit. "all", or a list of run tags / fnmatch
# globs, e.g. ["gpt-5.6-luna_xhigh_*", "claude-sonnet-5_high_*"].
LLM_INCLUDE = "all"
LLM_EXCLUDE: list[str] = []

BOOTSTRAP_N = 2000           # resamples for the headline alpha CIs; 0 to skip
BOOTSTRAP_N_PANEL = 600      # cheaper CIs for the secondary named panels
BOOTSTRAP_CI = 0.95
SEED = 20260831

MIN_SUPPORT = 3              # per-label metrics below this are starred, not suppressed
TOP_CONTESTED = 15           # most-disagreed reviews to list
SUBSET_PRINT_ALL = 80        # print every subset if there are at most this many
SUBSET_PRINT_EDGES = 12      # otherwise print this many best and worst per report
SUBSET_MAX_RATERS = 13       # refuse the exhaustive sweep beyond this many raters
# The sweep is 2^k panels and costs roughly: 7 raters 0.1s, 9 -> 0.3s, 11 -> 1.3s,
# 13 -> 6s, 15 -> 32s. Raise SUBSET_MAX_RATERS knowingly; the report only ever
# prints the extremes, but the metrics JSON carries every panel.

# ══════════════════════════════════════════════════════════════════════

SCRIPT_DIR = Path(__file__).resolve().parent

CLASS_PREFIX = {
    "Temporal": "T", "Monetary": "M", "Social": "S",
    "Psychological": "P", "Technical": "Tech",
}
CLASS_NAME = {v: k for k, v in CLASS_PREFIX.items()}
CLASS_ORDER = ["T", "M", "S", "P", "Tech"]

ROLE_ORDER = {"author": 0, "gold": 1, "human": 2, "llm": 3}


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
        hl, meso = lab.get("high_level"), lab.get("meso_label")
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

class DistSpace:
    """The value universe and its pairwise distance matrix, built once and
    shared by every panel. Rebuilding this per subset is what makes an
    exhaustive 2^k sweep quadratic in the number of raters instead of linear."""

    def __init__(self, values, dist):
        vals = sorted(values, key=lambda s: (len(s), sorted(s)))
        self.values = vals
        self.index = {v: i for i, v in enumerate(vals)}
        self.dist = dist
        k = len(vals)
        self.k = k
        D = [[0.0] * k for _ in range(k)]
        for i in range(k):
            for j in range(i + 1, k):
                d = dist(vals[i], vals[j])
                D[i][j] = D[j][i] = d
        self.D = D
        self.Dnp = _np.array(D, dtype=float) if (_np is not None and k) else None


class Alpha:
    """Alpha over set-valued units, with the pieces cached so a bootstrap
    over units is cheap: per-unit disagreement never changes, and the
    expected term is a quadratic form c'Dc over counts of distinct values."""

    def __init__(self, units: list[list], dist, space: "DistSpace | None" = None):
        self.units = [u for u in units if len(u) >= 2]
        self.dist = dist
        self.space = space or DistSpace({v for u in self.units for v in u}, dist)
        self.index = self.space.index
        D, k = self.space.D, self.space.k
        self.D, self.Dnp, self.k = D, self.space.Dnp, k
        # per unit: the observed term, and the count vector of its values
        self.unit_do, self.unit_counts, self.unit_m, self.unit_vec = [], [], [], []
        for u in self.units:
            ids = [self.index[v] for v in u]
            m = len(ids)
            s = 0.0
            for a in range(m):
                for b in range(m):
                    if a != b:
                        s += D[ids[a]][ids[b]]
            self.unit_do.append(s / (m - 1))
            self.unit_counts.append(Counter(ids))
            self.unit_m.append(m)
            if self.Dnp is not None:
                v = _np.zeros(k)
                for i in ids:
                    v[i] += 1
                self.unit_vec.append(v)
        if self.Dnp is not None and self.units:
            self.V = _np.array(self.unit_vec)
            self.do_np = _np.array(self.unit_do)
            self.m_np = _np.array(self.unit_m, dtype=float)

    def _alpha(self, idxs):
        if not idxs:
            return None
        n = sum(self.unit_m[i] for i in idxs)
        if n < 2:
            return None
        do = sum(self.unit_do[i] for i in idxs) / n
        if self.Dnp is not None:
            c = self.V[idxs].sum(axis=0)
            de = float(c @ self.Dnp @ c) / (n * (n - 1))
        else:
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
        """Percentile CI from resampling units with replacement."""
        if not self.units or n_resamples <= 0:
            return None, None
        N = len(self.units)
        out = []
        if self.Dnp is not None:
            gen = _np.random.default_rng(rng.randrange(2 ** 32))
            picks = gen.integers(0, N, size=(n_resamples, N))
            for row in picks:
                n = float(self.m_np[row].sum())
                if n < 2:
                    continue
                do = float(self.do_np[row].sum()) / n
                c = self.V[row].sum(axis=0)
                de = float(c @ self.Dnp @ c) / (n * (n - 1))
                if de == 0:
                    if do == 0:
                        out.append(1.0)
                    continue
                out.append(1.0 - do / de)
        else:
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


def alpha_of(units, dist, space=None):
    a = Alpha(units, dist, space)
    return a.value(), a


# ────────────────────────── the rater roster ──────────────────────────

class Rater:
    __slots__ = ("code", "name", "role", "source", "ballots", "independent",
                 "notes", "detail")

    def __init__(self, code, name, role, source, ballots, independent, notes,
                 detail=None):
        self.code = code
        self.name = name
        self.role = role
        self.source = source
        self.ballots = ballots
        self.independent = independent
        self.notes = notes
        self.detail = detail or {}

    def __repr__(self):
        return f"<Rater {self.code} {self.name} n={len(self.ballots)}>"


def letters(i: int) -> str:
    """0->A .. 25->Z, 26->AA."""
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def short_code(code: str) -> str:
    """'HUMAN-A' -> 'H-A', 'LLM-BC' -> 'L-BC', 'AUTHOR' -> 'AUTH'."""
    if code == "AUTHOR":
        return "AUTH"
    if code == "GOLD":
        return "GOLD"
    if code.startswith("HUMAN-"):
        return "H-" + code[6:]
    if code.startswith("LLM-"):
        return "L-" + code[4:]
    return code[:6]


# ───────────────────────────── loading ────────────────────────────────

def set_from_labels(labs, legal, unknown: Counter):
    known = []
    for c in labs or []:
        if isinstance(c, dict):
            c = c.get("label")
        c = str(c or "").strip()
        if not c:
            continue
        if c in legal:
            known.append(c)
        else:
            unknown[c] += 1
    return frozenset(known)


def load_reference(path: Path, legal: list[str]):
    """The author / gold file: ballots keyed by review_id, plus review order
    and per-review metadata."""
    ballots, order, meta, unknown = {}, [], {}, Counter()
    for o in jsonl(path):
        rid = str(o.get("review_id", ""))
        if not rid or rid in ballots:
            continue
        labs = o.get("actual_labels")
        if labs is None:
            labs = [s.strip() for s in str(o.get("actual_labels_str", "")).split(";")]
        ballots[rid] = set_from_labels(labs, legal, unknown)
        order.append(rid)
        meta[rid] = {
            "game_name": o.get("game_name", ""),
            "market": o.get("market", ""),
            "star_rating": o.get("star_rating"),
            "stratum": o.get("stratum", ""),
            "codebook_version": o.get("codebook_version", ""),
        }
    return ballots, order, meta, dict(unknown)


def coder_labels(o: dict, legal: list[str], unknown: Counter):
    """dp_coder's own tolerance: labels, else assigned_labels, else the
    29 binary columns. Booleans arrive as 0/1 or as true/false."""
    if isinstance(o.get("labels"), list):
        labs = o["labels"]
    elif isinstance(o.get("assigned_labels"), list):
        labs = o["assigned_labels"]
    else:
        labs = [c for c in legal if o.get(c) in (1, "1", True)]
    return set_from_labels(labs, legal, unknown)


def load_human_coders(folder: Path, legal: list[str], known_ids: set[str]):
    """-> [(name, ballots, notes), ...] in filename order.

    Ballots are restricted to review_ids that exist in the reference file. A
    coder file carrying ids from somewhere else must not silently inflate that
    coder's coverage."""
    out = []
    seen = set()
    for p in sorted(folder.glob("*.jsonl")):
        rows = list(jsonl(p))
        if not rows:
            continue
        names = Counter(str(r.get("coder_name", "")).strip()
                        for r in rows if str(r.get("coder_name", "")).strip())
        base = names.most_common(1)[0][0] if names else re.sub(r"^coder[_-]", "", p.stem)
        name, n = base, 2
        while name in seen:
            name, n = f"{base}#{n}", n + 1
        seen.add(name)

        ballots, abstain, foreign, unknown = {}, 0, 0, Counter()
        for r in rows:
            rid = str(r.get("review_id", ""))
            if not rid:
                continue
            if rid not in known_ids:
                foreign += 1
                continue
            if r.get("saved") not in (1, "1", True):
                abstain += 1
                continue
            ballots[rid] = coder_labels(r, legal, unknown)
        out.append((name, ballots, {
            "file": p.name, "rows": len(rows), "coded": len(ballots),
            "abstain": abstain, "foreign": foreign,
            "unknown_codes": dict(unknown),
            "renamed_from": base if name != base else None,
            "name_variants": [k for k, _ in names.most_common()[1:]],
        }))
    return out


def discover_llm_runs(runs_dir: Path):
    """Every <model>/<effort>/<prompt>/*_responses.jsonl under runs_dir, with
    whatever its sibling summary knows about it."""
    runs = []
    if not runs_dir.is_dir():
        return runs
    for resp in sorted(runs_dir.glob("**/*_responses.jsonl")):
        d = resp.parent
        summary = {}
        for s in d.glob("*_summary.json"):
            try:
                summary = json.loads(s.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                summary = {}
            break
        tag = summary.get("tag") or resp.name.replace("_responses.jsonl", "")
        try:
            parts = d.relative_to(runs_dir).parts
        except ValueError:
            parts = ()
        runs.append({
            "tag": tag,
            "path": resp,
            "model": summary.get("model") or (parts[0] if len(parts) > 0 else "?"),
            "effort": summary.get("reasoning_effort") or (parts[1] if len(parts) > 1 else "?"),
            "prompt_stem": summary.get("prompt_stem") or (parts[2] if len(parts) > 2 else "?"),
            "provider": summary.get("provider", "?"),
            "n": summary.get("n"),
            "complete": summary.get("complete"),
            "web_search": summary.get("web_search"),
            "eval_set": summary.get("eval_set"),
            "reviews_file": summary.get("reviews_file"),
            "prompt_sha256": (summary.get("prompt_sha256") or "")[:12],
        })
    runs.sort(key=lambda r: (r["model"], r["prompt_stem"], r["effort"]))
    return runs


def load_llm_run(run: dict, legal: list[str], known_ids: set[str]):
    """A model run is a rater. A row that failed to parse is an abstention,
    never a NONE: the model did not decline to label, we failed to read it."""
    ballots, abstain, foreign, unknown = {}, 0, 0, Counter()
    dup = 0
    for r in jsonl(run["path"]):
        rid = str(r.get("review_id", ""))
        if not rid:
            continue
        if rid not in known_ids:
            foreign += 1
            continue
        if rid in ballots:
            dup += 1
            continue
        parsed = r.get("parsed")
        if r.get("error_type") or not isinstance(parsed, dict) \
                or not isinstance(parsed.get("labels"), list):
            abstain += 1
            continue
        ballots[rid] = set_from_labels(parsed["labels"], legal, unknown)
    return ballots, {
        "file": str(run["path"].name), "rows": len(ballots) + abstain + foreign,
        "coded": len(ballots), "abstain": abstain, "foreign": foreign,
        "duplicate_rows": dup, "unknown_codes": dict(unknown),
        "renamed_from": None, "name_variants": [],
    }


def run_source(run: dict, runs_dir: Path) -> str:
    """A short, stable pointer to the run: the directory, not the filename."""
    try:
        return f"{LLM_RUNS_DIR.rstrip('/')}/{run['path'].parent.relative_to(runs_dir)}"
    except ValueError:
        return str(run["path"].parent)


def select_runs(runs, include, exclude):
    def matches(tag, pats):
        return any(tag == p or fnmatch.fnmatch(tag, p) for p in pats)
    if include == "all" or include is None:
        keep = list(runs)
    else:
        keep = [r for r in runs if matches(r["tag"], include)]
    if exclude:
        keep = [r for r in keep if not matches(r["tag"], exclude)]
    return keep


# ─────────────────────────── formatting ───────────────────────────────

def bar(ch="=", n=100):
    return ch * n


def head(title, ch="="):
    return f"{bar(ch)}\n{title}\n{bar(ch)}"


def f3(x):
    return "n/a" if x is None else f"{x:.3f}"


def table(rows, headers, aligns=None, indent="  "):
    if not rows:
        return indent + "(none)"
    cols = len(headers)
    w = [len(str(h)) for h in headers]
    for r in rows:
        for i in range(cols):
            w[i] = max(w[i], len(str(r[i])))
    aligns = aligns or ["<"] + [">"] * (cols - 1)
    out = [indent + "  ".join(f"{headers[i]:{aligns[i]}{w[i]}}" for i in range(cols))]
    for r in rows:
        out.append(indent + "  ".join(
            f"{str(r[i]):{aligns[i]}{w[i]}}" for i in range(cols)))
    return "\n".join(out)


def grid(codes, cell, diag="  .  ", indent="  "):
    """Square rater x rater matrix, printed with short codes."""
    sc = [short_code(c) for c in codes]
    w = max([len(s) for s in sc] + [5])
    out = [indent + " " * (w + 1) + " ".join(f"{s:>{w}}" for s in sc)]
    for i, a in enumerate(codes):
        row = []
        for j, b in enumerate(codes):
            row.append(f"{diag:>{w}}" if i == j else f"{cell(a, b):>{w}}")
        out.append(indent + f"{sc[i]:<{w}} " + " ".join(row))
    return "\n".join(out)


def interpret(a):
    if a is None:
        return "undefined"
    if a >= 0.800:
        return "firm (>= .800)"
    if a >= 0.667:
        return "tentative (>= .667)"
    if a >= 0.600:
        return "below tentative; defensible for a 29-label multi-label construct only with documented adjudication"
    return "below .600"


def prf(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return p, r, f


# ───────────────────────────── panels ─────────────────────────────────

def panel_units(raters, order):
    """Ballot rows for a set of raters, in review order."""
    return [[r.ballots[rid] for r in raters if rid in r.ballots] for rid in order]


def panel_alpha(raters, order, dist=d_masi, space=None):
    return alpha_of(panel_units(raters, order), dist, space)


def pair_stats(a: Rater, b: Rater, order):
    both = [rid for rid in order if rid in a.ballots and rid in b.ballots]
    if not both:
        return {"n": 0, "exact": None, "jaccard": None, "masi": None, "alpha": None}
    ex = sum(1 for r in both if a.ballots[r] == b.ballots[r]) / len(both)
    jc = sum(jaccard(a.ballots[r], b.ballots[r]) for r in both) / len(both)
    ms = sum(masi_sim(a.ballots[r], b.ballots[r]) for r in both) / len(both)
    al, _ = alpha_of([[a.ballots[r], b.ballots[r]] for r in both], d_masi)
    return {"n": len(both), "exact": ex, "jaccard": jc, "masi": ms, "alpha": al}


def score_against(pred: Rater, ref: Rater, order):
    """Micro P/R/F1 and example-F1 of one rater treated as a prediction of
    another. Only reviews both of them coded."""
    both = [rid for rid in order if rid in pred.ballots and rid in ref.ballots]
    tp = fp = fn = 0
    ex_f1 = 0.0
    exact = 0
    for rid in both:
        P, G = pred.ballots[rid], ref.ballots[rid]
        t = len(P & G)
        tp += t
        fp += len(P - G)
        fn += len(G - P)
        if not P and not G:
            ex_f1 += 1.0
        elif P or G:
            ex_f1 += 2 * t / (len(P) + len(G)) if (len(P) + len(G)) else 0.0
        if P == G:
            exact += 1
    p, r, f = prf(tp, fp, fn)
    n = len(both)
    return {"n": n, "tp": tp, "fp": fp, "fn": fn, "micro_p": p, "micro_r": r,
            "micro_f1": f, "example_f1": ex_f1 / n if n else None,
            "exact_match": exact / n if n else None}


# ─────────────────────────────── main ─────────────────────────────────

def build_args():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list-llms", action="store_true",
                    help="print the discovered LLM runs and exit")
    ap.add_argument("--llm", action="append", default=None, metavar="TAG",
                    help="run tag or glob to include; repeatable. Overrides LLM_INCLUDE.")
    ap.add_argument("--exclude-llm", action="append", default=None, metavar="TAG",
                    help="run tag or glob to drop; repeatable")
    ap.add_argument("--no-llm", action="store_true", help="humans only")
    ap.add_argument("--no-gold", action="store_true", help="drop the GOLD rater")
    ap.add_argument("--no-author", action="store_true", help="drop the AUTHOR rater")
    ap.add_argument("--only", default=None, metavar="CODES",
                    help="comma-separated rater codes to keep, e.g. AUTHOR,HUMAN-A,LLM-A")
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--report", default=None, help="report filename")
    ap.add_argument("--json", default=None, help="metrics filename, or 'none'")
    ap.add_argument("--bootstrap", type=int, default=None)
    ap.add_argument("--quiet", action="store_true", help="do not echo the report")
    return ap


def main() -> int:
    args = build_args().parse_args()
    rng = random.Random(SEED)
    t_start = datetime.datetime.now()

    auth_path = rel(AUTHOR_FILE)
    if not auth_path.exists():
        print(f"ERROR: author file not found: {auth_path}", file=sys.stderr)
        return 1

    legal = load_codebook(rel(CODEBOOK))
    if not legal:
        print("ERROR: no labels parsed from the codebook", file=sys.stderr)
        return 1
    legal_pos = {c: i for i, c in enumerate(legal)}

    runs_dir = rel(LLM_RUNS_DIR)
    all_runs = discover_llm_runs(runs_dir)

    if args.list_llms:
        print(f"LLM runs under {runs_dir}\n")
        print(table([[r["tag"], r["model"], r["effort"], r["prompt_stem"],
                      r["provider"], r["n"] if r["n"] is not None else "?",
                      "yes" if r["complete"] else "NO",
                      "yes" if r["web_search"] else "no",
                      r["eval_set"] or "-"] for r in all_runs],
                    ["tag", "model", "effort", "prompt", "provider", "n",
                     "complete", "search", "eval_set"],
                    ["<", "<", "<", "<", "<", ">", ">", ">", "<"]))
        return 0

    # ── the review universe comes from the author file ────────────────
    author_b, order, meta, author_unknown = load_reference(auth_path, legal)
    known_ids = set(order)

    raters: list[Rater] = []
    if INCLUDE_AUTHOR and not args.no_author:
        raters.append(Rater("AUTHOR", "author", "author", AUTHOR_FILE,
                            author_b, True,
                            {"file": auth_path.name, "rows": len(order),
                             "coded": len(author_b), "abstain": 0, "foreign": 0,
                             "unknown_codes": author_unknown,
                             "renamed_from": None, "name_variants": []}))

    gold_unknown = {}
    if INCLUDE_GOLD and GOLD_FILE and not args.no_gold:
        gpath = rel(GOLD_FILE)
        if gpath.exists():
            gold_b, _, _, gold_unknown = load_reference(gpath, legal)
            gold_b = {k: v for k, v in gold_b.items() if k in known_ids}
            raters.append(Rater("GOLD", "adjudicated_panel", "gold", GOLD_FILE,
                                gold_b, False,
                                {"file": gpath.name, "rows": len(gold_b),
                                 "coded": len(gold_b), "abstain": 0, "foreign": 0,
                                 "unknown_codes": gold_unknown,
                                 "renamed_from": None, "name_variants": []}))
        else:
            print(f"  ! gold file not found, skipped: {gpath}", file=sys.stderr)

    cod_dir = rel(CODERS_DIR)
    humans = load_human_coders(cod_dir, legal, known_ids) if cod_dir.is_dir() else []
    for i, (name, ballots, notes) in enumerate(humans):
        raters.append(Rater(f"HUMAN-{letters(i)}", name, "human",
                            f"{CODERS_DIR}/{notes['file']}", ballots, True, notes))

    chosen_runs = []
    if not args.no_llm:
        include = args.llm if args.llm else LLM_INCLUDE
        exclude = (args.exclude_llm or []) + list(LLM_EXCLUDE)
        chosen_runs = select_runs(all_runs, include, exclude)
        for i, run in enumerate(chosen_runs):
            ballots, notes = load_llm_run(run, legal, known_ids)
            raters.append(Rater(
                f"LLM-{letters(i)}",
                f"{run['model']} @ {run['effort']} / {run['prompt_stem']}",
                "llm",
                run_source(run, runs_dir),
                ballots, True, notes,
                {k: run[k] for k in ("tag", "model", "effort", "prompt_stem",
                                     "provider", "n", "complete", "web_search",
                                     "eval_set", "prompt_sha256")}))

    if args.only:
        keep = {c.strip().upper() for c in args.only.split(",") if c.strip()}
        raters = [r for r in raters if r.code in keep]

    if len(raters) < 2:
        print("ERROR: fewer than two raters after selection", file=sys.stderr)
        return 1

    boot_n = BOOTSTRAP_N if args.bootstrap is None else args.bootstrap
    boot_n_panel = min(BOOTSTRAP_N_PANEL, boot_n)

    by_code = {r.code: r for r in raters}
    codes = [r.code for r in raters]
    indep = [r for r in raters if r.independent]
    humans_r = [r for r in raters if r.role == "human"]
    llms_r = [r for r in raters if r.role == "llm"]
    author_r = [r for r in raters if r.role == "author"]
    gold_r = [r for r in raters if r.role == "gold"]
    human_side = author_r + humans_r          # every independent human ballot

    units_all = panel_units(raters, order)
    pairable = [i for i, u in enumerate(units_all) if len(u) >= 2]

    # Every panel draws its values from the same pool of ballots, so the value
    # index and the distance matrix are built once and reused by all of them.
    pool = {v for u in units_all for v in u}
    SP_MASI = DistSpace(pool, d_masi)
    SP_JAC = DistSpace(pool, d_jaccard)
    SP_NOM = DistSpace(pool, d_nominal)
    SP_BIN = DistSpace({frozenset([0]), frozenset([1])}, d_nominal)

    # ══════════════════════════════ report ════════════════════════════
    L = [
        head("AGREEMENT — HUMAN CODERS, AUTHOR, ADJUDICATED GOLD, AND LLM ANNOTATORS"),
        f"generated={t_start.isoformat(timespec='seconds')}",
        f"review universe={AUTHOR_FILE}  units={len(order)}",
        f"codebook={CODEBOOK}  labels={len(legal)}",
        f"raters={len(raters)}  independent={len(indep)}  "
        f"(author={len(author_r)} human={len(humans_r)} llm={len(llms_r)} gold={len(gold_r)})",
        f"llm_runs_dir={LLM_RUNS_DIR}  discovered={len(all_runs)}  "
        f"selected={len(chosen_runs)}  in panel={len(llms_r)}",
        f"BOOTSTRAP_N={boot_n} (secondary panels {boot_n_panel}) CI={BOOTSTRAP_CI} "
        f"SEED={SEED} MIN_SUPPORT={MIN_SUPPORT}",
        "",
        head("RATER LEGEND", "-"),
    ]

    lrows = []
    for r in raters:
        extra = ""
        if r.role == "llm":
            d = r.detail
            extra = (f"{d.get('provider','?')}  search={'yes' if d.get('web_search') else 'no'}"
                     f"  prompt#{d.get('prompt_sha256','')}")
        elif r.role == "gold":
            extra = "NOT INDEPENDENT — adjudicated from the human ballots"
        lrows.append([r.code, short_code(r.code), r.role,
                      "yes" if r.independent else "NO", r.name, r.source, extra])
    L += [table(lrows, ["code", "short", "role", "indep", "identity", "source", "notes"],
                ["<", "<", "<", ">", "<", "<", "<"]), ""]

    # ── coverage ──────────────────────────────────────────────────────
    L += [head("RATER COVERAGE AND LABELLING RATE", "-")]
    crows = []
    for r in raters:
        cov = len(r.ballots)
        nl = sum(len(s) for s in r.ballots.values())
        none_n = sum(1 for s in r.ballots.values() if not s)
        mx = max((len(s) for s in r.ballots.values()), default=0)
        crows.append([r.code, r.name[:34], cov, len(order) - cov,
                      r.notes.get("abstain", 0), nl,
                      f"{nl / cov:.2f}" if cov else "n/a", mx,
                      none_n, f"{none_n / cov:.3f}" if cov else "n/a"])
    L += [table(crows, ["code", "identity", "coded", "absent", "abstain", "labels",
                        "lab/rev", "max", "NONE", "NONE rate"],
                ["<", "<", ">", ">", ">", ">", ">", ">", ">", ">"]), ""]

    # ── data notes ────────────────────────────────────────────────────
    warn = []
    for r in raters:
        nt = r.notes
        if nt.get("renamed_from"):
            warn.append(f"{r.code}: duplicate name, renamed from {nt['renamed_from']}")
        if nt.get("name_variants"):
            warn.append(f"{r.code}: coder_name varies in-file, also saw "
                        + ", ".join(nt["name_variants"]))
        if nt.get("unknown_codes"):
            warn.append(f"{r.code}: codes not in the codebook: "
                        + ", ".join(f"{k} x{v}" for k, v in nt["unknown_codes"].items()))
        if nt.get("abstain"):
            warn.append(f"{r.code}: {nt['abstain']} row(s) unfinished/unparsed, "
                        "excluded as abstentions (not counted as NONE)")
        if nt.get("foreign"):
            warn.append(f"{r.code}: {nt['foreign']} review_id(s) outside the "
                        "review universe, excluded")
        if nt.get("duplicate_rows"):
            warn.append(f"{r.code}: {nt['duplicate_rows']} duplicate review_id row(s), "
                        "first kept")
        gap = len(order) - nt.get("coded", 0) - nt.get("abstain", 0)
        if gap > 0:
            warn.append(f"{r.code}: {gap} review(s) of {len(order)} missing entirely")
        if r.role == "llm":
            d = r.detail
            if d.get("complete") is False:
                warn.append(f"{r.code}: run marked incomplete in its summary")
            if d.get("eval_set") not in (None, "validation"):
                warn.append(f"{r.code}: summary says eval_set={d.get('eval_set')!r}, "
                            "not 'validation'")
    if gold_r:
        warn.append("GOLD is the adjudicated consensus of AUTHOR and the HUMAN "
                    "coders. Any panel containing GOLD measures distance to "
                    "consensus, not inter-rater reliability.")
    dup_models = Counter(r.detail.get("model") for r in llms_r)
    for m, c in dup_models.items():
        if c > 1:
            warn.append(f"{c} LLM raters share the model {m}; alpha across them is "
                        "self-consistency under a setting change, not independent "
                        "agreement.")
    missing = [order[i] for i, u in enumerate(units_all) if len(u) < 2]
    if missing:
        warn.append(f"{len(missing)} unit(s) with <2 ballots, excluded from alpha")
    if warn:
        L += [head("DATA NOTES", "-")] + [f"  - {w}" for w in warn] + [""]

    # ── headline alpha ────────────────────────────────────────────────
    a_masi, A = panel_alpha(indep, order, d_masi, SP_MASI)
    a_jac, _ = panel_alpha(indep, order, d_jaccard, SP_JAC)
    a_exact, _ = panel_alpha(indep, order, d_nominal, SP_NOM)
    lo, hi = A.bootstrap(boot_n, BOOTSTRAP_CI, rng)
    ci_cache = {tuple(r.code for r in indep): (lo, hi)} if lo is not None else {}
    n_ballots = sum(len(u) for u in panel_units(indep, order) if len(u) >= 2)

    L += [
        head(f"KRIPPENDORFF'S ALPHA — FULL INDEPENDENT PANEL "
             f"({', '.join(r.code for r in indep)})"),
        table([
            ["MASI (set-valued, primary)", f3(a_masi),
             f"[{f3(lo)}, {f3(hi)}]" if lo is not None else "n/a", interpret(a_masi)],
            ["Jaccard (set-valued)", f3(a_jac), "", ""],
            ["nominal (exact set match)", f3(a_exact), "", ""],
        ], ["distance", "alpha", f"{int(BOOTSTRAP_CI * 100)}% CI", "reading"],
            ["<", ">", ">", "<"]),
        "",
        f"  units={len(A.units)}  ballots={n_ballots}  distinct_value_sets={len(A.index)}",
        "",
    ]

    # ── per-class alpha, per panel ────────────────────────────────────
    class_space = {}

    def class_alpha(rs, pre):
        sub = [[frozenset(x for x in s if x.startswith(pre + "_")) for s in u]
               for u in panel_units(rs, order)]
        if pre not in class_space:
            class_space[pre] = DistSpace(
                {frozenset(x for x in s if x.startswith(pre + "_"))
                 for u in units_all for s in u}, d_masi)
        return alpha_of(sub, d_masi, class_space[pre])[0]

    L += [head("PER-CLASS ALPHA (MASI, label set restricted to the class)", "-")]
    prows = []
    for pre in CLASS_ORDER:
        sup = sum(1 for u in panel_units(indep, order) for s in u
                  if any(x.startswith(pre + "_") for x in s))
        row = [f"{pre}  {CLASS_NAME[pre]}", f3(class_alpha(indep, pre)), sup]
        row.append(f3(class_alpha(human_side, pre)) if len(human_side) >= 2 else "n/a")
        row.append(f3(class_alpha(llms_r, pre)) if len(llms_r) >= 2 else "n/a")
        prows.append(row)
    L += [table(prows, ["class", "alpha(all indep)", "positive ballots",
                        "alpha(humans)", "alpha(LLMs)"],
                ["<", ">", ">", ">", ">"]), ""]

    # ── named panels ──────────────────────────────────────────────────
    named: list[tuple[str, list[Rater], int, str]] = []

    def add_panel(label, rs, boot=0, note=""):
        rs = [r for r in rs if r is not None]
        if len(rs) >= 2:
            named.append((label, rs, boot, note))

    add_panel("ALL INDEPENDENT (headline)", indep, boot_n)
    add_panel("ALL RATERS incl. GOLD", raters, boot_n_panel,
              "GOLD dependent — read as distance-to-consensus")
    add_panel("HUMANS + AUTHOR", human_side, boot_n)
    add_panel("HUMAN CODERS only (no author)", humans_r, boot_n)
    add_panel("LLM ANNOTATORS only", llms_r, boot_n_panel,
              "same model at two settings" if len(set(
                  r.detail.get("model") for r in llms_r)) == 1 and len(llms_r) > 1 else "")
    for l in llms_r:
        add_panel(f"HUMANS + AUTHOR + {l.code}", human_side + [l], boot_n_panel)
    if llms_r and human_side:
        add_panel("HUMANS + AUTHOR + all LLMs", human_side + llms_r, boot_n_panel)
    if gold_r and human_side:
        add_panel("AUTHOR + GOLD", author_r + gold_r, 0, "dependent")

    L += [head("NAMED PANELS — ALPHA BY GROUPING")]
    nrows = []
    panel_json = []
    for label, rs, boot, note in named:
        am, Ax = panel_alpha(rs, order, d_masi, SP_MASI)
        aj, _ = panel_alpha(rs, order, d_jaccard, SP_JAC)
        an, _ = panel_alpha(rs, order, d_nominal, SP_NOM)
        key = tuple(r.code for r in rs)
        if key in ci_cache:
            plo, phi = ci_cache[key]
        else:
            plo, phi = Ax.bootstrap(boot, BOOTSTRAP_CI, rng) if boot else (None, None)
            if plo is not None:
                ci_cache[key] = (plo, phi)
        nrows.append([label, len(rs), len(Ax.units), f3(am),
                      f"[{f3(plo)}, {f3(phi)}]" if plo is not None else "",
                      f3(aj), f3(an), note])
        panel_json.append({
            "panel": label, "codes": [r.code for r in rs], "n_raters": len(rs),
            "n_units": len(Ax.units), "alpha_masi": am,
            "alpha_masi_ci": [plo, phi] if plo is not None else None,
            "alpha_jaccard": aj, "alpha_nominal": an, "note": note,
        })
    L += [table(nrows, ["panel", "k", "units", "alpha(MASI)",
                        f"{int(BOOTSTRAP_CI * 100)}% CI", "alpha(Jac)",
                        "alpha(exact)", "note"],
                ["<", ">", ">", ">", ">", ">", ">", "<"]), ""]

    # ── pairwise matrices ─────────────────────────────────────────────
    P = {}
    for a, b in combinations(raters, 2):
        st = pair_stats(a, b, order)
        P[(a.code, b.code)] = st
        P[(b.code, a.code)] = st

    L += [head("PAIRWISE MATRICES (units both raters coded)")]
    legend = "  ".join(f"{short_code(r.code)}={r.code}" for r in raters)
    L += ["  legend: " + legend, ""]
    for title, key, fmt in [
        ("alpha (MASI), pairwise", "alpha", f3),
        ("mean MASI similarity", "masi", f3),
        ("mean Jaccard similarity", "jaccard", f3),
        ("exact set-match rate", "exact", f3),
        ("units compared", "n", lambda v: "n/a" if v is None else str(v)),
    ]:
        L += [f"  {title}",
              grid(codes, lambda a, b: fmt(P[(a, b)][key])), ""]

    # per-rater mean to everyone else, and to each block
    L += [head("PAIRWISE SUMMARY PER RATER (mean over the other raters)", "-")]
    srows = []
    for r in raters:
        def mean_to(group, key="masi"):
            vs = [P[(r.code, o.code)][key] for o in group
                  if o.code != r.code and P[(r.code, o.code)][key] is not None]
            return sum(vs) / len(vs) if vs else None
        srows.append([
            r.code, r.role,
            f3(mean_to(raters)), f3(mean_to(human_side)), f3(mean_to(llms_r)),
            f3(mean_to(raters, "alpha")), f3(mean_to(raters, "exact")),
        ])
    L += [table(srows, ["code", "role", "MASI to all", "MASI to humans",
                        "MASI to LLMs", "alpha to all", "exact to all"],
                ["<", "<", ">", ">", ">", ">", ">"]), ""]

    # ── human ceiling vs LLM ──────────────────────────────────────────
    hh = [P[(a.code, b.code)] for a, b in combinations(human_side, 2)]
    ceiling = None
    if hh:
        hm = [x["masi"] for x in hh if x["masi"] is not None]
        ha = [x["alpha"] for x in hh if x["alpha"] is not None]
        ceiling = {
            "pairs": len(hh),
            "masi_mean": sum(hm) / len(hm) if hm else None,
            "masi_min": min(hm) if hm else None,
            "masi_max": max(hm) if hm else None,
            "alpha_mean": sum(ha) / len(ha) if ha else None,
            "alpha_min": min(ha) if ha else None,
            "alpha_max": max(ha) if ha else None,
            "panel_alpha": panel_alpha(human_side, order, d_masi, SP_MASI)[0],
        }

    if llms_r and ceiling:
        L += [head("HUMAN CEILING vs LLM ANNOTATORS")]
        L += [
            "  The question a corpus paper has to answer is not 'is the model good',",
            "  it is 'does the model disagree with the humans no more than the humans",
            "  disagree with each other'. The human-human band below is that ceiling.",
            "",
            table([
                ["human-human pairs", ceiling["pairs"], "", ""],
                ["mean pairwise MASI", f3(ceiling["masi_mean"]),
                 f3(ceiling["masi_min"]), f3(ceiling["masi_max"])],
                ["mean pairwise alpha", f3(ceiling["alpha_mean"]),
                 f3(ceiling["alpha_min"]), f3(ceiling["alpha_max"])],
                ["human panel alpha (MASI)", f3(ceiling["panel_alpha"]), "", ""],
            ], ["human ceiling", "value", "min", "max"], ["<", ">", ">", ">"]),
            "",
        ]
        crows2 = []
        for l in llms_r:
            ms = [P[(l.code, h.code)]["masi"] for h in human_side]
            ms = [x for x in ms if x is not None]
            als = [P[(l.code, h.code)]["alpha"] for h in human_side]
            als = [x for x in als if x is not None]
            mmean = sum(ms) / len(ms) if ms else None
            amean = sum(als) / len(als) if als else None
            swap_panels = []
            for h in human_side:
                rest = [x for x in human_side if x.code != h.code]
                if len(rest) >= 1:
                    swap_panels.append(
                        panel_alpha(rest + [l], order, d_masi, SP_MASI)[0])
            swap = [x for x in swap_panels if x is not None]
            added = panel_alpha(human_side + [l], order, d_masi, SP_MASI)[0]
            if mmean is None or ceiling["masi_min"] is None:
                verdict = "n/a"
            elif mmean >= ceiling["masi_mean"]:
                verdict = "at or above the human mean"
            elif mmean >= ceiling["masi_min"]:
                verdict = "inside the human band"
            else:
                verdict = "BELOW the weakest human pair"
            crows2.append([
                l.code, l.name[:32], f3(mmean), f3(min(ms) if ms else None),
                f3(max(ms) if ms else None), f3(amean), f3(added),
                f3(sum(swap) / len(swap) if swap else None), verdict])
        L += [table(crows2, ["code", "identity", "MASI to humans", "min", "max",
                             "alpha to humans", "panel+LLM", "swap-in alpha",
                             "verdict"],
                    ["<", "<", ">", ">", ">", ">", ">", ">", "<"]),
              "  panel+LLM   = alpha of the human panel with the LLM added as an extra rater",
              "  swap-in     = mean alpha when the LLM replaces one human, over each human dropped",
              ""]

    # ── leave-one-out ─────────────────────────────────────────────────
    if len(indep) >= 3:
        L += [head("LEAVE-ONE-OUT (independent panel)", "-")]
        base = a_masi
        lrows2 = []
        for r in indep:
            rest = [x for x in indep if x.code != r.code]
            a2, _ = panel_alpha(rest, order, d_masi, SP_MASI)
            delta = (a2 - base) if (a2 is not None and base is not None) else None
            lrows2.append([f"drop {r.code}", r.name[:30], len(rest), f3(a2),
                           ("" if delta is None else f"{delta:+.3f}")])
        lrows2.sort(key=lambda r: -(float(r[4]) if r[4] else 0))
        L += [table(lrows2, ["panel", "identity", "k", "alpha(MASI)", "delta"],
                    ["<", "<", ">", ">", ">"]),
              f"  baseline (all {len(indep)} independent raters) = {f3(base)};"
              " a large positive delta marks the rater most out of step",
              ""]

    # ── all subsets ───────────────────────────────────────────────────
    L += [head("ALL RATER COMBINATIONS")]
    subsets = []
    if len(raters) > SUBSET_MAX_RATERS:
        L += [f"  {len(raters)} raters — the exhaustive sweep over 2^k subsets is "
              f"skipped past SUBSET_MAX_RATERS={SUBSET_MAX_RATERS}.", ""]
    else:
        for k in range(2, len(raters) + 1):
            for combo in combinations(raters, k):
                am, Ax = panel_alpha(list(combo), order, d_masi, SP_MASI)
                aj, _ = panel_alpha(list(combo), order, d_jaccard, SP_JAC)
                cds = [r.code for r in combo]
                subsets.append({
                    "codes": cds, "size": k, "n_units": len(Ax.units),
                    "alpha_masi": am, "alpha_jaccard": aj,
                    "has_gold": any(r.role == "gold" for r in combo),
                    "n_human": sum(1 for r in combo if r.role in ("human", "author")),
                    "n_llm": sum(1 for r in combo if r.role == "llm"),
                })

        by_size = defaultdict(list)
        for s in subsets:
            if s["alpha_masi"] is not None:
                by_size[s["size"]].append(s)
        srows2 = []
        for k in sorted(by_size):
            vs = sorted(s["alpha_masi"] for s in by_size[k])
            best = max(by_size[k], key=lambda s: s["alpha_masi"])
            worst = min(by_size[k], key=lambda s: s["alpha_masi"])
            srows2.append([
                k, len(vs), f3(min(vs)), f3(vs[len(vs) // 2]),
                f3(sum(vs) / len(vs)), f3(max(vs)),
                "+".join(short_code(c) for c in best["codes"]),
                "+".join(short_code(c) for c in worst["codes"])])
        L += ["  distribution of alpha(MASI) by panel size",
              table(srows2, ["k", "panels", "min", "median", "mean", "max",
                             "best panel", "worst panel"],
                    ["<", ">", ">", ">", ">", ">", "<", "<"]), ""]

        # composition effect: pure-human vs mixed vs pure-LLM
        def bucket(s):
            if s["has_gold"]:
                return "contains GOLD (dependent)"
            if s["n_llm"] == 0:
                return "humans only"
            if s["n_human"] == 0:
                return "LLMs only"
            return "mixed human + LLM"
        bk = defaultdict(list)
        for s in subsets:
            if s["alpha_masi"] is not None:
                bk[bucket(s)].append(s["alpha_masi"])
        brows = []
        for name in ["humans only", "LLMs only", "mixed human + LLM",
                     "contains GOLD (dependent)"]:
            vs = sorted(bk.get(name, []))
            if vs:
                brows.append([name, len(vs), f3(min(vs)), f3(vs[len(vs) // 2]),
                              f3(sum(vs) / len(vs)), f3(max(vs))])
        L += ["  alpha(MASI) by panel composition",
              table(brows, ["composition", "panels", "min", "median", "mean", "max"],
                    ["<", ">", ">", ">", ">", ">"]), ""]

        ranked = sorted([s for s in subsets if s["alpha_masi"] is not None],
                        key=lambda s: -s["alpha_masi"])
        def sub_row(s):
            return ["+".join(short_code(c) for c in s["codes"]), s["size"],
                    s["n_units"], f3(s["alpha_masi"]), f3(s["alpha_jaccard"]),
                    "gold" if s["has_gold"] else ""]
        hdr = ["panel", "k", "units", "alpha(MASI)", "alpha(Jac)", "flag"]
        al = ["<", ">", ">", ">", ">", "<"]
        if len(ranked) <= SUBSET_PRINT_ALL:
            L += [f"  every panel of 2+ raters, best first ({len(ranked)} panels)",
                  table([sub_row(s) for s in ranked], hdr, al), ""]
        else:
            e = SUBSET_PRINT_EDGES
            L += [f"  {len(ranked)} panels; the {e} strongest and {e} weakest "
                  "(the full sweep is in the metrics JSON)",
                  table([sub_row(s) for s in ranked[:e]], hdr, al),
                  "  ...",
                  table([sub_row(s) for s in ranked[-e:]], hdr, al), ""]

    # ── each rater against GOLD ───────────────────────────────────────
    if gold_r:
        g = gold_r[0]
        L += [head("EVERY RATER AGAINST THE ADJUDICATED GOLD SET", "-")]
        grows = []
        for r in raters:
            if r.code == g.code:
                continue
            sc = score_against(r, g, order)
            grows.append([r.code, r.role, r.name[:30], sc["n"],
                          f"{sc['micro_p']:.3f}", f"{sc['micro_r']:.3f}",
                          f"{sc['micro_f1']:.3f}", f3(sc["example_f1"]),
                          f3(sc["exact_match"]), sc["tp"], sc["fp"], sc["fn"]])
        grows.sort(key=lambda r: -float(r[6]))
        L += [table(grows, ["code", "role", "identity", "n", "micro P", "micro R",
                            "micro F1", "example F1", "exact", "tp", "fp", "fn"],
                    ["<", "<", "<", ">", ">", ">", ">", ">", ">", ">", ">", ">"]),
              "  GOLD was adjudicated from AUTHOR and the HUMAN ballots, so their",
              "  scores here are inflated by construction and are not comparable to",
              "  the LLM scores. Only the LLM rows are an out-of-sample measurement.",
              ""]

    # ── per label ─────────────────────────────────────────────────────
    L += [head("PER-LABEL AGREEMENT (binary presence)")]

    def binary_units(rs, col):
        return [[frozenset([1 if col in s else 0]) for s in u]
                for u in panel_units(rs, order)]

    def fleiss(rs, col):
        kk, mm = [], []
        for u in panel_units(rs, order):
            v = [1 if col in s else 0 for s in u]
            kk.append(sum(v))
            mm.append(len(v))
        idx = [i for i in range(len(kk)) if mm[i] >= 2]
        if not idx:
            return None
        pbar = sum((kk[i] * (kk[i] - 1) + (mm[i] - kk[i]) * (mm[i] - kk[i] - 1))
                   / (mm[i] * (mm[i] - 1)) for i in idx) / len(idx)
        p = sum(kk[i] for i in idx) / sum(mm[i] for i in idx)
        pe = p * p + (1 - p) * (1 - p)
        return (pbar - pe) / (1 - pe) if pe < 1 else None

    per_label = {}
    prows2 = []
    for col in legal:
        a_all, _ = alpha_of(binary_units(indep, col), d_nominal, SP_BIN)
        kap = fleiss(indep, col)
        a_hum = alpha_of(binary_units(human_side, col), d_nominal, SP_BIN)[0] \
            if len(human_side) >= 2 else None
        a_llm = alpha_of(binary_units(llms_r, col), d_nominal, SP_BIN)[0] \
            if len(llms_r) >= 2 else None
        uu = panel_units(indep, order)
        kk = [sum(1 for s in u if col in s) for u in uu]
        mm = [len(u) for u in uu]
        idx = [i for i in range(len(uu)) if mm[i] >= 2]
        support = sum(1 for i in idx if kk[i] > 0)
        full = sum(1 for i in idx if kk[i] == mm[i] and kk[i] > 0)
        assigns = sum(kk)
        star = "*" if support < MIN_SUPPORT else " "
        prows2.append([col + star, support, full, assigns, f3(a_all), f3(kap),
                       f3(a_hum), f3(a_llm)])
        per_label[col] = {
            "units_any": support, "units_unanimous": full, "assignments": assigns,
            "alpha_all_independent": a_all, "fleiss_kappa": kap,
            "alpha_humans": a_hum, "alpha_llms": a_llm,
            "low_support": support < MIN_SUPPORT,
        }
    L += [table(prows2, ["label", "units", "unanim", "assigns", "alpha(indep)",
                         "Fleiss k", "alpha(humans)", "alpha(LLMs)"],
                ["<", ">", ">", ">", ">", ">", ">", ">"]),
          f"  (* support < MIN_SUPPORT={MIN_SUPPORT}; alpha on a handful of units is "
          "noise, not a measurement)", ""]

    # ── prevalence ────────────────────────────────────────────────────
    L += [head("LABEL PREVALENCE BY RATER (assignments over the units that rater coded)", "-")]
    prow2 = []
    for col in legal:
        cells = [sum(1 for s in r.ballots.values() if col in s) for r in raters]
        prow2.append([col] + cells + [sum(cells)])
    prow2.append(["TOTAL"] + [sum(len(s) for s in r.ballots.values()) for r in raters]
                 + [sum(len(s) for r in raters for s in r.ballots.values())])
    prow2.append(["NONE"] + [sum(1 for s in r.ballots.values() if not s) for r in raters]
                 + [sum(1 for r in raters for s in r.ballots.values() if not s)])
    L += [table(prow2, ["label"] + [short_code(c) for c in codes] + ["total"]),
          "  legend: " + legend, ""]

    # ── contested ─────────────────────────────────────────────────────
    L += [head(f"MOST CONTESTED REVIEWS (top {TOP_CONTESTED} by mean pairwise "
               "MASI distance, independent raters)", "-")]
    scored = []
    for rid in order:
        u = [(r.code, r.ballots[rid]) for r in indep if rid in r.ballots]
        if len(u) < 2:
            continue
        ps = list(combinations(u, 2))
        d = sum(1 - masi_sim(s1, s2) for (_, s1), (_, s2) in ps) / len(ps)
        allc = sorted({x for _, s in u for x in s},
                      key=lambda c: legal_pos.get(c, 999))
        split = sorted([c for c in allc
                        if 0 < sum(1 for _, s in u if c in s) < len(u)],
                       key=lambda c: -sum(1 for _, s in u if c in s))
        agreed = [c for c in allc if c not in split]
        txt = ", ".join(f"{c}({sum(1 for _, s in u if c in s)}/{len(u)})"
                        for c in split)
        scored.append([rid[:8], meta[rid]["game_name"][:22], len(u), f"{d:.3f}",
                       len({s for _, s in u}), len(agreed),
                       (txt[:96] + "…") if len(txt) > 97 else (txt or "(none)")])
    scored.sort(key=lambda r: -float(r[3]))
    L += [table(scored[:TOP_CONTESTED],
                ["review", "game", "k", "MASI dist", "distinct sets",
                 "agreed", "labels raters split on (votes/k)"],
                ["<", "<", ">", ">", ">", ">", "<"]),
          "  'agreed' counts labels every rater who coded the review assigned;",
          "  the split column lists the rest with how many raters wanted each.",
          ""]

    # ── NONE ──────────────────────────────────────────────────────────
    none_units = [[1 if not s else 0 for s in u] for u in panel_units(indep, order)
                  if len(u) >= 2]
    none_alpha, _ = alpha_of([[frozenset([v]) for v in u] for u in none_units],
                             d_nominal, SP_BIN)
    none_all = sum(1 for u in none_units if all(u))
    none_any = sum(1 for u in none_units if any(u))
    L += [
        head("NONE (the empty label set)", "-"),
        table([
            ["units where every independent rater said NONE", none_all],
            ["units where at least one said NONE", none_any],
            ["units where raters split on NONE", none_any - none_all],
            ["alpha on NONE as a binary decision", f3(none_alpha)],
        ], ["measure", "n"]),
        "",
        table([[r.code, r.role,
                sum(1 for s in r.ballots.values() if not s),
                f"{sum(1 for s in r.ballots.values() if not s) / len(r.ballots):.3f}"
                if r.ballots else "n/a"] for r in raters],
              ["code", "role", "NONE ballots", "NONE rate"],
              ["<", "<", ">", ">"]),
        "",
        bar(),
    ]

    # ── write ─────────────────────────────────────────────────────────
    out_dir = rel(args.out_dir or OUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    report_name = args.report or REPORT
    report = "\n".join(L) + "\n"
    (out_dir / report_name).write_text(report, encoding="utf-8")

    json_name = args.json if args.json is not None else METRICS_JSON
    wrote_json = None
    if json_name and json_name.lower() != "none":
        payload = {
            "generated": t_start.isoformat(timespec="seconds"),
            "config": {
                "author_file": AUTHOR_FILE, "gold_file": GOLD_FILE,
                "coders_dir": CODERS_DIR, "llm_runs_dir": LLM_RUNS_DIR,
                "codebook": CODEBOOK, "bootstrap_n": boot_n,
                "bootstrap_n_panel": boot_n_panel, "ci": BOOTSTRAP_CI,
                "seed": SEED, "min_support": MIN_SUPPORT,
            },
            "n_units": len(order), "n_pairable": len(pairable),
            "raters": [{
                "code": r.code, "short": short_code(r.code), "name": r.name,
                "role": r.role, "independent": r.independent, "source": r.source,
                "coded": len(r.ballots),
                "labels": sum(len(s) for s in r.ballots.values()),
                "none": sum(1 for s in r.ballots.values() if not s),
                "notes": r.notes, "run": r.detail,
            } for r in raters],
            "discovered_llm_runs": [
                {k: (str(v) if isinstance(v, Path) else v) for k, v in run.items()}
                for run in all_runs],
            "selected_llm_runs": [r["tag"] for r in chosen_runs],
            "headline": {
                "panel": [r.code for r in indep],
                "alpha_masi": a_masi, "alpha_masi_ci": [lo, hi],
                "alpha_jaccard": a_jac, "alpha_nominal": a_exact,
                "units": len(A.units), "ballots": n_ballots,
            },
            "per_class_alpha": {
                r[0].split()[0]: {
                    "all_independent": None if r[1] == "n/a" else float(r[1]),
                    "humans": None if r[3] == "n/a" else float(r[3]),
                    "llms": None if r[4] == "n/a" else float(r[4]),
                } for r in prows},
            "named_panels": panel_json,
            "pairwise": {f"{a}|{b}": P[(a, b)]
                         for a, b in combinations(codes, 2)},
            "human_ceiling": ceiling,
            "subsets": subsets,
            "per_label": per_label,
            "prevalence": {col: {r.code: sum(1 for s in r.ballots.values() if col in s)
                                 for r in raters} for col in legal},
            "none": {"all": none_all, "any": none_any,
                     "split": none_any - none_all, "alpha": none_alpha,
                     "per_rater": {r.code: sum(1 for s in r.ballots.values() if not s)
                                   for r in raters}},
            "vs_gold": ({r.code: score_against(r, gold_r[0], order)
                         for r in raters if r.role != "gold"} if gold_r else None),
            "warnings": warn,
        }
        (out_dir / json_name).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        wrote_json = out_dir / json_name

    if not args.quiet:
        print(report)
    print(f"wrote {out_dir / report_name}"
          + (f" and {wrote_json}" if wrote_json else "")
          + f"  ({(datetime.datetime.now() - t_start).total_seconds():.1f}s)",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
