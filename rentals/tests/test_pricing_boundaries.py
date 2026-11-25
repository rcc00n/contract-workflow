from datetime import date, time
from types import SimpleNamespace

from django.test import SimpleTestCase
from rentals.services.pricing import rental_days, season_for_date


class PricingBoundaryTests(SimpleTestCase):
    def test_return_time_extends_day_count_only_when_later(self):
        start, end = date(2026, 1, 1), date(2026, 1, 3)
        self.assertEqual(rental_days(start, end, time(10), time(10)), 2)
        self.assertEqual(rental_days(start, end, time(10), time(11)), 3)
        self.assertEqual(rental_days(start, end, time(10), time(9)), 2)

    def test_missing_or_reversed_period_never_creates_negative_days(self):
        self.assertEqual(rental_days(None, date(2026, 1, 3)), 0)
        self.assertEqual(rental_days(date(2026, 1, 3), date(2026, 1, 1)), 0)
        self.assertEqual(rental_days(date(2026, 1, 1), date(2026, 1, 1)), 0)

    def test_cross_year_high_season_is_inclusive(self):
        config = SimpleNamespace(high_season_start=date(2000, 11, 1),
                                 high_season_end=date(2001, 3, 1))
        for day, expected in ((date(2026, 11, 1), 'high'), (date(2027, 1, 1), 'high'),
                              (date(2027, 3, 1), 'high'), (date(2027, 3, 2), 'low')):
            with self.subTest(day=day):
                self.assertEqual(season_for_date(day, config), expected)
