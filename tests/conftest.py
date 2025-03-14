"""Pytest configuration and test utilities."""

import shutil
import warnings
import os
import sys
from decimal import Decimal, InvalidOperation

import pytest
from faker import Faker

from config.plugins import load_plugins
from config.env import HISTORY_FILE_PATH
from history.history import History
from operations.operation_base import Operation
from mappings.operations_map import operation_mapping

# ✅ Ensure plugins load before using `operation_mapping`
load_plugins()

# ✅ Verify operations are registered
if not Operation.registry:
    raise RuntimeError("❌ Critical Error: No operations loaded. Check plugin imports.")

fake = Faker()
BACKUP_FILE = HISTORY_FILE_PATH + ".bak"

@pytest.fixture(scope="session", autouse=True)
def backup_and_restore_csv():
    """Backs up the CSV file before testing and restores it after testing."""
    if os.path.exists(HISTORY_FILE_PATH):
        shutil.copy(HISTORY_FILE_PATH, BACKUP_FILE)  # ✅ Backup the CSV file

    yield  # Run the tests

    if os.path.exists(BACKUP_FILE):  # ✅ Restore backup after tests
        shutil.move(BACKUP_FILE, HISTORY_FILE_PATH)

@pytest.fixture(scope="function", autouse=True)
def reset_operation_registry():
    """Clear `Operation.registry` before each test."""
    Operation.registry.clear()

@pytest.fixture
def operation_test_cases():
    """Static arithmetic operation test cases."""
    return [
        ("add", Decimal("2"), Decimal("3"), Decimal("5")),
        ("subtract", Decimal("7"), Decimal("3"), Decimal("4")),
        ("multiply", Decimal("4"), Decimal("3"), Decimal("12")),
        ("divide", Decimal("10"), Decimal("2"), Decimal("5")),
    ]

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Ensure a clean slate before and after each test."""
    History.clear_history()
    yield
    History.clear_history()

def generate_test_data(num_record):
    """Dynamically generate test data for operations."""
    if not operation_mapping:
        raise ValueError("⚠️ No operations found! Ensure plugins are properly loaded.")

    for _ in range(num_record):
        try:
            op_name = fake.random_element(elements=list(operation_mapping.keys()))
            operation_func = operation_mapping[op_name]
            a = Decimal(fake.random_number(digits=2))
            b = Decimal(fake.random_number(digits=2))

            if op_name == "divide":
                b = b if b != 0 else Decimal("1")  # ✅ Avoid division by zero

            expected = operation_func.execute(a, b)

        except (ValueError, TypeError, InvalidOperation):
            continue  # ✅ Skip problematic test cases

        yield op_name, a, b, expected

def pytest_addoption(parser):
    """Add custom CLI option `--num_record`."""
    parser.addoption(
        "--num_record",
        action="store",
        default=5,
        type=int,
        help="Number of test records to generate"
    )

def pytest_generate_tests(metafunc):
    """Dynamic test parametrization based on CLI option."""
    num_records = metafunc.config.getoption("num_record")
    parameters = list(generate_test_data(num_records))

    try:
        keys, values = next(
            (keys, [(op, a, b, exp) if "expected" in keys else (op, a, b)
                    for op, a, b, exp in parameters])
            for keys in [("operation_name", "a", "b", "expected"), ("operation_name", "a", "b")]
            if set(keys).issubset(metafunc.fixturenames)
        )
        metafunc.parametrize(",".join(keys), values)

    except StopIteration:
        warnings.warn(
            f"⚠️ Skipping test case generation: Missing fixtures {metafunc.fixturenames}",
            UserWarning,
        )
