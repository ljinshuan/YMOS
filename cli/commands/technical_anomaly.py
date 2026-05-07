"""ymos fetch-technical-anomaly command — technical anomaly via Futu OpenD."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import typer

from cli.core.futu_utils import OPEND_STARTUP_GUIDE, check_opend_connection
from cli.utils.env_loader import load_dotenv

app = typer.Typer(help="Fetch technical anomaly data via Futu OpenD")

INDICATOR_CHOICES = [
    "CCI", "KDJ", "BIAS", "AR", "BR", "VR", "PSY", "OSC", "WMSR",
    "MACD", "BOLL", "MA", "RSI6", "RSI12", "RSI24",
]


def _read_tickers_from_state() -> list[str]:
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
    ticker: str = typer.Option("", help="Single ticker (e.g. 0700.HK, AAPL)"),
    from_state: bool = typer.Option(False, help="Read tickers from state machines"),
    output_dir: str = typer.Option("", help="Output directory for JSON results"),
    time_range: int = typer.Option(7, help="Time range in days (default 7)"),
    indicators: list[str] = typer.Option(None, help="Filter to specific indicators"),
):
    """Fetch technical anomaly data from Futu OpenD."""
    load_dotenv()

    if not check_opend_connection():
        from cli.core.futu_utils import _resolve_opend_addr
        host, port = _resolve_opend_addr()
        typer.echo(f"❌ 无法连接 Futu OpenD ({host}:{port})")
        typer.echo(OPEND_STARTUP_GUIDE)
        raise typer.Exit(code=1)

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

    indicator_filters = indicators if indicators else None
    if indicator_filters:
        typer.echo(f"📊 Fetching technical anomaly for {len(tickers)} ticker(s) [{', '.join(indicator_filters)}]")
    else:
        typer.echo(f"📊 Fetching technical anomaly for {len(tickers)} ticker(s) [全扫]")

    from cli.core.sources.technical_anomaly import fetch_technical_anomaly

    results = []
    for t in tickers:
        typer.echo(f"  → {t}...", nl=False)
        result = fetch_technical_anomaly(t, time_range=time_range, indicator_filters=indicator_filters)
        results.append(result)
        if result.get("error"):
            typer.echo(f" ❌ {result['error']}")
        else:
            count = len(result.get("anomalies", []))
            typer.echo(f" ✅ ({count} anomalies)")

    now = dt.datetime.now()
    output = {
        "fetched_at": now.isoformat(),
        "count": len(results),
        "time_range": time_range,
        "indicator_filters": indicator_filters,
        "results": results,
    }

    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        file_path = out_path / f"technical_anomaly_{now.strftime('%Y%m%d')}.json"
    else:
        from cli.core.paths import get_paths
        paths = get_paths()
        default_dir = paths.radar / "raw" / now.strftime("%Y-%m")
        default_dir.mkdir(parents=True, exist_ok=True)
        file_path = default_dir / f"technical_anomaly_{now.strftime('%Y%m%d')}.json"

    file_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    typer.echo(f"\n💾 Saved: {file_path}")
