@echo off
title NEXORA [OMEGA] - Universal Adaptive Intelligence Runtime
cls
echo =====================================================================
echo           NEXORA [OMEGA] -- RUNTIME INITIALIZING...
echo =====================================================================
echo.

cd /d "%~dp0"
chcp 65001 >nul
set PYTHONIOENCODING=utf-8

echo [1/2] Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found on your PATH.
    pause
    exit /b 1
)

netstat -ano | findstr :8000 | findstr LISTENING >nul 2>&1
if %errorlevel% equ 0 (
    echo [NOTICE] Port 8000 is currently occupied by another process.
    echo [AUTO-RESOLVE] Routing to Port 8080 to prevent conflicts...
    set NEXORA_PORT=8080
) else (
    set NEXORA_PORT=8000
)

echo [2/2] Launching NEXORA Server on http://localhost:%NEXORA_PORT% ...
echo.
echo Dashboard URL:  http://localhost:%NEXORA_PORT%
echo API Docs:       http://localhost:%NEXORA_PORT%/docs
echo.
echo Opening Holographic Dashboard in your default browser...
start "" "http://localhost:%NEXORA_PORT%"
echo Press Ctrl+C in this terminal window to stop the runtime.
echo =====================================================================
echo.

python -m uvicorn backend.main:app --reload --port %NEXORA_PORT% --host 0.0.0.0
pause
