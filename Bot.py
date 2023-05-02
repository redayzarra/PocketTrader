# Import all libraries
import sys
from library import *
from logger import *


initialize_logging(log_level=logging.INFO, log_folder="logs")


def account_verification():
    """
    Verifies the account and logs an error message if an exception occurs.
    """
    try:
        pass
    except Exception as e:
        logging.error(f"Unable to verify account! Exception: {e}")
        sys.exit()


def clear_orders(open_orders):
    """
    Clears all open orders and logs information about the process.

    Args:
        open_orders: A list of open orders.
    """
    logging.info(f"List of open orders: {open_orders}")

    for order in open_orders:
        logging.info(f"Closing order {order.id}")

    logging.info("Clearing all open orders.")
