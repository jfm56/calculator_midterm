"""Tests for the Menu class using EAFP principles."""

import pytest
import logging
from unittest.mock import patch
from history.history import History
from app.menu import Menu  # ✅ Ensure correct import path


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Ensure a clean history before and after each test."""
    try:
        History.clear_history()
    except Exception as e:
        pytest.fail(f"❌ Setup failed: {e}")

    yield  # ✅ Run the test

    try:
        History.clear_history()
    except Exception as e:
        pytest.fail(f"❌ Teardown failed: {e}")


def test_show_menu(capfd):
    """Test that the menu displays correctly."""
    try:
        Menu.show_menu()
        captured = capfd.readouterr()
        assert "📜 Calculator Menu:" in captured.out, "⚠️ Menu text missing."
    except Exception as e:
        pytest.fail(f"❌ Unexpected error: {e}")


@patch("builtins.input", side_effect=["yes"])
def test_clear_history(mock_input, capfd, caplog):
    """Test clearing history using EAFP."""
    try:
        caplog.set_level(logging.INFO)

        History.add_entry("add", 2, 3, 5)
        Menu.clear_history()

        captured = capfd.readouterr()
        assert "✅ History cleared successfully!" in captured.out, "⚠️ Expected history cleared message."
        assert "✅ History cleared successfully." in caplog.text, "⚠️ Expected log message missing."

        assert History.get_history().empty, "⚠️ History should be empty after clearing."
    except Exception as e:
        pytest.fail(f"❌ Unexpected error: {e}")


@patch("builtins.input", side_effect=["no"])
def test_clear_history_cancel(mock_input, capfd, caplog):
    """Test cancelling history clear operation using EAFP."""
    try:
        caplog.set_level(logging.INFO)

        History.add_entry("subtract", 10, 5, 5)
        Menu.clear_history()

        captured = capfd.readouterr()
        assert "🚫 History clear operation cancelled." in captured.out, "⚠️ Expected cancel message."
        assert "🚫 History clear operation cancelled." in caplog.text, "⚠️ Expected log message missing."

        assert not History.get_history().empty, "⚠️ History should remain unchanged."
    except Exception as e:
        pytest.fail(f"❌ Unexpected error: {e}")


@patch("builtins.input", side_effect=["999"])
def test_remove_nonexistent_entry(mock_input, capfd, caplog):
    """Test attempting to remove a non-existent entry using EAFP."""
    try:
        caplog.set_level(logging.WARNING)

        # ✅ Ensure there's at least one entry in history
        History.add_entry("multiply", 4, 2, 8)
        Menu.remove_entry()

        captured = capfd.readouterr()
        assert "⚠️ Entry with ID 999 not found." in captured.out, f"⚠️ Unexpected output: {captured.out}"
        assert "⚠️ Entry with ID 999 not found." in caplog.text, "⚠️ Expected log warning missing."
    except Exception as e:
        pytest.fail(f"❌ Unexpected error: {e}")


@patch("builtins.input", side_effect=["1"])
@patch("app.menu.Menu.view_history")  # ✅ Fix incorrect module reference
def test_handle_choice_valid(mock_view_history, mock_input):
    """Test valid menu choices using EAFP."""
    try:
        Menu.handle_choice("1")
        mock_view_history.assert_called_once()
    except Exception as e:
        pytest.fail(f"❌ Unexpected error: {e}")


@patch("builtins.input", side_effect=["99"])
@patch("app.menu.logger.warning")  # ✅ Fix incorrect module reference
def test_handle_invalid_choice(mock_logger, mock_input):
    """Test invalid menu choice handling using EAFP."""
    try:
        Menu.handle_choice("99")
        mock_logger.assert_called_once_with("❌ Invalid selection made in menu.")
    except Exception as e:
        pytest.fail(f"❌ Unexpected error: {e}")


@patch("builtins.input", side_effect=["exit"])
@patch("builtins.exit")
def test_exit_program(mock_exit, mock_input, capfd, caplog):
    """Test the exit function using EAFP."""
    try:
        caplog.set_level(logging.INFO)
        Menu.exit_program()

        captured = capfd.readouterr()
        assert "👋 Exiting calculator. Goodbye!" in captured.out, f"⚠️ Unexpected output: {captured.out}"
        assert "👋 Exiting calculator. Goodbye!" in caplog.text, "⚠️ Expected log message missing."

        mock_exit.assert_called_once()
    except Exception as e:
        pytest.fail(f"❌ Unexpected error: {e}")
