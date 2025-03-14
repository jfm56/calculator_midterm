"""Multiplication Plugin Operation"""
from decimal import Decimal, InvalidOperation
from operations.operation_base import Operation

class Multiply(Operation):
    """Performs multiplication of two numbers."""

    @staticmethod
    def execute(a, b) -> Decimal:
        """
        Returns the product of two numbers after validation.

        Args:
            a: The first input value.
            b: The second input value.

        Returns:
            Decimal: The product of `a` and `b`.

        Raises:
            ValueError: If inputs cannot be converted to Decimal.
        """
        a, b = Multiply.validate_numbers(a, b)
        return a * b

    @classmethod
    def validate_numbers(cls, a, b) -> tuple[Decimal, Decimal]:
        """
        Ensures input values are Decimal-compatible and returns them.

        Args:
            a: The first input value.
            b: The second input value.

        Returns:
            tuple[Decimal, Decimal]: The validated and converted numbers.

        Raises:
            ValueError: If inputs cannot be converted to Decimal.
        """
        try:
            return Decimal(a), Decimal(b)  # ✅ Convert and return the values
        except (InvalidOperation, ValueError):
            raise ValueError(f"⚠️ Invalid input(s): '{a}' ({type(a).__name__}), '{b}' ({type(b).__name__}) - Expected numbers.")
