"""Tests for Equity Valuation formulas."""

import pytest
from cfa_calculator.formulas.equity_formulas import (
    calculate_gordon_growth_model,
    calculate_multistage_ddm,
    calculate_fcfe_valuation,
    calculate_pe_valuation,
    calculate_justified_pe_ratio,
    calculate_peg_ratio,
)


class TestGordonGrowthModel:
    def test_ddm_basic(self):
        """Test basic Gordon Growth Model calculation."""
        result = calculate_gordon_growth_model(
            dividend=5.0,
            required_return=0.12,
            growth_rate=0.05
        )
        # V0 = 5.0 / (0.12 - 0.05) = 5.0 / 0.07 = 71.43
        assert abs(result - 71.43) < 0.01

    def test_ddm_high_growth(self):
        """Test DDM with higher growth rate."""
        result = calculate_gordon_growth_model(
            dividend=3.0,
            required_return=0.15,
            growth_rate=0.08
        )
        # V0 = 3.0 / (0.15 - 0.08) = 3.0 / 0.07 = 42.86
        assert abs(result - 42.86) < 0.01

    def test_ddm_invalid_growth(self):
        """Test DDM with growth rate >= required return."""
        with pytest.raises(ValueError, match="greater than growth rate"):
            calculate_gordon_growth_model(5.0, 0.08, 0.10)

    def test_ddm_equal_rates(self):
        """Test DDM with equal growth and required return."""
        with pytest.raises(ValueError, match="greater than growth rate"):
            calculate_gordon_growth_model(5.0, 0.10, 0.10)


class TestMultistageDDM:
    def test_two_stage_ddm(self):
        """Test two-stage DDM calculation."""
        result = calculate_multistage_ddm(
            current_dividend=2.0,
            high_growth_rate=0.15,
            high_growth_years=5,
            stable_growth_rate=0.05,
            required_return=0.12
        )
        # Should be positive and reasonable
        assert result > 0
        assert result > 30  # Should be higher than simple DDM due to high growth

    def test_two_stage_short_period(self):
        """Test two-stage DDM with short high growth period."""
        result = calculate_multistage_ddm(
            current_dividend=3.0,
            high_growth_rate=0.20,
            high_growth_years=3,
            stable_growth_rate=0.04,
            required_return=0.10
        )
        assert result > 0

    def test_two_stage_invalid_stable_growth(self):
        """Test two-stage DDM with invalid stable growth rate."""
        with pytest.raises(ValueError, match="greater than stable growth rate"):
            calculate_multistage_ddm(2.0, 0.15, 5, 0.12, 0.10)

    def test_two_stage_zero_years(self):
        """Test two-stage DDM with zero high growth years."""
        with pytest.raises(ValueError, match="at least 1"):
            calculate_multistage_ddm(2.0, 0.15, 0, 0.05, 0.12)


class TestFCFEValuation:
    def test_fcfe_basic(self):
        """Test basic FCFE valuation."""
        result = calculate_fcfe_valuation(
            fcfe=10.0,
            required_return=0.12,
            growth_rate=0.05
        )
        # V0 = 10.0 / (0.12 - 0.05) = 10.0 / 0.07 = 142.86
        assert abs(result - 142.86) < 0.01

    def test_fcfe_negative_fcfe(self):
        """Test FCFE valuation with negative FCFE."""
        result = calculate_fcfe_valuation(-5.0, 0.12, 0.05)
        # Should handle negative FCFE
        assert result < 0

    def test_fcfe_invalid_growth(self):
        """Test FCFE with growth rate >= required return."""
        with pytest.raises(ValueError, match="greater than growth rate"):
            calculate_fcfe_valuation(10.0, 0.08, 0.10)


class TestPEValuation:
    def test_pe_valuation_basic(self):
        """Test basic P/E valuation."""
        result = calculate_pe_valuation(
            earnings_per_share=5.0,
            benchmark_pe=15.0
        )
        # V0 = 5.0 × 15.0 = 75.0
        assert result == 75.0

    def test_pe_valuation_high_pe(self):
        """Test P/E valuation with high P/E ratio."""
        result = calculate_pe_valuation(
            earnings_per_share=3.0,
            benchmark_pe=25.0
        )
        assert result == 75.0

    def test_pe_valuation_negative_eps(self):
        """Test P/E valuation with negative EPS."""
        with pytest.raises(ValueError, match="cannot be negative"):
            calculate_pe_valuation(-5.0, 15.0)

    def test_pe_valuation_negative_pe(self):
        """Test P/E valuation with negative P/E."""
        with pytest.raises(ValueError, match="cannot be negative"):
            calculate_pe_valuation(5.0, -15.0)


class TestJustifiedPERatio:
    def test_justified_pe_basic(self):
        """Test basic justified P/E calculation."""
        result = calculate_justified_pe_ratio(
            dividend_payout_ratio=0.40,
            required_return=0.12,
            growth_rate=0.05
        )
        # P/E = 0.40 × (1 + 0.05) / (0.12 - 0.05) = 0.42 / 0.07 = 6.0
        assert abs(result - 6.0) < 0.01

    def test_justified_pe_high_payout(self):
        """Test justified P/E with high payout ratio."""
        result = calculate_justified_pe_ratio(
            dividend_payout_ratio=0.80,
            required_return=0.10,
            growth_rate=0.03
        )
        # P/E = 0.80 × 1.03 / 0.07 = 11.77
        assert abs(result - 11.77) < 0.01

    def test_justified_pe_invalid_payout(self):
        """Test justified P/E with invalid payout ratio."""
        with pytest.raises(ValueError, match="between 0 and 1"):
            calculate_justified_pe_ratio(1.5, 0.12, 0.05)

    def test_justified_pe_invalid_growth(self):
        """Test justified P/E with growth >= required return."""
        with pytest.raises(ValueError, match="greater than growth rate"):
            calculate_justified_pe_ratio(0.40, 0.08, 0.10)


class TestPEGRatio:
    def test_peg_basic(self):
        """Test basic PEG ratio calculation."""
        result = calculate_peg_ratio(
            pe_ratio=20.0,
            growth_rate=0.15
        )
        # PEG = 20.0 / (0.15 × 100) = 20.0 / 15.0 = 1.33
        assert abs(result - 1.33) < 0.01

    def test_peg_undervalued(self):
        """Test PEG ratio indicating undervaluation."""
        result = calculate_peg_ratio(
            pe_ratio=12.0,
            growth_rate=0.20
        )
        # PEG = 12.0 / 20.0 = 0.60 (undervalued)
        assert result < 1.0

    def test_peg_overvalued(self):
        """Test PEG ratio indicating overvaluation."""
        result = calculate_peg_ratio(
            pe_ratio=30.0,
            growth_rate=0.10
        )
        # PEG = 30.0 / 10.0 = 3.0 (overvalued)
        assert result > 1.0

    def test_peg_zero_growth(self):
        """Test PEG with zero growth rate."""
        with pytest.raises(ValueError, match="must be positive"):
            calculate_peg_ratio(20.0, 0.0)

    def test_peg_negative_growth(self):
        """Test PEG with negative growth rate."""
        with pytest.raises(ValueError, match="must be positive"):
            calculate_peg_ratio(20.0, -0.05)
