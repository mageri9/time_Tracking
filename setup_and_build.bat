@echo off
REM =============================================
REM  Timer — Setup & Build
REM  One-click for non-programmers
REM =============================================

echo.
echo ========================================
echo  Timer - Setup & Build
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

echo [1/3] Python found. Creating virtual environment...
"%PYTHON%" -m venv .venv

echo [2/3] Installing dependencies...
call .venv\Scripts\activate
"%PYTHON%" -m pip install -r requirements.txt --quiet

echo [3/3] Building Timer.exe...
"%PYTHON%" -m PyInstaller ^
    --noconfirm ^
    --noconsole ^
    --onefile ^
    --name Timer ^
    --add-data "_timer.ico;." ^
    --hidden-import pystray ^
    --hidden-import PIL ^
    --hidden-import PIL.Image ^
    --hidden-import PIL.ImageDraw ^
    --hidden-import queue ^
    --icon=_timer.ico ^
    stopwatch\__main__.py

echo.
echo ========================================
echo  DONE!
echo    dist\Timer.exe
echo ========================================
echo.

echo.
pause