"""
src/starter/client.py

Minimal MCP client for the agentic-mcp-starter workshop.

This module shows how an MCP client:
  1. Connects to the local MCP server
  2. Discovers available tools   (tools/list)
  3. Discovers resources         (resources/list)
  4. Reads a resource            (resources/read)
  5. Invokes a tool              (tools/call)
  6. Receives the result

The class ``MCPClient`` wraps the MCP Python SDK's ``ClientSession``
and exposes a simple async interface that the agent loop uses.

Connection
----------
In workshop / local mode we launch the server as a subprocess via
``stdio`` transport, which is the simplest and most educational option.
"""

from __future__ import annotations

import logging
import sys
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logger = logging.getLogger(__name__)


class MCPClient:
    """A lightweight async MCP client.

    Usage (async context manager)
    -----------------------------
    ::

        async with MCPClient() as client:
            tools    = await client.list_tools()
            result   = await client.call_tool("calculate", {"expression": "2+3"})
    """

    def __init__(self, server_module: str = "starter.server") -> None:
        self._server_module = server_module
        self._session: ClientSession | None = None
        self._exit_stack: Any = None

    async def __aenter__(self) -> MCPClient:
        await self.connect()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.disconnect()

    async def connect(self) -> None:
        """Start the MCP server subprocess and open the session."""
        from contextlib import AsyncExitStack

        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", self._server_module],
        )

        self._exit_stack = AsyncExitStack()
        stdio_transport = await self._exit_stack.enter_async_context(
            stdio_client(params)
        )
        read_stream, write_stream = stdio_transport
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )
        await self._session.initialize()
        logger.info("MCP session initialised.")

    async def disconnect(self) -> None:
        """Close the session and stop the server subprocess."""
        if self._exit_stack is not None:
            await self._exit_stack.aclose()
            self._exit_stack = None
            self._session = None
        logger.info("MCP session closed.")

    # ──────────────────────────────────────────────────────────────
    # Tools
    # ──────────────────────────────────────────────────────────────

    async def list_tools(self) -> list[dict[str, Any]]:
        """Return a list of tool descriptors from the server."""
        self._ensure_connected()
        response = await self._session.list_tools()  # type: ignore[union-attr]
        tools = [
            {
                "name": t.name,
                "description": t.description,
                "inputSchema": t.inputSchema,
            }
            for t in response.tools
        ]
        logger.info("Discovered %d tool(s): %s", len(tools), [t["name"] for t in tools])
        return tools

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> str:
        """Invoke an MCP tool and return the text result.

        Parameters
        ----------
        name:
            Tool name, e.g. ``"calculate"``.
        arguments:
            Keyword arguments matching the tool's input schema.

        Returns
        -------
        str
            The text content of the first result block.
        """
        self._ensure_connected()
        logger.info("Calling tool %r with args %r", name, arguments)
        response = await self._session.call_tool(name, arguments)  # type: ignore[union-attr]
        contents = response.content
        if not contents:
            return ""
        return str(contents[0].text) if hasattr(contents[0], "text") else str(contents[0])

    # ──────────────────────────────────────────────────────────────
    # Resources
    # ──────────────────────────────────────────────────────────────

    async def list_resources(self) -> list[dict[str, str]]:
        """Return a list of resource descriptors from the server."""
        self._ensure_connected()
        response = await self._session.list_resources()  # type: ignore[union-attr]
        resources = [
            {
                "uri": str(r.uri),
                "name": r.name or "",
                "description": r.description or "",
                "mimeType": r.mimeType or "text/plain",
            }
            for r in response.resources
        ]
        logger.info(
            "Discovered %d resource(s): %s",
            len(resources),
            [r["uri"] for r in resources],
        )
        return resources

    async def read_resource(self, uri: str) -> str:
        """Retrieve the content of an MCP resource.

        Parameters
        ----------
        uri:
            Resource URI, e.g. ``"workshop://introduction"``.

        Returns
        -------
        str
            The text content of the resource.
        """
        self._ensure_connected()
        logger.info("Reading resource %r", uri)
        from mcp.types import AnyUrl

        response = await self._session.read_resource(AnyUrl(uri))  # type: ignore[union-attr]
        contents = response.contents
        if not contents:
            return ""
        item = contents[0]
        return item.text if hasattr(item, "text") else str(item)

    # ──────────────────────────────────────────────────────────────
    # Internal helpers
    # ──────────────────────────────────────────────────────────────

    def _ensure_connected(self) -> None:
        if self._session is None:
            raise RuntimeError("MCPClient is not connected. Use 'async with MCPClient()' or call connect() first.")
