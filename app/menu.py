import sys
import os
import pandas as pd
from history.history import History
from config.env import HISTORY_FILE_PATH
from config.log_config import logger

class Menu:
    """Calculator Menu - Uses LBYL (Look Before You Leap)"""

    @classmethod
    def show_menu(cls):
        """Displays the calculator menu options."""
        menu_options = (
            "\n📜 Calculator Menu:\n"
            "1️⃣ - View Calculation History\n"
            "2️⃣ - Clear Calculation History\n"
            "3️⃣ - Remove Entry by ID\n"
            "4️⃣ - Reload History from CSV\n"
            "5️⃣ - Exit Calculator"
        )
        logger.info(menu_options)

    @classmethod
    def _history_exists(cls):
        """Helper function to check if history file exists and has content."""
        return os.path.exists(HISTORY_FILE_PATH) and os.path.getsize(HISTORY_FILE_PATH) > 0

    @classmethod
    def handle_choice(cls, choice):
        """Handles user menu selections using LBYL."""
        actions = {
            "1": cls.view_history,
            "2": cls.clear_history,
            "3": cls.remove_entry,
            "4": cls.reload_history,
            "5": lambda: sys.exit(logger.info("\n👋 Exiting calculator. Goodbye!")),
        }
        actions.get(choice, lambda: logger.warning("\n❌ Invalid selection. Please try again."))()

    @classmethod
    def view_history(cls):
        """Handles viewing calculation history."""
        if cls._history_exists():
            history_df = History.get_history()
            logger.info("\n📜 Calculation History:\n%s", history_df if not history_df.empty else "⚠️ No calculations found.")
        else:
            logger.warning("\n⚠️ No history file found or it is empty.")

    @classmethod
    def clear_history(cls):
        """Clears the calculation history."""
        if cls._history_exists():
            History.clear_history()
            logger.info("\n✅ History cleared successfully!")
        else:
            logger.warning("\n⚠️ No history file to clear.")

    @classmethod
    def remove_entry(cls):
        """Removes an entry by ID."""
        if not cls._history_exists():
            logger.warning("\n⚠️ No history file exists.")
            return

        history_df = History.get_history()
        if history_df.empty:
            logger.warning("\n⚠️ No history available to remove.")
            return

        logger.info("\n📜 Current History:\n%s", history_df)
        try:
            entry_id = int(input("\n🔢 Enter the ID of the entry to remove: "))
            if entry_id in history_df["ID"].astype(int).values:
                History.remove_entry(entry_id)
                logger.info(f"\n✅ Entry ID {entry_id} removed successfully!")
            else:
                logger.warning(f"\n⚠️ Entry ID {entry_id} not found.")
        except ValueError:
            logger.error("\n❌ Invalid input. Please enter a valid numeric ID.")

    @classmethod
    def reload_history(cls):
        """Reloads history from CSV."""
        if cls._history_exists():
            History.load_history()
            logger.info("\n🔄 History reloaded from CSV!")
        else:
            logger.warning("\n⚠️ No valid history file to reload.")
