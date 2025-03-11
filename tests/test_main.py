"""Tests for the Calculator REPL system."""

from decimal import Decimal
import sys
import subprocess
import pytest
from unittest.mock import patch
from main import CalculatorREPL
from history.history import History
from operations.operation_base import Operation

@pytest.fixture(autouse=True)
def reset_history():
    """Ensures history is cleared before each test."""
    History.clear_history()


@pytest.fixture(autouse=True)
def mock_operations():
    """Mock some operations for testing."""
    class MockAdd(Operation):
        """Mock addition operation."""
        @classmethod
        def execute(cls, a, b):
            return a + b

    class MockDivide(Operation):
        """Mock division operation with zero handling."""
        @classmethod
        def execute(cls, a, b):
            if b == 0:
                raise ZeroDivisionError
            return a / b

    Operation.registry = {"add": MockAdd, "divide": MockDivide}


@pytest.mark.parametrize("operation, a, b, expected", [
    ("add", Decimal("2"), Decimal("3"), Decimal("5")),
    ("add", Decimal("-1"), Decimal("4"), Decimal("3")),
    ("divide", Decimal("10"), Decimal("2"), Decimal("5")),
])
def test_run_operation_valid(operation, a, b, expected):
    """Tests valid arithmetic operations."""
    result = CalculatorREPL.run_operation(operation, a, b)
    assert result == expected


def test_run_operation_invalid():
    """Tests handling of unknown operations."""
    result = CalculatorREPL.run_operation("unknown", Decimal("2"), Decimal("3"))
    assert result == "Operation 'unknown' not found."


def test_run_operation_divide_by_zero():
    """Tests division by zero handling."""
    result = CalculatorREPL.run_operation("divide", Decimal("5"), Decimal("0"))
    assert result == "Error: Division by zero is not allowed."


def test_repl_menu_command():
    """Tests that the 'menu' command is executed correctly."""
    with patch("builtins.input", side_effect=["menu", "5", "exit"]), patch("builtins.print") as mock_print:
        CalculatorREPL.repl()

    mock_print.assert_any_call("\n== Welcome to REPL Calculator ==")


def test_repl_history_command():
    """Tests that the 'history' command displays history."""
    History.add_entry("add", 2, 3, 5)

    with patch("builtins.input", side_effect=["menu", "2", "5", "exit"]), patch("builtins.print") as mock_print:
        CalculatorREPL.repl()

    printed_output = [call.args[0] for call in mock_print.call_args_list]

    assert any("add 2 3 = 5" in line for line in printed_output), "Expected history output missing"


def test_repl_last_command():
    """Tests that the 'last' command displays last calculation."""
    History.add_entry("multiply", 4, 5, 20)

    with patch("builtins.input", side_effect=["last", "exit"]), patch("builtins.print") as mock_print:
        CalculatorREPL.repl()

    mock_print.assert_any_call("multiply 4 5 = 20")


def test_repl_clear_command():
    """Tests that the 'clear' command clears history."""
    History.add_entry("subtract", 8, 3, 5)

    with patch("builtins.input", side_effect=["clear", "exit"]), patch("builtins.print") as mock_print:
        CalculatorREPL.repl()

    mock_print.assert_any_call("History cleared.")


def test_repl_invalid_command():
    """Tests handling of invalid commands."""
    with patch("builtins.input", side_effect=["invalid_command", "exit"]), patch("builtins.print") as mock_print:
        CalculatorREPL.repl()

    mock_print.assert_any_call("Error: Invalid format! Use: <operation> <number1> <number2>")


def test_repl_valid_operation():
    """Tests execution of a valid arithmetic operation."""
    with patch("builtins.input", side_effect=["add 5 3", "exit"]), patch("builtins.print") as mock_print:
        CalculatorREPL.repl()

    mock_print.assert_any_call("Result: 8")


def test_repl_invalid_number_format():
    """Tests handling of invalid number format."""
    with patch("builtins.input", side_effect=["add five 3", "exit"]), patch("builtins.print") as mock_print:
        CalculatorREPL.repl()

    mock_print.assert_any_call("Error: Invalid number format! Ensure you're using numeric values.")

def test_repl_unexpected_error():
    """Tests REPL handling of unexpected errors."""
    with patch("builtins.input", side_effect=["add 2 3", "exit"]), \
         patch("builtins.print") as mock_print, \
         patch.object(CalculatorREPL, "run_operation", side_effect=Exception("Unexpected failure")):

        CalculatorREPL.repl()

    mock_print.assert_any_call("Unexpected error: Unexpected failure")

def test_main_entrypoint():
    """Tests if running main.py executes CalculatorREPL.repl()."""

    with subprocess.Popen(
        [sys.executable, "main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    ) as process:

        stdout, stderr = process.communicate(input="exit\n")

    # ✅ Print the captured output for debugging
    print("\n🚀 STDOUT Output:\n", stdout)
    print("\n❌ STDERR Output:\n", stderr)

    assert "== Welcome to REPL Calculator ==" in stdout, "REPL did not start correctly!"
    assert process.returncode == 0, f"Calculator script exited with error: {stderr}"
