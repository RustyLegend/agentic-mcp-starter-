"""
src/starter/config.py

Configuration loader for agentic-mcp-starter.

Environment variables are read from a .env file (if present) or from
the actual environment. Defaults are provided so the repository works
out-of-the-box without any .env file.

Usage
-----
    from starter.config import config
    print(config.llm_provider)  # "mock"
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

# Load .env if it exists — silently ignored when it does not.
load_dotenv(override=False)


@dataclass
class Config:
    """Application-level configuration.

    All values default to the mock/local settings so the workshop
    works without any API keys or external services.
    """

    llm_provider: str = field(default_factory=lambda: os.getenv("LLM_PROVIDER", "mock"))
    mcp_mode: str = field(default_factory=lambda: os.getenv("MCP_MODE", "local"))
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))


# Single shared instance — import this wherever you need configuration.
config = Config()
