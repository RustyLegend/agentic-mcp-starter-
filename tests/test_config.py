"""
tests/test_config.py

Tests for src/starter/config.py.
"""

from __future__ import annotations

import importlib


def test_default_llm_provider():
    """Without an env variable, LLM_PROVIDER defaults to 'mock'."""
    from starter.config import Config

    cfg = Config()
    assert cfg.llm_provider == "mock"


def test_default_mcp_mode():
    from starter.config import Config

    cfg = Config()
    assert cfg.mcp_mode == "local"


def test_env_override(monkeypatch):
    """Environment variables override the defaults."""
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("MCP_MODE", "remote")

    # Force a fresh Config so it reads the patched env
    from starter import config as config_module

    importlib.reload(config_module)
    cfg = config_module.Config()
    assert cfg.llm_provider == "openai"
    assert cfg.mcp_mode == "remote"

    # Reload to restore defaults after test
    importlib.reload(config_module)


def test_shared_config_instance():
    """The module-level config singleton is a Config instance."""
    from starter.config import Config, config

    assert isinstance(config, Config)
