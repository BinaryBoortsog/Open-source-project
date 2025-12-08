@echo off
REM Setup script for Tor Crawler on Windows

echo =========================================
echo Tor Crawler - Portable Setup
echo =========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Docker is not installed.
    echo     Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo [+] Docker is installed

REM Check if Docker daemon is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Docker daemon is not running.
    echo     Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo [+] Docker daemon is running

REM Create data directory if it doesn't exist
if not exist "tor-crawler\data" (
    echo [+] Creating data directory...
    mkdir tor-crawler\data
)

echo [+] Data directory ready

REM Build Docker image
echo [+] Building Docker image (this may take a few minutes)...
docker compose build

if %errorlevel% neq 0 (
    echo [!] Docker build failed
    pause
    exit /b 1
)

echo [+] Docker image built successfully

REM Start containers
echo [+] Starting containers...
docker compose up -d

if %errorlevel% neq 0 (
    echo [!] Failed to start containers
    pause
    exit /b 1
)

echo [+] Containers started successfully

REM Wait for services to be ready
echo [+] Waiting for services to start (10 seconds)...
timeout /t 10 /nobreak

REM Check if web server is running
curl -s http://localhost:8000 >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo =========================================
    echo [+] Setup Complete!
    echo =========================================
    echo.
    echo Your Tor crawler is now running!
    echo.
    echo Dashboard: http://localhost:8000
    echo.
    echo Commands:
    echo   View logs:     docker compose logs -f tor-crawler
    echo   Stop:          docker compose down
    echo   Restart:       docker compose restart tor-crawler
    echo   Status:        docker compose ps
    echo.
) else (
    echo [!] Web server not responding. Check logs:
    echo     docker compose logs tor-crawler
    pause
    exit /b 1
)

pause
