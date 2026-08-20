"""Stage 1 — scrape up to N most-relevant English reviews per (app × market).

For every app in games_resolved.csv (needs_review must be 0) and every
market in config.MARKETS where the app is available, pull reviews in
batches of 200 via continuation tokens, sleeping between batches and
retrying with exponential backoff on errors.

Two-phase fill: Sort.MOST_RELEVANT first; if it runs dry before the
per-pair quota is reached, the scraper automatically switches to
Sort.NEWEST (fresh pagination) and tops up to the quota, deduping by
review_id across phases. Each row records sort_origin
("relevant"/"newest"), and scrape_log.csv reports n_relevant/n_newest
per app×market.

Resumable: after every batch the continuation token is pickled to
state/{app_id}_{market}.pkl and rows are appended to
raw/{app_id}_{market}.jsonl. Killing and re-running continues where it
left off; finished pairs are skipped. Per-file counts go to
scrape_log.csv (idempotent upserts, one row per app×market).

Run:  python scrape.py
"""
import csv
import pickle
import time

from tqdm import tqdm
from google_play_scraper import app as gp_app, reviews as gp_reviews, Sort
from google_play_scraper.exceptions import NotFoundError

import config
from utils import append_jsonl, count_lines, read_jsonl, upsert_csv_row

LOG_FIELDS = ["app_id", "market", "status", "n_reviews",
              "n_relevant", "n_newest", "finished_utc"]

# scrape phases: exhaust MOST_RELEVANT first, then top up with NEWEST
PHASES = [("relevant", Sort.MOST_RELEVANT), ("newest", Sort.NEWEST)]


def state_path(app_id, market):
    return config.STATE_DIR / f"{app_id}_{market}.pkl"


def raw_path(app_id, market):
    return config.RAW_DIR / f"{app_id}_{market}.jsonl"


def load_state(app_id, market):
    p = state_path(app_id, market)
    if p.exists():
        with open(p, "rb") as f:
            st = pickle.load(f)
        # migrate pre-phase state files from earlier runs
        st.setdefault("phase", "relevant")
        st.setdefault("phase_counts", {"relevant": st.get("count", 0),
                                       "newest": 0})
        return st
    return {"token": None, "count": 0, "done": False,
            "phase": "relevant", "phase_counts": {"relevant": 0, "newest": 0}}


def save_state(app_id, market, st):
    with open(state_path(app_id, market), "wb") as f:
        pickle.dump(st, f)


