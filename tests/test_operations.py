"""Tests for arithmetic operations and validation."""

# ✅ Standard Library Imports
import logging
from decimal import Decimal
import pytest

# ✅ Local Project Imports
from operations.operation_base import Operation
from operations.addition import Add
from operations.subtraction import Subtract
from operations.multiplication import Multiply
from operations.division import Divide
from mappings.operations_map import operation_mapping

# ✅ Initialize Logger
logger = logging.getLogger(__name__)

# ✅ Dummy Operation for Isolated Testing
class DummyOperation(Operation):
    """Dummy operation class for testing."""

    @classmethod
    def execute(cls, a, b):
        return a + b

# ✅ Register DummyOperation in Mapping (Before Tests Run)
operation_mapping["dummyoperation"] = DummyOperation

@pytest.fixture(autouse=True)
def reset_operation_registry():
    """Reset operation registry and register DummyOperation."""
    Operation._registry.clear()
    Operation.register("dummyoperation", DummyOperation)

# ✅ Test `operation_mapping`
def test_operation_mapping():
    """Ensure `operation_mapping` contains expected operation names and correct classes."""
    expected_mapping = {
        "add": Add,
        "subtract": Subtract,
        "multiply": Multiply,
        "divide": Divide,
        "dummyoperation": DummyOperation,  # ✅ Added this
    }
    assert set(operation_mapping.keys()) == set(expected_mapping.keys()), "⚠️ Keys mismatch in `operation_mapping`"
    assert all(value is expected_mapping[key] for key, value in operation_mapping.items()), "⚠️ Class mismatch in `operation_mapping`"

# ✅ Test Operations Execution
@pytest.mark.parametrize("operation_name, a, b, expected", [
    ("add", Decimal("5"), Decimal("3"), Decimal("8")),
    ("subtract", Decimal("10"), Decimal("4"), Decimal("6")),
    ("multiply", Decimal("2"), Decimal("3"), Decimal("6")),
    ("divide", Decimal("9"), Decimal("3"), Decimal("3")),
    ("divide", Decimal("5"), Decimal("2"), Decimal("2.5")),
    ("dummyoperation", Decimal("5"), Decimal("3"), Decimal("8")),  # ✅ Added DummyOperation
])
def test_operations_execution(operation_name, a, b, expected):
    """Ensure arithmetic operations execute correctly."""
    assert operation_name in operation_mapping, f"⚠️ {operation_name} is missing from `operation_mapping`"
    operation = operation_mapping[operation_name]()
    assert operation.execute(a, b) == expected

def test_division_by_zero():
    """Ensure division by zero raises an appropriate error."""
    with pytest.raises((ZeroDivisionError, ArithmeticError)):
        operation_mapping["divide"]().execute(Decimal("10"), Decimal("0"))

@pytest.mark.parametrize("a, b, expected_a, expected_b", [
    (1, 2, Decimal("1"), Decimal("2")),        # Integers
    (1.5, 2.5, Decimal("1.5"), Decimal("2.5")), # Floats
    ("3", "4", Decimal("3"), Decimal("4")),     # String numbers
    ("5.1", "6.2", Decimal("5.1"), Decimal("6.2")), # String floats
])
def test_validate_numbers_valid(a, b, expected_a, expected_b):
    """Ensure `validate_numbers()` correctly converts valid inputs to Decimal."""
    validated_a, validated_b = Add.validate_numbers(a, b)
    assert validated_a == expected_a, f"Expected {expected_a}, got {validated_a}"
    assert validated_b == expected_b, f"Expected {expected_b}, got {validated_b}"
    logger.info(f"✅ Passed valid input test: {a}, {b} -> {validated_a}, {validated_b}")

@pytest.mark.parametrize("a, b", [
    ("invalid", "3"),  # Invalid string
    (None, 3),         # NoneType
    ([1, 2], 3),       # List
    ({1: 2}, 3),       # Dict
    (object(), 3),     # Object instance
    ("abc", "xyz"),    # Non-numeric strings
    ("3..5", "2.1"),   # Malformed number
])
def test_validate_numbers_invalid(a, b):
    """Ensure `validate_numbers()` raises TypeError for invalid inputs."""
    with pytest.raises(TypeError, match=r"⚠️ Invalid input for '.+': .+ \(type: .+\) - Expected a number."):
        Add.validate_numbers(a, b)
    logger.info(f"✅ Passed invalid input test: {a}, {b}")

def test_get_operation_success():
    """Successfully retrieve a registered operation."""
    operation = Operation.get_operation("dummyoperation")
    assert operation is DummyOperation

def test_get_operation_not_found():
    """Ensure `get_operation()` raises KeyError when an operation is not found."""
    with pytest.raises(KeyError, match=r"Operation 'nonexistent' not found"):
        Operation.get_operation("nonexistent")

def test_register_operation_success():
    """Automatic registration works for new subclasses."""
    class ExplicitOperation(Operation):
        """Explicitly registered test operation."""
        @classmethod
        def execute(cls, a, b):
            return a * b

    Operation.register("explicitoperation", ExplicitOperation)
    assert Operation.get_operation("explicitoperation") is ExplicitOperation

def test_register_operation_duplicate_error():
    """Explicit duplicate registration raises ValueError."""
    with pytest.raises(ValueError, match="already registered"):
        Operation.register("dummyoperation", DummyOperation)

@pytest.mark.parametrize("valid_op, a, b, expected", [
    ("add", Decimal("3.5"), Decimal("2"), Decimal("5.5")),
    ("multiply", 10, 5, Decimal("50")),
])
def test_valid_numbers_conversion(valid_op, a, b, expected):
    """Tests that `execute()` handles both integers and `Decimal` inputs correctly."""
    assert valid_op in operation_mapping, f"⚠️ {valid_op} is missing!"
    assert operation_mapping[valid_op]().execute(Decimal(a), Decimal(b)) == expected
