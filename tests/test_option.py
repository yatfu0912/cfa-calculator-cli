"""Tests for Derivatives and Option pricing formulas."""

import pytest
import math
from cfa_calculator.formulas.option_formulas import (
    calculate_option_payoff,
    calculate_put_call_parity,
    calculate_black_scholes,
    calculate_binomial_option,
)


class TestOptionPayoff:
    def test_call_payoff_itm(self):
        """Test call option payoff when in-the-money."""
        result = calculate_option_payoff("call", spot_price=110, strike_price=100)
        assert result == 10.0

    def test_call_payoff_otm(self):
        """Test call option payoff when out-of-the-money."""
        result = calculate_option_payoff("call", spot_price=90, strike_price=100)
        assert result == 0.0

    def test_put_payoff_itm(self):
        """Test put option payoff when in-the-money."""
        result = calculate_option_payoff("put", spot_price=90, strike_price=100)
        assert result == 10.0

    def test_put_payoff_otm(self):
        """Test put option payoff when out-of-the-money."""
        result = calculate_option_payoff("put", spot_price=110, strike_price=100)
        assert result == 0.0

    def test_call_profit_with_premium(self):
        """Test call option profit including premium."""
        result = calculate_option_payoff("call", spot_price=110, strike_price=100, premium=3.0)
        # Payoff = 10, Premium = 3, Profit = 7
        assert result == 7.0

    def test_put_loss_with_premium(self):
        """Test put option loss when OTM with premium."""
        result = calculate_option_payoff("put", spot_price=110, strike_price=100, premium=5.0)
        # Payoff = 0, Premium = 5, Loss = -5
        assert result == -5.0

    def test_invalid_option_type(self):
        """Test with invalid option type."""
        with pytest.raises(ValueError, match="must be 'call' or 'put'"):
            calculate_option_payoff("invalid", 100, 100)


class TestPutCallParity:
    def test_solve_for_call(self):
        """Test solving for call price."""
        result = calculate_put_call_parity(
            call_price=None,
            put_price=5.0,
            spot_price=100.0,
            strike_price=100.0,
            risk_free_rate=0.05,
            time_to_expiry=1.0
        )
        # C = P + S - K×e^(-r×T)
        # C = 5 + 100 - 100×e^(-0.05×1) = 5 + 100 - 95.12 = 9.88
        assert abs(result["call_price"] - 9.88) < 0.01

    def test_solve_for_put(self):
        """Test solving for put price."""
        result = calculate_put_call_parity(
            call_price=10.0,
            put_price=None,
            spot_price=100.0,
            strike_price=100.0,
            risk_free_rate=0.05,
            time_to_expiry=1.0
        )
        # P = C + K×e^(-r×T) - S
        # P = 10 + 100×e^(-0.05×1) - 100 = 10 + 95.12 - 100 = 5.12
        assert abs(result["put_price"] - 5.12) < 0.01

    def test_solve_for_spot(self):
        """Test solving for spot price."""
        result = calculate_put_call_parity(
            call_price=10.0,
            put_price=5.0,
            spot_price=None,
            strike_price=100.0,
            risk_free_rate=0.05,
            time_to_expiry=1.0
        )
        # S = C + K×e^(-r×T) - P
        assert abs(result["spot_price"] - 100.12) < 0.01

    def test_no_missing_value(self):
        """Test with no missing value."""
        with pytest.raises(ValueError, match="Exactly one value must be None"):
            calculate_put_call_parity(10.0, 5.0, 100.0, 100.0, 0.05, 1.0)

    def test_multiple_missing_values(self):
        """Test with multiple missing values."""
        with pytest.raises(ValueError, match="Exactly one value must be None"):
            calculate_put_call_parity(None, None, 100.0, 100.0, 0.05, 1.0)


