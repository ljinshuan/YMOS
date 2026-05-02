"""Futu OpenD historical OHLCV data source for technical analysis."""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import pandas as pd

from cli.core.futu_utils import ticker_to_futu_symbol


def fetch_futu_history(
    ticker: str,
    host: str = "127.0.0.1",
    port: int = 11111,
) -> pd.DataFrame | None:
    """Fetch ~1 year of daily OHLCV data from Futu OpenD via request_history_kline.

    Returns DataFrame with columns: open, high, low, close, volume (float64).
    DatetimeIndex sorted ascending. Returns None on any failure.
    """
    try:
        import futu as ft
    except ImportError:
        return None

    symbol = ticker_to_futu_symbol(ticker)
    host = host or os.getenv("FUTU_OPEND_HOST", "127.0.0.1")
    port = port or int(os.getenv("FUTU_OPEND_PORT", "11111"))

    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=400)

    try:
        quote_ctx = ft.OpenQuoteContext(host=host, port=port)
        try:
            ret, data, page_req_key = quote_ctx.request_history_kline(
                symbol,
                start=start_date.strftime("%Y-%m-%d"),
                end=end_date.strftime("%Y-%m-%d"),
                ktype=ft.KLType.K_DAY,
                autype=ft.AuType.QFQ,
                max_count=1000,
            )
        finally:
            quote_ctx.close()
    except Exception as e:
        print(f"⚠️  Futu OpenD connection failed for {ticker}: {e}")
        return None

    if ret != ft.RET_OK:
        print(f"⚠️  Futu get_history_kline error for {ticker}: {data}")
        return None

    if data is None or data.empty:
        return None

    # Normalize: select and rename columns to standard format
    col_map = {
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "volume": "volume",
    }

    # The Futu API returns columns including: code, time_key, open, close, high, low,
    # pe_ratio, turnover, volume, turnover_rate, change_rate, last_close
    available = {c: col_map[c] for c in col_map if c in data.columns}
    df = data[list(available.keys())].rename(columns=available).copy()

    # Convert time_key to DatetimeIndex
    if "time_key" in data.columns:
        df.index = pd.to_datetime(data["time_key"])
    else:
        df.index = pd.to_datetime(data.index)

    df = df.sort_index()
    df = df.dropna()

    if df.empty:
        return None

    return df.astype(float)
