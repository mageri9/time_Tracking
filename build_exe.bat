@echo off
REM Сборка для тех, у кого уже настроено окружение
call .venv\Scripts\activate
python -m PyInstaller ^
    --noconfirm ^
    --noconsole ^
    --onefile ^
    --name LeagueTimer ^
    --add-data "_timer.ico;." ^
    --hidden-import pystray ^
    --hidden-import PIL ^
    --hidden-import PIL.Image ^
    --hidden-import PIL.ImageDraw ^
    --hidden-import queue ^
    --icon=_timer.ico ^
    stopwatch\__main__.py

echo.
echo Сборка завершена: dist\Timer.exe
pause