"""Derivatives and Option pricing formulas for CFA Calculator."""

import math
from typing import Literal
from scipy.stats import norm


def calculate_option_payoff(
    option_type: Literal["call", "put"],
    spot_price: float,
    strike_price: float,
    premium: float = 0.0
) -> float:
    """
    Calculate option payoff at expiration.

    Args:
        option_type: "call" or "put"
        spot_price: Stock price at expiration
        strike_price: Strike price
        premium: Option premium paid (optional, for profit calculation)

    Returns:
        Option payoff (or profit if premium provided)
    """
    if option_type == "call":
        intrinsic_value = max(spot_price - strike_price, 0)
    elif option_type == "put":
        intrinsic_value = max(strike_price - spot_price, 0)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    return intrinsic_value - premium


def calculate_put_call_parity(
    call_price: float = None,
    put_price: float = None,
    spot_price: float = None,
    strike_price: float = None,
    risk_free_rate: float = None,
    time_to_expiry: float = None
) -> dict:
    """
    Calculate missing value using Put-Call Parity.

    Formula: C + PV(K) = P + S
    or: C + K×e^(-r×T) = P + S

    Args:
        call_price: Call option price
        put_price: Put option price
        spot_price: Current stock price
        strike_price: Strike price
        risk_free_rate: Risk-free rate (as decimal)
        time_to_expiry: Time to expiration (in years)

    Returns:
        Dictionary with all values including the calculated one

    Raises:
        ValueError: If not exactly one value is missing
    """
    values = {
        "call_price": call_price,
        "put_price": put_price,
        "spot_price": spot_price,
        "strike_price": strike_price,
        "risk_free_rate": risk_free_rate,
        "time_to_expiry": time_to_expiry
    }

    none_count = sum(1 for v in values.values() if v is None)
    if none_count != 1:
        raise ValueError("Exactly one value must be None to solve for it")

    # Calculate PV of strike price
    if strike_price is not None and risk_free_rate is not None and time_to_expiry is not None:
        pv_strike = strike_price * math.exp(-risk_free_rate * time_to_expiry)
    else:
        pv_strike = None

    # Solve for missing value
    if call_price is None:
        values["call_price"] = put_price + spot_price - pv_strike
    elif put_price is None:
        values["put_price"] = call_price + pv_strike - spot_price
    elif spot_price is None:
        values["spot_price"] = call_price + pv_strike - put_price
    elif strike_price is None:
        # K = (C - P + S) / e^(-r×T)
        values["strike_price"] = (call_price - put_price + spot_price) / math.exp(-risk_free_rate * time_to_expiry)
    elif risk_free_rate is None:
        # Solve for r: e^(-r×T) = (C - P + S) / K
        # -r×T = ln((C - P + S) / K)
        # r = -ln((C - P + S) / K) / T
        values["risk_free_rate"] = -math.log((call_price - put_price + spot_price) / strike_price) / time_to_expiry
    elif time_to_expiry is None:
        # Solve for T: e^(-r×T) = (C - P + S) / K
        # T = -ln((C - P + S) / K) / r
        values["time_to_expiry"] = -math.log((call_price - put_price + spot_price) / strike_price) / risk_free_rate

    return values


