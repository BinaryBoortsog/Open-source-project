# deep_crawl.py
import time
import sys
from crawler import tor_client
from crawler.seeds import get_seed_urls, get_ahmia_urls
from crawler.tor_identity import new_tor_identity
from crawler.parser import extract_onion_links
from database.db import save_page, close_db

# Config
MAX_PAGES = 200
REFRESH_CIRCUIT_EVERY = 20

# Initialize seeds
seeds = list(set(get_seed_urls() + get_ahmia_urls()))
queue = seeds.copy()
visited = set()
offline = set()
count = 0
success = 0

print(f"[+] Starting deep crawl with {len(seeds)} seeds")
print(f"[+] Max pages: {MAX_PAGES}, Circuit refresh every: {REFRESH_CIRCUIT_EVERY}\n")

# Main crawl loop
while queue and count < MAX_PAGES:
    url = queue.pop(0)
    if url in visited or url in offline:
        continue
    
    count += 1
    print(f"[{count}/{MAX_PAGES}] Crawling {url}")

    try:
        r = tor_client.session.get(url, timeout=30)
        if r.status_code != 200:
            print(f"[offline] {url} returned {r.status_code}")
            offline.add(url)
            continue

        html = r.text
        visited.add(url)
        success += 1

        # Extract .onion links
        new_links = extract_onion_links(html)
        for link in new_links:
            if link not in visited and link not in queue and link not in offline:
                queue.append(link)
                print(f"  -> found: {link}")

        # Save to DB
        save_page(url, html)

    except Exception as e:
        print(f"[offline] {url} failed: {e}")
        offline.add(url)

    # Refresh circuit periodically
    if count % REFRESH_CIRCUIT_EVERY == 0:
        new_tor_identity()

    time.sleep(1)  # Polite delay

print(f"\n[✓] Crawl complete!")
print(f"    Total visited: {len(visited)}")
print(f"    Successfully saved: {success}")
print(f"    Offline/failed: {len(offline)}")
print(f"    Remaining queue: {len(queue)}")
