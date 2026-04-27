import psutil

LEAGUE_PROCESSES = [
    "League of Legends.exe",
]


def _get_processes():
    """Обёртка для psutil.process_iter (для тестирования)."""
    return psutil.process_iter(["name"])


def is_league_running() -> bool:
    """Возвращает True, если хотя бы один процесс Лиги запущен."""
    for proc in _get_processes():
        try:
            if proc.info["name"] in LEAGUE_PROCESSES:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False