@echo off
REM Site Manager Build Script
echo Starting to build Site Manager...

REM Check if dependencies are installed
python -c "import PySide6" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Build with PyInstaller
echo Building executable file...
pyinstaller --name="SiteManager" ^
    --onefile ^
    --windowed ^
    --icon=asww.ico ^
    --add-data="asww.ico;." ^
    main.py

echo.
echo Build completed!
echo Executable location: dist\SiteManager.exe
echo.
pause
