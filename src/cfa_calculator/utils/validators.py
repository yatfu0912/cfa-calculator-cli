"""Input validation utilities."""

from typing import Union, List


def validate_positive(value: float, name: str) -> None:
    """Validate that a value is positive."""
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")


def validate_non_negative(value: float, name: str) -> None:
    """Validate that a value is non-negative."""
    if value < 0:
        raise ValueError(f"{name} must be non-negative, got {value}")


def validate_rate(rate: float, name: str = "Rate") -> None:
    """Validate that a rate is reasonable (between -1 and 10)."""
    if rate < -1 or rate > 10:
        raise ValueError(f"{name} seems unreasonable: {rate}. Expected value between -1 and 10")


def validate_probability(prob: float, name: str = "Probability") -> None:
    """Validate that a probability is between 0 and 1."""
    if prob < 0 or prob > 1:
        raise ValueError(f"{name} must be between 0 and 1, got {prob}")


def validate_periods(n: int, name: str = "Number of periods") -> None:
    """Validate that number of periods is positive."""
    if n <= 0:
        raise ValueError(f"{name} must be positive, got {n}")


def validate_frequency(freq: int) -> None:
    """Validate compounding frequency."""
    valid_frequencies = [1, 2, 4, 12, 52, 365]
    if freq not in valid_frequencies:
        raise ValueError(
            f"Frequency must be one of {valid_frequencies} (annual, semi-annual, quarterly, monthly, weekly, daily), got {freq}"
        )


def validate_list_length(data: List[float], min_length: int, name: str = "Data") -> None:
    """Validate that a list has minimum required length."""
    if len(data) < min_length:
        raise ValueError(f"{name} must have at least {min_length} elements, got {len(data)}")


def validate_equal_length(list1: List[float], list2: List[float], name1: str, name2: str) -> None:
    """Validate that two lists have equal length."""
    if len(list1) != len(list2):
        raise ValueError(f"{name1} and {name2} must have equal length, got {len(list1)} and {len(list2)}")


def parse_percentage(value: Union[float, str]) -> float:
    """
    Parse a percentage value that might be given as decimal or percentage.

    Examples:
        0.05 -> 0.05
        5 -> 0.05
        "5%" -> 0.05
    """
    if isinstance(value, str):
        value = value.strip()
        if value.endswith('%'):
            return float(value[:-1]) / 100
        return float(value)

    # If value is greater than 1, assume it's a percentage
    if value > 1:
        return value / 100

    return value
