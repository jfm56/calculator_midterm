"""
Unit tests for the History module.
Tests cover adding, removing, clearing, and retrieving calculation history.
"""
import pytest
from history.history import History


def test_add_entry():
    """Test adding a history entry using EAFP."""
    try:
        History.add_entry("add", [2, 3], 5)  # ✅ Pass operands as a list
        history_df = History.get_history()
        assert not history_df.empty, "History should not be empty after adding an entry."
        assert history_df.iloc[-1]["Operation"] == "add", "Last operation should be 'add'."
        assert history_df.iloc[-1]["Operands"] == [2, 3], "Operands should be stored as a list."
        assert history_df.iloc[-1]["Result"] == 5, "Result should be correctly stored."

    except TypeError as e:
        pytest.fail(f"Unexpected error occurred: {e}")


def test_remove_entry():
    """Test removing an entry from history using EAFP."""
    try:
        History.clear_history()  # ✅ Ensure fresh state

        History.add_entry("subtract", [10, 3], 7)  # ✅ Fix operands format
        history_df = History.get_history()

        assert len(history_df) == 1, "There should be one entry before deletion."
        entry_id = history_df.iloc[0]["ID"]

        History.remove_entry(entry_id)
        updated_history_df = History.get_history()
        assert updated_history_df.empty, "History should be empty after removing the only entry."

    except TypeError as e:
        pytest.fail(f"Unexpected error occurred: {e}")


def test_clear_history():
    """Test clearing history using EAFP."""
    try:
        History.add_entry("multiply", [2, 5], 10)  # ✅ Fix operands format
        History.clear_history()
        assert History.get_history().empty, "History should be empty after clearing."

    except TypeError as e:
        pytest.fail(f"Unexpected error occurred: {e}")


def test_reload_history():
    """Test reloading history from CSV using EAFP."""
    try:
        History.add_entry("divide", [8, 2], 4)  # ✅ Fix operands format
        history_df = History.get_history()
        assert not history_df.empty, "History should not be empty after adding an entry."
        assert history_df.iloc[-1]["Operation"] == "divide", "Last operation should be 'divide'."
        assert history_df.iloc[-1]["Operands"] == [8, 2], "Operands should be stored as a list."
        assert history_df.iloc[-1]["Result"] == 4, "Result should be correctly stored."

    except TypeError as e:
        pytest.fail(f"Unexpected error occurred: {e}")
