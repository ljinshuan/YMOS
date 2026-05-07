"""ymos position fetch command — fetch real holdings from Futu OpenD."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import typer

from cli.core.futu_utils import OPEND_STARTUP_GUIDE, check_opend_connection, _resolve_opend_addr
from cli.core.sources.futu_position import fetch_positions
from cli.utils.env_loader import load_dotenv

app = typer.Typer(help="Position management — fetch and display holdings")


def _format_number(value: float, decimals: int = 2) -> str:
    """Format number with comma separators."""
    if abs(value) >= 1:
        return f"{value:,.{decimals}f}"
    return f"{value:.{decimals}f}"


def _to_json(positions: list[dict], fetched_at: str) -> dict:
    """Build JSON output structure."""
    return {
        "meta": {
            "source": "futu_opend",
            "fetched_at": fetched_at,
            "position_count": len(positions),
        },
        "positions": positions,
    }


def _to_markdown(positions: list[dict], fetched_at: str) -> str:
    """Build Markdown output with table and summary."""
    date_str = fetched_at[:10]
    lines = [
        f"# 持仓明细 ({date_str})",
        "",
        "| 代码 | 名称 | 数量 | 成本价 | 当前价 | 市值 | 盈亏 | 盈亏% |",
        "|------|------|------|--------|--------|------|------|-------|",
    ]

    total_mv = 0.0
    total_pl = 0.0
    for p in positions:
        mv = p.get("market_value", 0)
        pl = p.get("profit_loss", 0)
        pl_pct = p.get("profit_loss_pct", 0)
        total_mv += mv
        total_pl += pl
        sign = "+" if pl >= 0 else ""
        lines.append(
            f"| {p['ticker']} | {p['name']} | {int(p['quantity'])} "
            f"| {_format_number(p['cost_price'])} | {_format_number(p['current_price'])} "
            f"| {_format_number(mv)} | {sign}{_format_number(pl)} "
            f"| {sign}{_format_number(pl_pct)}% |"
        )

    total_pl_pct = (total_pl / (total_mv - total_pl) * 100) if (total_mv - total_pl) != 0 else 0
    sign = "+" if total_pl >= 0 else ""
    lines.append("")
    lines.append(
        f"**汇总**: 总市值 ¥{_format_number(total_mv)} "
        f"| 总盈亏 ¥{sign}{_format_number(total_pl)} ({sign}{_format_number(total_pl_pct)}%)"
    )

    return "\n".join(lines)


@app.command("fetch")
def fetch_cmd(
    output_dir: str = typer.Option("", help="Output directory"),
    format: str = typer.Option("both", help="Output format: json, markdown, both"),
):
    """Fetch current positions from Futu OpenD."""
    load_dotenv()

    if not check_opend_connection():
        host, port = _resolve_opend_addr()
        typer.echo(f"无法连接 Futu OpenD ({host}:{port})")
        typer.echo(OPEND_STARTUP_GUIDE)
        raise typer.Exit(code=1)

    host, port = _resolve_opend_addr()
    typer.echo("正在从 Futu OpenD 获取持仓数据...")
    positions = fetch_positions(host=host, port=port)

    if positions is None:
        typer.echo("获取持仓失败，请检查 Futu OpenD 连接和登录状态")
        raise typer.Exit(code=1)

    if len(positions) == 0:
        typer.echo("当前账户无持仓")
        return

    now = dt.datetime.now()
    fetched_at = now.isoformat(timespec="seconds")
    date_tag = now.strftime("%Y%m%d")

    # Determine output directory
    if output_dir:
        out_path = Path(output_dir)
    else:
        from cli.core.paths import get_paths
        paths = get_paths()
        out_path = paths.data / "position"

    out_path.mkdir(parents=True, exist_ok=True)

    # Write outputs
    if format in ("json", "both"):
        json_data = _to_json(positions, fetched_at)
        json_path = out_path / f"positions_{date_tag}.json"
        json_path.write_text(json.dumps(json_data, ensure_ascii=False, indent=2), encoding="utf-8")
        typer.echo(f"JSON saved: {json_path}")

    if format in ("markdown", "both"):
        md_text = _to_markdown(positions, fetched_at)
        md_path = out_path / f"positions_{date_tag}.md"
        md_path.write_text(md_text, encoding="utf-8")
        typer.echo(f"Markdown saved: {md_path}")

    # Print summary to console
    typer.echo(f"\n共 {len(positions)} 只持仓")
    for p in positions:
        pl = p["profit_loss"]
        sign = "+" if pl >= 0 else ""
        typer.echo(f"  {p['ticker']} {p['name']} | {int(p['quantity'])}股 | {sign}{_format_number(pl)} ({sign}{_format_number(p['profit_loss_pct'])}%)")
