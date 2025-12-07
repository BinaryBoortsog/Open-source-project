"""
Seed URLs for Tor crawler.
Includes static well-known onions and dynamic scraping from Ahmia.
"""
from crawler.ahmia import get_ahmia_urls as _fetch_dynamic_seeds


# Hand-picked, public, legal onion seeds
STATIC_SEEDS = [
    "https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/",
    "http://darkfailenbsdla5mal2mxn2uz66od5vtzd5qozslagrfzachha3f3id.onion/",
]


def get_seed_urls():
    """Return static seeds plus dynamic Ahmia seeds."""
    seeds = set(STATIC_SEEDS)
    try:
        seeds.update(_fetch_dynamic_seeds())
    except Exception:
        pass  # Fall back to static seeds if Ahmia fails
    return sorted(seeds)


def get_ahmia_urls():
    """Fetch dynamic seeds from Ahmia search + directory scraping."""
    try:
        return _fetch_dynamic_seeds()
    except Exception:
        return []
