"""
examples/resource_demo.py

Demonstrates MCP resource discovery and retrieval:

    Resource registration (on the server)
          ↓
    Resource discovery   (resources/list)
          ↓
    Resource retrieval   (resources/read)

Run:
    python examples/resource_demo.py
"""

from __future__ import annotations

import asyncio
import sys

sys.path.insert(0, "src")
sys.path.insert(0, ".")

from starter.client import MCPClient  # noqa: E402


async def main() -> None:
    print("=== MCP Resource Demo ===\n")

    async with MCPClient() as client:
        # Step 1 — List all resources
        resources = await client.list_resources()
        print(f"Discovered {len(resources)} resource(s):\n")
        for r in resources:
            print(f"  URI  : {r['uri']}")
            print(f"  Name : {r['name']}")
            print(f"  Desc : {r['description']}")
            print()

        # Step 2 — Read each resource
        for r in resources:
            print(f"── Reading {r['uri']} ──")
            content = await client.read_resource(r["uri"])
            print(content)
            print()


if __name__ == "__main__":
    asyncio.run(main())
