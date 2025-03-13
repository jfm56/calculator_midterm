import sys
import os
from history.history import History
from config.env import HISTORY_FILE_PATH

class Menu:
    """Calculator Menu - Uses LBYL (Look Before You Leap)"""

    @classmethod
    def show_menu(cls):
        """Displays the calculator menu options."""
        print("\n📜 Calculator Menu:")
        print("1️⃣ - View Calculation History")
        print("2️⃣ - Clear Calculation History")
        print("3️⃣ - Remove Entry by ID")
        print("4️⃣ - Reload History from CSV")
        print("5️⃣ - Exit Calculator")

    @classmethod
    def handle_choice(cls, choice):
        """Handles user menu selections using LBYL."""
        
        if choice == "1":
            cls.view_history()
        elif choice == "2":
            cls.clear_history()
        elif choice == "3":
            cls.remove_entry()
        elif choice == "4":
            cls.reload_history()
        elif choice == "5":
            print("\n👋 Exiting calculator. Goodbye!")
            sys.exit(0)
        else:
            print("\n❌ Invalid selection. Please try again.")

    @classmethod
    def view_history(cls):
        """Handles viewing calculation history."""
        if os.path.exists(HISTORY_FILE_PATH) and os.path.getsize(HISTORY_FILE_PATH) > 0:
            history_df = History.get_history()
            print("\n📜 Calculation History:\n", history_df if not history_df.empty else "⚠️ No calculations found.")
        else:
            print("\n⚠️ No history file found or it is empty.")

    @classmethod
    def clear_history(cls):
        """Clears the calculation history."""
        if os.path.exists(HISTORY_FILE_PATH) and os.path.getsize(HISTORY_FILE_PATH) > 0:
            History.clear_history()
            print("\n✅ History cleared successfully!")
        else:
            print("\n⚠️ No history file to clear.")

    @classmethod
    def remove_entry(cls):
        """Removes an entry by ID."""
        if os.path.exists(HISTORY_FILE_PATH) and os.path.getsize(HISTORY_FILE_PATH) > 0:
            history_df = History.get_history()
            if not history_df.empty:
                print("\n📜 Current History:\n", history_df)
                try:
                    entry_id = int(input("\n🔢 Enter the ID of the entry to remove: "))
                    if entry_id in history_df["ID"].astype(int).values:
                        History.remove_entry(entry_id)
                        print(f"\n✅ Entry ID {entry_id} removed successfully!")
                    else:
                        print(f"\n⚠️ Entry ID {entry_id} not found.")
                except ValueError:
                    print("\n❌ Invalid input. Please enter a valid numeric ID.")
            else:
                print("\n⚠️ No history available to remove.")
        else:
            print("\n⚠️ No history file exists.")

    @classmethod
    def reload_history(cls):
        """Reloads history from CSV."""
        if os.path.exists(HISTORY_FILE_PATH) and os.path.getsize(HISTORY_FILE_PATH) > 0:
            History.load_history()
            print("\n🔄 History reloaded from CSV!")
        else:
            print("\n⚠️ No valid history file to reload.")
