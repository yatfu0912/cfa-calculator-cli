"""Fixed Income (Bond) CLI commands."""

import typer
from cfa_calculator.formulas.bond_formulas import (
    calculate_bond_price,
    calculate_ytm,
    calculate_ytc,
    calculate_current_yield,
    calculate_macaulay_duration,
    calculate_modified_duration,
    calculate_convexity,
)
from cfa_calculator.utils.formatters import format_result, print_error
from cfa_calculator.utils.validators import (
    validate_positive,
    validate_frequency,
)

app = typer.Typer(help="Fixed Income (Bond) calculations")


@app.command()
def price(
    face_value: float = typer.Option(..., "--face", "-f", help="Face/par value of the bond"),
    coupon_rate: float = typer.Option(..., "--coupon-rate", "-c", help="Annual coupon rate (as decimal)"),
    ytm: float = typer.Option(..., "--ytm", "-y", help="Yield to maturity (annual, as decimal)"),
    years: float = typer.Option(..., "--years", "-n", help="Years to maturity"),
    frequency: int = typer.Option(2, "--freq", help="Coupon payment frequency per year (default: 2 for semi-annual)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate bond price."""
    try:
        validate_positive(face_value, "Face value")
        validate_positive(years, "Years to maturity")
        validate_frequency(frequency)

        result = calculate_bond_price(face_value, coupon_rate, ytm, years, frequency)

        inputs = {
            "Face Value": face_value,
            "Coupon Rate": f"{coupon_rate * 100:.2f}%",
            "Yield to Maturity (YTM)": f"{ytm * 100:.2f}%",
            "Years to Maturity": years,
            "Payment Frequency": f"{frequency}x per year",
        }

        results = {"Bond Price": result}

        formula = "Price = Σ[C/(1+y)^t] + FV/(1+y)^n" if explain else None
        notes = "Price > Face Value: Premium bond; Price < Face Value: Discount bond"

        format_result("Bond Price Calculation", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def ytm(
    price: float = typer.Option(..., "--price", "-p", help="Current bond price"),
    face_value: float = typer.Option(..., "--face", "-f", help="Face/par value of the bond"),
    coupon_rate: float = typer.Option(..., "--coupon-rate", "-c", help="Annual coupon rate (as decimal)"),
    years: float = typer.Option(..., "--years", "-n", help="Years to maturity"),
    frequency: int = typer.Option(2, "--freq", help="Coupon payment frequency per year"),
    initial_guess: float = typer.Option(0.05, "--guess", help="Initial guess for YTM"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate Yield to Maturity (YTM)."""
    try:
        validate_positive(price, "Bond price")
        validate_positive(face_value, "Face value")
        validate_positive(years, "Years to maturity")
        validate_frequency(frequency)

        result = calculate_ytm(price, face_value, coupon_rate, years, frequency, initial_guess)

        inputs = {
            "Current Price": price,
            "Face Value": face_value,
            "Coupon Rate": f"{coupon_rate * 100:.2f}%",
            "Years to Maturity": years,
            "Payment Frequency": f"{frequency}x per year",
        }

        results = {"Yield to Maturity (YTM)": f"{result * 100:.4f}%"}

        formula = "Solve for y: Price = Σ[C/(1+y)^t] + FV/(1+y)^n" if explain else None
        notes = "YTM is the internal rate of return if held to maturity"

        format_result("Yield to Maturity", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def ytc(
    price: float = typer.Option(..., "--price", "-p", help="Current bond price"),
    face_value: float = typer.Option(..., "--face", "-f", help="Face value of the bond"),
    coupon_rate: float = typer.Option(..., "--coupon-rate", "-c", help="Annual coupon rate (as decimal)"),
    years_to_call: float = typer.Option(..., "--years-to-call", help="Years until call date"),
    call_price: float = typer.Option(..., "--call-price", help="Call price of the bond"),
    frequency: int = typer.Option(2, "--freq", help="Coupon payment frequency per year"),
    initial_guess: float = typer.Option(0.05, "--guess", help="Initial guess for YTC"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate Yield to Call (YTC)."""
    try:
        validate_positive(price, "Bond price")
        validate_positive(face_value, "Face value")
        validate_positive(years_to_call, "Years to call")
        validate_positive(call_price, "Call price")
        validate_frequency(frequency)

        result = calculate_ytc(price, face_value, coupon_rate, years_to_call, call_price, frequency, initial_guess)

        inputs = {
            "Current Price": price,
            "Face Value": face_value,
            "Coupon Rate": f"{coupon_rate * 100:.2f}%",
            "Years to Call": years_to_call,
            "Call Price": call_price,
            "Payment Frequency": f"{frequency}x per year",
        }

        results = {"Yield to Call (YTC)": f"{result * 100:.4f}%"}

        formula = "Solve for y: Price = Σ[C/(1+y)^t] + CallPrice/(1+y)^n" if explain else None
        notes = "YTC assumes the bond is called at the earliest call date"

        format_result("Yield to Call", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def current_yield(
    price: float = typer.Option(..., "--price", "-p", help="Current bond price"),
    face_value: float = typer.Option(..., "--face", "-f", help="Face value of the bond"),
    coupon_rate: float = typer.Option(..., "--coupon-rate", "-c", help="Annual coupon rate (as decimal)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate current yield."""
    try:
        validate_positive(price, "Bond price")
        validate_positive(face_value, "Face value")

        result = calculate_current_yield(price, face_value, coupon_rate)

        inputs = {
            "Current Price": price,
            "Face Value": face_value,
            "Coupon Rate": f"{coupon_rate * 100:.2f}%",
        }

        results = {"Current Yield": f"{result * 100:.4f}%"}

        formula = "Current Yield = Annual Coupon Payment / Current Price" if explain else None
        notes = "Current yield does not account for capital gains/losses"

        format_result("Current Yield", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def duration(
    face_value: float = typer.Option(..., "--face", "-f", help="Face value of the bond"),
    coupon_rate: float = typer.Option(..., "--coupon-rate", "-c", help="Annual coupon rate (as decimal)"),
    ytm: float = typer.Option(..., "--ytm", "-y", help="Yield to maturity (annual, as decimal)"),
    years: float = typer.Option(..., "--years", "-n", help="Years to maturity"),
    frequency: int = typer.Option(2, "--freq", help="Coupon payment frequency per year"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate Macaulay and Modified Duration."""
    try:
        validate_positive(face_value, "Face value")
        validate_positive(years, "Years to maturity")
        validate_frequency(frequency)

        macaulay_dur = calculate_macaulay_duration(face_value, coupon_rate, ytm, years, frequency)
        modified_dur = calculate_modified_duration(face_value, coupon_rate, ytm, years, frequency)

        inputs = {
            "Face Value": face_value,
            "Coupon Rate": f"{coupon_rate * 100:.2f}%",
            "Yield to Maturity": f"{ytm * 100:.2f}%",
            "Years to Maturity": years,
            "Payment Frequency": f"{frequency}x per year",
        }

        results = {
            "Macaulay Duration": f"{macaulay_dur:.4f} years",
            "Modified Duration": f"{modified_dur:.4f}",
        }

        formula = "ModDur = MacDur / (1 + YTM/freq)" if explain else None
        notes = "Modified Duration measures price sensitivity to yield changes"

        format_result("Duration Calculation", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def convexity(
    face_value: float = typer.Option(..., "--face", "-f", help="Face value of the bond"),
    coupon_rate: float = typer.Option(..., "--coupon-rate", "-c", help="Annual coupon rate (as decimal)"),
    ytm: float = typer.Option(..., "--ytm", "-y", help="Yield to maturity (annual, as decimal)"),
    years: float = typer.Option(..., "--years", "-n", help="Years to maturity"),
    frequency: int = typer.Option(2, "--freq", help="Coupon payment frequency per year"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate Convexity."""
    try:
        validate_positive(face_value, "Face value")
        validate_positive(years, "Years to maturity")
        validate_frequency(frequency)

        result = calculate_convexity(face_value, coupon_rate, ytm, years, frequency)

        inputs = {
            "Face Value": face_value,
            "Coupon Rate": f"{coupon_rate * 100:.2f}%",
            "Yield to Maturity": f"{ytm * 100:.2f}%",
            "Years to Maturity": years,
            "Payment Frequency": f"{frequency}x per year",
        }

        results = {"Convexity": f"{result:.4f}"}

        formula = "Convexity = Σ[t(t+1) × PV(CFt)] / [Price × (1+y)^2]" if explain else None
        notes = "Convexity measures the curvature of the price-yield relationship"

        format_result("Convexity Calculation", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)
