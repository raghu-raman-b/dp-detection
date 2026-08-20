"""Central configuration for the Play-review corpus pipeline.

Every tunable constant lives here so the paper's methodology section can
cite a single file. All scripts import from this module only.
"""
from pathlib import Path

# ---------------------------------------------------------------- paths ----
ROOT = Path(__file__).resolve().parent
GAMES_CSV = ROOT / "games.csv"
RESOLVED_CSV = ROOT / "games_resolved.csv"
RESOLVE_CACHE = ROOT / "cache" / "resolve_cache.json"

RAW_DIR = ROOT / "raw"                 # raw/{app_id}_{market}.jsonl
STATE_DIR = ROOT / "state"             # scrape resume state (pickled tokens)
FILTERED_DIR = ROOT / "filtered"       # filtered/{app_id}_{market}.jsonl
SAMPLES_DIR = ROOT / "samples"

SCRAPE_LOG = ROOT / "scrape_log.csv"
FILTER_LOG = ROOT / "filter_log.csv"
CORPUS_STATS = ROOT / "corpus_stats.json"

POOL_JSONL = SAMPLES_DIR / "pool.jsonl"
PILOT_RANDOM_JSONL = SAMPLES_DIR / "pilot_random.jsonl"
PILOT_TARGETED_JSONL = SAMPLES_DIR / "pilot_targeted.jsonl"

# ------------------------------------------------------------- stage 0 -----
MARKETS = ["us", "in", "gb"]
SEARCH_N_HITS = 3                 # candidates fetched per Play search
FUZZY_THRESHOLD = 0.80            # title similarity below this -> needs_review

# ------------------------------------------------------------- stage 1 -----
REVIEWS_PER_APP_MARKET = 5000
BATCH_SIZE = 200
SLEEP_BETWEEN_BATCHES = 1.0       # seconds
MAX_RETRIES = 5
BACKOFF_BASE = 2.0                # sleep = BACKOFF_BASE ** attempt
REVIEW_LANG = "en"

# ------------------------------------------------------------- stage 2 -----
MIN_WORDS = 10                    # length floor (whitespace tokens)
NEAR_DUP_JACCARD = 0.90           # MinHash/LSH threshold
MINHASH_NUM_PERM = 128
SHINGLE_SIZE = 3                  # word n-gram size for MinHash shingles
LANGDETECT_SEED = 0               # langdetect is stochastic; pin it

# ------------------------------------------------------------- stage 3 -----
RNG_SEED = 42
POOL_N = 200_000
PER_GAME_CAP = 800                # max reviews per app_id in the pool
PILOT_RANDOM_N = 300
PILOT_TARGETED_N = 20
# ---------------------------------------------------------------- 20 slots
# ---------------------------------------------------------------- FS/I
FOMO_R2 = [
    # A. named anxiety about missing (highest precision)
    "fomo", "fear of missing out", "afraid to miss", "scared to miss",
    "afraid ill miss", "worried ill miss", "anxious about missing",
    "stressed about missing", "guilty if i dont play", "guilty if i miss",
    "feel guilty when i", "feel obligated to log in", "feel obligated to play",
    "cant relax", "can't relax", "cant enjoy a day off", "stresses me out to miss",
    "makes me anxious", "gives me anxiety", "dread missing",
    # B. compulsion to return or continue
    "cant stop checking", "can't stop checking", "have to check the game",
    "have to log in every", "have to play every day or", "cant take a break",
    "can't take a break", "cant go on holiday", "afraid to stop playing",
    "scared to stop playing", "if i stop playing i", "if i quit i lose",
    "cant take a day off", "wake up to collect", "set an alarm to",
    # C. falling behind other players
    "fall behind", "falling behind", "left behind", "cant catch up",
    "can't catch up", "never catch up", "impossible to catch up",
    "everyone else will be ahead", "everyone else is ahead",
    "keep up with everyone", "keeping up with the top", "lose my rank if",
    "lose my place if", "drop down the leaderboard", "lose my spot",
    "lose my streak if", "break my streak", "ruin my streak",
    # D. closing window WITH felt pressure (triage — see note)
    "last chance to get", "wont get another chance", "won't get another chance",
    "never available again", "if you miss the event", "miss out on the",
    "before its gone", "before it's gone", "only chance to get",
    "pressure to buy before", "rush to finish before",
]
TARGET_KEYWORDS = FOMO_R2
def ensure_dirs():
    for d in (RAW_DIR, STATE_DIR, FILTERED_DIR, SAMPLES_DIR, RESOLVE_CACHE.parent):
        d.mkdir(parents=True, exist_ok=True)
