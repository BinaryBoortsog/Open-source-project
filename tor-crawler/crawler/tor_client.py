import os
import requests
import urllib3

TOR_PROXY = os.getenv("TOR_PROXY", "socks5h://127.0.0.1:9150")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

session = requests.Session()
session.trust_env = False
session.proxies = {
    "http": TOR_PROXY,
    "https": TOR_PROXY
}
session.verify = False

session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
})
