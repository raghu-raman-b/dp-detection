#!/usr/bin/env python3
"""
web_search_tool.py -- a web-search tool for teacher runners whose provider has none.

    python web_search_tool.py "what is a welkin pass in Genshin Impact"
    python web_search_tool.py --backend stub "anything"        # offline, no key

DeepSeek ships no web search at any tier, but the teacher prompt's R10 grants every
provider one search per review to resolve a term the reviewer used ("welkin", "battle
pass", "pity"). This module is that capability, as a plain function-calling tool: a
runner declares tool_spec(), and when the model calls it, execute() answers.

What the model gets back is deliberately SHORT -- an answer paragraph plus the hosts it
came from, capped at MAX_ANSWER_CHARS. A search result is context for a labelling
decision, not reading material; a full SERP dump would cost more tokens than the review
it is helping to label and would bury the review text in the middle of the context.

Nothing here is DeepSeek-specific. It is a standalone module with its own CLI, so the
search half can be debugged without spending a cent of model budget.

Three properties that matter for the bake-off, not just for cost:

  1. ANSWERS ARE CACHED ON DISK, keyed by the normalised query. The same term recurs
     across reviews and across providers, so most searches after the first are free --
     but the real reason is replayability: re-running a review next month feeds the
     model the byte-identical string it saw the first time. A live search is a moving
     target and would make a re-run unreproducible.
  2. EVERY CALL IS AUDITED to audit.jsonl -- the query the model generated, the query
     actually sent, the answer returned, and the sources. The paper has to be able to
     say what the teacher was shown, and "the model searched something" is not that.
  3. THE BACKEND IS PLUGGABLE and named in every record. Swapping engines must never
     silently reuse another engine's cached answer, so the backend is part of the key.

On backends: Tavily is the default because its /search returns a written `answer`
field, so no second model sits in the measurement path assembling one. The raw-SERP
backends (brave, serper) join the top snippets locally instead. A local LLM summariser
is deliberately NOT offered -- it would put an extra, separately-versioned model between
the web and the teacher, which is exactly the confound the audit trail exists to avoid.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
import time
import unicodedata
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent))
import runner_common as rc

SCRIPT_DIR = Path(__file__).resolve().parent

# ============================== DEFAULTS ==============================
DEFAULT_BACKEND   = "tavily"
DEFAULT_CACHE_DIR = "../outputs/web-search-cache"
MAX_ANSWER_CHARS  = 480     # ~2-4 sentences. The cap the model's context actually feels.
MAX_SOURCES_SHOWN = 3       # hosts listed after the answer, so the model can cite one
DEFAULT_MAX_RESULTS = 5
TIMEOUT           = 20.0
RETRIES           = 3
ENV_FILE          = ".env"

# Which key each backend needs. Looked up through rc.load_api_key, same as the runners.
BACKEND_KEY_ENV = {
    "tavily": "TAVILY_API_KEY",
    "brave":  "BRAVE_API_KEY",
    "serper": "SERPER_API_KEY",
    "stub":   None,
}

# Glossary-shaped queries do better pinned to game wikis than to the open web, where
# storefront and SEO pages outrank them. Applied only when looks_glossary() agrees and
# pin_game_wikis is "auto" -- see the note there before widening this list.
GAME_WIKI_DOMAINS = ["fandom.com", "wiki.gg", "gamepedia.com", "fextralife.com"]
# ======================================================================


# ------------------------------------------------------------------ normalisation

_WS = re.compile(r"\s+")
_EDGE_PUNCT = re.compile(r"^[\W_]+|[\W_]+$", re.UNICODE)


def normalize(query: str) -> str:
    """The cache key's basis. Casing, padding and a trailing question mark are not
    different questions, and treating them as such would miss most of the hits that
    make a run cheap and replayable."""
    q = unicodedata.normalize("NFKC", query or "")
    q = _WS.sub(" ", q).strip().casefold()
    return _EDGE_PUNCT.sub("", q)


def query_hash(query: str, backend: str, max_results: int) -> str:
    """Backend is in the key on purpose: two engines answering the same question are
    not interchangeable evidence, and a silent cross-engine hit after a backend swap
    would be undetectable in the audit trail."""
    basis = f"{backend}|{max_results}|{normalize(query)}"
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()[:16]


def looks_glossary(query: str) -> bool:
    """Cheap heuristic for 'what does this game term mean', which is the only shape R10
    actually authorises a search for."""
    q = normalize(query)
    return q.startswith(("what is", "what are", "what does", "who is", "define")) \
        or len(q.split()) <= 8


def clip(text: str, limit: int = MAX_ANSWER_CHARS) -> str:
    """Truncate on a sentence boundary where there is one within reach, so the model is
    never handed half a clause."""
    text = _WS.sub(" ", (text or "").strip())
    if len(text) <= limit:
        return text
    cut = text[:limit]
    stop = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    return (cut[:stop + 1] if stop > limit * 0.5 else cut.rstrip()) + " ..."


def host_of(url: str) -> str:
    m = re.match(r"https?://([^/]+)", url or "")
    return (m.group(1) if m else "").removeprefix("www.")


# ---------------------------------------------------------------------- result

@dataclass
class SearchResult:
    """One search, everything the runner and the paper need to know about it."""
    query: str                          # exactly what the model generated
    sent_query: str                     # what actually went to the backend
    query_hash: str
    answer: str                         # what the model is shown. <= MAX_ANSWER_CHARS
    sources: list = field(default_factory=list)   # [{title, url, host}]
    backend: str = ""
    cached: bool = False                # served from disk => cost_usd == 0.0
    cost_usd: float = 0.0
    latency_s: float = 0.0
    n_results: int = 0
    domains: list = field(default_factory=list)   # include_domains, if pinned
    error: str | None = None
    ts: str = ""                        # when the LIVE search ran, not when replayed
    raw: dict = field(default_factory=dict)       # full payload, audit only

    def as_tool_content(self) -> str:
        """The exact string that becomes the tool message. Answer first, because that
        is the part the model needs; hosts second, so it can fill the prompt's
        search_result field with something real."""
        if self.error and not self.answer:
            return (f"Search failed ({self.error}). "
                    f"Answer from the review text alone.")
        hosts = []
        for s in self.sources[:MAX_SOURCES_SHOWN]:
            h = s.get("host") or host_of(s.get("url", ""))
            if h and h not in hosts:
                hosts.append(h)
        tail = f"\n(sources: {', '.join(hosts)})" if hosts else ""
        return self.answer + tail

    def audit_row(self, **extra) -> dict:
        row = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "query": self.query, "sent_query": self.sent_query,
               "query_hash": self.query_hash, "backend": self.backend,
               "cached": self.cached, "answer": self.answer,
               "n_results": self.n_results, "cost_usd": self.cost_usd,
               "domains": self.domains,
               "source_hosts": [s.get("host") for s in self.sources],
               "error": self.error}
        return row | extra


# --------------------------------------------------------------------- backends

class TavilyBackend:
    """Tavily returns a written `answer` alongside the results, which is why it is the
    default: the short answer the teacher needs already exists and no second model has
    to be introduced to produce one. Disclose in the paper that the answer text is
    Tavily-generated -- the raw results are kept in the audit trail either way."""
    name = "tavily"
    cost_per_search = 0.008          # 1 credit, PAYG rate; free tier is 1000/month
    url = "https://api.tavily.com/search"

    def run(self, key, query, *, domains, max_results, timeout) -> dict:
        body = {"query": query, "search_depth": "basic", "topic": "general",
                "include_answer": "basic", "max_results": max_results}
        if domains:
            body["include_domains"] = domains
        r = requests.post(self.url, json=body, timeout=timeout,
                          headers={"Authorization": f"Bearer {key}"})
        r.raise_for_status()
        return r.json()

    def to_answer(self, raw) -> tuple[str, list, int]:
        results = raw.get("results") or []
        srcs = [{"title": x.get("title", ""), "url": x.get("url", ""),
                 "host": host_of(x.get("url", ""))} for x in results]
        answer = raw.get("answer") or ""
        if not answer and results:      # answer can come back empty on a thin query
            answer = results[0].get("content", "")
        return clip(answer), srcs, len(results)


class BraveBackend:
    """Raw SERP. No written answer, so the top snippets are joined locally -- more
    tokens and rougher prose than Tavily, but nothing writes it except this function."""
    name = "brave"
    cost_per_search = 0.005
    url = "https://api.search.brave.com/res/v1/web/search"

    def run(self, key, query, *, domains, max_results, timeout) -> dict:
        q = query + "".join(f" site:{d}" for d in (domains or [])[:1])
        r = requests.get(self.url, timeout=timeout,
                         params={"q": q, "count": max_results},
                         headers={"X-Subscription-Token": key,
                                  "Accept": "application/json"})
        r.raise_for_status()
        return r.json()

    def to_answer(self, raw) -> tuple[str, list, int]:
        results = ((raw.get("web") or {}).get("results")) or []
        srcs = [{"title": x.get("title", ""), "url": x.get("url", ""),
                 "host": host_of(x.get("url", ""))} for x in results]
        joined = " ".join(re.sub(r"<[^>]+>", "", x.get("description", ""))
                          for x in results[:3])
        return clip(joined), srcs, len(results)


class SerperBackend:
    """Raw SERP, cheapest per query. Same local-join caveat as Brave."""
    name = "serper"
    cost_per_search = 0.001
    url = "https://google.serper.dev/search"

    def run(self, key, query, *, domains, max_results, timeout) -> dict:
        q = query + "".join(f" site:{d}" for d in (domains or [])[:1])
        r = requests.post(self.url, json={"q": q, "num": max_results}, timeout=timeout,
                          headers={"X-API-KEY": key, "Content-Type": "application/json"})
        r.raise_for_status()
        return r.json()

    def to_answer(self, raw) -> tuple[str, list, int]:
        results = raw.get("organic") or []
        srcs = [{"title": x.get("title", ""), "url": x.get("link", ""),
                 "host": host_of(x.get("link", ""))} for x in results]
        kg = (raw.get("knowledgeGraph") or {}).get("description", "")
        answer = kg or " ".join(x.get("snippet", "") for x in results[:3])
        return clip(answer), srcs, len(results)


class StubBackend:
    """No network, no key, no cost. Exists so --check is genuinely offline and so the
    DeepSeek tool loop can be exercised end to end without buying searches."""
    name = "stub"
    cost_per_search = 0.0

    def run(self, key, query, *, domains, max_results, timeout) -> dict:
        return {"stub": True, "query": query}

    def to_answer(self, raw) -> tuple[str, list, int]:
        return (f"[stub backend] No live search was performed for "
                f"{raw.get('query')!r}.", [], 0)


BACKENDS = {b.name: b for b in (TavilyBackend, BraveBackend, SerperBackend, StubBackend)}


# ------------------------------------------------------------------------ cache

class SearchCache:
    """Disk cache, one JSON file per (backend, normalised query, max_results).

    Never expires by default. That is the point: freshness is worth less here than a
    run being replayable months later against the identical evidence. Pass force=True
    on a search to refresh a single entry."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.by_hash = self.root / "by-hash"
        self.index = self.root / "index.jsonl"
        self.audit = self.root / "audit.jsonl"

    def path_for(self, h: str, backend: str) -> Path:
        # Shard on the first two hex chars: a flat directory of thousands of files is
        # slow to list and unpleasant to grep through by hand.
        return self.by_hash / backend / h[:2] / f"{h}.json"

    def get(self, h: str, backend: str) -> dict | None:
        p = self.path_for(h, backend)
        if not p.exists():
            return None
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None      # a half-written file is a miss, not a crash

    def put(self, res: SearchResult) -> None:
        p = self.path_for(res.query_hash, res.backend)
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(asdict(res), ensure_ascii=False, indent=2),
                       encoding="utf-8")
        tmp.replace(p)
        self._append(self.index, {"query_hash": res.query_hash,
                                  "normalized": normalize(res.sent_query),
                                  "backend": res.backend, "ts": res.ts,
                                  "cost_usd": res.cost_usd,
                                  "path": str(p.relative_to(self.root))})

    def log_audit(self, row: dict) -> None:
        self._append(self.audit, row)

    def _append(self, path: Path, row: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


# ------------------------------------------------------------------------- tool

TOOL_NAME = "web_search"
TOOL_DESCRIPTION = (
    "Look up a term or fact on the web and get back a short factual answer. Use it "
    "only to resolve what a term the reviewer used actually refers to (a game mode, "
    "an item, a currency, a subscription). One search per review."
)
TOOL_PARAMETERS = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "The question to look up, e.g. "
                           "'what is a welkin pass in Genshin Impact'.",
        }
    },
    "required": ["query"],
    "additionalProperties": False,
}


