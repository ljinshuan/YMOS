"""ymos fetch-sentiment command — stock comment sentiment via Futu."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import typer

from cli.utils.env_loader import load_dotenv

app = typer.Typer(help="Fetch stock comment sentiment data")

FUTU_FEED_URL = "https://ai-news-search.futunn.com/stock_feed"
FUTU_USER_AGENT = "futunn-comment-sentiment/0.0.2 (Skill)"


def _ticker_to_keyword(ticker: str) -> str:
    """Convert YMOS ticker format to Futu search keyword.

    YMOS: 0700.HK, AAPL, 688008.SS
    Futu prefers: 00700, AAPL, company names, short tickers
    """
    if "." in ticker:
        base, suffix = ticker.rsplit(".", 1)
        if suffix == "HK":
            return base.zfill(5)  # 0700 → 00700
        return base  # AAPL (no suffix issues for US)
    return ticker


def _fetch_feed(ticker: str, size: int = 30) -> dict:
    """Fetch community feed posts for a single ticker via Futu search API."""
    import requests
    from urllib.parse import quote

    keyword = _ticker_to_keyword(ticker)
    try:
        resp = requests.get(
            FUTU_FEED_URL,
            params={"keyword": keyword, "size": str(size)},
            headers={"User-Agent": FUTU_USER_AGENT},
            timeout=15,
        )
        body = resp.json()
        if body.get("code") == 0 and body.get("data"):
            posts = []
            for item in body["data"]:
                ts_raw = item.get("publish_time", 0)
                ts = 0
                try:
                    ts = float(ts_raw)
                    if ts > 1e12:
                        ts = ts / 1000
                except (TypeError, ValueError):
                    ts = 0
                published_at = ""
                if ts:
                    try:
                        published_at = dt.datetime.fromtimestamp(
                            ts, tz=dt.timezone(dt.timedelta(hours=8))
                        ).strftime("%Y-%m-%d %H:%M")
                    except (OSError, ValueError):
                        pass
                title = item.get("title", "")
                desc = item.get("desc", "")
                posts.append({
                    "id": item.get("id", ""),
                    "title": title,
                    "desc": desc,
                    "text": f"{title} {desc}".strip(),
                    "published_at": published_at,
                    "url": item.get("url", ""),
                })
            return {
                "ticker": ticker,
                "source": "futu_stock_feed",
                "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                "post_count": len(posts),
                "data": posts,
            }
        return {
            "ticker": ticker,
            "source": "futu_stock_feed",
            "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "post_count": 0,
            "data": [],
            "raw_code": body.get("code"),
            "raw_message": body.get("message", ""),
        }
    except requests.RequestException as e:
        return {
            "ticker": ticker,
            "source": "none",
            "error": f"Network error: {e}",
            "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "post_count": 0,
            "data": [],
        }


def _read_tickers_from_state() -> list[str]:
    """Read tickers from holdings + watchlist state machines."""
    from cli.core.paths import get_paths
    from cli.core.sources.news import extract_tickers_from_state_machine

    paths = get_paths()
    tickers: list[str] = []
    for state_file in [paths.holdings_state, paths.watchlist_state]:
        for t in extract_tickers_from_state_machine(state_file, us_only=False):
            if t not in tickers:
                tickers.append(t)
    return tickers


@app.command()
def fetch(
    ticker: str = typer.Option("", help="Single ticker to fetch sentiment for"),
    from_state: bool = typer.Option(False, help="Read tickers from state machines"),
    output_dir: str = typer.Option("", help="Output directory for JSON results"),
    size: int = typer.Option(30, help="Number of posts to fetch per ticker (1-50)"),
):
    """Fetch stock comment sentiment data from Futu community feed."""
    load_dotenv()

    tickers: list[str] = []
    if ticker:
        tickers.append(ticker.strip().upper())
    if from_state:
        for t in _read_tickers_from_state():
            if t not in tickers:
                tickers.append(t)
    if not tickers:
        typer.echo("No tickers provided. Use --ticker TICKER or --from-state")
        raise typer.Exit(code=1)

    size = max(1, min(50, size))
    typer.echo(f"📊 Fetching sentiment for {len(tickers)} ticker(s): {', '.join(tickers)}")

    results = []
    for t in tickers:
        typer.echo(f"  → {t}...", nl=False)
        result = _fetch_feed(t, size=size)
        results.append(result)
        count = result.get("post_count", 0)
        if result.get("error"):
            typer.echo(f" ❌ {result['error']}")
        elif count == 0:
            typer.echo(" ⚠️ no posts found")
        else:
            typer.echo(f" ✅ ({count} posts)")

    now = dt.datetime.now()
    output = {
        "fetched_at": now.isoformat(),
        "count": len(results),
        "total_posts": sum(r.get("post_count", 0) for r in results),
        "results": results,
    }

    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        file_path = out_path / f"sentiment_{now.strftime('%Y%m%d')}.json"
    else:
        from cli.core.paths import get_paths
        paths = get_paths()
        default_dir = paths.reports / "sentiment" / "raw" / now.strftime("%Y-%m")
        default_dir.mkdir(parents=True, exist_ok=True)
        file_path = default_dir / f"sentiment_{now.strftime('%Y%m%d')}.json"

    file_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    typer.echo(f"\n💾 Saved: {file_path}")
