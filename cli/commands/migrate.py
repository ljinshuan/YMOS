"""ymos migrate command — migrate old directory structure to data/."""

from __future__ import annotations

import shutil
from pathlib import Path

import typer

from cli.utils.env_loader import load_dotenv

app = typer.Typer(help="Migrate old directory structure to data/")


@app.command()
def run():
    """Migrate data from old paths (Eyes/, Brain/, 持仓与关注/) to data/."""
    load_dotenv()
    from cli.core.paths import get_paths

    paths = get_paths()
    root = paths.root
    migrated = 0

    # State machines
    old_state_files = {
        root / "持仓与关注" / "持仓_状态机.md": paths.holdings_state,
        root / "持仓与关注" / "Watchlist_状态机.md": paths.watchlist_state,
        root / "持仓与关注" / "当前关注方向与投资偏好.md": paths.preferences,
    }
    for old, new in old_state_files.items():
        if old.exists() and not new.exists():
            new.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(old, new)
            typer.echo(f"  📋 {old.name} → {new}")
            migrated += 1

    # Stock folders
    for label, old_base, new_base in [
        ("holdings", root / "持仓与关注" / "持仓", paths.holdings_dir),
        ("watchlist", root / "持仓与关注" / "动态Watchlist", paths.watchlist_dir),
    ]:
        if not old_base.exists():
            continue
        for stock_dir in old_base.iterdir():
            if stock_dir.is_dir() and not stock_dir.name.startswith("_"):
                target = new_base / stock_dir.name
                if not target.exists():
                    shutil.copytree(stock_dir, target)
                    typer.echo(f"  📁 [{label}] {stock_dir.name} → {target}")
                    migrated += 1

    # Reports
    for label, old_base, new_base in [
        ("market-insight", root / "Eyes" / "市场洞察", paths.market_insight),
        ("radar", root / "Eyes" / "投资雷达", paths.radar),
        ("strategy", root / "Brain" / "策略分析", paths.strategy),
    ]:
        if not old_base.exists():
            continue
        for md_file in old_base.rglob("*.md"):
            rel = md_file.relative_to(old_base)
            target = new_base / rel
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(md_file, target)
                migrated += 1
        # Also copy JSON raw data
        for json_file in old_base.rglob("*.json"):
            rel = json_file.relative_to(old_base)
            target = new_base / rel
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(json_file, target)
                migrated += 1

    if migrated:
        typer.echo(f"\n✅ Migrated {migrated} items to data/")
    else:
        typer.echo("Nothing to migrate (data/ already up to date)")
