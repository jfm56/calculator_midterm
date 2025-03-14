"""
Main Calculator Program - Interactive Menu & REPL
"""
import logging
from app.menu import Menu
from mappings.operations_map import operation_mapping
from history.history import History
from config.log_config import logger

def main():
    """Runs the interactive calculator program."""
    print("\n✨ Welcome to the Interactive Calculator! ✨")
    print("🔹 Type 'menu' to see available options.")
    print("🔹 Type 'exit' to quit the calculator.")
    print("🔹 To calculate: Enter operation followed by two numbers (e.g., 'add 2 3').\n")

    logger.info("📢 Calculator started!")

    while True:
        command = input("👉 Enter command: ").strip().lower()

        if command == "menu":
            Menu.show_menu()
        elif command == "exit":
            print("👋 Exiting calculator. Goodbye!")
            logger.info("👋 Exiting calculator.")
            break
        elif command in {"1", "2", "3", "4"}:  # Menu options
            Menu.handle_choice(command)
        else:
            process_calculation(command)  # Try to process as a calculation

def process_calculation(command):
    """Processes arithmetic commands (e.g., 'add 2 3')."""
    try:
        parts = command.split()
        if len(parts) != 3:
            raise ValueError("⚠️ Invalid format. Expected: operation num1 num2")

        operation, num1, num2 = parts[0], float(parts[1]), float(parts[2])

        if operation in operation_mapping:
            result = operation_mapping[operation]().execute(num1, num2)
            print(f"✅ Result: {result}")  # ✅ User message
            logger.info(f"🧮 Calculation performed: {operation} {num1} {num2} = {result}")  # ✅ Silent log
            History.add_entry(operation, num1, num2, result)  # Save calculation
        else:
            print(f"❌ Unknown operation: '{operation}'. Type 'menu' for options.")  # ✅ User message
            logger.warning(f"❌ Invalid operation attempted: {operation}")  # ✅ Silent log

    except ValueError as e:
        print(f"❌ Error: {e}")  # ✅ User message
        logger.error(f"❌ Input error: {e}")  # ✅ Silent log

if __name__ == "__main__":
    main()
