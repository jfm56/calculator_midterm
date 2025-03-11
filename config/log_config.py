"""Logging configuration for the calculator application."""

import logging
import sys

# ✅ Create logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Capture DEBUG, INFO, WARNING, and ERROR logs

# ✅ Format log messages
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# 🔹 Console Handler (prints logs to terminal)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)  # Show logs in console

# 🔹 File Handler (saves logs to `app.log`)
file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)  # Log everything to file

# ✅ Attach handlers to the logger (avoid duplicates)
if not logger.hasHandlers():
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