def tool_spec(style: str = "openai") -> dict:
    """The tool declaration, in whichever dialect the caller's provider speaks.

    Keep this deterministic: on providers that cache a prompt prefix, tools render
    BEFORE the prefix, so a tool declaration that varies between calls silently kills
    caching for the whole run."""
    if style == "openai":
        return {"type": "function",
                "function": {"name": TOOL_NAME,
                             "description": TOOL_DESCRIPTION,
                             "parameters": TOOL_PARAMETERS}}
    if style == "anthropic":
        return {"name": TOOL_NAME,
                "description": TOOL_DESCRIPTION,
                "input_schema": TOOL_PARAMETERS}
    raise ValueError(f"unknown tool style {style!r}")


def openai_tools() -> list:
    return [tool_spec("openai")]


class WebSearchTool:
    """Stateful across a run: holds the backend, the cache, and the running tally."""

    def __init__(self, backend: str = DEFAULT_BACKEND, *,
                 cache_dir: str | Path | None = DEFAULT_CACHE_DIR,
                 api_key: str | None = None,
                 max_results: int = DEFAULT_MAX_RESULTS,
                 pin_game_wikis: str = "off",
                 max_answer_chars: int = MAX_ANSWER_CHARS,
                 timeout: float = TIMEOUT, retries: int = RETRIES,
                 rng: random.Random | None = None):
        if backend not in BACKENDS:
            sys.exit(f"unknown search backend {backend!r}. "
                     f"known: {', '.join(sorted(BACKENDS))}")
        self.backend = BACKENDS[backend]()
        self.max_results = max_results
        self.pin_game_wikis = pin_game_wikis      # off | auto
        self.max_answer_chars = max_answer_chars
        self.timeout, self.retries = timeout, retries
        self.rng = rng or random.Random(0)
        self.cache = SearchCache(rc.resolve(cache_dir)) if cache_dir else None
        self.key = ""
        env = BACKEND_KEY_ENV.get(backend)
        if env:
            self.key = api_key or rc.load_api_key(env, SCRIPT_DIR, ENV_FILE)
        self.calls: list = []

    # -- properties the runner needs for its pricing assert and its meta rows ----
    @property
    def cost_per_search(self) -> float:
        return self.backend.cost_per_search

    @property
    def name(self) -> str:
        return self.backend.name

    def stats(self) -> dict:
        return {"n_calls": len(self.calls),
                "n_cache_hits": sum(c.cached for c in self.calls),
                "n_live": sum(not c.cached for c in self.calls),
                "n_errors": sum(bool(c.error) for c in self.calls),
                "cost_usd": round(sum(c.cost_usd for c in self.calls), 6),
                "backend": self.name}

    # ---------------------------------------------------------------- searching
    def domains_for(self, query: str) -> list:
        if self.pin_game_wikis == "auto" and looks_glossary(query):
            return list(GAME_WIKI_DOMAINS)
        return []

    def search(self, query: str, *, force: bool = False) -> SearchResult:
        """One search. Returns a SearchResult; never raises on a backend failure --
        a search that fails must not take a review down with it, so the error rides
        along in the result and the model is told to answer without it."""
        query = (query or "").strip()
        domains = self.domains_for(query)
        h = query_hash(query, self.backend.name, self.max_results)

        if self.cache and not force:
            hit = self.cache.get(h, self.backend.name)
            if hit:
                res = SearchResult(**hit)
                res.query = query          # the generated query, not the cached one
                res.cached, res.cost_usd, res.latency_s = True, 0.0, 0.0
                self.calls.append(res)
                return res

        t0 = time.time()
        raw, _, etype, emsg = rc.call_with_retries(
            lambda: self.backend.run(self.key, query, domains=domains,
                                     max_results=self.max_results,
                                     timeout=self.timeout),
            self.retries, self.rng, label="search")
        latency = round(time.time() - t0, 3)

        if etype:
            res = SearchResult(query=query, sent_query=query, query_hash=h, answer="",
                               backend=self.backend.name, latency_s=latency,
                               error=f"{etype}: {emsg}",
                               ts=datetime.now(timezone.utc).isoformat(timespec="seconds"))
            self.calls.append(res)
            return res      # NOT cached: a transport failure is not an answer

        answer, sources, n = self.backend.to_answer(raw)
        res = SearchResult(
            query=query, sent_query=query, query_hash=h,
            answer=clip(answer, self.max_answer_chars), sources=sources,
            backend=self.backend.name, cached=False,
            cost_usd=self.backend.cost_per_search, latency_s=latency,
            n_results=n, domains=domains, error=None,
            ts=datetime.now(timezone.utc).isoformat(timespec="seconds"), raw=raw)
        if self.cache:
            self.cache.put(res)
        self.calls.append(res)
        return res

    def execute(self, arguments, *, review_id: str = "", caller: str = "",
                force: bool = False) -> SearchResult:
        """Entry point for a tool loop: takes the model's generated arguments (a JSON
        string, or an already-parsed dict), searches, and writes the audit row.

        Arguments are always parsed with json.loads and never string-matched: models
        vary their escaping of unicode and slashes inside tool-call arguments, and a
        regex over the serialised form breaks on the first review with a quote in it."""
        if isinstance(arguments, str):
            try:
                arguments = json.loads(arguments or "{}")
            except json.JSONDecodeError as e:
                res = SearchResult(query="", sent_query="", query_hash="", answer="",
                                   backend=self.name, error=f"bad tool arguments: {e}")
                self.calls.append(res)
                if self.cache:
                    self.cache.log_audit(res.audit_row(review_id=review_id,
                                                       caller=caller))
                return res
        query = (arguments or {}).get("query", "")
        res = self.search(query, force=force)
        if self.cache:
            self.cache.log_audit(res.audit_row(review_id=review_id, caller=caller))
        return res


