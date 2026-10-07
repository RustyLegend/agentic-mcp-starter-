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


# ──────────────────────────────────────────────────────────────────────────────
# Issue B02 — calculator edge-case coverage
# ──────────────────────────────────────────────────────────────────────────────
class TestB02ValidExpressions:
    """The valid inputs listed in issue B02, as one table."""

    @pytest.mark.parametrize(
        ("expression", "expected"),
        [
            ("2 + 3", "5"),
            ("10 * 5", "50"),
            # 15 / 3 is 5.0 internally; whole numbers must print without ".0".
            ("(10 + 5) / 3", "5"),
            # Large results must stay exact integers, not 4.294967296e+09.
            ("2 ** 32", "4294967296"),
        ],
    )
    def test_valid_expression(self, expression, expected):
        assert safe_calculate(expression) == expected

    def test_large_power_has_no_scientific_notation(self):
        result = safe_calculate("2 ** 32")
        assert "e" not in result.lower()
        assert result.isdigit()

    def test_negative_exponent_gives_fraction(self):
        assert safe_calculate("2 ** -1") == "0.5"

    def test_underscore_digit_separators(self):
        # Python literal syntax: 1_000 is the integer 1000.
        assert safe_calculate("1_000 + 1") == "1001"


class TestB02DivisionByZero:
    """Every operator that can divide must report zero as ValueError."""

    @pytest.mark.parametrize(
        "expression",
        ["1 / 0", "10 // 0", "10 % 0", "0 ** -1", "5 / (3 - 3)"],
    )
    def test_zero_divisor_raises_value_error(self, expression):
        with pytest.raises(ValueError, match="[Dd]ivision by zero"):
            safe_calculate(expression)


class TestB02EmptyAndMalformed:
    @pytest.mark.parametrize("expression", ["", " ", "\t\n"])
    def test_blank_input_raises_value_error(self, expression):
        with pytest.raises(ValueError, match="empty"):
            safe_calculate(expression)

    @pytest.mark.parametrize("expression", ["1 +", "(1 + 2", "1 + * 2", "2 3"])
    def test_malformed_input_is_reported_as_invalid(self, expression):
        # SyntaxError must be translated; callers only ever see ValueError.
        with pytest.raises(ValueError, match="Invalid expression"):
            safe_calculate(expression)


class TestB02UnsafeInput:
    """Unsafe input must be rejected by the allow-list, not by luck.

    Asserting on the "Disallowed"/"Unsupported"/"Non-numeric" message proves
    the expression parsed fine and was refused for what it *is*, rather than
    failing earlier as a syntax error.
    """

    @pytest.mark.parametrize(
        "expression",
        [
            "abc",  # bare name
            "__import__('os')",  # function call
            "__import__('os').system('echo hi')",  # attribute access + call
            "(1).__class__",  # attribute access on a literal
            "[1, 2, 3]",  # list display
            "lambda: 1",  # lambda
            "1 if True else 2",  # conditional expression
            "1 < 2",  # comparison
        ],
    )
    def test_disallowed_syntax_is_rejected(self, expression):
        with pytest.raises(ValueError, match="Disallowed AST node"):
            safe_calculate(expression)

    @pytest.mark.parametrize("expression", ["'hello'", "None", "b'x'", "1j"])
    def test_non_numeric_constants_are_rejected(self, expression):
        with pytest.raises(ValueError, match="Non-numeric constant"):
            safe_calculate(expression)

    @pytest.mark.parametrize("expression", ["1 << 2", "1 & 3", "7 @ 2"])
    def test_unlisted_binary_operators_are_rejected(self, expression):
        with pytest.raises(ValueError, match="Unsupported operator"):
            safe_calculate(expression)

    @pytest.mark.parametrize("expression", ["+5", "~5"])
    def test_unlisted_unary_operators_are_rejected(self, expression):
        with pytest.raises(ValueError, match="Unsupported unary operator"):
            safe_calculate(expression)
