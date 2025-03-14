"""Tests for the calculator menu system."""
import builtins
import pytest
from app.menu import Menu  # ✅ Import Menu class
from history.history import History

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Ensures history is cleared before and after each test."""
    History.clear_history()
    yield
    History.clear_history()


def test_show_menu(capsys):
    """Ensure the menu is displayed correctly."""
    Menu.show_menu()
    captured = capsys.readouterr()
    assert "📜 Calculator Menu:" in captured.out
    assert "1️⃣ - View Calculation History" in captured.out
    assert "5️⃣ - Exit Calculator" in captured.out


def test_handle_view_history_empty(capsys):
    """Ensure viewing history shows no data when empty."""
    Menu.handle_choice("1")
    captured = capsys.readouterr()
    assert "⚠️ No calculations found." in captured.out


def test_handle_view_history_with_entries(capsys):
    """Ensure history displays correct entries when data is available."""
    History.add_entry("add", 10, 5, 15)
    Menu.handle_choice("1")
    captured = capsys.readouterr()
    assert "add" in captured.out
    assert "10" in captured.out
    assert "5" in captured.out
    assert "15" in captured.out


def test_handle_clear_history(capsys):
    """Ensure clearing history removes all entries."""
    History.add_entry("subtract", 20, 4, 16)
    Menu.handle_choice("2")
    captured = capsys.readouterr()
    assert "✅ History cleared successfully!" in captured.out
    assert History.get_history().empty, "⚠️ History should be empty after clearing."


def test_handle_remove_entry_existing(capsys, monkeypatch):
    """Ensure a valid entry is removed correctly."""
    History.add_entry("multiply", 5, 2, 10)

    # ✅ Ensure history is not empty before accessing ID
    history_df = History.get_history()
    assert not history_df.empty, "⚠️ No history available to remove."

    entry_id = int(history_df.iloc[0]["ID"])

    # ✅ Directly set input instead of lambda function
    monkeypatch.setattr(builtins, "input", str(entry_id))
    Menu.handle_choice("3")

    captured = capsys.readouterr()
    assert f"✅ Entry ID {entry_id} removed successfully!" in captured.out
    assert entry_id not in History.get_history()["ID"].values


def test_handle_remove_entry_invalid_id(capsys, monkeypatch):
    """Ensure removing a non-existent entry fails gracefully."""
    History.add_entry("divide", 100, 10, 10)

    # ✅ Simulate user input of an invalid ID
    monkeypatch.setattr(builtins, "input", "999")
    Menu.handle_choice("3")

    captured = capsys.readouterr()
    assert "⚠️ Entry ID 999 not found." in captured.out


def test_handle_remove_entry_non_numeric_input(capsys, monkeypatch):
    """Ensure non-numeric input does not cause a crash."""
    History.add_entry("add", 1, 1, 2)

    monkeypatch.setattr(builtins, "input", "abc")
    Menu.handle_choice("3")

    captured = capsys.readouterr()
    assert "❌ Invalid input. Please enter a valid numeric ID." in captured.out
