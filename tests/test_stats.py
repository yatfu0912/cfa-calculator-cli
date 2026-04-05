"""Tests for Statistical formulas."""

import pytest
import numpy as np
from cfa_calculator.formulas.stats_formulas import (
    calculate_mean,
    calculate_median,
    calculate_mode,
    calculate_variance,
    calculate_std_dev,
    calculate_covariance_stats,
    calculate_correlation_stats,
    calculate_skewness,
    calculate_kurtosis,
    calculate_z_score,
    calculate_confidence_interval,
    calculate_percentile,
    calculate_range,
    calculate_coefficient_of_variation,
)


class TestMean:
    def test_mean_basic(self):
        """Test basic mean calculation."""
        data = [1, 2, 3, 4, 5]
        result = calculate_mean(data)
        assert result == 3.0

    def test_mean_decimals(self):
        """Test mean with decimal values."""
        data = [1.5, 2.5, 3.5]
        result = calculate_mean(data)
        assert abs(result - 2.5) < 0.0001


class TestMedian:
    def test_median_odd(self):
        """Test median with odd number of values."""
        data = [1, 3, 5, 7, 9]
        result = calculate_median(data)
        assert result == 5.0

    def test_median_even(self):
        """Test median with even number of values."""
        data = [1, 2, 3, 4]
        result = calculate_median(data)
        assert result == 2.5


class TestVarianceStdDev:
    def test_sample_variance(self):
        """Test sample variance calculation."""
        data = [2, 4, 6, 8, 10]
        result = calculate_variance(data, sample=True)
        assert result > 0

    def test_population_variance(self):
        """Test population variance calculation."""
        data = [2, 4, 6, 8, 10]
        sample_var = calculate_variance(data, sample=True)
        pop_var = calculate_variance(data, sample=False)
        # Population variance should be smaller
        assert pop_var < sample_var

    def test_std_dev_relationship(self):
        """Test that std dev is square root of variance."""
        data = [1, 2, 3, 4, 5]
        variance = calculate_variance(data, sample=True)
        std_dev = calculate_std_dev(data, sample=True)
        assert abs(std_dev ** 2 - variance) < 0.0001


class TestCovarianceCorrelation:
    def test_covariance_positive(self):
        """Test covariance with positively correlated data."""
        data1 = [1, 2, 3, 4, 5]
        data2 = [2, 4, 6, 8, 10]
        result = calculate_covariance_stats(data1, data2)
        assert result > 0

    def test_correlation_perfect(self):
        """Test perfect positive correlation."""
        data1 = [1, 2, 3, 4, 5]
        data2 = [2, 4, 6, 8, 10]
        result = calculate_correlation_stats(data1, data2)
        assert abs(result - 1.0) < 0.0001

    def test_correlation_range(self):
        """Test that correlation is between -1 and 1."""
        data1 = [1, 2, 3, 4, 5]
        data2 = [5, 3, 4, 2, 1]
        result = calculate_correlation_stats(data1, data2)
        assert -1 <= result <= 1


class TestSkewness:
    def test_skewness_symmetric(self):
        """Test skewness of symmetric distribution."""
        data = [1, 2, 3, 4, 5]
        result = calculate_skewness(data)
        assert abs(result) < 0.1

    def test_skewness_right(self):
        """Test right-skewed distribution."""
        data = [1, 1, 1, 2, 2, 3, 10]
        result = calculate_skewness(data)
        assert result > 0


class TestKurtosis:
    def test_kurtosis_excess(self):
        """Test excess kurtosis calculation."""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = calculate_kurtosis(data, excess=True)
        # Uniform distribution has negative excess kurtosis
        assert result < 0

    def test_kurtosis_raw(self):
        """Test raw kurtosis calculation."""
        data = [1, 2, 3, 4, 5]
        excess = calculate_kurtosis(data, excess=True)
        raw = calculate_kurtosis(data, excess=False)
        assert abs(raw - excess - 3.0) < 0.01


class TestZScore:
    def test_z_score_basic(self):
        """Test basic z-score calculation."""
        result = calculate_z_score(value=110, mean=100, std_dev=10)
        assert result == 1.0

    def test_z_score_negative(self):
        """Test negative z-score."""
        result = calculate_z_score(value=90, mean=100, std_dev=10)
        assert result == -1.0

    def test_z_score_zero_std(self):
        """Test z-score with zero std dev raises error."""
        with pytest.raises(ValueError, match="Standard deviation cannot be zero"):
            calculate_z_score(100, 100, 0)


class TestConfidenceInterval:
    def test_confidence_interval_95(self):
        """Test 95% confidence interval."""
        data = [10, 12, 14, 16, 18, 20]
        mean, lower, upper = calculate_confidence_interval(data, 0.95)

        # Mean should be in the middle
        assert lower < mean < upper

        # Interval should be reasonable
        assert upper - lower > 0

    def test_confidence_interval_contains_mean(self):
        """Test that confidence interval contains the mean."""
        data = [5, 10, 15, 20, 25]
        mean, lower, upper = calculate_confidence_interval(data, 0.95)
        assert lower <= mean <= upper


class TestPercentile:
    def test_percentile_50(self):
        """Test 50th percentile (median)."""
        data = [1, 2, 3, 4, 5]
        result = calculate_percentile(data, 50)
        assert result == 3.0

    def test_percentile_25(self):
        """Test 25th percentile."""
        data = [1, 2, 3, 4, 5, 6, 7, 8]
        result = calculate_percentile(data, 25)
        assert result <= 3

    def test_percentile_invalid(self):
        """Test invalid percentile raises error."""
        data = [1, 2, 3]
        with pytest.raises(ValueError, match="Percentile must be between 0 and 100"):
            calculate_percentile(data, 150)


class TestRange:
    def test_range_basic(self):
        """Test range calculation."""
        data = [1, 5, 10]
        result = calculate_range(data)
        assert result == 9.0


class TestCoefficientOfVariation:
    def test_cv_basic(self):
        """Test coefficient of variation."""
        data = [10, 20, 30, 40, 50]
        result = calculate_coefficient_of_variation(data)
        assert result > 0

    def test_cv_zero_mean(self):
        """Test CV with zero mean raises error."""
        data = [-5, 0, 5]
        with pytest.raises(ValueError, match="Mean cannot be zero"):
            calculate_coefficient_of_variation(data)
