@echo off
REM Сборка LeagueWatcher.exe
call .venv\Scripts\activate
python -m PyInstaller ^
    --noconfirm ^
    --noconsole ^
    --onefile ^
    --name LeagueWatcher ^
    --hidden-import psutil ^
    --icon=league_timer.ico ^
    watcher.py

echo.
echo Готово: dist\LeagueWatcher.exe
pause