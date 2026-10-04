"""
src/starter/agent.py

Basic educational agent loop for the agentic-mcp-starter workshop.

The agent demonstrates the following flow:

    User Input
        ↓
    Agent
        ↓
    Mock LLM  ← decides whether a tool is needed
        ↓
    Tool Request
        ↓
    MCP Client
        ↓
    MCP Server
        ↓
    Calculator Tool
        ↓
    Tool Result
        ↓
    Agent
        ↓
    Final Response

The agent is intentionally simple.  Its purpose is to show **how** an
agent interacts with an MCP server — not to implement sophisticated
reasoning.
"""

from __future__ import annotations

import logging
from typing import Any

from mocks.llm import MockLLM
from starter.client import MCPClient

logger = logging.getLogger(__name__)


class Agent:
    """A minimal agent that can call an MCP tool via a Mock LLM.

    Parameters
    ----------
    llm:
        An LLM (or mock) that decides whether to call a tool.
        Defaults to :class:`mocks.llm.MockLLM`.
    client:
        An :class:`starter.client.MCPClient` instance.
        If *None* the agent creates one when running.
    """

    def __init__(
        self,
        llm: MockLLM | None = None,
        client: MCPClient | None = None,
    ) -> None:
        self.llm = llm or MockLLM()
        self._client = client

    async def run(self, user_message: str) -> str:
        """Process a single user message and return a response.

        The method handles its own MCP client lifecycle if no external
        client was injected.

        Parameters
        ----------
        user_message:
            The plain-text message from the user.

        Returns
        -------
        str
            The agent's final answer.
        """
        logger.info("Agent received message: %r", user_message)

        # Step 1 — Ask the Mock LLM whether to call a tool
        decision: dict[str, Any] = self.llm.decide(user_message)
        logger.info("LLM decision: %r", decision)

        if not decision.get("use_tool"):
            # No tool needed — return a direct reply
            reply = decision.get("reply", "I'm not sure how to help with that.")
            logger.info("No tool needed. Replying directly.")
            return reply

        tool_name: str = decision["tool"]
        tool_args: dict[str, Any] = decision["args"]

        # Step 2 — Use the MCP client to call the tool
        if self._client is not None:
            result = await self._client.call_tool(tool_name, tool_args)
        else:
            async with MCPClient() as client:
                result = await client.call_tool(tool_name, tool_args)

        logger.info("Tool %r returned: %r", tool_name, result)

        # Step 3 — Format the final response
        expression = tool_args.get("expression", "")
        final = f"The result of {expression} is {result}."
        logger.info("Final response: %r", final)
        return final
