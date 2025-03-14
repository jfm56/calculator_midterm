import pandas as pd
import os
import logging

# ✅ Setup logging
logger = logging.getLogger("calculator_logger")

# ✅ Define history file path
HISTORY_FILE = "history.csv"

class History:
    """Handles storing and retrieving calculator history."""

    # ✅ Initialize empty DataFrame with correct columns
    _history = pd.DataFrame(columns=["ID", "Operation", "Operand1", "Operand2", "Result"])

    @classmethod
    def add_entry(cls, operation, operand1, operand2, result):
        """Adds a new calculation entry to history and saves to CSV."""
        new_entry = pd.DataFrame([{
            "ID": len(cls._history) + 1,
            "Operation": operation,
            "Operand1": operand1,
            "Operand2": operand2,
            "Result": result
        }])

        if cls._history.empty:
            cls._history = new_entry
        else:
            cls._history = pd.concat([cls._history, new_entry], ignore_index=True)

        cls._save_history()
        logger.info(f"✅ Calculation saved: {operation} {operand1} {operand2} = {result}")

    @classmethod
    def get_history(cls):
        """Loads history from CSV file or returns an empty DataFrame."""
        if os.path.exists(HISTORY_FILE):
            cls._history = pd.read_csv(HISTORY_FILE)

            # ✅ Ensure DataFrame always has correct columns
            if cls._history.empty or set(cls._history.columns) != {"ID", "Operation", "Operand1", "Operand2", "Result"}:
                logger.warning("⚠️ CSV exists but contains no valid data. Initializing empty history.")
                cls._history = pd.DataFrame(columns=["ID", "Operation", "Operand1", "Operand2", "Result"])
        return cls._history

    @classmethod
    def remove_entry(cls, entry_id):
        """Removes an entry from history by ID."""
        if cls._history.empty:
            logger.warning("⚠️ No history available to remove.")
            return

        if entry_id not in cls._history["ID"].values:
            logger.warning(f"❌ Entry ID {entry_id} not found.")
            return

        cls._history = cls._history[cls._history["ID"] != entry_id]
        cls._save_history()
        logger.info(f"✅ Entry {entry_id} removed successfully.")

    @classmethod
    def clear_history(cls):
        """Clears the history."""
        cls._history = pd.DataFrame(columns=["ID", "Operation", "Operand1", "Operand2", "Result"])
        cls._save_history()
        logger.info("✅ History cleared successfully!")

    @classmethod
    def reload_history(cls):
        """Reloads history from CSV (wrapper for get_history)."""
        cls.get_history()
        logger.info("🔄 History reloaded from CSV.")

    @classmethod
    def _save_history(cls):
        """Saves the history DataFrame to CSV."""
        cls._history.to_csv(HISTORY_FILE, index=False)
        logger.debug("💾 History saved to CSV.")
