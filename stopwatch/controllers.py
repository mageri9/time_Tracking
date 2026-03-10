import json
import os
import time
from dataclasses import asdict
from datetime import datetime, timedelta
from typing import Dict, List, Literal

from .models import LapRecord, SessionRecord, StopwatchState
from .utils import parse_time


LapResultType = Literal["stats", "recorded"]


class StopwatchController:
    """Логика секундомера, независимая от GUI."""

    def __init__(self, data_file: str = "laps_data.json") -> None:
        self.state = StopwatchState()
        self.data_file = data_file
        self.sessions: List[SessionRecord] = []
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

        now = datetime.now()
        finished_at = now.isoformat(timespec="seconds")
        started_at = (now - timedelta(seconds=elapsed)).isoformat(timespec="seconds")

        lap_record = LapRecord(seconds=elapsed, recorded_at=finished_at)
        session = SessionRecord(
            id=finished_at,
            started_at=started_at,
            finished_at=finished_at,
            total_seconds=elapsed,
            laps=[lap_record],
        )

        self.sessions.append(session)
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
        """Сохраняет сессии и круги в JSON-файл."""
        payload = {
            "version": 1,
            "sessions": [asdict(session) for session in self.sessions],
        }
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    def load_laps(self) -> None:
        """Загружает сессии и круги из JSON-файла.

        Поддерживает два формата:
        - новый: {"version": 1, "sessions": [...]}
        - старый: [seconds, seconds, ...] — список длительностей кругов
        """
        self.sessions = []
        self.state.laps = []

        if not os.path.exists(self.data_file):
            return

        with open(self.data_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Новый формат с сессиями
        if isinstance(data, dict) and "sessions" in data:
            for sess in data.get("sessions", []):
                laps_data = sess.get("laps", [])
                laps = [
                    LapRecord(
                        seconds=float(lap.get("seconds", 0.0)),
                        recorded_at=str(lap.get("recorded_at", "")),
                    )
                    for lap in laps_data
                ]
                session = SessionRecord(
                    id=str(sess.get("id", "")),
                    started_at=str(sess.get("started_at", "")),
                    finished_at=str(sess.get("finished_at", "")),
                    total_seconds=float(sess.get("total_seconds", 0.0)),
                    laps=laps,
                    note=str(sess.get("note", "")),
                    tags=list(sess.get("tags", [])),
                )
                self.sessions.append(session)
                for lap in laps:
                    self.state.laps.append(lap.seconds)
            return

        # Старый формат: просто список длительностей кругов
        if isinstance(data, list):
            now = datetime.now()
            for seconds in data:
                try:
                    value = float(seconds)
                except (TypeError, ValueError):
                    continue
                finished_at = now.isoformat(timespec="seconds")
                lap_record = LapRecord(seconds=value, recorded_at=finished_at)
                session = SessionRecord(
                    id=finished_at,
                    started_at=finished_at,
                    finished_at=finished_at,
                    total_seconds=value,
                    laps=[lap_record],
                )
                self.sessions.append(session)
                self.state.laps.append(value)

