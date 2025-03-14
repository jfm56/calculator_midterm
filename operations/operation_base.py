from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Type
from config.plugins import load_plugins

class Operation(ABC):
    """Abstract base class for calculator operations."""
    
    registry = {}

    def __init_subclass__(cls, **kwargs):
        """Automatically registers subclasses in the operation registry."""
        super().__init_subclass__(**kwargs)
        operation_name = cls.__name__.lower()
        cls.register_operation(operation_name, cls)

    @classmethod
    @abstractmethod
    def execute(cls, a: Decimal, b: Decimal) -> Decimal:
        """Abstract method that must be implemented by subclasses."""

    @classmethod
    def validate_numbers(cls, a, b):
        """Ensures input values are Decimal-compatible."""
        try:
            return Decimal(a), Decimal(b)
        except Exception as exc:
            raise TypeError(f"Invalid type: {type(a).__name__} or {type(b).__name__}") from exc

    @classmethod
    def get_operation(cls, name: str) -> Type["Operation"]:
        """Retrieve a registered operation class by name."""
        try:
            return cls.registry[name.lower()]
        except KeyError as exc:
            raise KeyError(f"Operation '{name}' not found in registry.") from exc

    @classmethod
    def register_operation(cls, name: str, operation_class: Type["Operation"]):
        """Registers an operation, preventing duplicates."""
        name = name.lower()
        if name in cls.registry:
            raise ValueError(f"Operation '{name}' is already registered.")
        cls.registry[name] = operation_class

# ✅ Load plugins AFTER defining `Operation` to prevent circular imports
load_plugins()
