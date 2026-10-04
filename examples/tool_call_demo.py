"""
examples/tool_call_demo.py

Step-by-step demonstration of the MCP tool call lifecycle:

    Tool definition
          ↓
    Tool registration   (on the server)
          ↓
    Tool discovery      (tools/list)
          ↓
    Tool invocation     (tools/call)
          ↓
    Tool result

Run:
    python examples/tool_call_demo.py
"""

from __future__ import annotations

import asyncio
import sys

sys.path.insert(0, "src")
sys.path.insert(0, ".")

from starter.client import MCPClient  # noqa: E402
from starter.tools import CALCULATOR_TOOL_DESCRIPTION  # noqa: E402


async def main() -> None:
    print("=== MCP Tool Call Lifecycle Demo ===\n")

    # Step 1 — Show the tool definition (the schema we registered)
    print("Step 1 — Tool definition (registered on the server):")
    print(f"  Name       : {CALCULATOR_TOOL_DESCRIPTION['name']}")
    print(f"  Description: {CALCULATOR_TOOL_DESCRIPTION['description']}")
    print(f"  Schema     : {CALCULATOR_TOOL_DESCRIPTION['inputSchema']}")
    print()

    async with MCPClient() as client:
        # Step 2 — Discover the tool via tools/list
        print("Step 2 — Tool discovery (tools/list):")
        tools = await client.list_tools()
        for tool in tools:
            print(f"  Found: {tool['name']}")
        print()

        # Step 3 — Invoke the tool via tools/call
        expressions = [
            "2 + 3",
            "10 * 5",
            "(10 + 5) / 3",
        ]
        print("Step 3 — Tool invocation (tools/call):")
        for expr in expressions:
            result = await client.call_tool("calculate", {"expression": expr})
            print(f"  calculate({expr!r}) = {result}")


if __name__ == "__main__":
    asyncio.run(main())
