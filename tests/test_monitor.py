import unittest
from unittest.mock import patch

import psutil


class FakeProcess:
    def __init__(self, name: str):
        self.info = {"name": name}


class TestMonitor(unittest.TestCase):

    def test_league_client_running(self) -> None:
        from stopwatch.monitor import is_league_running
        procs = [FakeProcess("LeagueClientUx.exe")]
        with patch("stopwatch.monitor._get_processes", return_value=procs):
            self.assertTrue(is_league_running())

    def test_league_game_running(self) -> None:
        from stopwatch.monitor import is_league_running
        procs = [FakeProcess("League of Legends.exe")]
        with patch("stopwatch.monitor._get_processes", return_value=procs):
            self.assertTrue(is_league_running())

    def test_both_running(self) -> None:
        from stopwatch.monitor import is_league_running
        procs = [
            FakeProcess("LeagueClientUx.exe"),
            FakeProcess("League of Legends.exe"),
        ]
        with patch("stopwatch.monitor._get_processes", return_value=procs):
            self.assertTrue(is_league_running())

    def test_league_not_running(self) -> None:
        from stopwatch.monitor import is_league_running
        procs = [
            FakeProcess("notepad.exe"),
            FakeProcess("chrome.exe"),
        ]
        with patch("stopwatch.monitor._get_processes", return_value=procs):
            self.assertFalse(is_league_running())

    def test_empty_process_list(self) -> None:
        from stopwatch.monitor import is_league_running
        with patch("stopwatch.monitor._get_processes", return_value=[]):
            self.assertFalse(is_league_running())

    def test_access_denied_skipped(self) -> None:
        from stopwatch.monitor import is_league_running

        class BadProcess:
            @property
            def info(self):
                raise psutil.AccessDenied("pid=1")

        procs = [BadProcess(), FakeProcess("LeagueClientUx.exe")]
        with patch("stopwatch.monitor._get_processes", return_value=procs):
            self.assertTrue(is_league_running())


if __name__ == "__main__":
    unittest.main()