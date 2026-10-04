"""
tests/test_resources.py

Tests for src/starter/resources.py.
"""

from __future__ import annotations

import pytest

from starter.resources import RESOURCES, list_resources, read_resource


class TestListResources:
    def test_returns_list(self):
        result = list_resources()
        assert isinstance(result, list)

    def test_at_least_two_resources(self):
        assert len(list_resources()) >= 2

    def test_uri_in_each_resource(self):
        for r in list_resources():
            assert "uri" in r

    def test_no_content_in_list(self):
        """Content should NOT be returned by list— only metadata."""
        for r in list_resources():
            assert "content" not in r

    def test_introduction_resource_listed(self):
        uris = [r["uri"] for r in list_resources()]
        assert "workshop://introduction" in uris

    def test_architecture_resource_listed(self):
        uris = [r["uri"] for r in list_resources()]
        assert "workshop://architecture" in uris


class TestReadResource:
    def test_read_introduction(self):
        content = read_resource("workshop://introduction")
        assert "Welcome" in content
        assert "MCP" in content

    def test_read_architecture(self):
        content = read_resource("workshop://architecture")
        assert "Agent" in content
        assert "MCP" in content

    def test_unknown_uri_raises(self):
        with pytest.raises(KeyError, match="Unknown resource"):
            read_resource("workshop://does-not-exist")

    def test_content_is_string(self):
        content = read_resource("workshop://introduction")
        assert isinstance(content, str)
        assert len(content) > 0

    def test_all_registered_resources_readable(self):
        """Every URI in RESOURCES should be readable without error."""
        for uri in RESOURCES:
            content = read_resource(uri)
            assert isinstance(content, str)
