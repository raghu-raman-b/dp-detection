"""Stage 3 — build the labeling pool and the pilot sets.

pool.jsonl                (python sample.py)
    Stratified sample to POOL_N. PER_GAME_CAP is the *baseline* cap; if
    sum(min(cap, available)) falls short of POOL_N, the effective cap is
    raised by water-filling to the smallest level where the pool exactly
    reaches POOL_N (games with fewer reviews contribute everything;
    large games are capped at the computed level). Proportional across
    markets within each game, seeded RNG. Rows carry sample_weight =
    available/selected per (app_id, market) stratum when truncated.

pilot_random.jsonl        (python sample.py)
    PILOT_RANDOM_N uniform-random reviews from the text-filtered corpus
    (filtered/ output — no ML/binary-classifier filtering).

pilot_targeted.jsonl      (python sample.py --targeted)
    Generated ONLY when requested (run it after labeling the random
    pilot). PILOT_TARGETED_N keyword-matched reviews, round-robin across
    config.TARGET_KEYWORDS, deduped against pilot_random.jsonl on disk,
    stamped stratum + seed_keyword.

Each component has its own RNG stream seeded from config.RNG_SEED, so
pool / pilot_random / pilot_targeted are individually reproducible no
matter which subset of them a given run produces.

Run:  python sample.py [--targeted]
"""
import argparse
import csv
import random
import re
from collections import defaultdict

from tqdm import tqdm

import config
from utils import read_jsonl, write_jsonl_atomic


def rng_for(component: str) -> random.Random:
    return random.Random(f"{config.RNG_SEED}-{component}")


# ------------------------------------------------------ output format ------
MARKET_OUT = {"us": "US", "in": "IN", "gb": "UK"}


