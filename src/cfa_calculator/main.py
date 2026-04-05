"""Main CLI entry point for CFA Calculator."""

import typer
from typing import Optional

app = typer.Typer(
    name="cfa",
    help="CFA Calculator - Command-line tool for financial calculations",
    no_args_is_help=True,
)


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit",
        is_eager=True,
    )
):
    """CFA Calculator CLI Tool."""
    if version:
        from cfa_calculator import __version__
        typer.echo(f"CFA Calculator version {__version__}")
        raise typer.Exit()


# Import and register command groups
from cfa_calculator.commands import tvm, portfolio, bond, stats, other

app.add_typer(tvm.app, name="tvm", help="Time Value of Money calculations")
app.add_typer(portfolio.app, name="portfolio", help="Portfolio Management calculations")
app.add_typer(bond.app, name="bond", help="Fixed Income (Bond) calculations")
app.add_typer(stats.app, name="stats", help="Statistical calculations")
app.add_typer(other.app, name="other", help="Other calculations (NPV, IRR, etc.)")


if __name__ == "__main__":
    app()
