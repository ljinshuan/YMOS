"""Unified historical OHLCV data fetching for technical analysis."""

from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timedelta, timezone

import pandas as pd

from cli.core.crypto import normalize_for_source
from cli.core.router import classify
from cli.core.sources import tushare
from cli.core.sources.yahoo import _SSL_CTX


def fetch_history(symbols: list[str], tushare_token: str = "") -> dict[str, pd.DataFrame]:
    """Fetch historical OHLCV data for multiple symbols.

    Returns {symbol: DataFrame} with columns: open, high, low, close, volume (float64).
    DatetimeIndex is timezone-naive dates, sorted ascending. ~1 year of daily data.
    Skips failed symbols with warnings.
    """
    results = {}
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=400)

    for symbol in symbols:
        try:
            source = classify(symbol)
            if source == "tushare":
                df = _fetch_tushare_history(symbol, start_date, end_date, tushare_token)
            else:
                norm_symbol = normalize_for_source(symbol, "yahoo")
                df = _fetch_yahoo_history(norm_symbol)
            if df is not None and not df.empty:
                results[symbol] = df
        except Exception as e:
            print(f"⚠️  Failed to fetch history for {symbol}: {e}")

    return results


def _fetch_tushare_history(symbol: str, start_date: datetime,
                           end_date: datetime, token: str) -> pd.DataFrame | None:
    """Fetch full daily history from Tushare for A-shares."""
    ts_code = tushare.to_tushare_code(symbol)
    if not ts_code:
        return None

    payload = json.dumps({
        "api_name": "daily",
        "token": token,
        "params": {
            "ts_code": ts_code,
            "start_date": start_date.strftime("%Y%m%d"),
            "end_date": end_date.strftime("%Y%m%d"),
        },
        "fields": "ts_code,trade_date,open,high,low,close,vol",
    }).encode("utf-8")

    try:
        req = urllib.request.Request(
            "http://api.tushare.pro",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"⚠️  Tushare API error for {symbol}: {e}")
        return None

    if result.get("code") != 0:
        print(f"⚠️  Tushare API error for {symbol}: {result.get('msg')}")
        return None

    raw_items = result.get("data", {}).get("items", [])
    raw_fields = result.get("data", {}).get("fields", [])

    if not raw_items or not raw_fields:
        return None

    rows = [dict(zip(raw_fields, row)) for row in raw_items]
    df = pd.DataFrame(rows)

    df["trade_date"] = pd.to_datetime(df["trade_date"], format="%Y%m%d")
    df = df.sort_values("trade_date").reset_index(drop=True)
    df.index = df["trade_date"]
    df = df.drop(columns=["ts_code", "trade_date"])
    df = df.rename(columns={"vol": "volume"})

    return df.astype(float)


def _fetch_yahoo_history(symbol: str) -> pd.DataFrame | None:
    """Fetch full 1-year daily history from Yahoo Finance V8 Chart API."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1y"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json",
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15, context=_SSL_CTX) as resp:
            payload = json.loads(resp.read().decode())
    except Exception as e:
        print(f"⚠️  Yahoo API error for {symbol}: {e}")
        return None

    result = payload.get("chart", {}).get("result")
    if not result:
        err = payload.get("chart", {}).get("error", {})
        print(f"⚠️  Yahoo error for {symbol}: {err}")
        return None

    r = result[0]
    timestamps = r.get("timestamp", [])
    quotes = r.get("indicators", {}).get("quote", [{}])[0]

    if not timestamps:
        return None

    data = {
        "open": quotes.get("open", []),
        "high": quotes.get("high", []),
        "low": quotes.get("low", []),
        "close": quotes.get("close", []),
        "volume": quotes.get("volume", []),
    }

    df = pd.DataFrame(data)
    dates = pd.to_datetime(timestamps, unit="s", utc=True).tz_localize(None)
    df.index = dates.date
    df.index = pd.DatetimeIndex(df.index)
    df = df.sort_index()
    df = df.dropna()

    return df.astype(float)
