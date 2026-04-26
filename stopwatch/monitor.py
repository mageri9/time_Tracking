import psutil

# Для теста без LoL — замена на ["notepad.exe"]
LEAGUE_PROCESS = [
    "notepad.exe",
]

def is_league_running() -> bool:
    """Возвращает True, если процесс Лиги запущен."""
    for proc in psutil.process_iter(["name"]):
        try:
            if proc.info["name"] in LEAGUE_PROCESS:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False