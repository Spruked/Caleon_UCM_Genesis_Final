# UCM System Startup Script
param(
    [switch]$NoBrowser,
    [switch]$Verbose
)

Write-Host "Starting UCM Cognitive Architecture..." -ForegroundColor Green
Write-Host ""

# Check Docker
try {
    $dockerVersion = docker --version 2>$null
    if ($LASTEXITCODE -ne 0) { throw "Docker not found" }
    Write-Host "✓ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Docker is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Docker Desktop and ensure it's running" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Start services
Write-Host "Starting Docker services..." -ForegroundColor Cyan
try {
    docker-compose up -d 2>$null
    if ($LASTEXITCODE -ne 0) { throw "Failed to start services" }
} catch {
    Write-Host "✗ Failed to start Docker services" -ForegroundColor Red
    Write-Host "Try running: docker-compose up -d manually" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Wait for services
Start-Sleep -Seconds 5

# Check status
Write-Host ""
Write-Host "Checking service status..." -ForegroundColor Cyan
docker-compose ps

# Open dashboard
if (-not $NoBrowser) {
    Write-Host ""
    Write-Host "Opening monitoring dashboard..." -ForegroundColor Cyan
    Start-Process "http://localhost:3000"
}

Write-Host ""
Write-Host "UCM System started successfully!" -ForegroundColor Green
Write-Host "• API endpoints: http://localhost:8000" -ForegroundColor White
Write-Host "• Monitoring dashboard: http://localhost:3000" -ForegroundColor White
Write-Host "• Voice consent API: http://localhost:8080" -ForegroundColor White

if ($Verbose) {
    Write-Host ""
    Write-Host "Available services:" -ForegroundColor Cyan
    docker-compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
}

Write-Host ""
Read-Host "Press Enter to continue"