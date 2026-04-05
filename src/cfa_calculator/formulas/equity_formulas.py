"""Equity Valuation formulas for CFA Calculator."""

from typing import List


def calculate_gordon_growth_model(
    dividend: float,
    required_return: float,
    growth_rate: float
) -> float:
    """
    Calculate stock value using Gordon Growth Model (Constant Growth DDM).

    Formula: V0 = D1 / (r - g)

    Args:
        dividend: Expected dividend next year (D1)
        required_return: Required rate of return (r)
        growth_rate: Constant growth rate (g)

    Returns:
        Stock value

    Raises:
        ValueError: If required_return <= growth_rate
    """
    if required_return <= growth_rate:
        raise ValueError("Required return must be greater than growth rate")

    return dividend / (required_return - growth_rate)


def calculate_multistage_ddm(
    current_dividend: float,
    high_growth_rate: float,
    high_growth_years: int,
    stable_growth_rate: float,
    required_return: float
) -> float:
    """
    Calculate stock value using Two-Stage DDM.

    Stage 1: High growth period
    Stage 2: Stable growth period (Gordon Growth Model)

    Args:
        current_dividend: Current dividend (D0)
        high_growth_rate: Growth rate during high growth period
        high_growth_years: Number of years of high growth
        stable_growth_rate: Growth rate after high growth period
        required_return: Required rate of return

    Returns:
        Stock value

    Raises:
        ValueError: If required_return <= stable_growth_rate
    """
    if required_return <= stable_growth_rate:
        raise ValueError("Required return must be greater than stable growth rate")

    if high_growth_years < 1:
        raise ValueError("High growth years must be at least 1")

    # Stage 1: PV of dividends during high growth period
    pv_stage1 = 0.0
    for t in range(1, high_growth_years + 1):
        dividend_t = current_dividend * ((1 + high_growth_rate) ** t)
        pv_stage1 += dividend_t / ((1 + required_return) ** t)

    # Stage 2: PV of terminal value (Gordon Growth Model)
    dividend_at_end = current_dividend * ((1 + high_growth_rate) ** high_growth_years)
    dividend_stable = dividend_at_end * (1 + stable_growth_rate)
    terminal_value = dividend_stable / (required_return - stable_growth_rate)
    pv_stage2 = terminal_value / ((1 + required_return) ** high_growth_years)

    return pv_stage1 + pv_stage2


def calculate_fcfe_valuation(
    fcfe: float,
    required_return: float,
    growth_rate: float
) -> float:
    """
    Calculate equity value using Free Cash Flow to Equity (FCFE) model.

    Formula: V0 = FCFE1 / (r - g)

    Args:
        fcfe: Expected FCFE next year
        required_return: Required rate of return on equity
        growth_rate: Constant growth rate

    Returns:
        Equity value

    Raises:
        ValueError: If required_return <= growth_rate
    """
    if required_return <= growth_rate:
        raise ValueError("Required return must be greater than growth rate")

    return fcfe / (required_return - growth_rate)


def calculate_pe_valuation(
    earnings_per_share: float,
    benchmark_pe: float
) -> float:
    """
    Calculate stock value using P/E ratio valuation.

    Formula: V0 = EPS × P/E

    Args:
        earnings_per_share: Expected earnings per share
        benchmark_pe: Benchmark P/E ratio (industry average or comparable company)

    Returns:
        Stock value

    Raises:
        ValueError: If inputs are negative
    """
    if earnings_per_share < 0:
        raise ValueError("EPS cannot be negative for P/E valuation")
    if benchmark_pe < 0:
        raise ValueError("P/E ratio cannot be negative")

    return earnings_per_share * benchmark_pe


def calculate_justified_pe_ratio(
    dividend_payout_ratio: float,
    required_return: float,
    growth_rate: float
) -> float:
    """
    Calculate justified P/E ratio using Gordon Growth Model.

    Formula: P/E = (1 - b) × (1 + g) / (r - g)
    where b = retention ratio = 1 - payout ratio

    Args:
        dividend_payout_ratio: Dividend payout ratio (0 to 1)
        required_return: Required rate of return
        growth_rate: Growth rate

    Returns:
        Justified P/E ratio

    Raises:
        ValueError: If required_return <= growth_rate or invalid payout ratio
    """
    if required_return <= growth_rate:
        raise ValueError("Required return must be greater than growth rate")
    if not 0 <= dividend_payout_ratio <= 1:
        raise ValueError("Dividend payout ratio must be between 0 and 1")

    return dividend_payout_ratio * (1 + growth_rate) / (required_return - growth_rate)


def calculate_peg_ratio(
    pe_ratio: float,
    growth_rate: float
) -> float:
    """
    Calculate PEG (Price/Earnings to Growth) ratio.

    Formula: PEG = P/E / (g × 100)

    Args:
        pe_ratio: P/E ratio
        growth_rate: Expected growth rate (as decimal, e.g., 0.15 for 15%)

    Returns:
        PEG ratio

    Raises:
        ValueError: If growth_rate is zero or negative
    """
    if growth_rate <= 0:
        raise ValueError("Growth rate must be positive")

    return pe_ratio / (growth_rate * 100)
