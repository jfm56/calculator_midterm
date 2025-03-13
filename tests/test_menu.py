"""Tests for the calculator menu system."""
import pytest
import builtins
from app.menu import show_menu, handle_menu_choice
from history.history import History

@pytest.fixture(autouse=True)
def reset_history():
    """Ensures history is cleared before each test."""
    History.clear_history()

def test_show_menu(capsys):
    """Ensure the menu is displayed correctly."""
    show_menu()
    captured = capsys.readouterr()
    assert "📜 Calculator Menu:" in captured.out
    assert "1️⃣ - View Calculation History" in captured.out
    assert "5️⃣ - Exit Calculator" in captured.out

def test_handle_view_history_empty(capsys):
    """Ensure viewing history shows no data when empty."""
    handle_menu_choice("1")
    captured = capsys.readouterr()
    assert "⚠️ No history file found or it is empty." in captured.out

def test_handle_view_history_with_entries(capsys):
    """Ensure history displays correct entries when data is available."""
    History.add_entry("add", 10, 5, 15)
    handle_menu_choice("1")
    captured = capsys.readouterr()
    assert "add" in captured.out
    assert "10" in captured.out
    assert "5" in captured.out
    assert "15" in captured.out

def test_handle_clear_history(capsys):
    """Ensure clearing history removes all entries."""
    History.add_entry("subtract", 20, 4, 16)
    handle_menu_choice("2")
    captured = capsys.readouterr()
    assert "✅ History cleared successfully!" in captured.out
    assert History.get_history().empty, "⚠️ History should be empty after clearing."

def test_handle_remove_entry_existing(capsys, monkeypatch):
    """Ensure a valid entry is removed correctly."""
    History.add_entry("multiply", 5, 2, 10)
    entry_id = int(History.get_history().iloc[0]["ID"])
    
    # Simulate user input
    monkeypatch.setattr(builtins, "input", lambda _: str(entry_id))
    handle_menu_choice("3")
    
    captured = capsys.readouterr()
    assert f"✅ Entry ID {entry_id} removed successfully!" in captured.out
    assert entry_id not in History.get_history()["ID"].values

def test_handle_remove_entry_invalid_id(capsys, monkeypatch):
    """Ensure removing a non-existent entry fails gracefully."""
    History.add_entry("divide", 100, 10, 10)
    
    # Simulate user input of an invalid ID
    monkeypatch.setattr(builtins, "input", lambda _: "999")
    handle_menu_choice("3")
    
    captured = capsys.readouterr()
    assert "⚠️ Entry ID 999 not found." in captured.out

def test_handle_reload_history(capsys):
    """Ensure reloading history from CSV works."""
    History.add_entry("add", 10, 5, 15)
    History.save_history()
    
    History.clear_history()
    handle_menu_choice("4")  # Reload history
    
    captured = capsys.readouterr()
    assert "🔄 History reloaded from CSV!" in captured.out
    assert not History.get_history().empty, "⚠️ History should be reloaded from CSV."

def test_handle_invalid_selection(capsys):
    """Ensure invalid menu selections are handled correctly."""
    handle_menu_choice("999")
    captured = capsys.readouterr()
    assert "❌ Invalid selection. Please try again." in captured.out
