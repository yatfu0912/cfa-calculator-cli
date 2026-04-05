"""Derivatives and Option pricing CLI commands."""

import typer
from typing import Optional
from cfa_calculator.formulas.option_formulas import (
    calculate_option_payoff,
    calculate_put_call_parity,
    calculate_black_scholes,
    calculate_binomial_option,
)
from cfa_calculator.utils.formatters import format_result, print_error
from cfa_calculator.utils.validators import validate_positive

app = typer.Typer(help="Derivatives and Option pricing calculations")


@app.command()
def payoff(
    option_type: str = typer.Option(..., "--type", "-t", help="Option type: 'call' or 'put'"),
    spot_price: float = typer.Option(..., "--spot", "-s", help="Stock price at expiration"),
    strike_price: float = typer.Option(..., "--strike", "-k", help="Strike price"),
    premium: float = typer.Option(0.0, "--premium", "-p", help="Option premium paid (optional)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate option payoff at expiration."""
    try:
        validate_positive(spot_price, "Spot price")
        validate_positive(strike_price, "Strike price")

        result = calculate_option_payoff(option_type.lower(), spot_price, strike_price, premium)

        inputs = {
            "Option Type": option_type.capitalize(),
            "Spot Price at Expiration": f"${spot_price:.2f}",
            "Strike Price": f"${strike_price:.2f}",
            "Premium Paid": f"${premium:.2f}" if premium > 0 else "N/A",
        }

        if premium > 0:
            results = {"Profit/Loss": f"${result:.2f}"}
            notes = "Profit = Intrinsic Value - Premium"
        else:
            results = {"Payoff": f"${result:.2f}"}
            notes = "Payoff = Intrinsic Value at expiration"

        formula = None
        if explain:
            if option_type.lower() == "call":
                formula = "Call Payoff = max(S - K, 0)"
            else:
                formula = "Put Payoff = max(K - S, 0)"

        format_result("Option Payoff", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def put_call_parity(
    call_price: Optional[float] = typer.Option(None, "--call", "-c", help="Call option price"),
    put_price: Optional[float] = typer.Option(None, "--put", "-p", help="Put option price"),
    spot_price: Optional[float] = typer.Option(None, "--spot", "-s", help="Current stock price"),
    strike_price: Optional[float] = typer.Option(None, "--strike", "-k", help="Strike price"),
    risk_free_rate: Optional[float] = typer.Option(None, "--rf", "-r", help="Risk-free rate (as decimal)"),
    time_to_expiry: Optional[float] = typer.Option(None, "--time", "-t", help="Time to expiration (in years)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate missing value using Put-Call Parity."""
    try:
        result = calculate_put_call_parity(
            call_price, put_price, spot_price, strike_price, risk_free_rate, time_to_expiry
        )

        # Find which value was calculated
        inputs = {}
        calculated_value = None
        calculated_name = None

        if call_price is None:
            calculated_value = result["call_price"]
            calculated_name = "Call Price"
        else:
            inputs["Call Price"] = f"${call_price:.2f}"

        if put_price is None:
            calculated_value = result["put_price"]
            calculated_name = "Put Price"
        else:
            inputs["Put Price"] = f"${put_price:.2f}"

        if spot_price is None:
            calculated_value = result["spot_price"]
            calculated_name = "Spot Price"
        else:
            inputs["Spot Price"] = f"${spot_price:.2f}"

        if strike_price is None:
            calculated_value = result["strike_price"]
            calculated_name = "Strike Price"
        else:
            inputs["Strike Price"] = f"${strike_price:.2f}"

        if risk_free_rate is None:
            calculated_value = result["risk_free_rate"]
            calculated_name = "Risk-Free Rate"
        else:
            inputs["Risk-Free Rate"] = f"{risk_free_rate * 100:.2f}%"

        if time_to_expiry is None:
            calculated_value = result["time_to_expiry"]
            calculated_name = "Time to Expiry"
        else:
            inputs["Time to Expiry"] = f"{time_to_expiry:.4f} years"

        # Format result
        if calculated_name in ["Call Price", "Put Price", "Spot Price", "Strike Price"]:
            results = {calculated_name: f"${calculated_value:.2f}"}
        elif calculated_name == "Risk-Free Rate":
            results = {calculated_name: f"{calculated_value * 100:.4f}%"}
        else:
            results = {calculated_name: f"{calculated_value:.4f} years"}

        formula = "C + PV(K) = P + S  or  C + K×e^(-r×T) = P + S" if explain else None
        notes = "Put-Call Parity: relationship between European call and put options"

        format_result("Put-Call Parity", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def black_scholes(
    option_type: str = typer.Option(..., "--type", "-t", help="Option type: 'call' or 'put'"),
    spot_price: float = typer.Option(..., "--spot", "-s", help="Current stock price"),
    strike_price: float = typer.Option(..., "--strike", "-k", help="Strike price"),
    time_to_expiry: float = typer.Option(..., "--time", "-T", help="Time to expiration (in years)"),
    risk_free_rate: float = typer.Option(..., "--rf", "-r", help="Risk-free rate (as decimal)"),
    volatility: float = typer.Option(..., "--vol", "-v", help="Volatility (as decimal, e.g., 0.25 for 25%)"),
    dividend_yield: float = typer.Option(0.0, "--div", "-q", help="Continuous dividend yield (as decimal)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate option price using Black-Scholes-Merton model."""
    try:
        validate_positive(spot_price, "Spot price")
        validate_positive(strike_price, "Strike price")
        validate_positive(time_to_expiry, "Time to expiry")
        validate_positive(volatility, "Volatility")

        result = calculate_black_scholes(
            option_type.lower(),
            spot_price,
            strike_price,
            time_to_expiry,
            risk_free_rate,
            volatility,
            dividend_yield
        )

        inputs = {
            "Option Type": option_type.capitalize(),
            "Spot Price (S)": f"${spot_price:.2f}",
            "Strike Price (K)": f"${strike_price:.2f}",
            "Time to Expiry (T)": f"{time_to_expiry:.4f} years",
            "Risk-Free Rate (r)": f"{risk_free_rate * 100:.2f}%",
            "Volatility (σ)": f"{volatility * 100:.2f}%",
            "Dividend Yield (q)": f"{dividend_yield * 100:.2f}%" if dividend_yield > 0 else "0%",
        }

        results = {
            "Option Price": f"${result['option_price']:.4f}",
            "Delta (Δ)": f"{result['delta']:.4f}",
            "Gamma (Γ)": f"{result['gamma']:.6f}",
            "Vega (ν)": f"{result['vega']:.4f} (per 1% vol change)",
            "Theta (Θ)": f"{result['theta']:.4f} (per day)",
            "Rho (ρ)": f"{result['rho']:.4f} (per 1% rate change)",
        }

        formula = None
        if explain:
            formula = "Black-Scholes: C = S×e^(-q×T)×N(d1) - K×e^(-r×T)×N(d2)\n"
            formula += f"d1 = {result['d1']:.4f}, d2 = {result['d2']:.4f}"

        notes = "Greeks measure option price sensitivity to various factors"

        format_result("Black-Scholes Option Pricing", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def binomial(
    option_type: str = typer.Option(..., "--type", "-t", help="Option type: 'call' or 'put'"),
    spot_price: float = typer.Option(..., "--spot", "-s", help="Current stock price"),
    strike_price: float = typer.Option(..., "--strike", "-k", help="Strike price"),
    time_to_expiry: float = typer.Option(..., "--time", "-T", help="Time to expiration (in years)"),
    risk_free_rate: float = typer.Option(..., "--rf", "-r", help="Risk-free rate (as decimal)"),
    volatility: float = typer.Option(..., "--vol", "-v", help="Volatility (as decimal)"),
    steps: int = typer.Option(100, "--steps", "-n", help="Number of time steps"),
    american: bool = typer.Option(False, "--american", help="American option (default: European)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate option price using Binomial Tree model."""
    try:
        validate_positive(spot_price, "Spot price")
        validate_positive(strike_price, "Strike price")
        validate_positive(time_to_expiry, "Time to expiry")
        validate_positive(volatility, "Volatility")

        result = calculate_binomial_option(
            option_type.lower(),
            spot_price,
            strike_price,
            time_to_expiry,
            risk_free_rate,
            volatility,
            steps,
            american
        )

        inputs = {
            "Option Type": option_type.capitalize(),
            "Exercise Style": "American" if american else "European",
            "Spot Price (S)": f"${spot_price:.2f}",
            "Strike Price (K)": f"${strike_price:.2f}",
            "Time to Expiry (T)": f"{time_to_expiry:.4f} years",
            "Risk-Free Rate (r)": f"{risk_free_rate * 100:.2f}%",
            "Volatility (σ)": f"{volatility * 100:.2f}%",
            "Time Steps": steps,
        }

        results = {"Option Price": f"${result:.4f}"}

        formula = None
        if explain:
            formula = "Binomial Tree: u = e^(σ√Δt), d = 1/u, p = (e^(rΔt) - d)/(u - d)\n"
            formula += "Backward induction from terminal nodes"

        notes = "Binomial model can price American options with early exercise"

        format_result("Binomial Option Pricing", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)
