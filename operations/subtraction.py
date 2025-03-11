"""Subtraction Plugin Operation"""
from decimal import Decimal
from operations.operation_base import Operation

class Subtract(Operation):
    """Performs subtraction of two numbers."""

    @staticmethod
    def execute(a: Decimal, b: Decimal) -> Decimal:
        """Returns the difference of two numbers."""
        Subtract.validate_numbers(a, b)
        return a - b

    @classmethod
    def validate_numbers(cls, a, b) -> None:
        """Validates that both inputs are Decimal-compatible."""
        for var, var_name in [(a, "a"), (b, "b")]:
            if not isinstance(var, Decimal):
                try:
                    Decimal(var)
                except Exception as exc:
                    raise TypeError(f"Invalid type for '{var_name}': {type(var).__name__}, expected Decimal-compatible.") from exc
