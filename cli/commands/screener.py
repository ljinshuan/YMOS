"""ymos screen command — stock screening via Futu OpenD."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import typer

from cli.core.futu_utils import OPEND_STARTUP_GUIDE, check_opend_connection, create_quote_context
from cli.utils.env_loader import load_dotenv

app = typer.Typer(help="Stock screening via Futu OpenD")

PRESETS = {
    "growth": {
        "name": "成长股",
        "desc": "高营收增速 + 净利润增速，市值 > 100 亿",
        "filters": {
            "HK": ["REVENUE_YOY", "NET_PROFIT_YOY", "MARKET_VAL"],
            "US": ["REVENUE_YOY", "NET_PROFIT_YOY", "MARKET_VAL"],
            "CN": ["REVENUE_YOY", "NET_PROFIT_YOY", "MARKET_VAL"],
        },
    },
    "value": {
        "name": "价值股",
        "desc": "低 PE + 低 PB + 高 ROE + 高股息",
        "filters": {
            "HK": ["PE_TTM", "PB", "ROE_TTM", "DIVIDEND_YIELD"],
            "US": ["PE_TTM", "PB", "ROE_TTM", "DIVIDEND_YIELD"],
            "CN": ["PE_TTM", "PB", "ROE_TTM", "DIVIDEND_YIELD"],
        },
    },
    "high-dividend": {
        "name": "高息股",
        "desc": "股息率 > 4% + 低 PE + 市值 > 50 亿",
        "filters": {
            "HK": ["DIVIDEND_YIELD", "PE_TTM", "MARKET_VAL"],
            "US": ["DIVIDEND_YIELD", "PE_TTM", "MARKET_VAL"],
            "CN": ["DIVIDEND_YIELD", "PE_TTM", "MARKET_VAL"],
        },
    },
    "momentum": {
        "name": "动量股",
        "desc": "20 日涨幅 > 10% + 高换手率 + 市值 > 30 亿",
        "filters": {
            "HK": ["CHANGE_RATE", "TURNOVER_RATE", "MARKET_VAL"],
            "US": ["CHANGE_RATE", "TURNOVER_RATE", "MARKET_VAL"],
            "CN": ["CHANGE_RATE", "TURNOVER_RATE", "MARKET_VAL"],
        },
    },
}

# Sort order: True = ascending, False = descending
SORT_ASCENDING = {
    "PE_TTM": True,
    "PB": True,
}

FIELD_NAME_MAP = {
    "stock_code": "代码",
    "stock_name": "名称",
    "REVENUE_YOY": "营收增速",
    "NET_PROFIT_YOY": "净利润增速",
    "MARKET_VAL": "市值",
    "PE_TTM": "PE(TTM)",
    "PB": "PB",
    "ROE_TTM": "ROE",
    "DIVIDEND_YIELD": "股息率",
    "CHANGE_RATE": "涨幅",
    "TURNOVER_RATE": "换手率",
}


def _market_to_futu(market: str) -> str:
    return {"HK": "HK", "US": "US", "CN": "SH", "SH": "SH", "SZ": "SZ"}.get(
        market.upper(), "US"
    )


def _build_preset_filters(preset: str, market: str) -> list:
    """Build SimpleFilter list from preset name."""
    import futu as ft

    stock_field_map = {
        "REVENUE_YOY": ft.StockField.SUM_OF_BUSINESS_GROWTH,
        "NET_PROFIT_YOY": ft.StockField.NET_PROFIX_GROWTH,
        "MARKET_VAL": ft.StockField.MARKET_VAL,
        "PE_TTM": ft.StockField.PE_TTM,
        "PB": ft.StockField.PB_RATE,
        "ROE_TTM": ft.StockField.RETURN_ON_EQUITY_RATE,
        "DIVIDEND_YIELD": ft.StockField.PCF_TTM,
        "CHANGE_RATE": ft.StockField.CHANGE_RATE,
        "TURNOVER_RATE": ft.StockField.TURNOVER_RATE,
    }

    preset_cfg = PRESETS.get(preset)
    if not preset_cfg:
        return []

    market_key = market.upper()
    if market_key == "CN":
        market_key = "SH"
    fields = preset_cfg["filters"].get(market_key, preset_cfg["filters"]["HK"])
    primary = fields[0] if fields else None

    if primary and primary in stock_field_map:
        sf = ft.SimpleFilter()
        sf.stock_field = stock_field_map[primary]
        sf.is_no_filter = True
        sf.sort = ft.SortDir.ASCEND if SORT_ASCENDING.get(primary, False) else ft.SortDir.DESCEND
        return [sf]

    return []


def _build_custom_filters(config_data: dict) -> list:
    """Build SimpleFilter list from custom JSON config."""
    import futu as ft

    stock_field_map = {
        "revenue_yoy": ft.StockField.SUM_OF_BUSINESS_GROWTH,
        "net_profit_yoy": ft.StockField.NET_PROFIX_GROWTH,
        "market_val": ft.StockField.MARKET_VAL,
        "pe_ttm": ft.StockField.PE_TTM,
        "pb": ft.StockField.PB_RATE,
        "roe_ttm": ft.StockField.RETURN_ON_EQUITY_RATE,
        "dividend_yield": ft.StockField.PCF_TTM,
        "change_rate": ft.StockField.CHANGE_RATE,
        "turnover_rate": ft.StockField.TURNOVER_RATE,
    }

    filters = []
    sort_by = config_data.get("sort_by", "market_val")
    sort_asc = config_data.get("sort_asc", False)

    if sort_by in stock_field_map:
        sf = ft.SimpleFilter()
        sf.stock_field = stock_field_map[sort_by]
        sf.is_no_filter = True
        sf.sort = ft.SortDir.ASCEND if sort_asc else ft.SortDir.DESCEND
        filters.append(sf)

    return filters


def _run_screen(market: str, simple_filters: list, begin: int = 0, num: int = 20) -> dict:
    try:
        import futu as ft

        market_code = _market_to_futu(market)
        quote_ctx = create_quote_context()
        try:
            ret, data = quote_ctx.get_stock_filter(
                market=market_code,
                filter_list=simple_filters,
                begin=begin,
                num=num,
            )
        finally:
            quote_ctx.close()

        if ret != ft.RET_OK:
            return {"error": str(data)}

        # get_stock_filter returns (has_next_page, total_count, [FilterStockData])
        if isinstance(data, tuple) and len(data) == 3:
            _, total_count, stock_list = data
            results = []
            for item in stock_list:
                results.append({
                    "stock_code": getattr(item, "stock_code", ""),
                    "stock_name": getattr(item, "stock_name", ""),
                })
            return {"data": results, "count": len(results), "total": total_count}

        return {"data": [], "count": 0}

    except ImportError:
        return {"error": "futu-api SDK not installed. Run: uv add futu-api"}
    except Exception as e:
        return {"error": f"OpenD connection failed: {e}"}


def _generate_markdown_report(output: dict, preset_key: str = "") -> str:
    """Generate Markdown report from screening results."""
    now_str = output.get("fetched_at", "")[:10]
    market = output.get("market", "")
    preset = preset_key or output.get("preset", "custom")
    preset_name = PRESETS.get(preset, {}).get("name", preset)
    count = output.get("count", 0)
    results = output.get("results", [])

    lines = [
        f"# 选股结果 - {now_str}",
        "",
        f"- **市场**: {market}",
        f"- **筛选模板**: {preset_name} ({preset})",
        f"- **结果数量**: {count}",
        "",
    ]

    if not results:
        lines.append("**无符合条件的标的**")
        return "\n".join(lines)

    # Build table
    if isinstance(results[0], dict):
        cols = list(results[0].keys())
        header = "| " + " | ".join(cols) + " |"
        sep = "| " + " | ".join(["---"] * len(cols)) + " |"
        lines.append(header)
        lines.append(sep)
        for row in results[:50]:
            vals = [str(row.get(c, "")) for c in cols]
            lines.append("| " + " | ".join(vals) + " |")
    else:
        for item in results:
            lines.append(f"- {item}")

    lines.append("")
    lines.append("> 筛选结果仅供参考，不构成投资建议。如需深度分析，请对感兴趣的标的运行 `调研一下 [ticker]`。")
    return "\n".join(lines)


@app.command("screen")
def screen_cmd(
    market: str = typer.Option("HK", help="Market: HK, US, CN"),
    preset: str = typer.Option("", help="Preset: growth, value, high-dividend, momentum"),
    config: str = typer.Option("", help="Custom JSON config file path"),
    limit: int = typer.Option(20, help="Max results (default 20)"),
    output_dir: str = typer.Option("", help="Output directory"),
    list_presets: bool = typer.Option(False, help="List available presets"),
):
    """Screen stocks via Futu OpenD stock filter."""
    load_dotenv()

    if list_presets:
        typer.echo("Available presets:\n")
        for key, p in PRESETS.items():
            typer.echo(f"  {key:15s} — {p['name']}: {p['desc']}")
        return

    if not check_opend_connection():
        typer.echo("❌ 无法连接 Futu OpenD")
        typer.echo(OPEND_STARTUP_GUIDE)
        raise typer.Exit(code=1)

    if not preset and not config:
        typer.echo("Please specify --preset or --config. Use --list-presets to see options.")
        raise typer.Exit(code=1)

    simple_filters = []
    preset_key = ""
    if preset:
        preset_key = preset.lower().strip()
        if preset_key not in PRESETS:
            typer.echo(f"Unknown preset: {preset_key}. Use --list-presets.")
            raise typer.Exit(code=1)
        simple_filters = _build_preset_filters(preset_key, market)
    elif config:
        config_path = Path(config)
        if not config_path.exists():
            typer.echo(f"Config file not found: {config}")
            raise typer.Exit(code=1)
        config_data = json.loads(config_path.read_text(encoding="utf-8"))
        simple_filters = _build_custom_filters(config_data)

    if not simple_filters:
        typer.echo("No valid filter criteria. Check preset name or config format.")
        raise typer.Exit(code=1)

    typer.echo(f"🔍 Screening {market} stocks (preset: {preset or 'custom'}, limit: {limit})...")

    result = _run_screen(market, simple_filters, begin=0, num=limit)

    if "error" in result:
        typer.echo(f"❌ {result['error']}")
        raise typer.Exit(code=1)

    data = result.get("data", [])
    count = result.get("count", 0)
    typer.echo(f"✅ Found {count} stocks")

    now = dt.datetime.now()
    output = {
        "fetched_at": now.isoformat(),
        "market": market,
        "preset": preset_key or "custom",
        "limit": limit,
        "count": count,
        "results": data,
    }

    if output_dir:
        out_path = Path(output_dir)
    else:
        from cli.core.paths import get_paths

        paths = get_paths()
        out_path = paths.reports / "screener" / now.strftime("%Y-%m")
    out_path.mkdir(parents=True, exist_ok=True)

    # Save JSON
    json_path = out_path / f"screener_{now.strftime('%Y%m%d')}.json"
    json_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    typer.echo(f"💾 JSON: {json_path}")

    # Save Markdown
    md_content = _generate_markdown_report(output, preset_key)
    md_path = out_path / f"选股结果_{now.strftime('%Y-%m-%d')}.md"
    md_path.write_text(md_content, encoding="utf-8")
    typer.echo(f"📄 Markdown: {md_path}")