class TestBlackScholes:
    def test_call_option_atm(self):
        """Test Black-Scholes call option at-the-money."""
        result = calculate_black_scholes(
            option_type="call",
            spot_price=100.0,
            strike_price=100.0,
            time_to_expiry=1.0,
            risk_free_rate=0.05,
            volatility=0.20
        )
        # ATM call should have positive value
        assert result["option_price"] > 0
        assert 7 < result["option_price"] < 12  # Reasonable range

    def test_put_option_atm(self):
        """Test Black-Scholes put option at-the-money."""
        result = calculate_black_scholes(
            option_type="put",
            spot_price=100.0,
            strike_price=100.0,
            time_to_expiry=1.0,
            risk_free_rate=0.05,
            volatility=0.20
        )
        # ATM put should have positive value
        assert result["option_price"] > 0
        assert 5 < result["option_price"] < 10

    def test_call_delta_positive(self):
        """Test that call delta is positive."""
        result = calculate_black_scholes(
            option_type="call",
            spot_price=100.0,
            strike_price=100.0,
            time_to_expiry=1.0,
            risk_free_rate=0.05,
            volatility=0.20
        )
        assert 0 < result["delta"] < 1

    def test_put_delta_negative(self):
        """Test that put delta is negative."""
        result = calculate_black_scholes(
            option_type="put",
            spot_price=100.0,
            strike_price=100.0,
            time_to_expiry=1.0,
            risk_free_rate=0.05,
            volatility=0.20
        )
        assert -1 < result["delta"] < 0

    def test_gamma_positive(self):
        """Test that gamma is always positive."""
        result = calculate_black_scholes(
            option_type="call",
            spot_price=100.0,
            strike_price=100.0,
            time_to_expiry=1.0,
            risk_free_rate=0.05,
            volatility=0.20
        )
        assert result["gamma"] > 0

    def test_vega_positive(self):
        """Test that vega is always positive."""
        result = calculate_black_scholes(
            option_type="call",
            spot_price=100.0,
            strike_price=100.0,
            time_to_expiry=1.0,
            risk_free_rate=0.05,
            volatility=0.20
        )
        assert result["vega"] > 0

    def test_call_theta_negative(self):
        """Test that call theta is typically negative."""
        result = calculate_black_scholes(
            option_type="call",
            spot_price=100.0,
            strike_price=100.0,
            time_to_expiry=1.0,
            risk_free_rate=0.05,
            volatility=0.20
        )
        # Theta is negative for long options (time decay)
        assert result["theta"] < 0

    def test_with_dividend(self):
        """Test Black-Scholes with dividend yield."""
        result = calculate_black_scholes(
            option_type="call",
            spot_price=100.0,
            strike_price=100.0,
            time_to_expiry=1.0,
            risk_free_rate=0.05,
            volatility=0.20,
            dividend_yield=0.02
        )
        # Call price should be lower with dividends
        assert result["option_price"] > 0

    def test_invalid_spot_price(self):
        """Test with invalid spot price."""
        with pytest.raises(ValueError, match="must be positive"):
            calculate_black_scholes("call", -100, 100, 1.0, 0.05, 0.20)

    def test_invalid_volatility(self):
        """Test with invalid volatility."""
        with pytest.raises(ValueError, match="must be positive"):
            calculate_black_scholes("call", 100, 100, 1.0, 0.05, 0.0)


class TestBinomialOption:
    def test_european_call(self):
        """Test binomial model for European call."""
        result = calculate_binomial_option(
            option_type="call",
            spot_price=100.0,
            strike_price=100.0,
            time_to_expiry=1.0,
            risk_free_rate=0.05,
            volatility=0.20,
            steps=100,
            american=False
        )
        # Should be close to Black-Scholes for European options
        bs_result = calculate_black_scholes("call", 100, 100, 1.0, 0.05, 0.20)
        assert abs(result - bs_result["option_price"]) < 0.5

    def test_european_put(self):
        """Test binomial model for European put."""
        result = calculate_binomial_option(
            option_type="put",
            spot_price=100.0,
            strike_price=100.0,
            time_to_expiry=1.0,
            risk_free_rate=0.05,
            volatility=0.20,
            steps=100,
            american=False
        )
        # Should be close to Black-Scholes for European options
        bs_result = calculate_black_scholes("put", 100, 100, 1.0, 0.05, 0.20)
        assert abs(result - bs_result["option_price"]) < 0.5

    def test_american_put_higher(self):
        """Test that American put is worth more than European put."""
        european = calculate_binomial_option(
            "put", 100, 100, 1.0, 0.05, 0.20, steps=100, american=False
        )
        american = calculate_binomial_option(
            "put", 100, 100, 1.0, 0.05, 0.20, steps=100, american=True
        )
        # American put should be worth at least as much as European
        assert american >= european

    def test_few_steps(self):
        """Test binomial model with few steps."""
        result = calculate_binomial_option(
            "call", 100, 100, 1.0, 0.05, 0.20, steps=10, american=False
        )
        # Should still produce reasonable result
        assert result > 0

    def test_invalid_steps(self):
        """Test with invalid number of steps."""
        with pytest.raises(ValueError, match="at least 1"):
            calculate_binomial_option("call", 100, 100, 1.0, 0.05, 0.20, steps=0)

    def test_deep_itm_call(self):
        """Test binomial model for deep in-the-money call."""
        result = calculate_binomial_option(
            "call", 120, 100, 1.0, 0.05, 0.20, steps=50, american=False
        )
        # Deep ITM call should be worth at least intrinsic value
        assert result > 20.0

    def test_deep_otm_put(self):
        """Test binomial model for deep out-of-the-money put."""
        result = calculate_binomial_option(
            "put", 120, 100, 1.0, 0.05, 0.20, steps=50, american=False
        )
        # Deep OTM put should be worth very little (but still has some time value)
        assert result < 2.0
