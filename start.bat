@echo off
REM Start script for WSG MCP Server

echo ============================================================
echo Starting WSG Courses API MCP Server
echo ============================================================
echo.

REM Activate conda environment and start server
call conda activate wsg-courses-mcp-dev
if %errorlevel% neq 0 (
    echo Error: Failed to activate conda environment wsg-courses-mcp-dev
    echo Please run: conda env create -f environment-dev.yml
    pause
    exit /b 1
)

echo Environment: wsg-courses-mcp-dev activated
echo Starting server on http://localhost:8000
echo.
echo Available endpoints:
echo   - Swagger UI:   http://localhost:8000/docs
echo   - ReDoc:        http://localhost:8000/redoc
echo   - Health check: http://localhost:8000/health
echo   - MCP endpoint: http://localhost:8000/mcp
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

REM Start the server
python main.py
