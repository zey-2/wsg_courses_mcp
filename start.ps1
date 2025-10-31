# Start script for WSG MCP Server
# Usage: .\start.ps1

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Starting WSG Courses API MCP Server" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if conda environment exists
$envExists = conda env list | Select-String "wsg-courses-mcp-dev"
if (-not $envExists) {
    Write-Host "Error: Conda environment 'wsg-courses-mcp-dev' not found" -ForegroundColor Red
    Write-Host "Please run: conda env create -f environment-dev.yml" -ForegroundColor Yellow
    exit 1
}

Write-Host "Environment: wsg-courses-mcp-dev" -ForegroundColor Green
Write-Host "Starting server on http://localhost:8000" -ForegroundColor Green
Write-Host ""
Write-Host "Available endpoints:" -ForegroundColor Yellow
Write-Host "  - Swagger UI:   http://localhost:8000/docs" -ForegroundColor White
Write-Host "  - ReDoc:        http://localhost:8000/redoc" -ForegroundColor White
Write-Host "  - Health check: http://localhost:8000/health" -ForegroundColor White
Write-Host "  - MCP endpoint: http://localhost:8000/mcp" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Start the server using conda run
conda run -n wsg-courses-mcp-dev python main.py
