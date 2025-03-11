"""Division Plugin Operation"""
from decimal import Decimal
from operations.operation_base import Operation

class Divide(Operation):
    """Performs division of two numbers."""

    @staticmethod
    def execute(a: Decimal, b: Decimal) -> Decimal:
        """
        Returns the quotient of two numbers, handling division by zero.

        Args:
            a (Decimal): Dividend.
            b (Decimal): Divisor.

        Returns:
            Decimal: The quotient if b is not zero.

        Raises:
            ZeroDivisionError: If b is zero.
        """
        Divide.validate_numbers(a, b)
        return a / b

    @classmethod
    def validate_numbers(cls, a, b) -> None:
        """
        Validates that both inputs are Decimal-compatible and ensures b is not zero.

        Args:
            a: The first input (dividend).
            b: The second input (divisor).

        Raises:
            TypeError: If inputs are not Decimal-compatible.
            ZeroDivisionError: If b is zero.
        """
        for var, var_name in [(a, "a"), (b, "b")]:
            if not isinstance(var, Decimal):
                try:
                    var = Decimal(var)
                except Exception as exc:
                    raise TypeError(f"Invalid type for '{var_name}': {type(var).__name__}, expected Decimal-compatible.") from exc

        # Ensure divisor is not zero
        if b == Decimal("0"):
            raise ZeroDivisionError("Error: Division by zero!")
