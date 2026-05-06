"""Trading hours detection for US, HK, and A-share markets."""

from __future__ import annotations

import datetime as dt
from enum import StrEnum
from zoneinfo import ZoneInfo


class Market(StrEnum):
    US = "US"
    HK = "HK"
    A = "A"


_MARKET_HOURS = {
    Market.US: [
        # (start_hour, start_min, end_hour, end_min) in local time
        # US regular: 9:30 AM - 4:00 PM ET
        (9, 30, 16, 0),
    ],
    Market.HK: [
        # HK: 9:30 AM - 12:00 PM, 1:00 PM - 4:00 PM HKT
        (9, 30, 12, 0),
        (13, 0, 16, 0),
    ],
    Market.A: [
        # A-share: 9:30-11:30 AM, 1:00-3:00 PM CST
        (9, 30, 11, 30),
        (13, 0, 15, 0),
    ],
}

_MARKET_TZ = {
    Market.US: ZoneInfo("America/New_York"),
    Market.HK: ZoneInfo("Asia/Hong_Kong"),
    Market.A: ZoneInfo("Asia/Shanghai"),
}


def classify_market(ticker: str) -> Market:
    """Classify ticker to its market."""
    if "." not in ticker:
        return Market.US
    suffix = ticker.rsplit(".", 1)[1].upper()
    if suffix == "HK":
        return Market.HK
    if suffix in ("SS", "SZ"):
        return Market.A
    return Market.US


def is_trading_hours(
    ticker: str,
    now: dt.datetime | None = None,
) -> bool:
    """Check if the ticker's market is currently in trading hours.

    Args:
        ticker: YMOS ticker format (e.g. AAPL, 0700.HK, 688008.SS)
        now: Override current time (for testing). Defaults to utcnow.
    """
    market = classify_market(ticker)
    tz = _MARKET_TZ[market]

    if now is None:
        now = dt.datetime.now(dt.timezone.utc)
    local = now.astimezone(tz)

    # Weekend check (Saturday=5, Sunday=6)
    if local.weekday() >= 5:
        return False

    for start_h, start_m, end_h, end_m in _MARKET_HOURS[market]:
        session_start = local.replace(hour=start_h, minute=start_m, second=0, microsecond=0)
        session_end = local.replace(hour=end_h, minute=end_m, second=0, microsecond=0)
        if session_start <= local <= session_end:
            return True

    return False
