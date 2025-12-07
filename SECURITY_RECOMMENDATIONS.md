## Tor Onion Crawler - Security & Safety Recommendations

### 🎯 Legal Usage Guidelines

#### ✅ SAFE to crawl:
- Public onion news/media mirrors (NYTimes, BBC, etc.)
- Onion directories & search engines (Ahmia, DuckDuckGo onion)
- Privacy/security project sites (Tor Project, EFF, etc.)
- Academic/research onion archives
- Public forums & discussion sites (legal content only)

#### ❌ DO NOT crawl:
- Known darknet markets (Silk Road clones, etc.)
- Illegal content repositories (drugs, weapons, CSAM, etc.)
- Any site hosting illegal material
- Sites with Terms of Service forbidding automated access

---

### 🔐 Technical Security Hardening

#### 1. **Disk Encryption**
```bash
# Windows: Enable BitLocker
manage-bde -status
manage-bde -on C:

# Linux: Enable LUKS
sudo cryptsetup luksFormat /dev/sdX
```
Encrypts `onions.db` so raw disk access doesn't expose crawled content.

#### 2. **Input Validation & Sanitization**
Update `crawler/parser.py` to sanitize HTML:
```python
import html
import re

def extract_onion_links(html):
    if not html:
        return []
    # Remove script tags and dangerous content
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    return list(set(ONION_RE.findall(html)))
```

#### 3. **Database Encryption**
Add encrypted storage for sensitive data:
```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()  # Store securely
cipher = Fernet(key)

def save_page_encrypted(url, html):
    encrypted = cipher.encrypt(html.encode())
    cur.execute("INSERT INTO pages VALUES (?, ?)", (url, encrypted))
```

#### 4. **Logging & Audit Trail**
```python
import logging
from datetime import datetime

logging.basicConfig(
    filename=f"crawl_log_{datetime.now().strftime('%Y%m%d')}.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_crawl(url, status, reason=""):
    logging.info(f"Crawl: {url} | Status: {status} | {reason}")
```

#### 5. **Strict Content Filtering**
Blacklist known illegal marketplaces & dangerous sites:
```python
# Add to crawler/tor_client.py
BLACKLIST_DOMAINS = {
    "darkfailllnkf4vf.onion",  # Known marketplace aggregator
    # Add other known illegal sites
}

def is_safe_to_crawl(url):
    for domain in BLACKLIST_DOMAINS:
        if domain in url:
            return False
    return True
```

#### 6. **Rate Limiting & Responsible Crawling**
```python
import time
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests_per_hour=100):
        self.max_requests = max_requests_per_hour
        self.request_times = []
    
    def should_crawl(self):
        now = datetime.now()
        # Remove old requests outside the 1-hour window
        self.request_times = [t for t in self.request_times 
                              if now - t < timedelta(hours=1)]
        
        if len(self.request_times) < self.max_requests:
            self.request_times.append(now)
            return True
        return False
```

---

### 🛡️ Network & Privacy Hardening

#### 7. **Tor Circuit Management**
Implement smarter circuit rotation:
```python
def refresh_tor_identity_smart():
    """Refresh circuit with exponential backoff on failures."""
    import time
    retry_count = 0
    while retry_count < 3:
        try:
            new_tor_identity()
            return True
        except Exception as e:
            retry_count += 1
            time.sleep(2 ** retry_count)  # Exponential backoff
    return False
```

#### 8. **VPN + Tor Stack** (Optional, for extra protection)
```python
# Route through VPN first, then Tor
session.proxies = {
    'http': 'socks5h://127.0.0.1:9150',  # Tor
    'https': 'socks5h://127.0.0.1:9150',
}
# Use a VPN provider's SOCKS endpoint before Tor if maximum anonymity needed
```

