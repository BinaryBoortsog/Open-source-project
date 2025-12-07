"""
Parse HTML to extract onion links.
"""
import re

ONION_RE = re.compile(r"https?://[a-z2-7]{56}\.onion", re.IGNORECASE)


def extract_onion_links(html):
    """Extract all .onion URLs from HTML."""
    if not html:
        return []
    return list(set(ONION_RE.findall(html)))