def log_row(app_id, market, status, st):
    pc = st.get("phase_counts", {})
    upsert_csv_row(config.SCRAPE_LOG, LOG_FIELDS, ["app_id", "market"], {
        "app_id": app_id, "market": market, "status": status,
        "n_reviews": st["count"],
        "n_relevant": pc.get("relevant", 0),
        "n_newest": pc.get("newest", 0),
        "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    })


def app_available(app_id, market) -> bool:
    for attempt in range(config.MAX_RETRIES):
        try:
            gp_app(app_id, lang=config.REVIEW_LANG, country=market)
            return True
        except NotFoundError:
            return False
        except Exception as e:
            wait = config.BACKOFF_BASE ** attempt
            tqdm.write(f"  availability check failed ({app_id}, {market}): {e} — retry {wait:.0f}s")
            time.sleep(wait)
    return False  # persistent errors: treat as unavailable, logged below


def fetch_batch(app_id, market, token, sort):
    """One reviews() call with exponential-backoff retries."""
    last_err = None
    for attempt in range(config.MAX_RETRIES):
        try:
            return gp_reviews(
                app_id,
                lang=config.REVIEW_LANG,
                country=market,
                sort=sort,
                count=config.BATCH_SIZE,
                continuation_token=token,
            )
        except Exception as e:
            last_err = e
            wait = config.BACKOFF_BASE ** attempt
            tqdm.write(f"  batch failed ({app_id}, {market}): {e} — retry in {wait:.0f}s")
            time.sleep(wait)
    raise RuntimeError(f"giving up on {app_id}/{market}: {last_err}")


def scrape_pair(app_id, market, pbar):
    rp = raw_path(app_id, market)
    st = load_state(app_id, market)

    # reconcile state with what is actually on disk (torn writes etc.)
    on_disk = count_lines(rp)
    if on_disk < st["count"]:
        st["count"] = on_disk
        st["token"] = None if on_disk == 0 else st["token"]
    seen_ids = {r["review_id"] for r in read_jsonl(rp)} if on_disk else set()

    if st["done"] or st["count"] >= config.REVIEWS_PER_APP_MARKET:
        log_row(app_id, market, "done", st)
        return

    if not app_available(app_id, market):
        log_row(app_id, market, "unavailable", st)
        st["done"] = True
        save_state(app_id, market, st)
        return

    # resume in whatever phase we were in; phases run in PHASES order
    phase_names = [p for p, _ in PHASES]
    sorts = dict(PHASES)
    phase_idx = phase_names.index(st.get("phase", "relevant"))

    while st["count"] < config.REVIEWS_PER_APP_MARKET and phase_idx < len(PHASES):
        phase = phase_names[phase_idx]
        batch, token = fetch_batch(app_id, market, st["token"], sorts[phase])
        rows = []
        for r in batch:
            rid = str(r["reviewId"])
            if rid in seen_ids:          # also dedupes NEWEST vs RELEVANT overlap
                continue
            seen_ids.add(rid)
            rows.append({
                "review_id": rid,
                "app_id": app_id,
                "market": market,
                "text": r.get("content") or "",
                "rating": r.get("score"),
                "date": r["at"].isoformat() if r.get("at") else None,
                "thumbs_up": r.get("thumbsUpCount", 0),
                "sort_origin": phase,
            })
        room = config.REVIEWS_PER_APP_MARKET - st["count"]
        rows = rows[:room]
        append_jsonl(rp, rows)
        st["count"] += len(rows)
        st["phase_counts"][phase] = st["phase_counts"].get(phase, 0) + len(rows)
        st["token"] = token
        pbar.set_postfix_str(f"{app_id[:32]}/{market}: {st['count']} [{phase}]")

        exhausted = (token is None or getattr(token, "token", None) is None
                     or not batch)
        if exhausted:
            # current sort ran dry: switch to the next phase automatically
            phase_idx += 1
            if phase_idx < len(PHASES) and st["count"] < config.REVIEWS_PER_APP_MARKET:
                st["phase"] = phase_names[phase_idx]
                st["token"] = None       # fresh pagination for the new sort
                tqdm.write(f"  {app_id}/{market}: '{phase}' exhausted at "
                           f"{st['count']} — switching to '{st['phase']}'")
            else:
                st["done"] = True
        save_state(app_id, market, st)
        if st["done"]:
            break
        time.sleep(config.SLEEP_BETWEEN_BATCHES)

    if st["count"] >= config.REVIEWS_PER_APP_MARKET or phase_idx >= len(PHASES):
        st["done"] = True
        save_state(app_id, market, st)
    log_row(app_id, market, "done", st)


def main():
    config.ensure_dirs()
    if not config.RESOLVED_CSV.exists():
        raise SystemExit("games_resolved.csv missing — run resolve_ids.py first")
    with open(config.RESOLVED_CSV, encoding="utf-8", newline="") as f:
        apps = list(csv.DictReader(f))

    pending_review = [a for a in apps if str(a["needs_review"]) == "1"]
    if pending_review:
        print("REFUSING to scrape while needs_review rows remain unverified:")
        for a in pending_review:
            print(f"  - {a['canonical_title']} ({a['app_id']})")
        raise SystemExit("hand-verify these in games_resolved.csv, set needs_review=0, re-run")

    pairs = [(a["app_id"], m) for a in apps for m in a["markets"].split(";")]
    with tqdm(pairs, desc="scraping app×market") as pbar:
        for app_id, market in pbar:
            scrape_pair(app_id, market, pbar)
    print(f"\ndone — per-file counts in {config.SCRAPE_LOG}")


if __name__ == "__main__":
    main()
