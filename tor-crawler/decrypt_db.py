"""
Decrypt and view your encrypted database.
USE ONLY when you need to read the data (e.g., for analysis).
"""
import sqlite3
from cryptography.fernet import Fernet
import sys

# Load encryption key
try:
    with open("encryption.key", "rb") as f:
        key = f.read()
except FileNotFoundError:
    print("[✗] encryption.key not found!")
    print("[!] Enter your key manually:")
    key = input("Key: ").strip().encode()

cipher = Fernet(key)

# Connect to encrypted DB
conn = sqlite3.connect("onions.db")
c = conn.cursor()

print("[+] Decrypting database...\n")

# Show stats
total = c.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
print(f"Total encrypted pages: {total}\n")

# Decrypt and display recent URLs
print("Recent URLs (decrypted):")
print("-" * 80)

rows = c.execute("SELECT url, content FROM pages ORDER BY crawled_at DESC LIMIT 10").fetchall()

for url, encrypted_html in rows:
    try:
        html = cipher.decrypt(encrypted_html.encode()).decode()
        preview = html[:100].replace('\n', ' ')
        print(f"URL: {url}")
        print(f"Content preview: {preview}...")
        print()
    except Exception as e:
        print(f"[✗] Failed to decrypt {url}: {e}")

conn.close()
print("\n[✓] Decryption complete")
