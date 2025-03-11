"""Addition Plugin Operation"""
from decimal import Decimal
from operations.operation_base import Operation

class Add(Operation):
    """Performs addition of two numbers."""

    @staticmethod
    def execute(a: Decimal, b: Decimal) -> Decimal:
        """Returns the sum of two numbers."""
        Add.validate_numbers(a, b)
        return a + b

    @classmethod
    def validate_numbers(cls, a, b) -> None:
        """
        Validates that both inputs are numbers and converts them to Decimal if needed.

        Args:
            a: The first input (expected to be Decimal-compatible).
            b: The second input (expected to be Decimal-compatible).

        Raises:
            TypeError: If a or b cannot be converted to Decimal.
        """
        for var, var_name in [(a, "a"), (b, "b")]:
            if not isinstance(var, Decimal):
                try:
                    Decimal(var)
                except Exception as exc:
                    raise TypeError(f"Invalid type for '{var_name}': {type(var).__name__}, expected Decimal-compatible.") from exc
