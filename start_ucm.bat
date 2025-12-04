@echo off
echo Starting UCM Cognitive Architecture...
echo.

REM Check if Docker is running
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker Desktop and ensure it's running
    pause
    exit /b 1
)

REM Start the services
echo Starting Docker services...
docker-compose up -d

REM Wait a moment for services to start
timeout /t 5 /nobreak >nul

REM Check service status
echo.
echo Checking service status...
docker-compose ps

REM Open monitoring dashboard
echo.
echo Opening monitoring dashboard...
start http://localhost:3000

echo.
echo UCM System started successfully!
echo - API endpoints available at http://localhost:8000
echo - Monitoring dashboard at http://localhost:3000
echo - Voice consent API at http://localhost:8080
echo.
echo Press any key to continue...
pause >nul