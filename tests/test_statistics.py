import unittest
from datetime import datetime, timedelta

from stopwatch.controllers import StopwatchController


class TestStatistics(unittest.TestCase):
    """Проверяет методы get_stats_today, get_stats_week, get_stats_total."""

    def setUp(self) -> None:
        """Создаём контроллер с тестовыми сессиями вручную."""
        self.controller = StopwatchController(":memory:")  # не пишем в файл
        self.controller.sessions = []

    def _add_session(self, days_ago: int, seconds: float) -> None:
        """Добавляет тестовую сессию с заданным смещением в днях."""
        from stopwatch.models import LapRecord, SessionRecord

        now = datetime.now()
        session_time = now - timedelta(days=days_ago)
        finished_at = session_time.isoformat(timespec="seconds")
        started_at = (session_time - timedelta(seconds=seconds)).isoformat(
            timespec="seconds"
        )

        lap = LapRecord(seconds=seconds, recorded_at=finished_at)
        session = SessionRecord(
            id=finished_at,
            started_at=started_at,
            finished_at=finished_at,
            total_seconds=seconds,
            laps=[lap],
        )
        self.controller.sessions.append(session)

    # --- Тесты ---

    def test_total_zero_when_empty(self) -> None:
        self.assertEqual(self.controller.get_stats_total(), 0.0)

    def test_total_sums_all_sessions(self) -> None:
        self._add_session(0, 100.0)
        self._add_session(1, 200.0)
        self._add_session(10, 300.0)
        self.assertEqual(self.controller.get_stats_total(), 600.0)

    def test_today_only_today(self) -> None:
        self._add_session(0, 100.0)   # сегодня
        self._add_session(1, 200.0)   # вчера
        self._add_session(0, 50.0)    # сегодня
        self.assertEqual(self.controller.get_stats_today(), 150.0)

    def test_today_zero_when_no_today_sessions(self) -> None:
        self._add_session(1, 100.0)
        self._add_session(2, 200.0)
        self.assertEqual(self.controller.get_stats_today(), 0.0)

    def test_week_includes_last_7_days(self) -> None:
        self._add_session(0, 100.0)  # сегодня
        self._add_session(3, 200.0)  # 3 дня назад
        self._add_session(6, 300.0)  # 6 дней назад
        self._add_session(8, 400.0)  # 8 дней назад (не входит)
        self.assertEqual(self.controller.get_stats_week(), 600.0)

    def test_week_zero_when_no_recent_sessions(self) -> None:
        self._add_session(8, 100.0)
        self._add_session(30, 200.0)
        self.assertEqual(self.controller.get_stats_week(), 0.0)

    def test_negative_seconds_handled(self) -> None:
        """Отрицательное время (баг ручного ввода) — суммируется как есть."""
        self._add_session(0, -100.0)
        self.assertEqual(self.controller.get_stats_total(), -100.0)


if __name__ == "__main__":
    unittest.main()