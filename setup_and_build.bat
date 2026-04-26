@echo off
REM =============================================
REM  League Timer — установка, сборка и автозагрузка
REM  Для тех, кто никогда не видел Python
REM =============================================

echo.
echo ========================================
echo  League Timer - Установка и сборка
echo ========================================
echo.

REM Ищем Python
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
    echo Python не найден!
    echo.
    echo 1. Скачай Python 3.10+ с https://www.python.org/downloads/
    echo 2. Запусти установщик
    echo 3. ОБЯЗАТЕЛЬНО поставь галочку "Add Python to PATH"
    echo 4. Запусти этот батник ещё раз
    echo.
    pause
    exit /b 1
)

echo [1/4] Python найден. Создаю виртуальное окружение...
"%PYTHON%" -m venv .venv

echo [2/4] Устанавливаю зависимости...
call .venv\Scripts\activate
"%PYTHON%" -m pip install -r requirements.txt --quiet

echo [3/4] Собираю LeagueTimer.exe...
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

echo.
echo ========================================
echo  ГОТОВО! dist\LeagueTimer.exe
echo ========================================
echo.

REM Автозагрузка
set /p AUTOSTART="Добавить в автозагрузку? (Y/N): "
if /i "%AUTOSTART%"=="Y" (
    echo Создаю ярлык в автозагрузке...

    powershell -Command ^
        "$startup = [Environment]::GetFolderPath('Startup');" ^
        "$shortcut = Join-Path $startup 'LeagueTimer.lnk';" ^
        "$ws = New-Object -ComObject WScript.Shell;" ^
        "$s = $ws.CreateShortcut($shortcut);" ^
        "$s.TargetPath = '%CD%\dist\LeagueTimer.exe';" ^
        "$s.Arguments = '--minimized';" ^
        "$s.WorkingDirectory = '%CD%\dist';" ^
        "$s.Save();" ^
        "Write-Host 'Ярлык создан:' $shortcut"

    echo Готово! League Timer будет запускаться при старте Windows.
) else (
    echo Пропускаем автозагрузку.
)

echo.
pause