"""
examples/basic_server.py

Demonstrates how to start the MCP server directly.

Run:
    python examples/basic_server.py

The server listens on stdio and waits for an MCP client to connect.
Press Ctrl+C to stop it.
"""

from __future__ import annotations

import logging
import sys

# Add src/ to Python path so we can import starter.*
sys.path.insert(0, "src")

logging.basicConfig(level=logging.INFO, stream=sys.stderr)

from starter.server import mcp  # noqa: E402

if __name__ == "__main__":
    print("Starting MCP server — waiting for client connections …", file=sys.stderr)
    print("Press Ctrl+C to stop.", file=sys.stderr)
    mcp.run()