def calculate_black_scholes(
    option_type: Literal["call", "put"],
    spot_price: float,
    strike_price: float,
    time_to_expiry: float,
    risk_free_rate: float,
    volatility: float,
    dividend_yield: float = 0.0
) -> dict:
    """
    Calculate option price using Black-Scholes-Merton model.

    Args:
        option_type: "call" or "put"
        spot_price: Current stock price
        strike_price: Strike price
        time_to_expiry: Time to expiration (in years)
        risk_free_rate: Risk-free rate (as decimal)
        volatility: Volatility (as decimal, e.g., 0.25 for 25%)
        dividend_yield: Continuous dividend yield (as decimal, default 0)

    Returns:
        Dictionary with option_price, delta, gamma, vega, theta, rho

    Raises:
        ValueError: If inputs are invalid
    """
    if spot_price <= 0:
        raise ValueError("Spot price must be positive")
    if strike_price <= 0:
        raise ValueError("Strike price must be positive")
    if time_to_expiry <= 0:
        raise ValueError("Time to expiry must be positive")
    if volatility <= 0:
        raise ValueError("Volatility must be positive")

    # Calculate d1 and d2
    d1 = (math.log(spot_price / strike_price) +
          (risk_free_rate - dividend_yield + 0.5 * volatility ** 2) * time_to_expiry) / \
         (volatility * math.sqrt(time_to_expiry))

    d2 = d1 - volatility * math.sqrt(time_to_expiry)

    # Calculate option price
    if option_type == "call":
        option_price = (spot_price * math.exp(-dividend_yield * time_to_expiry) * norm.cdf(d1) -
                       strike_price * math.exp(-risk_free_rate * time_to_expiry) * norm.cdf(d2))
        delta = math.exp(-dividend_yield * time_to_expiry) * norm.cdf(d1)
        theta = (-(spot_price * norm.pdf(d1) * volatility * math.exp(-dividend_yield * time_to_expiry)) /
                (2 * math.sqrt(time_to_expiry)) -
                risk_free_rate * strike_price * math.exp(-risk_free_rate * time_to_expiry) * norm.cdf(d2) +
                dividend_yield * spot_price * math.exp(-dividend_yield * time_to_expiry) * norm.cdf(d1))
        rho = strike_price * time_to_expiry * math.exp(-risk_free_rate * time_to_expiry) * norm.cdf(d2)
    elif option_type == "put":
        option_price = (strike_price * math.exp(-risk_free_rate * time_to_expiry) * norm.cdf(-d2) -
                       spot_price * math.exp(-dividend_yield * time_to_expiry) * norm.cdf(-d1))
        delta = -math.exp(-dividend_yield * time_to_expiry) * norm.cdf(-d1)
        theta = (-(spot_price * norm.pdf(d1) * volatility * math.exp(-dividend_yield * time_to_expiry)) /
                (2 * math.sqrt(time_to_expiry)) +
                risk_free_rate * strike_price * math.exp(-risk_free_rate * time_to_expiry) * norm.cdf(-d2) -
                dividend_yield * spot_price * math.exp(-dividend_yield * time_to_expiry) * norm.cdf(-d1))
        rho = -strike_price * time_to_expiry * math.exp(-risk_free_rate * time_to_expiry) * norm.cdf(-d2)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    # Calculate Greeks (same for call and put)
    gamma = (norm.pdf(d1) * math.exp(-dividend_yield * time_to_expiry)) / \
            (spot_price * volatility * math.sqrt(time_to_expiry))

    vega = spot_price * math.exp(-dividend_yield * time_to_expiry) * norm.pdf(d1) * math.sqrt(time_to_expiry)

    return {
        "option_price": option_price,
        "delta": delta,
        "gamma": gamma,
        "vega": vega / 100,  # Vega per 1% change in volatility
        "theta": theta / 365,  # Theta per day
        "rho": rho / 100,  # Rho per 1% change in interest rate
        "d1": d1,
        "d2": d2
    }


def calculate_binomial_option(
    option_type: Literal["call", "put"],
    spot_price: float,
    strike_price: float,
    time_to_expiry: float,
    risk_free_rate: float,
    volatility: float,
    steps: int = 100,
    american: bool = False
) -> float:
    """
    Calculate option price using Binomial Tree model.

    Args:
        option_type: "call" or "put"
        spot_price: Current stock price
        strike_price: Strike price
        time_to_expiry: Time to expiration (in years)
        risk_free_rate: Risk-free rate (as decimal)
        volatility: Volatility (as decimal)
        steps: Number of time steps in the tree (default 100)
        american: True for American option, False for European (default False)

    Returns:
        Option price

    Raises:
        ValueError: If inputs are invalid
    """
    if spot_price <= 0:
        raise ValueError("Spot price must be positive")
    if strike_price <= 0:
        raise ValueError("Strike price must be positive")
    if time_to_expiry <= 0:
        raise ValueError("Time to expiry must be positive")
    if volatility <= 0:
        raise ValueError("Volatility must be positive")
    if steps < 1:
        raise ValueError("Steps must be at least 1")

    dt = time_to_expiry / steps
    u = math.exp(volatility * math.sqrt(dt))  # Up factor
    d = 1 / u  # Down factor
    p = (math.exp(risk_free_rate * dt) - d) / (u - d)  # Risk-neutral probability
    discount = math.exp(-risk_free_rate * dt)

    # Initialize asset prices at maturity
    asset_prices = [spot_price * (u ** (steps - i)) * (d ** i) for i in range(steps + 1)]

    # Initialize option values at maturity
    if option_type == "call":
        option_values = [max(price - strike_price, 0) for price in asset_prices]
    elif option_type == "put":
        option_values = [max(strike_price - price, 0) for price in asset_prices]
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    # Backward induction
    for step in range(steps - 1, -1, -1):
        for i in range(step + 1):
            # Calculate option value from next period
            option_values[i] = discount * (p * option_values[i] + (1 - p) * option_values[i + 1])

            # For American options, check early exercise
            if american:
                asset_price = spot_price * (u ** (step - i)) * (d ** i)
                if option_type == "call":
                    exercise_value = max(asset_price - strike_price, 0)
                else:  # put
                    exercise_value = max(strike_price - asset_price, 0)
                option_values[i] = max(option_values[i], exercise_value)

    return option_values[0]
