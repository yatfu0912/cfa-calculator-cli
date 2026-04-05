"""Portfolio Management formulas."""

import numpy as np
from typing import List


def calculate_portfolio_return(weights: List[float], returns: List[float]) -> float:
    """
    Calculate expected portfolio return.

    Formula: E(Rp) = Σ(wi × E(Ri))

    Args:
        weights: List of asset weights (must sum to 1)
        returns: List of expected returns for each asset

    Returns:
        Expected portfolio return
    """
    if len(weights) != len(returns):
        raise ValueError("Weights and returns must have same length")

    if abs(sum(weights) - 1.0) > 0.0001:
        raise ValueError(f"Weights must sum to 1, got {sum(weights)}")

    return sum(w * r for w, r in zip(weights, returns))


def calculate_portfolio_variance(
    weights: List[float],
    variances: List[float],
    covariances: List[List[float]] = None
) -> float:
    """
    Calculate portfolio variance.

    For 2 assets: σp² = w1²σ1² + w2²σ2² + 2w1w2Cov(1,2)
    For n assets: Uses covariance matrix

    Args:
        weights: List of asset weights
        variances: List of asset variances
        covariances: Covariance matrix (optional, for 2+ assets)

    Returns:
        Portfolio variance
    """
    n = len(weights)

    if n == 2 and covariances is None:
        raise ValueError("Covariance required for 2-asset portfolio")

    if covariances is not None:
        # Use full covariance matrix
        w = np.array(weights)
        cov_matrix = np.array(covariances)
        return float(w @ cov_matrix @ w.T)
    else:
        # Single asset or no correlation
        return sum(w**2 * v for w, v in zip(weights, variances))


def calculate_portfolio_std(
    weights: List[float],
    variances: List[float],
    covariances: List[List[float]] = None
) -> float:
    """
    Calculate portfolio standard deviation.

    Args:
        weights: List of asset weights
        variances: List of asset variances
        covariances: Covariance matrix (optional)

    Returns:
        Portfolio standard deviation
    """
    variance = calculate_portfolio_variance(weights, variances, covariances)
    return np.sqrt(variance)


def calculate_sharpe_ratio(
    portfolio_return: float,
    risk_free_rate: float,
    portfolio_std: float
) -> float:
    """
    Calculate Sharpe Ratio.

    Formula: Sharpe = (Rp - Rf) / σp

    Args:
        portfolio_return: Expected portfolio return
        risk_free_rate: Risk-free rate
        portfolio_std: Portfolio standard deviation

    Returns:
        Sharpe Ratio
    """
    if portfolio_std == 0:
        raise ValueError("Portfolio standard deviation cannot be zero")

    return (portfolio_return - risk_free_rate) / portfolio_std


def calculate_treynor_ratio(
    portfolio_return: float,
    risk_free_rate: float,
    beta: float
) -> float:
    """
    Calculate Treynor Ratio.

    Formula: Treynor = (Rp - Rf) / βp

    Args:
        portfolio_return: Expected portfolio return
        risk_free_rate: Risk-free rate
        beta: Portfolio beta

    Returns:
        Treynor Ratio
    """
    if beta == 0:
        raise ValueError("Beta cannot be zero")

    return (portfolio_return - risk_free_rate) / beta


def calculate_jensens_alpha(
    portfolio_return: float,
    risk_free_rate: float,
    beta: float,
    market_return: float
) -> float:
    """
    Calculate Jensen's Alpha.

    Formula: α = Rp - [Rf + βp(Rm - Rf)]

    Args:
        portfolio_return: Actual portfolio return
        risk_free_rate: Risk-free rate
        beta: Portfolio beta
        market_return: Market return

    Returns:
        Jensen's Alpha
    """
    expected_return = risk_free_rate + beta * (market_return - risk_free_rate)
    return portfolio_return - expected_return


def calculate_sortino_ratio(
    portfolio_return: float,
    risk_free_rate: float,
    downside_deviation: float
) -> float:
    """
    Calculate Sortino Ratio.

    Formula: Sortino = (Rp - Rf) / σd

    Args:
        portfolio_return: Expected portfolio return
        risk_free_rate: Risk-free rate or target return
        downside_deviation: Downside deviation (std of negative returns)

    Returns:
        Sortino Ratio
    """
    if downside_deviation == 0:
        raise ValueError("Downside deviation cannot be zero")

    return (portfolio_return - risk_free_rate) / downside_deviation


def calculate_beta(
    asset_returns: List[float],
    market_returns: List[float]
) -> float:
    """
    Calculate Beta.

    Formula: β = Cov(Ra, Rm) / Var(Rm)

    Args:
        asset_returns: List of asset returns
        market_returns: List of market returns

    Returns:
        Beta
    """
    if len(asset_returns) != len(market_returns):
        raise ValueError("Asset and market returns must have same length")

    if len(asset_returns) < 2:
        raise ValueError("Need at least 2 observations")

    asset_arr = np.array(asset_returns)
    market_arr = np.array(market_returns)

    covariance = np.cov(asset_arr, market_arr)[0, 1]
    market_variance = np.var(market_arr, ddof=1)

    if market_variance == 0:
        raise ValueError("Market variance cannot be zero")

    return covariance / market_variance


def calculate_capm(
    risk_free_rate: float,
    beta: float,
    market_return: float
) -> float:
    """
    Calculate required return using CAPM.

    Formula: E(Ri) = Rf + βi[E(Rm) - Rf]

    Args:
        risk_free_rate: Risk-free rate
        beta: Asset beta
        market_return: Expected market return

    Returns:
        Required return
    """
    return risk_free_rate + beta * (market_return - risk_free_rate)


def calculate_covariance(returns1: List[float], returns2: List[float]) -> float:
    """
    Calculate covariance between two assets.

    Args:
        returns1: Returns for asset 1
        returns2: Returns for asset 2

    Returns:
        Covariance
    """
    if len(returns1) != len(returns2):
        raise ValueError("Return series must have same length")

    return float(np.cov(returns1, returns2)[0, 1])


def calculate_correlation(returns1: List[float], returns2: List[float]) -> float:
    """
    Calculate correlation between two assets.

    Args:
        returns1: Returns for asset 1
        returns2: Returns for asset 2

    Returns:
        Correlation coefficient
    """
    if len(returns1) != len(returns2):
        raise ValueError("Return series must have same length")

    return float(np.corrcoef(returns1, returns2)[0, 1])
