"""Tests for History class using EAFP principles."""

import os
import pytest
from history.history import History

# ✅ Define a test CSV file separate from the main history file
TEST_HISTORY_FILE = "test_history.csv"

# ✅ Override HISTORY_FILE in History for testing
History.HISTORY_FILE = TEST_HISTORY_FILE


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Ensure a clean history before and after each test."""
    try:
        # ✅ Remove any existing test history file
        if os.path.exists(TEST_HISTORY_FILE):
            os.remove(TEST_HISTORY_FILE)

        # ✅ Ensure history is properly cleared
        History.clear_history()

    except (FileNotFoundError, ValueError) as e:
        pytest.fail(f"❌ Setup failed: {e}")

    yield  # ✅ Run the test

    try:
        # ✅ Cleanup after tests
        if os.path.exists(TEST_HISTORY_FILE):
            os.remove(TEST_HISTORY_FILE)

        # ✅ Reset history
        History.clear_history()
    except (FileNotFoundError, ValueError) as e:
        pytest.fail(f"❌ Teardown failed: {e}")


def test_add_entry():
    """Test adding a history entry using EAFP."""
    try:
        History.add_entry("add", 2, 3, 5)
        history = History.get_history()
        assert not history.empty, "⚠️ History should not be empty after adding an entry."
        assert history.iloc[-1]["Operation"] == "add", "⚠️ Last entry should be an addition operation."
    except (KeyError, ValueError) as e:
        pytest.fail(f"❌ Unexpected error: {e}")


def test_get_history_empty():
    """Test retrieving history when no CSV exists using EAFP."""
    try:
        # ✅ Ensure history is cleared before testing
        History.clear_history()
        history = History.get_history()

        assert history.empty, f"⚠️ Expected an empty history, but got:\n{history}"
    except (FileNotFoundError, ValueError) as e:
        pytest.fail(f"❌ Unexpected error: {e}")


def test_remove_entry():
    """Test removing an entry from history using EAFP."""
    try:
        History.clear_history()  # ✅ Ensure fresh state

        History.add_entry("subtract", 10, 3, 7)
        initial_size = len(History.get_history())

        entry_id = History.get_history().iloc[-1]["ID"]  # ✅ Get last entry's ID
        History.remove_entry(entry_id)

        history_after = History.get_history()
        assert len(history_after) == initial_size - 1, f"⚠️ Expected history size to decrease after removing entry {entry_id}."
    except KeyError:
        pytest.fail("❌ KeyError: Entry ID should exist before removal.")
    except (FileNotFoundError, ValueError) as e:
        pytest.fail(f"❌ Unexpected error: {e}")


def test_remove_nonexistent_entry():
    """Test trying to remove a non-existent entry using EAFP."""
    try:
        History.remove_entry(999)  # ✅ Non-existent ID should not raise an error
    except KeyError:
        pytest.fail("❌ Unexpected KeyError: Should handle missing entries gracefully.")
    except (FileNotFoundError, ValueError) as e:
        pytest.fail(f"❌ Unexpected error: {e}")


def test_clear_history():
    """Test clearing history using EAFP."""
    try:
        History.add_entry("multiply", 2, 5, 10)
        History.clear_history()

        history = History.get_history()
        assert history.empty, f"⚠️ History should be empty after clearing, but got:\n{history}"
    except (FileNotFoundError, ValueError) as e:
        pytest.fail(f"❌ Unexpected error: {e}")


def test_reload_history():
    """Test reloading history from CSV using EAFP."""
    try:
        History.add_entry("divide", 8, 2, 4)
        History.reload_history()

        history = History.get_history()
        assert not history.empty, "⚠️ Expected history to be present after reloading."
    except (FileNotFoundError, ValueError) as e:
        pytest.fail(f"❌ Unexpected error: {e}")
