"""
Abstract Base Class for Calculator Operations.
"""

from abc import ABC, abstractmethod
import logging
from decimal import Decimal, InvalidOperation

logger = logging.getLogger(__name__)

class Operation(ABC):
    """Base class for all operations."""

    _registry = {}  # Stores registered operations

    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Performs the operation."""

    @classmethod
    def validate_numbers(cls, a, b) -> tuple[Decimal, Decimal]:
        """Convert inputs to Decimals or raise TypeError for invalid inputs."""
    
        # 🚨 Explicitly reject booleans
        if isinstance(a, bool) or isinstance(b, bool):
            error_msg = f"⚠️ Invalid input: {repr(a)} ({type(a).__name__}) or {repr(b)} ({type(b).__name__}) - Boolean values are not allowed."
            logger.error(error_msg)
            raise TypeError(error_msg)

        try:
            validated_a = Decimal(str(a))
            validated_b = Decimal(str(b))
            logger.debug(f"✅ Validated inputs: {validated_a}, {validated_b}")
            return validated_a, validated_b
        except (InvalidOperation, ValueError, TypeError) as exc:
            error_msg = f"⚠️ Invalid input: {repr(a)} ({type(a).__name__}) or {repr(b)} ({type(b).__name__}) - Expected a number."
            logger.error(error_msg)
            raise TypeError(error_msg) from exc

    @classmethod
    def register(cls, operation_name, operation_class):
        """Registers an operation."""
        if not issubclass(operation_class, Operation):
            logger.error(f"❌ Invalid class '{operation_class}' registration attempt.")
            raise TypeError(f"❌ {operation_class} is not a subclass of Operation.")

        if operation_name in cls._registry:
            logger.warning(f"⚠️ Duplicate registration: '{operation_name}'.")
            raise ValueError(f"⚠️ Operation '{operation_name}' already registered.")

        cls._registry[operation_name] = operation_class
        logger.info(f"✅ Registered: {operation_name}")

    @classmethod
    def get_operation(cls, operation_name):
        """Retrieves a registered operation."""
        if operation_name not in cls._registry:
            logger.error(f"❌ Operation '{operation_name}' not found.")
            raise KeyError(f"⚠️ Operation '{operation_name}' not found.")
        return cls._registry[operation_name]
