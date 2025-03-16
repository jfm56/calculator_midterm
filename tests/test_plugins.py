"""
Unit tests for the plugin loader module.
"""

import logging
import pytest
from unittest.mock import patch, MagicMock
from config.plugins import load_plugin, load_plugins, register_operations, main, _loaded_plugins
from config.plugins import operation_mapping

@pytest.fixture
def mock_logger():
    """Mock the logger to prevent real logging during tests."""
    with patch("config.log_config.logger") as mock_log:
        yield mock_log


@patch("config.plugins.importlib.import_module")
@patch("config.plugins.pkgutil.iter_modules")
def test_load_plugins(mock_iter_modules, mock_import_module, caplog):
    """Ensure load_plugins() correctly loads modules dynamically."""

    _loaded_plugins.clear()  # ✅ Clear globally before running the test

    # Simulate discovering plugins
    mock_iter_modules.return_value = [
        (None, "operations.addition", None),
        (None, "operations.subtraction", None),
    ]

    # ✅ Mock successful module import
    mock_import_module.side_effect = lambda name: MagicMock(__name__=name)

    # ✅ Capture logs to verify log behavior
    with caplog.at_level(logging.INFO):
        load_plugins()

    # ✅ Validate modules were imported
    mock_import_module.assert_any_call("operations.addition")
    mock_import_module.assert_any_call("operations.subtraction")

    # ✅ Ensure logs were written
    assert "✅ Successfully loaded plugin: operations.addition" in caplog.text
    assert "✅ Successfully loaded plugin: operations.subtraction" in caplog.text


@patch("config.plugins.importlib.import_module")
def test_load_plugin_success(mock_import_module, caplog):
    """Ensure a single plugin loads correctly."""

    _loaded_plugins.clear()

    # ✅ Mock successful import
    mock_import_module.return_value = MagicMock(__name__="operations.addition")

    # ✅ Capture logs to verify logging behavior
    with caplog.at_level(logging.INFO):
        load_plugin("operations.addition")

    # ✅ Verify import_module was called once
    mock_import_module.assert_called_once_with("operations.addition")

    # ✅ Ensure expected log messages exist
    assert "✅ Successfully loaded plugin: operations.addition" in caplog.text


@patch("config.plugins.importlib.import_module", side_effect=ImportError("Fake import error"))
def test_load_plugin_failure(mock_import_module, caplog):
    """Ensure load_plugin() raises an error for an invalid module."""

    # Enable capturing logs
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ImportError, match="Fake import error"):
            load_plugin("operations.invalid")

    # Verify the import_module was called once
    mock_import_module.assert_called_once_with("operations.invalid")

    # Check if the error message is in the captured logs
    assert "❌ Failed to load plugin: operations.invalid - Fake import error" in caplog.text

@patch("config.plugins.logger")
@patch.dict("config.plugins.operation_mapping", {
    "add": MagicMock(),
    "subtract": MagicMock(),
    "multiply": MagicMock(),
    "divide": MagicMock(),
}, clear=True)
def test_register_operations(mock_logger):
    """Ensure register_operations() initializes all registered operations."""

    register_operations()

    # ✅ Verify each operation was initialized
    for name, operation in operation_mapping.items():  # 🔹 Use operation_mapping directly
        operation.assert_called_once()
        mock_logger.info.assert_any_call(f"✅ Registered operation: {name}")

@patch("config.plugins.register_operations")
@patch("config.plugins.load_plugins")
def test_main_loads_plugins_once(mock_register_operations, mock_load_plugins):
    """Ensure main() calls load_plugins() and register_operations() only once."""

    _loaded_plugins.clear()  # ✅ Reset before running the test

    # Call main function
    main()

    # Ensure plugins and operations were loaded once
    mock_load_plugins.assert_called_once()
    mock_register_operations.assert_called_once()
