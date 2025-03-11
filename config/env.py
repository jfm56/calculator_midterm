import os
from dotenv import load_dotenv

# ✅ Load environment variables from .env file
load_dotenv()

# ✅ Define function to fetch environment variables safely
def get_env_var(var_name, default=None, cast_func=str):
    """
    Retrieve an environment variable, apply type conversion if needed, or return a default value.
    
    Args:
        var_name (str): The name of the environment variable.
        default (Any): The default value if the environment variable is not set.
        cast_func (callable): A function to cast the variable's value (e.g., int, bool, float).
    
    Returns:
        Any: The environment variable value, cast to the desired type.
    """
    value = os.getenv(var_name, default)
    try:
        return cast_func(value)
    except (ValueError, TypeError):
        return default

# ✅ Define key environment variables
LOG_LEVEL = get_env_var("LOG_LEVEL", "INFO").upper()
PLUGIN_DIRECTORY = get_env_var("PLUGIN_DIRECTORY", "operations")
DATABASE_URL = get_env_var("DATABASE_URL", "sqlite:///calculator.db")

# ✅ Boolean and Integer Variables
DEBUG_MODE = get_env_var("DEBUG_MODE", "False", lambda x: x.lower() in ["true", "1"])
TEST_MODE = get_env_var("TEST_MODE", "False", lambda x: x.lower() in ["true", "1"])
COVERAGE_THRESHOLD = get_env_var("COVERAGE_THRESHOLD", 80, int)

# ✅ Export all relevant variables
__all__ = ["get_env_var", "LOG_LEVEL", "PLUGIN_DIRECTORY", "DATABASE_URL", "DEBUG_MODE", "TEST_MODE", "COVERAGE_THRESHOLD"]
