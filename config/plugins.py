"""Plugin Loader Module - Dynamically loads operation plugins"""

import importlib
import logging
import pkgutil
from config.log_config import logger
from mappings.operations_map import operation_mapping

# ✅ Store loaded plugins to prevent duplicate imports
_loaded_plugins = set()


def load_plugins():
    """Dynamically loads all operation plugins from the 'operations' package."""
    import operations  # ✅ Prevents circular imports

    logger.info("🔄 Loading operation plugins...")

    package = operations
    for _, module_name, _ in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
        if module_name in _loaded_plugins:
            logger.debug("🔄 Skipping already loaded plugin: %s", module_name)
            continue

        try:
            importlib.import_module(module_name)
            _loaded_plugins.add(module_name)
            logger.info("✅ Successfully loaded plugin: %s", module_name)
        except ImportError as e:
            logger.error("❌ Failed to import plugin: %s - %s", module_name, e)

    logger.info("✅ Plugin system initialized!")


def load_plugin(plugin_name):
    """Loads a plugin by name and raises ImportError if it fails."""
    if plugin_name in _loaded_plugins:
        logger.debug("🔄 Skipping already loaded plugin: %s", plugin_name)
        return

    try:
        logger.debug("🚀 Attempting to load plugin: %s", plugin_name)
        module = importlib.import_module(plugin_name)
        _loaded_plugins.add(plugin_name)
        logger.info("✅ Successfully loaded plugin: %s", plugin_name)
        return module

    except ImportError as e:
        logger.error("❌ Failed to load plugin: %s - %s", plugin_name, e)
        raise


def register_operations():
    """Registers all dynamically loaded operations."""
    for operation_name, operation_class in operation_mapping.items():
        try:
            operation_class()  # ✅ Ensures the class is initialized
            logger.info(f"✅ Registered operation: {operation_name}")
        except Exception as e:
            logger.error(f"❌ Failed to register operation '{operation_name}': {e}")


def main():
    """Loads plugins once to avoid duplicate logs."""
    if not _loaded_plugins:  # ✅ Ensures it only runs once
        load_plugins()
        register_operations()


if __name__ == "__main__":
    main()
