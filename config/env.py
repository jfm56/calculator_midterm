import os
from dotenv import load_dotenv

import operations

# ✅ Load environment variables from .env file
load_dotenv()

PLUGIN_DIRECTORY = operations


# ✅ Define function to fetch environment variables
def get_env_var(var_name, default=None):
    """Retrieve an environment variable or return a default value."""
    return os.getenv(var_name, default)

# ✅ Define key environment variables
LOG_LEVEL = get_env_var("LOG_LEVEL", "INFO").upper()
PLUGIN_DIRECTORY = get_env_var("PLUGIN_DIRECTORY", "operations")
DATABASE_URL = get_env_var("DATABASE_URL", "sqlite:///calculator2.db")

# ✅ Export all relevant variables
__all__ = ["get_env_var", "LOG_LEVEL", "PLUGIN_DIRECTORY", "DATABASE_URL"]
