"""Futu news search source — covers HK/CN markets that Finnhub misses.

Zero third-party dependencies (uses urllib.request).
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

from cli.core.sources.news import P15_KEYWORDS

_FUTU_NEWS_URL = "https://ai-news-search.futunn.com/news_search"
_FUTU_USER_AGENT = "ymos-futu-news/0.0.1"


def ticker_to_news_keyword(ticker: str) -> str:
    """Convert YMOS ticker format to Futu news search keyword.

    >>> ticker_to_news_keyword("0700.HK")
    '00700'
    >>> ticker_to_news_keyword("AAPL")
    'AAPL'
    >>> ticker_to_news_keyword("688008.SS")
    '688008'
    >>> ticker_to_news_keyword("000001.SZ")
    '000001'
    """
    if "." in ticker:
        base, suffix = ticker.rsplit(".", 1)
        if suffix == "HK":
            return base.zfill(5)  # 0700 -> 00700
        return base  # .SS / .SZ -> bare code
    return ticker


def fetch_futu_news(
    keyword: str,
    size: int = 10,
    news_type: int = 1,
    lang: str = "zh-CN",
) -> list[dict]:
    """Fetch news articles from Futu news search API.

    Args:
        keyword: Search keyword (use ticker_to_news_keyword output).
        size: Number of articles to return.
        news_type: 1=News, 2=Notice, 3=Research.
        lang: Language preference.

    Returns:
        List of raw article dicts from Futu, or empty list on error.
    """
    params = {
        "keyword": keyword,
        "size": str(size),
        "news_type": str(news_type),
        "lang": lang,
        "sort_type": "2",  # sort by time
    }
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{_FUTU_NEWS_URL}?{qs}"

    req = urllib.request.Request(url, headers={"User-Agent": _FUTU_USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"  ❌ Futu news HTTP {e.code}: {e.reason}")
        return []
    except Exception as e:
        print(f"  ❌ Futu news request failed: {e}")
        return []

    if body.get("code") != 0:
        print(f"  ⚠️ Futu news API returned code={body.get('code')}, msg={body.get('message', '')}")
        return []

    data = body.get("data")
    if not data:
        return []

    return data if isinstance(data, list) else []


def _convert_publish_time(ts_raw) -> str:
    """Convert Futu publish_time to 'YYYY-MM-DD HH:MM' in UTC+8.

    Handles millisecond timestamps (>1e12) by dividing by 1000.
    Returns empty string on failure.
    """
    try:
        ts = float(ts_raw)
    except (TypeError, ValueError):
        return ""
    if ts > 1e12:
        ts = ts / 1000
    try:
        return datetime.fromtimestamp(
            ts, tz=timezone(timedelta(hours=8))
        ).strftime("%Y-%m-%d %H:%M")
    except (OSError, ValueError):
        return ""


def normalize_article(item: dict, ticker: str) -> dict:
    """Normalize a Futu news article to a standard dict.

    The output is compatible with the Finnhub article format so that
    deduplicate() and downstream consumers work uniformly.
    """
    title = item.get("title", "")
    desc = item.get("desc", "")
    published_at = _convert_publish_time(item.get("publish_time", 0))
    text_lc = (title + " " + desc).lower()

    # Build a unix timestamp for sorting compatibility with deduplicate()
    ts = 0
    try:
        raw = float(item.get("publish_time", 0))
        if raw > 1e12:
            raw = raw / 1000
        ts = int(raw)
    except (TypeError, ValueError):
        pass

    return {
        "ticker": ticker,
        "id": str(item.get("news_id", "")),
        "title": title,
        "summary": desc,
        "published_at": published_at,
        "url": item.get("url", ""),
        "source": "futu_news_search",
        "datetime_ts": ts,
        "datetime_readable": published_at + " UTC+8" if published_at else "",
        "headline": title,  # for deduplicate() compatibility
        "p15_trigger": any(kw in text_lc for kw in P15_KEYWORDS),
    }
