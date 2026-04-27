"""Finnhub data source — US stocks and Crypto (migrated from fetch_price_api.py).

Zero third-party dependencies. Uses urllib + json stdlib only.
"""

from __future__ import annotations

import json
import os
import ssl
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

FINNHUB_BASE = "https://finnhub.io/api/v1"
NEWS_CATEGORIES = ["general", "merger"]


def _finnhub_get(endpoint: str, params: dict | None, api_key: str):
    """Finnhub GET request with token auth via URL parameter."""
    query = {"token": api_key}
    if params:
        query.update(params)

    url = FINNHUB_BASE + endpoint + "?" + urllib.parse.urlencode(query)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "YMOS-Personal/1.0", "Accept": "application/json"},
        method="GET",
    )
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"   ❌ HTTP {e.code} — {endpoint}")
        if e.code == 429:
            print("     → Rate limit exceeded (60/min), retry later")
        return None
    except Exception as e:
        print(f"   ❌ Request failed: {e}")
        return None


def fetch_quotes(symbols: list[str], api_key: str) -> list[dict]:
    """Real-time quotes via GET /quote."""
    print(f"\n📊 Finnhub quotes: {', '.join(symbols)}")
    quotes = []
    for symbol in symbols:
        data = _finnhub_get("/quote", {"symbol": symbol}, api_key)
        if not data or data.get("c", 0) == 0:
            print(f"   ⚠️  {symbol}: no quote (non-trading hours)")
            continue
        pct = data.get("dp", 0) or 0
        sign = "+" if pct >= 0 else ""
        arrow = "📈" if pct >= 0 else "📉"
        print(f"   {arrow} {symbol:<6} ${data['c']:.2f}  {sign}{pct:.2f}%"
              f"  |  H ${data['h']:.2f}  L ${data['l']:.2f}  Prev ${data['pc']:.2f}")
        quotes.append({
            "type": "quote", "symbol": symbol,
            "price": data.get("c"), "change": data.get("d"),
            "change_pct": data.get("dp"), "high": data.get("h"),
            "low": data.get("l"), "open": data.get("o"),
            "prev_close": data.get("pc"), "timestamp": data.get("t"),
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        })
    return quotes


def fetch_company_news(symbol: str, api_key: str, days: int = 1) -> list[dict]:
    """Company news via GET /company-news."""
    date_to = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    date_from = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    data = _finnhub_get("/company-news", {"symbol": symbol, "from": date_from, "to": date_to}, api_key)
    if not data or not isinstance(data, list):
        return []
    return [
        {
            "type": "company_news", "symbol": symbol,
            "category": item.get("category", ""),
            "headline": item.get("headline", ""),
            "summary": item.get("summary", ""),
            "source": item.get("source", ""),
            "url": item.get("url", ""),
            "datetime": datetime.fromtimestamp(item.get("datetime", 0), tz=timezone.utc).isoformat(),
        }
        for item in data
    ]


def fetch_market_news(api_key: str, days: int = 1) -> list[dict]:
    """Market news via GET /news."""
    print(f"\n📰 Market news (last {days} days)...")
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).timestamp()
    all_items: list[dict] = []
    for category in NEWS_CATEGORIES:
        data = _finnhub_get("/news", {"category": category}, api_key)
        if not data or not isinstance(data, list):
            continue
        filtered = [
            {
                "type": "market_news", "category": category,
                "headline": item.get("headline", ""),
                "summary": item.get("summary", ""),
                "source": item.get("source", ""),
                "url": item.get("url", ""),
                "datetime": datetime.fromtimestamp(item.get("datetime", 0), tz=timezone.utc).isoformat(),
                "related": item.get("related", ""),
            }
            for item in data
            if item.get("datetime", 0) >= cutoff
        ]
        all_items.extend(filtered)
        print(f"   [{category}] → {len(filtered)} items")
    return all_items


def fetch_earnings_calendar(symbols: list[str], api_key: str, days: int = 7) -> list[dict]:
    """Earnings calendar via GET /calendar/earnings."""
    print(f"\n📅 Earnings calendar (next {days} days, watchlist only)...")
    date_from = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    date_to = (datetime.now(timezone.utc) + timedelta(days=days)).strftime("%Y-%m-%d")
    data = _finnhub_get("/calendar/earnings", {"from": date_from, "to": date_to}, api_key)
    if not data or "earningsCalendar" not in data:
        print("   — no data")
        return []
    hits = [
        {
            "type": "earnings", "symbol": e.get("symbol"),
            "date": e.get("date"), "eps_estimate": e.get("epsEstimate"),
            "revenue_estimate": e.get("revenueEstimate"),
            "quarter": e.get("quarter"), "year": e.get("year"),
        }
        for e in data["earningsCalendar"]
        if e.get("symbol") in symbols
    ]
    if hits:
        print(f"   ⚠️  Upcoming earnings: {[e['symbol'] for e in hits]}")
    else:
        print(f"   — No earnings in next {days} days for tracked symbols")
    return hits
