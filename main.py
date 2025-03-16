"""
Main entry point for the interactive command-line calculator.
"""

import sys
import logging
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

from history.history import History
from mappings.operations_map import operation_mapping
from app.menu import Menu
from operations import operation_base

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger("calculator_logger")


class CalculatorREPL:
    """Interactive Read-Eval-Print Loop (REPL) for the calculator."""

    @staticmethod
    def start():
        """Starts the interactive calculator loop."""
        print("\n✨ Welcome to the Interactive Calculator! ✨")
        CalculatorREPL.display_instructions()

        try:
            while True:
                command = input("\n📝 Enter command: ").strip().lower()
                if command == "exit":
                    print("👋 Exiting calculator.")
                    logger.info("👋 Exiting calculator.")
                    sys.exit(0)
                elif command == "menu":
                    Menu.show_menu()
                elif command == "history":
                    Menu.show_history()
                elif command == "clear":
                    Menu.clear_history()
                elif command == "help":
                    CalculatorREPL.display_instructions()
                else:
                    CalculatorREPL.process_calculation(command)

        except KeyboardInterrupt:
            print("\n👋 Exiting calculator.")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            logger.error(f"Unexpected error: {e}")

    @staticmethod
    def display_instructions():
        """Displays usage instructions for the REPL."""
        print("📌 Instructions:")
        print("🔹 Type 'menu' to see available operations.")
        print("🔹 Type 'exit' to quit the calculator.")
        print("🔹 To perform calculations, enter: `<operation> <num1> <num2>` (e.g., `add 2 3`).")
        print("🔹 To use statistical operations, enter: `<operation> <num1> <num2> <num3> ...` (e.g., `mean 10 20 30`).")
        print("🔹 Type 'history' to view past calculations.")
        print("🔹 Type 'clear' to erase calculation history.")
        print("🔹 Type 'help' to display this message again.")

    @staticmethod
    def process_calculation(command):
        """Processes user commands for calculations."""
        parts = command.split()

        if not parts:
            print("⚠️ Invalid format. Expected: <operation> <num1> <num2> ...")
            return

        operation_name = parts[0]

        # 🔹 Fix: Check for unknown operations before processing numbers
        if operation_name not in operation_mapping:
            print(f"❌ Unknown operation: '{operation_name}'. Type 'menu' for options.")
            return

        try:
            numbers = [Decimal(num) for num in parts[1:]]
        except InvalidOperation:
            print("⚠️ Invalid number format. Ensure all values are numeric.")
            return

        try:
            # ✅ Corrected key lookup
            result = operation_mapping[operation_name].execute(*numbers)
            formatted_result = result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            # ✅ Corrected argument for history
            print(f"✅ Result: {formatted_result}")
            History.add_entry(operation_name, list(numbers), formatted_result)

        except ZeroDivisionError:
            print("❌ Division by zero is not allowed.")
            logger.error("Attempted division by zero.")
        except Exception as e:
            print(f"❌ Error: {e}")
            logger.error(f"Error during calculation ({command}): {e}")


if __name__ == "__main__":
    CalculatorREPL.start()
