"""ymos tech-analysis command — technical indicator analysis."""

from __future__ import annotations

import datetime as dt
import os
from pathlib import Path

import typer

from cli.utils.env_loader import load_dotenv

app = typer.Typer(help="Technical analysis — indicators, signals, multi-timeframe")


def format_report(ticker: str, result: dict, date_str: str) -> str:
    """Format analysis result as Markdown report."""
    summary = result["summary"]
    lines = [
        f"# {ticker} 技术面分析 ({date_str})",
        "",
        f"## 综合判断: {summary['verdict']}",
        summary["note"],
        "",
    ]

    for timeframe, label in [("daily", "日线"), ("weekly", "周线")]:
        signals = result[timeframe]
        lines.append(f"## {label}")
        lines.append("| 维度 | 指标 | 当前值 | 信号 |")
        lines.append("|------|------|--------|------|")
        for s in signals:
            lines.append(f"| {s['dimension']} | {s['name']} | {s['value']} | {s['signal']} |")
        lines.append("")

    lines.append("## 关键信号摘要")

    all_signals = result["daily"] + result["weekly"]
    bullish = [s for s in all_signals if s["signal"] == "多头"]
    bearish = [s for s in all_signals if s["signal"] == "空头"]

    if bullish:
        top_bull = bullish[:3]
        for s in top_bull:
            lines.append(f"- {s.get('note', s['name'])} ({s['name']})")

    if bearish:
        top_bear = bearish[:3]
        for s in top_bear:
            lines.append(f"- {s.get('note', s['name'])} ({s['name']})")

    if not bullish and not bearish:
        lines.append("- 所有指标均为中性，无明显多空信号")

    lines.append("")
    return "\n".join(lines)


@app.command()
def analyze(
    symbols: str = typer.Option("", help="Comma-separated tickers"),
    from_state: bool = typer.Option(False, help="Read tickers from state machines"),
    output_dir: str = typer.Option("", help="Output directory for reports"),
    source: str = typer.Option("auto", help="Data source: auto, futu, yahoo, tushare"),
):
    """Run technical analysis and generate reports."""
    load_dotenv()

    from cli.core.paths import get_paths
    from cli.core.sources.history import fetch_history
    from cli.core.tech import analyze as run_analysis
    from cli.core.sources.news import extract_tickers_from_state_machine

    paths = get_paths()

    tickers: list[str] = []
    if symbols:
        tickers.extend(s.strip().upper() for s in symbols.split(",") if s.strip())

    if from_state:
        for state_file in [paths.watchlist_state, paths.holdings_state]:
            for t in extract_tickers_from_state_machine(state_file, us_only=False):
                if t not in tickers:
                    tickers.append(t)

    if not tickers:
        typer.echo("No symbols provided. Use --symbols or --from-state")
        raise typer.Exit(code=1)

    typer.echo(f"📊 Running tech analysis for {len(tickers)} tickers: {', '.join(tickers)}")

    tushare_token = os.getenv("TUSHARE_TOKEN", "")

    if source not in ("auto", "futu", "yahoo", "tushare"):
        typer.echo(f"❌ Unknown source: {source}. Use auto, futu, yahoo, or tushare")
        raise typer.Exit(code=1)

    if source == "futu":
        from cli.core.futu_utils import check_opend_connection, OPEND_STARTUP_GUIDE
        if not check_opend_connection():
            typer.echo("❌ Futu OpenD not reachable but --source futu was specified")
            typer.echo(OPEND_STARTUP_GUIDE)
            raise typer.Exit(code=1)

    history = fetch_history(tickers, tushare_token, source=source)

    if not history:
        typer.echo("❌ No historical data fetched for any ticker")
        raise typer.Exit(code=1)

    now = dt.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    month_str = now.strftime("%Y-%m")

    out_base = Path(output_dir) if output_dir else paths.reports / "tech" / month_str
    out_base.mkdir(parents=True, exist_ok=True)

    for ticker, df in history.items():
        typer.echo(f"  🔍 Analyzing {ticker} ({len(df)} bars)...")
        result = run_analysis(df)
        report = format_report(ticker, result, date_str)

        out_file = out_base / f"{ticker}_技术面分析.md"
        out_file.write_text(report, encoding="utf-8")
        typer.echo(f"  ✅ {ticker} → {out_file}")

    typer.echo(f"✅ Done. Reports saved to {out_base}")
