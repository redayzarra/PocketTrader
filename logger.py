import logging
import os

# Create a logs directory if it doesn't already exist
path = "./logs"
os.makedirs(path, exist_ok=True)
print(f"Directory '{path}' created or already exists.")

# Configure logging
log_file = os.path.join(path, "trading_bot.log")
logging.basicConfig(filename=log_file,
                    format="%(asctime)s - %(levelname)s: %(message)s",
                    encoding="utf-8",
                    level=logging.DEBUG)

# Sample log messages
logging.debug("Debugging message")
logging.info("Informational message")
logging.warning("Warning message")
logging.error("Error message")
logging.critical("Critical message")