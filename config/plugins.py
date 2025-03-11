"""Plugin Loader Module - Dynamically loads operation plugins"""
import importlib
import pkgutil
from config.log_config import logger
from config.env import PLUGIN_DIRECTORY

# ✅ Store loaded plugins to prevent duplicate imports
_loaded_plugins = set()

def load_plugins():
    """Dynamically loads all operation plugins from the specified directory."""
    try:
        package = importlib.import_module(PLUGIN_DIRECTORY)
        if not hasattr(package, "__path__"):
            logger.error("⚠️ Plugin directory '%s' does not have a valid __path__.", PLUGIN_DIRECTORY)
            return
    except ImportError:
        logger.error("⚠️ Plugin directory '%s' not found.", PLUGIN_DIRECTORY)
        return

    for _, module_name, _ in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
        if module_name in _loaded_plugins:
            logger.debug("Skipping already loaded plugin: %s", module_name)
            continue

        try:
            importlib.import_module(module_name)
            _loaded_plugins.add(module_name)
            logger.info("✅ Successfully loaded plugin: %s", module_name)
        except ImportError as e:
            logger.error("❌ Failed to import %s: %s", module_name, e)

def load_plugin(plugin_name):
    """Loads a specific plugin by name and raises ImportError if it fails."""
    if plugin_name in _loaded_plugins:
        logger.debug("Skipping already loaded plugin: %s", plugin_name)
        return importlib.import_module(plugin_name)

    try:
        logger.debug("Attempting to load plugin: %s", plugin_name)
        module = importlib.import_module(plugin_name)
        _loaded_plugins.add(plugin_name)
        logger.info("✅ Successfully loaded plugin: %s", plugin_name)
        return module

    except ImportError as e:
        logger.error("❌ Failed to load plugin: %s - %s", plugin_name, e)
        raise

def main():
    """Ensures plugins are loaded only once to prevent duplicate logs."""
    if not _loaded_plugins:
        load_plugins()

if __name__ == "__main__":
    main()
