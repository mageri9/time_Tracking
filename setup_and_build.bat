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

echo [1/4] Python found. Creating virtual environment...
"%PYTHON%" -m venv .venv

echo [2/4] Installing dependencies...
call .venv\Scripts\activate
"%PYTHON%" -m pip install -r requirements.txt --quiet

echo [3/4] Building Timer.exe...
"%PYTHON%" -m PyInstaller ^
    --noconfirm ^
    --noconsole ^
    --onefile ^
    --windowed ^
    --name Timer ^
    --add-data "_timer.ico;." ^
    --add-data "stopwatch\theme.py;stopwatch" ^
    --add-data "stopwatch\models.py;stopwatch" ^
    --add-data "stopwatch\views.py;stopwatch" ^
    --add-data "stopwatch\controllers.py;stopwatch" ^
    --add-data "stopwatch\single_instance.py;stopwatch" ^
    --add-data "stopwatch\tray.py;stopwatch" ^
    --add-data "stopwatch\utils.py;stopwatch" ^
    --hidden-import pystray ^
    --hidden-import PIL ^
    --hidden-import PIL.Image ^
    --hidden-import PIL.ImageDraw ^
    --hidden-import queue ^
    --collect-all pystray ^
    --collect-all PIL ^
    --icon=_timer.ico ^
    stopwatch\__main__.py

echo [4/4] Creating shortcut...
set "INSTALL_DIR=%USERPROFILE%\Timer"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

copy "dist\Timer.exe" "%INSTALL_DIR%\Timer.exe" >nul
copy "_timer.ico" "%INSTALL_DIR%\_timer.ico" >nul

REM Create shortcut using PowerShell
powershell -Command "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut('%USERPROFILE%\Desktop\Timer.lnk'); $SC.TargetPath = '%INSTALL_DIR%\Timer.exe'; $SC.IconLocation = '%INSTALL_DIR%\_timer.ico'; $SC.WorkingDirectory = '%INSTALL_DIR%'; $SC.Save()"

echo.
echo ========================================
echo  DONE!
echo    EXE: %INSTALL_DIR%\Timer.exe
echo    Shortcut: Desktop\Timer.lnk
echo ========================================
echo.

pause