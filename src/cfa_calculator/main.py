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
    ),
    formulas: Optional[bool] = typer.Option(
        None,
        "--formulas",
        "-f",
        help="Show formula reference guide",
    )
):
    """CFA Calculator CLI Tool."""
    if version:
        from cfa_calculator import __version__
        typer.echo(f"CFA Calculator version {__version__}")
        raise typer.Exit()

    if formulas:
        show_formula_reference()
        raise typer.Exit()

    # Launch interactive mode if no subcommand provided or --interactive flag used
    if interactive or ctx.invoked_subcommand is None:
        from cfa_calculator.interactive import InteractiveMode
        mode = InteractiveMode()
        mode.run()
        raise typer.Exit()


def show_formula_reference():
    """Display formula reference guide."""
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import box

    console = Console()

    console.print("\n[bold cyan]CFA Calculator - Formula Reference Guide[/bold cyan]\n")

    # Time Value of Money
    tvm_table = Table(title="Time Value of Money (TVM)", box=box.ROUNDED, show_header=True, header_style="bold magenta")
    tvm_table.add_column("Calculation", style="cyan", width=20)
    tvm_table.add_column("Formula", style="green")
    tvm_table.add_row("Future Value", "FV = PV × (1 + r/freq)^(n×freq)")
    tvm_table.add_row("Present Value", "PV = FV / (1 + r/freq)^(n×freq)")
    tvm_table.add_row("Annuity FV", "FV = PMT × [(1 + r)^n - 1] / r")
    tvm_table.add_row("Annuity PV", "PV = PMT × [1 - (1 + r)^-n] / r")
    tvm_table.add_row("Perpetuity", "PV = PMT / r")
    tvm_table.add_row("Growing Perpetuity", "PV = PMT / (r - g)")
    tvm_table.add_row("EAR", "EAR = (1 + stated_rate/freq)^freq - 1")
    console.print(tvm_table)
    console.print()

    # Portfolio Management
    portfolio_table = Table(title="Portfolio Management", box=box.ROUNDED, show_header=True, header_style="bold magenta")
    portfolio_table.add_column("Calculation", style="cyan", width=20)
    portfolio_table.add_column("Formula", style="green")
    portfolio_table.add_row("Sharpe Ratio", "Sharpe = (Rp - Rf) / σp")
    portfolio_table.add_row("Treynor Ratio", "Treynor = (Rp - Rf) / βp")
    portfolio_table.add_row("Jensen's Alpha", "α = Rp - [Rf + βp(Rm - Rf)]")
    portfolio_table.add_row("Beta", "β = Cov(Ra, Rm) / Var(Rm)")
    portfolio_table.add_row("CAPM", "E(Ri) = Rf + βi[E(Rm) - Rf]")
    portfolio_table.add_row("Sortino Ratio", "Sortino = (Rp - Target) / Downside σ")
    console.print(portfolio_table)
    console.print()

    # Fixed Income
    bond_table = Table(title="Fixed Income (Bonds)", box=box.ROUNDED, show_header=True, header_style="bold magenta")
    bond_table.add_column("Calculation", style="cyan", width=20)
    bond_table.add_column("Formula", style="green")
    bond_table.add_row("Bond Price", "P = Σ[C/(1+y)^t] + FV/(1+y)^n")
    bond_table.add_row("Current Yield", "Current Yield = Annual Coupon / Price")
    bond_table.add_row("Macaulay Duration", "MacDur = Σ[t × PV(CFt)] / Bond Price")
    bond_table.add_row("Modified Duration", "ModDur = MacDur / (1 + YTM/freq)")
    bond_table.add_row("Convexity", "Convexity = Σ[t(t+1) × PV(CFt)] / [P×(1+y)^2]")
    console.print(bond_table)
    console.print()

    # Equity Valuation
    equity_table = Table(title="Equity Valuation", box=box.ROUNDED, show_header=True, header_style="bold magenta")
    equity_table.add_column("Calculation", style="cyan", width=20)
    equity_table.add_column("Formula", style="green")
    equity_table.add_row("Gordon Growth (DDM)", "V0 = D1 / (r - g)")
    equity_table.add_row("FCFE Valuation", "V0 = FCFE1 / (r - g)")
    equity_table.add_row("P/E Valuation", "V0 = EPS × P/E")
    equity_table.add_row("Justified P/E", "P/E = Payout × (1 + g) / (r - g)")
    equity_table.add_row("PEG Ratio", "PEG = P/E / (g × 100)")
    console.print(equity_table)
    console.print()

    # Derivatives
    option_table = Table(title="Derivatives (Options)", box=box.ROUNDED, show_header=True, header_style="bold magenta")
    option_table.add_column("Calculation", style="cyan", width=20)
    option_table.add_column("Formula", style="green")
    option_table.add_row("Call Payoff", "max(S - K, 0)")
    option_table.add_row("Put Payoff", "max(K - S, 0)")
    option_table.add_row("Put-Call Parity", "C + PV(K) = P + S")
    option_table.add_row("Black-Scholes", "C = S×N(d1) - K×e^(-rT)×N(d2)")
    console.print(option_table)
    console.print()

    # Other Calculations
    other_table = Table(title="Other Calculations", box=box.ROUNDED, show_header=True, header_style="bold magenta")
    other_table.add_column("Calculation", style="cyan", width=20)
    other_table.add_column("Formula", style="green")
    other_table.add_row("NPV", "NPV = Σ[CFt / (1 + r)^t]")
    other_table.add_row("IRR", "0 = Σ[CFt / (1 + IRR)^t]")
    other_table.add_row("Profitability Index", "PI = PV(future CFs) / Initial Investment")
    other_table.add_row("Payback Period", "Time until Σ(Cash Flows) = Investment")
    console.print(other_table)
    console.print()

    # Statistics
    stats_table = Table(title="Statistics", box=box.ROUNDED, show_header=True, header_style="bold magenta")
    stats_table.add_column("Calculation", style="cyan", width=20)
    stats_table.add_column("Formula", style="green")
    stats_table.add_row("Mean", "μ = Σx / n")
    stats_table.add_row("Variance", "σ² = Σ(x - μ)² / (n-1)")
    stats_table.add_row("Std Deviation", "σ = √Variance")
    stats_table.add_row("Covariance", "Cov(X,Y) = Σ[(xi - μx)(yi - μy)] / (n-1)")
    stats_table.add_row("Correlation", "ρ = Cov(X,Y) / (σx × σy)")
    stats_table.add_row("Z-Score", "z = (x - μ) / σ")
    console.print(stats_table)
    console.print()

    help_text = """
[bold]Usage Examples:[/bold]
  cfa tvm fv --pv 1000 --rate 0.05 --n 10 --explain
  cfa portfolio sharpe --return 0.12 --rf 0.03 --std 0.15 --explain
  cfa equity ddm --dividend 5.0 --required-return 0.12 --growth 0.05 --explain

[bold]Tips:[/bold]
  • Add --explain flag to any command to see the formula
  • Use mathematical expressions: cfa tvm fv --pv "13*3*365" --rate 0.07 --n 1
  • Launch interactive mode: cfa -i
  • Get command help: cfa tvm fv --help
    """
    console.print(Panel(help_text, title="[bold cyan]Quick Reference[/bold cyan]", border_style="cyan"))
    console.print()


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
