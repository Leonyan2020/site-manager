@echo off
chcp 65001 >nul
echo ========================================
echo   Site Manager v2.0
echo ========================================
echo.
echo Starting application...
echo.

if exist venv\Scripts\python.exe (
    venv\Scripts\python.exe main.py
) else (
    python main.py
)

if errorlevel 1 (
    echo.
    echo Application error occurred!
    pause
)
