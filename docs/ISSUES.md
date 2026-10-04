# Contributor Issues

This document describes the **5 contributor issues** available in this repository.
Each issue is designed as a learning step in the MCP workshop.

---

## Issue B01 — Add MCP Client Tests

**Label:** `tier:beginner` · `area:mcp` · `good-first-issue`

### Title

```
[B01] Add MCP Client Tests
```

### Goal

Learn how an MCP client connects to a server, discovers capabilities, and invokes a tool.

### Context

src/starter/client.py contains the basic MCP client used by the starter agent.
The existing implementation should have tests covering its important behaviors. This issue adds beginner-friendly test coverage without changing the client architecture

### Expected work

Add tests that verify:
1. The client can initialize/connect to the local MCP server.
2. The client can discover the calculate tool.
3. The client can invoke the calculate tool.
4. A valid calculation returns the expected result.
5. The client can retrieve/read a registered MCP resource.
Use mocks/fakes where appropriate so the tests remain deterministic and do not require external services.
### Do not:

- redesign the MCP client
- add new production tools
- add SQLite
- add external APIs
- add RAG/vector databases
- introduce a real LLM

### Learning outcome

```
MCP Client
    ↓
Connect
    ↓
Discover
    ↓
Invoke / Read
    ↓
Verify Result
```

### Branch naming

```
test/B01-mcp-client-tests
```

---

## Issue B02 — Add Calculator Edge-Case Tests

**Label:** `tier:beginner` · `area:mcp` · `good-first-issue`

### Title

```
[B02] Add Calculator Edge-Case Tests
```

### Goal

Learn how to test an MCP tool thoroughly.

### Context

`tests/test_tools.py` has a basic test suite for `safe_calculate()`.
This issue adds more edge-case coverage.

### Expected work

Add tests for:

| Input | Expected behaviour |
|-------|-------------------|
| `"2 + 3"` | `"5"` |
| `"10 * 5"` | `"50"` |
| `"(10 + 5) / 3"` | `"5"` |
| `"1 / 0"` | raises `ValueError` (division by zero) |
| `""` | raises `ValueError` (empty) |
| `"abc"` | raises `ValueError` (unsafe) |
| `"__import__('os')"` | raises `ValueError` (unsafe) |
| `"2 ** 32"` | large-number result |

Do **not** redesign the calculator — the task is purely testing.

### Branch naming

```
test/B02-calculator-edge-cases
```

---

## Issue B03 — Add a New Static MCP Resource

**Label:** `tier:beginner` · `area:resources` · `good-first-issue`

### Title

```
[B03] Add a New Static MCP Resource
```

### Goal

Learn how MCP resources are defined, registered, and retrieved.

### Context

`src/starter/resources.py` contains two resources:
- `workshop://introduction`
- `workshop://architecture`

### Expected work

1. Add a new resource, for example:

   ```
   workshop://getting-started
   ```

   It should contain a short guide explaining the setup steps or
   the learning flow for participants.

2. Register it in `RESOURCES` in `resources.py`.
3. Add tests in `tests/test_resources.py`:
   - The new URI is returned by `list_resources()`.
   - `read_resource("workshop://getting-started")` returns a non-empty string.
4. Update `README.md` if needed.

### Branch naming

```
feat/B03-new-static-resource
```

---

## Issue I01 — Add a Markdown MCP Resource

**Label:** `tier:intermediate` · `area:resources`

### Title

```
[I01] Add a Markdown MCP Resource
```

### Goal

Gain deeper practice with MCP resource handling.

### Context

Current resources are all of type `text/plain`.
This issue adds another deterministic resource with richer content,
such as a structured MIME type (e.g. `text/markdown` or `application/json`).

Example URIs to consider:

```
workshop://contributing
workshop://troubleshooting
workshop://json-rpc-primer
```

### Expected work

1. Add a new resource entry to `RESOURCES` in `resources.py`.
2. The resource content must be **local and deterministic** — no external API calls.
3. Use a different `mimeType` than `text/plain` (e.g. `text/markdown`).
4. Add tests covering:
   - The resource appears in `list_resources()`.
   - `read_resource()` returns its content.
   - The content is a non-empty string.
5. Update documentation if needed.

### Branch naming

```
feat/I01-new-resource-type
```

---

## Issue I02 — Improve Mock LLM to MCP Tool Routing

**Label:** `tier:intermediate` · `area:agent`

### Title

```
[I02] Improve Mock LLM to MCP Tool Routing
```

### Goal

Understand how an agent decides to call an MCP tool.

### Context

`mocks/llm.py` uses simple keyword matching to route messages to the
`calculate` tool.  The routing can be made more robust.

### Expected work

1. Extend `MockLLM._is_calculation_request()` and `_extract_expression()`
   to handle more phrasings, for example:
   - `"what is the result of 8 ** 2"` → `calculate("8 ** 2")`
   - `"please compute 100 / 4"` → `calculate("100 / 4")`
   - `"add 3 and 7"` → `calculate("3 + 7")`

2. Add tests in `tests/test_mock_llm.py` that assert each new phrasing
   routes correctly.

3. **Do not** introduce a real LLM or make any network requests.
4. **Do not** use complex NLP libraries — keep it regex / keyword based.

### Branch naming

```
feat/I02-improved-llm-routing
```

---

## Quick Reference

| ID | Title | Level | Area |
|----|-------|-------|------|
| B01 | Improve Tool Schema Validation | Beginner | MCP |
| B02 | Add Calculator Edge-Case Tests | Beginner | Testing |
| B03 | Add a New Static MCP Resource | Beginner | Resources |
| I01 | Add a New MCP Resource Type | Intermediate | Resources |
| I02 | Improve Mock LLM to MCP Tool Routing | Intermediate | Agent |
