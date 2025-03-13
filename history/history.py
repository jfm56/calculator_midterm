"""Manages calculation history using Pandas for data storage and retrieval."""
import os
import pandas as pd
from config.env import HISTORY_FILE_PATH

print(f"\n🔍 Checking CSV File Path: {HISTORY_FILE_PATH}")
print(f"📁 File Exists? {os.path.exists(HISTORY_FILE_PATH)}")
print(f"📏 File Size: {os.path.getsize(HISTORY_FILE_PATH)} bytes")


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

        print(f"\n❌ Removing entry with ID {entry_id}...")

        # ✅ Ensure ID column is treated as an integer for filtering
        cls._history_df["ID"] = cls._history_df["ID"].astype(int)

        # ✅ Remove the entry
        before_removal = cls._history_df.copy()  # Debugging: Save before removal
        cls._history_df = cls._history_df[cls._history_df["ID"] != entry_id]

        print("\n🗑️ Before Removing Entry:")
        print(before_removal)

        print("\n✅ After Removing Entry:")
        print(cls._history_df)

        # ✅ Save updated history (even if empty)
        cls.save_history()

    @classmethod
    def reconstitute_entry(cls, record):
        """
        Converts a CSV record read by Pandas into a dictionary.

        Args:
            record (pd.Series): A row from the history DataFrame.

        Returns:
            dict: Converted record as a dictionary.
        """
        if isinstance(record, pd.Series):
            return record.to_dict()
        raise TypeError("⚠️ Invalid record format. Expected Pandas Series.")

    @classmethod
    def clear_history(cls):
        """Clears all stored history but ensures the CSV structure remains."""
        cls._history_df = pd.DataFrame(columns=["ID", "Operation", "Operand1", "Operand2", "Result"])
    
        # ✅ Save an empty DataFrame with headers to avoid reloading issues
        cls._history_df.to_csv(HISTORY_FILE_PATH, index=False, encoding="utf-8")

        print("\n✅ History cleared and structure retained.")

    @classmethod
    def load_history(cls):
        """Loads calculation history from the CSV file."""
        try:
            if not os.path.exists(HISTORY_FILE_PATH) or os.path.getsize(HISTORY_FILE_PATH) == 0:
                print("⚠️ CSV file missing or empty. Initializing empty history.")
                cls._history_df = pd.DataFrame(columns=["ID", "Operation", "Operand1", "Operand2", "Result"])
                return

            print("\n✅ CSV Exists, Attempting to Read...")

            # 🚨 Force pandas to treat all columns as strings
            temp_df = pd.read_csv(
                HISTORY_FILE_PATH,
                dtype=str,
                skip_blank_lines=True,
                encoding="utf-8",
                keep_default_na=False,  # Prevent misinterpretation of empty strings as NaN
            )

            print("\n📂 CSV Read Output Before Processing (RAW DataFrame):")
            print(temp_df)

            if temp_df.empty or temp_df.isnull().all().all():
                print("⚠️ CSV exists but contains no valid data after cleaning. Initializing empty history.")
                cls._history_df = pd.DataFrame(columns=["ID", "Operation", "Operand1", "Operand2", "Result"])
            else:
                # 🚨 Convert data types explicitly
                temp_df["ID"] = pd.to_numeric(temp_df["ID"], errors="coerce").fillna(0).astype(int)
                temp_df["Operand1"] = pd.to_numeric(temp_df["Operand1"], errors="coerce")
                temp_df["Operand2"] = pd.to_numeric(temp_df["Operand2"], errors="coerce")
                temp_df["Result"] = pd.to_numeric(temp_df["Result"], errors="coerce")

                cls._history_df = temp_df.dropna()
                print("\n✅ Successfully Loaded History From CSV (Final DataFrame):")
                print(cls._history_df)

        except Exception as e:
            print(f"\n❌ Error loading CSV: {e}")
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
        """Ensures history is saved correctly, even when empty."""
    
        print("\n✅ Saving history to CSV:")
        print(cls._history_df)

        # ✅ Ensure the CSV is updated even if history is empty
        cls._history_df.to_csv(HISTORY_FILE_PATH, index=False, encoding="utf-8")

        print(f"\n✅ History successfully saved to {HISTORY_FILE_PATH}")

    @classmethod
    def _generate_id(cls):
        """Generates a unique ID for each entry."""
        if cls._history_df.empty or "ID" not in cls._history_df.columns:
            return 1
        return int(cls._history_df["ID"].max() + 1)
