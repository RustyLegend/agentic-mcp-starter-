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


# ──────────────────────────────────────────────────────────────────────────────
# Issue B03 — workshop://getting-started
# ──────────────────────────────────────────────────────────────────────────────
GETTING_STARTED_URI = "workshop://getting-started"


class TestGettingStartedResource:
    def test_uri_is_returned_by_list_resources(self):
        uris = [r["uri"] for r in list_resources()]
        assert GETTING_STARTED_URI in uris

    def test_read_returns_non_empty_string(self):
        content = read_resource(GETTING_STARTED_URI)
        assert isinstance(content, str)
        assert content.strip() != ""

    def test_listed_metadata_is_complete(self):
        (entry,) = [r for r in list_resources() if r["uri"] == GETTING_STARTED_URI]
        assert entry["name"].strip() != ""
        assert entry["description"].strip() != ""
        assert entry["mimeType"] == "text/plain"

    def test_guide_covers_setup_and_learning_flow(self):
        content = read_resource(GETTING_STARTED_URI)
        # Setup: environment creation and installation.
        assert "venv" in content
        assert "pip install" in content
        # Verification commands that CONTRIBUTING.md asks for.
        assert "pytest" in content
        assert "ruff" in content

    def test_existing_resources_are_unaffected(self):
        uris = [r["uri"] for r in list_resources()]
        assert "workshop://introduction" in uris
        assert "workshop://architecture" in uris


class TestRegistryConsistency:
    """server.py registers resources using both the dict key and its fields,
    so a typo that makes them disagree would only show up at runtime."""

    @pytest.mark.parametrize("uri", list(RESOURCES))
    def test_key_matches_embedded_uri(self, uri):
        assert RESOURCES[uri]["uri"] == uri

    @pytest.mark.parametrize("uri", list(RESOURCES))
    def test_required_fields_present_and_non_empty(self, uri):
        for field in ("uri", "name", "description", "mimeType", "content"):
            assert RESOURCES[uri][field].strip() != "", f"{uri}: empty {field!r}"
