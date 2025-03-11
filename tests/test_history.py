"""Tests for the History class managing calculation history."""

import pytest
from history.history import History


@pytest.fixture(autouse=True)
def reset_history():
    """Ensures the history is cleared before each test."""
    History.clear_history()


def test_add_entry():
    """Ensure history correctly stores calculation entries."""
    History.add_entry("add", 5, 3, 8)
    assert History.get_history() == "add 5 3 = 8"


def test_get_history():
    """Ensure history returns correct entries."""
    History.add_entry("multiply", 2, 3, 6)
    History.add_entry("divide", 10, 2, 5)

    expected = "multiply 2 3 = 6\ndivide 10 2 = 5"
    assert History.get_history() == expected


def test_get_history_when_empty():
    """Ensure history returns a message when empty."""
    assert History.get_history() == "No calculations yet."


def test_get_last_entry():
    """Ensure get_last_entry() retrieves the last calculation."""
    History.add_entry("subtract", 10, 5, 5)
    History.add_entry("add", 3, 2, 5)
    assert History.get_last_entry() == "add 3 2 = 5"


def test_get_last_entry_when_empty():
    """Ensure get_last_entry() handles an empty history correctly."""
    assert History.get_last_entry() == "No history available."


def test_clear_history():
    """Ensure history is cleared properly."""
    History.add_entry("add", 1, 1, 2)
    History.clear_history()
    assert History.get_history() == "No calculations yet."
