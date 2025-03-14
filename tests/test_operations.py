"""Tests for arithmetic operations and validation."""

# ✅ Standard Library Imports
from decimal import Decimal

# ✅ Third-Party Imports
import pytest

# ✅ Local Project Imports (grouped from the same package together)
from operations.operation_base import Operation
from operations.addition import Add
from operations.subtraction import Subtract
from operations.multiplication import Multiply
from operations.division import Divide
from mappings.operations_map import operation_mapping


def test_operation_mapping():
    """Ensure `operation_mapping` contains expected operation names and correct classes."""
    expected_mapping = {
        "add": Add,
        "subtract": Subtract,
        "multiply": Multiply,
        "divide": Divide,
    }

    # ✅ Compare dictionary keys as sets (avoids order-related failures)
    assert set(operation_mapping.keys()) == set(expected_mapping.keys()), "⚠️ Keys mismatch in `operation_mapping`"

    # ✅ Ensure correct operation classes are assigned
    assert all(value is expected_mapping[key] for key, value in operation_mapping.items()), "⚠️ Class mismatch in `operation_mapping`"


@pytest.fixture(params=[
    ("add", Decimal("5"), Decimal("3"), Decimal("8")),
    ("subtract", Decimal("10"), Decimal("4"), Decimal("6")),
    ("multiply", Decimal("2"), Decimal("3"), Decimal("6")),
    ("divide", Decimal("9"), Decimal("3"), Decimal("3")),
    ("divide", Decimal("5"), Decimal("2"), Decimal("2.5")),
    ("multiply", Decimal("-4"), Decimal("3"), Decimal("-12")),
    ("multiply", Decimal("1000000"), Decimal("1000000"), Decimal("1000000000000")),
    ("multiply", Decimal("0.5"), Decimal("0.5"), Decimal("0.25")),
])
def operation_test_case(request):
    """Fixture to supply arithmetic test cases."""
    return request.param


def test_operations_execution(operation_test_case):
    """Tests arithmetic operations execute correctly."""
    operation_name, a, b, expected = operation_test_case
    assert operation_name in operation_mapping, f"⚠️ {operation_name} is missing from `operation_mapping`"

    operation = operation_mapping[operation_name]()
    assert operation.execute(a, b) == expected


def test_division_by_zero():
    """Ensure division by zero raises an appropriate error."""
    with pytest.raises((ZeroDivisionError, ArithmeticError)):
        operation_mapping["divide"]().execute(Decimal("10"), Decimal("0"))


@pytest.mark.parametrize("valid_op, a, b, expected", [
    ("add", Decimal("3.5"), Decimal("2"), Decimal("5.5")),
    ("multiply", 10, 5, Decimal("50")),
])
def test_valid_numbers_conversion(valid_op, a, b, expected):
    """Tests that `execute()` handles both integers and `Decimal` inputs correctly."""
    assert valid_op in operation_mapping, f"⚠️ {valid_op} is missing!"
    assert operation_mapping[valid_op]().execute(Decimal(a), Decimal(b)) == expected


@pytest.mark.parametrize("a, b", [
    ("invalid", "3"),
    (None, 3),
    ([1, 2], 3),
    ({1: 2}, 3),
    (object(), 3),
])
def test_validate_numbers_invalid(a, b):
    """Ensure `validate_numbers` rejects invalid types."""
    for operation in operation_mapping.values():
        with pytest.raises(TypeError):
            operation().validate_numbers(a, b)


def test_get_operation_not_found():
    """Ensure `get_operation()` raises KeyError when an operation is not found."""
    with pytest.raises(KeyError, match=r"Operation 'nonexistent' not found in registry."):
        Operation.get_operation("nonexistent")


def test_validate_numbers_invalid_type():
    """Ensure `validate_numbers()` raises TypeError for invalid inputs."""
    operation_instance = Add()  # ✅ Create an instance before calling `validate_numbers`

    with pytest.raises(TypeError, match="Invalid type"):
        operation_instance.validate_numbers("abc", "xyz")  # ✅ Call on an instance instead of the class
