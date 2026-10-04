# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this repository, **please do not open a public issue**.

Instead, email the maintainers directly (replace with actual contact):

```
security@example.com
```

Please include:

- A description of the vulnerability
- Steps to reproduce
- Potential impact

We will acknowledge your report within 48 hours and aim to resolve confirmed vulnerabilities within 7 days.

## Scope

This repository is a **workshop starter kit** intended for local, educational use.
It is **not** designed for production deployment.

Common security considerations:

- **No secrets committed**: `.env` is in `.gitignore`. Never commit API keys.
- **No `eval()`**: The calculator uses `ast.parse()` to safely evaluate expressions.
- **No network access**: The mock mode makes no external requests.
- **No authentication**: This is a local demo — do not expose it on a public network.

## Supported Versions

| Version | Supported |
|---------|-----------|
| `main` | ✅ |
| All others | ❌ |
