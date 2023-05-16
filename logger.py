import logging
import os
from datetime import datetime


def initialize_logging(log_level=logging.DEBUG, log_folder="logs"):
    # Create a logs directory if it doesn't already exist
    log_path = os.path.join(".", log_folder)
    os.makedirs(log_path, exist_ok=True)
    print(f"Directory '{log_path}' created or already exists.")

    # Configure logging
    log_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
    log_file = os.path.join(log_path, log_name)

    logging.basicConfig(
        filename=log_file,
        format="%(asctime)s - %(levelname)s: %(message)s",
        encoding="utf-8",
        level=log_level,
    )

    logging.getLogger().addHandler(logging.StreamHandler())
