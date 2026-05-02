"""ymos monitor commands — automated market watching via Futu OpenD."""

from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path

import typer

from cli.utils.env_loader import load_dotenv

app = typer.Typer(help="Market monitoring — fetch prices and check strategy signals")

KLINE_MAP = {
    "1m": None,  # filled after futu import
    "5m": None,
    "15m": None,
    "60m": None,
}


def _get_kline_type(kline: str):
    """Map kline string to Futu KLType enum."""
    import futu as ft

    mapping = {
        "1m": ft.KLType.K_1M,
        "5m": ft.KLType.K_5M,
        "15m": ft.KLType.K_15M,
        "60m": ft.KLType.K_60M,
    }
    return mapping[kline]


def _fetch_kline(
    ticker: str,
    kline_type,
    count: int,
    host: str,
    port: int,
) -> list[list[str]] | None:
    """Fetch kline data from Futu OpenD for a single ticker.

    Returns list of [timestamp, open, high, low, close, volume] rows, or None on error.
    """
    import futu as ft

    from cli.core.futu_utils import ticker_to_futu_symbol

    symbol = ticker_to_futu_symbol(ticker)
    end_date = dt.datetime.now(dt.timezone.utc)
    start_date = end_date - dt.timedelta(days=count + 30)  # extra buffer for minute klines

    try:
        quote_ctx = ft.OpenQuoteContext(host=host, port=port)
        try:
            ret, data, page_req_key = quote_ctx.request_history_kline(
                symbol,
                start=start_date.strftime("%Y-%m-%d"),
                end=end_date.strftime("%Y-%m-%d"),
                ktype=kline_type,
                autype=ft.AuType.QFQ,
                max_count=count,
            )
        finally:
            quote_ctx.close()
    except Exception as e:
        typer.echo(f"⚠️  Futu OpenD error for {ticker}: {e}", err=True)
        return None

    if ret != ft.RET_OK:
        typer.echo(f"⚠️  Futu API error for {ticker}: {data}", err=True)
        return None

    if data is None or data.empty:
        return []

    rows = []
    for _, row in data.iterrows():
        ts = str(row.get("time_key", ""))
        o = row.get("open", "")
        h = row.get("high", "")
        lo = row.get("low", "")
        c = row.get("close", "")
        v = row.get("volume", "")
        if ts:
            rows.append([ts, str(o), str(h), str(lo), str(c), str(v)])
    return rows


def _get_snapshot_price(rows: list[list[str]]) -> dict:
    """Extract latest price info from kline rows for snapshot."""
    if not rows:
        return {}
    latest = rows[-1]
    prev = rows[-2] if len(rows) >= 2 else latest
    try:
        close = float(latest[4])
        prev_close = float(prev[4])
        change_pct = round((close - prev_close) / prev_close * 100, 2) if prev_close else 0
    except (ValueError, ZeroDivisionError):
        close = 0
        change_pct = 0
    return {
        "price": close,
        "open": float(latest[1]) if latest[1] else 0,
        "high": float(latest[2]) if latest[2] else 0,
        "low": float(latest[3]) if latest[3] else 0,
        "close": close,
        "volume": int(float(latest[5])) if latest[5] else 0,
        "change_pct": change_pct,
        "source": "futu_opend",
    }


