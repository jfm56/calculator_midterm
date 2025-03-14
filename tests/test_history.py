# ✅ Standard Library Imports
import os
import pytest

# ✅ Local Imports
from history.history import History
from config.env import HISTORY_FILE_PATH

def test_save_and_load_history():
    """Test saving and loading history from CSV with forced file flush."""

    # ✅ Step 1: Add Entry & Save
    History.add_entry("add", 1, 2, 3)
    History.save_history()

    # ✅ Step 2: Ensure the file exists
    assert os.path.exists(HISTORY_FILE_PATH), "⚠️ CSV file should exist after saving"

    # ✅ Step 3: Verify File Contents
    with open(HISTORY_FILE_PATH, "r+", encoding="utf-8") as file:
        file.flush()  # ✅ Ensure OS flushes data to disk
        os.fsync(file.fileno())  # ✅ Force OS-level file write
        csv_contents = file.read()

        # ✅ Check if data is written correctly
        assert csv_contents.strip(), "⚠️ CSV file should not be empty"
        assert "add,1,2,3" in csv_contents, "⚠️ Expected data not found in CSV file"

    # ✅ Step 4: Clear History & Verify Empty
    History.clear_history()
    assert History.get_history().empty, "⚠️ History should be empty after clearing"

    # ✅ Step 5: Reload & Verify Data Integrity
    History.load_history()
    df = History.get_history()

    assert len(df) > 0, "⚠️ History should be reloaded from CSV"
    assert set(df.columns) == {"ID", "Operation", "Operand1", "Operand2", "Result"}, "⚠️ Missing expected columns"
