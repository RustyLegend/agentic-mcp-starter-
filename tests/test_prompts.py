"""
tests/test_prompts.py

Tests for src/starter/prompts.py.
"""

from __future__ import annotations

from starter.prompts import (
    FINAL_RESPONSE_PROMPT,
    SYSTEM_PROMPT,
    TOOL_SELECTION_PROMPT,
    build_final_response_prompt,
    build_tool_selection_prompt,
)


class TestSystemPrompt:
    def test_is_string(self):
        assert isinstance(SYSTEM_PROMPT, str)

    def test_mentions_calculate_tool(self):
        assert "calculate" in SYSTEM_PROMPT.lower()

    def test_non_empty(self):
        assert len(SYSTEM_PROMPT.strip()) > 0


class TestToolSelectionPrompt:
    def test_template_has_placeholder(self):
        assert "{user_message}" in TOOL_SELECTION_PROMPT

    def test_build_inserts_message(self):
        prompt = build_tool_selection_prompt("5 + 7")
        assert "5 + 7" in prompt
        assert "{user_message}" not in prompt

    def test_build_mentions_tool(self):
        prompt = build_tool_selection_prompt("calculate something")
        assert "calculate" in prompt.lower()


class TestFinalResponsePrompt:
    def test_template_has_placeholders(self):
        assert "{user_message}" in FINAL_RESPONSE_PROMPT
        assert "{tool_result}" in FINAL_RESPONSE_PROMPT

    def test_build_inserts_values(self):
        prompt = build_final_response_prompt("5 + 7", "12")
        assert "5 + 7" in prompt
        assert "12" in prompt
        assert "{user_message}" not in prompt
        assert "{tool_result}" not in prompt
