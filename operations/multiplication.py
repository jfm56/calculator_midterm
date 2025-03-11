"""Multiplication Plugin Operation"""
from decimal import Decimal
from operations.operation_base import Operation

class Multiply(Operation):
    """Performs multiplication of two numbers."""

    @staticmethod
    def execute(a, b):
        """Returns the product of two numbers."""
        a, b = Multiply.validate_numbers(a, b)
        return a * b

    @classmethod
    def validate_numbers(cls, a, b):
        """Ensures input values are Decimal-compatible and returns them."""
        try:
            return Decimal(a), Decimal(b)  # ✅ Convert and return the values
        except Exception as exc:
            raise TypeError(f"Invalid type: {type(a).__name__}, {type(b).__name__}") from exc
