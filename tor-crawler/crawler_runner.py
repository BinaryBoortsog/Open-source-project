# crawler_runner.py
import time
from crawler.crawler import TorCrawler

while True:
    print("\n[*] Starting NEW deep crawl cycle...\n")

    crawler = TorCrawler(max_pages=200, refresh_every=20)
    crawler.crawl()

    print("[*] Sleeping 5 minutes before next cycle...\n")
    time.sleep(300)  # 5 minutes
