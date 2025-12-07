# tor_identity.py
import time
from crawler import tor_client


def new_tor_identity():
    """Refresh Tor identity by getting a new circuit."""
    try:
        # Close and recreate the session to get a new circuit
        tor_client.session.close()
        time.sleep(2)
        
        import requests
        import urllib3
        
        tor_client.session = requests.Session()
        tor_client.session.trust_env = False
        tor_client.session.proxies = {
            "http": "socks5h://127.0.0.1:9150",
            "https": "socks5h://127.0.0.1:9150",
        }
        tor_client.session.verify = False
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        print("[info] New Tor circuit obtained")
        return True
    except Exception as e:
        print(f"[error] Failed to refresh Tor identity: {e}")
        return False
