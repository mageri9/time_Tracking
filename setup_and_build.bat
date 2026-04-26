@echo off
REM =============================================
REM  League Timer — установка и сборка в один клик
REM  Для тех, кто никогда не видел Python
REM =============================================

echo.
echo ========================================
echo  League Timer - Установка и сборка
echo ========================================
echo.

REM 1. Ищем Python
where python >nul 2>&1
if errorlevel 1 (
    echo Python не найден!
    echo Скачай с https://www.python.org/downloads/
    echo При установке ОБЯЗАТЕЛЬНО поставь галочку "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo [1/3] Python найден. Создаю окружение...
python -m venv .venv

echo [2/3] Устанавливаю зависимости...
call .venv\Scripts\activate
pip install -r requirements.txt --quiet

echo [3/3] Собираю LeagueTimer.exe...
python -m PyInstaller ^
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
echo  ГОТОВО! Запускай: dist\LeagueTimer.exe
echo ========================================
echo.
pause