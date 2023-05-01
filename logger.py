import logging
import os
from datetime import datetime

# Create a logs directory if it doesn't already exist
log_path = "./logs"
os.makedirs(log_path, exist_ok=True)
print(f"Directory '{log_path}' created or already exists.")

# Configure logging
log_name = datetime.now().strftime(
    "%Y-%m-%d_%H-%M-%S.log")  # Changed format
log_file = os.path.join(log_path, log_name)

logging.basicConfig(filename=log_file,
                    format="%(asctime)s - %(levelname)s: %(message)s",
                    encoding="utf-8",
                    level=logging.DEBUG)

logging.getLogger().addHandler(logging.StreamHandler())

# Sample log messages
logging.debug("Debugging message")
logging.info("Informational message")
logging.warning("Warning message")
logging.error("Error message")
logging.critical("Critical message")
