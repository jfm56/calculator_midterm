"""Addition Plugin Operation"""
from decimal import Decimal
from operations.operation_base import Operation

class Add(Operation):
    """Performs addition of two numbers."""

    @staticmethod
    def execute(a, b) -> Decimal:
        """Returns the sum of two numbers."""
        a, b = Add.validate_numbers(a, b)  # ✅ Convert numbers if needed
        return a + b

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
            ValueError: If a or b cannot be converted to Decimal.
        """
        validated_numbers = []
        for var, var_name in [(a, "a"), (b, "b")]:
            try:
                validated_numbers.append(Decimal(var))
            except Exception:
                raise ValueError(f"⚠️ Invalid input for '{var_name}': {var} (type: {type(var).__name__}) - Expected a number.")
        
        return tuple(validated_numbers)  # ✅ Return as a tuple for unpacking
