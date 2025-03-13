"""Handles the calculator REPL menu system."""
import os
import sys

# ✅ Get the absolute path of the `app/` directory dynamically
APP_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(APP_DIR))  # ✅ Adds the project root dynamically

class Menu:
    """Handles the calculator REPL menu system."""

    options = {
        "1": "Perform Calculation",
        "2": "View History",
        "3": "Filter History by Operation",
        "4": "Clear History",
        "5": "Exit"
    }

    @classmethod
    def display_menu(cls):
        """Displays the calculator menu."""
        print("\n===== Calculator Menu =====")
        for key, value in cls.options.items():
            print(f"{key}. {value}")
        print("===========================")

    @classmethod
    def get_user_choice(cls):
        """Gets the user's menu selection."""
        choice = input("Enter your choice: ").strip()
        return choice if choice in cls.options else None

    @classmethod
    def handle_choice(cls, choice):
        """Handles menu choices."""
        if choice == "1":
            from main import CalculatorREPL  # ✅ Import inside function to prevent circular import
            CalculatorREPL.run()
        elif choice == "5":
            print("\nGoodbye! 👋")
            sys.exit()
        else:
            print("\n⚠️ Invalid choice, please try again.")

    @classmethod
    def run(cls):
        """Runs the menu loop."""
        while True:
            cls.display_menu()
            choice = cls.get_user_choice()
            cls.handle_choice(choice)
