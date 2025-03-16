"""
Unit tests for the Menu module.

These tests cover:
- Displaying the menu
- Handling user choices
- Viewing, clearing, and removing history
- Reloading history
- Exiting the program
- Handling invalid menu selections
"""
import pandas as pd
from unittest.mock import patch
from app.menu import Menu
from history.history import History


@patch("builtins.print")
def test_show_menu(mock_print):
    """Ensure Menu.show_menu() displays the correct menu."""
    Menu.show_menu()
    mock_print.assert_any_call("\n📜 Calculator Menu:\n==============================\n1️⃣ - View Calculation History\n2️⃣ - Clear Calculation History\n3️⃣ - Remove Entry by ID\n4️⃣ - Reload History from CSV\n5️⃣ - Exit Calculator\n==============================\n")


@patch("builtins.print")
@patch("builtins.input", side_effect=["1", "5"])  # Simulate user input
@patch("sys.exit", autospec=True)  # Prevent the test from exiting
def test_handle_choice(mock_exit, mock_input, mock_print):
    """Ensure Menu handles user choices correctly."""

    # ✅ **Mock history with a DataFrame (not a list)**
    mock_history_df = pd.DataFrame({
        "ID": [1],
        "Operation": ["add"],
        "Operands": ["[2, 3]"],
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
    mock_exit.assert_called_once()


@patch("builtins.print")
def test_view_history_empty(mock_print):
    """Ensure Menu.view_history() handles empty history."""
    with patch.object(History, "get_history", return_value=pd.DataFrame()):
        Menu.view_history()
    mock_print.assert_any_call("\n⚠️ No calculations found.")


@patch("builtins.print")
def test_view_history_with_data(mock_print):
    """Ensure Menu.view_history() displays history when present."""
    mock_history_df = pd.DataFrame({
        "ID": [1],
        "Operation": ["add"],
        "Operands": ["[2, 3]"],
        "Result": [5]
    })
    with patch.object(History, "get_history", return_value=mock_history_df):
        Menu.view_history()
    mock_print.assert_any_call("\n📜 Calculation History:")


@patch("builtins.print")
@patch("builtins.input", side_effect=["yes"])
def test_clear_history_confirm(mock_input, mock_print):
    """Ensure Menu.clear_history() clears history when confirmed."""
    with patch.object(History, "clear_history") as mock_clear:
        Menu.clear_history()
        mock_clear.assert_called_once()
    mock_print.assert_any_call("\n✅ History cleared successfully!")


@patch("builtins.print")
@patch("builtins.input", side_effect=["no"])
def test_clear_history_cancel(mock_input, mock_print):
    """Ensure Menu.clear_history() does not clear history when cancelled."""
    with patch.object(History, "clear_history") as mock_clear:
        Menu.clear_history()
        mock_clear.assert_not_called()
    mock_print.assert_any_call("\n🚫 History clear operation cancelled.")


@patch("builtins.print")
@patch("builtins.input", side_effect=["2"])
def test_remove_nonexistent_entry(mock_input, mock_print):
    """Ensure Menu.remove_entry() handles missing entries correctly."""
    with patch.object(History, "get_history", return_value=pd.DataFrame()):
        Menu.remove_entry()
    mock_print.assert_any_call("\n⚠️ No history available to remove.")


@patch("builtins.print")
@patch("builtins.input", side_effect=["3"])
def test_remove_entry_invalid(mock_input, mock_print):
    """Ensure Menu.remove_entry() handles invalid IDs correctly."""
    mock_history_df = pd.DataFrame({
        "ID": [1],
        "Operation": ["add"],
        "Operands": ["[2, 3]"],
        "Result": [5]
    })
    with patch.object(History, "get_history", return_value=mock_history_df):
        Menu.remove_entry()
    mock_print.assert_any_call("\n⚠️ Entry with ID 3 not found.")


@patch("builtins.print")
@patch("builtins.input", side_effect=["1"])
def test_remove_entry_valid(mock_input, mock_print):
    """Ensure Menu.remove_entry() removes valid entry."""
    mock_history_df = pd.DataFrame({
        "ID": [1],
        "Operation": ["add"],
        "Operands": ["[2, 3]"],
        "Result": [5]
    })
    with patch.object(History, "get_history", return_value=mock_history_df):
        with patch.object(History, "remove_entry") as mock_remove:
            Menu.remove_entry()
            mock_remove.assert_called_once_with(1)
    mock_print.assert_any_call("\n✅ Entry 1 removed successfully.")


@patch("builtins.print")
def test_reload_history(mock_print):
    """Ensure Menu.reload_history() calls get_history()."""
    with patch.object(History, "get_history") as mock_reload:
        Menu.reload_history()
        mock_reload.assert_called_once()
    mock_print.assert_any_call("\n🔄 History reloaded successfully.")

@patch("builtins.print")
@patch("sys.exit", autospec=True)
def test_exit_program(mock_exit, mock_print):
    """Ensure Menu.exit_program() exits the program."""
    Menu.exit_program()

    # ✅ Verify sys.exit(0) was called
    mock_exit.assert_called_once_with(0)

    # ✅ Ensure exit message was printed
    mock_print.assert_any_call("\n👋 Exiting calculator. Goodbye!")

@patch("builtins.print")
def test_invalid_choice(mock_print):
    """Ensure invalid menu selections are handled."""
    Menu.invalid_choice()
    mock_print.assert_any_call("\n❌ Invalid selection. Please try again.")
