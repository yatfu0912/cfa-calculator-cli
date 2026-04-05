"""Time Value of Money formulas."""

from typing import Literal


def calculate_fv(pv: float, rate: float, n: int, freq: int = 1) -> float:
    """
    Calculate Future Value.

    Formula: FV = PV × (1 + r/freq)^(n×freq)

    Args:
        pv: Present Value
        rate: Annual interest rate (as decimal, e.g., 0.05 for 5%)
        n: Number of years
        freq: Compounding frequency per year (default: 1 for annual)

    Returns:
        Future Value
    """
    return pv * (1 + rate / freq) ** (n * freq)


def calculate_pv(fv: float, rate: float, n: int, freq: int = 1) -> float:
    """
    Calculate Present Value.

    Formula: PV = FV / (1 + r/freq)^(n×freq)

    Args:
        fv: Future Value
        rate: Annual interest rate (as decimal)
        n: Number of years
        freq: Compounding frequency per year (default: 1)

    Returns:
        Present Value
    """
    return fv / (1 + rate / freq) ** (n * freq)


def calculate_annuity_fv(pmt: float, rate: float, n: int, annuity_type: Literal["ordinary", "due"] = "ordinary") -> float:
    """
    Calculate Future Value of an Annuity.

    Ordinary Annuity: FV = PMT × [(1 + r)^n - 1] / r
    Annuity Due: FV = PMT × [(1 + r)^n - 1] / r × (1 + r)

    Args:
        pmt: Payment amount per period
        rate: Interest rate per period (as decimal)
        n: Number of periods
        annuity_type: "ordinary" (payments at end) or "due" (payments at beginning)

    Returns:
        Future Value of Annuity
    """
    if rate == 0:
        return pmt * n

    fv_ordinary = pmt * (((1 + rate) ** n - 1) / rate)

    if annuity_type == "due":
        return fv_ordinary * (1 + rate)

    return fv_ordinary


def calculate_annuity_pv(pmt: float, rate: float, n: int, annuity_type: Literal["ordinary", "due"] = "ordinary") -> float:
    """
    Calculate Present Value of an Annuity.

    Ordinary Annuity: PV = PMT × [1 - (1 + r)^(-n)] / r
    Annuity Due: PV = PMT × [1 - (1 + r)^(-n)] / r × (1 + r)

    Args:
        pmt: Payment amount per period
        rate: Interest rate per period (as decimal)
        n: Number of periods
        annuity_type: "ordinary" or "due"

    Returns:
        Present Value of Annuity
    """
    if rate == 0:
        return pmt * n

    pv_ordinary = pmt * ((1 - (1 + rate) ** (-n)) / rate)

    if annuity_type == "due":
        return pv_ordinary * (1 + rate)

    return pv_ordinary


def calculate_perpetuity(pmt: float, rate: float) -> float:
    """
    Calculate Present Value of a Perpetuity.

    Formula: PV = PMT / r

    Args:
        pmt: Payment amount per period
        rate: Interest rate per period (as decimal)

    Returns:
        Present Value of Perpetuity
    """
    if rate == 0:
        raise ValueError("Rate cannot be zero for perpetuity calculation")

    return pmt / rate


def calculate_growing_perpetuity(pmt: float, rate: float, growth_rate: float) -> float:
    """
    Calculate Present Value of a Growing Perpetuity.

    Formula: PV = PMT / (r - g)

    Args:
        pmt: Initial payment amount
        rate: Discount rate (as decimal)
        growth_rate: Growth rate of payments (as decimal)

    Returns:
        Present Value of Growing Perpetuity
    """
    if rate <= growth_rate:
        raise ValueError("Discount rate must be greater than growth rate")

    return pmt / (rate - growth_rate)


def calculate_ear(stated_rate: float, freq: int) -> float:
    """
    Calculate Effective Annual Rate.

    Formula: EAR = (1 + stated_rate/freq)^freq - 1

    Args:
        stated_rate: Stated annual rate (as decimal)
        freq: Compounding frequency per year

    Returns:
        Effective Annual Rate
    """
    return (1 + stated_rate / freq) ** freq - 1
