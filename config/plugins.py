import importlib
import pkgutil
import logging
from mappings.operations_map import operation_mapping

logger = logging.getLogger(__name__)

def load_plugins():
    """Dynamically loads available operations."""
    try:
        for op_name, op_class in operation_mapping.items():
            if op_name not in operation_mapping:
                logger.debug(f"🔄 Attempting to load plugin: {op_name}")
                operation_mapping[op_name] = op_class
                logger.info(f"✅ Successfully loaded plugin: {op_name}")
    except ImportError as e:
        logger.error(f"❌ Failed to load plugins: {e}")

load_plugins()
