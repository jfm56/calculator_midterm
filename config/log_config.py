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

# 🔹 File Handler (saves logs to `app.log`)
file_handler = logging.FileHandler("app.log", mode="a")  # ✅ Append to logs
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)  # ✅ Log everything to file

# ✅ Remove previous handlers to prevent duplicates
if logger.hasHandlers():
    logger.handlers.clear()

# ✅ Attach handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# ✅ Log system initialization
logger.info("✅ Logging system initialized successfully!")
