"""
tests/test_client.py

Tests for src/starter/client.py (MCPClient).

The file has two layers, because they prove different things:

1. Unit tests with a fake ClientSession (class ``TestClientWithFakeSession``).
   These check the logic MCPClient itself owns: turning SDK response objects
   into plain dicts/strings, handling empty results, and refusing to work
   when not connected. No subprocess is started, so they are instant and
   cannot be broken by anything outside client.py.

2. A real round trip over stdio (class ``TestRealRoundTrip``).
   These launch ``python -m starter.server`` as a subprocess and talk to it
   through MCPClient. This is the only layer that proves the client and
   server actually agree on the protocol. The server is local and
   deterministic, so no network or external service is involved.

Covers the five behaviours listed in issue B01:
  1. connect / initialise            4. a valid calculation returns the result
  2. discover the calculate tool     5. read a registered resource
  3. invoke the calculate tool
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

from starter.client import MCPClient

# A hung subprocess would otherwise stall the whole test run silently.
ROUND_TRIP_TIMEOUT_SECONDS = 30


# ──────────────────────────────────────────────────────────────────────────────
# Fake session — stands in for mcp.ClientSession, returns canned SDK-shaped data
# ──────────────────────────────────────────────────────────────────────────────
class FakeSession:
    """Mimics the few ClientSession methods that MCPClient calls.

    Each method returns a SimpleNamespace shaped like the real SDK response
    (e.g. ``response.tools``), so MCPClient's attribute access works unchanged.
    """

    def __init__(
        self,
        *,
        tools: list[Any] | None = None,
        resources: list[Any] | None = None,
        call_content: list[Any] | None = None,
        read_contents: list[Any] | None = None,
    ) -> None:
        self._tools = tools or []
        self._resources = resources or []
        self._call_content = call_content if call_content is not None else []
        self._read_contents = read_contents if read_contents is not None else []
        self.calls: list[tuple[str, tuple[Any, ...]]] = []

    async def list_tools(self) -> SimpleNamespace:
        self.calls.append(("list_tools", ()))
        return SimpleNamespace(tools=self._tools)

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> SimpleNamespace:
        self.calls.append(("call_tool", (name, arguments)))
        return SimpleNamespace(content=self._call_content)

    async def list_resources(self) -> SimpleNamespace:
        self.calls.append(("list_resources", ()))
        return SimpleNamespace(resources=self._resources)

    async def read_resource(self, uri: Any) -> SimpleNamespace:
        self.calls.append(("read_resource", (str(uri),)))
        return SimpleNamespace(contents=self._read_contents)


def client_with(session: FakeSession) -> MCPClient:
    """Build an MCPClient that believes it is connected to *session*."""
    client = MCPClient()
    client._session = session  # type: ignore[assignment]
    return client


def text_block(text: str) -> SimpleNamespace:
    return SimpleNamespace(type="text", text=text)


# ──────────────────────────────────────────────────────────────────────────────
# Layer 1 — unit tests, no subprocess
# ──────────────────────────────────────────────────────────────────────────────
class TestNotConnected:
    """Using the client before connect() must fail loudly and clearly."""

    @pytest.mark.parametrize(
        ("method", "args"),
        [
            ("list_tools", ()),
            ("call_tool", ("calculate", {"expression": "1 + 1"})),
            ("list_resources", ()),
            ("read_resource", ("workshop://introduction",)),
        ],
    )
    async def test_method_raises_runtime_error(self, method, args):
        client = MCPClient()
        with pytest.raises(RuntimeError, match="not connected"):
            await getattr(client, method)(*args)

    async def test_disconnect_without_connect_is_a_noop(self):
        client = MCPClient()
        await client.disconnect()  # must not raise
        assert client._session is None


class TestClientWithFakeSession:
    async def test_list_tools_returns_plain_dicts(self):
        session = FakeSession(
            tools=[
                SimpleNamespace(
                    name="calculate",
                    description="Evaluate arithmetic.",
                    inputSchema={"type": "object", "required": ["expression"]},
                )
            ]
        )
        tools = await client_with(session).list_tools()

        assert tools == [
            {
                "name": "calculate",
                "description": "Evaluate arithmetic.",
                "inputSchema": {"type": "object", "required": ["expression"]},
            }
        ]

    async def test_list_tools_empty_server(self):
        assert await client_with(FakeSession()).list_tools() == []

    async def test_call_tool_forwards_name_and_arguments(self):
        session = FakeSession(call_content=[text_block("5")])
        result = await client_with(session).call_tool(
            "calculate", {"expression": "2 + 3"}
        )

        assert result == "5"
        assert session.calls == [("call_tool", ("calculate", {"expression": "2 + 3"}))]

    async def test_call_tool_returns_only_the_first_block(self):
        session = FakeSession(call_content=[text_block("first"), text_block("second")])
        assert await client_with(session).call_tool("calculate", {}) == "first"

    async def test_call_tool_with_no_content_returns_empty_string(self):
        session = FakeSession(call_content=[])
        assert await client_with(session).call_tool("calculate", {}) == ""

    async def test_call_tool_falls_back_to_str_for_non_text_block(self):
        # e.g. an image block has no .text attribute.
        block = SimpleNamespace(type="image", data="abc")
        session = FakeSession(call_content=[block])
        result = await client_with(session).call_tool("calculate", {})
        assert result == str(block)

    async def test_list_resources_returns_plain_dicts(self):
        session = FakeSession(
            resources=[
                SimpleNamespace(
                    uri="workshop://introduction",
                    name="Workshop Introduction",
                    description="A brief introduction.",
                    mimeType="text/plain",
                )
            ]
        )
        resources = await client_with(session).list_resources()

        assert resources == [
            {
                "uri": "workshop://introduction",
                "name": "Workshop Introduction",
                "description": "A brief introduction.",
                "mimeType": "text/plain",
            }
        ]

    async def test_list_resources_applies_defaults_for_missing_fields(self):
        session = FakeSession(
            resources=[
                SimpleNamespace(
                    uri="workshop://bare", name=None, description=None, mimeType=None
                )
            ]
        )
        (resource,) = await client_with(session).list_resources()

        assert resource["name"] == ""
        assert resource["description"] == ""
        assert resource["mimeType"] == "text/plain"

    async def test_read_resource_returns_text_and_passes_uri(self):
        session = FakeSession(read_contents=[SimpleNamespace(text="Welcome!")])
        text = await client_with(session).read_resource("workshop://introduction")

        assert text == "Welcome!"
        assert session.calls == [("read_resource", ("workshop://introduction",))]

    async def test_read_resource_with_no_contents_returns_empty_string(self):
        session = FakeSession(read_contents=[])
        assert await client_with(session).read_resource("workshop://x") == ""


# ──────────────────────────────────────────────────────────────────────────────
# Layer 2 — real round trip: MCPClient <-> stdio <-> starter.server
# ──────────────────────────────────────────────────────────────────────────────
class TestRealRoundTrip:
    """Each test opens its own connection (about half a second each).

    The client is entered with ``async with`` inside the test body, not in a
    fixture: the SDK's stdio transport uses task groups that must be entered
    and exited from the same task, which fixture setup/teardown does not
    guarantee.
    """

    async def test_connects_and_exposes_a_session(self):
        async with asyncio.timeout(ROUND_TRIP_TIMEOUT_SECONDS):
            async with MCPClient() as client:
                assert client._session is not None

    async def test_session_is_closed_after_leaving_context(self):
        async with asyncio.timeout(ROUND_TRIP_TIMEOUT_SECONDS):
            async with MCPClient() as client:
                pass
            assert client._session is None
            with pytest.raises(RuntimeError, match="not connected"):
                await client.list_tools()

    async def test_discovers_the_calculate_tool(self):
        async with asyncio.timeout(ROUND_TRIP_TIMEOUT_SECONDS):
            async with MCPClient() as client:
                tools = await client.list_tools()

        by_name = {tool["name"]: tool for tool in tools}
        assert "calculate" in by_name
        schema = by_name["calculate"]["inputSchema"]
        assert "expression" in schema["properties"]
        assert "expression" in schema["required"]

    @pytest.mark.parametrize(
        ("expression", "expected"),
        [("2 + 3", "5"), ("10 * 5", "50"), ("(10 + 5) / 3", "5")],
    )
    async def test_valid_calculation_returns_expected_result(
        self, expression, expected
    ):
        async with asyncio.timeout(ROUND_TRIP_TIMEOUT_SECONDS):
            async with MCPClient() as client:
                result = await client.call_tool("calculate", {"expression": expression})

        assert result == expected

    async def test_calculator_error_comes_back_as_text_not_exception(self):
        # server.py catches ValueError and returns "Error: ..." as the result,
        # so the client sees a normal string rather than a raised exception.
        async with asyncio.timeout(ROUND_TRIP_TIMEOUT_SECONDS):
            async with MCPClient() as client:
                result = await client.call_tool("calculate", {"expression": "1 / 0"})

        assert result.startswith("Error:")
        assert "zero" in result.lower()

    async def test_discovers_registered_resources(self):
        async with asyncio.timeout(ROUND_TRIP_TIMEOUT_SECONDS):
            async with MCPClient() as client:
                resources = await client.list_resources()

        uris = {resource["uri"] for resource in resources}
        assert {"workshop://introduction", "workshop://architecture"} <= uris

    async def test_reads_a_registered_resource(self):
        from starter.resources import read_resource

        async with asyncio.timeout(ROUND_TRIP_TIMEOUT_SECONDS):
            async with MCPClient() as client:
                text = await client.read_resource("workshop://introduction")

        # Compare with the source of truth instead of hard-coding the prose,
        # so editing the resource text does not break this test.
        assert text == read_resource("workshop://introduction")
        assert text.strip() != ""
