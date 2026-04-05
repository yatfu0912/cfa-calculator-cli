"""Portfolio Management CLI commands."""

import typer
from typing import List
from cfa_calculator.formulas.portfolio_formulas import (
    calculate_sharpe_ratio,
    calculate_treynor_ratio,
    calculate_jensens_alpha,
    calculate_sortino_ratio,
    calculate_beta,
    calculate_capm,
    calculate_portfolio_return,
    calculate_covariance,
    calculate_correlation,
)
from cfa_calculator.utils.formatters import format_result, print_error
from cfa_calculator.utils.validators import validate_positive

app = typer.Typer(help="Portfolio Management calculations")


@app.command()
def sharpe(
    portfolio_return: float = typer.Option(..., "--return", "-r", help="Portfolio return (as decimal)"),
    risk_free_rate: float = typer.Option(..., "--rf", help="Risk-free rate (as decimal)"),
    portfolio_std: float = typer.Option(..., "--std", "-s", help="Portfolio standard deviation (as decimal)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate Sharpe Ratio."""
    try:
        validate_positive(portfolio_std, "Portfolio standard deviation")

        result = calculate_sharpe_ratio(portfolio_return, risk_free_rate, portfolio_std)

        inputs = {
            "Portfolio Return (Rp)": f"{portfolio_return * 100:.2f}%",
            "Risk-Free Rate (Rf)": f"{risk_free_rate * 100:.2f}%",
            "Portfolio Std Dev (σp)": f"{portfolio_std * 100:.2f}%",
        }

        results = {"Sharpe Ratio": f"{result:.4f}"}

        formula = "Sharpe = (Rp - Rf) / σp" if explain else None
        notes = "Higher Sharpe ratio indicates better risk-adjusted return"

        format_result("Sharpe Ratio", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def treynor(
    portfolio_return: float = typer.Option(..., "--return", "-r", help="Portfolio return (as decimal)"),
    risk_free_rate: float = typer.Option(..., "--rf", help="Risk-free rate (as decimal)"),
    beta: float = typer.Option(..., "--beta", "-b", help="Portfolio beta"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate Treynor Ratio."""
    try:
        result = calculate_treynor_ratio(portfolio_return, risk_free_rate, beta)

        inputs = {
            "Portfolio Return (Rp)": f"{portfolio_return * 100:.2f}%",
            "Risk-Free Rate (Rf)": f"{risk_free_rate * 100:.2f}%",
            "Beta (βp)": f"{beta:.4f}",
        }

        results = {"Treynor Ratio": f"{result:.4f}"}

        formula = "Treynor = (Rp - Rf) / βp" if explain else None
        notes = "Measures excess return per unit of systematic risk"

        format_result("Treynor Ratio", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def alpha(
    portfolio_return: float = typer.Option(..., "--return", "-r", help="Portfolio return (as decimal)"),
    risk_free_rate: float = typer.Option(..., "--rf", help="Risk-free rate (as decimal)"),
    beta: float = typer.Option(..., "--beta", "-b", help="Portfolio beta"),
    market_return: float = typer.Option(..., "--market-return", "-m", help="Market return (as decimal)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate Jensen's Alpha."""
    try:
        result = calculate_jensens_alpha(portfolio_return, risk_free_rate, beta, market_return)

        inputs = {
            "Portfolio Return (Rp)": f"{portfolio_return * 100:.2f}%",
            "Risk-Free Rate (Rf)": f"{risk_free_rate * 100:.2f}%",
            "Beta (βp)": f"{beta:.4f}",
            "Market Return (Rm)": f"{market_return * 100:.2f}%",
        }

        results = {"Jensen's Alpha (α)": f"{result * 100:.4f}%"}

        formula = "α = Rp - [Rf + βp(Rm - Rf)]" if explain else None
        notes = "Positive alpha indicates outperformance relative to CAPM"

        format_result("Jensen's Alpha", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def sortino(
    portfolio_return: float = typer.Option(..., "--return", "-r", help="Portfolio return (as decimal)"),
    target_return: float = typer.Option(..., "--target", "-t", help="Target return or risk-free rate (as decimal)"),
    downside_deviation: float = typer.Option(..., "--downside-std", "-d", help="Downside deviation (as decimal)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate Sortino Ratio."""
    try:
        validate_positive(downside_deviation, "Downside deviation")

        result = calculate_sortino_ratio(portfolio_return, target_return, downside_deviation)

        inputs = {
            "Portfolio Return (Rp)": f"{portfolio_return * 100:.2f}%",
            "Target Return": f"{target_return * 100:.2f}%",
            "Downside Deviation (σd)": f"{downside_deviation * 100:.2f}%",
        }

        results = {"Sortino Ratio": f"{result:.4f}"}

        formula = "Sortino = (Rp - Target) / σd" if explain else None
        notes = "Similar to Sharpe but only penalizes downside volatility"

        format_result("Sortino Ratio", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def beta(
    asset_returns: str = typer.Option(..., "--asset-returns", help="Asset returns as comma-separated values (e.g., 0.1,0.15,0.12)"),
    market_returns: str = typer.Option(..., "--market-returns", help="Market returns as comma-separated values"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate Beta."""
    try:
        asset_ret = [float(x.strip()) for x in asset_returns.split(",")]
        market_ret = [float(x.strip()) for x in market_returns.split(",")]

        result = calculate_beta(asset_ret, market_ret)

        inputs = {
            "Asset Returns": f"{len(asset_ret)} observations",
            "Market Returns": f"{len(market_ret)} observations",
        }

        results = {"Beta (β)": f"{result:.4f}"}

        formula = "β = Cov(Ra, Rm) / Var(Rm)" if explain else None
        notes = "β > 1: more volatile than market; β < 1: less volatile; β = 1: same as market"

        format_result("Beta Calculation", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def capm(
    risk_free_rate: float = typer.Option(..., "--rf", help="Risk-free rate (as decimal)"),
    beta: float = typer.Option(..., "--beta", "-b", help="Asset beta"),
    market_return: float = typer.Option(..., "--market-return", "-m", help="Expected market return (as decimal)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate required return using CAPM."""
    try:
        result = calculate_capm(risk_free_rate, beta, market_return)

        inputs = {
            "Risk-Free Rate (Rf)": f"{risk_free_rate * 100:.2f}%",
            "Beta (β)": f"{beta:.4f}",
            "Market Return (Rm)": f"{market_return * 100:.2f}%",
        }

        results = {"Required Return E(Ri)": f"{result * 100:.4f}%"}

        formula = "E(Ri) = Rf + βi[E(Rm) - Rf]" if explain else None
        notes = "CAPM calculates the expected return based on systematic risk"

        format_result("CAPM Required Return", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def portfolio_return(
    weights: str = typer.Option(..., "--weights", "-w", help="Asset weights as comma-separated values (must sum to 1)"),
    returns: str = typer.Option(..., "--returns", "-r", help="Expected returns as comma-separated values"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate expected portfolio return."""
    try:
        weight_list = [float(x.strip()) for x in weights.split(",")]
        return_list = [float(x.strip()) for x in returns.split(",")]

        result = calculate_portfolio_return(weight_list, return_list)

        inputs = {
            "Weights": ", ".join([f"{w:.2%}" for w in weight_list]),
            "Returns": ", ".join([f"{r:.2%}" for r in return_list]),
        }

        results = {"Portfolio Return E(Rp)": f"{result * 100:.4f}%"}

        formula = "E(Rp) = Σ(wi × E(Ri))" if explain else None

        format_result("Portfolio Expected Return", inputs, results, formula)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def covariance(
    returns1: str = typer.Option(..., "--returns1", help="Returns for asset 1 as comma-separated values"),
    returns2: str = typer.Option(..., "--returns2", help="Returns for asset 2 as comma-separated values"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate covariance between two assets."""
    try:
        ret1 = [float(x.strip()) for x in returns1.split(",")]
        ret2 = [float(x.strip()) for x in returns2.split(",")]

        cov_result = calculate_covariance(ret1, ret2)
        corr_result = calculate_correlation(ret1, ret2)

        inputs = {
            "Asset 1 Returns": f"{len(ret1)} observations",
            "Asset 2 Returns": f"{len(ret2)} observations",
        }

        results = {
            "Covariance": f"{cov_result:.6f}",
            "Correlation": f"{corr_result:.4f}",
        }

        formula = "Cov(X,Y) = E[(X - μx)(Y - μy)]" if explain else None

        format_result("Covariance & Correlation", inputs, results, formula)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)
