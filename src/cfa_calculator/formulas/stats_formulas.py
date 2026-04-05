"""Statistical formulas."""

import numpy as np
from scipy import stats
from typing import List, Tuple


def calculate_mean(data: List[float]) -> float:
    """
    Calculate arithmetic mean.

    Formula: Mean = Σx / n

    Args:
        data: List of values

    Returns:
        Mean
    """
    return float(np.mean(data))


def calculate_median(data: List[float]) -> float:
    """
    Calculate median.

    Args:
        data: List of values

    Returns:
        Median
    """
    return float(np.median(data))


def calculate_mode(data: List[float]) -> float:
    """
    Calculate mode (most frequent value).

    Args:
        data: List of values

    Returns:
        Mode
    """
    mode_result = stats.mode(data, keepdims=True)
    return float(mode_result.mode[0])


def calculate_variance(data: List[float], sample: bool = True) -> float:
    """
    Calculate variance.

    Formula (sample): s² = Σ(x - x̄)² / (n - 1)
    Formula (population): σ² = Σ(x - μ)² / n

    Args:
        data: List of values
        sample: True for sample variance (default), False for population variance

    Returns:
        Variance
    """
    ddof = 1 if sample else 0
    return float(np.var(data, ddof=ddof))


def calculate_std_dev(data: List[float], sample: bool = True) -> float:
    """
    Calculate standard deviation.

    Formula (sample): s = √[Σ(x - x̄)² / (n - 1)]
    Formula (population): σ = √[Σ(x - μ)² / n]

    Args:
        data: List of values
        sample: True for sample std dev (default), False for population std dev

    Returns:
        Standard deviation
    """
    ddof = 1 if sample else 0
    return float(np.std(data, ddof=ddof))


def calculate_covariance_stats(data1: List[float], data2: List[float]) -> float:
    """
    Calculate covariance between two datasets.

    Formula: Cov(X,Y) = Σ[(x - x̄)(y - ȳ)] / (n - 1)

    Args:
        data1: First dataset
        data2: Second dataset

    Returns:
        Covariance
    """
    return float(np.cov(data1, data2)[0, 1])


def calculate_correlation_stats(data1: List[float], data2: List[float]) -> float:
    """
    Calculate Pearson correlation coefficient.

    Formula: r = Cov(X,Y) / (σx × σy)

    Args:
        data1: First dataset
        data2: Second dataset

    Returns:
        Correlation coefficient (-1 to 1)
    """
    return float(np.corrcoef(data1, data2)[0, 1])


def calculate_skewness(data: List[float]) -> float:
    """
    Calculate skewness (measure of asymmetry).

    Positive skew: right tail is longer
    Negative skew: left tail is longer

    Args:
        data: List of values

    Returns:
        Skewness
    """
    return float(stats.skew(data))


def calculate_kurtosis(data: List[float], excess: bool = True) -> float:
    """
    Calculate kurtosis (measure of tail heaviness).

    Args:
        data: List of values
        excess: True for excess kurtosis (default), False for raw kurtosis

    Returns:
        Kurtosis
    """
    if excess:
        return float(stats.kurtosis(data, fisher=True))
    else:
        return float(stats.kurtosis(data, fisher=False))


def calculate_z_score(value: float, mean: float, std_dev: float) -> float:
    """
    Calculate z-score (standardized score).

    Formula: z = (x - μ) / σ

    Args:
        value: Value to standardize
        mean: Population/sample mean
        std_dev: Population/sample standard deviation

    Returns:
        Z-score
    """
    if std_dev == 0:
        raise ValueError("Standard deviation cannot be zero")
    return (value - mean) / std_dev


def calculate_confidence_interval(
    data: List[float],
    confidence_level: float = 0.95
) -> Tuple[float, float, float]:
    """
    Calculate confidence interval for the mean.

    Args:
        data: List of values
        confidence_level: Confidence level (default: 0.95 for 95%)

    Returns:
        Tuple of (mean, lower_bound, upper_bound)
    """
    n = len(data)
    mean = np.mean(data)
    std_err = stats.sem(data)

    # Use t-distribution for small samples
    confidence_interval = stats.t.interval(
        confidence_level,
        df=n-1,
        loc=mean,
        scale=std_err
    )

    return float(mean), float(confidence_interval[0]), float(confidence_interval[1])


def calculate_percentile(data: List[float], percentile: float) -> float:
    """
    Calculate percentile.

    Args:
        data: List of values
        percentile: Percentile to calculate (0-100)

    Returns:
        Value at the given percentile
    """
    if percentile < 0 or percentile > 100:
        raise ValueError("Percentile must be between 0 and 100")

    return float(np.percentile(data, percentile))


def calculate_range(data: List[float]) -> float:
    """
    Calculate range (max - min).

    Args:
        data: List of values

    Returns:
        Range
    """
    return float(np.max(data) - np.min(data))


def calculate_coefficient_of_variation(data: List[float]) -> float:
    """
    Calculate coefficient of variation (CV).

    Formula: CV = (σ / μ) × 100%

    Args:
        data: List of values

    Returns:
        Coefficient of variation (as percentage)
    """
    mean = np.mean(data)
    if mean == 0:
        raise ValueError("Mean cannot be zero for CV calculation")

    std_dev = np.std(data, ddof=1)
    return float((std_dev / mean) * 100)
