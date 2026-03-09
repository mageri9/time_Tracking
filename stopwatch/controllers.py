import json
import os
import time
from typing import Dict, Literal

from .models import StopwatchState
from .utils import parse_time


LapResultType = Literal["stats", "recorded"]


class StopwatchController:
    """Логика секундомера, независимая от GUI."""

    def __init__(self, data_file: str = "laps_data.json") -> None:
        self.state = StopwatchState()
        self.data_file = data_file
        self.load_laps()

    # --- Основные действия ---

    def start(self) -> None:
        """Запускает секундомер (или продолжает после паузы)."""
        if not self.state.running:
            self.state.running = True
            self.state.start_time = time.time() - self.state.elapsed_time

    def stop(self) -> None:
        """Останавливает секундомер (пауза)."""
        if self.state.running:
            self.state.running = False
            self.state.elapsed_time = time.time() - self.state.start_time

    def reset(self) -> str:
        """Сбрасывает время с возможностью отмены.

        Возвращает один из вариантов:
        - "restored" — восстановили сохранённое время
        - "saved"    — сохранили текущее время, таймер сброшен
        - "nothing"  — нечего сбрасывать
        """
        current_time = self.state.current_time

        if current_time == 0.0 and self.state.has_saved_time:
            # Второе нажатие — возвращаем сохранёнку
            self.state.elapsed_time = self.state.saved_time
            self.state.saved_time = 0.0
            return "restored"

        if current_time > 0:
            # Первое нажатие — сохраняем текущее время
            self.state.saved_time = current_time
            self.state.running = False
            self.state.elapsed_time = 0.0
            return "saved"

        # Время 0 и сохранёнки нет — просто сброс
        return "nothing"

    def clear(self) -> None:
        """Полный сброс времени без сохранения."""
        self.state.running = False
        self.state.start_time = 0.0
        self.state.elapsed_time = 0.0

    def lap(self) -> Dict[str, float | LapResultType]:
        """Записывает круг или возвращает статистику.

        Возвращает словарь:
        - {"type": "stats", "total": ..., "avg": ...}
        - {"type": "recorded", "elapsed": ...}
        """
        if (
            not self.state.running
            and self.state.elapsed_time == 0.0
            and self.state.has_laps
        ):
            total = sum(self.state.laps)
            avg = total / len(self.state.laps)
            return {"type": "stats", "total": total, "avg": avg}

        self.stop()
        elapsed = self.state.elapsed_time
        self.state.laps.append(elapsed)
        self.save_laps()
        self.clear()
        return {"type": "recorded", "elapsed": elapsed}

    # --- Ввод/вывод времени ---

    def set_elapsed_from_str(self, time_str: str) -> None:
        """Устанавливает elapsed_time из строки времени."""
        self.state.elapsed_time = parse_time(time_str)

    # --- Работа с файлами ---

    def save_laps(self) -> None:
        """Сохраняет круги в JSON-файл."""
        with open(self.data_file, "w") as f:
            json.dump(self.state.laps, f, indent=2)

    def load_laps(self) -> None:
        """Загружает круги из JSON-файла."""
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.state.laps = json.load(f)
        else:
            self.state.laps = []