#### 9. **DNS Leak Prevention**
Ensure all DNS queries go through Tor:
```python
# tor_client.py: Already using socks5h (hostname resolution through Tor)
# This prevents DNS leaks—good!
session.proxies = {
    'http': 'socks5h://127.0.0.1:9150',  # 'h' = hostname resolution via Tor
    'https': 'socks5h://127.0.0.1:9150',
}
```

#### 10. **User-Agent Rotation**
Vary user agents to avoid fingerprinting:
```python
import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

# Use in tor_client.py
session.headers['User-Agent'] = get_random_user_agent()
```

---

### 📋 Operational Security (OpSec)

#### 11. **Isolated VM/Machine**
- Run crawler on a dedicated VM or separate machine
- Use network isolation (firewall rules limiting outbound)
- Never browse clearnet on the same machine while crawling

#### 12. **Access Control**
```bash
# Restrict database file permissions
chmod 600 onions.db

# Restrict log file permissions
chmod 600 crawl_log_*.log
```

#### 13. **Data Retention Policy**
```python
# Delete old crawl data after N days
def cleanup_old_data(days=30):
    cutoff = datetime.now() - timedelta(days=days)
    cur.execute("DELETE FROM pages WHERE crawled_at < ?", (cutoff,))
    conn.commit()

# Schedule weekly cleanup
schedule.every().week.do(cleanup_old_data)
```

#### 14. **Backup Security**
```bash
# Encrypt backups
gpg --encrypt --recipient your-email@example.com onions.db.backup

# Store backups securely (not in cloud unless encrypted)
```

#### 15. **Monitoring & Alerts**
```python
def check_tor_health():
    """Verify Tor connection is still active."""
    try:
        r = requests.get("https://check.torproject.org/", 
                        proxies=session.proxies, 
                        timeout=10)
        if r.status_code == 200:
            return True
    except:
        pass
    return False

# Alert if Tor drops
if not check_tor_health():
    logging.error("Tor connection lost! Stopping crawler.")
    # Stop crawler gracefully
```

---

### 📝 Compliance & Legal Checklist

- [ ] Only crawl **public, legal content**
- [ ] Respect `robots.txt` equivalents (even on .onion sites)
- [ ] Don't store **PII, payment info, or illegal content**
- [ ] Comply with **local jurisdiction laws** on Tor use
- [ ] Maintain **audit logs** of what was crawled
- [ ] Don't share/distribute **illegal content** found
- [ ] Have **terms of use** documenting crawl scope
- [ ] Implement **content moderation** to prevent crawling known illegal sites

---

### 🚨 If Law Enforcement Contacts You

1. **Do NOT consent to searches** - Invoke right to attorney
2. **Your legal right**: Using Tor for lawful purposes is legal in most jurisdictions
3. **Defense**: Crawl logs showing only legal content access
4. **Expert help**: Contact a lawyer familiar with Tor/anonymity law

---

### 📊 Recommended Monitoring Dashboard

Add to `web/app.py`:
```python
@app.get("/api/health")
def health_check():
    """System health & security status."""
    return {
        "tor_status": check_tor_health(),
        "last_crawl": get_last_crawl_time(),
        "total_pages": get_page_count(),
        "blacklist_violations": count_blacklist_hits(),
        "encryption_enabled": check_encryption(),
    }
```

---

### ✅ Summary: Safe Crawler Best Practices

1. ✅ Crawl **only public, legal** .onion content
2. ✅ Encrypt your **disk & database**
3. ✅ Use **Tor SOCKS** (already done)
4. ✅ Rotate **user agents & circuits**
5. ✅ Implement **content filtering** (blacklist illegal sites)
6. ✅ Keep **audit logs** of all crawls
7. ✅ Run in **isolated environment** (VM/separate machine)
8. ✅ Maintain **legal compliance** documentation
9. ✅ Monitor **Tor health** continuously
10. ✅ Implement **data retention policies** (don't keep forever)

---

**Your current crawler is safe for legal research. Use these hardening recommendations to maximize security and ensure full compliance with laws.**
