Timer Mimer — Time Tracker for Freelancers (Python/Tkinter)
===========================================================

Made for personal use.

Features
--------
- Stopwatch with pause and reset
- Lap recording with JSON storage (laps_data.json)
- Lap statistics viewer
- Manual time entry (double-click to edit)

Requirements
------------
- Python 3.10+

Installation & Run
------------------
1. Clone or download the repository
2. Run:

   python -m stopwatch

Build .exe for Windows
----------------------
1. Install PyInstaller:

   pip install pyinstaller

2. Run:

   pyinstaller --noconfirm --noconsole --onefile --name TimerMimer -m stopwatch

3. Output file: dist\TimerMimer.exe

Controls
--------
▶ / ⏸ — start / pause
🔄      — reset timer
⏱️      — record lap / show statistics

Close
-----
If the stopwatch is running, a confirmation dialog will appear.

Manual Time Input
-----------------
Double-click on the timer display. Supported formats:
- HH:MM:SS
- MM:SS.hundredths
- Human-friendly: 70h, 1h30m, 90m15s, 30s (also with Russian letters)
- Plain number (treated as hours)

Project Structure
-----------------
timer_mimer/
  stopwatch/           — main module
  tests/               — unit tests
  dist/                — built .exe (created during build)
  build_exe.bat        — Windows build script
  README.txt           — this file (Russian)
  README_EN.txt        — English version

Tests
-----
python -m unittest

License
-------
MIT