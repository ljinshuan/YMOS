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
    """Convert YMOS ticker format to Futu search keyword."""
    if "." in ticker:
        base, suffix = ticker.rsplit(".", 1)
        if suffix == "HK":
            return base.zfill(5)
        return base
    return ticker


def _fetch_feed(ticker: str, size: int = 30) -> dict:
    """Fetch community feed posts for a single ticker via Futu search API."""
    import requests

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
                "status": "ok",
                "source": "futu_stock_feed",
                "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                "post_count": len(posts),
                "data": posts,
            }
        return {
            "ticker": ticker,
            "status": "empty",
            "source": "futu_stock_feed",
            "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "post_count": 0,
            "data": [],
            "raw_code": body.get("code"),
            "raw_message": body.get("message", ""),
        }
    except Exception as e:
        return {
            "ticker": ticker,
            "status": "error",
            "source": "none",
            "error": f"Network error: {e}",
            "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "post_count": 0,
            "data": [],
        }


def _compute_group_aggregation(symbols: list[dict]) -> dict | None:
    """Compute group-level sentiment aggregation across multiple symbols.

    Returns None if only one symbol (single mode).
    """
    if len(symbols) < 2:
        return None

    total_posts = sum(s.get("post_count", 0) for s in symbols)
    if total_posts == 0:
        return {
            "label": "neutral",
            "bull_pct": "0%",
            "bear_pct": "0%",
            "neutral_pct": "0%",
            "post_count": 0,
            "summary": "所有标的均无社区数据",
        }

    # Sum percentages weighted by post count
    weighted_bull = sum(
        float(s.get("bull_pct", "0%").rstrip("%")) * s.get("post_count", 0)
        for s in symbols
    )
    weighted_bear = sum(
        float(s.get("bear_pct", "0%").rstrip("%")) * s.get("post_count", 0)
        for s in symbols
    )
    weighted_neutral = sum(
        float(s.get("neutral_pct", "0%").rstrip("%")) * s.get("post_count", 0)
        for s in symbols
    )

    bull_pct = round(weighted_bull / total_posts, 1) if total_posts else 0
    bear_pct = round(weighted_bear / total_posts, 1) if total_posts else 0
    neutral_pct = round(weighted_neutral / total_posts, 1) if total_posts else 0

    # Determine group label
    label = _determine_label(bull_pct, bear_pct, neutral_pct)

    # Find driving symbols
    driving = []
    for s in symbols:
        s_bull = float(s.get("bull_pct", "0%").rstrip("%"))
        s_bear = float(s.get("bear_pct", "0%").rstrip("%"))
        if abs(s_bull - bull_pct) > 15 or abs(s_bear - bear_pct) > 15:
            driving.append(s.get("ticker", ""))

    return {
        "label": label,
        "bull_pct": f"{bull_pct:.1f}%",
        "bear_pct": f"{bear_pct:.1f}%",
        "neutral_pct": f"{neutral_pct:.1f}%",
        "post_count": total_posts,
        "summary": f"Overall sentiment is {label}.",
        "driving_symbols": driving or None,
    }


def _determine_label(bull_pct: float, bear_pct: float, neutral_pct: float) -> str:
    """Determine aggregate sentiment label with mixed rule.

    Priority: clear dominance > mixed > neutral.
    """
    # Clear dominance: one side is significantly larger
    diff = abs(bull_pct - bear_pct)
    if bull_pct > bear_pct and diff >= 15:
        return "bullish"
    if bear_pct > bull_pct and diff >= 15:
        return "bearish"
    # Mixed: both sides meaningful and close
    if bull_pct >= 25 and bear_pct >= 25 and diff < 15:
        return "mixed"
    # Dominant but not large enough gap
    if bull_pct > bear_pct and bull_pct > neutral_pct:
        return "bullish"
    if bear_pct > bull_pct and bear_pct > neutral_pct:
        return "bearish"
    return "neutral"


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
        # Support comma-separated tickers for multi-symbol mode
        for t in ticker.split(","):
            t = t.strip().upper()
            if t and t not in tickers:
                tickers.append(t)
    if from_state:
        for t in _read_tickers_from_state():
            if t not in tickers:
                tickers.append(t)
    if not tickers:
        typer.echo("No tickers provided. Use --ticker TICKER or --from-state")
        raise typer.Exit(code=1)

    size = max(1, min(50, size))
    mode = "multi" if len(tickers) > 1 else "single"
    typer.echo(f"📊 Fetching sentiment for {len(tickers)} ticker(s): {', '.join(tickers)}")

    symbols = []
    for t in tickers:
        typer.echo(f"  → {t}...", nl=False)
        result = _fetch_feed(t, size=size)
        # Placeholder sentiment percentages — actual classification done by P19 prompt
        # CLI outputs raw posts; LLM does the classification
        result["bull_pct"] = "0%"
        result["bear_pct"] = "0%"
        result["neutral_pct"] = "0%"
        result["label"] = "pending"
        symbols.append(result)
        count = result.get("post_count", 0)
        if result.get("error"):
            typer.echo(f" ❌ {result['error']}")
        elif count == 0:
            typer.echo(" ⚠️ no posts found")
        else:
            typer.echo(f" ✅ ({count} posts)")

    now = dt.datetime.now()
    group = _compute_group_aggregation(symbols)

    output = {
        "request": {
            "symbol_list": tickers,
            "size_per_symbol": size,
        },
        "generated_at": now.isoformat(),
        "mode": mode,
        "group": group,
        "symbols": symbols,
        "disclaimer": "This content is based on public information and does not constitute investment advice.",
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
