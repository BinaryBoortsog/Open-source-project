"""
FastAPI web UI for onion crawler.
Displays discovered onions and crawler stats.
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="web/templates")

# Try to create static directory
import os
os.makedirs("web/static", exist_ok=True)


@app.get("/")
def index(request: Request):
    """Homepage with crawler stats and discovered onions."""
    try:
        conn = sqlite3.connect("onions.db")
        c = conn.cursor()
        
        # Get stats
        total = c.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
        recent = c.execute("SELECT url, crawled_at FROM pages ORDER BY crawled_at DESC LIMIT 50").fetchall()
        
        conn.close()
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "total_pages": total,
            "recent_urls": recent,
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": str(e),
            "total_pages": 0,
            "recent_urls": [],
        })


@app.get("/api/stats")
def api_stats():
    """API endpoint for crawler stats (JSON)."""
    try:
        conn = sqlite3.connect("onions.db")
        c = conn.cursor()
        
        total = c.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
        
        conn.close()
        
        return {"total_pages": total, "status": "running"}
    except Exception as e:
        return {"error": str(e), "status": "error"}
