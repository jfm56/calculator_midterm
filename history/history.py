"""Manages calculation history using Pandas for data storage and retrieval."""
from pathlib import Path
import pandas as pd
import logging
from config.env import HISTORY_FILE_PATH

# ✅ Setup logger
logger = logging.getLogger(__name__)

class History:
    """Maintains the history of calculations performed using Pandas."""
    
    _history_df = pd.DataFrame(columns=["ID", "Operation", "Operand1", "Operand2", "Result"])
    _history_path = Path(HISTORY_FILE_PATH)

    @classmethod
    def add_entry(cls, operation, a, b, result):
        """Adds a calculation entry to history and saves it."""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            logger.warning(f"⚠️ Invalid data types: {a}, {b}")
            return

        new_entry = pd.DataFrame([{
            "ID": cls._generate_id(),
            "Operation": operation,
            "Operand1": a,
            "Operand2": b,
            "Result": result
        }])

        cls._history_df = pd.concat([cls._history_df, new_entry], ignore_index=True)
        cls.save_history()

    @classmethod
    def get_history(cls):
        """Returns the calculation history as a DataFrame. Loads if empty."""
        if cls._history_df.empty:
            cls.load_history()
        return cls._history_df

    @classmethod
    def remove_entry(cls, entry_id):
        """Removes a specific history entry by ID and updates the CSV."""
        if cls._history_df.empty or "ID" not in cls._history_df.columns:
            logger.warning("⚠️ No history available.")
            return

        logger.info(f"❌ Removing entry with ID {entry_id}...")

        # ✅ Ensure ID column is treated as an integer for filtering
        cls._history_df["ID"] = cls._history_df["ID"].astype(int)
        cls._history_df = cls._history_df[cls._history_df["ID"] != entry_id]

        cls.save_history()

    @classmethod
    def clear_history(cls):
        """Clears all stored history but ensures the CSV structure remains."""
        cls._history_df = pd.DataFrame(columns=["ID", "Operation", "Operand1", "Operand2", "Result"])
        cls._history_df.to_csv(cls._history_path, index=False, encoding="utf-8")
        logger.info("✅ History cleared and structure retained.")

    @classmethod
    def load_history(cls):
        """Loads calculation history from the CSV file."""
        try:
            if not cls._history_path.exists() or cls._history_path.stat().st_size == 0:
                logger.warning("⚠️ CSV file missing or empty. Initializing empty history.")
                cls._history_df = pd.DataFrame(columns=["ID", "Operation", "Operand1", "Operand2", "Result"])
                return

            logger.info("✅ CSV Exists, Attempting to Read...")

            # 🚨 Read CSV safely
            temp_df = pd.read_csv(
                cls._history_path,
                dtype=str,
                skip_blank_lines=True,
                encoding="utf-8",
                keep_default_na=False,
            )

            if temp_df.empty or temp_df.isnull().all().all():
                logger.warning("⚠️ CSV exists but contains no valid data. Initializing empty history.")
                cls._history_df = pd.DataFrame(columns=["ID", "Operation", "Operand1", "Operand2", "Result"])
            else:
                # ✅ Convert data types explicitly
                temp_df["ID"] = pd.to_numeric(temp_df["ID"], errors="coerce").fillna(0).astype(int)
                temp_df["Operand1"] = pd.to_numeric(temp_df["Operand1"], errors="coerce")
                temp_df["Operand2"] = pd.to_numeric(temp_df["Operand2"], errors="coerce")
                temp_df["Result"] = pd.to_numeric(temp_df["Result"], errors="coerce")

                cls._history_df = temp_df.dropna()
                logger.info("✅ Successfully Loaded History From CSV.")

        except Exception as e:
            logger.error(f"❌ Error loading CSV: {e}")
            cls._history_df = pd.DataFrame(columns=["ID", "Operation", "Operand1", "Operand2", "Result"])

    @classmethod
    def get_last_entry(cls):
        """Returns the last calculation performed."""
        if cls._history_df.empty:
            return "No history available."
        return cls._history_df.iloc[-1].to_dict()

    @classmethod
    def save_history(cls):
        """Ensures history is saved correctly, even when empty."""
        logger.info("✅ Saving history to CSV.")
        cls._history_df.to_csv(cls._history_path, index=False, encoding="utf-8")

    @classmethod
    def _generate_id(cls):
        """Generates a unique ID for each entry."""
        if cls._history_df.empty or "ID" not in cls._history_df.columns:
            return 1
        return int(cls._history_df["ID"].fillna(0).max() + 1)
