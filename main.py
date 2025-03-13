"""Calculator REPL (Read-Eval-Print Loop)"""
import os
import sys
from decimal import Decimal, InvalidOperation

# ✅ Get absolute path dynamically
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

from operations.operation_base import Operation
from config import plugins
from history.history import History
from config.log_config import logger

logger.info("Calculator started")

plugins.load_plugins()

class CalculatorREPL:
    """Command-line Read-Eval-Print Loop (REPL) for the calculator."""

    @staticmethod
    def run_operation(operation_name, a: Decimal, b: Decimal):
        """
        Executes a calculator operation dynamically from the plugin system.

        Args:
            operation_name (str): The operation name (e.g., "add", "subtract").
            a (Decimal): First operand.
            b (Decimal): Second operand.

        Returns:
            Decimal | str: The result or an error message.
        """
        try:
            operation_class = Operation.registry[operation_name.lower()]
            result = operation_class.execute(a, b)  # Ensure it calls the correct function
            History.add_entry(operation_name, a, b, result)
            return result
        except KeyError:
            return f"Operation '{operation_name}' not found."
        except ZeroDivisionError:
            return "Error: Division by zero is not allowed."

    @classmethod
    def repl(cls):
        """Starts the interactive REPL session."""
        print("\n== Welcome to REPL Calculator ==")
        print("Type 'menu' for options, or enter calculations (e.g., add 2 3).")

        from app.menu import Menu  # ✅ Delayed import to prevent circular import

        commands = {
            "menu": Menu.run,
            "history": lambda: print("\n".join(History.get_history())),
            "last": lambda: print(History.get_last_entry()),
            "clear": lambda: (History.clear_history(), print("History cleared.")),
            "exit": lambda: sys.exit("Exiting calculator. Goodbye!"),
            "quit": lambda: sys.exit("Exiting calculator. Goodbye!"),
        }

        while True:
            user_input = input(">> ").strip().lower()

            # Try executing a command first
            try:
                if user_input in commands:
                    commands[user_input]()
                    continue
            except SystemExit:
                break  # Exit cleanly

            # Try executing an arithmetic operation
            try:
                parts = user_input.split()

                if len(parts) != 3:
                    print("Error: Invalid format! Use: <operation> <number1> <number2>")
                    continue

                operation, a, b = parts

                try:
                    a, b = Decimal(a), Decimal(b)
                except InvalidOperation:
                    print("Error: Invalid number format! Ensure you're using numeric values.")
                    continue

                result = cls.run_operation(operation, a, b)
                print(f"Result: {result}")

            except Exception as e:
                print(f"Unexpected error: {e}")

if __name__ == "__main__":
    CalculatorREPL.repl()
