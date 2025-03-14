import logging
import sys

# ✅ Create logger instance
logger = logging.getLogger("calculator_logger")
logger.setLevel(logging.DEBUG)

# ✅ Define log format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# 🔹 Console Handler (Only WARNING and ERROR messages show in the terminal)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.WARNING)  # ✅ Show warnings/errors only

# 🔹 File Handler (Logs everything)
file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

# ✅ Attach handlers to the logger (avoid duplicates)
if not logger.hasHandlers():
    logger.addHandler(console_handler)  # ✅ Console: Only warnings/errors
    logger.addHandler(file_handler)  # ✅ File: Logs everything
