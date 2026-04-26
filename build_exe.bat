@echo off
REM Сборка League Timer в один .exe через PyInstaller

pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo PyInstaller не найден. Установи:
    echo.
    echo     pip install pyinstaller
    echo.
    pause
    exit /b 1
)

pyinstaller ^
    --noconfirm ^
    --noconsole ^
    --onefile ^
    --name LeagueTimer ^
    --add-data "league_timer.ico;." ^
    --hidden-import pystray ^
    --hidden-import PIL ^
    --hidden-import PIL.Image ^
    --hidden-import PIL.ImageDraw ^
    --hidden-import psutil ^
    --hidden-import queue ^
    --icon=league_timer.ico ^
    -m stopwatch

echo.
echo Сборка завершена: dist\LeagueTimer.exe
pause