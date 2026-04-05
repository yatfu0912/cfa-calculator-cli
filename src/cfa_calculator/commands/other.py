"""Other financial calculations CLI commands."""

import typer
from cfa_calculator.formulas.other_formulas import (
    calculate_npv,
    calculate_irr,
    calculate_money_weighted_return,
    calculate_time_weighted_return,
    calculate_payback_period,
    calculate_profitability_index,
    calculate_mirr,
)
from cfa_calculator.utils.formatters import format_result, print_error
from cfa_calculator.utils.validators import validate_positive

app = typer.Typer(help="Other financial calculations (NPV, IRR, etc.)")


@app.command()
def npv(
    rate: float = typer.Option(..., "--rate", "-r", help="Discount rate (as decimal)"),
    cash_flows: str = typer.Option(..., "--cash-flows", "-cf", help="Cash flows as comma-separated (CF0, CF1, CF2, ...)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate Net Present Value (NPV)."""
    try:
        cf_list = [float(x.strip()) for x in cash_flows.split(",")]

        if len(cf_list) < 2:
            raise ValueError("Need at least 2 cash flows")

        result = calculate_npv(rate, cf_list)

        inputs = {
            "Discount Rate": f"{rate * 100:.2f}%",
            "Number of Cash Flows": len(cf_list),
            "Initial Investment (CF0)": cf_list[0],
        }

        results = {"Net Present Value (NPV)": result}

        formula = "NPV = Σ[CFt / (1 + r)^t]" if explain else None
        notes = "NPV > 0: Accept project; NPV < 0: Reject project"

        format_result("Net Present Value", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def irr(
    cash_flows: str = typer.Option(..., "--cash-flows", "-cf", help="Cash flows as comma-separated (CF0, CF1, CF2, ...)"),
    initial_guess: float = typer.Option(0.1, "--guess", help="Initial guess for IRR"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate Internal Rate of Return (IRR)."""
    try:
        cf_list = [float(x.strip()) for x in cash_flows.split(",")]

        result = calculate_irr(cf_list, initial_guess)

        inputs = {
            "Number of Cash Flows": len(cf_list),
            "Initial Investment (CF0)": cf_list[0],
        }

        results = {"Internal Rate of Return (IRR)": f"{result * 100:.4f}%"}

        formula = "IRR is the rate where NPV = 0" if explain else None
        notes = "IRR > required return: Accept project; IRR < required return: Reject project"

        format_result("Internal Rate of Return", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def money_weighted(
    beginning_value: float = typer.Option(..., "--beginning", "-b", help="Portfolio value at start"),
    ending_value: float = typer.Option(..., "--ending", "-e", help="Portfolio value at end"),
    cash_flows: str = typer.Option("", "--cash-flows", "-cf", help="Cash flows as comma-separated (optional)"),
    times: str = typer.Option("", "--times", "-t", help="Times as comma-separated fractions (optional)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate Money-Weighted Return."""
    try:
        validate_positive(beginning_value, "Beginning value")
        validate_positive(ending_value, "Ending value")

        if cash_flows and times:
            cf_list = [float(x.strip()) for x in cash_flows.split(",")]
            time_list = [float(x.strip()) for x in times.split(",")]
            result = calculate_money_weighted_return(beginning_value, ending_value, cf_list, time_list)
        else:
            # Simple case: no intermediate cash flows
            result = (ending_value - beginning_value) / beginning_value

        inputs = {
            "Beginning Value": beginning_value,
            "Ending Value": ending_value,
            "Cash Flows": len(cash_flows.split(",")) if cash_flows else 0,
        }

        results = {"Money-Weighted Return": f"{result * 100:.4f}%"}

        formula = "Similar to IRR; accounts for timing and size of cash flows" if explain else None

        format_result("Money-Weighted Return", inputs, results, formula)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def time_weighted(
    beginning_values: str = typer.Option(..., "--beginning", "-b", help="Beginning values for each period (comma-separated)"),
    ending_values: str = typer.Option(..., "--ending", "-e", help="Ending values for each period (comma-separated)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate Time-Weighted Return."""
    try:
        bv_list = [float(x.strip()) for x in beginning_values.split(",")]
        ev_list = [float(x.strip()) for x in ending_values.split(",")]

        result = calculate_time_weighted_return(bv_list, ev_list)

        inputs = {
            "Number of Periods": len(bv_list),
        }

        results = {"Time-Weighted Return": f"{result * 100:.4f}%"}

        formula = "TWR = [(1 + R1) × (1 + R2) × ... × (1 + Rn)] - 1" if explain else None
        notes = "TWR eliminates the effect of cash flow timing; better for comparing managers"

        format_result("Time-Weighted Return", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def payback(
    initial_investment: float = typer.Option(..., "--investment", "-i", help="Initial investment"),
    cash_flows: str = typer.Option(..., "--cash-flows", "-cf", help="Annual cash flows as comma-separated"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate Payback Period."""
    try:
        validate_positive(initial_investment, "Initial investment")
        cf_list = [float(x.strip()) for x in cash_flows.split(",")]

        result = calculate_payback_period(initial_investment, cf_list)

        inputs = {
            "Initial Investment": initial_investment,
            "Number of Years": len(cf_list),
        }

        results = {"Payback Period": f"{result:.2f} years"}

        formula = "Time until cumulative cash flows = initial investment" if explain else None
        notes = "Shorter payback period is better; ignores time value of money"

        format_result("Payback Period", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def profitability_index(
    rate: float = typer.Option(..., "--rate", "-r", help="Discount rate (as decimal)"),
    initial_investment: float = typer.Option(..., "--investment", "-i", help="Initial investment"),
    cash_flows: str = typer.Option(..., "--cash-flows", "-cf", help="Future cash flows as comma-separated"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate Profitability Index."""
    try:
        validate_positive(initial_investment, "Initial investment")
        cf_list = [float(x.strip()) for x in cash_flows.split(",")]

        result = calculate_profitability_index(rate, initial_investment, cf_list)

        inputs = {
            "Discount Rate": f"{rate * 100:.2f}%",
            "Initial Investment": initial_investment,
            "Number of Cash Flows": len(cf_list),
        }

        results = {"Profitability Index": f"{result:.4f}"}

        formula = "PI = PV(future cash flows) / Initial Investment" if explain else None
        notes = "PI > 1: Accept project; PI < 1: Reject project"

        format_result("Profitability Index", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def mirr(
    cash_flows: str = typer.Option(..., "--cash-flows", "-cf", help="Cash flows as comma-separated"),
    finance_rate: float = typer.Option(..., "--finance-rate", "-f", help="Financing rate for negative cash flows"),
    reinvest_rate: float = typer.Option(..., "--reinvest-rate", "-r", help="Reinvestment rate for positive cash flows"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate Modified Internal Rate of Return (MIRR)."""
    try:
        cf_list = [float(x.strip()) for x in cash_flows.split(",")]

        result = calculate_mirr(cf_list, finance_rate, reinvest_rate)

        inputs = {
            "Number of Cash Flows": len(cf_list),
            "Finance Rate": f"{finance_rate * 100:.2f}%",
            "Reinvestment Rate": f"{reinvest_rate * 100:.2f}%",
        }

        results = {"Modified IRR (MIRR)": f"{result * 100:.4f}%"}

        formula = "MIRR = (FV of positive CFs / PV of negative CFs)^(1/n) - 1" if explain else None
        notes = "MIRR addresses IRR's reinvestment rate assumption"

        format_result("Modified Internal Rate of Return", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)
