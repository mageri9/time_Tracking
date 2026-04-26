import os
import sys
import tempfile

LOCK_NAME = "league_timer.lock"

def get_lock_path() -> str:
    """Путь к файлу-локу в TEMP."""
    return os.path.join(tempfile.gettempdir(), LOCK_NAME)

def already_running() -> bool:
    """True, если другой экземпляр уже запущен и жив."""
    lock_path = get_lock_path()

    if not os.path.exists(lock_path):
        return False

    try:
        with open(lock_path, "r") as f:
            pid = int(f.read().strip())
    except (ValueError, OSError):
        return False

    try:
        import psutil
        psutil.Process(pid)
        return True
    except (psutil.NoSuchProcess, Exception):
        return False

def create_lock() -> None:
    """Создаёт файл-лок с текущим PID."""
    lock_path = get_lock_path()
    with open(lock_path, "w") as f:
        f.write(str(os.getpid()))

def remove_lock() -> None:
    """Удаляет файл-лок."""
    lock_path = get_lock_path()
    try:
        os.remove(lock_path)
    except OSError:
        pass