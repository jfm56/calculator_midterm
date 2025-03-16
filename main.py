"""
Main Calculator Program - Interactive Menu & REPL
"""
from app.menu import Menu
from mappings.operations_map import operation_mapping  # ✅ Corrected import
from history.history import History
from config.log_config import logger
from operations.operation_base import Operation

class CalculatorREPL:
    """Handles the interactive Read-Eval-Print Loop (REPL) for the calculator."""

    @classmethod
    def repl(cls):
        """Starts the REPL loop."""
        print("\n✨ Welcome to the Interactive Calculator! ✨")
        while True:
            command = input("Enter command: ").strip().lower()

            if command == "exit":
                print("👋 Exiting calculator. Goodbye!")
                logger.info("👋 Exiting calculator.")
                break
            elif command == "menu":
                Menu.show_menu()
            else:
                cls.process_calculation(command)

    @classmethod
    def run_operation(cls, operation_name, a, b):
        """Runs a registered operation."""
        try:
            logger.info(f"📝 Running operation: {operation_name} with inputs {a}, {b}")
            operation = Operation.get_operation(operation_name)

            # ✅ Ensure valid input conversion
            a, b = operation.validate_numbers(a, b)

            # ✅ Handle division by zero explicitly
            if operation_name == "divide" and b == 0:
                raise ZeroDivisionError("❌ Division by zero is not allowed.")

            result = operation.execute(a, b)
            logger.info(f"✅ Operation successful: {operation_name}({a}, {b}) = {result}")
            return result

        except KeyError:
            logger.error(f"❌ Operation '{operation_name}' not found.")
            raise KeyError(f"⚠️ Operation '{operation_name}' not found.")
        except ZeroDivisionError as e:
            logger.error(f"❌ {e}")
            raise  # ✅ Now correctly raises the error
        except Exception as e:
            logger.error(f"❌ Error during operation '{operation_name}': {e}")
            raise

    @staticmethod
    def start():
        """Starts the interactive calculator REPL."""
        print("\n✨ Welcome to the Interactive Calculator! ✨")
        print("🔹 Type 'menu' to see available options.")
        print("🔹 Type 'exit' to quit the calculator.")
        print("🔹 To calculate: Enter operation followed by two numbers (e.g., 'add 2 3').\n")

        logger.info("📢 Calculator started!")

        while True:
            command = input("👉 Enter command: ").strip().lower()
            logger.info(f"📝 User entered command: {command}")

            if command == "menu":
                Menu.show_menu()
            elif command == "exit":
                print("👋 Exiting calculator. Goodbye!")
                logger.info("👋 Exiting calculator.")
                break
            elif command in {"1", "2", "3", "4"}:
                Menu.handle_choice(command)
            else:
                CalculatorREPL.process_calculation(command)

    @staticmethod
    def process_calculation(command: str):
        """Processes a calculation command entered in the REPL and logs it to history."""
        try:
            parts = command.split()
            if len(parts) != 3:
                print("❌ Error: ⚠️ Invalid format. Expected: operation num1 num2")
                return

            operation_name, num1, num2 = parts[0], parts[1], parts[2]

            if operation_name not in operation_mapping:
                print(f"❌ Unknown operation: '{operation_name}'. Type 'menu' for options.")
                return

            operation = operation_mapping[operation_name]
            num1, num2 = operation.validate_numbers(num1, num2)
            result = operation.execute(num1, num2)

            # ✅ Log to history after successful calculation
            History.add_entry(operation_name, num1, num2, result)

            print(f"✅ Result: {result}")

        except ZeroDivisionError as e:
            print(f"{e}")  # Handle division by zero properly
        except TypeError as e:
            print(f"⚠️ Invalid input: {e}")
        except Exception as e:
            print(f"🚨 Unexpected error: {e}")

    @classmethod
    def get_available_operations(cls):
        """Returns a list of available operations."""
        return list(operation_mapping.keys())  # ✅ Updated reference

if __name__ == "__main__":
    CalculatorREPL.start()
