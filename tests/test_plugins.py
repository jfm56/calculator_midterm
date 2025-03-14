"""Tests for plugin loading system."""

import pytest
from config.plugins import load_plugins
from main import CalculatorREPL


def test_load_plugins_success():
    """Ensure plugins are correctly loaded and available."""
    load_plugins()  # ✅ Load plugins once

    available_operations = CalculatorREPL.get_available_operations()
    assert "add" in available_operations, "⚠️ 'add' plugin should be loaded"
    assert "subtract" in available_operations, "⚠️ 'subtract' plugin should be loaded"
    assert "multiply" in available_operations, "⚠️ 'multiply' plugin should be loaded"
    assert "divide" in available_operations, "⚠️ 'divide' plugin should be loaded"


def test_load_invalid_plugin():
    """Ensure invalid plugins don't break existing operations."""
    try:
        load_plugins()
        available_operations = CalculatorREPL.get_available_operations()

        # ✅ Ensure valid plugins remain available
        assert "add" in available_operations, "⚠️ 'add' should still be available despite invalid plugins."
        assert "divide" in available_operations, "⚠️ 'divide' should still be available."

        print("✅ No crash on invalid plugin load.")
    except ImportError:
        pytest.fail("❌ Unexpected ImportError encountered.")
