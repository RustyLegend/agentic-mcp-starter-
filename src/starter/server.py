"""
src/starter/server.py

Minimal MCP server for the agentic-mcp-starter workshop.

This server demonstrates:
  1. Server initialisation
  2. Tool registration  (tools/list)
  3. Tool invocation    (tools/call)
  4. Resource registration (resources/list)
  5. Resource retrieval    (resources/read)

The MCP Python SDK handles all JSON-RPC framing for us — we simply
decorate functions with @mcp.tool() and @mcp.resource().

Run directly:
    python -m starter.server
"""

from __future__ import annotations

import logging

from mcp.server.fastmcp import FastMCP

from starter.resources import RESOURCES, read_resource
from starter.tools import CALCULATOR_TOOL_DESCRIPTION, safe_calculate

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# Create the MCP server
# ──────────────────────────────────────────────────────────────────────────────
mcp = FastMCP(
    name="agentic-mcp-starter",
    instructions=(
        "This is a workshop MCP server. "
        "It provides a calculator tool and two educational resources."
    ),
)


# ──────────────────────────────────────────────────────────────────────────────
# Tool registration
# ──────────────────────────────────────────────────────────────────────────────
@mcp.tool(
    name=CALCULATOR_TOOL_DESCRIPTION["name"],
    description=CALCULATOR_TOOL_DESCRIPTION["description"],
)
def calculate(expression: str) -> str:
    """MCP tool: evaluate a simple arithmetic expression.

    Parameters
    ----------
    expression:
        Plain arithmetic such as ``"2 + 3"`` or ``"(10 + 5) / 3"``.

    Returns
    -------
    str
        The numeric result, or an error message prefixed with "Error: ".
    """
    logger.info("Tool invoked: calculate(%r)", expression)
    try:
        result = safe_calculate(expression)
        logger.info("Tool result: %r", result)
        return result
    except ValueError as exc:
        logger.warning("Tool error: %s", exc)
        return f"Error: {exc}"


# ──────────────────────────────────────────────────────────────────────────────
# Resource registration
# ──────────────────────────────────────────────────────────────────────────────
for _uri, _meta in RESOURCES.items():

    def _make_handler(uri: str):  # noqa: ANN202
        """Create a closure so each handler captures its own *uri*."""

        @mcp.resource(
            uri=uri,
            name=RESOURCES[uri]["name"],
            description=RESOURCES[uri]["description"],
            mime_type=RESOURCES[uri].get("mimeType", "text/plain"),
        )
        def _resource_handler() -> str:
            logger.info("Resource read: %r", uri)
            return read_resource(uri)

        return _resource_handler

    _make_handler(_uri)


# ──────────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    logger.info("Starting MCP server …")
    mcp.run()
