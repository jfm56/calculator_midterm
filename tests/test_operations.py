"""
Test cases for arithmetic operations in the calculator.
"""

import logging
from decimal import Decimal
import pytest
from operations.division import Divide
from operations.subtraction import Subtract
from operations.multiplication import Multiply
from operations.addition import Add

logger = logging.getLogger(__name__)

# ✅ List of all operations to test
operations = [("add", Add), ("subtract", Subtract), ("multiply", Multiply), ("divide", Divide)]

@pytest.mark.parametrize("operation, cls, a, b, expected", [
    ("add", Add, 10, 5, Decimal(15)),
    ("add", Add, 3.5, 1.2, Decimal("4.7")),
    ("add", Add, "-8", "2", Decimal("-6")),
    ("add", Add, Decimal("100.50"), Decimal("50.25"), Decimal("150.75")),

    ("subtract", Subtract, 10, 5, Decimal(5)),
    ("subtract", Subtract, 3.5, 1.2, Decimal("2.3")),
    ("subtract", Subtract, "-8", "2", Decimal("-10")),
    ("subtract", Subtract, Decimal("100.50"), Decimal("50.25"), Decimal("50.25")),

    ("multiply", Multiply, 3, 4, Decimal(12)),
    ("multiply", Multiply, 1.5, 2, Decimal("3.0")),
    ("multiply", Multiply, "5", "2", Decimal(10)),

    ("divide", Divide, 10, 2, Decimal(5)),
    ("divide", Divide, "20", "4", Decimal(5)),
    ("divide", Divide, Decimal("15.5"), Decimal("2.5"), Decimal("6.2")),
])
def test_valid_operations(operation, cls, a, b, expected):
    """Test valid arithmetic operations."""
    assert cls.execute(a, b) == pytest.approx(expected)

@pytest.mark.parametrize("operation, cls, a, b, expected_error", [
    ("divide", Divide, 10, 0, ZeroDivisionError),  # ✅ Division by zero

    # Invalid inputs should raise TypeError
    ("add", Add, "abc", 5, TypeError),
    ("add", Add, 10, None, TypeError),
    ("add", Add, [], {}, TypeError),
    ("add", Add, 3, object(), TypeError),

    ("subtract", Subtract, "abc", 5, TypeError),
    ("subtract", Subtract, 10, None, TypeError),
    ("subtract", Subtract, [], {}, TypeError),
    ("subtract", Subtract, 3, object(), TypeError),

    ("multiply", Multiply, "abc", 5, TypeError),
    ("multiply", Multiply, 10, None, TypeError),
    ("multiply", Multiply, [], {}, TypeError),
    ("multiply", Multiply, object(), "5", TypeError),

    ("divide", Divide, "abc", 5, TypeError),
    ("divide", Divide, 10, None, TypeError),
    ("divide", Divide, [], {}, TypeError),
    ("divide", Divide, 3, object(), TypeError),
])
def test_invalid_operations(operation, cls, a, b, expected_error):
    """Test invalid operations that should raise TypeError or ZeroDivisionError."""
    with pytest.raises(expected_error):
        cls.execute(a, b)

@pytest.mark.parametrize("cls, a, b", [
    (Add, True, 5),
    (Add, 5, False),
    (Subtract, True, 5),
    (Subtract, 5, False),
    (Multiply, True, 5),
    (Multiply, 5, False),
    (Divide, True, 5),
    (Divide, 5, False),
])
def test_validate_numbers_boolean(cls, a, b):
    """Test validate_numbers() should not accept boolean values."""
    with pytest.raises(TypeError, match=r"⚠️ Invalid input: .* \((int|bool)\) or .* \((int|bool)\) - Invalid type\."):
        cls.validate_numbers(a, b)

@pytest.mark.parametrize("cls, a, b, expected_a, expected_b", [
    (Add, "3.5", "1.2", Decimal("3.5"), Decimal("1.2")),
    (Subtract, "2.5", "3.5", Decimal("2.5"), Decimal("3.5")),
    (Multiply, "4.2", "1.1", Decimal("4.2"), Decimal("1.1")),
    (Divide, "7.5", "2.5", Decimal("7.5"), Decimal("2.5")),
])
def test_validate_numbers_valid(cls, a, b, expected_a, expected_b):
    """Test validate_numbers() with valid numeric inputs."""
    assert cls.validate_numbers(a, b) == (expected_a, expected_b)