# --------------------------------------------------------------------- module api

def search(query: str, **kw) -> SearchResult:
    """One-off search without holding a tool object. Convenience for other scripts."""
    return WebSearchTool(**kw).search(query)


# ---------------------------------------------------------------------------- cli

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Search the web and print the short answer a teacher would see.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("query", nargs="+", help="the question to look up")
    ap.add_argument("--backend", default=DEFAULT_BACKEND, choices=sorted(BACKENDS))
    ap.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR)
    ap.add_argument("--no-cache", action="store_true",
                    help="ignore the disk cache entirely (also skips writing it)")
    ap.add_argument("--force", action="store_true",
                    help="refresh this one entry: search live, overwrite the cache")
    ap.add_argument("--max-results", type=int, default=DEFAULT_MAX_RESULTS)
    ap.add_argument("--pin-game-wikis", default="off", choices=("off", "auto"))
    ap.add_argument("--json", action="store_true", help="dump the full SearchResult")
    a = ap.parse_args()

    tool = WebSearchTool(a.backend, cache_dir=None if a.no_cache else a.cache_dir,
                         max_results=a.max_results, pin_game_wikis=a.pin_game_wikis)
    res = tool.search(" ".join(a.query), force=a.force)

    if a.json:
        print(json.dumps(asdict(res), ensure_ascii=False, indent=2))
        return
    print(f"\nbackend   {res.backend}   cached={res.cached}   "
          f"${res.cost_usd:.4f}   {res.latency_s}s   results={res.n_results}")
    if res.domains:
        print(f"pinned    {', '.join(res.domains)}")
    if res.error:
        print(f"ERROR     {res.error}")
    print(f"\n--- what the model would see ({len(res.as_tool_content())} chars) ---")
    print(res.as_tool_content())
    if res.sources:
        print("\nsources:")
        for s in res.sources[:5]:
            print(f"  {s['host']:<28} {s['title'][:60]}")


if __name__ == "__main__":
    main()
