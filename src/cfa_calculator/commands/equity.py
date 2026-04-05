"""Equity Valuation CLI commands."""

import typer
from cfa_calculator.formulas.equity_formulas import (
    calculate_gordon_growth_model,
    calculate_multistage_ddm,
    calculate_fcfe_valuation,
    calculate_pe_valuation,
    calculate_justified_pe_ratio,
    calculate_peg_ratio,
)
from cfa_calculator.utils.formatters import format_result, print_error
from cfa_calculator.utils.validators import validate_positive

app = typer.Typer(help="Equity Valuation calculations")


@app.command()
def ddm(
    dividend: float = typer.Option(..., "--dividend", "-d", help="Expected dividend next year (D1)"),
    required_return: float = typer.Option(..., "--required-return", "-r", help="Required rate of return (as decimal)"),
    growth_rate: float = typer.Option(..., "--growth", "-g", help="Constant growth rate (as decimal)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate stock value using Gordon Growth Model (Constant Growth DDM)."""
    try:
        validate_positive(dividend, "Dividend")

        result = calculate_gordon_growth_model(dividend, required_return, growth_rate)

        inputs = {
            "Expected Dividend (D1)": f"${dividend:.2f}",
            "Required Return (r)": f"{required_return * 100:.2f}%",
            "Growth Rate (g)": f"{growth_rate * 100:.2f}%",
        }

        results = {"Stock Value (V0)": f"${result:.2f}"}

        formula = "V0 = D1 / (r - g)" if explain else None
        notes = "Gordon Growth Model assumes constant dividend growth forever"

        format_result("Gordon Growth Model (DDM)", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def multistage_ddm(
    current_dividend: float = typer.Option(..., "--current-dividend", "-d0", help="Current dividend (D0)"),
    high_growth_rate: float = typer.Option(..., "--high-growth", "-gh", help="High growth rate (as decimal)"),
    high_growth_years: int = typer.Option(..., "--high-years", "-n", help="Years of high growth"),
    stable_growth_rate: float = typer.Option(..., "--stable-growth", "-gs", help="Stable growth rate (as decimal)"),
    required_return: float = typer.Option(..., "--required-return", "-r", help="Required rate of return (as decimal)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate stock value using Two-Stage DDM."""
    try:
        validate_positive(current_dividend, "Current dividend")

        result = calculate_multistage_ddm(
            current_dividend,
            high_growth_rate,
            high_growth_years,
            stable_growth_rate,
            required_return
        )

        inputs = {
            "Current Dividend (D0)": f"${current_dividend:.2f}",
            "High Growth Rate": f"{high_growth_rate * 100:.2f}%",
            "High Growth Years": high_growth_years,
            "Stable Growth Rate": f"{stable_growth_rate * 100:.2f}%",
            "Required Return": f"{required_return * 100:.2f}%",
        }

        results = {"Stock Value (V0)": f"${result:.2f}"}

        formula = "V0 = PV(Stage 1 dividends) + PV(Terminal Value)" if explain else None
        notes = "Two-stage model: high growth period followed by stable growth"

        format_result("Two-Stage DDM", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def fcfe(
    fcfe: float = typer.Option(..., "--fcfe", "-f", help="Expected FCFE next year"),
    required_return: float = typer.Option(..., "--required-return", "-r", help="Required rate of return on equity (as decimal)"),
    growth_rate: float = typer.Option(..., "--growth", "-g", help="Constant growth rate (as decimal)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate equity value using Free Cash Flow to Equity (FCFE) model."""
    try:
        result = calculate_fcfe_valuation(fcfe, required_return, growth_rate)

        inputs = {
            "Expected FCFE": f"${fcfe:.2f}",
            "Required Return (r)": f"{required_return * 100:.2f}%",
            "Growth Rate (g)": f"{growth_rate * 100:.2f}%",
        }

        results = {"Equity Value": f"${result:.2f}"}

        formula = "V0 = FCFE1 / (r - g)" if explain else None
        notes = "FCFE = Cash available to equity holders after all expenses and reinvestment"

        format_result("FCFE Valuation", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def pe_valuation(
    eps: float = typer.Option(..., "--eps", "-e", help="Expected earnings per share"),
    benchmark_pe: float = typer.Option(..., "--pe", "-p", help="Benchmark P/E ratio"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate stock value using P/E ratio valuation."""
    try:
        result = calculate_pe_valuation(eps, benchmark_pe)

        inputs = {
            "Earnings Per Share (EPS)": f"${eps:.2f}",
            "Benchmark P/E Ratio": f"{benchmark_pe:.2f}",
        }

        results = {"Stock Value": f"${result:.2f}"}

        formula = "V0 = EPS × P/E" if explain else None
        notes = "Use industry average or comparable company P/E as benchmark"

        format_result("P/E Ratio Valuation", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def justified_pe(
    payout_ratio: float = typer.Option(..., "--payout", "-p", help="Dividend payout ratio (0 to 1)"),
    required_return: float = typer.Option(..., "--required-return", "-r", help="Required rate of return (as decimal)"),
    growth_rate: float = typer.Option(..., "--growth", "-g", help="Growth rate (as decimal)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate justified P/E ratio using Gordon Growth Model."""
    try:
        result = calculate_justified_pe_ratio(payout_ratio, required_return, growth_rate)

        inputs = {
            "Dividend Payout Ratio": f"{payout_ratio * 100:.2f}%",
            "Required Return (r)": f"{required_return * 100:.2f}%",
            "Growth Rate (g)": f"{growth_rate * 100:.2f}%",
        }

        results = {"Justified P/E Ratio": f"{result:.4f}"}

        formula = "P/E = (1 - b) × (1 + g) / (r - g)" if explain else None
        notes = "b = retention ratio = 1 - payout ratio"

        format_result("Justified P/E Ratio", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def peg(
    pe_ratio: float = typer.Option(..., "--pe", "-p", help="P/E ratio"),
    growth_rate: float = typer.Option(..., "--growth", "-g", help="Expected growth rate (as decimal)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate PEG (Price/Earnings to Growth) ratio."""
    try:
        result = calculate_peg_ratio(pe_ratio, growth_rate)

        inputs = {
            "P/E Ratio": f"{pe_ratio:.2f}",
            "Growth Rate": f"{growth_rate * 100:.2f}%",
        }

        results = {"PEG Ratio": f"{result:.4f}"}

        formula = "PEG = P/E / (g × 100)" if explain else None
        notes = "PEG < 1: potentially undervalued; PEG > 1: potentially overvalued"

        format_result("PEG Ratio", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)
