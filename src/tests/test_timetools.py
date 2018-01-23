from unittest import TestCase

from lib.core.timetools import Timetools


class TestTimetools(TestCase):
    def setUp(self):
        self.year = 2015
        self.month = 2
        self.day = 13

    def test_weekday(self):
        weekday = Timetools.get_weekday(self.year, self.month, self.day)
        self.assertEqual(weekday, 5)

    def test_diffdays(self):
        num_days = Timetools.get_diffdays(
            self.year, self.month, self.day,
            2016, 9, 3
        )

        self.assertEqual(num_days, 568)

    def test_calendar(self):
        cal = Timetools.get_calendar(self.year, self.month)

        cal_expected = [[0] * 7] \
                       + [range(i * 7 + 1, i * 7 + 8) for i in xrange(4)] \
                       + [[0] * 7]

        self.assertEqual(cal, cal_expected)

    def tearDown(self):
        pass
