"""Tests for the Menu system in the calculator REPL."""
import pytest
from app.menu import Menu
from history.history import History
from unittest.mock import patch

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Ensure a clean history before and after each test."""
    History.clear_history()
    yield
    History.clear_history()

def test_display_menu(capfd):
    """Test if the menu displays correctly."""
    Menu.display_menu()
    captured = capfd.readouterr()
    
    assert "Calculator Menu" in captured.out
    assert "1. Perform Calculation" in captured.out
    assert "5. Exit" in captured.out

def test_get_user_choice(monkeypatch):
    """Test getting a valid menu choice."""
    monkeypatch.setattr("builtins.input", lambda _: "1")
    choice = Menu.get_user_choice()
    assert choice == "1"

def test_invalid_choice(monkeypatch, capfd):
    """Test invalid menu input handling."""
    monkeypatch.setattr("builtins.input", lambda _: "999")
    choice = Menu.get_user_choice()
    
    captured = capfd.readouterr()
    assert "Invalid choice" in captured.out
    assert choice is None

@patch("builtins.input", side_effect=["5"])
def test_menu_exit(mock_input, capfd):
    """Test if the menu handles exit properly."""
    with patch("sys.exit") as mock_exit:
        Menu.run()

    captured = capfd.readouterr()
    assert "Goodbye!" in captured.out
    mock_exit.assert_called_once()
