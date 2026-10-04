# Contributing to agentic-mcp-starter

Thank you for joining the Agentic AI Open-Source Workshop!
This guide explains everything you need to know to make your first contribution.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Fork and Clone](#fork-and-clone)
3. [Set Up Locally](#set-up-locally)
4. [Pick an Issue](#pick-an-issue)
5. [Create a Branch](#create-a-branch)
6. [Make Your Changes](#make-your-changes)
7. [Add Tests](#add-tests)
8. [Run CI Locally](#run-ci-locally)
9. [Open a Pull Request](#open-a-pull-request)
10. [Review Process](#review-process)
11. [Contributor Boundaries](#contributor-boundaries)
12. [Labels](#labels)

---

## Prerequisites

- Python 3.12
- Git
- A GitHub account

---

## Fork and Clone

1. Click **Fork** on the top-right of the repository page.
2. Clone your fork:

```bash
git clone https://github.com/<your-username>/agentic-mcp-starter.git
cd agentic-mcp-starter
```

3. Add the upstream remote:

```bash
git remote add upstream https://github.com/<org>/agentic-mcp-starter.git
```

---

## Set Up Locally

**Linux / macOS:**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

**Windows PowerShell:**

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

Verify:

```bash
python --version   # Python 3.12.x
pytest --version
ruff --version
```

---

## Pick an Issue

Browse the open issues and look for one tagged:

```
good-first-issue
tier:beginner
tier:intermediate
```

Comment: **"I'd like to work on this"** before you start so maintainers can assign it to you.

Available issues are documented in [`docs/ISSUES.md`](docs/ISSUES.md).

---

## Create a Branch

Always branch off `main`:

```bash
git checkout main
git pull upstream main
git checkout -b feat/issue-123-description
```

Branch naming conventions:

| Type | Pattern |
|------|---------|
| Feature | `feat/issue-123-description` |
| Bug fix | `fix/issue-123-description` |
| Docs | `docs/issue-123-description` |
| Tests | `test/issue-123-description` |

---

## Make Your Changes

Keep changes focused on your assigned issue.

Generally, avoid modifying:

- `client.py`, `agent.py`, `config.py` — unless your issue specifically requires it
- `.github/workflows/` — CI is maintained by maintainers
- `.github/CODEOWNERS` — ownership is managed by maintainers

---

## Add Tests

> Every code change must include tests.

Put tests in `tests/` following the existing pattern.

Run the full test suite before opening a PR:

```bash
pytest -q
```

All tests must pass.

---

## Run CI Locally

```bash
# Lint
ruff check .

# Tests
pytest -q
```

Both must pass before opening a PR.

---

## Open a Pull Request

1. Push your branch:

```bash
git push origin feat/issue-123-description
```

2. Go to your fork on GitHub and click **New Pull Request**.
3. Fill in the PR template (What changed? Related issue? Tests?).
4. Ensure CI passes (GitHub Actions will run automatically).

---

## Review Process

A maintainer will review your PR and may:

- Approve and merge it ✅
- Request changes with comments

Please respond to review comments promptly.

---

## Contributor Boundaries

To keep the repository simple and beginner-friendly, **please do not add**:

- New LLM providers or API integrations
- Vector databases, RAG pipelines, or multi-agent frameworks
- External database connectors
- Web search, weather, or GitHub API tools
- Additional tools beyond the calculator (those belong in Repo 2)

If you think something should be added, open a discussion issue first.

---

## Labels

| Label | Meaning |
|-------|---------|
| `tier:beginner` | Suitable for first-time contributors |
| `tier:intermediate` | Requires some Python / MCP familiarity |
| `area:mcp` | Changes to MCP server/client code |
| `area:resources` | Changes to MCP resources |
| `area:agent` | Changes to the agent loop |
| `good-first-issue` | Great starting point |
| `hacktoberfest` | Eligible for Hacktoberfest |
