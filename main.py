import sys
from decimal import Decimal, InvalidOperation
from config import plugins
from config.log_config import logger
from history.history import History
from operations.operation_base import Operation
from app.menu import Menu  

plugins.load_plugins()

class CalculatorREPL:
    """Command-line Read-Eval-Print Loop (REPL) for the calculator."""

    @classmethod
    def get_available_operations(cls):
        """Returns a list of available operations."""
        return list(Operation.registry.keys())

    @classmethod
    def run_operation(cls, operation_name, a: Decimal, b: Decimal):
        """Executes a calculator operation dynamically from the plugin system."""
        try:
            operation_class = Operation.registry.get(operation_name.lower())
            if not operation_class:
                return f"❌ Operation '{operation_name}' not found."
            
            result = operation_class.execute(a, b)
            History.add_entry(operation_name, a, b, result)
            return result

        except ZeroDivisionError:
            return "❌ Error: Division by zero is not allowed."

        except Exception as e:
            return f"❌ Unexpected error: {e}"

    @classmethod
    def repl(cls):
        """Starts the interactive REPL session."""
        print("\n== Welcome to REPL Calculator ==")
        print("Type 'menu' for options, or enter calculations (e.g., add 2 3).")

        commands = {
            "menu": Menu.show_menu,
            "history": lambda: logger.info(History.get_history()),
            "clear": lambda: (History.clear_history(), logger.info("History cleared.")),
            "remove": lambda: Menu.handle_choice("3"),
            "reload": lambda: Menu.handle_choice("4"),
            "exit": lambda: sys.exit("Exiting calculator. Goodbye!"),
        }

        while True:
            user_input = input(">> ").strip().lower()

            if user_input in commands:
                commands[user_input]()
                continue

            parts = user_input.split()
            if len(parts) != 3:
                logger.error("Invalid format! Use: <operation> <number1> <number2>")
                continue

            operation, a, b = parts
            try:
                a, b = Decimal(a), Decimal(b)
            except InvalidOperation:
                logger.error("Invalid number format! Ensure you're using numeric values.")
                continue

            result = cls.run_operation(operation, a, b)
            logger.info(f"🧮 Result: {result}")

if __name__ == "__main__":
    CalculatorREPL.repl()
