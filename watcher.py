import os
import subprocess
import sys
import time

import psutil

LEAGUE_PROCESSES = [
    "LeagueClientUx.exe",
    "League of Legends.exe",
]

CHECK_INTERVAL = 10

TIMER_EXE = "LeagueTimer.exe"

def find_timer_path() -> str | None:
    """Ищет LeagueTimer.exe рядом с watcher'ом или в PATH."""
    own_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    nearby = os.path.join(own_dir, TIMER_EXE)
    if os.path.isfile(nearby):
        return nearby

    # Ищем в папке dist/ рядом (если запущен из исходников)
    dist_path = os.path.join(own_dir, "dist", TIMER_EXE)
    if os.path.isfile(dist_path):
        return dist_path

    return None


def is_timer_running() -> bool:
    """Проверяет, запущен ли уже LeagueTimer.exe."""
    for proc in psutil.process_iter(["name"]):
        try:
            if proc.info["name"] == TIMER_EXE:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


def is_league_running() -> bool:
    """Проверяет, запущен ли клиент или игра LoL."""
    for proc in psutil.process_iter(["name"]):
        try:
            if proc.info["name"] in LEAGUE_PROCESSES:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def is_watcher_already_running() -> bool:
    """Проверяет, не запущен ли уже LeagueWatcher.exe."""
    current_pid = os.getpid()
    for proc in psutil.process_iter(["name", "pid"]):
        try:
            if proc.info["name"] == "LeagueWatcher.exe" and proc.info["pid"] != current_pid:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


def main() -> None:
    """Основной цикл: спим, проверяем, запускаем."""
    if is_watcher_already_running():
        sys.exit(0)
    timer_path = find_timer_path()
    if timer_path is None:
        # Нет смысла работать без таймера
        sys.exit(1)

    while True:
        try:
            if is_league_running() and not is_timer_running():
                subprocess.Popen(
                    [timer_path, "--minimized"],
                    creationflags=subprocess.CREATE_NO_WINDOW
                    if sys.platform == "win32"
                    else 0,
                )
        except Exception:
            pass  # Не даём сторожу упасть

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()