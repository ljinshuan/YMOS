"""ymos fetch-market command — Market Data API fetching."""

from __future__ import annotations

import json
import os
from pathlib import Path

import typer

from cli.utils.env_loader import load_dotenv

app = typer.Typer(help="Fetch market data from API")


@app.command()
def fetch(
    days: float = typer.Option(1.0, help="Days to look back"),
    output: str = typer.Option("market_data.json", help="Output file path"),
    api_url: str = typer.Option("", help="Market data API URL"),
    api_key: str = typer.Option("", help="Market data API key"),
    categories: str = typer.Option("", help="Comma-separated categories"),
):
    """Fetch market data from configured API."""
    load_dotenv()
    from cli.core.sources.market import fetch_reports, DEFAULT_API_URL, DEFAULT_CATEGORIES

    url = api_url or os.environ.get("YMOS_MARKET_API_URL", DEFAULT_API_URL)
    key = api_key or os.environ.get("YMOS_MARKET_API_KEY", "")
    cats = [c.strip() for c in categories.split(",") if c.strip()] if categories else DEFAULT_CATEGORIES

    if not key:
        typer.echo("⚠️ No Market API Key provided (YMOS_MARKET_API_KEY)")
        typer.echo("   Use RSS as free alternative: ymos fetch-rss")
        raise typer.Exit(code=0)

    typer.echo(f"📡 Fetching market data from {url}")
    result = fetch_reports(url, key, days, cats)
    if not result:
        raise typer.Exit(code=1)

    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    count = result.get("count", "N/A") if isinstance(result, dict) else "N/A"
    typer.echo(f"\n💾 Saved: {out_path}")
    typer.echo(f"✅ {count} items")