def load_app_meta() -> dict:
    """app_id -> {game_name, casino} from games_resolved.csv."""
    if not config.RESOLVED_CSV.exists():
        raise SystemExit("games_resolved.csv missing — run resolve_ids.py")
    meta = {}
    with open(config.RESOLVED_CSV, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            meta[row["app_id"]] = {
                "game_name": row["canonical_title"],
                "casino": bool(int(row["casino"] or 0)),
            }
    return meta


def to_output_row(r: dict, meta: dict, stratum: str,
                  seed_keyword: str = "", extra: dict | None = None) -> dict:
    """Project an internal corpus row onto the delivery schema."""
    m = meta.get(r["app_id"])
    if m is None:
        raise SystemExit(f"app_id {r['app_id']} in filtered corpus but not in "
                         f"games_resolved.csv — resolve/scrape out of sync")
    out = {
        "review_id": r["review_id"],
        "app_id": r["app_id"],
        "game_name": m["game_name"],
        "market": MARKET_OUT[r["market"]],
        "review_date": (r.get("date") or "")[:10],
        "star_rating": r.get("rating"),
        "review_text": r["text"],
        "stratum": stratum,
        "seed_keyword": seed_keyword,
        "casino": m["casino"],
    }
    if extra:
        out.update(extra)
    return out


def load_corpus():
    corpus = []
    files = sorted(config.FILTERED_DIR.glob("*.jsonl"))
    if not files:
        raise SystemExit("no filtered/*.jsonl files — run filter.py first")
    for fp in tqdm(files, desc="loading filtered corpus"):
        corpus.extend(read_jsonl(fp))
    return corpus


# --------------------------------------------------------------- pool ------
def effective_cap(avail: dict, n: int, base_cap: int) -> int:
    """Smallest cap level L >= base_cap with sum(min(L, a)) >= n.
    Returns base_cap when it already suffices, and max(avail) when even
    taking everything cannot reach n."""
    if sum(min(base_cap, a) for a in avail.values()) >= n:
        return base_cap
    lo, hi = base_cap, max(avail.values())
    if sum(avail.values()) <= n:
        return hi
    while lo < hi:
        mid = (lo + hi) // 2
        if sum(min(mid, a) for a in avail.values()) >= n:
            hi = mid
        else:
            lo = mid + 1
    return lo


def build_pool(corpus, rng, meta):
    by_app = defaultdict(lambda: defaultdict(list))     # app -> market -> rows
    for r in corpus:
        by_app[r["app_id"]][r["market"]].append(r)

    avail = {a: sum(len(v) for v in mk.values()) for a, mk in by_app.items()}
    cap = effective_cap(avail, config.POOL_N, config.PER_GAME_CAP)
    quota = {a: min(cap, n) for a, n in avail.items()}

    # trim the overshoot (water level is integral) from capped apps,
    # deterministically by app_id; or scale down if base cap overshot
    excess = sum(quota.values()) - config.POOL_N
    if excess > 0:
        for a in sorted(q for q in quota if quota[q] == cap):
            if excess == 0:
                break
            quota[a] -= 1
            excess -= 1
        if excess > 0:                                  # base cap already > N
            scale = config.POOL_N / sum(quota.values())
            quota = {a: max(1, int(q * scale)) for a, q in quota.items()}

    pool = []
    for app_id in sorted(by_app):                        # deterministic order
        markets = by_app[app_id]
        q_app, n_app = quota[app_id], avail[app_id]
        # proportional split across this game's markets (largest remainder)
        share = {m: q_app * len(rows) / n_app for m, rows in markets.items()}
        take = {m: int(s) for m, s in share.items()}
        for m in sorted(share, key=lambda m: share[m] - take[m], reverse=True):
            if sum(take.values()) >= q_app:
                break
            take[m] += 1
        for m in sorted(markets):
            rows, k = markets[m], min(take[m], len(markets[m]))
            chosen = rng.sample(rows, k) if k < len(rows) else list(rows)
            w = len(rows) / k if 0 < k < len(rows) else 1.0
            for r in chosen:
                pool.append(to_output_row(
                    r, meta, stratum="pool",
                    extra={"sample_weight": round(w, 6)}))
    return pool, cap


# -------------------------------------------------------------- pilots -----
def build_pilot_random(corpus, rng, meta):
    n = min(config.PILOT_RANDOM_N, len(corpus))
    return [to_output_row(r, meta, stratum="random")
            for r in rng.sample(corpus, n)]


def build_pilot_targeted(corpus, rng, meta):
    if not config.PILOT_RANDOM_JSONL.exists():
        raise SystemExit("pilot_random.jsonl missing — run `python sample.py` "
                         "first so the targeted set can be deduped against it")
    used = {r["review_id"] for r in read_jsonl(config.PILOT_RANDOM_JSONL)}

    kw_pat = {k: re.compile(re.escape(k), re.IGNORECASE)
              for k in config.TARGET_KEYWORDS}
    cands = {k: [] for k in config.TARGET_KEYWORDS}
    for r in corpus:
        for k, pat in kw_pat.items():
            if pat.search(r["text"]):
                cands[k].append(r)
    for k in cands:
        cands[k].sort(key=lambda r: r["review_id"])      # order-independent
        rng.shuffle(cands[k])

    out, ptr, exhausted = [], {k: 0 for k in cands}, set()
    while len(out) < config.PILOT_TARGETED_N and len(exhausted) < len(cands):
        for k in config.TARGET_KEYWORDS:                 # round-robin
            if len(out) >= config.PILOT_TARGETED_N or k in exhausted:
                continue
            while ptr[k] < len(cands[k]):
                r = cands[k][ptr[k]]
                ptr[k] += 1
                if r["review_id"] not in used:
                    used.add(r["review_id"])
                    out.append(to_output_row(r, meta, stratum="targeted",
                                             seed_keyword=k))
                    break
            else:
                exhausted.add(k)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--targeted", action="store_true",
                    help="build pilot_targeted.jsonl (run after the random "
                         "pilot is labeled); pool/pilot_random are skipped")
    args = ap.parse_args()

    config.ensure_dirs()
    meta = load_app_meta()
    corpus = load_corpus()

    if args.targeted:
        pt = build_pilot_targeted(corpus, rng_for("targeted"), meta)
        write_jsonl_atomic(config.PILOT_TARGETED_JSONL, pt)
        per_kw = defaultdict(int)
        for r in pt:
            per_kw[r["seed_keyword"]] += 1
        print(f"\npilot_targeted: {len(pt)} rows ({len(per_kw)} keywords hit)")
        for k in config.TARGET_KEYWORDS:
            if per_kw[k]:
                print(f"    {k:<14} {per_kw[k]}")
        return

    pool, cap = build_pool(corpus, rng_for("pool"), meta)
    write_jsonl_atomic(config.POOL_JSONL, pool)

    pr = build_pilot_random(corpus, rng_for("random"), meta)
    write_jsonl_atomic(config.PILOT_RANDOM_JSONL, pr)

    n_capped = sum(1 for r in pool if r["sample_weight"] != 1.0)
    print(f"\npool:         {len(pool):,} rows -> {config.POOL_JSONL}")
    print(f"effective per-game cap: {cap:,} "
          f"(baseline {config.PER_GAME_CAP}; water-filled to reach "
          f"{config.POOL_N:,})" if cap != config.PER_GAME_CAP else
          f"per-game cap: {cap:,}")
    print(f"rows with sample_weight > 1 (truncated strata): {n_capped:,}")
    print(f"pilot_random: {len(pr)} rows")
    print("targeted pilot NOT built — run `python sample.py --targeted` "
          "when ready")


if __name__ == "__main__":
    main()