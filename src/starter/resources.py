"""
src/starter/resources.py

MCP resource definitions for the starter repository.

An MCP Resource is a piece of information an agent can *read*.
Unlike a Tool (which performs an operation), a Resource is essentially
a named document or data blob.

Resources are identified by a URI, for example:
    workshop://introduction

The client calls resources/list to discover resources and
resources/read to retrieve one.
"""

from __future__ import annotations

# ──────────────────────────────────────────────────────────────────────────────
# Static resource definitions
# ──────────────────────────────────────────────────────────────────────────────

RESOURCES: dict[str, dict[str, str]] = {
    "workshop://introduction": {
        "uri": "workshop://introduction",
        "name": "Workshop Introduction",
        "description": "A brief introduction to the Agentic AI and MCP workshop.",
        "mimeType": "text/plain",
        "content": (
            "Welcome to the Agentic AI and MCP Workshop!\n\n"
            "Model Context Protocol (MCP) is a standardised interface that lets AI agents\n"
            "discover and interact with external tools and resources.\n\n"
            "In this workshop you will learn:\n"
            "  1. What MCP is and why it exists\n"
            "  2. How an MCP server registers tools and resources\n"
            "  3. How an MCP client discovers and invokes tools\n"
            "  4. How a basic agent loop ties everything together\n\n"
            "Happy hacking!"
        ),
    },
    "workshop://architecture": {
        "uri": "workshop://architecture",
        "name": "MCP Architecture Overview",
        "description": "A text diagram explaining the MCP client/server architecture.",
        "mimeType": "text/plain",
        "content": (
            "MCP Architecture\n"
            "================\n\n"
            "┌─────────────┐\n"
            "│    Agent    │\n"
            "└──────┬──────┘\n"
            "       │\n"
            "       ▼\n"
            "┌─────────────┐\n"
            "│ MCP Client  │\n"
            "└──────┬──────┘\n"
            "       │\n"
            "       │  MCP / JSON-RPC\n"
            "       ▼\n"
            "┌─────────────┐\n"
            "│ MCP Server  │\n"
            "└──────┬──────┘\n"
            "       │\n"
            "   ┌───┴────────┐\n"
            "   ▼            ▼\n"
            "┌───────┐   ┌──────────┐\n"
            "│ Tool  │   │ Resource │\n"
            "└───────┘   └──────────┘\n\n"
            "Tool     → performs an operation (e.g. calculate)\n"
            "Resource → provides information  (e.g. workshop://introduction)\n"
        ),
    },
    "workshop://getting-started": {
        "uri": "workshop://getting-started",
        "name": "Getting Started Guide",
        "description": "Setup steps and the learning flow for workshop participants.",
        "mimeType": "text/plain",
        "content": (
            "Getting Started\n"
            "===============\n\n"
            "Setup\n"
            "-----\n"
            "  1. Clone the repository and open a terminal in its root folder.\n"
            "  2. Create a virtual environment with Python 3.12:\n"
            "       Linux / macOS : python3.12 -m venv .venv\n"
            "       Windows       : py -3.12 -m venv .venv\n"
            "  3. Activate it:\n"
            "       Linux / macOS : source .venv/bin/activate\n"
            "       Windows       : .venv\\Scripts\\Activate.ps1\n"
            "  4. Install the dependencies, then the project itself:\n"
            "       pip install -r requirements.txt\n"
            "       pip install -e .\n"
            "  5. Check that everything works:\n"
            "       pytest -q\n"
            "       ruff check .\n\n"
            "No API keys are needed. The workshop runs offline with a mock LLM.\n\n"
            "Learning flow\n"
            "-------------\n"
            "  1. Read the README to learn what MCP is and how the pieces fit.\n"
            "  2. Run the scripts in examples/ to watch discovery and invocation.\n"
            "  3. Read the source in this order: server.py, client.py, agent.py.\n"
            "  4. Run the tests to see how each part is verified.\n"
            "  5. Pick an issue from docs/ISSUES.md, implement it, add tests,\n"
            "     and open a pull request.\n"
        ),
    },
}


def list_resources() -> list[dict[str, str]]:
    """Return metadata for all registered resources (without content)."""
    return [
        {k: v for k, v in res.items() if k != "content"}
        for res in RESOURCES.values()
    ]


def read_resource(uri: str) -> str:
    """Return the text content of the resource identified by *uri*.

    Raises
    ------
    KeyError
        If no resource with the given URI is registered.
    """
    if uri not in RESOURCES:
        raise KeyError(f"Unknown resource URI: {uri!r}")
    return RESOURCES[uri]["content"]
