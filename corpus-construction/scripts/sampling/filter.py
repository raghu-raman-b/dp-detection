"""Stage 2 — filter the raw corpus. STAGE ORDER MATTERS and is logged.

Cascade (survivor counts per stage per app×market go to filter_log.csv,
feeding the PRISMA-style flow figure):

  0. scraped          (input)
  1. english          language filter (langdetect, seeded)
  2. min_words        length floor: >= config.MIN_WORDS whitespace tokens
  3. exact_dedup      normalized-text hash, GLOBAL across the corpus
  4. near_dedup       MinHash/LSH at ~0.9 Jaccard, GLOBAL, keep first
  5. cleaned          strip HTML entities/markup ONLY (emojis, punctuation,
                      casing preserved; no stopword removal, no lemmatization)

"Keep first occurrence" is made deterministic by processing files in
sorted filename order and reviews in file order. Cleaning (5) happens
last so dedup operates on near-original text; cleaning never drops rows.

Idempotent: full deterministic recompute; outputs are rewritten atomically.

Run:  python filter.py
"""
import hashlib
import html
import re
from collections import defaultdict

from tqdm import tqdm
from datasketch import MinHash, MinHashLSH
from langdetect import DetectorFactory, detect, LangDetectException

import config
from utils import read_jsonl, write_csv_atomic, write_json_atomic, write_jsonl_atomic

DetectorFactory.seed = config.LANGDETECT_SEED

STAGES = ["scraped", "english", "min_words", "exact_dedup", "near_dedup"]
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def is_english(text: str) -> bool:
    try:
        return detect(text) == "en"
    except LangDetectException:
        return False


def norm_for_dedup(text: str) -> str:
    return WS_RE.sub(" ", text.lower()).strip()


def exact_hash(text: str) -> str:
    return hashlib.sha1(norm_for_dedup(text).encode("utf-8")).hexdigest()


def minhash_of(text: str) -> MinHash:
    words = norm_for_dedup(text).split()
    k = config.SHINGLE_SIZE
    shingles = ({" ".join(words[i:i + k]) for i in range(len(words) - k + 1)}
                if len(words) >= k else set(words))
    m = MinHash(num_perm=config.MINHASH_NUM_PERM)
    for s in shingles:
        m.update(s.encode("utf-8"))
    return m


def clean_text(text: str) -> str:
    """HTML entities/markup only. Emojis, punctuation, casing untouched."""
    text = html.unescape(text)
    text = TAG_RE.sub(" ", text)
    return WS_RE.sub(" ", text).strip()


def main():
    config.ensure_dirs()
    files = sorted(config.RAW_DIR.glob("*.jsonl"))
    if not files:
        raise SystemExit("no raw/*.jsonl files — run scrape.py first")

    counts = defaultdict(lambda: {s: 0 for s in STAGES})   # (app,market) -> stage counts
    seen_hashes: set[str] = set()
    lsh = MinHashLSH(threshold=config.NEAR_DUP_JACCARD,
                     num_perm=config.MINHASH_NUM_PERM)
    lsh_i = 0

    for fp in tqdm(files, desc="filtering files"):
        survivors = []
        key = None
        for r in read_jsonl(fp):
            key = (r["app_id"], r["market"])
            c = counts[key]
            c["scraped"] += 1
            text = r.get("text") or ""

            if not is_english(text):                          # 1
                continue
            c["english"] += 1

            if len(text.split()) < config.MIN_WORDS:          # 2
                continue
            c["min_words"] += 1

            h = exact_hash(text)                              # 3
            if h in seen_hashes:
                continue
            seen_hashes.add(h)
            c["exact_dedup"] += 1

            m = minhash_of(text)                              # 4
            if lsh.query(m):
                continue
            lsh.insert(f"r{lsh_i}", m)
            lsh_i += 1
            c["near_dedup"] += 1

            r = dict(r)
            r["text"] = clean_text(text)                      # 5
            survivors.append(r)

        if key is not None:
            out = config.FILTERED_DIR / fp.name
            write_jsonl_atomic(out, survivors)

    # ---- logs -------------------------------------------------------------
    log_rows = []
    for (app_id, market), c in sorted(counts.items()):
        row = {"app_id": app_id, "market": market}
        row.update(c)
        log_rows.append(row)
    write_csv_atomic(config.FILTER_LOG, ["app_id", "market"] + STAGES, log_rows)

    stats = {
        "stage_totals": {s: sum(c[s] for c in counts.values()) for s in STAGES},
        "per_app": {},
        "per_market": {m: {s: 0 for s in STAGES} for m in config.MARKETS},
    }
    for (app_id, market), c in counts.items():
        app = stats["per_app"].setdefault(app_id, {s: 0 for s in STAGES})
        for s in STAGES:
            app[s] += c[s]
            stats["per_market"][market][s] += c[s]
    write_json_atomic(config.CORPUS_STATS, stats)

    t = stats["stage_totals"]
    print("\nsurvivors per stage (corpus totals):")
    for s in STAGES:
        print(f"  {s:<12} {t[s]:>10,}")
    print(f"\nlogs: {config.FILTER_LOG}, {config.CORPUS_STATS}")


if __name__ == "__main__":
    main()
