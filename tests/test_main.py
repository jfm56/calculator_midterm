"""Tests for the main calculator interface and REPL behavior using EAFP."""
import runpy
import re
from decimal import Decimal
from unittest.mock import patch
import pytest

# ✅ Local Imports
from config import plugins
from main import CalculatorREPL
from history.history import History


@pytest.fixture(scope="session", autouse=True)
def load_plugins():
    """Ensure plugins are loaded before running tests."""
    plugins.load_plugins()


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Ensure a clean history before and after each test."""
    History.clear_history()
    yield
    History.clear_history()


def test_run_operation_valid():
    """Test valid calculator operations using EAFP."""
    try:
        result = CalculatorREPL.run_operation("add", Decimal("2"), Decimal("3"))
        assert result == Decimal("5"), "⚠️ Expected 5"
    except Exception as e:
        pytest.fail(f"❌ Unexpected error: {e}")


def test_run_operation_invalid():
    """Test invalid operation handling using EAFP."""
    with pytest.raises(KeyError, match=r"⚠️ Operation 'nonexistent' not found"):
        CalculatorREPL.run_operation("nonexistent", Decimal("2"), Decimal("3"))


def test_run_operation_divide_by_zero():
    """Test division by zero handling using EAFP."""
    with pytest.raises(ZeroDivisionError, match=r"❌ Division by zero is not allowed."):
        CalculatorREPL.run_operation("divide", Decimal("10"), Decimal("0"))


@patch("builtins.input", side_effect=["exit"])
def test_main_entrypoint(mock_input, capfd):
    """Tests if running main.py executes CalculatorREPL.repl()."""
    try:
        runpy.run_path("main.py", run_name="__main__")
    except SystemExit:
        pass  # ✅ Handle `sys.exit()` without patching

    captured = capfd.readouterr()
    assert "✨ Welcome to the Interactive Calculator!" in captured.out


@patch("builtins.input", side_effect=["menu", "exit"])
@patch("app.menu.Menu.show_menu")
def test_repl_menu_command(mock_menu, mock_input, capfd):
    """Test entering 'menu' in the REPL calls the menu using EAFP."""
    try:
        CalculatorREPL.repl()
    except SystemExit:
        pass  # ✅ Prevent breaking test

    mock_menu.assert_called_once()
    captured = capfd.readouterr()
    assert "✨ Welcome to the Interactive Calculator!" in captured.out


@patch("builtins.input", side_effect=["add 2 3", "exit"])
def test_repl_addition(mock_input, capfd):
    """Test entering an addition command in REPL using EAFP."""
    try:
        CalculatorREPL.repl()
    except SystemExit:
        pass  # ✅ Avoid breaking test

    captured = capfd.readouterr()
    assert re.search(r"✅\s*Result:\s*5(\.0)?", captured.out), f"⚠️ Unexpected output: {captured.out}"


@patch("builtins.input", side_effect=["multiply 5 5", "exit"])
def test_repl_multiplication(mock_input, capfd):
    """Test entering a multiplication command in REPL using EAFP."""
    try:
        CalculatorREPL.repl()
    except SystemExit:
        pass  # ✅ Avoid breaking test

    captured = capfd.readouterr()
    assert re.search(r"✅\s*Result:\s*25(\.0)?", captured.out), f"⚠️ Unexpected output: {captured.out}"


@patch("builtins.input", side_effect=["add x y", "exit"])
def test_repl_invalid_numbers(mock_input, capfd):
    """Test entering invalid numbers in REPL using EAFP."""
    try:
        CalculatorREPL.repl()
    except SystemExit:
        pass

    captured = capfd.readouterr()
    assert re.search(
        r"⚠️ Invalid input for 'a': x \(type: str\) - Expected a number.", captured.out, re.IGNORECASE
    ), f"⚠️ Unexpected output: {captured.out}"


@patch("builtins.input", side_effect=["add 2", "exit"])
def test_repl_too_few_arguments(mock_input, capfd):
    """Test entering an incomplete calculation command in REPL using EAFP."""
    try:
        CalculatorREPL.repl()
    except SystemExit:
        pass

    captured = capfd.readouterr()
    assert re.search(r"⚠️ Invalid format", captured.out, re.IGNORECASE), f"⚠️ Unexpected output: {captured.out}"


@patch("builtins.input", side_effect=["unknown_op 2 3", "exit"])
def test_repl_unknown_operation(mock_input, capfd):
    """Test entering an unknown operation in REPL using EAFP."""
    try:
        CalculatorREPL.repl()
    except SystemExit:
        pass

    captured = capfd.readouterr()
    assert re.search(r"❌ Unknown operation", captured.out, re.IGNORECASE), f"⚠️ Unexpected output: {captured.out}"
