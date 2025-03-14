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

        Args:
            a: The first input (expected to be Decimal-compatible).
            b: The second input (expected to be Decimal-compatible).

        Returns:
            tuple[Decimal, Decimal]: The validated and converted numbers.

        Raises:
            TypeError: If a or b cannot be converted to Decimal.
        """
        validated_numbers = []
        for var, var_name in [(a, "a"), (b, "b")]:
            try:
                validated_numbers.append(Decimal(var))
            except (InvalidOperation, TypeError):
                raise TypeError(f"⚠️ Invalid input for '{var_name}': {var} (type: {type(var).__name__}) - Expected a number.")

        return tuple(validated_numbers)

# ✅ Register the operation
Operation.register("divide", Divide)
