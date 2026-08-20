"""Stage 0.5 — verify scraped app_ids via the google_play_scraper API.

Takes games_with_ids.csv (output of scrape_play_ids.py: one row per
title_raw x market_listed, with an `id` column holding whatever appId
the raw-HTML scraper found) and verifies each id against Google Play's
own app-detail API (google_play_scraper.app()) instead of trusting the
scraper's guess. This is a direct id -> app lookup, not a search, so
there's no ranking or ambiguity involved — either the id resolves to a
real app or it doesn't, and either way we compare its *current* title
against title_raw.

Output is games_resolved.csv-compatible: identical columns, identical
aggregation by app_id across markets, identical needs_review
convention (0 = clean, 1 = a human should look), so scrape.py can
consume it unchanged — no pipeline changes needed downstream.

needs_review is set to 1 when:
  - the id was empty/missing to begin with (scraper found nothing)
  - the app() lookup 404s (NotFoundError) — the scraped id was wrong
  - the API's title doesn't match title_raw closely enough
    (score < FUZZY_THRESHOLD)
  - the row's original notes say "verify"
  - COLLISION GUARD: two different title_raws resolved to the same
    app_id

Also writes verified entries into cache/resolve_cache.json using the
same v2::market::title key format resolve_ids.py uses (one-candidate
list, since this is a lookup not a search), so a later run of
resolve_ids.py / resolve_ids_simple.py can reuse this already-verified
result instead of re-searching Play for the same title.

Run:  python verify_ids.py
"""
import csv
import json
import re
import time
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

from tqdm import tqdm
from google_play_scraper import app as gp_app
from google_play_scraper.exceptions import NotFoundError

import config
from utils import write_csv_atomic, write_json_atomic

# where scrape_play_ids.py wrote its output
IDS_CSV = getattr(config, "IDS_CSV", Path("games_with_ids.csv"))


def normalize_title(t: str) -> str:
    t = re.sub(r"[\u2122\u00ae\u00a9]", "", t)
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.lower()
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    t = re.sub(r"(?<=[a-z])(?=[0-9])|(?<=[0-9])(?=[a-z])", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def similarity(a: str, b: str) -> float:
    na, nb = normalize_title(a), normalize_title(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    seq = SequenceMatcher(None, na, nb).ratio()
    tok = SequenceMatcher(None, " ".join(sorted(na.split())),
                          " ".join(sorted(nb.split()))).ratio()
    return max(seq, tok)


def load_cache() -> dict:
    if config.RESOLVE_CACHE.exists():
        with open(config.RESOLVE_CACHE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def verify_app(app_id: str, market: str):
    """Direct id -> app lookup. Returns (title, developer) or None if the
    id doesn't resolve (NotFoundError) after retries on transient errors."""
    for attempt in range(config.MAX_RETRIES):
        try:
            info = gp_app(app_id, lang=config.REVIEW_LANG, country=market)
            return info.get("title", ""), info.get("developer", "")
        except NotFoundError:
            return None
        except Exception as e:
            wait = config.BACKOFF_BASE ** attempt
            tqdm.write(f"  app lookup failed ({app_id}, {market}): {e} — retry {wait:.0f}s")
            time.sleep(wait)
    return None


def main():
    config.ensure_dirs()
    if not IDS_CSV.exists():
        raise SystemExit(f"{IDS_CSV} missing — run scrape_play_ids.py first")
    with open(IDS_CSV, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    cache = load_cache()
    resolved: dict[str, dict] = {}
    unmatched: list[dict] = []

    for row in tqdm(rows, desc="verifying ids"):
        title = row["title_raw"].strip()
        market = row["market_listed"].strip().lower()
        casino = int(row.get("casino") or 0)
        notes = (row.get("notes") or "").strip()
        app_id = (row.get("id") or "").strip()

        if market not in config.MARKETS:
            raise ValueError(f"unknown market {market!r} for {title!r}")

        if not app_id:
            unmatched.append({"title_raw": title, "market": market,
                              "note": "scraper found no id"})
            continue

        info = verify_app(app_id, market)
        time.sleep(config.SLEEP_BETWEEN_BATCHES)
        if info is None:
            unmatched.append({"title_raw": title, "market": market,
                              "note": f"appId '{app_id}' not found via API"})
            continue

        api_title, api_dev = info
        needs_review, flags = 0, []
        score = similarity(title, api_title)
        if score < config.FUZZY_THRESHOLD:
            needs_review = 1
            flags.append(f"low score {score:.2f}")
        if "verify" in notes.lower():
            needs_review = 1

        # cache this verified id in the same v2 format resolve_ids.py
        # uses (a one-candidate list), keyed by the ORIGINAL query title
        # so future resolve_ids.py / resolve_ids_simple.py runs for the
        # same title reuse this verified result instead of re-searching
        cache_key = f"v2::{market}::{title}"
        cache[cache_key] = [{"appId": app_id, "title": api_title, "developer": api_dev}]
        write_json_atomic(config.RESOLVE_CACHE, cache)

        rec = resolved.setdefault(app_id, {
            "app_id": app_id,
            "canonical_title": api_title,
            "developer": api_dev,
            "markets": set(), "casino": 0,
            "title_raws": set(), "match_score": 1.0,
            "needs_review": 0, "notes": set(),
        })
        # COLLISION GUARD: same app claimed by a different raw title
        for prior_raw in rec["title_raws"]:
            if prior_raw != title:
                needs_review = 1
                rec["needs_review"] = 1
                flags.append(f"also matched by raw '{prior_raw}'")
        rec["title_raws"].add(title)
        rec["markets"].add(market)
        rec["casino"] = max(rec["casino"], casino)
        rec["needs_review"] = max(rec["needs_review"], needs_review)
        rec["match_score"] = min(rec["match_score"], score)
        if notes:
            rec["notes"].add(notes)
        if flags:
            rec["notes"].add("FLAG: " + "; ".join(flags))

    out = []
    for rec in resolved.values():
        out.append({
            "app_id": rec["app_id"],
            "canonical_title": rec["canonical_title"],
            "developer": rec["developer"],
            "markets": ";".join(sorted(rec["markets"])),
            "casino": rec["casino"],
            "title_raw": ";".join(sorted(rec["title_raws"])),
            "match_score": f"{rec['match_score']:.3f}",
            "needs_review": rec["needs_review"],
            "notes": " | ".join(sorted(rec["notes"])),
        })
    out.sort(key=lambda r: r["canonical_title"].lower())
    write_csv_atomic(config.RESOLVED_CSV,
                     ["app_id", "canonical_title", "developer", "markets",
                      "casino", "title_raw", "match_score", "needs_review",
                      "notes"], out)

    n_review = sum(r["needs_review"] for r in resolved.values())
    print(f"\nverified {len(resolved)} unique apps from {len(rows)} csv rows")
    print(f"needs_review: {n_review}  (hand-verify these before running scrape.py)")
    if unmatched:
        print(f"NO VERIFIED MATCH for {len(unmatched)} rows — fix and re-run:")
        for u in unmatched:
            print(f"  - {u['title_raw']} [{u['market']}]: {u['note']}")


if __name__ == "__main__":
    main()