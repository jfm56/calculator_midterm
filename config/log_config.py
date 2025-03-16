"""Logging configuration for the calculator application."""

import logging
import sys

# ✅ Define a single logger for the entire application
logger = logging.getLogger("calculator_logger")
logger.setLevel(logging.DEBUG)  # Log DEBUG and above messages

# ✅ Define log format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# 🔹 Console Handler (prints logs to terminal)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.ERROR)  # ✅ Only show errors in the console

# 🔹 File Handler (saves logs to `app.log`, overwriting old logs on each run)
file_handler = logging.FileHandler("app.log", mode="w")  # ✅ Overwrite logs for each run
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)  # ✅ Log everything to file

# ✅ Ensure all previous handlers are cleared before adding new ones
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# ✅ Attach handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# ✅ Log system initialization at both INFO and ERROR levels
logger.info("✅ Logging system initialized successfully!")
logger.error("🔴 Logging system initialized (console-visible)")
