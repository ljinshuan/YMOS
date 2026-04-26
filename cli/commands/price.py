"""ymos price-scan command — unified price fetching."""

from __future__ import annotations

import datetime as dt
import os
from pathlib import Path

import typer

from cli.utils.env_loader import load_dotenv

app = typer.Typer(help="Price scanning — fetch prices from multiple sources")


@app.command()
def scan(
    symbols: str = typer.Option("", help="Comma-separated tickers"),
    from_state: bool = typer.Option(False, help="Read tickers from state machines"),
    output_dir: str = typer.Option("", help="Output directory for JSON results"),
    date_tag: str = typer.Option("", help="Date tag for output files (YYYYMMDD)"),
):
    """Fetch prices for given symbols or from state machines."""
    load_dotenv()
    from cli.core.paths import get_paths
    from cli.core.router import route_prices
    from cli.core.sources.news import extract_tickers_from_state_machine

    paths = get_paths()

    # Resolve symbols
    tickers: list[str] = []
    if symbols:
        tickers.extend(s.strip().upper() for s in symbols.split(",") if s.strip())

    if from_state:
        # Read from both state machines
        for state_file in [paths.watchlist_state, paths.holdings_state]:
            for t in extract_tickers_from_state_machine(state_file, us_only=False):
                if t not in tickers:
                    tickers.append(t)

    if not tickers:
        typer.echo("No symbols provided. Use --symbols or --from-state")
        raise typer.Exit(code=1)

    typer.echo(f"📊 Fetching prices for {len(tickers)} tickers: {', '.join(tickers)}")

    # Default output dir
    tag = date_tag or dt.datetime.now().strftime("%Y%m%d")
    out = Path(output_dir) if output_dir else paths.radar_raw_dir(tag)

    finnhub_key = os.getenv("FINNHUB_API_KEY", "")
    tushare_token = os.getenv("TUSHARE_TOKEN", "")

    route_prices(tickers, out, tag, finnhub_key, tushare_token)
