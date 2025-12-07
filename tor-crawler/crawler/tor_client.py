# tor_client.py
import requests
import urllib3

# Silence HTTPS warnings for self-signed onion certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Create a requests session routed through Tor
session = requests.Session()
session.trust_env = False
session.proxies = {
    'http': 'socks5h://127.0.0.1:9150',
    'https': 'socks5h://127.0.0.1:9150'
}
session.verify = False

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
session.headers.update(DEFAULT_HEADERS)
