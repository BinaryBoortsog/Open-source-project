# For Professor - How to Review This Project

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/BinaryBoortsog/Open-source-project.git
cd tor-crawler

# 2. Read the documentation
cat README.md                    # Project overview
cat PROJECT_REPORT.md            # Full technical report
cat SECURITY_RECOMMENDATIONS.md  # Security analysis
```

## Code Review Checklist

### Academic Rigor
- [ ] **README.md**: Clear research objectives stated
- [ ] **Legal Compliance**: Explicit statement of legal/ethical guidelines
- [ ] **Methodology**: BFS crawl algorithm documented
- [ ] **Data Handling**: Encryption and audit logging implemented

### Security Implementation
- [ ] **Tor Integration**: SOCKS5 proxy correctly configured
- [ ] **Circuit Refresh**: Every 20 crawls (good practice)
- [ ] **Content Filtering**: Blacklist prevents illegal content
- [ ] **Encryption**: Database encrypted with Fernet
- [ ] **Audit Logs**: All activity logged with timestamps

### Code Quality
- [ ] **Modularity**: Separate concerns (crawler, parser, database, web)
- [ ] **Error Handling**: Try/except blocks prevent crashes
- [ ] **Documentation**: Comments explain complex sections
- [ ] **Dependencies**: Listed in requirements.txt

### Ethics & Compliance
- [ ] **Only Public Content**: Uses Ahmia, DuckDuckGo onion mirrors
- [ ] **No Unauthorized Access**: Respects site protections
- [ ] **Transparent Intent**: Research purpose documented
- [ ] **Data Minimization**: Automatic 30-day cleanup
- [ ] **Legal Compliance**: Complies with research guidelines

## Key Files to Review

1. **README.md** - Start here (project overview)
2. **deep_crawl.py** - Main crawling algorithm
3. **crawler/tor_client.py** - Tor integration
4. **crawler/parser.py** - Link extraction logic
5. **database/db.py** - Data storage
6. **web/app.py** - Dashboard interface
7. **PROJECT_REPORT.md** - Full technical analysis

## Testing the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Run with Tor Browser active
python deep_crawl.py

# View dashboard
uvicorn web.app:app --port 8000
# Open: http://localhost:8000
```

## Security Features

- ✅ Tor anonymity (SOCKS5 proxy)
- ✅ Database encryption (Fernet AES-128)
- ✅ Circuit rotation (every 20 crawls)
- ✅ Content blacklist (prevents illegal sites)
- ✅ Audit logging (activity tracking)
- ✅ Data retention policy (30-day cleanup)

## Legal Compliance

This project is designed for **legal, academic research only**:
- Only crawls PUBLIC .onion sites
- Automatically skips illegal content
- Uses published research sources (Ahmia, DuckDuckGo)
- Encrypts and secures all data
- Maintains audit logs
- Complies with Tor Project guidelines

See SECURITY_RECOMMENDATIONS.md for full legal analysis.

## Questions?

Review the documentation files:
- README.md - Project overview
- PROJECT_REPORT.md - Technical details
- SECURITY_RECOMMENDATIONS.md - Security & legal analysis

---

**This project demonstrates academic research practices in cryptography, networking, and data science.**
