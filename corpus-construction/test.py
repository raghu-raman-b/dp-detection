from google_play_scraper import search
import config

title = "Candy Crush Saga"

hits = search(title, lang=config.REVIEW_LANG, country=config.MARKETS[1],
                          n_hits=16)

print([(r['title'], r['appId']) for r in hits])
