"""Division Plugin Operation"""
from decimal import Decimal, InvalidOperation
from operations.operation_base import Operation

class Divide(Operation):
    """Performs division of two numbers."""

    @staticmethod
    def execute(a, b) -> Decimal:
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
        a, b = Divide.validate_numbers(a, b)  # ✅ Convert first
        return a / b

    @classmethod
    def validate_numbers(cls, a, b) -> tuple[Decimal, Decimal]:
        """
        Validates that both inputs are Decimal-compatible and ensures b is not zero.

        Args:
            a: The first input (dividend).
            b: The second input (divisor).

        Returns:
            tuple[Decimal, Decimal]: The validated and converted numbers.

        Raises:
            ValueError: If inputs cannot be converted to Decimal.
            ZeroDivisionError: If b is zero.
        """
        validated_numbers = []
        for var, var_name in [(a, "a"), (b, "b")]:
            try:
                validated_numbers.append(Decimal(var))
            except (InvalidOperation, ValueError):
                raise ValueError(f"⚠️ Invalid input for '{var_name}': {var} (type: {type(var).__name__}) - Expected a number.")

        # ✅ Ensure divisor is not zero AFTER conversion
        if validated_numbers[1] == Decimal("0"):
            raise ZeroDivisionError("❌ Division by zero is not allowed (b = 0).")

        return tuple(validated_numbers)  # ✅ Return validated numbers
