"""ymos catalyst-calendar command — catalyst event management."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from cli.utils.env_loader import load_dotenv

app = typer.Typer(help="Catalyst calendar management")
console = Console()

DATA_DIR = Path("data/reports/catalyst-calendar")


def _month_dir(date: dt.date | None = None) -> Path:
    d = date or dt.date.today()
    return DATA_DIR / f"{d.year}-{d.month:02d}"


def _calendar_path(date: dt.date | None = None) -> Path:
    return _month_dir(date) / "催化剂日历.md"


def _load_calendar_events(date: dt.date | None = None) -> list[dict]:
    """Load events from the calendar markdown file. Simple JSON sidecar approach."""
    sidecar = _month_dir(date) / "events.json"
    if sidecar.exists():
        with open(sidecar, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def _save_calendar_events(events: list[dict], date: dt.date | None = None) -> None:
    sidecar = _month_dir(date) / "events.json"
    sidecar.parent.mkdir(parents=True, exist_ok=True)
    with open(sidecar, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)


@app.command("list")
def list_events(
    days: int = typer.Option(30, "--days", "-d", help="Number of days to look ahead"),
    impact: str | None = typer.Option(None, "--impact", "-i", help="Filter by impact: High/Medium/Low"),
    event_type: str | None = typer.Option(None, "--type", "-t", help="Filter by type: Earnings/Corporate/Industry/Macro"),
    ticker: str | None = typer.Option(None, "--ticker", help="Filter by ticker"),
) -> None:
    """List upcoming catalyst events."""
    load_dotenv()
    today = dt.date.today()
    end_date = today + dt.timedelta(days=days)

    # Load events from current and next month
    events: list[dict] = []
    events.extend(_load_calendar_events(today))
    next_month = today.replace(day=28) + dt.timedelta(days=4)
    events.extend(_load_calendar_events(next_month))

    # Filter
    filtered = []
    for ev in events:
        ev_date = dt.date.fromisoformat(ev.get("date", "2099-12-31"))
        if ev_date < today or ev_date > end_date:
            continue
        if impact and ev.get("impact") != impact:
            continue
        if event_type and ev.get("type") != event_type:
            continue
        if ticker and ticker not in ev.get("tickers", []):
            continue
        filtered.append(ev)

    if not filtered:
        console.print("[yellow]未找到符合条件的催化剂事件[/yellow]")
        return

    # Sort by date
    filtered.sort(key=lambda x: x.get("date", ""))

    table = Table(title=f"催化剂日历（未来 {days} 天）")
    table.add_column("日期", style="cyan")
    table.add_column("事件", style="white")
    table.add_column("类型", style="green")
    table.add_column("影响", style="yellow")
    table.add_column("标的", style="magenta")
    table.add_column("距今", style="blue", justify="right")

    for ev in filtered:
        ev_date = dt.date.fromisoformat(ev["date"])
        days_until = (ev_date - today).days
        impact_str = ev.get("impact", "Medium")
        if impact_str == "High":
            impact_str = f"[red]{impact_str}[/red]"
        table.add_row(
            ev["date"],
            ev.get("description", ""),
            ev.get("type", ""),
            impact_str,
            ", ".join(ev.get("tickers", [])),
            f"{days_until}天",
        )

    console.print(table)


@app.command("add")
def add_event(
    date: str = typer.Option(..., "--date", "-d", help="Event date (YYYY-MM-DD)"),
    description: str = typer.Option(..., "--description", help="Event description"),
    event_type: str = typer.Option("Corporate", "--type", "-t", help="Event type: Earnings/Corporate/Industry/Macro"),
    impact: str = typer.Option("Medium", "--impact", "-i", help="Impact level: High/Medium/Low"),
    tickers: str = typer.Option("", "--tickers", help="Comma-separated related tickers"),
    notes: str = typer.Option("", "--notes", "-n", help="Additional notes"),
) -> None:
    """Add a catalyst event to the calendar."""
    load_dotenv()

    event_date = dt.date.fromisoformat(date)
    event = {
        "date": date,
        "description": description,
        "type": event_type,
        "impact": impact,
        "tickers": [t.strip() for t in tickers.split(",") if t.strip()],
        "notes": notes,
    }

    events = _load_calendar_events(event_date)
    events.append(event)
    _save_calendar_events(events, event_date)

    console.print(f"[green]已添加事件: {date} {description}[/green]")


@app.command("fetch-earnings")
def fetch_earnings(
    tickers: str = typer.Option(..., "--tickers", "-t", help="Comma-separated tickers"),
    output_dir: str | None = typer.Option(None, "--output-dir", "-o", help="Output directory"),
) -> None:
    """Fetch earnings dates for given tickers."""
    load_dotenv()

    ticker_list = [t.strip() for t in tickers.split(",")]
    out = Path(output_dir) if output_dir else DATA_DIR
    out.mkdir(parents=True, exist_ok=True)

    results = []
    for ticker in ticker_list:
        console.print(f"[cyan]获取 {ticker} 财报日期...[/cyan]")
        try:
            from cli.core.router import get_source
            source = get_source(ticker)

            if source in ("finnhub", "yahoo"):
                import requests
                symbol = ticker.replace(".", "-")
                resp = requests.get(
                    f"https://finnhub.io/api/v1/calendar/earnings",
                    params={"symbol": symbol},
                    headers={"X-Finnhub-Token": _get_finnhub_key()},
                    timeout=10,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    for earning in data.get("earningsCalendar", []):
                        if earning.get("symbol") == symbol:
                            results.append({
                                "date": earning.get("date", ""),
                                "description": f"{ticker} 财报发布（{earning.get('period', '')}）",
                                "type": "Earnings",
                                "impact": "High",
                                "tickers": [ticker],
                                "notes": f"EPS 预期: {earning.get('epsEstimate', 'N/A')}",
                            })
                            break
            else:
                console.print(f"[yellow]{ticker}: A股/港股财报日期需通过其他数据源获取[/yellow]")

        except Exception as e:
            console.print(f"[red]{ticker} 获取失败: {e}[/red]")

    if results:
        for r in results:
            event_date = dt.date.fromisoformat(r["date"]) if r["date"] else dt.date.today()
            events = _load_calendar_events(event_date)
            events.append(r)
            _save_calendar_events(events, event_date)

        console.print(f"[green]已添加 {len(results)} 个财报事件到日历[/green]")
    else:
        console.print("[yellow]未获取到财报日期[/yellow]")


def _get_finnhub_key() -> str:
    import os
    return os.environ.get("FINNHUB_API_KEY", "")


@app.command("weekly")
def weekly_preview(
    output_dir: str | None = typer.Option(None, "--output-dir", "-o", help="Output directory"),
) -> None:
    """Generate weekly catalyst preview report."""
    load_dotenv()

    today = dt.date.today()
    week_start = today - dt.timedelta(days=today.weekday())
    week_end = week_start + dt.timedelta(days=6)

    events: list[dict] = []
    for offset in range(14):
        d = today + dt.timedelta(days=offset)
        events.extend(_load_calendar_events(d))

    # Filter to this week
    week_events = [
        e for e in events
        if week_start <= dt.date.fromisoformat(e.get("date", "2099-12-31")) <= week_end
    ]
    week_events.sort(key=lambda x: x.get("date", ""))

    # Generate report
    out = Path(output_dir) if output_dir else _month_dir()
    out.mkdir(parents=True, exist_ok=True)
    report_path = out / f"催化剂周报_{today.isoformat()}.md"

    lines = [
        f"# 催化剂周报 — {week_start.isoformat()} 至 {week_end.isoformat()}",
        f"",
        f"> 生成日期：{today.isoformat()}",
        f"",
        f"## 本周关键事件",
        f"",
    ]

    for ev in week_events:
        impact = "High" if ev.get("impact") == "High" else "Medium" if ev.get("impact") == "Medium" else "Low"
        lines.append(f"- **{ev['date']}** {ev.get('description', '')}（{ev.get('type', '')}）")
        if ev.get("tickers"):
            lines.append(f"   - 关联标的：{', '.join(ev['tickers'])}")
        if ev.get("notes"):
            lines.append(f"   - 备注：{ev['notes']}")
        lines.append("")

    if not week_events:
        lines.append("本周无催化剂事件。")
        lines.append("")

    next_week_events = [
        ev for ev in events
        if week_end < dt.date.fromisoformat(ev.get("date", "2099-12-31")) <= week_end + dt.timedelta(days=7)
    ]
    lines.extend([
        "## 下周前瞻",
        "",
        *(f"- {ev['date']} {ev.get('description', '')}（{ev.get('impact', '')}）"
          for ev in next_week_events),
        "",
        "## 风险提示",
        "",
        *(f"- {ev['date']} {ev.get('description', '')}（高影响事件需特别关注）"
          for ev in week_events if ev.get("impact") == "High"),
    ])

    if not any(ev.get("impact") == "High" for ev in week_events):
        lines.append("- 本周无高影响事件")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    console.print(f"[green]周报已生成: {report_path}[/green]")


@app.command("export")
def export_excel(
    output: str | None = typer.Option(None, "--output", "-o", help="Output file path"),
    days: int = typer.Option(90, "--days", "-d", help="Number of days to export"),
) -> None:
    """Export catalyst calendar to Excel."""
    load_dotenv()

    try:
        from cli.excel_writer import write_excel
    except ImportError:
        console.print("[red]Excel 输出功能未安装。请运行: uv add openpyxl xlsxwriter[/red]")
        raise typer.Exit(1)

    today = dt.date.today()
    end_date = today + dt.timedelta(days=days)

    events: list[dict] = []
    for offset in range(days):
        d = today + dt.timedelta(days=offset)
        events.extend(_load_calendar_events(d))

    filtered = [
        e for e in events
        if today <= dt.date.fromisoformat(e.get("date", "2099-12-31")) <= end_date
    ]
    filtered.sort(key=lambda x: x.get("date", ""))

    out_path = Path(output) if output else _month_dir() / f"催化剂日历_{today.isoformat()}.xlsx"

    rows_by_date = [[e["date"], e.get("description", ""), e.get("type", ""), e.get("impact", ""),
                      ", ".join(e.get("tickers", [])), e.get("notes", "")] for e in filtered]

    rows_by_ticker = []
    for e in filtered:
        for t in e.get("tickers", [""]):
            rows_by_ticker.append([t, e["date"], e.get("description", ""), e.get("impact", "")])

    rows_by_impact = sorted(rows_by_date, key=lambda x: {"High": 0, "Medium": 1, "Low": 2}.get(x[3], 3))

    write_excel(
        out_path,
        sheets=[
            {
                "name": "按日期排序",
                "title": f"催化剂日历 — {today.isoformat()}",
                "headers": ["日期", "事件", "类型", "影响等级", "关联标的", "备注"],
                "rows": rows_by_date,
                "column_widths": [12, 40, 12, 10, 20, 30],
            },
            {
                "name": "按标的分组",
                "title": "催化剂 — 按标的",
                "headers": ["标的", "日期", "事件", "影响等级"],
                "rows": rows_by_ticker,
                "column_widths": [12, 12, 40, 10],
            },
            {
                "name": "按影响排序",
                "title": "催化剂 — 按影响等级",
                "headers": ["日期", "事件", "类型", "影响等级", "关联标的", "备注"],
                "rows": rows_by_impact,
                "column_widths": [12, 40, 12, 10, 20, 30],
            },
        ],
    )

    console.print(f"[green]Excel 已导出: {out_path}[/green]")
