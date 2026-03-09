import unittest

from stopwatch.utils import format_time, parse_time


class TestTimeUtils(unittest.TestCase):
    def test_format_time_minutes_seconds_hundredths(self) -> None:
        # 90.25 секунд = 1 минута 30.25
        self.assertEqual(format_time(90.25), "01:30.25")

    def test_format_time_with_hours(self) -> None:
        # 1 час 2 минуты 3 секунды
        self.assertEqual(format_time(3723, include_hours=True), "01:02:03")

    def test_parse_time_classic_hours(self) -> None:
        self.assertAlmostEqual(parse_time("01:02:03"), 3723)

    def test_parse_time_minutes_seconds_hundredths(self) -> None:
        self.assertAlmostEqual(parse_time("01:30.25"), 90.25)

    def test_parse_time_human_hours(self) -> None:
        self.assertAlmostEqual(parse_time("70h"), 70 * 3600)
        self.assertAlmostEqual(parse_time("70ч"), 70 * 3600)

    def test_parse_time_human_hours_minutes(self) -> None:
        self.assertAlmostEqual(parse_time("1h30m"), 1 * 3600 + 30 * 60)
        self.assertAlmostEqual(parse_time("1ч30м"), 1 * 3600 + 30 * 60)

    def test_parse_time_human_minutes_seconds(self) -> None:
        self.assertAlmostEqual(parse_time("90m15s"), 90 * 60 + 15)
        self.assertAlmostEqual(parse_time("90м15с"), 90 * 60 + 15)

    def test_parse_time_human_seconds_only(self) -> None:
        self.assertAlmostEqual(parse_time("30s"), 30)
        self.assertAlmostEqual(parse_time("30с"), 30)

    def test_parse_time_plain_number_as_hours(self) -> None:
        self.assertAlmostEqual(parse_time("70"), 70 * 3600)

    def test_parse_time_invalid_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_time("abc")


if __name__ == "__main__":
    unittest.main()

