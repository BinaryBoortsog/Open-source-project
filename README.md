# Docker is added to software read the Portable_setup.mn

# Tor Onion Crawler - Open Source Project Report
## Summary

**Project Name:** Tor Onion Crawler  
**Repository:** BinaryBoortsog/Open-source-project  
**Language:** Python 3.12

# What is crawler ? 

A crawler, or web spider/bot, is an automated software program that systematically browses the World Wide Web, following links to discover and index web pages, collecting data like text, images, and links to build searchable databases for search engines

# What i tried to build ?

My project is Tor onion crawler . Python apllication it is designed to crawl through public accessible (onion sites ). It starts from seed URLs and recursively follows links, much like a standard crawler, but on the hidden network. Crawling is used for Cybercrime Research , Threat Intelligence and data collection.
# Alert this project is only for education and research purpose. Only for my interest in cypersecurity and for studying.
# !!! RECOMMENDING NOT TRY GET INTO CRAWLED ONION URLS IT CAN BE SOME SECURITY VULNERABILITIES .


### Problem It Solves
- **Decentralized indexing** - No single point of failure (unlike centralized search engines)
- **Anonymity** - Researchers can study .onion sites without revealing their IP
- **Automation** - Saves thousands of hours of manual crawling
- **Transparency** - Open source, auditable code (no proprietary surveillance)

### Core Modules

| Module | Purpose | Lines | Status |
|--------|---------|-------|--------|
| `tor_client.py` | Tor SOCKS proxy setup | 20 | ✅ Stable |
| `seeds.py` | Seed URL generation | 35 | ✅ Stable |
| `ahmia.py` | Ahmia search + directory scraping | 85 | ✅ Stable |
| `parser.py` | HTML link extraction (regex) | 10 | ✅ Stable |
| `tor_identity.py` | Circuit refresh logic | 30 | ✅ Stable |
| `deep_crawl.py` | Main crawl loop | 60 | ✅ Stable |
| `database/db.py` | SQLite persistence | 20 | ✅ Stable |
| `web/app.py` | FastAPI web server | 40 | ✅ Stable |
| `web/templates/index.html` | Dashboard UI | 150 | ✅ Stable |



## Project Structure

```
tor-crawler/
├── crawler/                    # Core crawler modules
│   ├── __init__.py
│   ├── ahmia.py               # Ahmia search + directory scraping
│   ├── parser.py              # HTML → .onion link extraction
│   ├── seeds.py               # Seed URL generation
│   ├── tor_client.py          # Tor SOCKS5 session setup
│   └── tor_identity.py        # Circuit refresh logic
│
├── database/                  # Data persistence
│   ├── __init__.py
│   ├── db.py                  # SQLite schema + save_page()
│   └── onions.db              # SQLite database (auto-created)
│
├── web/                       # Web dashboard
│   ├── app.py                 # FastAPI server + routes
│   ├── static/                # CSS/JS (future enhancement)
│   └── templates/
│       └── index.html         # Dashboard UI (Jinja2)
│
├── deep_crawl.py              # Main crawler loop (200 pages)
├── run_crawler.py             # Alternative crawler (simpler)
├── test_seeds.py              # Seed discovery test
├── requirements.txt           # Python dependencies
├── README.md                  # User documentation
```

# Quick Start Guide

## Step 1: Install Requirements
```bash
cd tor-crawler
pip install -r requirements.txt
```

## Step 2: Start Tor Browser
- Download: https://www.torproject.org/download/
- Install and run it
- Leave it open while crawling

## Step 3: Run Crawler
```bash
python deep_crawl.py

## Step 4: View Dashboard (In New Terminal)
```bash
uvicorn web.app:app --port 8000
```

Open browser: **http://localhost:8000**


### ✅ Security Features

1. **Tor Anonymization** - Full routing through Tor SOCKS5
2. **No DNS Leaks** - Using `socks5h://` (hostname resolution in Tor)
3. **SSL Bypass** - Accepts self-signed certs (necessary for .onion)
4. **Circuit Rotation** - New Tor identity every 20 crawls
5. **Rate Limiting** - Polite 1-second delays
6. **Error Isolation** - Failed sites don't crash crawler
7. **Offline Tracking** - Won't re-attempt dead sites


# Image 
run Crawler . it is fetching from seed urls and scannig HTML pages of browser  if there is .onion links it will copy and check the status 
![Crawler Screenshot](https://drive.google.com/uc?export=view&id=1yF7FpbvH6xNGQZ6todIZ_2mzmvOndSB_)


# Web template 
it shows crawled links list
<p align="center">
  <img src="https://drive.google.com/uc?export=view&id=1g50JmBfGB5o5ETOjjl74cM6Cqp3Tkh8q" width="350">
  <br>
  <em>Tor Crawler Screenshot</em>
</p>

<p align="center">
  <img src="https://drive.google.com/uc?export=view&id=1HesySL6MFghVbX76uxBu3iANJno_YGM9" width="500">
</p>





