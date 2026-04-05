"""Tests for Other financial calculation formulas."""

import pytest
from cfa_calculator.formulas.other_formulas import (
    calculate_npv,
    calculate_irr,
    calculate_money_weighted_return,
    calculate_time_weighted_return,
    calculate_payback_period,
    calculate_profitability_index,
    calculate_mirr,
)


class TestNPV:
    def test_npv_positive(self):
        """Test NPV with positive result."""
        cash_flows = [-1000, 300, 400, 500, 600]
        result = calculate_npv(0.10, cash_flows)
        assert result > 0

    def test_npv_negative(self):
        """Test NPV with negative result."""
        cash_flows = [-1000, 100, 100, 100]
        result = calculate_npv(0.20, cash_flows)
        assert result < 0

    def test_npv_zero_rate(self):
        """Test NPV with zero discount rate."""
        cash_flows = [-1000, 500, 600]
        result = calculate_npv(0, cash_flows)
        assert result == 100


class TestIRR:
    def test_irr_basic(self):
        """Test basic IRR calculation."""
        cash_flows = [-1000, 500, 500, 500]
        result = calculate_irr(cash_flows)
        # IRR should be positive and reasonable
        assert 0.20 < result < 0.30

    def test_irr_npv_zero(self):
        """Test that NPV at IRR equals zero."""
        cash_flows = [-1000, 400, 400, 400]
        irr = calculate_irr(cash_flows)
        npv_at_irr = calculate_npv(irr, cash_flows)
        assert abs(npv_at_irr) < 0.01

    def test_irr_insufficient_flows(self):
        """Test IRR with insufficient cash flows."""
        with pytest.raises(ValueError, match="at least 2 cash flows"):
            calculate_irr([100])

    def test_irr_no_sign_change(self):
        """Test IRR with no sign change."""
        with pytest.raises(ValueError, match="at least one sign change"):
            calculate_irr([100, 200, 300])


class TestMoneyWeightedReturn:
    def test_mwr_simple(self):
        """Test simple money-weighted return."""
        result = calculate_money_weighted_return(
            beginning_value=1000,
            ending_value=1200,
            cash_flows=[],
            times=[]
        )
        # Should be close to 20%
        assert 0.15 < result < 0.25

    def test_mwr_with_flows(self):
        """Test money-weighted return with cash flows."""
        result = calculate_money_weighted_return(
            beginning_value=1000,
            ending_value=1500,
            cash_flows=[200],
            times=[0.5]
        )
        assert result > 0


class TestTimeWeightedReturn:
    def test_twr_single_period(self):
        """Test time-weighted return for single period."""
        result = calculate_time_weighted_return(
            beginning_values=[1000],
            ending_values=[1100]
        )
        assert abs(result - 0.10) < 0.0001

    def test_twr_multiple_periods(self):
        """Test time-weighted return for multiple periods."""
        result = calculate_time_weighted_return(
            beginning_values=[1000, 1100],
            ending_values=[1100, 1210]
        )
        # (1.1 * 1.1) - 1 = 0.21
        assert abs(result - 0.21) < 0.0001

    def test_twr_mismatched_lengths(self):
        """Test TWR with mismatched lengths."""
        with pytest.raises(ValueError, match="same length"):
            calculate_time_weighted_return([1000], [1100, 1200])

    def test_twr_zero_beginning(self):
        """Test TWR with zero beginning value."""
        with pytest.raises(ValueError, match="Beginning value cannot be zero"):
            calculate_time_weighted_return([0], [100])


class TestPaybackPeriod:
    def test_payback_exact(self):
        """Test payback period with exact recovery."""
        result = calculate_payback_period(1000, [500, 500])
        assert result == 2.0

    def test_payback_fractional(self):
        """Test payback period with fractional year."""
        result = calculate_payback_period(1000, [400, 400, 400])
        assert 2.0 < result < 3.0

    def test_payback_not_recovered(self):
        """Test payback when investment not recovered."""
        with pytest.raises(ValueError, match="not recovered"):
            calculate_payback_period(1000, [100, 100])

    def test_payback_negative_investment(self):
        """Test payback with negative investment."""
        with pytest.raises(ValueError, match="must be positive"):
            calculate_payback_period(-1000, [500, 500])


class TestProfitabilityIndex:
    def test_pi_greater_than_one(self):
        """Test PI greater than 1 (accept project)."""
        result = calculate_profitability_index(
            rate=0.10,
            initial_investment=1000,
            cash_flows=[500, 500, 500]
        )
        assert result > 1.0

    def test_pi_less_than_one(self):
        """Test PI less than 1 (reject project)."""
        result = calculate_profitability_index(
            rate=0.20,
            initial_investment=1000,
            cash_flows=[200, 200, 200]
        )
        assert result < 1.0

    def test_pi_negative_investment(self):
        """Test PI with negative investment."""
        with pytest.raises(ValueError, match="must be positive"):
            calculate_profitability_index(0.10, -1000, [500, 500])


class TestMIRR:
    def test_mirr_basic(self):
        """Test basic MIRR calculation."""
        cash_flows = [-1000, 300, 400, 500, 600]
        result = calculate_mirr(cash_flows, finance_rate=0.10, reinvest_rate=0.12)
        # MIRR should be positive and reasonable
        assert 0.10 < result < 0.25

    def test_mirr_different_rates(self):
        """Test MIRR with different finance and reinvest rates."""
        cash_flows = [-1000, 500, 500, 500]
        mirr1 = calculate_mirr(cash_flows, 0.10, 0.10)
        mirr2 = calculate_mirr(cash_flows, 0.10, 0.15)
        # Higher reinvestment rate should give higher MIRR
        assert mirr2 > mirr1

    def test_mirr_no_negative_flows(self):
        """Test MIRR with no negative cash flows."""
        with pytest.raises(ValueError, match="at least one negative cash flow"):
            calculate_mirr([100, 200, 300], 0.10, 0.10)
