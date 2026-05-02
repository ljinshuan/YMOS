"""Tests for cli.monitor.trading_hours — market classification and trading hours."""

import datetime as dt
from zoneinfo import ZoneInfo

from cli.monitor.trading_hours import Market, classify_market, is_trading_hours


class TestClassifyMarket:
    def test_us_stock_no_suffix(self):
        assert classify_market("AAPL") == Market.US

    def test_us_stock_bare(self):
        assert classify_market("SOXL") == Market.US

    def test_hk_stock(self):
        assert classify_market("0700.HK") == Market.HK

    def test_shanghai_stock(self):
        assert classify_market("688008.SS") == Market.A

    def test_shenzhen_stock(self):
        assert classify_market("000001.SZ") == Market.A


class TestIsTradingHours:
    def _make_time(self, market: Market, hour: int, minute: int, weekday: int = 0) -> dt.datetime:
        """Create a datetime at specific local time for a market, on a Monday (weekday=0)."""
        tz = {
            Market.US: ZoneInfo("America/New_York"),
            Market.HK: ZoneInfo("Asia/Hong_Kong"),
            Market.A: ZoneInfo("Asia/Shanghai"),
        }[market]
        # 2026-01-05 is a Monday
        base = dt.datetime(2026, 1, 5, hour, minute, tzinfo=tz)
        # Adjust to desired weekday
        days_ahead = weekday - base.weekday()
        return base + dt.timedelta(days=days_ahead)

    def test_us_trading_hours(self):
        # US market: 9:30 AM ET Monday
        now = self._make_time(Market.US, 10, 0)
        assert is_trading_hours("AAPL", now) is True

    def test_us_before_open(self):
        # US market: 8:00 AM ET Monday
        now = self._make_time(Market.US, 8, 0)
        assert is_trading_hours("AAPL", now) is False

    def test_us_after_close(self):
        # US market: 5:00 PM ET Monday
        now = self._make_time(Market.US, 17, 0)
        assert is_trading_hours("AAPL", now) is False

    def test_us_weekend(self):
        # Saturday
        now = self._make_time(Market.US, 10, 0, weekday=5)
        assert is_trading_hours("AAPL", now) is False

    def test_hk_trading_hours_morning(self):
        # HK market: 10:00 AM HKT Monday
        now = self._make_time(Market.HK, 10, 0)
        assert is_trading_hours("0700.HK", now) is True

    def test_hk_lunch_break(self):
        # HK market: 12:30 PM HKT Monday (lunch break)
        now = self._make_time(Market.HK, 12, 30)
        assert is_trading_hours("0700.HK", now) is False

    def test_hk_afternoon_session(self):
        # HK market: 14:00 PM HKT Monday
        now = self._make_time(Market.HK, 14, 0)
        assert is_trading_hours("0700.HK", now) is True

    def test_hk_after_close(self):
        # HK market: 17:00 PM HKT Monday
        now = self._make_time(Market.HK, 17, 0)
        assert is_trading_hours("0700.HK", now) is False

    def test_a_trading_hours_morning(self):
        # A-share: 10:00 AM CST Monday
        now = self._make_time(Market.A, 10, 0)
        assert is_trading_hours("688008.SS", now) is True

    def test_a_lunch_break(self):
        # A-share: 12:00 PM CST Monday (lunch break)
        now = self._make_time(Market.A, 12, 0)
        assert is_trading_hours("688008.SS", now) is False

    def test_a_afternoon_session(self):
        # A-share: 14:00 PM CST Monday
        now = self._make_time(Market.A, 14, 0)
        assert is_trading_hours("688008.SS", now) is True

    def test_a_after_close(self):
        # A-share: 16:00 PM CST Monday
        now = self._make_time(Market.A, 16, 0)
        assert is_trading_hours("688008.SS", now) is False

    def test_a_weekend(self):
        # Sunday
        now = self._make_time(Market.A, 10, 0, weekday=6)
        assert is_trading_hours("688008.SS", now) is False