@app.command()
def fetch_prices(
    symbols: str = typer.Option("", help="Comma-separated tickers"),
    from_state: bool = typer.Option(False, help="Read tickers from state machines"),
    output_dir: str = typer.Option("data/monitor", help="Output root directory"),
    kline: str = typer.Option("5m", help="Minute kline period: 1m/5m/15m/60m"),
    count: int = typer.Option(60, help="Number of recent candles to fetch"),
    skip_non_trading_hours: bool = typer.Option(True, help="Skip tickers outside trading hours"),
):
    """Fetch kline data via Futu OpenD and accumulate to CSV history."""
    load_dotenv()

    import futu as ft

    from cli.core.futu_utils import OPEND_STARTUP_GUIDE, check_opend_connection
    from cli.core.paths import get_paths
    from cli.core.sources.news import extract_tickers_from_state_machine
    from cli.monitor.history import merge_kline_to_csv
    from cli.monitor.trading_hours import classify_market, is_trading_hours

    # Validate kline period
    if kline not in KLINE_MAP:
        typer.echo(f"Invalid kline period: {kline}. Use: 1m, 5m, 15m, 60m", err=True)
        raise typer.Exit(code=1)

    # Resolve tickers
    tickers: list[str] = []
    if symbols:
        tickers.extend(s.strip().upper() for s in symbols.split(",") if s.strip())

    if from_state:
        paths = get_paths()
        for state_file in [paths.watchlist_state, paths.holdings_state]:
            for t in extract_tickers_from_state_machine(state_file, us_only=False):
                if t not in tickers:
                    tickers.append(t)

    if not tickers:
        typer.echo("No symbols provided. Use --symbols or --from-state", err=True)
        raise typer.Exit(code=1)

    # Check OpenD connection
    host = os.getenv("FUTU_OPEND_HOST", "127.0.0.1")
    port = int(os.getenv("FUTU_OPEND_PORT", "11111"))

    if not check_opend_connection(host, port):
        typer.echo(OPEND_STARTUP_GUIDE, err=True)
        raise typer.Exit(code=1)

    # Filter by trading hours
    if skip_non_trading_hours:
        active = [t for t in tickers if is_trading_hours(t)]
        skipped = set(tickers) - set(active)
        if skipped:
            for t in sorted(skipped):
                market = classify_market(t)
                typer.echo(f"⏭️  {t} ({market}) outside trading hours, skipping")
        if not active:
            typer.echo("All tickers outside trading hours")
            return
        tickers = active

    typer.echo(f"📊 Fetching kline for {len(tickers)} tickers: {', '.join(tickers)}")

    root = Path(output_dir)
    now = dt.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H%M")

    kline_type = _get_kline_type(kline)
    snapshot_tickers: dict[str, dict] = {}

    for ticker in tickers:
        # Fetch daily kline
        daily_rows = _fetch_kline(ticker, ft.KLType.K_DAY, count, host, port)
        if daily_rows:
            csv_path = root / "history" / f"{ticker}_daily.csv"
            added = merge_kline_to_csv(csv_path, daily_rows)
            typer.echo(f"  {ticker} daily: {len(daily_rows)} fetched, {added} new rows")

        # Fetch minute kline
        minute_rows = _fetch_kline(ticker, kline_type, count, host, port)
        if minute_rows:
            csv_path = root / "history" / f"{ticker}_{kline}.csv"
            added = merge_kline_to_csv(csv_path, minute_rows)
            typer.echo(f"  {ticker} {kline}: {len(minute_rows)} fetched, {added} new rows")

        # Build snapshot from minute kline (more recent data)
        price_data = _get_snapshot_price(minute_rows or daily_rows or [])
        if price_data:
            snapshot_tickers[ticker] = price_data

    # Write snapshot
    if snapshot_tickers:
        snap_dir = root / "prices" / date_str
        snap_dir.mkdir(parents=True, exist_ok=True)
        snap_path = snap_dir / f"{time_str}.json"
        snapshot = {
            "fetched_at": now.strftime("%Y-%m-%d %H:%M:%S"),
            "tickers": snapshot_tickers,
        }
        snap_path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False))
        typer.echo(f"📁 Snapshot saved: {snap_path}")

    typer.echo(f"✅ Done — {len(snapshot_tickers)} tickers updated")


@app.command()
def check_signals(
    tickers: str = typer.Option("", help="Comma-separated tickers to check (empty = all)"),
    signal_dir: str = typer.Option("data/monitor/signals", help="Signal files directory"),
    output_dir: str = typer.Option("data/monitor", help="Output root directory"),
):
    """Scan strategy signal files and generate alerts for new signals."""
    load_dotenv()

    from cli.monitor.signal_reader import (
        find_new_signals,
        format_alert_entry,
        scan_signals,
        write_alerts,
    )

    sig_path = Path(signal_dir)
    root = Path(output_dir)

    # Parse ticker filter
    ticker_list: list[str] | None = None
    if tickers:
        ticker_list = [s.strip().upper() for s in tickers.split(",") if s.strip()]

    # Scan signals
    signals = scan_signals(sig_path, ticker_list)
    if not signals:
        return  # Silent exit, suitable for cron

    # Find new signals
    today = dt.datetime.now().strftime("%Y-%m-%d")
    alert_path = root / "alerts" / f"{today}.md"
    new_signals = find_new_signals(signals, alert_path)

    if not new_signals:
        return  # No new signals, silent exit

    # Write alerts
    written = write_alerts(alert_path, new_signals)

    # Print to terminal
    for sig in new_signals:
        typer.echo(format_alert_entry(sig))
        typer.echo("")

    typer.echo(f"📋 {written} new alert(s) written to {alert_path}")
