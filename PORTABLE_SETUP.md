# Portable Setup Guide

## Requirements

- **Docker Desktop** (Windows/Mac) or **Docker** (Linux)
- **Git** (optional, for cloning)
- **4 GB RAM** minimum
- **2 GB disk space** for database

## Quick Start (Any OS)

### Windows
```bash
# Run setup script
setup.bat
```

### Mac/Linux
```bash
# Make script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

## Manual Setup

If the setup script doesn't work, follow these steps:

### 1. Install Docker
- **Windows/Mac:** [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux:** `sudo apt install docker.io docker-compose`

### 2. Start Docker
- **Windows/Mac:** Open Docker Desktop application
- **Linux:** `sudo systemctl start docker`

### 3. Build and Run
```bash
# Clone the project (if needed)
git clone https://github.com/BinaryBoortsog/Open-source-project.git
cd Open-source-project

# Build Docker image
docker compose build

# Start containers
docker compose up -d

# Wait 10 seconds, then open browser
# http://localhost:8000
```

## Common Commands

| Command | Purpose |
|---------|---------|
| `docker compose ps` | Check container status |
| `docker compose logs tor-crawler` | View crawler logs |
| `docker compose logs -f tor-crawler` | Live logs (Ctrl+C to stop) |
| `docker compose restart tor-crawler` | Restart crawler |
| `docker compose down` | Stop all containers |
| `docker compose up -d` | Start containers in background |

## Transferring to Another PC

### Option 1: Git Clone (Recommended)
```bash
git clone https://github.com/BinaryBoortsog/Open-source-project.git
cd Open-source-project
./setup.bat  # or setup.sh on Mac/Linux
```

### Option 2: USB Drive
1. Copy entire `Open-source-project` folder to USB
2. Plug USB into new PC
3. Run `setup.bat` (Windows) or `./setup.sh` (Mac/Linux)

### Option 3: Cloud (OneDrive/Google Drive)
1. Upload `Open-source-project` folder
2. Download on new PC
3. Run setup script

**Note:** Database (`tor-crawler/data/onions.db`) will be empty on new PC - crawler will rebuild it.

## Troubleshooting

### Docker not found
```bash
# Check Docker installation
docker --version

# If not installed, download from:
# https://www.docker.com/products/docker-desktop
```

### Port 8000 already in use
```bash
# Find what's using port 8000
# Then stop it, or edit docker-compose.yml to use different port

# Windows
netstat -ano | findstr :8000

# Mac/Linux
lsof -i :8000
```

### No internet connection
- Crawler requires Tor (included in Docker)
- Make sure Docker has internet access
- Check logs: `docker compose logs tor-crawler`

### Database errors
```bash
# Reset database
docker compose exec tor-crawler rm -f data/onions.db

# Restart
docker compose restart tor-crawler
```

## Persistence

All data is saved in `tor-crawler/data/`:
- `onions.db` - Main database (encrypted)
- `backups/` - Automatic backups
- `crawler_audit.log` - Activity log

Copy this folder to preserve your data when moving to another PC.

## Performance

- **RAM Usage:** ~300-500 MB
- **Disk Usage:** ~50 MB + database size
- **Network:** Runs through Tor (slower, for privacy)
- **CPU:** Low usage (mostly I/O wait)

## Security Notes

- ✅ All database operations are encrypted (Fernet)
- ✅ Tor routing (anonymous)
- ✅ No external API calls
- ⚠️ Keep Docker updated for security patches
- ⚠️ Encryption key is stored in `.gitignore` (not in repo)

## Support

For issues, check:
1. Docker logs: `docker compose logs tor-crawler`
2. Container status: `docker compose ps`
3. GitHub issues: https://github.com/BinaryBoortsog/Open-source-project/issues
