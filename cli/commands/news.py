"""ymos fetch-news command — multi-source news fetching (Finnhub + Futu)."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import typer

from cli.utils.env_loader import load_dotenv

app = typer.Typer(help="Fetch company news from Finnhub and Futu")

_TICKER_RE = re.compile(r"^[A-Z0-9]{1,6}(\.(SS|SZ|HK))?$")


def _is_valid_ticker(ticker: str) -> bool:
    return bool(_TICKER_RE.match(ticker))


def _classify_market(ticker: str) -> str:
    """Classify ticker into market: 'hk_cn' or 'us_crypto'."""
    if ticker.endswith((".SS", ".SZ", ".HK")):
        return "hk_cn"
    return "us_crypto"


@app.command()
def fetch(
    hours: int = typer.Option(24, help="Hours to look back"),
    output: str = typer.Option("finnhub_news.json", help="Output file path"),
    api_key: str = typer.Option("", help="Finnhub API key"),
):
    """Fetch company news for holdings from Finnhub and Futu."""
    load_dotenv()
    from cli.core.paths import get_paths
    from cli.core.sources.news import (
        extract_tickers_from_state_machine,
        fetch_company_news,
        _enrich_article,
        deduplicate,
    )
    from cli.core.sources.futu_news import (
        fetch_futu_news,
        ticker_to_news_keyword,
        normalize_article,
    )

    key = api_key or os.environ.get("FINNHUB_API_KEY", "")

    paths = get_paths()
    holding_path = paths.holdings_state
    tickers = sorted(t for t in extract_tickers_from_state_machine(holding_path, us_only=False) if _is_valid_ticker(t))
    if not tickers:
        typer.echo("⚠️ No tickers in holdings state machine")
        raise typer.Exit(code=0)

    # Classify tickers by market
    hk_cn = [t for t in tickers if _classify_market(t) == "hk_cn"]
    us_crypto = [t for t in tickers if _classify_market(t) == "us_crypto"]

    typer.echo(f"📋 Holdings tickers: {', '.join(tickers)}")
    if hk_cn:
        typer.echo(f"   HK/CN: {', '.join(hk_cn)}")
    if us_crypto:
        typer.echo(f"   US/Crypto: {', '.join(us_crypto)}")

    now_utc = datetime.now(timezone.utc)
    cutoff_ts = (now_utc - timedelta(hours=hours)).timestamp()
    to_date = now_utc.strftime("%Y-%m-%d")
    from_date = (now_utc - timedelta(hours=hours)).strftime("%Y-%m-%d")

    typer.echo(f"📡 Fetching news (past {hours}h: {from_date} ~ {to_date})")

    all_articles: list[dict] = []
    sources_used: list[str] = []
    ticker_counts: dict[str, int] = {}

    # --- US/Crypto: try Finnhub first, Futu fallback per ticker ---
    futu_fallback_tickers: list[str] = []
    if us_crypto:
        if key:
            typer.echo("  [Finnhub] US/Crypto tickers:")
            for ticker in us_crypto:
                typer.echo(f"    → {ticker}...", nl=False)
                raw = fetch_company_news(ticker, key, from_date, to_date)
                enriched = [a for a in (_enrich_article(item, ticker, cutoff_ts) for item in raw) if a is not None]
                ticker_counts[ticker] = len(enriched)
                all_articles.extend(enriched)
                typer.echo(f" {len(enriched)} items")
                if not enriched:
                    futu_fallback_tickers.append(ticker)
            sources_used.append("finnhub")
        else:
            typer.echo("  ⚠️ No FINNHUB_API_KEY, skipping Finnhub for US/Crypto")
            futu_fallback_tickers = us_crypto

        # Futu fallback for US/Crypto tickers with no Finnhub results
        if futu_fallback_tickers:
            typer.echo("  [Futu] US/Crypto tickers (fallback):")
            for ticker in futu_fallback_tickers:
                typer.echo(f"    → {ticker}...", nl=False)
                kw = ticker_to_news_keyword(ticker)
                raw = fetch_futu_news(kw, size=10)
                articles = [normalize_article(item, ticker) for item in raw]
                ticker_counts[ticker] = ticker_counts.get(ticker, 0) + len(articles)
                all_articles.extend(articles)
                typer.echo(f" {len(articles)} items")
            if "futu_news_search" not in sources_used:
                sources_used.append("futu_news_search")

    # --- HK/CN: always use Futu directly ---
    if hk_cn:
        typer.echo("  [Futu] HK/CN tickers:")
        for ticker in hk_cn:
            typer.echo(f"    → {ticker}...", nl=False)
            kw = ticker_to_news_keyword(ticker)
            raw = fetch_futu_news(kw, size=10)
            articles = [normalize_article(item, ticker) for item in raw]
            ticker_counts[ticker] = len(articles)
            all_articles.extend(articles)
            typer.echo(f" {len(articles)} items")
        if "futu_news_search" not in sources_used:
            sources_used.append("futu_news_search")

    # Deduplicate across sources
    deduped = deduplicate(all_articles)
    p15_count = sum(1 for a in deduped if a.get("p15_trigger"))

    source_label = "+".join(sources_used) if sources_used else "none"

    result = {
        "meta": {
            "source": source_label,
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
    typer.echo(f"   {len(deduped)} articles (deduped) | p15_trigger={p15_count} | sources={source_label}")
