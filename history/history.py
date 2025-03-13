"""Manages calculation history using Pandas for data storage and retrieval."""
import os
import pandas as pd
from config.env import HISTORY_FILE_PATH

class History:
    """Maintains the history of calculations performed using Pandas."""

    _history_df = pd.DataFrame(columns=["ID", "Operation", "Operand1", "Operand2", "Result"])

    @classmethod
    def add_entry(cls, operation, a, b, result):
        """Adds a calculation entry to history and saves it."""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            print(f"⚠️ Invalid data types: {a}, {b}")
            return  # ✅ LBYL: Invalid data → exit early

        new_entry = pd.DataFrame([{
            "ID": cls._generate_id(),  # ✅ Unique ID for tracking
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
            cls.load_history()  # ✅ Ensure history is loaded
        return cls._history_df

    @classmethod
    def remove_entry(cls, entry_id):
        """Removes a specific history entry by ID and updates the CSV."""
        if cls._history_df.empty or "ID" not in cls._history_df.columns:
            print("⚠️ No history available.")
            return

        # ✅ Ensure ID column is an integer for proper filtering
        cls._history_df["ID"] = cls._history_df["ID"].astype(int)

        # ✅ Remove the entry
        cls._history_df = cls._history_df[cls._history_df["ID"] != entry_id]

        # ✅ Save updated history
        cls.save_history()

    @classmethod
    def clear_history(cls):
     """Clears all stored history and overwrites the CSV with an empty DataFrame."""
     cls._history_df = pd.DataFrame(columns=["ID", "Operation", "Operand1", "Operand2", "Result"])
    
     # ✅ Ensure the empty DataFrame is saved
     cls._history_df.to_csv(HISTORY_FILE_PATH, index=False)

     # ✅ Only delete the CSV if NOT running tests
     if "PYTEST_CURRENT_TEST" not in os.environ:
         os.remove(HISTORY_FILE_PATH) if os.path.exists(HISTORY_FILE_PATH) else None

    @classmethod
    def load_history(cls):
        """Loads calculation history from the CSV file."""
        try:
            if not os.path.exists(HISTORY_FILE_PATH) or os.path.getsize(HISTORY_FILE_PATH) == 0:
                raise FileNotFoundError("⚠️ CSV file is missing or empty.")

            # ✅ Read CSV with correct data types
            cls._history_df = pd.read_csv(
                HISTORY_FILE_PATH,
                dtype={"ID": int, "Operation": str, "Operand1": float, "Operand2": float, "Result": float}
            )

            print("\n✅ Successfully Loaded History From CSV:\n", cls._history_df)

        except (FileNotFoundError, pd.errors.EmptyDataError) as e:
            print(f"\n⚠️ No valid CSV found. Initializing empty history. {e}")
            cls._history_df = pd.DataFrame(columns=["ID", "Operation", "Operand1", "Operand2", "Result"])

    @classmethod
    def get_last_entry(cls):
        """Returns the last calculation performed."""
        if cls._history_df.empty:
            return "No history available."

        last_entry = cls._history_df.iloc[-1]
        return last_entry.to_dict()  # ✅ Convert Pandas Series to dictionary

    @classmethod
    def save_history(cls):
        """Saves the history DataFrame to a CSV file."""
        cls._history_df.to_csv(HISTORY_FILE_PATH, index=False, encoding="utf-8")

        print("\n✅ History saved to CSV successfully.")

    @classmethod
    def _generate_id(cls):
        """Generates a unique ID for each entry."""
        if cls._history_df.empty or "ID" not in cls._history_df.columns:
            return 1
        return int(cls._history_df["ID"].max() + 1)
