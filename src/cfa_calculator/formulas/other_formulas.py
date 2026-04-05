"""Other financial calculation formulas (NPV, IRR, etc.)."""

import numpy as np
from scipy.optimize import newton
from typing import List


def calculate_npv(rate: float, cash_flows: List[float]) -> float:
    """
    Calculate Net Present Value.

    Formula: NPV = Σ[CFt / (1 + r)^t]

    Args:
        rate: Discount rate (as decimal)
        cash_flows: List of cash flows (CF0, CF1, CF2, ...)
                   First cash flow is typically the initial investment (negative)

    Returns:
        Net Present Value
    """
    npv = 0
    for t, cf in enumerate(cash_flows):
        npv += cf / (1 + rate) ** t
    return npv


def calculate_irr(cash_flows: List[float], initial_guess: float = 0.1) -> float:
    """
    Calculate Internal Rate of Return.

    IRR is the discount rate that makes NPV = 0

    Args:
        cash_flows: List of cash flows (CF0, CF1, CF2, ...)
        initial_guess: Initial guess for IRR (default: 0.1)

    Returns:
        Internal Rate of Return
    """
    if len(cash_flows) < 2:
        raise ValueError("Need at least 2 cash flows for IRR calculation")

    # Check if there's a sign change (required for IRR)
    signs = [1 if cf >= 0 else -1 for cf in cash_flows]
    if len(set(signs)) == 1:
        raise ValueError("Cash flows must have at least one sign change for IRR")

    def npv_func(rate):
        return calculate_npv(rate, cash_flows)

    try:
        irr = newton(npv_func, initial_guess, maxiter=100)
        return irr
    except RuntimeError:
        raise ValueError("IRR calculation did not converge. Try a different initial guess.")


def calculate_money_weighted_return(
    beginning_value: float,
    ending_value: float,
    cash_flows: List[float],
    times: List[float]
) -> float:
    """
    Calculate Money-Weighted Return (similar to IRR).

    Args:
        beginning_value: Portfolio value at start
        ending_value: Portfolio value at end
        cash_flows: List of cash flows (positive for contributions, negative for withdrawals)
        times: List of times (as fraction of period, e.g., 0.25 for quarter)

    Returns:
        Money-weighted return
    """
    if len(cash_flows) != len(times):
        raise ValueError("Cash flows and times must have same length")

    # Build full cash flow list
    full_cf = [-beginning_value]  # Initial investment (negative)

    # Add intermediate cash flows
    for cf in cash_flows:
        full_cf.append(cf)

    full_cf.append(ending_value)  # Final value (positive)

    return calculate_irr(full_cf)


def calculate_time_weighted_return(
    beginning_values: List[float],
    ending_values: List[float]
) -> float:
    """
    Calculate Time-Weighted Return.

    Formula: TWR = [(1 + R1) × (1 + R2) × ... × (1 + Rn)] - 1

    Args:
        beginning_values: Beginning values for each sub-period
        ending_values: Ending values for each sub-period

    Returns:
        Time-weighted return
    """
    if len(beginning_values) != len(ending_values):
        raise ValueError("Beginning and ending values must have same length")

    if len(beginning_values) == 0:
        raise ValueError("Need at least one period")

    twr = 1.0
    for bv, ev in zip(beginning_values, ending_values):
        if bv == 0:
            raise ValueError("Beginning value cannot be zero")
        period_return = (ev - bv) / bv
        twr *= (1 + period_return)

    return twr - 1


def calculate_payback_period(
    initial_investment: float,
    cash_flows: List[float]
) -> float:
    """
    Calculate Payback Period.

    Args:
        initial_investment: Initial investment (positive value)
        cash_flows: List of annual cash flows

    Returns:
        Payback period in years
    """
    if initial_investment <= 0:
        raise ValueError("Initial investment must be positive")

    cumulative = 0
    for year, cf in enumerate(cash_flows):
        cumulative += cf
        if cumulative >= initial_investment:
            # Interpolate within the year
            previous_cumulative = cumulative - cf
            fraction = (initial_investment - previous_cumulative) / cf
            return year + fraction

    raise ValueError("Investment not recovered within the given cash flows")


def calculate_profitability_index(
    rate: float,
    initial_investment: float,
    cash_flows: List[float]
) -> float:
    """
    Calculate Profitability Index.

    Formula: PI = PV(future cash flows) / Initial Investment

    Args:
        rate: Discount rate (as decimal)
        initial_investment: Initial investment (positive value)
        cash_flows: List of future cash flows (excluding initial investment)

    Returns:
        Profitability Index
    """
    if initial_investment <= 0:
        raise ValueError("Initial investment must be positive")

    # Calculate PV of future cash flows
    pv_future = 0
    for t, cf in enumerate(cash_flows, start=1):
        pv_future += cf / (1 + rate) ** t

    return pv_future / initial_investment


def calculate_mirr(
    cash_flows: List[float],
    finance_rate: float,
    reinvest_rate: float
) -> float:
    """
    Calculate Modified Internal Rate of Return.

    Args:
        cash_flows: List of cash flows (CF0, CF1, CF2, ...)
        finance_rate: Rate for financing negative cash flows
        reinvest_rate: Rate for reinvesting positive cash flows

    Returns:
        Modified IRR
    """
    n = len(cash_flows) - 1

    # Present value of negative cash flows
    pv_negative = 0
    for t, cf in enumerate(cash_flows):
        if cf < 0:
            pv_negative += cf / (1 + finance_rate) ** t

    # Future value of positive cash flows
    fv_positive = 0
    for t, cf in enumerate(cash_flows):
        if cf > 0:
            fv_positive += cf * (1 + reinvest_rate) ** (n - t)

    if pv_negative == 0:
        raise ValueError("Need at least one negative cash flow")

    # MIRR formula
    mirr = (fv_positive / abs(pv_negative)) ** (1 / n) - 1
    return mirr
