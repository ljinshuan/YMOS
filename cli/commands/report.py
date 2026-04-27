"""ymos report command — list reports."""

from __future__ import annotations

import re
from datetime import date

import typer

from cli.utils.env_loader import load_dotenv

app = typer.Typer(help="List and inspect reports")


@app.command()
def list_reports(
    type: str = typer.Option("all", help="Report type: insight | radar | strategy | all"),
    latest: bool = typer.Option(False, help="Show only the most recent report"),
    date_filter: str = typer.Option("", help="Filter by date (YYYY-MM-DD)"),
):
    """List available reports."""
    load_dotenv()
    from cli.core.paths import get_paths

    paths = get_paths()
    type_map = {
        "insight": paths.market_insight,
        "radar": paths.radar,
        "strategy": paths.strategy,
    }

    dirs_to_scan = [type_map[type]] if type in type_map else list(type_map.values())

    found: list[tuple[str, str]] = []
    for label, scan_dir in zip(
        ["insight", "radar", "strategy"],
        dirs_to_scan if len(dirs_to_scan) == 3 else [type_map.get(type, paths.reports)],
    ):
        if not scan_dir.exists():
            continue
        for md_file in sorted(scan_dir.rglob("*.md")):
            rel = md_file.relative_to(scan_dir)
            if date_filter and date_filter not in str(rel):
                continue
            found.append((label, str(md_file)))

    if not found:
        typer.echo("No reports found")
        return

    if latest:
        # Keep only the last one per type
        by_type: dict[str, list[str]] = {}
        for label, path in found:
            by_type.setdefault(label, []).append(path)
        for label in by_type:
            by_type[label] = [by_type[label][-1]]
        found = [(l, p) for l, paths_list in by_type.items() for p in paths_list]

    for label, path in found:
        typer.echo(f"  [{label}] {path}")
    typer.echo(f"\n{len(found)} reports found")
