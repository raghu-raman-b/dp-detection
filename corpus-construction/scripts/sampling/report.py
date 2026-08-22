"""Final report — prints the full count table as markdown for direct
paste into the paper's data section.

Covers: games resolved, reviews scraped, survivors per filter stage
(overall / per market / per app), pool size, and pilot strata.

Run:  python report.py            (or  python report.py > data_section.md)
"""
import csv
import json
from collections import defaultdict

import config
from utils import read_jsonl


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def fmt(n):
    return f"{n:,}"


def main():
    print("# Corpus construction — count tables\n")

    # ---- games resolved ---------------------------------------------------
    if config.RESOLVED_CSV.exists():
        with open(config.RESOLVED_CSV, encoding="utf-8", newline="") as f:
            apps = list(csv.DictReader(f))
        n_casino = sum(int(a["casino"]) for a in apps)
        n_review = sum(int(a["needs_review"]) for a in apps)
        per_mkt = defaultdict(int)
        for a in apps:
            for m in a["markets"].split(";"):
                per_mkt[m] += 1
        print("## Games resolved\n")
        print(md_table(
            ["Metric", "Count"],
            [["Unique apps (deduped by app_id)", fmt(len(apps))],
             ["Casino-flagged apps", fmt(n_casino)],
             ["Hand-verified (needs_review resolved)", fmt(len(apps) - n_review)]]
            + [[f"Apps listed in market `{m}`", fmt(per_mkt[m])]
               for m in config.MARKETS]))
        print()

    # ---- scraped ------------------------------------------------------------
    if config.SCRAPE_LOG.exists():
        with open(config.SCRAPE_LOG, encoding="utf-8", newline="") as f:
            slog = list(csv.DictReader(f))
        per_mkt = defaultdict(int)
        unavailable = 0
        for r in slog:
            if r["status"] == "unavailable":
                unavailable += 1
            per_mkt[r["market"]] += int(r["n_reviews"] or 0)
        print("## Reviews scraped\n")
        print(md_table(
            ["Market", "Reviews scraped"],
            [[m, fmt(per_mkt[m])] for m in config.MARKETS]
            + [["**Total**", f"**{fmt(sum(per_mkt.values()))}**"]]))
        print(f"\nApp×market pairs unavailable in store: {unavailable}\n")

    # ---- filter cascade -----------------------------------------------------
    if config.CORPUS_STATS.exists():
        with open(config.CORPUS_STATS, encoding="utf-8") as f:
            stats = json.load(f)
        stages = list(stats["stage_totals"].keys())
        totals = stats["stage_totals"]
        print("## Filter cascade (PRISMA-style)\n")
        rows, prev = [], None
        for s in stages:
            n = totals[s]
            rows.append([s, fmt(n), "—" if prev is None else fmt(prev - n)])
            prev = n
        print(md_table(["Stage", "Survivors", "Removed"], rows))
        print("\n### Per market\n")
        print(md_table(
            ["Market"] + stages,
            [[m] + [fmt(stats["per_market"][m][s]) for s in stages]
             for m in config.MARKETS if m in stats["per_market"]]))
        print("\n### Per app\n")
        app_rows = sorted(stats["per_app"].items(),
                          key=lambda kv: -kv[1][stages[-1]])
        print(md_table(["App ID"] + stages,
                       [[a] + [fmt(c[s]) for s in stages]
                        for a, c in app_rows]))
        print()

    # ---- samples --------------------------------------------------------------
    print("## Sampling\n")
    pool = list(read_jsonl(config.POOL_JSONL))
    if pool:
        per_mkt = defaultdict(int)
        capped = sum(1 for r in pool if r.get("sample_weight", 1.0) != 1.0)
        apps_in_pool = len({r["app_id"] for r in pool})
        for r in pool:
            per_mkt[r["market"]] += 1
        print(md_table(
            ["Metric", "Count"],
            [["Labeling pool size", fmt(len(pool))],
             ["Apps represented", fmt(apps_in_pool)],
             ["Rows with sample_weight > 1 (capped strata)", fmt(capped)]]
            + [[f"Pool rows from `{m}`", fmt(per_mkt[m])]
               for m in sorted(per_mkt)]))
        print()
    pr = list(read_jsonl(config.PILOT_RANDOM_JSONL))
    pt = list(read_jsonl(config.PILOT_TARGETED_JSONL))
    if pr or pt:
        per_kw = defaultdict(int)
        for r in pt:
            per_kw[r["seed_keyword"]] += 1
        print("### Pilot strata\n")
        print(md_table(
            ["Stratum", "Seed keyword", "Reviews"],
            [["random", "—", fmt(len(pr))]]
            + [["targeted", k, fmt(per_kw[k])]
               for k in config.TARGET_KEYWORDS if per_kw[k]]
            + [["**targeted total**", "", f"**{fmt(len(pt))}**"]]))


if __name__ == "__main__":
    main()