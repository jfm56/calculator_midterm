"""
Unit tests for main.py - Calculator REPL.
"""

import pytest
from unittest.mock import patch
from decimal import Decimal
from main import CalculatorREPL
from history.history import History


@pytest.fixture
def mock_logger():
    """Mock the logger to avoid real logging during tests."""
    with patch("main.logger") as mock_log:
        yield mock_log


@pytest.fixture
def mock_history():
    """Mock the history module to prevent real file writes."""
    with patch.object(History, "add_entry") as mock_add_entry:
        yield mock_add_entry


def test_run_operation_valid(mock_logger):
    """Test run_operation() with valid operations."""
    assert CalculatorREPL.run_operation("add", 2, 3) == Decimal(5)
    assert CalculatorREPL.run_operation("subtract", 10, 3) == Decimal(7)
    assert CalculatorREPL.run_operation("multiply", 4, 2) == Decimal(8)
    assert CalculatorREPL.run_operation("divide", 8, 2) == Decimal(4)


def test_run_operation_invalid(mock_logger):
    """Ensure run_operation() raises KeyError for unknown operations."""
    with pytest.raises(KeyError, match="⚠️ Operation 'unknown' not found."):
        CalculatorREPL.run_operation("unknown", 2, 3)


def test_run_operation_divide_by_zero(mock_logger):
    """Ensure ZeroDivisionError is raised when dividing by zero."""
    with pytest.raises(ZeroDivisionError, match="❌ Division by zero is not allowed."):
        CalculatorREPL.run_operation("divide", 10, 0)


def test_process_calculation_valid(mock_logger, mock_history):
    """Test process_calculation() with a valid command."""
    with patch("builtins.print") as mock_print:
        CalculatorREPL.process_calculation("add 5 3")
        mock_print.assert_called_with("✅ Result: 8")


def test_process_calculation_invalid_format(mock_logger):
    """Ensure process_calculation() handles invalid input formats."""
    with patch("builtins.print") as mock_print:
        CalculatorREPL.process_calculation("add 5")  # Missing second number
        mock_print.assert_called_with("❌ Error: ⚠️ Invalid format. Expected: operation num1 num2")


def test_process_calculation_unknown_operation(mock_logger):
    """Ensure process_calculation() rejects unknown operations."""
    with patch("builtins.print") as mock_print:
        CalculatorREPL.process_calculation("mod 4 2")  # Unknown operation
        mock_print.assert_called_with("❌ Unknown operation: 'mod'. Type 'menu' for options.")


def test_get_available_operations():
    """Ensure get_available_operations() returns the correct operations."""
    available_ops = CalculatorREPL.get_available_operations()
    assert "add" in available_ops
    assert "subtract" in available_ops
    assert "multiply" in available_ops
    assert "divide" in available_ops


@patch("builtins.input", side_effect=["menu", "exit"])
@patch("builtins.print")
def test_start_repl(mock_print, mock_input, mock_logger):
    """Test REPL start function with mocked user input."""
    with patch.object(CalculatorREPL, "process_calculation") as mock_process:
        CalculatorREPL.start()
        mock_print.assert_any_call("👋 Exiting calculator. Goodbye!")
        mock_process.assert_not_called()  # Since no calculations were attempted


@patch("builtins.input", side_effect=["add 2 3", "exit"])
@patch("builtins.print")
def test_start_repl_with_calculation(mock_print, mock_input, mock_logger):
    """Test REPL start function with a calculation command."""
    with patch.object(CalculatorREPL, "process_calculation") as mock_process:
        CalculatorREPL.start()
        mock_process.assert_called_with("add 2 3")
        mock_print.assert_any_call("👋 Exiting calculator. Goodbye!")

@patch("builtins.input", side_effect=["exit"])
@patch("builtins.print")
def test_repl_exit(mock_print, mock_input):
    """Ensure REPL exits correctly when 'exit' is entered."""
    CalculatorREPL.repl()
    mock_print.assert_any_call("\n✨ Welcome to the Interactive Calculator! ✨")
    mock_print.assert_any_call("👋 Exiting calculator. Goodbye!")


@patch("builtins.input", side_effect=["menu", "exit"])
@patch("builtins.print")
def test_repl_menu(mock_print, mock_input):
    """Ensure REPL correctly calls the menu when 'menu' is entered."""
    with patch("app.menu.Menu.show_menu") as mock_menu:
        CalculatorREPL.repl()
        mock_menu.assert_called_once()
        mock_print.assert_any_call("\n✨ Welcome to the Interactive Calculator! ✨")


@patch("builtins.input", side_effect=["add 2 3", "exit"])
@patch("builtins.print")
def test_repl_process_calculation(mock_print, mock_input):
    """Ensure REPL correctly processes arithmetic commands."""
    with patch.object(CalculatorREPL, "process_calculation") as mock_process:
        CalculatorREPL.repl()
        mock_process.assert_called_with("add 2 3")
        mock_print.assert_any_call("\n✨ Welcome to the Interactive Calculator! ✨")


@patch("builtins.input", side_effect=["invalid command", "exit"])
@patch("builtins.print")
def test_repl_invalid_command(mock_print, mock_input):
    """Ensure REPL correctly processes an invalid command."""
    with patch.object(CalculatorREPL, "process_calculation") as mock_process:
        CalculatorREPL.repl()
        mock_process.assert_called_with("invalid command")
        mock_print.assert_any_call("\n✨ Welcome to the Interactive Calculator! ✨")


@patch("builtins.input", side_effect=["exit"])
@patch("builtins.print")
def test_repl_welcome_message(mock_print, mock_input):
    """Ensure REPL prints the welcome message."""
    CalculatorREPL.repl()
    mock_print.assert_any_call("\n✨ Welcome to the Interactive Calculator! ✨")

@patch("main.logger")
def test_run_operation_unexpected_error(mock_logger):
    """Test unexpected error handling in run_operation."""
    with pytest.raises(RuntimeError, match="Unexpected error"):
        with patch("operations.operation_base.Operation.get_operation", side_effect=RuntimeError("Unexpected error")):
            CalculatorREPL.run_operation("add", 2, 3)

    mock_logger.error.assert_any_call("❌ Error during operation 'add': Unexpected error")

@patch("app.menu.Menu.handle_choice")
@patch("builtins.input", side_effect=["1", "exit"])  # Simulating user choosing option 1 and then exiting
@patch("main.logger")
def test_menu_handle_choice(mock_logger, mock_input, mock_handle_choice):
    """Test that Menu.handle_choice is correctly called when user enters a valid menu option."""

    # Run REPL loop (this will process "1" and "exit")
    CalculatorREPL.start()

    # Verify that Menu.handle_choice was called with "1"
    mock_handle_choice.assert_called_with("1")
