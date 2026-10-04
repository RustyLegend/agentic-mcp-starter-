"""
mocks/llm.py

Deterministic Mock LLM for the agentic-mcp-starter workshop.

The Mock LLM replaces a real language model.  It uses simple keyword /
regex matching to decide whether the user's message requires a tool call
and, if so, what arguments to extract.

Key properties
--------------
- Completely deterministic
- Makes no network requests
- Requires no API keys
- Always returns the same output for the same input

How it works
------------
1. Strip the user message of whitespace.
2. Look for the keyword "calculate" (case-insensitive).
3. If found, extract the expression that follows and return a
   ``use_tool=True`` decision pointing at the ``calculate`` tool.
4. Otherwise return ``use_tool=False`` with a canned reply.

This is intentionally simple.  Real LLMs use probabilistic reasoning;
the mock shows *the shape* of the interaction without the complexity.

Extending (Issue I02)
---------------------
Contributors working on issue I02 should extend ``_extract_expression``
or add more sophisticated routing logic here.
"""

from __future__ import annotations

import re
from typing import Any

# Pattern: optional "calculate" keyword, then the arithmetic part
_CALCULATE_RE = re.compile(
    r"(?:calculate|compute|eval|evaluate|what\s+is)?\s*"
    r"([\d\s\+\-\*\/\(\)\.\%\^]+)",
    re.IGNORECASE,
)


class MockLLM:
    """A fully deterministic, offline mock LLM.

    Parameters
    ----------
    name:
        A label used in repr / logs (cosmetic only).
    """

    def __init__(self, name: str = "MockLLM-v1") -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"MockLLM(name={self.name!r})"

    # ──────────────────────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────────────────────

    def decide(self, user_message: str) -> dict[str, Any]:
        """Return a routing decision for *user_message*.

        Returns
        -------
        dict
            One of two shapes:

            **Tool call**::

                {
                    "use_tool": True,
                    "tool": "calculate",
                    "args": {"expression": "<expr>"},
                }

            **Direct reply**::

                {
                    "use_tool": False,
                    "reply": "<canned response>",
                }
        """
        message = user_message.strip()

        if self._is_calculation_request(message):
            expression = self._extract_expression(message)
            return {
                "use_tool": True,
                "tool": "calculate",
                "args": {"expression": expression},
            }

        return {
            "use_tool": False,
            "reply": self._canned_reply(message),
        }

    # ──────────────────────────────────────────────────────────────
    # Private helpers
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def _is_calculation_request(message: str) -> bool:
        """Return True if the message looks like a maths request."""
        calc_keywords = ("calculate", "compute", "eval", "evaluate", "what is")
        lower = message.lower()
        if any(kw in lower for kw in calc_keywords):
            return True
        # Also treat bare expressions like "5 + 7" as calculation requests
        if _CALCULATE_RE.match(message) and any(op in message for op in "+-*/"):
            return True
        return False

    @staticmethod
    def _extract_expression(message: str) -> str:
        """Pull the arithmetic portion out of *message*.

        Examples
        --------
        >>> MockLLM._extract_expression("calculate 5 + 7")
        '5 + 7'
        >>> MockLLM._extract_expression("what is (10 + 5) / 3")
        '(10 + 5) / 3'
        """
        # Remove leading keyword if present
        cleaned = re.sub(
            r"^(?:calculate|compute|eval|evaluate|what\s+is)\s*",
            "",
            message,
            flags=re.IGNORECASE,
        ).strip()
        return cleaned if cleaned else message

    @staticmethod
    def _canned_reply(message: str) -> str:
        """Return a deterministic canned reply for non-tool messages."""
        lower = message.lower()
        if "hello" in lower or "hi" in lower:
            return "Hello! I'm the workshop mock agent. Ask me to calculate something!"
        if "help" in lower:
            return (
                "I can evaluate arithmetic expressions. "
                "Try: 'calculate 5 + 7' or '(10 + 5) / 3'."
            )
        return f"I received your message: '{message}'. I can only calculate arithmetic in mock mode."
