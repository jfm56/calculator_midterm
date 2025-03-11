"""Interactive Menu Module for Calculator"""

from operations.operation_base import Operation
from history.history import History

def show_menu():
    """Displays an interactive calculator menu."""

    menu_options = {
        "1": lambda: print("\nAvailable Operations:\n" + "\n".join(f"  - {op}" for op in sorted(Operation.registry.keys()))),
        "2": lambda: print("\nCalculation History:\n" + History.get_history()),
        "3": lambda: print("\nLast Calculation:\n" + History.get_last_entry()),
        "4": lambda: (History.clear_history(), print("\nHistory cleared successfully.")),
        "5": lambda: print("\nExiting menu..."),
    }

    while True:
        print("\n=== Calculator Menu ===")
        print("1. View Available Operations")
        print("2. Show Calculation History")
        print("3. Show Last Calculation")
        print("4. Clear Calculation History")
        print("5. Exit Menu")

        try:
            choice = input("\nSelect an option (1-5): ").strip()
            menu_options[choice]()  # Try executing the selected menu option
            if choice == "5":
                break  # Exit loop if user selects option 5
        except KeyError:
            print("\nInvalid selection! Please choose a valid option.")
