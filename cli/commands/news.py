"""ymos fetch-news command — Finnhub company news fetching."""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import typer

from cli.utils.env_loader import load_dotenv

app = typer.Typer(help="Fetch company news from Finnhub")


@app.command()
def fetch(
    hours: int = typer.Option(24, help="Hours to look back"),
    output: str = typer.Option("finnhub_news.json", help="Output file path"),
    api_key: str = typer.Option("", help="Finnhub API key"),
):
    """Fetch company news for holdings from Finnhub."""
    load_dotenv()
    from cli.core.paths import get_paths
    from cli.core.sources.news import (
        extract_tickers_from_state_machine,
        fetch_company_news,
        _enrich_article,
        deduplicate,
    )

    key = api_key or os.environ.get("FINNHUB_API_KEY", "")
    if not key:
        typer.echo("⚠️ No Finnhub API Key, skipping news fetch")
        raise typer.Exit(code=0)

    paths = get_paths()
    holding_path = paths.holdings_state
    tickers = sorted(extract_tickers_from_state_machine(holding_path, us_only=True))
    if not tickers:
        typer.echo("⚠️ No US/Crypto tickers in holdings state machine")
        raise typer.Exit(code=0)

    typer.echo(f"📋 Holdings US/Crypto tickers: {', '.join(tickers)}")

    now_utc = datetime.now(timezone.utc)
    cutoff_ts = (now_utc - timedelta(hours=hours)).timestamp()
    to_date = now_utc.strftime("%Y-%m-%d")
    from_date = (now_utc - timedelta(hours=hours)).strftime("%Y-%m-%d")

    typer.echo(f"📡 Fetching news (past {hours}h: {from_date} ~ {to_date})")

    all_articles: list[dict] = []
    ticker_counts: dict[str, int] = {}
    for ticker in tickers:
        typer.echo(f"  → {ticker}...", nl=False)
        raw = fetch_company_news(ticker, key, from_date, to_date)
        enriched = [a for a in (_enrich_article(item, ticker, cutoff_ts) for item in raw) if a is not None]
        ticker_counts[ticker] = len(enriched)
        all_articles.extend(enriched)
        typer.echo(f" {len(enriched)} items")

    deduped = deduplicate(all_articles)
    p15_count = sum(1 for a in deduped if a.get("p15_trigger"))

    result = {
        "meta": {
            "source": "Finnhub company-news",
            "hours_back": hours,
            "date_range": f"{from_date} ~ {to_date}",
            "generated_at": now_utc.strftime("%Y-%m-%d %H:%M UTC"),
            "holding_tickers": tickers,
            "counts": {
                "total_raw": sum(ticker_counts.values()),
                "after_dedup": len(deduped),
                "p15_trigger": p15_count,
                "by_ticker": ticker_counts,
            },
        },
        "articles": deduped,
    }

    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    typer.echo(f"\n💾 Saved: {out_path}")
    typer.echo(f"   {len(deduped)} articles (deduped) | p15_trigger={p15_count}")
