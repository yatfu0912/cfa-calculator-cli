"""Tests for Time Value of Money formulas."""

import pytest
from cfa_calculator.formulas.tvm_formulas import (
    calculate_fv,
    calculate_pv,
    calculate_annuity_fv,
    calculate_annuity_pv,
    calculate_perpetuity,
    calculate_growing_perpetuity,
    calculate_ear,
)


class TestFutureValue:
    def test_fv_basic(self):
        """Test basic FV calculation."""
        result = calculate_fv(pv=1000, rate=0.05, n=10, freq=1)
        assert abs(result - 1628.89) < 0.01

    def test_fv_semi_annual(self):
        """Test FV with semi-annual compounding."""
        result = calculate_fv(pv=1000, rate=0.08, n=5, freq=2)
        assert abs(result - 1480.24) < 0.01

    def test_fv_monthly(self):
        """Test FV with monthly compounding."""
        result = calculate_fv(pv=1000, rate=0.06, n=1, freq=12)
        assert abs(result - 1061.68) < 0.01


class TestPresentValue:
    def test_pv_basic(self):
        """Test basic PV calculation."""
        result = calculate_pv(fv=1628.89, rate=0.05, n=10, freq=1)
        assert abs(result - 1000) < 0.01

    def test_pv_quarterly(self):
        """Test PV with quarterly compounding."""
        result = calculate_pv(fv=2000, rate=0.08, n=5, freq=4)
        assert abs(result - 1345.94) < 0.01


class TestAnnuityFV:
    def test_annuity_fv_ordinary(self):
        """Test ordinary annuity FV."""
        result = calculate_annuity_fv(pmt=1000, rate=0.05, n=10, annuity_type="ordinary")
        assert abs(result - 12577.89) < 0.01

    def test_annuity_fv_due(self):
        """Test annuity due FV."""
        result = calculate_annuity_fv(pmt=1000, rate=0.05, n=10, annuity_type="due")
        assert abs(result - 13206.79) < 0.01

    def test_annuity_fv_zero_rate(self):
        """Test annuity FV with zero rate."""
        result = calculate_annuity_fv(pmt=1000, rate=0, n=10)
        assert result == 10000


class TestAnnuityPV:
    def test_annuity_pv_ordinary(self):
        """Test ordinary annuity PV."""
        result = calculate_annuity_pv(pmt=1000, rate=0.05, n=10, annuity_type="ordinary")
        assert abs(result - 7721.73) < 0.01

    def test_annuity_pv_due(self):
        """Test annuity due PV."""
        result = calculate_annuity_pv(pmt=1000, rate=0.05, n=10, annuity_type="due")
        assert abs(result - 8107.82) < 0.01

    def test_annuity_pv_zero_rate(self):
        """Test annuity PV with zero rate."""
        result = calculate_annuity_pv(pmt=1000, rate=0, n=10)
        assert result == 10000


class TestPerpetuity:
    def test_perpetuity_basic(self):
        """Test basic perpetuity calculation."""
        result = calculate_perpetuity(pmt=100, rate=0.05)
        assert result == 2000

    def test_perpetuity_zero_rate(self):
        """Test perpetuity with zero rate raises error."""
        with pytest.raises(ValueError, match="Rate cannot be zero"):
            calculate_perpetuity(pmt=100, rate=0)


class TestGrowingPerpetuity:
    def test_growing_perpetuity_basic(self):
        """Test growing perpetuity calculation."""
        result = calculate_growing_perpetuity(pmt=100, rate=0.08, growth_rate=0.03)
        assert result == 2000

    def test_growing_perpetuity_invalid_rates(self):
        """Test growing perpetuity with invalid rates."""
        with pytest.raises(ValueError, match="Discount rate must be greater than growth rate"):
            calculate_growing_perpetuity(pmt=100, rate=0.05, growth_rate=0.05)


class TestEAR:
    def test_ear_semi_annual(self):
        """Test EAR with semi-annual compounding."""
        result = calculate_ear(stated_rate=0.08, freq=2)
        assert abs(result - 0.0816) < 0.0001

    def test_ear_monthly(self):
        """Test EAR with monthly compounding."""
        result = calculate_ear(stated_rate=0.12, freq=12)
        assert abs(result - 0.1268) < 0.0001

    def test_ear_daily(self):
        """Test EAR with daily compounding."""
        result = calculate_ear(stated_rate=0.05, freq=365)
        assert abs(result - 0.0513) < 0.0001
