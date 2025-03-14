# ✅ Standard Library Imports
import runpy
import re  # ✅ Added regex for robust error message checking
from decimal import Decimal
from unittest.mock import patch

# ✅ Third-Party Imports
import pytest

# ✅ Local Imports
from config import plugins
from main import CalculatorREPL
from history.history import History

@pytest.fixture(scope="session", autouse=True)
def load_plugins():
    """Ensure plugins are loaded before running tests."""
    plugins.load_plugins()


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Ensure a clean history before and after each test."""
    History.clear_history()
    yield
    History.clear_history()


def test_run_operation_valid():
    """Test valid calculator operations."""
    assert "add" in CalculatorREPL.get_available_operations(), "⚠️ 'add' operation should be loaded"

    result = CalculatorREPL.run_operation("add", Decimal("2"), Decimal("3"))
    assert result == Decimal("5"), "⚠️ Expected 5"


def test_run_operation_invalid():
    """Test invalid operation handling."""
    result = CalculatorREPL.run_operation("nonexistent", Decimal("2"), Decimal("3"))
    assert re.search(r"not\s*found", result, re.IGNORECASE), "⚠️ Expected error message indicating operation was not found"


def test_run_operation_divide_by_zero():
    """Test division by zero handling."""
    assert "divide" in CalculatorREPL.get_available_operations(), "⚠️ 'divide' operation should be loaded"

    result = CalculatorREPL.run_operation("divide", Decimal("10"), Decimal("0"))
    assert re.search(r"division\s*by\s*zero", result, re.IGNORECASE), "⚠️ Expected division by zero error"


@patch("builtins.input", side_effect=["exit"])
def test_main_entrypoint(mock_input, capfd):
    """Tests if running main.py executes CalculatorREPL.repl()."""
    try:
        runpy.run_path("main.py", run_name="__main__")
    except SystemExit:
        pass  # ✅ Handle `sys.exit()` without patching

    captured = capfd.readouterr()
    assert "== Welcome to REPL Calculator ==" in captured.out


@patch("builtins.input", side_effect=["menu", "exit"])
@patch("app.menu.Menu.show_menu")
def test_repl_menu_command(mock_menu, mock_input, capfd):
    """Test entering 'menu' in the REPL calls the menu."""
    try:
        CalculatorREPL.repl()
    except SystemExit:
        pass

    mock_menu.assert_called_once()
    captured = capfd.readouterr()
    assert "== Welcome to REPL Calculator ==" in captured.out


@patch("builtins.input", side_effect=["add 2 3", "exit"])
def test_repl_addition(mock_input, capfd):
    """Test entering an addition command in REPL."""
    assert "add" in CalculatorREPL.get_available_operations(), "⚠️ 'add' operation should be loaded before starting REPL"

    try:
        CalculatorREPL.repl()
    except SystemExit:
        pass  # ✅ Avoid breaking test

    captured = capfd.readouterr()
    assert "Result: 5" in captured.out, "⚠️ Expected output 'Result: 5'"
