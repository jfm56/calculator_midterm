"""
Calculator Menu Module - Handles user interactions via menu
"""
import logging
import sys
from history.history import History
from mappings.operations_map import operation_mapping

# ✅ Setup logger
logger = logging.getLogger("calculator_logger")

class Menu:
    """Handles interactive menu actions for the calculator."""

    @classmethod
    def show_menu(cls):
        """Displays calculator menu including all available operations."""
        
        operations_list = sorted(operation_mapping.keys())
        operations_display = ', '.join(operations_list)

        menu_text = f"""
📜 Calculator Menu:
==============================
🔹 Available Operations:
{operations_display}

🔸 Menu Options:
1️⃣ - View Calculation History
2️⃣ - Clear Calculation History
3️⃣ - Remove Entry by ID
4️⃣ - Reload History from CSV
5️⃣ - Exit Calculator
==============================
"""
        print(menu_text)  # ✅ Display only in console
        logger.info("📜 Menu displayed.")  # ✅ Log as a simple message

    @classmethod
    def handle_choice(cls, choice):
        """Handles user selection from the menu."""
        actions = {
            "1": cls.view_history,
            "2": cls.clear_history,
            "3": cls.remove_entry,
            "4": cls.reload_history,
            "5": cls.exit_program
        }
        action = actions.get(choice, cls.invalid_choice)
        action()

    @classmethod
    def view_history(cls):
        """Displays the calculation history without duplicate logging."""
        history_df = History.get_history()

        if history_df.empty:
            message = "\n⚠️ No calculations found."
            print(message)  # ✅ Show only in console
            logger.warning("⚠️ No calculations found.")  # ✅ Log without duplication
        else:
            print("\n📜 Calculation History:")
            print(history_df.to_string(index=False))  # ✅ Print clean output
            logger.info("📜 Calculation history viewed.")  # ✅ Silent log

    @classmethod
    def clear_history(cls):
        """Clears the calculation history."""
        confirmation = input("\n🛑 Are you sure you want to clear history? (yes/no): ").strip().lower()
        if confirmation == "yes":
            History.clear_history()
            print("\n✅ History cleared successfully!")
            logger.info("✅ History cleared successfully.")  # ✅ Silent log
        else:
            print("\n🚫 History clear operation cancelled.")
            logger.info("🚫 History clear operation cancelled.")  # ✅ Silent log

    @classmethod
    def remove_entry(cls):
        """Removes an entry from history by ID."""
        history_df = History.get_history()

        if history_df.empty:
            print("\n⚠️ No history available to remove.")
            logger.warning("⚠️ No history available to remove.")
            return

        print("\n📜 Current History:")
        print(history_df.to_string(index=False))

        try:
            entry_id = int(input("\n🔢 Enter the ID of the entry to remove: ").strip())

            if entry_id not in history_df["ID"].values:
                print(f"\n⚠️ Entry with ID {entry_id} not found.")
                logger.warning(f"⚠️ Entry with ID {entry_id} not found.")
                return

            History.remove_entry(entry_id)
            print(f"\n✅ Entry {entry_id} removed successfully.")
            logger.info(f"✅ Entry {entry_id} removed successfully.")

        except ValueError:
            print("\n❌ Invalid input. Please enter a numeric ID.")
            logger.warning("❌ Invalid input. Non-numeric entry ID entered.")

    @classmethod
    def reload_history(cls):
        """Reloads history from CSV."""
        History.get_history()  # ✅ Correct method to load history
        print("\n🔄 History reloaded successfully.")
        logger.info("🔄 History reloaded successfully.")

    @classmethod
    def exit_program(cls):
        """Exits the calculator program."""
        print("\n👋 Exiting calculator. Goodbye!")
        logger.info("👋 Exiting calculator. Goodbye!")
        sys.exit(0)

    @staticmethod
    def invalid_choice():
        """Handles invalid menu selections."""
        print("\n❌ Invalid selection. Please try again.")
        logger.warning("❌ Invalid selection made in menu.")

__all__ = ["Menu"]
