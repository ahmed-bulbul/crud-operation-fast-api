import logging
import os

# Create logs folder if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")

# Create logger
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)  # Keep INFO level for console

# Console handler (optional)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
console_handler.setFormatter(console_format)

# File handler for errors only
error_file_handler = logging.FileHandler(ERROR_LOG_FILE)
error_file_handler.setLevel(logging.ERROR)  # ✅ only logs errors
file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
error_file_handler.setFormatter(file_format)

# Add handlers
logger.addHandler(console_handler)
logger.addHandler(error_file_handler)
