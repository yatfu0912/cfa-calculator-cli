"""Fixed Income (Bond) formulas."""

import numpy as np
from scipy.optimize import newton


def calculate_bond_price(
    face_value: float,
    coupon_rate: float,
    ytm: float,
    years: float,
    frequency: int = 2
) -> float:
    """
    Calculate bond price.

    Formula: Price = Σ[C/(1+y)^t] + FV/(1+y)^n
    Where C = coupon payment, y = YTM per period, n = total periods

    Args:
        face_value: Face/par value of the bond
        coupon_rate: Annual coupon rate (as decimal)
        ytm: Yield to maturity (annual, as decimal)
        years: Years to maturity
        frequency: Coupon payment frequency per year (default: 2 for semi-annual)

    Returns:
        Bond price
    """
    n_periods = int(years * frequency)
    coupon_payment = (face_value * coupon_rate) / frequency
    ytm_per_period = ytm / frequency

    if ytm_per_period == 0:
        return face_value + (coupon_payment * n_periods)

    # Present value of coupon payments
    pv_coupons = sum(
        coupon_payment / (1 + ytm_per_period) ** t
        for t in range(1, n_periods + 1)
    )

    # Present value of face value
    pv_face = face_value / (1 + ytm_per_period) ** n_periods

    return pv_coupons + pv_face


def calculate_ytm(
    price: float,
    face_value: float,
    coupon_rate: float,
    years: float,
    frequency: int = 2,
    initial_guess: float = 0.05
) -> float:
    """
    Calculate Yield to Maturity using numerical optimization.

    Args:
        price: Current bond price
        face_value: Face/par value of the bond
        coupon_rate: Annual coupon rate (as decimal)
        years: Years to maturity
        frequency: Coupon payment frequency per year
        initial_guess: Initial guess for YTM (default: 0.05)

    Returns:
        Yield to Maturity (annual)
    """
    def price_diff(ytm):
        calculated_price = calculate_bond_price(
            face_value, coupon_rate, ytm, years, frequency
        )
        return calculated_price - price

    try:
        ytm = newton(price_diff, initial_guess, maxiter=100)
        return ytm
    except RuntimeError:
        raise ValueError("YTM calculation did not converge. Try a different initial guess.")


def calculate_current_yield(
    price: float,
    face_value: float,
    coupon_rate: float
) -> float:
    """
    Calculate current yield.

    Formula: Current Yield = Annual Coupon Payment / Current Price

    Args:
        price: Current bond price
        face_value: Face value of the bond
        coupon_rate: Annual coupon rate (as decimal)

    Returns:
        Current yield
    """
    annual_coupon = face_value * coupon_rate
    return annual_coupon / price


def calculate_macaulay_duration(
    face_value: float,
    coupon_rate: float,
    ytm: float,
    years: float,
    frequency: int = 2
) -> float:
    """
    Calculate Macaulay Duration.

    Formula: Duration = Σ[t × PV(CFt)] / Price
    Where t = time period, CFt = cash flow at time t

    Args:
        face_value: Face value of the bond
        coupon_rate: Annual coupon rate (as decimal)
        ytm: Yield to maturity (annual, as decimal)
        years: Years to maturity
        frequency: Coupon payment frequency per year

    Returns:
        Macaulay Duration (in years)
    """
    n_periods = int(years * frequency)
    coupon_payment = (face_value * coupon_rate) / frequency
    ytm_per_period = ytm / frequency

    bond_price = calculate_bond_price(face_value, coupon_rate, ytm, years, frequency)

    # Calculate weighted present value of cash flows
    weighted_pv = 0
    for t in range(1, n_periods + 1):
        if t < n_periods:
            cash_flow = coupon_payment
        else:
            cash_flow = coupon_payment + face_value

        pv = cash_flow / (1 + ytm_per_period) ** t
        weighted_pv += (t / frequency) * pv  # Convert period to years

    return weighted_pv / bond_price


def calculate_modified_duration(
    face_value: float,
    coupon_rate: float,
    ytm: float,
    years: float,
    frequency: int = 2
) -> float:
    """
    Calculate Modified Duration.

    Formula: Modified Duration = Macaulay Duration / (1 + YTM/frequency)

    Args:
        face_value: Face value of the bond
        coupon_rate: Annual coupon rate (as decimal)
        ytm: Yield to maturity (annual, as decimal)
        years: Years to maturity
        frequency: Coupon payment frequency per year

    Returns:
        Modified Duration
    """
    macaulay_dur = calculate_macaulay_duration(
        face_value, coupon_rate, ytm, years, frequency
    )
    return macaulay_dur / (1 + ytm / frequency)


def calculate_convexity(
    face_value: float,
    coupon_rate: float,
    ytm: float,
    years: float,
    frequency: int = 2
) -> float:
    """
    Calculate Convexity.

    Formula: Convexity = Σ[t(t+1) × PV(CFt)] / [Price × (1+y)^2]

    Args:
        face_value: Face value of the bond
        coupon_rate: Annual coupon rate (as decimal)
        ytm: Yield to maturity (annual, as decimal)
        years: Years to maturity
        frequency: Coupon payment frequency per year

    Returns:
        Convexity
    """
    n_periods = int(years * frequency)
    coupon_payment = (face_value * coupon_rate) / frequency
    ytm_per_period = ytm / frequency

    bond_price = calculate_bond_price(face_value, coupon_rate, ytm, years, frequency)

    # Calculate weighted present value for convexity
    convexity_sum = 0
    for t in range(1, n_periods + 1):
        if t < n_periods:
            cash_flow = coupon_payment
        else:
            cash_flow = coupon_payment + face_value

        pv = cash_flow / (1 + ytm_per_period) ** t
        convexity_sum += t * (t + 1) * pv

    convexity = convexity_sum / (bond_price * (1 + ytm_per_period) ** 2)

    # Convert to annual convexity
    return convexity / (frequency ** 2)


def calculate_ytc(
    price: float,
    face_value: float,
    coupon_rate: float,
    years_to_call: float,
    call_price: float,
    frequency: int = 2,
    initial_guess: float = 0.05
) -> float:
    """
    Calculate Yield to Call.

    Args:
        price: Current bond price
        face_value: Face value of the bond
        coupon_rate: Annual coupon rate (as decimal)
        years_to_call: Years until call date
        call_price: Call price of the bond
        frequency: Coupon payment frequency per year
        initial_guess: Initial guess for YTC

    Returns:
        Yield to Call (annual)
    """
    n_periods = int(years_to_call * frequency)
    coupon_payment = (face_value * coupon_rate) / frequency

    def price_diff(ytc):
        ytc_per_period = ytc / frequency

        # Present value of coupon payments
        pv_coupons = sum(
            coupon_payment / (1 + ytc_per_period) ** t
            for t in range(1, n_periods + 1)
        )

        # Present value of call price
        pv_call = call_price / (1 + ytc_per_period) ** n_periods

        calculated_price = pv_coupons + pv_call
        return calculated_price - price

    try:
        ytc = newton(price_diff, initial_guess, maxiter=100)
        return ytc
    except RuntimeError:
        raise ValueError("YTC calculation did not converge. Try a different initial guess.")
