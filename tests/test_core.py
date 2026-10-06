import unittest

from tai_unix_offset import (
    LEAP_SECONDS,
    TAI_OFFSET,
    unix_to_tai,
    tai_to_unix,
)


class TestOffsetTable(unittest.TestCase):
    def test_known_offsets_present(self):
        last_ts, last_off = LEAP_SECONDS[-1]
        self.assertEqual(last_off, 37)

    def test_base_offset_is_8(self):
        self.assertEqual(TAI_OFFSET, 8)


class TestUnixToTai(unittest.TestCase):
    def test_epoch(self):
        self.assertEqual(unix_to_tai(0.0), 8.0)

    def test_well_before_any_leap(self):
        # 2000-01-01 predates the table (which starts 2015-07-01), so the
        # base offset of 8 applies.
        self.assertEqual(unix_to_tai(946684800), 946684800 + 8)

    def test_just_before_2017_leap(self):
        # One second before 2017-01-01T00:00:00Z. Offset is still 36.
        self.assertEqual(unix_to_tai(1483228799), 1483228799 + 36)

    def test_just_after_2017_leap(self):
        # The first normal second of 2017-01-01. Offset is now 37.
        self.assertEqual(unix_to_tai(1483228801), 1483228801 + 37)

    def test_nan_raises(self):
        with self.assertRaises(ValueError):
            unix_to_tai(float("nan"))


class TestTaiToUnix(unittest.TestCase):
    def test_round_trip_normal(self):
        u = 1500000000.0  # 2017-07, offset 37
        self.assertEqual(tai_to_unix(unix_to_tai(u)), u)

    def test_round_trip_pre_leap(self):
        u = 946684800.0  # 2000-01-01, offset 8 (predates table)
        self.assertEqual(tai_to_unix(unix_to_tai(u)), u)

    def test_nan_raises(self):
        with self.assertRaises(ValueError):
            tai_to_unix(float("nan"))

    def test_last_normal_second_before_2017_leap(self):
        # Unix 1483228799 is 2016-12-31T23:59:59Z. Offset before leap is 36.
        self.assertEqual(tai_to_unix(1483228799 + 36), 1483228799)

    def test_first_instant_of_leap_second(self):
        # The leap second begins at Unix B=1483228800. Per the README, the
        # pre-jump offset (36) is used at the start of the leap second, so
        # TAI = B + 36 maps to Unix B.
        self.assertEqual(tai_to_unix(1483228800 + 36), 1483228800)

    def test_second_instant_of_leap_second(self):
        # TAI one second into the leap second (B + 37) also maps to Unix B.
        self.assertEqual(tai_to_unix(1483228800 + 37), 1483228800)

    def test_first_normal_second_after_leap(self):
        # TAI = B + 38 corresponds to Unix B + 1 under the new offset of 37.
        self.assertEqual(tai_to_unix(1483228800 + 38), 1483228801)


if __name__ == "__main__":
    unittest.main()
