"""
tests/test_tools.py

Tests for src/starter/tools.py (the calculator).

Covers:
  - Basic arithmetic
  - Operator precedence / parentheses
  - Negative numbers
  - Division that yields a float
  - Division by zero
  - Empty expression
  - Invalid / syntactically broken expression
  - Unsafe expressions (function calls, names, etc.)
"""

from __future__ import annotations

import pytest

from starter.tools import safe_calculate


class TestBasicArithmetic:
    def test_addition(self):
        assert safe_calculate("2 + 3") == "5"

    def test_subtraction(self):
        assert safe_calculate("10 - 4") == "6"

    def test_multiplication(self):
        assert safe_calculate("10 * 5") == "50"

    def test_division_integer_result(self):
        assert safe_calculate("10 / 2") == "5"

    def test_division_float_result(self):
        result = safe_calculate("10 / 3")
        assert result.startswith("3.333")

    def test_floor_division(self):
        assert safe_calculate("10 // 3") == "3"

    def test_modulo(self):
        assert safe_calculate("10 % 3") == "1"

    def test_power(self):
        assert safe_calculate("2 ** 8") == "256"


class TestParenthesesAndPrecedence:
    def test_parentheses(self):
        assert safe_calculate("(10 + 5) / 3") == "5"

    def test_nested_parentheses(self):
        assert safe_calculate("((2 + 3) * 4)") == "20"

    def test_operator_precedence(self):
        # 2 + 3 * 4 = 2 + 12 = 14
        assert safe_calculate("2 + 3 * 4") == "14"


class TestNegativeNumbers:
    def test_unary_minus(self):
        assert safe_calculate("-5 + 10") == "5"

    def test_negative_result(self):
        assert safe_calculate("3 - 10") == "-7"


class TestEdgeCases:
    def test_single_number(self):
        assert safe_calculate("42") == "42"

    def test_float_input(self):
        assert safe_calculate("3.14 * 2") == "6.28"

    def test_whitespace_heavy(self):
        assert safe_calculate("  2  +  3  ") == "5"


class TestErrors:
    def test_empty_expression(self):
        with pytest.raises(ValueError, match="empty"):
            safe_calculate("")

    def test_whitespace_only(self):
        with pytest.raises(ValueError, match="empty"):
            safe_calculate("   ")

    def test_division_by_zero(self):
        with pytest.raises(ValueError, match="[Dd]ivision by zero"):
            safe_calculate("1 / 0")

    def test_syntax_error(self):
        with pytest.raises(ValueError, match="Invalid expression"):
            safe_calculate("2 +")

    def test_unsafe_function_call(self):
        with pytest.raises(ValueError):
            safe_calculate("__import__('os').system('echo hi')")

    def test_unsafe_name(self):
        with pytest.raises(ValueError):
            safe_calculate("x + 1")

    def test_string_literal(self):
        with pytest.raises(ValueError):
            safe_calculate("'hello'")
