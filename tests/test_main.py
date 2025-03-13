"""Tests for the Calculator REPL system."""
import pytest
import sys
import runpy
from decimal import Decimal
from unittest.mock import patch, MagicMock
from main import CalculatorREPL
from history.history import History
from operations.addition import Add

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Ensure a clean history before and after each test."""
    History.clear_history()
    yield
    History.clear_history()

@patch("builtins.input", side_effect=["exit"])
def test_main_entrypoint(mock_input, capfd):
    """Tests if running main.py executes CalculatorREPL.repl()."""
    with patch("sys.exit") as mock_exit:
        runpy.run_path("main.py", run_name="__main__")

    captured = capfd.readouterr()
    assert "== Welcome to REPL Calculator ==" in captured.out
    mock_exit.assert_called_once()

def test_run_operation_valid():
    """Test valid calculator operations."""
    from config import plugins  # ✅ Ensure plugin system is loaded
    plugins.load_plugins()  # ✅ Load operation plugins before testing
    
    result = CalculatorREPL.run_operation("add", Decimal("2"), Decimal("3"))
    assert result == Decimal("5"), "⚠️ Expected 5"


def test_run_operation_invalid():
    """Test invalid operation handling."""
    result = CalculatorREPL.run_operation("nonexistent", Decimal("2"), Decimal("3"))
    assert "not found" in result.lower(), "⚠️ Expected error message"

def test_run_operation_divide_by_zero():
    """Test division by zero handling."""
    result = CalculatorREPL.run_operation("divide", Decimal("10"), Decimal("0"))
    assert "division by zero" in result.lower(), "⚠️ Expected division by zero error"

@patch("builtins.input", side_effect=["menu", "exit"])
@patch("app.menu.Menu.run")
def test_repl_menu_command(mock_menu, mock_input, capfd):
    """Test entering 'menu' in the REPL calls the menu."""
    with patch("sys.exit") as mock_exit:
        CalculatorREPL.repl()
    
    mock_menu.assert_called_once()
    captured = capfd.readouterr()
    assert "== Welcome to REPL Calculator ==" in captured.out
    mock_exit.assert_called_once()

@patch("builtins.input", side_effect=["add 2 3", "exit"])
def test_repl_addition(mock_input, capfd):
    """Test entering an addition command in REPL."""
    with patch("sys.exit") as mock_exit:
        CalculatorREPL.repl()

    captured = capfd.readouterr()
    assert "Result: 5" in captured.out, "⚠️ Expected output 'Result: 5'"
    mock_exit.assert_called_once()
