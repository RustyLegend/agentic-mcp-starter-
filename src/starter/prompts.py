"""
src/starter/prompts.py

Simple, reusable prompt templates for the starter agent.

These are plain Python strings — no templating library is required.
You can substitute values with Python's str.format() or f-strings.

Templates
---------
SYSTEM_PROMPT        — Establishes the agent's role and available tools.
TOOL_SELECTION_PROMPT — Used to ask the mock LLM which tool to call.
FINAL_RESPONSE_PROMPT — Combines the tool result into a user-facing reply.
"""

from __future__ import annotations

# ──────────────────────────────────────────────────────────────────────────────
# System prompt
# ──────────────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a helpful assistant that can use tools via MCP.

Available tools:
  - calculate(expression): Evaluates a simple arithmetic expression.

When the user's request involves arithmetic, call the calculate tool.
Otherwise, reply directly.
"""

# ──────────────────────────────────────────────────────────────────────────────
# Tool-selection prompt — insert the user message at {user_message}
# ──────────────────────────────────────────────────────────────────────────────
TOOL_SELECTION_PROMPT = """Given the following user message, decide whether to call a tool.

User message: "{user_message}"

If arithmetic is involved, respond with:
  TOOL: calculate
  ARGS: <the arithmetic expression>

Otherwise respond with:
  NO_TOOL
"""

# ──────────────────────────────────────────────────────────────────────────────
# Final-response prompt
# ──────────────────────────────────────────────────────────────────────────────
FINAL_RESPONSE_PROMPT = """The user asked: "{user_message}"
The calculate tool returned: {tool_result}

Please provide a friendly, concise response.
"""


def build_tool_selection_prompt(user_message: str) -> str:
    """Return a formatted tool-selection prompt for *user_message*."""
    return TOOL_SELECTION_PROMPT.format(user_message=user_message)


def build_final_response_prompt(user_message: str, tool_result: str) -> str:
    """Return a formatted final-response prompt."""
    return FINAL_RESPONSE_PROMPT.format(
        user_message=user_message,
        tool_result=tool_result,
    )
