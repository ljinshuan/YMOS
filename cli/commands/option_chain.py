"""ymos fetch-option-chain command — option chain data via Futu OpenD."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import typer

from cli.core.futu_utils import OPEND_STARTUP_GUIDE, check_opend_connection, _resolve_opend_addr
from cli.core.sources.option_chain import (
    MONEYNESS_ALL, MONEYNESS_ATM, MONEYNESS_OUTSIDE, MONEYNESS_WITHIN,
    OPTION_TYPE_ALL, OPTION_TYPE_CALL, OPTION_TYPE_PUT,
)
from cli.utils.env_loader import load_dotenv

app = typer.Typer(help="Fetch option chain data from Futu OpenD")

OPTION_TYPE_CHOICES = [OPTION_TYPE_ALL, OPTION_TYPE_CALL, OPTION_TYPE_PUT]
MONEYNESS_CHOICES = [MONEYNESS_ALL, MONEYNESS_ATM, MONEYNESS_OUTSIDE, MONEYNESS_WITHIN]


def _read_tickers_from_state() -> list[str]:
    """Read tickers from holdings and watchlist state machines."""
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
    ticker: str = typer.Option("", help="Single ticker (e.g. AAPL, BABA, 0700.HK)"),
    from_state: bool = typer.Option(False, help="Read tickers from state machines"),
    output_dir: str = typer.Option("", help="Output directory for JSON results"),
    start: str = typer.Option("", help="Start date (expiry), e.g. 2026-05-08"),
    end: str = typer.Option("", help="End date (expiry), e.g. 2026-05-15"),
    option_type: str = typer.Option(OPTION_TYPE_ALL, help="Option type: ALL/CALL/PUT"),
    moneyness: str = typer.Option(MONEYNESS_ALL, help="Moneyness: ALL/ATM/OUTSIDE/WITHIN"),
):
    """Fetch option chain data from Futu OpenD."""
    load_dotenv()

    # Check OpenD connection
    if not check_opend_connection():
        host, port = _resolve_opend_addr()
        typer.echo(f"❌ 无法连接 Futu OpenD ({host}:{port})")
        typer.echo(OPEND_STARTUP_GUIDE)
        raise typer.Exit(code=1)

    # Determine tickers to fetch
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

    typer.echo(f"📊 Fetching option chain for {len(tickers)} ticker(s)")

    # Fetch option chain for each ticker
    from cli.core.sources.option_chain import fetch_option_chain

    results = []
    for t in tickers:
        typer.echo(f"  → {t}...", nl=False)
        result = fetch_option_chain(t, start=start or None, end=end or None,
                                option_type=option_type, moneyness=moneyness)
        results.append(result)

        if result.get("error"):
            typer.echo(f" ❌ {result['error']}")
        else:
            contract_count = len(result.get("contracts", []))
            typer.echo(f" ✅ ({contract_count} contracts)")

    # Determine output directory
    now = dt.datetime.now()
    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        file_path = out_path / f"option_chain_{now.strftime('%Y%m%d')}.json"
    else:
        from cli.core.paths import get_paths
        paths = get_paths()
        default_dir = paths.radar / "raw" / now.strftime("%Y-%m")
        default_dir.mkdir(parents=True, exist_ok=True)
        file_path = default_dir / f"option_chain_{now.strftime('%Y%m%d')}.json"

    # Write output
    output = {
        "fetched_at": now.isoformat(),
        "count": len(results),
        "results": results,  # 直接使用 results 数组
    }
    file_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    typer.echo(f"\n💾 Saved: {file_path}")
