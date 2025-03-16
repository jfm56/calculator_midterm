"""
Unit tests for the main interactive calculator (REPL).
"""

from decimal import Decimal, ROUND_HALF_UP
from unittest.mock import patch
import pandas as pd
import pytest
from app.menu import Menu
from history.history import History
from main import CalculatorREPL


@pytest.mark.parametrize("command, expected_output", [
    ("add 2 3", "✅ Result: 5"),
    ("subtract 10 4", "✅ Result: 6"),
    ("multiply 3 3", "✅ Result: 9"),
    ("divide 8 2", "✅ Result: 4"),
    ("mean 10 20 30", "✅ Result: 20"),
    ("median 3 1 2", "✅ Result: 2"),
    ("std_dev 4 4 4 4", "✅ Result: 0.0"),
    ("variance 2 4 6 8", "✅ Result: 6.67"),
])
@patch("builtins.print")
def test_process_calculation_valid(mock_print, command, expected_output):
    """Test valid arithmetic and statistical calculations."""
    CalculatorREPL.process_calculation(command)

    for call in mock_print.call_args_list:
        actual_output = call.args[0].strip()
        if "Result:" in actual_output:
            result_value = actual_output.split("✅ Result: ")[1]
            rounded_result = str(Decimal(result_value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)).rstrip("0").rstrip(".")
            expected_value = str(Decimal(expected_output.split("✅ Result: ")[1]).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)).rstrip("0").rstrip(".")
            assert rounded_result == expected_value, f"Expected {expected_value}, but got {rounded_result}"
            return

    pytest.fail(f"Expected result '{expected_output}' not found in output.")


@patch("builtins.print")
def test_process_calculation_divide_by_zero(mock_print):
    """Ensure division by zero is properly handled."""
    CalculatorREPL.process_calculation("divide 10 0")
    mock_print.assert_any_call("❌ Division by zero is not allowed.")


@patch("builtins.print")
def test_process_calculation_invalid(mock_print):
    """Ensure invalid commands are handled properly."""
    CalculatorREPL.process_calculation("invalid_command")
    mock_print.assert_any_call("❌ Unknown operation: 'invalid_command'. Type 'menu' for options.")


@patch("builtins.print")
@patch("builtins.input", side_effect=["exit"])
@patch("sys.exit", autospec=True)  # Mock sys.exit() to prevent actual exit
def test_repl_exit(mock_exit, mock_input, mock_print):
    """Ensure REPL exits when 'exit' command is entered."""
    CalculatorREPL.start()

    mock_print.assert_any_call("👋 Exiting calculator.")
    mock_exit.assert_called_once()

@patch("builtins.print")
def test_repl_welcome_message(mock_print):
    """Ensure REPL displays the welcome message."""
    CalculatorREPL.display_instructions()
    mock_print.assert_any_call("📌 Instructions:")

@patch("builtins.print")
@patch("builtins.input", side_effect=["exit"])
@patch("sys.exit")  # ✅ Mock sys.exit() to prevent actual exit
def test_repl_instructions(mock_exit, mock_input, mock_print):
    """Ensure REPL prints correct instructions at startup."""
    CalculatorREPL.start()

    # ✅ Verify the correct instructions were printed
    expected_messages = [
        "📌 Instructions:",
        "🔹 Type 'menu' to see available operations.",
        "🔹 Type 'exit' to quit the calculator.",
        "🔹 To perform calculations, enter: `<operation> <num1> <num2>` (e.g., `add 2 3`).",
        "🔹 To use statistical operations, enter: `<operation> <num1> <num2> <num3> ...` (e.g., `mean 10 20 30`).",
        "🔹 Type 'history' to view past calculations.",
        "🔹 Type 'clear' to erase calculation history.",
        "🔹 Type 'help' to display this message again.",
    ]

    for message in expected_messages:
        mock_print.assert_any_call(message)

    # ✅ Ensure sys.exit() was called once
    mock_exit.assert_called_once()

@patch("builtins.print")
def test_show_menu(mock_print):
    """Ensure Menu.show_menu() displays the correct menu options."""
    Menu.show_menu()
    mock_print.assert_any_call(
        "\n📜 Calculator Menu:\n==============================\n"
        "1️⃣ - View Calculation History\n"
        "2️⃣ - Clear Calculation History\n"
        "3️⃣ - Remove Entry by ID\n"
        "4️⃣ - Reload History from CSV\n"
        "5️⃣ - Exit Calculator\n"
        "==============================\n"
    )


@patch("builtins.print")
@patch("builtins.input", side_effect=["1", "5"])  # Simulate user input
@patch("sys.exit", autospec=True)  # Prevent the test from exiting
def test_menu_handle_choice(mock_exit, mock_input, mock_print):
    """Ensure menu handles user choices correctly."""

    # ✅ **Mock history with a DataFrame (not a list)**
    mock_history_df = pd.DataFrame({
        "Operation": ["add"],
        "Operands": [[2, 3]],
        "Result": [5]
    })

    with patch.object(History, "get_history", return_value=mock_history_df):
        Menu.handle_choice("1")  # Show history
        Menu.handle_choice("5")  # Exit program

    # ✅ **Verify history is printed**
    mock_print.assert_any_call("\n📜 Calculation History:")

    # ✅ **Ensure exit message is printed**
    mock_print.assert_any_call("\n👋 Exiting calculator. Goodbye!")

    # ✅ **Confirm sys.exit(0) was called once**
    mock_exit.assert_called_once_with(0)


@patch("builtins.print")
def test_process_calculation_unknown_operation(mock_print):
    """Ensure unknown operations are properly handled."""
    CalculatorREPL.process_calculation("unknown_op 5 10")
    mock_print.assert_any_call("❌ Unknown operation: 'unknown_op'. Type 'menu' for options.")


@patch("builtins.print")
def test_process_calculation_invalid_format(mock_print):
    """Ensure invalid input formats are handled properly."""
    CalculatorREPL.process_calculation("add two three")
    mock_print.assert_any_call("⚠️ Invalid number format. Ensure all values are numeric.")


@patch("builtins.print")
def test_repl_welcome(mock_print):
    """Ensure REPL prints the welcome message."""
    CalculatorREPL.display_instructions()
    mock_print.assert_any_call("📌 Instructions:")


@patch("builtins.print")
@patch("builtins.input", side_effect=["exit"])
@patch("sys.exit", autospec=True)
def test_repl_welcome_on_start(mock_exit, mock_input, mock_print):
    """Ensure REPL displays the welcome message on startup."""
    CalculatorREPL.start()
    mock_print.assert_any_call("\n✨ Welcome to the Interactive Calculator! ✨")
    mock_exit.assert_called_once_with(0)
