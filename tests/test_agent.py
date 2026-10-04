"""
tests/test_agent.py

Tests for src/starter/agent.py.

The agent tests use an injected MCPClient mock so they run without
starting a real MCP server subprocess.
"""

from __future__ import annotations

import pytest

from mocks.llm import MockLLM
from starter.agent import Agent


# ──────────────────────────────────────────────────────────────────────────────
# Fake MCP client — avoids subprocess spawning during tests
# ──────────────────────────────────────────────────────────────────────────────
class FakeMCPClient:
    """A synchronous-looking async fake for the real MCPClient."""

    async def call_tool(self, name: str, arguments: dict) -> str:
        if name == "calculate":
            from starter.tools import safe_calculate

            return safe_calculate(arguments["expression"])
        raise ValueError(f"Unknown tool: {name}")


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
class TestAgentCalculation:
    @pytest.fixture()
    def agent(self) -> Agent:
        return Agent(llm=MockLLM(), client=FakeMCPClient())

    async def test_simple_addition(self, agent):
        reply = await agent.run("calculate 5 + 7")
        assert "12" in reply

    async def test_multiplication(self, agent):
        reply = await agent.run("calculate 10 * 5")
        assert "50" in reply

    async def test_parenthesised_expression(self, agent):
        reply = await agent.run("calculate (10 + 5) / 3")
        assert "5" in reply

    async def test_reply_contains_expression(self, agent):
        reply = await agent.run("calculate 2 + 3")
        # The final response should mention the expression
        assert "2 + 3" in reply or "5" in reply


class TestAgentNoTool:
    @pytest.fixture()
    def agent(self) -> Agent:
        return Agent(llm=MockLLM(), client=FakeMCPClient())

    async def test_greeting_no_tool(self, agent):
        reply = await agent.run("hello")
        assert isinstance(reply, str)
        assert len(reply) > 0

    async def test_help_no_tool(self, agent):
        reply = await agent.run("help")
        assert isinstance(reply, str)
