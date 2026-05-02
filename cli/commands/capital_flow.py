"""ymos fetch-capital-flow command — capital flow anomaly via Futu OpenD."""

from __future__ import annotations

import datetime as dt
import json
import os
import socket
from pathlib import Path

import typer

from cli.utils.env_loader import load_dotenv

app = typer.Typer(help="Fetch capital flow anomaly data via Futu OpenD")

OPEND_STARTUP_GUIDE = """
Futu OpenD 未运行或不可连接。请按以下步骤操作：

1. 打开富途牛牛客户端（或独立的 FutuOpenD）
2. 确保菜单「更多 → Futu OpenD」已开启，监听端口 11111
3. 如端口被修改，设置环境变量 FUTU_OPEND_PORT=端口号
4. 等待 OpenD 状态变为「已连接」后重试
"""


def _ticker_to_futu_symbol(ticker: str) -> str:
    """Convert YMOS ticker to Futu standard symbol format.

    YMOS: 0700.HK, AAPL, 688008.SS, 000001.SZ
    Futu: HK.00700, US.AAPL, SH.688008, SZ.000001
    """
    if "." in ticker:
        base, suffix = ticker.rsplit(".", 1)
        mapping = {
            "HK": "HK",
            "SS": "SH",
            "SZ": "SZ",
        }
        market = mapping.get(suffix.upper(), "US")
        if market == "HK":
            return f"HK.{base.zfill(5)}"
        return f"{market}.{base}"
    # No suffix → assume US
    return f"US.{ticker}"


def _detect_market(ticker: str) -> str:
    """Detect market from YMOS ticker: HK, US, CN."""
    if "." in ticker:
        _, suffix = ticker.rsplit(".", 1)
        if suffix.upper() in ("SS", "SZ"):
            return "CN"
        if suffix.upper() == "HK":
            return "HK"
    return "US"


def _check_opend_connection(host: str = "127.0.0.1", port: int = 11111) -> bool:
    """Check if Futu OpenD is reachable on the given host:port."""
    try:
        with socket.create_connection((host, port), timeout=3):
            return True
    except (ConnectionRefusedError, OSError, TimeoutError):
        return False


def _normalize_capital_flow(raw_data, market: str) -> dict:
    """Normalize capital flow data to unified schema across HK/US/CN markets.

    Unified schema:
    - anomaly_items: list of detected anomalies
    - dimensions_covered: which analysis dimensions returned data
    - notes: market-specific caveats
    """
    items = raw_data if isinstance(raw_data, list) else [raw_data] if raw_data else []
    dimensions = set()
    for item in items:
        if isinstance(item, dict):
            dim = item.get("dimension") or item.get("analysis_dimension", "")
            if dim:
                dimensions.add(dim)

    notes = []
    if market == "CN":
        notes.append("A 股资金流数据通常有 15 分钟延迟")
    elif market == "US":
        notes.append("美股资金流数据不含经纪商席位信息")

    return {
        "anomaly_items": items,
        "anomaly_count": len(items),
        "dimensions_covered": sorted(dimensions),
        "market": market,
        "notes": notes or None,
    }


def _fetch_capital_flow(ticker: str, time_range: int = 7, language_id: int = 0) -> dict:
    """Fetch capital flow anomaly data via Futu OpenD get_financial_unusual."""
    symbol = _ticker_to_futu_symbol(ticker)
    market = _detect_market(ticker)
    host = os.getenv("FUTU_OPEND_HOST", "127.0.0.1")
    port = int(os.getenv("FUTU_OPEND_PORT", "11111"))

    try:
        import futu as ft

        quote_ctx = ft.OpenQuoteContext(host=host, port=port)
        try:
            ret, data = quote_ctx.get_financial_unusual(
                symbol,
                time_range=time_range,
                analysis_dimensions=None,
                language_id=language_id,
            )
        finally:
            quote_ctx.close()

        if ret != ft.RET_OK:
            return {
                "ticker": ticker,
                "symbol": symbol,
                "market": market,
                "source": "futu_opend",
                "error": str(data),
                "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            }

        normalized = data
        if hasattr(data, "to_dict"):
            try:
                normalized = data.to_dict(orient="records")
            except TypeError:
                normalized = data.to_dict()

        normalized_schema = _normalize_capital_flow(normalized, market)

        return {
            "ticker": ticker,
            "symbol": symbol,
            "market": market,
            "source": "futu_opend",
            "method": "get_financial_unusual",
            "time_range": time_range,
            "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            **normalized_schema,
        }
    except ImportError:
        return {
            "ticker": ticker,
            "symbol": symbol,
            "market": market,
            "source": "none",
            "error": "futu-api SDK not installed. Run: uv add futu-api",
            "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        }
    except Exception as e:
        return {
            "ticker": ticker,
            "symbol": symbol,
            "market": market,
            "source": "none",
            "error": f"OpenD connection failed: {e}",
            "hint": "Ensure Futu OpenD is running on localhost:11111",
            "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
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
    ticker: str = typer.Option("", help="Single ticker to check capital flow"),
    from_state: bool = typer.Option(False, help="Read tickers from state machines"),
    output_dir: str = typer.Option("", help="Output directory for JSON results"),
    time_range: int = typer.Option(7, help="Time range in days (default 7)"),
):
    """Fetch capital flow anomaly data from Futu OpenD."""
    load_dotenv()

    host = os.getenv("FUTU_OPEND_HOST", "127.0.0.1")
    port = int(os.getenv("FUTU_OPEND_PORT", "11111"))
    if not _check_opend_connection(host, port):
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

    typer.echo(f"📊 Fetching capital flow for {len(tickers)} ticker(s): {', '.join(tickers)}")

    results = []
    for t in tickers:
        futu_sym = _ticker_to_futu_symbol(t)
        typer.echo(f"  → {t} ({futu_sym})...", nl=False)
        result = _fetch_capital_flow(t, time_range=time_range)
        results.append(result)
        if result.get("error"):
            typer.echo(f" ❌ {result['error']}")
        else:
            typer.echo(" ✅")

    now = dt.datetime.now()
    output = {
        "fetched_at": now.isoformat(),
        "count": len(results),
        "time_range": time_range,
        "results": results,
    }

    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        file_path = out_path / f"capital_flow_{now.strftime('%Y%m%d')}.json"
    else:
        from cli.core.paths import get_paths
        paths = get_paths()
        default_dir = paths.radar / "raw" / now.strftime("%Y-%m")
        default_dir.mkdir(parents=True, exist_ok=True)
        file_path = default_dir / f"capital_flow_{now.strftime('%Y%m%d')}.json"

    file_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    typer.echo(f"\n💾 Saved: {file_path}")
