"""
History Module - Manages storage and retrieval of calculation history using Pandas.
"""

import pandas as pd
import logging
import ast

import pytest

# ✅ Setup logger
logger = logging.getLogger("calculator_logger")


class History:
    """Manages calculation history using a Pandas DataFrame."""
    _history = pd.DataFrame(columns=["ID", "Operation", "Operands", "Result"])
    _history_file = "history.csv"

    @classmethod
    def get_history(cls):
        """Retrieves stored history from CSV or initializes an empty DataFrame."""
        try:
            cls._history = pd.read_csv(cls._history_file)

            # ✅ Convert Operands back from string to list
            cls._history["Operands"] = cls._history["Operands"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

        except (FileNotFoundError, pd.errors.EmptyDataError):
            cls._history = pd.DataFrame(columns=["ID", "Operation", "Operands", "Result"])
        return cls._history

    @classmethod
    def add_entry(cls, operation, operands, result):
        """Adds a new calculation entry to history and saves to CSV."""

        # ✅ Ensure operands are stored as a **list or tuple**
        if not isinstance(operands, (list, tuple)):
            raise TypeError("Operands must be a list or tuple.")

        # ✅ Assign unique ID
        new_id = cls._history["ID"].max() + 1 if not cls._history.empty else 1

        new_entry = pd.DataFrame([{
            "ID": int(new_id),
            "Operation": operation,
            "Operands": str(operands),  # ✅ Store as string for CSV compatibility
            "Result": result
        }])

        if cls._history.empty:
            cls._history = new_entry
        else:
            cls._history = pd.concat([cls._history, new_entry], ignore_index=True)

        cls._save_history()
        logger.info(f"✅ Calculation saved: {operation} {operands} = {result}")

    @classmethod
    def _save_history(cls):
        """Saves history to CSV."""
        cls._history.to_csv(cls._history_file, index=False)

    @classmethod
    def clear_history(cls):
        """Clears all stored history."""
        cls._history = pd.DataFrame(columns=["ID", "Operation", "Operands", "Result"])
        cls._save_history()
        logger.info("🗑️ History cleared.")

    @classmethod
    def remove_entry(cls, entry_id):
        """Removes an entry from history by ID."""
        cls._history = cls._history[cls._history["ID"] != entry_id].reset_index(drop=True)
        cls._save_history()
        logger.info(f"❌ Entry {entry_id} removed from history.")


# ✅ TEST CASES
def test_reload_history():
    """Test reloading history from CSV using EAFP."""
    try:
        # ✅ Pass operands as a **list or tuple**
        History.add_entry("divide", [8, 2], 4)

        # ✅ Reload history and check if the entry exists
        history_df = History.get_history()
        assert not history_df.empty, "History should not be empty after adding an entry."
        assert history_df.iloc[-1]["Operation"] == "divide", "Last operation should be 'divide'."
        assert history_df.iloc[-1]["Operands"] == [8, 2], "Operands should be correctly stored and retrieved."
        assert history_df.iloc[-1]["Result"] == 4, "Result should be correctly stored."

    except Exception as e:
        pytest.fail(f"Unexpected error occurred: {e}")
