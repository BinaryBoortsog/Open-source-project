#!/bin/bash
# Setup script for Tor Crawler on any machine

echo "========================================="
echo "Tor Crawler - Portable Setup"
echo "========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "[!] Docker is not installed."
    echo "    Please install Docker from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "[✓] Docker is installed"

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "[!] Docker daemon is not running."
    echo "    Please start Docker Desktop and try again."
    exit 1
fi

echo "[✓] Docker daemon is running"

# Create data directory if it doesn't exist
if [ ! -d "tor-crawler/data" ]; then
    echo "[+] Creating data directory..."
    mkdir -p tor-crawler/data
fi

echo "[✓] Data directory ready"

# Build Docker image
echo "[+] Building Docker image (this may take a few minutes)..."
docker compose build

if [ $? -ne 0 ]; then
    echo "[!] Docker build failed"
    exit 1
fi

echo "[✓] Docker image built successfully"

# Start containers
echo "[+] Starting containers..."
docker compose up -d

if [ $? -ne 0 ]; then
    echo "[!] Failed to start containers"
    exit 1
fi

echo "[✓] Containers started successfully"

# Wait for services to be ready
echo "[+] Waiting for services to start (10 seconds)..."
sleep 10

# Check if web server is running
if curl -s http://localhost:8000 &> /dev/null; then
    echo ""
    echo "========================================="
    echo "✓ Setup Complete!"
    echo "========================================="
    echo ""
    echo "Your Tor crawler is now running!"
    echo ""
    echo "Dashboard: http://localhost:8000"
    echo ""
    echo "Commands:"
    echo "  View logs:     docker compose logs -f tor-crawler"
    echo "  Stop:          docker compose down"
    echo "  Restart:       docker compose restart tor-crawler"
    echo "  Status:        docker compose ps"
    echo ""
else
    echo "[!] Web server not responding. Check logs:"
    echo "    docker compose logs tor-crawler"
    exit 1
fi
