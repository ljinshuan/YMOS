"""ymos trade-history fetch command — fetch deal records from Futu OpenD."""

from __future__ import annotations

import datetime as dt
import json
from collections import defaultdict
from pathlib import Path

import typer

from cli.core.futu_utils import OPEND_STARTUP_GUIDE, check_opend_connection, _resolve_opend_addr
from cli.core.sources.futu_deals import fetch_deals
from cli.utils.env_loader import load_dotenv

app = typer.Typer(help="Trade history — fetch and display deal records")


def _format_number(value: float, decimals: int = 2) -> str:
    """Format number with comma separators."""
    if abs(value) >= 1:
        return f"{value:,.{decimals}f}"
    return f"{value:.{decimals}f}"


def _to_json(deals: list[dict], fetched_at: str, start_date: str, end_date: str) -> dict:
    """Build JSON output structure."""
    return {
        "meta": {
            "source": "futu_opend",
            "fetched_at": fetched_at,
            "start_date": start_date,
            "end_date": end_date,
            "deal_count": len(deals),
        },
        "deals": deals,
    }


def _to_markdown(deals: list[dict], fetched_at: str, start_date: str, end_date: str) -> str:
    """Build Markdown output with summary and per-ticker tables."""
    date_str = fetched_at[:10]
    lines = [
        f"# 交易记录 ({date_str})",
        "",
        f"**时间范围**: {start_date} ~ {end_date}",
    ]

    # Summary stats
    buy_count = sum(1 for d in deals if d["side"] == "BUY")
    sell_count = sum(1 for d in deals if d["side"] == "SELL")
    buy_amount = sum(d["price"] * d["quantity"] for d in deals if d["side"] == "BUY")
    sell_amount = sum(d["price"] * d["quantity"] for d in deals if d["side"] == "SELL")
    total_fee = sum(d["fee"] for d in deals)

    lines.append("")
    lines.append("## 统计摘要")
    lines.append("")
    lines.append(f"- 总笔数: {len(deals)}")
    lines.append(f"- 买入: {buy_count} 笔，金额 {_format_number(buy_amount)}")
    lines.append(f"- 卖出: {sell_count} 笔，金额 {_format_number(sell_amount)}")
    lines.append(f"- 总手续费: {_format_number(total_fee)}")

    # Group by ticker
    by_ticker: dict[str, list[dict]] = defaultdict(list)
    for d in deals:
        by_ticker[d["ticker"]].append(d)

    for ticker, ticker_deals in sorted(by_ticker.items()):
        lines.append("")
        lines.append(f"## {ticker} ({ticker_deals[0]['name']})")
        lines.append("")
        lines.append("| 时间 | 方向 | 价格 | 数量 | 手续费 |")
        lines.append("|------|------|------|------|--------|")
        for d in sorted(ticker_deals, key=lambda x: x["timestamp"]):
            side_label = "买入" if d["side"] == "BUY" else "卖出"
            lines.append(
                f"| {d['timestamp']} | {side_label} "
                f"| {_format_number(d['price'])} "
                f"| {int(d['quantity'])} "
                f"| {_format_number(d['fee'])} |"
            )

    return "\n".join(lines)


@app.command("fetch")
def fetch_cmd(
    days: int = typer.Option(30, help="回看天数"),
    ticker: str = typer.Option("", help="按标的过滤（YMOS 格式，如 AAPL, 0700.HK）"),
    output_dir: str = typer.Option("", help="Output directory"),
    format: str = typer.Option("both", help="Output format: json, markdown, both"),
):
    """Fetch deal history from Futu OpenD."""
    load_dotenv()

    if not check_opend_connection():
        host, port = _resolve_opend_addr()
        typer.echo(f"无法连接 Futu OpenD ({host}:{port})")
        typer.echo(OPEND_STARTUP_GUIDE)
        raise typer.Exit(code=1)

    host, port = _resolve_opend_addr()

    now = dt.datetime.now()
    end_date = now.strftime("%Y-%m-%d")
    start_date = (now - dt.timedelta(days=days)).strftime("%Y-%m-%d")
    fetched_at = now.isoformat(timespec="seconds")
    date_tag = now.strftime("%Y%m%d")

    ticker_filter = ticker if ticker else None
    typer.echo(f"正在从 Futu OpenD 获取 {start_date} ~ {end_date} 的成交记录...")

    deals = fetch_deals(
        host=host, port=port,
        start_date=start_date, end_date=end_date,
        ticker=ticker_filter,
    )

    if deals is None:
        typer.echo("获取成交记录失败，请检查 Futu OpenD 连接和登录状态")
        raise typer.Exit(code=1)

    if len(deals) == 0:
        typer.echo(f"在 {start_date} ~ {end_date} 期间无成交记录")
        return

    # Determine output directory
    if output_dir:
        out_path = Path(output_dir)
    else:
        from cli.core.paths import get_paths
        paths = get_paths()
        out_path = paths.data / "trade-history"

    out_path.mkdir(parents=True, exist_ok=True)

    # Write outputs
    if format in ("json", "both"):
        json_data = _to_json(deals, fetched_at, start_date, end_date)
        json_path = out_path / f"deals_{date_tag}.json"
        json_path.write_text(json.dumps(json_data, ensure_ascii=False, indent=2), encoding="utf-8")
        typer.echo(f"JSON saved: {json_path}")

    if format in ("markdown", "both"):
        md_text = _to_markdown(deals, fetched_at, start_date, end_date)
        md_path = out_path / f"deals_{date_tag}.md"
        md_path.write_text(md_text, encoding="utf-8")
        typer.echo(f"Markdown saved: {md_path}")

    # Print summary to console
    buy_count = sum(1 for d in deals if d["side"] == "BUY")
    sell_count = sum(1 for d in deals if d["side"] == "SELL")
    typer.echo(f"\n共 {len(deals)} 笔成交（买入 {buy_count} / 卖出 {sell_count}）")
    for d in sorted(deals, key=lambda x: x["timestamp"]):
        side_label = "买" if d["side"] == "BUY" else "卖"
        typer.echo(
            f"  {d['timestamp']} {side_label} {d['ticker']} {d['name']} "
            f"| {_format_number(d['price'])} x {int(d['quantity'])}"
        )
