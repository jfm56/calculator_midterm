"""Tests for the History class using Pandas for data storage."""
import os
import pandas as pd
import pytest
from history.history import History
from config.env import HISTORY_FILE_PATH

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Ensure a clean slate before and after each test."""
    History.clear_history()
    yield
    History.clear_history()

def test_add_entry():
    """Test adding an entry to history."""
    History.add_entry("add", 5, 3, 8)
    df = History.get_history()

    assert isinstance(df, pd.DataFrame), "⚠️ Expected a DataFrame"
    assert not df.empty, "⚠️ History should not be empty"
    assert df.iloc[-1]["Operation"] == "add"
    assert df.iloc[-1]["Operand1"] == 5
    assert df.iloc[-1]["Operand2"] == 3
    assert df.iloc[-1]["Result"] == 8

def test_get_last_entry():
    """Test retrieving the last calculation."""
    History.add_entry("multiply", 2, 4, 8)
    last_entry = History.get_last_entry()

    assert isinstance(last_entry, dict), "⚠️ Expected dictionary format"
    assert last_entry["Operation"] == "multiply", "⚠️ Expected last operation to be 'multiply'"
    assert last_entry["Result"] == 8, "⚠️ Expected result to be 8"


def test_remove_entry():
    """Test removing an entry from history."""
    History.add_entry("subtract", 10, 4, 6)
    df_before = History.get_history()

    assert not df_before.empty, "⚠️ History should not be empty before removal"

    first_id = int(df_before.iloc[0]["ID"])  # ✅ Ensure ID is treated as an integer
    History.remove_entry(first_id)

    df_after = History.get_history()

    print("\n📋 History After Removal:\n", df_after)  # Debugging print

    assert "ID" in df_after.columns, "⚠️ ID column should still exist"
    assert first_id not in df_after["ID"].astype(int).values, f"⚠️ Entry ID {first_id} should be removed"
    assert df_after.empty, "⚠️ History should be empty after removing all entries"

def test_clear_history():
    """Test clearing all history records."""
    History.add_entry("divide", 10, 2, 5)
    
    df_before = History.get_history()
    assert not df_before.empty, "⚠️ History should not be empty before clearing"

    History.clear_history()
    df_after = History.get_history()
    
    assert isinstance(df_after, pd.DataFrame), "⚠️ Expected DataFrame after clearing history"
    assert df_after.empty, "⚠️ History should be empty after clearing"

def test_save_and_load_history():
    """Test saving and loading history from CSV."""
    History.add_entry("add", 1, 2, 3)
    History.save_history()

    # ✅ Print raw CSV contents before clearing
    with open(HISTORY_FILE_PATH, "r", encoding="utf-8") as file:
        csv_contents = file.read()
        print("\n✅ CSV File Contents Before Clearing:\n", csv_contents)  # Debugging print

    assert os.path.exists(HISTORY_FILE_PATH), "⚠️ CSV file should exist after saving"
    assert csv_contents.strip(), "⚠️ CSV file should not be empty"

    History.clear_history()
    assert History.get_history().empty, "⚠️ History should be empty after clearing"

    # ✅ Manually read file contents again before reloading
    with open(HISTORY_FILE_PATH, "r", encoding="utf-8") as file:
        csv_contents_after_clear = file.read()
        print("\n🔄 CSV File Contents After Clearing (Before Reloading):\n", csv_contents_after_clear)

    History.load_history()
    df = History.get_history()

    print("\n📂 Loaded History From CSV:\n", df)  # Debugging print

    assert not df.empty, "⚠️ History should be reloaded from CSV"
    assert "add" in df["Operation"].values, "⚠️ 'add' operation should be in reloaded history"

def test_reconstitute_entry():
    """Test converting a CSV row to a dictionary."""
    History.add_entry("divide", 8, 2, 4)
    df = History.get_history()
    record = df.iloc[0]
    
    restored_entry = History.reconstitute_entry(record)
    assert isinstance(restored_entry, dict), "⚠️ Expected a dictionary"
    assert restored_entry["Operation"] == "divide"
