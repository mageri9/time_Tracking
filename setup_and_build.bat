@echo off
REM =============================================
REM  League Timer — Setup, Build & Autostart
REM  One-click for non-programmers
REM =============================================

echo.
echo ========================================
echo  League Timer - Setup & Build
echo ========================================
echo.

REM Find Python
set PYTHON=
for %%p in (
    "python"
    "python3"
    "%LocalAppData%\Programs\Python\Python313\python.exe"
    "%LocalAppData%\Programs\Python\Python312\python.exe"
    "%LocalAppData%\Programs\Python\Python311\python.exe"
    "C:\Python313\python.exe"
    "C:\Python312\python.exe"
    "C:\Python311\python.exe"
) do (
    if "%PYTHON%"=="" (
        %%p --version >nul 2>&1
        if not errorlevel 1 set PYTHON=%%p
    )
)

if "%PYTHON%"=="" (
    echo Python not found!
    echo.
    echo 1. Download Python 3.10+ from https://www.python.org/downloads/
    echo 2. Run the installer
    echo 3. CHECK "Add Python to PATH"
    echo 4. Run this script again
    echo.
    pause
    exit /b 1
)

echo [1/5] Python found. Creating virtual environment...
"%PYTHON%" -m venv .venv

echo [2/5] Installing dependencies...
call .venv\Scripts\activate
"%PYTHON%" -m pip install -r requirements.txt --quiet

echo [3/5] Building LeagueTimer.exe...
"%PYTHON%" -m PyInstaller ^
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
    stopwatch\__main__.py

echo [4/5] Building LeagueWatcher.exe...
"%PYTHON%" -m PyInstaller ^
    --noconfirm ^
    --noconsole ^
    --onefile ^
    --name LeagueWatcher ^
    --hidden-import psutil ^
    watcher.py

echo.
echo ========================================
echo  DONE!
echo    dist\LeagueTimer.exe
echo    dist\LeagueWatcher.exe
echo ========================================
echo.

REM Autostart
echo.
echo Add to Windows autostart?
echo   [1] LeagueTimer only (timer runs in tray, waits for game)
echo   [2] LeagueWatcher only (watcher launches timer when needed)
echo   [3] Nothing
echo.
set /p AUTOSTART="Choose (1/2/3): "

if "%AUTOSTART%"=="1" (
    echo Creating shortcut for LeagueTimer...
    powershell -Command ^
        "$startup = [Environment]::GetFolderPath('Startup');" ^
        "$shortcut = Join-Path $startup 'LeagueTimer.lnk';" ^
        "$ws = New-Object -ComObject WScript.Shell;" ^
        "$s = $ws.CreateShortcut($shortcut);" ^
        "$s.TargetPath = '%CD%\dist\LeagueTimer.exe';" ^
        "$s.Arguments = '--minimized';" ^
        "$s.WorkingDirectory = '%CD%\dist';" ^
        "$s.Save();" ^
        "Write-Host 'Shortcut created:' $shortcut"
    echo Done! League Timer will start with Windows.
)

if "%AUTOSTART%"=="2" (
    echo Creating shortcut for LeagueWatcher...
    powershell -Command ^
        "$startup = [Environment]::GetFolderPath('Startup');" ^
        "$shortcut = Join-Path $startup 'LeagueWatcher.lnk';" ^
        "$ws = New-Object -ComObject WScript.Shell;" ^
        "$s = $ws.CreateShortcut($shortcut);" ^
        "$s.TargetPath = '%CD%\dist\LeagueWatcher.exe';" ^
        "$s.WorkingDirectory = '%CD%\dist';" ^
        "$s.Save();" ^
        "Write-Host 'Shortcut created:' $shortcut"
    echo Done! League Watcher will start with Windows.
    echo.
    echo IMPORTANT: LeagueTimer.exe and LeagueWatcher.exe must be in the same folder!
)

if not "%AUTOSTART%"=="1" if not "%AUTOSTART%"=="2" (
    echo Skipping autostart.
)

echo.
pause