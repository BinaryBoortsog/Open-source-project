"""
Ahmia search + directory scraping for onion seeds.
"""
import re
import requests
from bs4 import BeautifulSoup
from crawler import tor_client

ONION_RE = re.compile(r"https?://[a-z2-7]{56}\.onion", re.IGNORECASE)

AHMIA_QUERIES = [
    "forum", "market", "wiki", "news", "chat",
    "blog", "hidden service", "test", "mirror"
]


def get_ahmia_seeds():
    """Scrape Ahmia search results for .onion URLs."""
    seeds = set()
    
    for q in AHMIA_QUERIES:
        try:
            url = f"https://ahmia.fi/search/?q={q}"
            r = requests.get(url, timeout=20, headers={"User-Agent": "seed-crawler"})
            if r.status_code != 200:
                continue
            
            soup = BeautifulSoup(r.text, "html.parser")
            
            # Find links
            for a in soup.find_all("a"):
                href = a.get("href", "")
                if ".onion" in href:
                    m = ONION_RE.search(href)
                    if m:
                        seeds.add(m.group(0))
            
            # Scan raw HTML
            for m in ONION_RE.findall(r.text):
                seeds.add(m)
        except Exception:
            continue
    
    return list(seeds)


def get_directory_seeds():
    """Scrape public onion directories."""
    seeds = set()
    
    directories = [
        ("http://darkfailllnkf4vf.onion/", True),
        ("http://oniontree-dbmh9e6g.onion/", True),
        ("https://onions.danwin1210.de/", False),
    ]
    
    for url, is_onion in directories:
        try:
            if is_onion:
                r = tor_client.session.get(url, timeout=30)
            else:
                r = requests.get(url, timeout=20, headers={"User-Agent": "seed-crawler"})
            
            if r.status_code != 200:
                continue
            
            for m in ONION_RE.findall(r.text):
                seeds.add(m)
        except Exception:
            continue
    
    return list(seeds)


def get_ahmia_urls():
    """Combine Ahmia search + directory seeds."""
    seeds = set()
    seeds.update(get_ahmia_seeds())
    seeds.update(get_directory_seeds())
    return sorted(seeds)
