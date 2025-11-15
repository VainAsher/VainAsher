"""Tests for calculator module demonstrating basic testing patterns."""

import pytest
from src.vainasher.calculator import add, subtract, multiply, divide, power


class TestAddition:
    """Test cases for addition function."""

    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        assert add(2, 3) == 5

    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        assert add(-2, -3) == -5

    def test_add_mixed_signs(self):
        """Test adding positive and negative numbers."""
        assert add(5, -3) == 2
        assert add(-5, 3) == -2

    def test_add_floats(self):
        """Test adding floating point numbers."""
        result = add(2.5, 3.7)
        assert pytest.approx(result, 0.01) == 6.2

    def test_add_zero(self):
        """Test adding zero."""
        assert add(5, 0) == 5
        assert add(0, 5) == 5


class TestSubtraction:
    """Test cases for subtraction function."""

    def test_subtract_positive_numbers(self):
        """Test subtracting positive numbers."""
        assert subtract(5, 3) == 2

    def test_subtract_results_in_negative(self):
        """Test subtraction resulting in negative."""
        assert subtract(3, 5) == -2

    def test_subtract_zero(self):
        """Test subtracting zero."""
        assert subtract(5, 0) == 5


class TestMultiplication:
    """Test cases for multiplication function."""

    def test_multiply_positive_numbers(self):
        """Test multiplying positive numbers."""
        assert multiply(3, 4) == 12

    def test_multiply_by_zero(self):
        """Test multiplying by zero."""
        assert multiply(5, 0) == 0
        assert multiply(0, 5) == 0

    def test_multiply_negative_numbers(self):
        """Test multiplying negative numbers."""
        assert multiply(-3, -4) == 12
        assert multiply(-3, 4) == -12


class TestDivision:
    """Test cases for division function."""

    def test_divide_positive_numbers(self):
        """Test dividing positive numbers."""
        assert divide(10, 2) == 5.0

    def test_divide_results_in_float(self):
        """Test division resulting in float."""
        assert divide(7, 2) == 3.5

    def test_divide_by_zero_raises_error(self):
        """Test that dividing by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(5, 0)

    def test_divide_zero_by_number(self):
        """Test dividing zero by a number."""
        assert divide(0, 5) == 0.0

    def test_divide_negative_numbers(self):
        """Test dividing negative numbers."""
        assert divide(-10, 2) == -5.0
        assert divide(10, -2) == -5.0
        assert divide(-10, -2) == 5.0


class TestPower:
    """Test cases for power function."""

    def test_power_positive_exponent(self):
        """Test raising to positive exponent."""
        assert power(2, 3) == 8
        assert power(5, 2) == 25

    def test_power_zero_exponent(self):
        """Test raising to power of zero."""
        assert power(5, 0) == 1

    def test_power_negative_exponent(self):
        """Test raising to negative exponent."""
        assert power(2, -1) == 0.5

    def test_power_fractional_exponent(self):
        """Test raising to fractional exponent (roots)."""
        result = power(4, 0.5)
        assert pytest.approx(result, 0.01) == 2.0
