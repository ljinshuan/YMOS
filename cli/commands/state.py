"""ymos state command — state machine operations."""

from __future__ import annotations

import json

import typer

from cli.utils.env_loader import load_dotenv

app = typer.Typer(help="State machine read / update / validate")


@app.command()
def read(
    target: str = typer.Argument(help="State file: holdings | watchlist | preferences"),
    output_json: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Read and display a state machine."""
    load_dotenv()
    from cli.core.paths import get_paths
    from cli.core.state import read_state

    paths = get_paths()
    state_map = {
        "holdings": paths.holdings_state,
        "watchlist": paths.watchlist_state,
        "preferences": paths.preferences,
    }
    filepath = state_map.get(target)
    if not filepath:
        typer.echo(f"Unknown target: {target}. Use: holdings, watchlist, preferences")
        raise typer.Exit(code=1)
    if not filepath.exists():
        typer.echo(f"State file not found: {filepath}")
        raise typer.Exit(code=1)

    records = read_state(filepath)
    if output_json:
        # Remove __meta__ from output
        clean = [{k: v for k, v in r.items() if k != "__meta__"} for r in records]
        typer.echo(json.dumps(clean, ensure_ascii=False, indent=2))
    else:
        typer.echo(filepath.read_text(encoding="utf-8"))


@app.command()
def update(
    target: str = typer.Argument(help="State file: holdings | watchlist"),
    ticker: str = typer.Option(..., help="Ticker to match"),
    field: str = typer.Option(..., help="Field to update"),
    value: str = typer.Option(..., help="New value"),
):
    """Update a specific field for a ticker in a state machine."""
    load_dotenv()
    from cli.core.paths import get_paths
    from cli.core.state import update_row

    paths = get_paths()
    state_map = {
        "holdings": paths.holdings_state,
        "watchlist": paths.watchlist_state,
    }
    filepath = state_map.get(target)
    if not filepath:
        typer.echo(f"Unknown target: {target}. Use: holdings, watchlist")
        raise typer.Exit(code=1)

    # Find the ticker column name
    from cli.core.state import read_state as _read
    records = _read(filepath)
    if not records:
        typer.echo("No records found")
        raise typer.Exit(code=1)

    # Detect ticker column
    first = records[0]
    ticker_col = None
    for col in first:
        if col.lower() in ("ticker", "代码", "标的"):
            ticker_col = col
            break
    if not ticker_col:
        typer.echo("Could not find ticker column in state machine")
        raise typer.Exit(code=1)

    found = update_row(filepath, ticker_col, ticker, {field: value})
    if found:
        typer.echo(f"✅ Updated {ticker}: {field} = {value}")
    else:
        typer.echo(f"❌ Ticker not found: {ticker}")
        raise typer.Exit(code=1)


@app.command()
def validate():
    """Validate all state machine files exist and are parseable."""
    load_dotenv()
    from cli.core.paths import get_paths
    from cli.core.state import read_state

    paths = get_paths()
    state_files = {
        "holdings": paths.holdings_state,
        "watchlist": paths.watchlist_state,
        "preferences": paths.preferences,
    }

    all_ok = True
    for name, filepath in state_files.items():
        if not filepath.exists():
            typer.echo(f"❌ {name}: file not found ({filepath})")
            all_ok = False
            continue
        try:
            records = read_state(filepath)
            typer.echo(f"✅ {name}: {len(records)} records ({filepath.name})")
        except Exception as e:
            typer.echo(f"❌ {name}: parse error — {e}")
            all_ok = False

    if all_ok:
        typer.echo("\n✅ All state files valid")
    else:
        typer.echo("\n❌ Some state files have issues")
        raise typer.Exit(code=1)
