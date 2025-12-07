"""
URGENT: Encrypt your existing database to protect your data.
Run this ONCE to encrypt onions.db, then use the encrypted version going forward.
"""
import sqlite3
from cryptography.fernet import Fernet
import os

# Generate encryption key (SAVE THIS SECURELY!)
print("[!] GENERATING ENCRYPTION KEY - SAVE THIS!")
print("[!] Without this key, your data is PERMANENTLY LOST!\n")

key = Fernet.generate_key()
print(f"YOUR ENCRYPTION KEY (save to password manager):")
print(f"{key.decode()}\n")

# Save key to file (MOVE THIS TO SECURE LOCATION AFTER!)
with open("encryption.key", "wb") as f:
    f.write(key)
print("[✓] Key saved to: encryption.key")
print("[!] MOVE THIS FILE TO A SECURE LOCATION (USB drive, password manager)")
print("[!] DELETE encryption.key from this folder after backing up!\n")

cipher = Fernet(key)

# Connect to existing DB
if not os.path.exists("onions.db"):
    print("[✗] No onions.db found. Run crawler first.")
    exit(1)

conn = sqlite3.connect("onions.db")
c = conn.cursor()

# Fetch all pages
print("[+] Reading existing database...")
rows = c.execute("SELECT url, content FROM pages").fetchall()
print(f"[+] Found {len(rows)} pages to encrypt\n")

if len(rows) == 0:
    print("[!] Database is empty. Nothing to encrypt.")
    exit(0)

# Create encrypted backup
print("[+] Creating encrypted backup: onions_encrypted.db")
conn_enc = sqlite3.connect("onions_encrypted.db")
c_enc = conn_enc.cursor()

c_enc.execute("""
CREATE TABLE IF NOT EXISTS pages (
    url TEXT PRIMARY KEY,
    content TEXT,
    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Encrypt and copy
for i, (url, html) in enumerate(rows, 1):
    encrypted_html = cipher.encrypt(html.encode()).decode()
    c_enc.execute("REPLACE INTO pages (url, content) VALUES (?, ?)", 
                  (url, encrypted_html))
    if i % 10 == 0:
        print(f"[+] Encrypted {i}/{len(rows)} pages...")

conn_enc.commit()
conn_enc.close()
conn.close()

print(f"\n[✓] SUCCESS! Encrypted {len(rows)} pages")
print(f"[✓] Encrypted database: onions_encrypted.db")
print(f"\n[!] NEXT STEPS:")
print(f"    1. BACKUP encryption.key to USB/password manager")
print(f"    2. DELETE encryption.key from this folder")
print(f"    3. DELETE original onions.db (KEEP onions_encrypted.db)")
print(f"    4. Rename: onions_encrypted.db → onions.db")
print(f"\n[!] To decrypt: Use decrypt_db.py (will be created next)")
