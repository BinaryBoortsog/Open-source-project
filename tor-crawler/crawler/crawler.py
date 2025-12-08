# crawler/crawler.py
import time
from crawler.tor_client import session
from crawler.seeds import get_seed_urls, get_ahmia_urls
from crawler.parser import extract_onion_links
from crawler.tor_identity import new_tor_identity
from database.db import save_page

class TorCrawler:

    def __init__(self, max_pages=200, refresh_every=20):
        self.max_pages = max_pages
        self.refresh_every = refresh_every
        self.seeds = list(set(get_seed_urls() + get_ahmia_urls()))
        self.queue = self.seeds.copy()
        self.visited = set()
        self.offline = set()
        self.success = 0
        self.count = 0

    def crawl(self):
        print(f"[+] Starting deep crawl with {len(self.seeds)} seeds")
        print(f"[+] Max pages: {self.max_pages}, Circuit refresh every: {self.refresh_every}\n")

        while self.queue and self.count < self.max_pages:
            url = self.queue.pop(0)

            if url in self.visited or url in self.offline:
                continue

            self.count += 1
            print(f"[{self.count}/{self.max_pages}] Crawling {url}")

            try:
                r = session.get(url, timeout=30)
                if r.status_code != 200:
                    print(f"[offline] {url} returned {r.status_code}")
                    self.offline.add(url)
                    continue

                html = r.text
                self.visited.add(url)
                self.success += 1

                # Parse new onion links
                for link in extract_onion_links(html):
                    if link not in self.visited and link not in self.queue and link not in self.offline:
                        self.queue.append(link)
                        print(f"  -> found: {link}")

                # Save to DB
                save_page(url, html)

            except Exception as e:
                print(f"[offline] {url} failed: {e}")
                self.offline.add(url)

            if self.count % self.refresh_every == 0:
                new_tor_identity()

            time.sleep(1)

        print(f"\n[✓] Crawl complete!")
        print(f"    Total visited: {len(self.visited)}")
        print(f"    Successfully saved: {self.success}")
        print(f"    Offline/failed: {len(self.offline)}")
        print(f"    Remaining queue: {len(self.queue)}")
