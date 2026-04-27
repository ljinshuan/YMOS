"""Yahoo Finance data source (migrated from fetch_price_yahoo.py).

Zero third-party dependencies. Uses Yahoo V8 Chart API via urllib.
"""

from __future__ import annotations

import json
import ssl
import time
import urllib.request
from datetime import datetime, timezone

_PERIOD_TO_RANGE = {
    "1d": "1d", "5d": "5d", "1mo": "1mo",
    "3mo": "3mo", "6mo": "6mo", "1y": "1y", "2y": "2y", "5y": "5y",
}


def _make_ssl_ctx() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


_SSL_CTX = _make_ssl_ctx()


def fetch_one(symbol: str, period: str = "1mo", interval: str = "1d", retries: int = 3) -> dict:
    """Fetch a single symbol from Yahoo Finance V8 Chart API."""
    yf_range = _PERIOD_TO_RANGE.get(period, "1mo")
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        f"?interval={interval}&range={yf_range}"
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json",
    }

    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15, context=_SSL_CTX) as resp:
                payload = json.loads(resp.read().decode())

            result = payload.get("chart", {}).get("result")
            if not result:
                err = payload.get("chart", {}).get("error", {})
                return {"symbol": symbol, "ok": False, "error": str(err) or "empty_result"}

            r = result[0]
            meta = r.get("meta", {})
            timestamps = r.get("timestamp", [])
            quotes = r.get("indicators", {}).get("quote", [{}])[0]

            closes = quotes.get("close", [])
            if not closes or all(c is None for c in closes):
                return {"symbol": symbol, "ok": False, "error": "empty_history"}

            current_price = meta.get("regularMarketPrice") or next(
                (c for c in reversed(closes) if c is not None), 0
            )

            opens = quotes.get("open", [])
            highs = quotes.get("high", [])
            lows = quotes.get("low", [])
            volumes = quotes.get("volume", [])

            def _safe(arr, i, default=0.0):
                try:
                    v = arr[i]
                    return float(v) if v is not None else default
                except (IndexError, TypeError):
                    return default

            n = len(timestamps)
            start_i = max(0, n - 10)
            rows = []
            for i in range(start_i, n):
                dt = datetime.fromtimestamp(timestamps[i], tz=timezone.utc).isoformat()
                rows.append({
                    "t": dt, "open": _safe(opens, i), "high": _safe(highs, i),
                    "low": _safe(lows, i), "close": _safe(closes, i), "volume": _safe(volumes, i),
                })

            last_i = n - 1
            return {
                "symbol": symbol, "ok": True,
                "last_close": float(current_price),
                "last_open": _safe(opens, last_i),
                "last_high": _safe(highs, last_i),
                "last_low": _safe(lows, last_i),
                "last_volume": _safe(volumes, last_i),
                "bars": rows,
            }

        except Exception as e:
            last_err = str(e)
            if attempt < retries - 1:
                time.sleep(1.2 * (attempt + 1))

    return {"symbol": symbol, "ok": False, "error": last_err or "unknown_error"}
