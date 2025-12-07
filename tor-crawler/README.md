# Tor Onion Crawler - Academic Research Project

## Project Purpose

This is an **academic research project** designed to discover and index publicly accessible .onion (dark web) websites for studying the Tor network ecosystem.

**Research Objectives:**
- Study the structure of the publicly accessible Tor onion network
- Analyze patterns in onion site discovery through link following
- Understand Tor anonymity mechanisms and network behavior
- Develop web crawling techniques for hidden services

---

## Legal & Ethical Statement

### ✅ This Project is Legal For:
- Academic research and study
- Security/privacy research
- Understanding Tor network topology
- Learning web crawling techniques

### ⚠️ Restrictions:
- **Only crawls PUBLIC .onion sites** (like Ahmia, DuckDuckGo onion mirrors)
- **Automatically skips known illegal content** (blacklist implemented)
- **No unauthorized access** to private or protected content
- **Data retention policy**: Automatically deletes data older than 30 days
- **Encryption**: Database encrypted to protect data

### ❌ This Project Explicitly Does NOT:
- Crawl illegal marketplaces or hidden services
- Store or download illegal content
- Bypass site protections or authentication
- Violate Terms of Service
- Perform DDoS or malicious attacks

---

## Installation

### Requirements
```bash
- Python 3.10+
- Tor Browser (running, with SOCKS5 on port 9150)
- 200MB disk space
```

### Setup
```bash
# 1. Clone repository
git clone https://github.com/BinaryBoortsog/Open-source-project.git
cd tor-crawler

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate      # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start Tor Browser
# Keep it running in background
```

---

## Usage

### Run Deep Crawl (Academic Mode)
```bash
python deep_crawl.py

# Output:
# [+] Starting deep crawl with 6 seeds
# [+] Crawler will skip known illegal sites
# [1/200] Crawling https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/
#   -> found: http://example.onion
# [✓] Crawl complete! 47 pages indexed
```

### View Dashboard
```bash
# Terminal 2:
uvicorn web.app:app --reload --port 8000

# Open: http://localhost:8000
```

### Query Database
```python
import sqlite3
conn = sqlite3.connect("onions.db")
c = conn.cursor()
print("Total pages:", c.execute("SELECT COUNT(*) FROM pages").fetchone()[0])
```

---

## Project Structure

```
tor-crawler/
├── crawler/                    # Core crawling modules
│   ├── ahmia.py               # Seed discovery from Ahmia
│   ├── parser.py              # Link extraction (regex)
│   ├── seeds.py               # Seed URL generation
│   ├── tor_client.py          # Tor SOCKS5 session
│   └── tor_identity.py        # Circuit refresh
│
├── database/db.py             # SQLite storage
├── web/app.py                 # FastAPI dashboard
├── deep_crawl.py              # Main crawler loop
├── requirements.txt           # Dependencies
├── RESEARCH_NOTES.md          # Academic documentation
└── SECURITY.md                # Security implementation details
```

---

## Technical Implementation

### Anonymity Features
- **Tor SOCKS5 Proxy**: All traffic routed through Tor network (127.0.0.1:9150)
- **Circuit Rotation**: New Tor identity every 20 crawls (~7 minutes)
- **No DNS Leaks**: Using `socks5h://` for hostname resolution through Tor
- **SSL Verification Disabled**: Necessary for self-signed .onion certificates

### Content Filtering
```python
BLACKLIST_KEYWORDS = [
    'market', 'drug', 'weapon', 'child', 'exploit',
    'cc', 'carding', 'fraud', 'hack', 'leak'
]
# Automatically skips any URL matching these keywords
```

### Data Security
- **Encryption**: SQLite database encrypted with Fernet (AES-128)
- **Audit Logging**: All crawl activities logged with timestamps
- **Data Retention**: Automatic deletion of data older than 30 days
- **Rate Limiting**: 1-second delay between requests (polite crawling)

---

## Research Methodology

### Seed Sources
1. **Static Seeds**: Known public .onion mirrors (news, social media)
2. **Ahmia Search**: Public search results from Ahmia.fi
3. **Public Directories**: Aggregated from darkfail.net, oniontree.org

### Crawl Algorithm
- **BFS (Breadth-First Search)** with queue-based exploration
- **Visited Tracking**: Prevents re-crawling same URL
- **Offline Tracking**: Remembers dead/unreachable sites
- **Maximum Depth**: 200 pages per crawl session (configurable)

### Data Collection
- **URL**: Full .onion address
- **Content**: Full HTML (for link extraction and analysis)
- **Timestamp**: When page was crawled
- **Source**: Which seed or discovered link

---

## Academic Use Cases

### Data Analysis
```python
# Analyze discovered onion sites
import sqlite3
conn = sqlite3.connect("onions.db")
c = conn.cursor()

# How many unique sites discovered?
total = c.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
print(f"Total sites indexed: {total}")

# When was most recent crawl?
recent = c.execute(
    "SELECT MAX(crawled_at) FROM pages"
).fetchone()[0]
print(f"Most recent: {recent}")
```

### Research Questions
1. How densely linked is the public onion ecosystem?
2. What's the average degree of separation between onion sites?
3. How quickly does the onion network grow/change?
4. What are common categories of public .onion sites?
5. How does circuit rotation affect crawl patterns?

---

## Security & Privacy Considerations

### Protecting Your Identity
- ✅ All traffic through Tor (ISP can't see what you visit)
- ✅ Exit node rotates regularly (no correlation attacks)
- ✅ User-Agent rotation (harder to fingerprint)
- ✅ No JavaScript execution (prevents Tor circumvention)

### Protecting Your Data
- ✅ Database encrypted at rest
- ✅ Encryption key stored separately (not in code)
- ✅ Audit logs maintained
- ✅ Automatic data cleanup (30-day retention)

### Legal Compliance
- ✅ Only crawls public content
- ✅ Respects content warnings/robots.txt
- ✅ Automatic illegal content blacklist
- ✅ No unauthorized access attempts
- ✅ No data extraction from protected areas

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| **Crawl Speed** | ~3 pages/minute |
| **Memory Usage** | ~50MB |
| **Database Size** | ~50MB (200 pages) |
| **Circuit Refresh** | Every 20 crawls |
| **Rate Limit** | 1 second between requests |

---

## Contributing & Feedback

This is an academic project. Contributions and feedback welcome:

1. **Bug Reports**: Open GitHub issue with details
2. **Feature Requests**: Describe use case and rationale
3. **Research Questions**: Suggest interesting analyses
4. **Code Review**: Help improve security/efficiency

---

## References & Citations

If you use this project for research, please cite:

```bibtex
@software{tor_crawler_2025,
  author = {BinaryBoortsog},
  title = {Tor Onion Crawler - Academic Research Project},
  year = {2025},
  url = {https://github.com/BinaryBoortsog/Open-source-project}
}
```

---

## Disclaimer

**This project is for academic research purposes only.** Users are responsible for:
- Complying with all applicable laws and regulations
- Understanding the legal implications of their jurisdiction
- Using the tool responsibly and ethically
- Not accessing illegal content
- Protecting their own privacy and security

The authors make no warranties and are not liable for misuse.

---

## Contact & Questions

For questions about this project:
- Open a GitHub issue
- Contact: (Your email if desired)
- See SECURITY.md for security concerns

---

**Last Updated:** December 8, 2025  
**Status:** Active Development  
**License:** MIT
