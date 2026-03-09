@echo off
REM Сборка Timer Mimer в один .exe через PyInstaller

REM 1. Проверяем, что установлен PyInstaller
pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo PyInstaller не найден. Установи его командой:
    echo.
    echo     pip install pyinstaller
    echo.
    pause
    exit /b 1
)

REM 2. Собираем exe из main.py
pyinstaller --noconfirm --noconsole --onefile --name TimerMimer main.py

echo.
echo Сборка завершена. Файл лежит в папке dist\TimerMimer.exe
pause

