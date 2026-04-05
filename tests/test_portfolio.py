"""Tests for Portfolio Management formulas."""

import pytest
import numpy as np
from cfa_calculator.formulas.portfolio_formulas import (
    calculate_portfolio_return,
    calculate_sharpe_ratio,
    calculate_treynor_ratio,
    calculate_jensens_alpha,
    calculate_sortino_ratio,
    calculate_beta,
    calculate_capm,
    calculate_covariance,
    calculate_correlation,
)


class TestPortfolioReturn:
    def test_portfolio_return_two_assets(self):
        """Test portfolio return with two assets."""
        weights = [0.6, 0.4]
        returns = [0.10, 0.15]
        result = calculate_portfolio_return(weights, returns)
        assert abs(result - 0.12) < 0.0001

    def test_portfolio_return_weights_not_sum_to_one(self):
        """Test that weights must sum to 1."""
        weights = [0.5, 0.4]
        returns = [0.10, 0.15]
        with pytest.raises(ValueError, match="Weights must sum to 1"):
            calculate_portfolio_return(weights, returns)

    def test_portfolio_return_mismatched_lengths(self):
        """Test that weights and returns must have same length."""
        weights = [0.6, 0.4]
        returns = [0.10]
        with pytest.raises(ValueError, match="same length"):
            calculate_portfolio_return(weights, returns)


class TestSharpeRatio:
    def test_sharpe_ratio_basic(self):
        """Test basic Sharpe ratio calculation."""
        result = calculate_sharpe_ratio(
            portfolio_return=0.12,
            risk_free_rate=0.03,
            portfolio_std=0.15
        )
        assert abs(result - 0.60) < 0.01

    def test_sharpe_ratio_zero_std(self):
        """Test Sharpe ratio with zero std raises error."""
        with pytest.raises(ValueError, match="standard deviation cannot be zero"):
            calculate_sharpe_ratio(0.12, 0.03, 0)


class TestTreynorRatio:
    def test_treynor_ratio_basic(self):
        """Test basic Treynor ratio calculation."""
        result = calculate_treynor_ratio(
            portfolio_return=0.15,
            risk_free_rate=0.03,
            beta=1.2
        )
        assert abs(result - 0.10) < 0.01

    def test_treynor_ratio_zero_beta(self):
        """Test Treynor ratio with zero beta raises error."""
        with pytest.raises(ValueError, match="Beta cannot be zero"):
            calculate_treynor_ratio(0.15, 0.03, 0)


class TestJensensAlpha:
    def test_jensens_alpha_positive(self):
        """Test Jensen's alpha with outperformance."""
        result = calculate_jensens_alpha(
            portfolio_return=0.15,
            risk_free_rate=0.03,
            beta=1.2,
            market_return=0.11
        )
        # Expected return = 0.03 + 1.2 * (0.11 - 0.03) = 0.126
        # Alpha = 0.15 - 0.126 = 0.024
        assert abs(result - 0.024) < 0.001

    def test_jensens_alpha_negative(self):
        """Test Jensen's alpha with underperformance."""
        result = calculate_jensens_alpha(
            portfolio_return=0.10,
            risk_free_rate=0.03,
            beta=1.0,
            market_return=0.12
        )
        # Expected return = 0.03 + 1.0 * (0.12 - 0.03) = 0.12
        # Alpha = 0.10 - 0.12 = -0.02
        assert abs(result - (-0.02)) < 0.001


class TestSortinoRatio:
    def test_sortino_ratio_basic(self):
        """Test basic Sortino ratio calculation."""
        result = calculate_sortino_ratio(
            portfolio_return=0.12,
            risk_free_rate=0.03,
            downside_deviation=0.10
        )
        assert abs(result - 0.90) < 0.01

    def test_sortino_ratio_zero_downside(self):
        """Test Sortino ratio with zero downside deviation raises error."""
        with pytest.raises(ValueError, match="Downside deviation cannot be zero"):
            calculate_sortino_ratio(0.12, 0.03, 0)


class TestBeta:
    def test_beta_basic(self):
        """Test basic beta calculation."""
        asset_returns = [0.10, 0.15, 0.12, 0.08, 0.14]
        market_returns = [0.08, 0.12, 0.10, 0.06, 0.11]
        result = calculate_beta(asset_returns, market_returns)
        # Beta should be positive and reasonable
        assert 0.5 < result < 2.0

    def test_beta_perfect_correlation(self):
        """Test beta with perfectly correlated returns."""
        asset_returns = [0.10, 0.12, 0.14, 0.16]
        market_returns = [0.10, 0.12, 0.14, 0.16]
        result = calculate_beta(asset_returns, market_returns)
        assert abs(result - 1.0) < 0.01

    def test_beta_mismatched_lengths(self):
        """Test beta with mismatched lengths."""
        asset_returns = [0.10, 0.15]
        market_returns = [0.08]
        with pytest.raises(ValueError, match="same length"):
            calculate_beta(asset_returns, market_returns)

    def test_beta_insufficient_data(self):
        """Test beta with insufficient data."""
        asset_returns = [0.10]
        market_returns = [0.08]
        with pytest.raises(ValueError, match="at least 2 observations"):
            calculate_beta(asset_returns, market_returns)


class TestCAPM:
    def test_capm_basic(self):
        """Test basic CAPM calculation."""
        result = calculate_capm(
            risk_free_rate=0.03,
            beta=1.2,
            market_return=0.11
        )
        # E(Ri) = 0.03 + 1.2 * (0.11 - 0.03) = 0.126
        assert abs(result - 0.126) < 0.001

    def test_capm_beta_one(self):
        """Test CAPM with beta = 1 (market portfolio)."""
        result = calculate_capm(
            risk_free_rate=0.03,
            beta=1.0,
            market_return=0.11
        )
        assert abs(result - 0.11) < 0.001

    def test_capm_beta_zero(self):
        """Test CAPM with beta = 0 (risk-free asset)."""
        result = calculate_capm(
            risk_free_rate=0.03,
            beta=0.0,
            market_return=0.11
        )
        assert abs(result - 0.03) < 0.001


class TestCovarianceCorrelation:
    def test_covariance_positive(self):
        """Test covariance with positively correlated returns."""
        returns1 = [0.10, 0.12, 0.14, 0.16]
        returns2 = [0.08, 0.10, 0.12, 0.14]
        result = calculate_covariance(returns1, returns2)
        assert result > 0

    def test_correlation_perfect(self):
        """Test correlation with perfectly correlated returns."""
        returns1 = [0.10, 0.12, 0.14, 0.16]
        returns2 = [0.10, 0.12, 0.14, 0.16]
        result = calculate_correlation(returns1, returns2)
        assert abs(result - 1.0) < 0.01

    def test_correlation_range(self):
        """Test that correlation is between -1 and 1."""
        returns1 = [0.10, 0.15, 0.12, 0.08, 0.14]
        returns2 = [0.08, 0.12, 0.10, 0.06, 0.11]
        result = calculate_correlation(returns1, returns2)
        assert -1 <= result <= 1
