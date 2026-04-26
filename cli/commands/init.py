"""ymos init command — initialise directories, stocks, templates."""

from __future__ import annotations

from pathlib import Path

import typer

from cli.utils.env_loader import load_dotenv

app = typer.Typer(help="Initialise YMOS directories, stocks, and templates")


@app.command()
def dirs():
    """Create all standard data/ sub-directories."""
    load_dotenv()
    from cli.core.paths import get_paths

    paths = get_paths()
    created = paths.ensure_dirs()
    typer.echo(f"✅ Ensured {len(created)} directories exist under {paths.data}")


@app.command()
def stock(
    ticker: str = typer.Option(..., help="Stock ticker, e.g. AAPL"),
    name: str = typer.Option("", help="Stock name, e.g. Apple"),
    location: str = typer.Option("watchlist", help="holdings | watchlist"),
):
    """Initialise a new stock folder with a knowledge-base template."""
    load_dotenv()
    from cli.core.paths import get_paths

    paths = get_paths()
    base = paths.holdings_dir if location == "holdings" else paths.watchlist_dir
    stock_dir = base / ticker.upper()
    stock_dir.mkdir(parents=True, exist_ok=True)

    kb_path = stock_dir / f"{ticker.upper()}_知识库.md"
    if not kb_path.exists():
        kb_path.write_text(
            f"# {name or ticker.upper()} 知识库\n\n"
            f"## 基本信息\n\n"
            f"- Ticker: {ticker.upper()}\n"
            f"- 名称: {name or '—'}\n"
            f"- 加入日期: {__import__('datetime').date.today().isoformat()}\n\n"
            f"## 投资逻辑\n\n（待补充）\n\n"
            f"## 关键事件\n\n（待补充）\n",
            encoding="utf-8",
        )
        typer.echo(f"✅ Created {kb_path}")
    else:
        typer.echo(f"ℹ️  Knowledge base already exists: {kb_path}")

    typer.echo(f"✅ Stock folder ready: {stock_dir}")


@app.command()
def template(
    type: str = typer.Option("knowledge-base", help="Template type: knowledge-base | memo"),
    ticker: str = typer.Option("", help="Ticker for the template"),
    name: str = typer.Option("", help="Name for the template"),
):
    """Generate a template file for a stock."""
    load_dotenv()
    from cli.core.paths import get_paths

    paths = get_paths()
    tmpl_dir = paths.templates
    tmpl_dir.mkdir(parents=True, exist_ok=True)

    if type == "knowledge-base":
        content = (
            f"# {name or 'TICKER'} 知识库\n\n"
            f"## 基本信息\n\n"
            f"- Ticker: {ticker or 'TICKER'}\n"
            f"- 名称: {name or '—'}\n\n"
            f"## 投资逻辑\n\n（待补充）\n\n"
            f"## 关键事件\n\n（待补充）\n"
        )
        filename = "knowledge-base.md"
    else:
        content = (
            f"# {name or 'TICKER'} 备忘录\n\n"
            f"日期: {__import__('datetime').date.today().isoformat()}\n\n"
            f"## 摘要\n\n（待补充）\n"
        )
        filename = "memo.md"

    out = tmpl_dir / filename
    out.write_text(content, encoding="utf-8")
    typer.echo(f"✅ Template created: {out}")
