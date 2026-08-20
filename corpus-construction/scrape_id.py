"""
scrape_play_ids.py — pull Google Play appIds by scraping the store's
search page and app-detail page HTML directly (no google_play_scraper
library). This sidesteps the "top hit has no appId" parsing gap we hit
in resolve_ids.py, since the id is read straight off the
/store/apps/details?id=... link, and the title is read straight off
the detail page's own metadata instead of a search-result card.

For each (title_raw, market_listed) row in games.csv:
  1. GET the Play Store search results page for that title/market.
  2. Pull every /store/apps/details?id=... link out of the raw HTML,
     in the order they appear, and dedupe.
  3. Take the FIRST id — no ranking, mirrors resolve_ids_simple.py.
  4. GET that app's detail page and read its canonical title from the
     page metadata.
  5. Score title_raw against the canonical title and flag low-confidence
     / no-result rows via needs_review (same convention as the other
     resolve scripts in this project).

Writes games_with_ids.csv = games.csv + id, matched_title, match_score,
needs_review, scrape_notes.

Caches (ids, canonical_title) per (title, market) in
cache/scrape_cache.json so reruns don't re-hit Play for rows you've
already resolved. Delete that file (or the specific key) to force a
re-scrape of a row.

RELIABILITY NOTES:
  - Play sometimes shows an EU/UK cookie-consent interstitial instead of
    real results. We send a CONSENT cookie to skip it; if Google changes
    that mechanism this will need updating.
  - Play's HTML is not a stable public API and can change without
    notice. If this stops finding ids/titles, inspect a fresh page
    source and adjust SEARCH_LINK_RE / TITLE_META_RE / OGTITLE_RE below.
  - This hits Play's website directly rather than an official API — keep
    REQUEST_DELAY_SEC reasonable so you don't get temporarily rate
    limited or blocked.

Run:  python scrape_play_ids.py
"""
import csv
import json
import re
import time
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import quote

import requests
from tqdm import tqdm

GAMES_CSV = Path("games.csv")
OUT_CSV = Path("games_with_ids.csv")
CACHE_PATH = Path("cache/scrape_cache.json")

FUZZY_THRESHOLD = 0.72
REQUEST_DELAY_SEC = 1.5
MAX_RETRIES = 3
BACKOFF_BASE = 2

HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/124.0 Safari/537.36"),
    "Accept-Language": "en-US,en;q=0.9",
    # skips the EU/UK cookie-consent interstitial page
    "Cookie": "CONSENT=YES+cb.20240101-00-p0.en+FX+000",
}

SEARCH_LINK_RE = re.compile(r'/store/apps/details\?id=([A-Za-z0-9_.]+)')
TITLE_META_RE = re.compile(r'<meta content="([^"]*)" itemprop="name"')
OGTITLE_RE = re.compile(r'<meta property="og:title" content="([^"]*)"')
OGTITLE_SUFFIX_RE = re.compile(r"\s*-\s*Apps? on Google Play\s*$", re.IGNORECASE)


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


def _get(url: str) -> str:
    for attempt in range(MAX_RETRIES):
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code == 200:
                return r.text
            tqdm.write(f"  HTTP {r.status_code} for {url}")
        except requests.RequestException as e:
            tqdm.write(f"  request failed for {url}: {e}")
        time.sleep(BACKOFF_BASE ** attempt)
    return ""


def search_ids(title: str, market: str) -> list:
    """Ordered, deduped list of appIds found on the search results page."""
    url = (f"https://play.google.com/store/search?q={quote(title)}"
           f"&c=apps&gl={market}&hl=en")
    html = _get(url)
    if not html:
        return []
    seen, ids = set(), []
    for m in SEARCH_LINK_RE.finditer(html):
        app_id = m.group(1)
        if app_id not in seen:
            seen.add(app_id)
            ids.append(app_id)
    return ids


def fetch_canonical_title(app_id: str, market: str) -> str:
    url = f"https://play.google.com/store/apps/details?id={app_id}&gl={market}&hl=en"
    html = _get(url)
    if not html:
        return ""
    m = TITLE_META_RE.search(html)
    if m:
        return m.group(1).strip()
    m = OGTITLE_RE.search(html)
    if m:
        return OGTITLE_SUFFIX_RE.sub("", m.group(1)).strip()
    return ""


def load_cache() -> dict:
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict):
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, indent=2, ensure_ascii=False),
                          encoding="utf-8")


def main():
    with GAMES_CSV.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    cache = load_cache()
    out_rows = []
    n_review = 0
    n_nomatch = 0

    for row in tqdm(rows, desc="scraping Play Store"):
        title = row["title_raw"].strip()
        market = row["market_listed"].strip().lower()
        key = f"{market}::{title}"

        if key in cache:
            ids = cache[key]["ids"]
            canon_title = cache[key]["canon_title"]
        else:
            ids = search_ids(title, market)
            canon_title = fetch_canonical_title(ids[0], market) if ids else ""
            cache[key] = {"ids": ids, "canon_title": canon_title}
            save_cache(cache)
            time.sleep(REQUEST_DELAY_SEC)

        out = dict(row)
        if not ids:
            out.update(id="", matched_title="", match_score="0.000",
                       needs_review=1, scrape_notes="NO RESULTS from Play search")
            n_nomatch += 1
        else:
            app_id = ids[0]      # first result, no ranking — as requested
            score = similarity(title, canon_title)
            needs_review, notes = 0, []
            if score < FUZZY_THRESHOLD:
                needs_review = 1
                notes.append(f"low score {score:.2f}")
            if not canon_title:
                needs_review = 1
                notes.append("couldn't read canonical title from detail page")
            out.update(id=app_id, matched_title=canon_title,
                       match_score=f"{score:.3f}", needs_review=needs_review,
                       scrape_notes="; ".join(notes))
            n_review += needs_review
        out_rows.append(out)

    fieldnames = list(rows[0].keys()) + ["id", "matched_title", "match_score",
                                          "needs_review", "scrape_notes"]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out_rows)

    print(f"\nwrote {len(out_rows)} rows to {OUT_CSV}")
    print(f"needs_review: {n_review}")
    print(f"no results at all: {n_nomatch}")


if __name__ == "__main__":
    main()