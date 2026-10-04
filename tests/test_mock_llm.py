"""
tests/test_mock_llm.py

Tests for mocks/llm.py (MockLLM).

Verifies that the mock LLM:
  - Is deterministic (same input → same output)
  - Routes calculation requests to the calculate tool
  - Returns the arithmetic expression correctly
  - Handles non-arithmetic messages without a tool call
  - Handles greetings with a canned reply
"""

from __future__ import annotations

import pytest

from mocks.llm import MockLLM


@pytest.fixture()
def llm() -> MockLLM:
    return MockLLM()


class TestCalculationRouting:
    def test_simple_addition(self, llm):
        decision = llm.decide("calculate 5 + 7")
        assert decision["use_tool"] is True
        assert decision["tool"] == "calculate"
        assert "5 + 7" in decision["args"]["expression"]

    def test_multiplication(self, llm):
        decision = llm.decide("calculate 10 * 5")
        assert decision["use_tool"] is True
        assert "10 * 5" in decision["args"]["expression"]

    def test_parenthesised_expression(self, llm):
        decision = llm.decide("calculate (10 + 5) / 3")
        assert decision["use_tool"] is True
        assert "(10 + 5) / 3" in decision["args"]["expression"]

    def test_bare_expression_routed(self, llm):
        """A bare arithmetic expression like '2 + 3' should route to calculate."""
        decision = llm.decide("2 + 3")
        assert decision["use_tool"] is True

    def test_what_is_phrasing(self, llm):
        decision = llm.decide("what is 8 * 8")
        assert decision["use_tool"] is True
        assert decision["tool"] == "calculate"


class TestNonCalculationMessages:
    def test_hello_returns_no_tool(self, llm):
        decision = llm.decide("hello")
        assert decision["use_tool"] is False

    def test_help_returns_no_tool(self, llm):
        decision = llm.decide("help")
        assert decision["use_tool"] is False

    def test_unknown_message_no_tool(self, llm):
        decision = llm.decide("who are you?")
        assert decision["use_tool"] is False
        assert "reply" in decision

    def test_no_tool_reply_is_string(self, llm):
        decision = llm.decide("hello there")
        assert isinstance(decision["reply"], str)
        assert len(decision["reply"]) > 0


class TestDeterminism:
    def test_same_output_twice(self, llm):
        """Identical calls must produce identical results."""
        d1 = llm.decide("calculate 3 + 4")
        d2 = llm.decide("calculate 3 + 4")
        assert d1 == d2

    def test_repr(self, llm):
        assert "MockLLM" in repr(llm)
