"""Tests for Fixed Income (Bond) formulas."""

import pytest
from cfa_calculator.formulas.bond_formulas import (
    calculate_bond_price,
    calculate_ytm,
    calculate_ytc,
    calculate_current_yield,
    calculate_macaulay_duration,
    calculate_modified_duration,
    calculate_convexity,
)


class TestBondPrice:
    def test_bond_price_at_par(self):
        """Test bond price when YTM equals coupon rate (should equal face value)."""
        result = calculate_bond_price(
            face_value=1000,
            coupon_rate=0.06,
            ytm=0.06,
            years=10,
            frequency=2
        )
        assert abs(result - 1000) < 0.01

    def test_bond_price_premium(self):
        """Test bond price when YTM < coupon rate (premium bond)."""
        result = calculate_bond_price(
            face_value=1000,
            coupon_rate=0.06,
            ytm=0.05,
            years=10,
            frequency=2
        )
        assert result > 1000

    def test_bond_price_discount(self):
        """Test bond price when YTM > coupon rate (discount bond)."""
        result = calculate_bond_price(
            face_value=1000,
            coupon_rate=0.06,
            ytm=0.07,
            years=10,
            frequency=2
        )
        assert result < 1000

    def test_bond_price_annual_coupon(self):
        """Test bond price with annual coupon payments."""
        result = calculate_bond_price(
            face_value=1000,
            coupon_rate=0.08,
            ytm=0.06,
            years=5,
            frequency=1
        )
        assert result > 1000


class TestYTM:
    def test_ytm_at_par(self):
        """Test YTM when bond is priced at par."""
        result = calculate_ytm(
            price=1000,
            face_value=1000,
            coupon_rate=0.06,
            years=10,
            frequency=2
        )
        assert abs(result - 0.06) < 0.0001

    def test_ytm_premium_bond(self):
        """Test YTM for premium bond (YTM < coupon rate)."""
        result = calculate_ytm(
            price=1100,
            face_value=1000,
            coupon_rate=0.08,
            years=10,
            frequency=2
        )
        assert result < 0.08

    def test_ytm_discount_bond(self):
        """Test YTM for discount bond (YTM > coupon rate)."""
        result = calculate_ytm(
            price=900,
            face_value=1000,
            coupon_rate=0.06,
            years=10,
            frequency=2
        )
        assert result > 0.06


class TestYTC:
    def test_ytc_basic(self):
        """Test basic YTC calculation."""
        result = calculate_ytc(
            price=1050,
            face_value=1000,
            coupon_rate=0.08,
            years_to_call=5,
            call_price=1030,
            frequency=2
        )
        # YTC should be positive and reasonable
        assert 0 < result < 0.20

    def test_ytc_at_call_price(self):
        """Test YTC when current price equals call price."""
        result = calculate_ytc(
            price=1030,
            face_value=1000,
            coupon_rate=0.08,
            years_to_call=5,
            call_price=1030,
            frequency=2
        )
        # YTC should be close to coupon rate
        assert abs(result - 0.08) < 0.01


class TestCurrentYield:
    def test_current_yield_at_par(self):
        """Test current yield when bond is at par."""
        result = calculate_current_yield(
            price=1000,
            face_value=1000,
            coupon_rate=0.06
        )
        assert abs(result - 0.06) < 0.0001

    def test_current_yield_premium(self):
        """Test current yield for premium bond."""
        result = calculate_current_yield(
            price=1100,
            face_value=1000,
            coupon_rate=0.06
        )
        # Current yield should be less than coupon rate
        assert result < 0.06

    def test_current_yield_discount(self):
        """Test current yield for discount bond."""
        result = calculate_current_yield(
            price=900,
            face_value=1000,
            coupon_rate=0.06
        )
        # Current yield should be greater than coupon rate
        assert result > 0.06


class TestMacaulayDuration:
    def test_duration_zero_coupon_bond(self):
        """Test duration of zero-coupon bond (should equal maturity)."""
        result = calculate_macaulay_duration(
            face_value=1000,
            coupon_rate=0.0,
            ytm=0.06,
            years=10,
            frequency=1
        )
        assert abs(result - 10) < 0.01

    def test_duration_coupon_bond(self):
        """Test duration of coupon bond (should be less than maturity)."""
        result = calculate_macaulay_duration(
            face_value=1000,
            coupon_rate=0.06,
            ytm=0.06,
            years=10,
            frequency=2
        )
        assert result < 10
        assert result > 0

    def test_duration_increases_with_maturity(self):
        """Test that duration increases with maturity."""
        dur_5y = calculate_macaulay_duration(1000, 0.06, 0.06, 5, 2)
        dur_10y = calculate_macaulay_duration(1000, 0.06, 0.06, 10, 2)
        assert dur_10y > dur_5y


class TestModifiedDuration:
    def test_modified_duration_relationship(self):
        """Test that modified duration < Macaulay duration."""
        macaulay = calculate_macaulay_duration(1000, 0.06, 0.06, 10, 2)
        modified = calculate_modified_duration(1000, 0.06, 0.06, 10, 2)
        assert modified < macaulay

    def test_modified_duration_formula(self):
        """Test modified duration formula."""
        macaulay = calculate_macaulay_duration(1000, 0.06, 0.06, 10, 2)
        modified = calculate_modified_duration(1000, 0.06, 0.06, 10, 2)
        expected = macaulay / (1 + 0.06 / 2)
        assert abs(modified - expected) < 0.0001


class TestConvexity:
    def test_convexity_positive(self):
        """Test that convexity is positive."""
        result = calculate_convexity(
            face_value=1000,
            coupon_rate=0.06,
            ytm=0.06,
            years=10,
            frequency=2
        )
        assert result > 0

    def test_convexity_increases_with_maturity(self):
        """Test that convexity increases with maturity."""
        conv_5y = calculate_convexity(1000, 0.06, 0.06, 5, 2)
        conv_10y = calculate_convexity(1000, 0.06, 0.06, 10, 2)
        assert conv_10y > conv_5y

    def test_convexity_zero_coupon(self):
        """Test convexity of zero-coupon bond."""
        result = calculate_convexity(
            face_value=1000,
            coupon_rate=0.0,
            ytm=0.06,
            years=10,
            frequency=1
        )
        # Zero-coupon bond has higher convexity
        assert result > 0
