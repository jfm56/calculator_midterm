"""
Abstract Base Class for Calculator Operations.
"""

from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation

class Operation(ABC):
    """
    Abstract base class for all operations.
    Each operation must implement the `execute` method.
    """

    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute the operation and return the result.

        Args:
            a (Decimal): The first operand.
            b (Decimal): The second operand.

        Returns:
            Decimal: The result of the operation.
        """
        pass

    @classmethod
    def validate_numbers(cls, a, b) -> tuple[Decimal, Decimal]:
        """
        Validates that both inputs are numbers and converts them to Decimal.

        Args:
            a: The first input (expected to be numeric).
            b: The second input (expected to be numeric).

        Returns:
            tuple[Decimal, Decimal]: The validated and converted numbers.

        Raises:
            ValueError: If a or b cannot be converted to Decimal.
        """
        validated_numbers = []
        for var, var_name in [(a, "a"), (b, "b")]:
            try:
                validated_numbers.append(Decimal(var))
            except (InvalidOperation, TypeError, ValueError):
                raise ValueError(f"⚠️ Invalid input for '{var_name}': {var} (type: {type(var).__name__}) - Expected a number.")

        return tuple(validated_numbers)
