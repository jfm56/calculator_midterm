"""Division Plugin Operation"""
from decimal import Decimal, InvalidOperation, DivisionByZero
from .operation_base import Operation

class Divide(Operation):
    """Performs division of two numbers, handling division by zero."""

    @staticmethod
    def execute(a, b) -> Decimal:
        """Returns the quotient of two numbers."""
        a, b = Divide.validate_numbers(a, b)  # ✅ Convert numbers if needed
        if b == 0:
            raise ZeroDivisionError("❌ Division by zero is not allowed.")
        return a / b

    @classmethod
    def validate_numbers(cls, a, b) -> tuple[Decimal, Decimal]:
        """
        Validates that both inputs are numbers and converts them to Decimal if needed.

        Raises:
            TypeError: If a or b is a boolean, list, dict, or cannot be converted to Decimal.
        """
        # 🚨 Explicitly reject booleans, lists, and dictionaries
        if isinstance(a, (bool, list, dict)) or isinstance(b, (bool, list, dict)):
            raise TypeError(f"⚠️ Invalid input: {repr(a)} ({type(a).__name__}) or {repr(b)} ({type(b).__name__}) - Invalid type.")

        validated_numbers = []
        for var, var_name in [(a, "a"), (b, "b")]:
            try:
                validated_numbers.append(Decimal(var))
            except Exception:
                raise TypeError(f"⚠️ Invalid input for '{var_name}': {repr(var)} ({type(var).__name__}) - Expected a number.")

        return tuple(validated_numbers)



# ✅ Register the operation
Operation.register("divide", Divide)
