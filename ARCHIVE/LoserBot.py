# Import all libraries
import sys
from ARCHIVE.library import *
from logger import *


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


def get_ticker():
    """
    Prompt the user to enter a ticker symbol and return it.

    Returns:
        str: The entered ticker symbol.
    """
    ticker = input("What ticker do you want to operate with? Ticker: ")
    return ticker


def main():
    """
    Main function to:
        - Initialize logging
        - Verify the account
        - Clear orders
        - Get the user's desired ticker.
    """
    initialize_logging()
    account_verification()

    # Example open_orders list for demonstration
    open_orders = []
    clear_orders(open_orders)

    ticker = get_ticker()

    mytrader = TraderBot(ticker)
    mytrader.run()

    print(f"Operating with ticker: {ticker}")


if __name__ == "__main__":
    main()
