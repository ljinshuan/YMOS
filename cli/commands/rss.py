"""ymos fetch-rss command — RSS data fetching."""

from __future__ import annotations

import json
from pathlib import Path

import typer

from cli.utils.env_loader import load_dotenv

app = typer.Typer(help="Fetch RSS data from configured sources")


@app.command()
def fetch(
    days: float = typer.Option(1.0, help="Fetch data from last N days"),
    config: str = typer.Option("", help="Custom RSS config file path"),
    category: str = typer.Option("", help="Filter by category"),
    output: str = typer.Option("financial_data.json", help="Output JSON path"),
    url: str = typer.Option("", help="Single RSS source URL (bypasses config)"),
):
    """Fetch RSS data from configured or specified sources."""
    load_dotenv()
    from cli.core.sources.rss import fetch_rss, fetch_all_sources, load_sources

    if url:
        typer.echo(f"\n🚀 Single source mode: {url}")
        items = fetch_rss(url, int(days))
        if items and items != "BLOCKED_403":
            result = {
                "source": url,
                "fetched_at": __import__("datetime").datetime.now(
                    __import__("datetime").timezone.utc
                ).isoformat(),
                "time_range_days": days,
                "count": len(items),
                "data": items,
            }
        else:
            typer.echo("No data fetched")
            raise typer.Exit(code=1)
    else:
        sources = load_sources(
            category_filter=category or None,
            config_path=config or None,
        )
        if not sources:
            typer.echo("No sources available")
            raise typer.Exit(code=1)
        result = fetch_all_sources(sources, int(days))

    if result and result.get("count", 0) > 0:
        out_path = Path(output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        typer.echo(f"\n💾 Saved: {out_path}")
        typer.echo(f"✅ {result['count']} items fetched")

        cat_summary = result.get("categories_summary", {})
        if cat_summary:
            typer.echo("\n📁 By category:")
            for cat, num in sorted(cat_summary.items()):
                typer.echo(f"   {cat}: {num}")
    else:
        typer.echo("No data fetched")
        raise typer.Exit(code=1)
