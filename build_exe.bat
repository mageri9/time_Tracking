@echo off
REM Сборка Timer Mimer в один .exe через PyInstaller

pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo PyInstaller не найден. Установи его командой:
    echo.
    echo     pip install pyinstaller
    echo.
    pause
    exit /b 1
)

REM Собираем из модуля stopwatch
pyinstaller --noconfirm --noconsole --onefile --name TimerMimer -m stopwatch

echo.
echo Сборка завершена. Файл лежит в папке dist\TimerMimer.exe
pause
