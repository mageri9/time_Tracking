import re


def format_time(amount: float, include_hours: bool = False) -> str:
    """Форматирует время в строки.

    По умолчанию: ММ:СС.сотые
    При include_hours=True: ЧЧ:ММ:СС
    """
    hours = int(amount // 3600)
    minutes = int((amount % 3600) // 60)
    seconds = int(amount % 60)
    hundredths = int((amount * 100) % 100)

    if include_hours:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}.{hundredths:02d}"


def parse_time(time_str: str) -> float:
    """Парсит строку времени в секунды.

    Поддерживаемые форматы:
    - ЧЧ:ММ:СС
    - ММ:СС.сотые
    - "человеческие": 70h, 1h30m, 90m15s, 30s (также с пробелами)
    """
    s = time_str.strip()

    # "Человеческий" формат с буквами h/m/s (поддержим и русские ч/м/с)
    if any(ch in s for ch in "hmsHMSчЧмМсС"):
        pattern = r"""^\s*
            (?:(\d+)\s*[hHчЧ])?\s*
            (?:(\d+)\s*[mMмМ])?\s*
            (?:(\d+)\s*[sSсС])?\s*$
        """
        match = re.match(pattern, s, re.VERBOSE)
        if match and any(g is not None for g in match.groups()):
            hours = int(match.group(1) or 0)
            minutes = int(match.group(2) or 0)
            seconds = int(match.group(3) or 0)
            return hours * 3600 + minutes * 60 + seconds

    parts = s.split(":")

    # Формат ЧЧ:ММ:СС
    if len(parts) == 3:
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        return hours * 3600 + minutes * 60 + seconds

    # Формат ММ:СС.сотые
    if len(parts) == 2:
        minutes = int(parts[0])
        sec_parts = parts[1].split(".")
        seconds = int(sec_parts[0])
        hundredths = int(sec_parts[1]) if len(sec_parts) > 1 else 0
        return minutes * 60 + seconds + hundredths / 100

    # Только число без букв и двоеточий — считаем часами (для крупных значений)
    digits = s.replace(" ", "")
    if digits.isdigit():
        hours = int(digits)
        return hours * 3600

    raise ValueError("Неверный формат времени")

