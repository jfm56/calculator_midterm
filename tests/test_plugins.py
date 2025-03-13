"""Pytest configuration and test utilities."""

import runpy
from config import plugins
import pytest
from unittest.mock import patch, MagicMock




@patch("config.plugins.importlib.import_module", side_effect=ImportError("Mocked failure"))
@patch("config.plugins.pkgutil.iter_modules", return_value=[(None, "operations.fake_module", None)])
def test_load_plugins_import_error(mock_iter_modules, mock_import, caplog):
    """Ensure `load_plugins()` logs an error when a plugin fails to import."""
    plugins.load_plugins()

    # ✅ Ensure import was attempted on the correct module
    mock_import.assert_called_with("operations")

    # ✅ Ensure an error log was recorded
    assert "⚠️ Plugin directory 'operations' not found." in caplog.text




def test_load_plugins_success(caplog):
    """Ensure successful plugin loads are logged."""
    fake_module = MagicMock()
    fake_module.__path__ = ["fake_path"]  # ✅ Required for `pkgutil.iter_modules()`
    fake_module.__name__ = "operations"  # ✅ Required for `package.__name__`

    with patch("config.plugins.pkgutil.iter_modules", return_value=[(None, "operations.fake_op", None)]):
        with patch("config.plugins.importlib.import_module", return_value=fake_module) as mock_import:
            plugins.load_plugins()

    # ✅ Ensure import was attempted on the correct module
    mock_import.assert_called_with("operations.fake_op")

    # ✅ Ensure log message is correct
    assert "Successfully loaded plugin: operations.fake_op" in caplog.text


def test_main_called_on_script_execution():
    """Ensure `load_plugins()` is called when script runs as __main__."""
    fake_module = MagicMock()
    fake_module.__path__ = ["fake_path"]
    fake_module.__name__ = "operations"

    with patch("importlib.import_module", return_value=fake_module) as mock_import_module:
        runpy.run_path(plugins.__file__, run_name="__main__")

    # ✅ Ensure `import_module` was called at least once
    assert mock_import_module.called, "⚠️ load_plugins() was never called!"


@patch("config.plugins.importlib.import_module")
def test_load_valid_plugin(mock_import, caplog):
    """Test that a valid plugin loads successfully."""
    plugins.load_plugin("operations.add")

    # ✅ Ensure import was attempted
    mock_import.assert_called_once_with("operations.add")

    # ✅ Ensure log contains success message
    assert "Successfully loaded plugin: operations.add" in caplog.text


@patch("config.plugins.importlib.import_module", side_effect=ImportError("Plugin not found"))
def test_load_invalid_plugin(mock_import, caplog):
    """Test that an invalid plugin raises ImportError and logs an error."""
    with pytest.raises(ImportError, match="Plugin not found"):
        plugins.load_plugin("operations.unknown_plugin")

    # ✅ Ensure log contains error message
    assert "Failed to load plugin: operations.unknown_plugin" in caplog.text


@patch("config.plugins.importlib.import_module", side_effect=ImportError("Plugin not found"))
def test_plugin_debug_logging(mock_import, caplog):
    """Ensure debug logs track plugin load attempts."""
    with pytest.raises(ImportError):
        plugins.load_plugin("operations.invalid_plugin")

    # ✅ Ensure the debug log is captured
    assert "Attempting to load plugin: operations.invalid_plugin" in caplog.text
