import sqlite3
import os
import shutil
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    filename='crawler_audit.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

DB_PATH = "data/onions.db"
BACKUP_DIR = "data/backups"
CHECKPOINT_EVERY = 10  # Save after every N pages

# Create backup directory
os.makedirs(BACKUP_DIR, exist_ok=True)


class CrawlerDB:
    def __init__(self):
        """Initialize database with crash recovery."""
        self.conn = None
        self.cur = None
        self.page_count = 0
        self._initialize_db()
        self._check_recovery()
    
    def _initialize_db(self):
        """Create database connection with safety settings."""
        try:
            self.conn = sqlite3.connect(DB_PATH, timeout=10)
            self.conn.isolation_level = 'DEFERRED'  # Transaction safety
            self.cur = self.conn.cursor()
            
            # Enable write-ahead logging (safer)
            self.cur.execute("PRAGMA journal_mode=WAL")
            # Increase cache for better performance
            self.cur.execute("PRAGMA cache_size=10000")
            
            self.cur.execute("""
            CREATE TABLE IF NOT EXISTS pages (
                url TEXT PRIMARY KEY,
                content TEXT,
                crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                backup_status TEXT DEFAULT 'active'
            )
            """)
            self.conn.commit()
            print("[✓] Database initialized with safety features")
            logging.info("Database initialized")
        except Exception as e:
            print(f"[✗] Database init failed: {e}")
            logging.error(f"Database init failed: {e}")
            raise
    
    def _check_recovery(self):
        """Check for incomplete transactions and recover."""
        try:
            # Count existing pages
            count = self.cur.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
            self.page_count = count
            print(f"[+] Database contains {count} pages")
            logging.info(f"Database recovered with {count} pages")
        except Exception as e:
            print(f"[!] Recovery check failed: {e}")
    
    def save_page(self, url, html):
        """Save page with crash safety."""
        try:
            # Use transaction for safety
            self.cur.execute("""
            INSERT OR REPLACE INTO pages (url, content, backup_status)
            VALUES (?, ?, 'active')
            """, (url, html))
            
            self.page_count += 1
            
            # Checkpoint every N pages (prevents data loss)
            if self.page_count % CHECKPOINT_EVERY == 0:
                self.conn.commit()
                self._create_checkpoint_backup()
                print(f"[✓] Checkpoint: {self.page_count} pages saved")
                logging.info(f"Checkpoint: {self.page_count} pages saved")
            else:
                self.conn.commit()
                
        except sqlite3.OperationalError as e:
            print(f"[✗] Database locked: {e}")
            logging.error(f"Database error: {e}")
            # Retry once
            self.conn.rollback()
            self.conn.execute("""
            INSERT OR REPLACE INTO pages (url, content, backup_status)
            VALUES (?, ?, 'active')
            """, (url, html))
            self.conn.commit()
    
    def _create_checkpoint_backup(self):
        """Create backup after every checkpoint."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(BACKUP_DIR, f"onions_backup_{timestamp}.db")
            
            # Close connection, backup, reopen
            self.conn.execute("PRAGMA optimize")
            shutil.copy2(DB_PATH, backup_file)
            
            # Keep only last 10 backups
            backups = sorted(os.listdir(BACKUP_DIR))
            if len(backups) > 10:
                for old_backup in backups[:-10]:
                    os.remove(os.path.join(BACKUP_DIR, old_backup))
                    print(f"[+] Cleaned old backup: {old_backup}")
            
            print(f"[+] Backup created: {backup_file}")
            logging.info(f"Backup created: {backup_file}")
        except Exception as e:
            print(f"[!] Backup failed: {e}")
            logging.warning(f"Backup failed: {e}")
    
    def get_stats(self):
        """Get database statistics."""
        try:
            total = self.cur.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
            return {"total_pages": total, "status": "healthy"}
        except Exception as e:
            return {"error": str(e), "status": "corrupted"}
    
    def close(self):
        """Safely close database."""
        try:
            if self.conn:
                self.conn.execute("PRAGMA optimize")
                self.conn.commit()
                self.conn.close()
                print("[✓] Database closed safely")
                logging.info("Database closed")
        except Exception as e:
            print(f"[!] Close failed: {e}")
            logging.error(f"Close failed: {e}")


# Initialize database
_db = CrawlerDB()

def save_page(url, html):
    """Save a crawled page to the database."""
    _db.save_page(url, html)

def get_stats():
    """Get database stats."""
    return _db.get_stats()

def close_db():
    """Close database connection."""
    _db.close()

def recover_from_backup():
    """Recover database from latest backup."""
    backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.endswith('.db')])
    if not backups:
        print("[✗] No backups found!")
        return False
    
    latest_backup = os.path.join(BACKUP_DIR, backups[-1])
    print(f"[+] Recovering from: {latest_backup}")
    
    try:
        _db.close()
        shutil.copy2(latest_backup, DB_PATH)
        _db._initialize_db()
        print("[✓] Database recovered")
        logging.info(f"Database recovered from {latest_backup}")
        return True
    except Exception as e:
        print(f"[✗] Recovery failed: {e}")
        return False
