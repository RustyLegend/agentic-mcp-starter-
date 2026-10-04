"""
examples/basic_client.py

Demonstrates how an MCP client connects to the server, discovers tools
and resources, and calls the calculator tool.

Run:
    python examples/basic_client.py

Expected output:
    === MCP Basic Client Demo ===

    [Tools]
    - calculate: Evaluate a simple arithmetic expression ...

    [Resources]
    - workshop://introduction : Workshop Introduction
    - workshop://architecture : MCP Architecture Overview

    [Tool call]  calculate('2 + 3')  →  5
"""

from __future__ import annotations

import asyncio
import sys

sys.path.insert(0, "src")
sys.path.insert(0, ".")

from starter.client import MCPClient  # noqa: E402


async def main() -> None:
    print("=== MCP Basic Client Demo ===\n")

    async with MCPClient() as client:
        # ── Discover tools ───────────────────────────────────────
        tools = await client.list_tools()
        print("[Tools]")
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description'][:60]}…")

        print()

        # ── Discover resources ───────────────────────────────────
        resources = await client.list_resources()
        print("[Resources]")
        for resource in resources:
            print(f"  - {resource['uri']} : {resource['name']}")

        print()

        # ── Invoke a tool ────────────────────────────────────────
        expression = "2 + 3"
        result = await client.call_tool("calculate", {"expression": expression})
        print(f"[Tool call]  calculate({expression!r})  →  {result}")


if __name__ == "__main__":
    asyncio.run(main())
