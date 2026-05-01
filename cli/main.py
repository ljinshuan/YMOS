"""YMOS CLI — unified entry point."""

import typer

app = typer.Typer(
    name="ymos",
    help="YMOS - Your Market Operating System (勇麦投资操作系统)",
    no_args_is_help=True,
)

# Register command groups
from cli.commands import price, rss, market, news, state, init, report, migrate, tech

app.add_typer(price.app, name="price-scan")
app.add_typer(rss.app, name="fetch-rss")
app.add_typer(market.app, name="fetch-market")
app.add_typer(news.app, name="fetch-news")
app.add_typer(state.app, name="state")
app.add_typer(init.app, name="init")
app.add_typer(report.app, name="report")
app.add_typer(migrate.app, name="migrate")
app.add_typer(tech.app, name="tech-analysis")


if __name__ == "__main__":
    app()
