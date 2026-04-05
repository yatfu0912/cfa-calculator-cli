"""Time Value of Money CLI commands."""

import typer
from typing import Optional, Literal
from cfa_calculator.formulas.tvm_formulas import (
    calculate_fv,
    calculate_pv,
    calculate_annuity_fv,
    calculate_annuity_pv,
    calculate_perpetuity,
    calculate_growing_perpetuity,
    calculate_ear,
)
from cfa_calculator.utils.formatters import format_result, print_error
from cfa_calculator.utils.validators import (
    validate_positive,
    validate_periods,
    validate_frequency,
)

app = typer.Typer(help="Time Value of Money calculations")


@app.command()
def fv(
    pv: float = typer.Option(..., "--pv", help="Present Value"),
    rate: float = typer.Option(..., "--rate", "-r", help="Annual interest rate (as decimal, e.g., 0.05 for 5%)"),
    n: str = typer.Option(..., "--n", "-n", help="Number of years (supports fractions like 1/12 for 1 month)"),
    freq: int = typer.Option(1, "--freq", "-f", help="Compounding frequency per year (1=annual, 2=semi-annual, 4=quarterly, 12=monthly)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate Future Value.

    Examples:
      cfa tvm fv --pv 1000 --rate 0.05 --n 10
      cfa tvm fv --pv 100000 --rate 0.07 --n 1/12 --freq 12
    """
    try:
        validate_positive(pv, "Present Value")

        # Parse n to support fractions
        if '/' in n:
            parts = n.split('/')
            n_value = float(parts[0]) / float(parts[1])
        else:
            n_value = float(n)

        validate_periods(n_value, "Number of years")
        validate_frequency(freq)

        result = calculate_fv(pv, rate, n_value, freq)

        inputs = {
            "Present Value (PV)": pv,
            "Interest Rate (r)": f"{rate * 100:.2f}%",
            "Number of Years (n)": n_value if '/' not in n else f"{n_value:.4f} ({n})",
            "Compounding Frequency": freq,
        }

        results = {"Future Value (FV)": result}

        formula = "FV = PV × (1 + r/freq)^(n×freq)" if explain else None

        format_result("Future Value Calculation", inputs, results, formula)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def pv(
    fv: float = typer.Option(..., "--fv", help="Future Value"),
    rate: float = typer.Option(..., "--rate", "-r", help="Annual interest rate (as decimal)"),
    n: str = typer.Option(..., "--n", "-n", help="Number of years (supports fractions like 1/12 for 1 month)"),
    freq: int = typer.Option(1, "--freq", "-f", help="Compounding frequency per year"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate Present Value.

    Examples:
      cfa tvm pv --fv 15000 --rate 0.06 --n 10
      cfa tvm pv --fv 10000 --rate 0.05 --n 6/12 --freq 12
    """
    try:
        validate_positive(fv, "Future Value")

        # Parse n to support fractions
        if '/' in n:
            parts = n.split('/')
            n_value = float(parts[0]) / float(parts[1])
        else:
            n_value = float(n)

        validate_periods(n_value, "Number of years")
        validate_frequency(freq)

        result = calculate_pv(fv, rate, n_value, freq)

        inputs = {
            "Future Value (FV)": fv,
            "Interest Rate (r)": f"{rate * 100:.2f}%",
            "Number of Years (n)": n_value if '/' not in n else f"{n_value:.4f} ({n})",
            "Compounding Frequency": freq,
        }

        results = {"Present Value (PV)": result}

        formula = "PV = FV / (1 + r/freq)^(n×freq)" if explain else None

        format_result("Present Value Calculation", inputs, results, formula)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def annuity(
    pmt: float = typer.Option(..., "--pmt", help="Payment amount per period"),
    rate: float = typer.Option(..., "--rate", "-r", help="Interest rate per period (as decimal)"),
    n: int = typer.Option(..., "--n", "-n", help="Number of periods"),
    calc_type: Literal["fv", "pv"] = typer.Option("pv", "--type", help="Calculate FV or PV"),
    annuity_type: Literal["ordinary", "due"] = typer.Option("ordinary", "--annuity-type", help="Ordinary (end) or Due (beginning)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate Future Value or Present Value of an Annuity."""
    try:
        validate_positive(abs(pmt), "Payment amount")
        validate_periods(n, "Number of periods")

        if calc_type == "fv":
            result = calculate_annuity_fv(pmt, rate, n, annuity_type)
            result_label = "Future Value (FV)"
            title = "Annuity Future Value"
            formula_text = "FV = PMT × [(1 + r)^n - 1] / r"
            if annuity_type == "due":
                formula_text += " × (1 + r)"
        else:
            result = calculate_annuity_pv(pmt, rate, n, annuity_type)
            result_label = "Present Value (PV)"
            title = "Annuity Present Value"
            formula_text = "PV = PMT × [1 - (1 + r)^(-n)] / r"
            if annuity_type == "due":
                formula_text += " × (1 + r)"

        inputs = {
            "Payment (PMT)": pmt,
            "Interest Rate (r)": f"{rate * 100:.2f}%",
            "Number of Periods (n)": n,
            "Annuity Type": annuity_type.capitalize(),
        }

        results = {result_label: result}

        formula = formula_text if explain else None

        format_result(title, inputs, results, formula)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def perpetuity(
    pmt: float = typer.Option(..., "--pmt", help="Payment amount per period"),
    rate: float = typer.Option(..., "--rate", "-r", help="Interest rate per period (as decimal)"),
    growth_rate: Optional[float] = typer.Option(None, "--growth", "-g", help="Growth rate (for growing perpetuity)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate Present Value of a Perpetuity."""
    try:
        validate_positive(pmt, "Payment amount")
        validate_positive(rate, "Interest rate")

        if growth_rate is not None:
            result = calculate_growing_perpetuity(pmt, rate, growth_rate)
            title = "Growing Perpetuity"
            formula_text = "PV = PMT / (r - g)"
            inputs = {
                "Payment (PMT)": pmt,
                "Discount Rate (r)": f"{rate * 100:.2f}%",
                "Growth Rate (g)": f"{growth_rate * 100:.2f}%",
            }
        else:
            result = calculate_perpetuity(pmt, rate)
            title = "Perpetuity"
            formula_text = "PV = PMT / r"
            inputs = {
                "Payment (PMT)": pmt,
                "Interest Rate (r)": f"{rate * 100:.2f}%",
            }

        results = {"Present Value (PV)": result}

        formula = formula_text if explain else None

        format_result(title, inputs, results, formula)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def ear(
    stated_rate: float = typer.Option(..., "--stated-rate", help="Stated annual rate (as decimal)"),
    freq: int = typer.Option(..., "--freq", "-f", help="Compounding frequency per year"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate Effective Annual Rate."""
    try:
        validate_positive(stated_rate, "Stated rate")
        validate_frequency(freq)

        result = calculate_ear(stated_rate, freq)

        inputs = {
            "Stated Annual Rate": f"{stated_rate * 100:.2f}%",
            "Compounding Frequency": freq,
        }

        results = {"Effective Annual Rate (EAR)": f"{result * 100:.4f}%"}

        formula = "EAR = (1 + stated_rate/freq)^freq - 1" if explain else None

        format_result("Effective Annual Rate", inputs, results, formula)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)
