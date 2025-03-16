"""
Unit tests for the Operation base class.

This module tests the core functionalities of the abstract base class `Operation`, including:
- Validation of numeric inputs (`validate_numbers`)
- Handling of invalid inputs
- Registration and retrieval of operations (`register`, `get_operation`)
- Prevention of duplicate registrations
- Ensuring only subclasses of `Operation` can be registered

Test cases cover various scenarios to ensure the robustness of the class methods.
"""
import pytest
from decimal import Decimal
from operations.operation_base import Operation


class MockOperation(Operation):
    """Mock operation for testing purposes."""
    def execute(self, a, b):
        return a + b

def test_validate_numbers_valid():
    """Ensure validate_numbers correctly converts inputs to Decimal."""
    assert Operation.validate_numbers(10, 5) == (Decimal("10"), Decimal("5"))
    assert Operation.validate_numbers("3.5", "1.2") == (Decimal("3.5"), Decimal("1.2"))
    assert Operation.validate_numbers(0, "-42.8") == (Decimal("0"), Decimal("-42.8"))


def test_validate_numbers_invalid():
    """Ensure validate_numbers raises TypeError for invalid inputs."""
    with pytest.raises(TypeError, match="Expected a number"):
        Operation.validate_numbers("abc", 5)

    with pytest.raises(TypeError, match="Expected a number"):
        Operation.validate_numbers(10, None)

    with pytest.raises(TypeError, match="Expected a number"):
        Operation.validate_numbers([], {})

    with pytest.raises(TypeError, match="Expected a number"):
        Operation.validate_numbers(3, object())

def test_validate_numbers_boolean():
    """Ensure validate_numbers does not accept boolean values."""
    with pytest.raises(TypeError, match="Boolean values are not allowed"):
        Operation.validate_numbers(True, 5)

    with pytest.raises(TypeError, match="Boolean values are not allowed"):
        Operation.validate_numbers(10, False)

@classmethod
def get_registry(cls):
    """Returns a copy of the operation registry."""
    return cls._registry.copy()

def test_register_duplicate_operation():
    """Ensure duplicate registration raises ValueError."""

    # Clear the registry before testing
    Operation._registry.clear()  # pylint: disable=protected-access

    # Register once
    Operation.register("mock", MockOperation)

    # Try registering again, should raise ValueError
    with pytest.raises(ValueError, match="Operation 'mock' already registered"):
        Operation.register("mock", MockOperation)

def test_register_invalid_class():
    """Ensure only subclasses of Operation can be registered."""
    class NotAnOperation:
        """A dummy class that does not inherit from Operation.
        This class is used for testing the `register` method of the `Operation` 
        base class to ensure that only subclasses of `Operation` can be registered.
        """

    with pytest.raises(TypeError, match="is not a subclass of Operation"):
        Operation.register("invalid", NotAnOperation)


def test_get_nonexistent_operation():
    """Ensure getting a non-existent operation raises KeyError."""
    with pytest.raises(KeyError, match="Operation 'unknown' not found"):
        Operation.get_operation("unknown")
