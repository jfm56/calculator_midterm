"""
Abstract Base Class for Calculator Operations.
"""

from abc import ABC, abstractmethod
import abc
from decimal import Decimal, InvalidOperation
import logging

logger = logging.getLogger 

class Operation(ABC):
    """
    Abstract base class for all operations.
    Each operation must implement the `execute` method.
    """

    # ✅ Operation registry to store registered operation classes
    _registry = {}

    @staticmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute the operation and return the result.

        Args:
            a (Decimal): The first operand.
            b (Decimal): The second operand.

        Returns:
            Decimal: The result of the operation.
        """
        pass  # ✅ Keep the method abstract

        @classmethod
        def validate_numbers(cls, a, b) -> tuple[Decimal, Decimal]:
            """
            Validates that both inputs are numbers and converts them to Decimal if needed.
            """
            logger.debug(f"🔍 Validating inputs - a: {a} (type: {type(a).__name__}), b: {b} (type: {type(b).__name__})")

            validated_numbers = []
            for var, var_name in [(a, "a"), (b, "b")]:
                if isinstance(var, (list, dict, object)):
                    logger.error(f"❌ Invalid input for '{var_name}': {var} (type: {type(var).__name__}) - Expected a number.")
                    raise TypeError(f"⚠️ Invalid input for '{var_name}': {var} (type: {type(var).__name__}) - Expected a number.")

                try:
                    validated_numbers.append(Decimal(str(var)))  # ✅ Convert safely
                except (InvalidOperation, ValueError):
                    logger.error(f"❌ Cannot convert '{var_name}' to Decimal: {var} (type: {type(var).__name__})")
                    raise TypeError(f"⚠️ Cannot convert '{var_name}' to Decimal: {var}")

            logger.debug(f"✅ Converted values - a: {validated_numbers[0]}, b: {validated_numbers[1]}")
            return tuple(validated_numbers)

    @classmethod
    def register(cls, operation_name, operation_class):
        """
        Registers an operation class under a specific name.

        Args:
            operation_name (str): The operation keyword (e.g., "add", "subtract").
            operation_class (Type[Operation]): The class implementing the operation.

        Raises:
            ValueError: If the operation is already registered.
        """
        if not issubclass(operation_class, Operation):
            raise TypeError(f"❌ {operation_class} is not a subclass of Operation.")

        if operation_name in cls._registry:
            raise ValueError(f"⚠️ Operation '{operation_name}' is already registered.")

        cls._registry[operation_name] = operation_class

    @classmethod
    def get_operation(cls, operation_name):
        """
        Retrieves a registered operation by name.

        Args:
            operation_name (str): The operation keyword.

        Returns:
            Type[Operation]: The class corresponding to the operation name.

        Raises:
            KeyError: If the operation is not registered.
        """
        if operation_name not in cls._registry:
            raise KeyError(f"⚠️ Operation '{operation_name}' not found in registry.")
        return cls._registry[operation_name]

    @abc.abstractmethod
    def execute(self, operand1, operand2):
        """Executes the operation. Must be implemented by subclasses."""
        pass
