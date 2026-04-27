"""Finnhub company news source (migrated from fetch_finnhub_news.py).

Zero third-party dependencies.
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

P15_KEYWORDS = {
    "earnings", "revenue", "guidance", "acquisition", "merger",
    "bankruptcy", "layoff", "recall", "investigation", "settlement",
    "partnership", "contract", "upgrade", "downgrade", "beat", "miss",
}


def extract_tickers_from_state_machine(filepath: Path, us_only: bool = True) -> set[str]:
    """Extract ticker column from a Markdown state-machine table."""
    if not filepath.exists():
        return set()
    text = filepath.read_text(encoding="utf-8")
    tickers: set[str] = set()
    in_table = False
    ticker_col_idx = -1

    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            in_table = False
            continue
        cols = [c.strip() for c in line.split("|") if c.strip()]
        if not in_table:
            for i, col in enumerate(cols):
                if col.lower() in ("ticker", "代码", "标的"):
                    ticker_col_idx = i
                    in_table = True
                    break
            continue
        if all(c.replace("-", "").replace(":", "") == "" for c in cols):
            continue
        if 0 <= ticker_col_idx < len(cols):
            val = cols[ticker_col_idx].strip().upper()
            if val and not val.startswith(":") and val != "---":
                if us_only:
                    if not any(val.endswith(s) for s in (".SS", ".SZ", ".HK")):
                        tickers.add(val)
                else:
                    tickers.add(val)
    return tickers


def fetch_company_news(ticker: str, api_key: str, from_date: str, to_date: str) -> list[dict]:
    """Fetch company news for a single ticker via Finnhub /company-news."""
    url = (
        f"https://finnhub.io/api/v1/company-news"
        f"?symbol={ticker}&from={from_date}&to={to_date}&token={api_key}"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "YMOS/2.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"  ❌ {ticker} HTTP {e.code}: {e.reason}")
        return []
    except Exception as e:
        print(f"  ❌ {ticker} request failed: {e}")
        return []


def _enrich_article(item: dict, ticker: str, cutoff_ts: float) -> dict | None:
    ts = item.get("datetime", 0)
    if ts < cutoff_ts:
        return None
    headline = item.get("headline", "")
    summary = item.get("summary", "")
    text_lc = (headline + " " + summary).lower()
    return {
        "ticker": ticker,
        "datetime_ts": ts,
        "datetime_readable": datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "source": item.get("source", ""),
        "headline": headline,
        "summary": summary,
        "url": item.get("url", ""),
        "image": item.get("image", ""),
        "p15_trigger": any(kw in text_lc for kw in P15_KEYWORDS),
    }


def deduplicate(articles: list[dict]) -> list[dict]:
    """Deduplicate by first 40 chars of headline."""
    seen: dict[str, dict] = {}
    for art in sorted(articles, key=lambda x: x["datetime_ts"]):
        key = re.sub(r"\s+", " ", art["headline"][:40].lower()).strip()
        if key not in seen:
            seen[key] = art
    return sorted(seen.values(), key=lambda x: x["datetime_ts"], reverse=True)
