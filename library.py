# Import all libraries - specify later.
from logger import *


class TraderBot:
    """
    A class representing a simple trading bot.
    """

    def __init__(self, ticker: str):
        """
        Initializes the trading bot and logs a startup message.

        Args:
            ticker (str): The ticker symbol the trading bot will use.
        """
        logging.info(f"The Trading Bot has awakened with ticker: {ticker}")

    def is_tradable(self, ticker: str) -> bool:
        """
        Checks if the given ticker is tradable.

        Args:
            ticker (str): The ticker symbol to check if it's tradable.

        Returns:
            bool: True if the ticker is tradable, False otherwise.
        """
        # This is just a skeleton, I would need an actual API call here!
        return True

    def if_tradable(self, ticker: str, is_tradable: bool) -> bool:
        """
        Checks if the given ticker is tradable and logs the result.

        Args:
            ticker (str): The ticker symbol to check if it's tradable.
            is_tradable (bool): Simulates whether the asset is tradable or not.

        Returns:
            bool: True if the ticker is tradable, False otherwise.
        """
        try:
            if not is_tradable:
                logging.info(f"{ticker} can't be traded.")  # Probably wrong ticker
                return False
            else:
                logging.info(f"{ticker} can be traded!")  # yay!
                return True
        except:
            logging.error(
                f"Can't tell if {ticker} is tradable."
            )  # Something is breaking:(
            return False

    def run(self):
        """
        Starts running the trading bot.
        """
        logging.info("Running the Trading Bot...")
