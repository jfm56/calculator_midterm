"""Tests for the interactive menu system."""

import pytest
from unittest.mock import patch
from app.menu import show_menu
from history.history import History
from operations.operation_base import Operation


@pytest.fixture(autouse=True)
def reset_history():
    """Ensures history is cleared before each test."""
    History.clear_history()


@pytest.fixture(autouse=True)
def mock_operations():
    """Mock some operations for testing."""
    Operation.registry = {"add": None, "subtract": None, "multiply": None, "divide": None}


def test_show_operations():
    """Ensure the menu correctly displays available operations."""
    with patch("builtins.input", side_effect=["1", "5"]), patch("builtins.print") as mock_print:
        show_menu()

    mock_print.assert_any_call("\nAvailable Operations:\n  - add\n  - divide\n  - multiply\n  - subtract")


def test_show_history():
    """Ensure the menu correctly displays calculation history."""
    History.add_entry("add", 5, 3, 8)

    with patch("builtins.input", side_effect=["2", "5"]), patch("builtins.print") as mock_print:
        show_menu()

    mock_print.assert_any_call("\nCalculation History:\nadd 5 3 = 8")


def test_show_last_calculation():
    """Ensure the menu correctly displays the last calculation."""
    History.add_entry("multiply", 2, 3, 6)

    with patch("builtins.input", side_effect=["3", "5"]), patch("builtins.print") as mock_print:
        show_menu()

    mock_print.assert_any_call("\nLast Calculation:\nmultiply 2 3 = 6")


def test_clear_history():
    """Ensure the menu clears history correctly."""
    History.add_entry("divide", 10, 2, 5)

    with patch("builtins.input", side_effect=["4", "5"]), patch("builtins.print") as mock_print:
        show_menu()

    mock_print.assert_any_call("\nHistory cleared successfully.")
    assert History.get_history() == "No calculations yet."


def test_invalid_choice():
    """Ensure the menu handles invalid selections gracefully."""
    with patch("builtins.input", side_effect=["invalid", "5"]), patch("builtins.print") as mock_print:
        show_menu()

    mock_print.assert_any_call("\nInvalid selection! Please choose a valid option.")
