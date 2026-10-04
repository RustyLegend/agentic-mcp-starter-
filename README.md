# agentic-mcp-starter

> A beginner-friendly MCP starter repository for the **Agentic AI Open-Source Workshop**.

[![CI](https://github.com/<org>/agentic-mcp-starter/actions/workflows/ci.yml/badge.svg)](https://github.com/<org>/agentic-mcp-starter/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Table of Contents

1. [What is MCP?](#1-what-is-mcp)
2. [Why MCP?](#2-why-mcp)
3. [MCP Architecture](#3-mcp-architecture)
4. [Tool vs Resource](#4-tool-vs-resource)
5. [Tool Registration vs Tool Invocation](#5-tool-registration-vs-tool-invocation)
6. [JSON-RPC Basics](#6-json-rpc-basics)
7. [Repository Structure](#7-repository-structure)
8. [Setup](#8-setup)
9. [Run the Examples](#9-run-the-examples)
10. [Run the Agent](#10-run-the-agent)
11. [Run Tests](#11-run-tests)
12. [Run Ruff](#12-run-ruff)
13. [Mock Mode](#13-mock-mode)
14. [First Contribution](#14-first-contribution)
15. [Contributor Issues](#15-contributor-issues)
16. [Troubleshooting](#16-troubleshooting)

---

## 1. What is MCP?

**Model Context Protocol (MCP)** is a standardised interface that lets AI agents communicate with external tools and data sources.

### The problem without MCP

Imagine you are building an AI assistant that can search the web, query a database, and call a calculator.  Without a standard, you have to write custom integration code for each tool.  Every agent has a different way of calling tools, and every tool has to support every agent separately.

### The solution MCP provides

MCP defines one common protocol.

```
Any Agent  ──(MCP)──▶  Any Tool
```

An agent that speaks MCP can talk to any MCP-compatible tool.
A tool that speaks MCP can be used by any MCP-compatible agent.

### A simple example

Without MCP:

```python
# Agent has to know how to call this specific calculator
import calculator
result = calculator.add(5, 7)
```

With MCP:

```python
# Agent calls any tool via the same interface
result = await mcp_client.call_tool("calculate", {"expression": "5 + 7"})
```

The agent does not need to know how the calculator is implemented.
It just needs to know the tool's name and its input schema.

---

## 2. Why MCP?

| Without MCP | With MCP |
|-------------|----------|
| Custom integration per tool | One protocol for all tools |
| Agent and tool are tightly coupled | Agent and tool are decoupled |
| Hard to swap tools | Swap tools without changing the agent |
| Hard to discover what a tool does | Tools describe themselves |
| Hard to test in isolation | Server and client can be tested separately |

MCP is to AI agents what HTTP is to the web — a shared language that
makes everything composable.

---

## 3. MCP Architecture

```
┌─────────────┐
│    Agent    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ MCP Client  │
└──────┬──────┘
       │
       │  MCP / JSON-RPC
       ▼
┌─────────────┐
│ MCP Server  │
└──────┬──────┘
       │
   ┌───┴────────┐
   ▼            ▼
┌───────┐   ┌──────────┐
│ Tool  │   │ Resource │
└───────┘   └──────────┘
```

| Component | Role |
|-----------|------|
| **Agent** | The AI loop that decides what to do |
| **MCP Client** | Speaks MCP protocol on behalf of the agent |
| **MCP Server** | Hosts tools and resources; handles requests |
| **Tool** | A callable capability (e.g. calculate) |
| **Resource** | A readable piece of information (e.g. documentation) |

The client and server communicate using **JSON-RPC 2.0** over standard I/O
(in local mode) or another transport.

---

## 4. Tool vs Resource

MCP distinguishes between two types of things a server can expose:

### Tool

> Something the agent can **call** to perform an operation.

A tool takes input, does something, and returns a result.

```
calculate("5 + 7")  →  "12"
```

### Resource

> Information the agent can **read**.

A resource is identified by a URI and returns static or semi-static content.

```
workshop://introduction  →  "Welcome to the workshop …"
```

### Summary

| | Tool | Resource |
|-|------|----------|
| Purpose | Perform an action | Provide information |
| How agent uses it | `call_tool()` | `read_resource()` |
| Example | `calculate("2+3")` | `workshop://introduction` |
| Analogy | A function call | A file or web page |

---

## 5. Tool Registration vs Tool Invocation

### Registration

When the server starts, it **registers** its tools.
This is the server saying:

> "I provide a tool called `calculate`.
> It takes one parameter: `expression` (a string).
> Here is its description."

```python
@mcp.tool(name="calculate", description="…")
def calculate(expression: str) -> str:
    ...
```

### Discovery

A client can ask the server: *"What tools do you have?"*

```
Client → tools/list → Server
Server → [{"name": "calculate", …}] → Client
```

### Invocation

Once the client knows the tool exists, it can call it:

```
Client → tools/call (name="calculate", args={"expression": "5+7"}) → Server
Server → "12" → Client
```

The registration is separate from the invocation.
You register once; you can invoke many times.

---

## 6. JSON-RPC Basics

MCP uses **JSON-RPC 2.0** as its message format.
You do not need to write JSON-RPC by hand — the MCP SDK handles it.
But understanding it helps you read logs and debug problems.

### A JSON-RPC request

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "calculate",
    "arguments": { "expression": "5 + 7" }
  }
}
```

| Field | Purpose |
|-------|---------|
| `jsonrpc` | Always `"2.0"` |
| `id` | A unique request ID — matched with the response |
| `method` | The operation to perform |
| `params` | Arguments for the operation |

### A JSON-RPC response

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{ "type": "text", "text": "12" }]
  }
}
```

The `id` in the response matches the request — this is how the client
knows which response belongs to which request.

---

## 7. Repository Structure

```
agentic-mcp-starter/
│
├── README.md              ← You are here
├── CONTRIBUTING.md        ← Contribution guide
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── LICENSE
├── .gitignore
├── .env.example           ← Copy to .env (optional)
├── pyproject.toml
├── requirements.txt
│
├── src/
│   └── starter/
│       ├── __init__.py
│       ├── config.py      ← Environment / configuration
│       ├── tools.py       ← Calculator tool (safe ast-based eval)
│       ├── resources.py   ← Static MCP resources
│       ├── prompts.py     ← Prompt templates
│       ├── server.py      ← MCP server entry point
│       ├── client.py      ← MCP client wrapper
│       └── agent.py       ← Basic agent loop
│
├── mocks/
│   ├── __init__.py
│   └── llm.py             ← Deterministic mock LLM (no API key needed)
│
├── examples/
│   ├── basic_server.py    ← Start the MCP server
│   ├── basic_client.py    ← Connect and discover tools/resources
│   ├── tool_call_demo.py  ← Step-by-step tool call demo
│   └── resource_demo.py   ← Resource discovery and retrieval demo
│
├── tests/
│   ├── test_config.py
│   ├── test_tools.py
│   ├── test_resources.py
│   ├── test_prompts.py
│   ├── test_mock_llm.py
│   └── test_agent.py
│
├── schemas/
│   └── tool.schema.json   ← JSON Schema for MCP tool definitions
│
└── docs/
    └── ISSUES.md          ← 5 contributor issues
```

---

## 8. Setup

### Step 1 — Clone the repository

```bash
git clone https://github.com/<org>/agentic-mcp-starter.git
cd agentic-mcp-starter
```

### Step 2 — Create a virtual environment

**Linux / macOS:**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell:**

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

> **Windows tip:** If you get a script execution error, run:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> Then try activating again.

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### Step 4 — Verify

```bash
python --version   # Should show Python 3.12.x
pytest --version
ruff --version
```

### Step 5 — (Optional) Configure environment

```bash
cp .env.example .env
```

The defaults in `.env.example` work without modification.
No API keys are required.

---

## 9. Run the Examples

All examples should be run from the repository root with the virtual environment active.

### basic_server.py — Start the MCP server

```bash
python examples/basic_server.py
```

The server starts and waits for a client.
Press **Ctrl+C** to stop it.

> In normal use you do not need to run the server manually — the client and agent start it automatically as a subprocess.

### basic_client.py — Connect and discover

```bash
python examples/basic_client.py
```

Expected output:

```
=== MCP Basic Client Demo ===

[Tools]
  - calculate: Evaluate a simple arithmetic expression …

[Resources]
  - workshop://introduction : Workshop Introduction
  - workshop://architecture : MCP Architecture Overview

[Tool call]  calculate('2 + 3')  →  5
```

### tool_call_demo.py — Step-by-step tool lifecycle

```bash
python examples/tool_call_demo.py
```

Shows the complete tool lifecycle: definition → discovery → invocation.

### resource_demo.py — Resource discovery and retrieval

```bash
python examples/resource_demo.py
```

Lists all resources and prints their content.

---

## 10. Run the Agent

The agent loop ties everything together.

```bash
python -c "
import asyncio, sys
sys.path.insert(0, 'src')
sys.path.insert(0, '.')
from starter.agent import Agent
async def main():
    agent = Agent()
    reply = await agent.run('calculate 5 + 7')
    print('Agent reply:', reply)
asyncio.run(main())
"
```

Expected output:

```
Agent reply: The result of 5 + 7 is 12.
```

### What happens step by step

```
User input: "calculate 5 + 7"
      ↓
Agent receives the message
      ↓
Mock LLM decides: use_tool=True, tool=calculate, args={"expression": "5 + 7"}
      ↓
MCP Client calls tools/call on the MCP Server
      ↓
MCP Server evaluates "5 + 7" → "12"
      ↓
Agent formats final reply: "The result of 5 + 7 is 12."
```

---

## 11. Run Tests

```bash
pytest -q
```

All tests should pass.  You should see output similar to:

```
.................................
33 passed in 0.42s
```

To see verbose output:

```bash
pytest -v
```

---

## 12. Run Ruff

```bash
ruff check .
```

No issues should be reported.

To auto-fix safe issues:

```bash
ruff check . --fix
```

---

## 13. Mock Mode

This repository is designed to work **entirely offline** without any API keys.

The default configuration (from `.env.example`) is:

```
LLM_PROVIDER=mock
MCP_MODE=local
```

### What "mock" means

- The **Mock LLM** (`mocks/llm.py`) uses keyword matching to decide which tool to call.
- It makes **no network requests**.
- It requires **no API keys**.
- It is **fully deterministic**: the same input always produces the same output.

This makes the workshop:

- Free to attend
- Reproducible
- Testable

When you are ready to use a real LLM, you can extend `src/starter/agent.py`
to call a real provider.  That is a separate workshop repository.

---

## 14. First Contribution

```
Find Issue        → docs/ISSUES.md lists 5 available issues
      ↓
Claim Issue       → Comment "I'd like to work on this"
      ↓
Create Branch     → git checkout -b feat/B01-description
      ↓
Implement         → Write code
      ↓
Write Tests       → Add tests in tests/
      ↓
Run CI Locally    → pytest -q && ruff check .
      ↓
Open PR           → Fill in the PR template
      ↓
Review            → Respond to maintainer comments
      ↓
Merge             → 🎉
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

---

## 15. Contributor Issues

See [`docs/ISSUES.md`](docs/ISSUES.md) for full details.

| ID | Title | Level |
|----|-------|-------|
| **B01** | Improve Tool Schema Validation | Beginner |
| **B02** | Add Calculator Edge-Case Tests | Beginner |
| **B03** | Add a New Static MCP Resource | Beginner |
| **I01** | Add a New MCP Resource Type | Intermediate |
| **I02** | Improve Mock LLM to MCP Tool Routing | Intermediate |

---

## 16. Troubleshooting

### Python version issues

```bash
python --version   # Must be 3.12.x
```

If you have an older Python, install Python 3.12 from [python.org](https://www.python.org/downloads/).

On Linux/macOS you can use `pyenv` to manage versions:

```bash
pyenv install 3.12.0
pyenv local 3.12.0
```

---

### Virtual environment activation fails (Windows)

Run this once in PowerShell:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate:

```powershell
.venv\Scripts\Activate.ps1
```

---

### `pytest` not found

Make sure your virtual environment is active and you installed dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

---

### `ModuleNotFoundError: No module named 'starter'`

Make sure you installed the package in editable mode:

```bash
pip install -e .
```

---

### Import errors for `mocks`

Run commands from the repository root so that the `mocks/` directory is on the Python path.

---

### Async/await issues

If you see `RuntimeError: no running event loop`, you need to use `asyncio.run()`:

```python
import asyncio
asyncio.run(my_async_function())
```

---

### Environment variable not read

Make sure `.env` exists (not just `.env.example`):

```bash
cp .env.example .env
```

---

### `ruff: command not found`

Install ruff:

```bash
pip install ruff
```

---

### MCP server won't start

Check that `mcp` is installed:

```bash
pip install mcp
```

Run:

```bash
python -c "import mcp; print(mcp.__version__)"
```

---

### Tests hanging or timing out

The agent tests use a fake MCP client by default so they do not start a subprocess.
If you have modified `tests/test_agent.py` to use the real client, revert that change.

---

## Workshop Learning Flow

```
1. Read this README
      ↓
2. Run setup
      ↓
3. Run examples
      ↓
4. Read source code: server.py → client.py → agent.py
      ↓
5. Run tests
      ↓
6. Pick a contributor issue
      ↓
7. Implement, test, submit PR
```

After completing this repository you will understand:

> "I know what MCP is, I understand the client/server architecture,
> and I know how an agent can discover and invoke an MCP tool."

Then you are ready for **Repo 2 — `mcp-tools-lab`** where you will build real MCP tools.

---

## License

MIT — see [LICENSE](LICENSE).
