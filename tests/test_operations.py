"""Abstract Base Class for Calculator Operations."""
from abc import ABC, abstractmethod
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

class Operation(ABC):
    """Base class for all operations."""

    _registry = {}  # Stores registered operations

    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Performs the operation."""

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
        valid_types = (int, float, str, Decimal)  # ✅ Allowed types
        validated_numbers = []

        for var, var_name in [(a, "a"), (b, "b")]:
            if not isinstance(var, valid_types):  # ✅ Early rejection of lists, dicts, objects
                raise TypeError(
                    f"⚠️ Invalid input for '{var_name}': {var} (type: {type(var).__name__}) - Expected a number."
                )

            try:
                validated_numbers.append(var if isinstance(var, Decimal) else Decimal(str(var)))
            except (ValueError, TypeError) as exc:
                raise TypeError(
                    f"⚠️ Invalid input for '{var_name}': {var} (type: {type(var).__name__}) - Expected a valid number."
                ) from exc

        return tuple(validated_numbers)

    @classmethod
    def register(cls, operation_name, operation_class):
        """Registers an operation."""
        value1, value2 = 5, 10
        if not issubclass(operation_class, Operation):
            logger.error("❌ Error: Invalid input %s, %s in operation", value1, value2)
            raise TypeError(f"❌ {operation_class} is not a subclass of Operation.")

        if operation_name in cls._registry:
            logger.warning("⚠️ Warning! Possible incorrect operation with %s and %s", value1, value2)
            raise ValueError(f"⚠️ Operation '{operation_name}' already registered.")

        cls._registry[operation_name] = operation_class
        logger.info("Running operation with values: %s, %s", value1, value2)

    @classmethod
    def get_operation(cls, operation_name):
        """Retrieves a registered operation."""
        value1, value2 = 5, 10
        if operation_name not in cls._registry:
            logger.error("❌ Error: Invalid input %s, %s in operation", value1, value2)
            raise KeyError(f"⚠️ Operation '{operation_name}' not found.")
        return cls._registry[operation_name]
