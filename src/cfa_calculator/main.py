"""Main CLI entry point for CFA Calculator."""

import typer
from typing import Optional

app = typer.Typer(
    name="cfa",
    help="""CFA Calculator - Comprehensive financial calculations tool

    \b
    Features:
    • 50+ financial calculations across 7 modules
    • Interactive mode with bilingual support (English/Chinese)
    • Command-line mode for advanced users
    • All formulas match CFA curriculum

    \b
    Quick Start:
      cfa                    Launch interactive mode
      cfa -i                 Launch interactive mode
      cfa tvm fv --help      Get help for specific command
      cfa --version          Show version

    \b
    Modules:
      tvm        Time Value of Money (FV, PV, Annuity, Perpetuity, EAR)
      portfolio  Portfolio Management (Sharpe, Treynor, Alpha, Beta, CAPM)
      bond       Fixed Income (Bond Price, YTM, Duration, Convexity)
      stats      Statistics (Descriptive, Z-Score, Correlation, etc.)
      other      Other Calculations (NPV, IRR, Payback, etc.)
      equity     Equity Valuation (DDM, P/E, PEG, FCFE)
      option     Derivatives (Black-Scholes, Binomial, Put-Call Parity)

    \b
    Examples:
      cfa tvm fv --pv 1000 --rate 0.05 --n 10
      cfa tvm fv --pv 100000 --rate 0.07 --n 1/12 --freq 12
      cfa equity ddm --dividend 5.0 --required-return 0.12 --growth 0.05
      cfa option black-scholes --type call --spot 100 --strike 100 --time 1.0 --rf 0.05 --vol 0.20

    \b
    GitHub: https://github.com/yatfu0912/cfa-calculator-cli
    """,
    no_args_is_help=True,
)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit",
        is_eager=True,
    ),
    interactive: Optional[bool] = typer.Option(
        None,
        "--interactive",
        "-i",
        help="Launch interactive mode",
    )
):
    """CFA Calculator CLI Tool."""
    if version:
        from cfa_calculator import __version__
        typer.echo(f"CFA Calculator version {__version__}")
        raise typer.Exit()

    # Launch interactive mode if no subcommand provided or --interactive flag used
    if interactive or ctx.invoked_subcommand is None:
        from cfa_calculator.interactive import InteractiveMode
        mode = InteractiveMode()
        mode.run()
        raise typer.Exit()


# Import and register command groups
from cfa_calculator.commands import tvm, portfolio, bond, stats, other, equity, option

app.add_typer(tvm.app, name="tvm", help="Time Value of Money calculations")
app.add_typer(portfolio.app, name="portfolio", help="Portfolio Management calculations")
app.add_typer(bond.app, name="bond", help="Fixed Income (Bond) calculations")
app.add_typer(stats.app, name="stats", help="Statistical calculations")
app.add_typer(other.app, name="other", help="Other calculations (NPV, IRR, etc.)")
app.add_typer(equity.app, name="equity", help="Equity Valuation calculations")
app.add_typer(option.app, name="option", help="Derivatives and Option pricing calculations")


if __name__ == "__main__":
    app()
