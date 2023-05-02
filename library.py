# Import all libraries - specify later.
from logger import *


class TraderBot:
    """
    A class representing a simple trading bot.
    """

    def __init__(self, ticker):
        """
        Initializes the trading bot and logs a startup message.
        """
        logging.info("The Trading Bot has awakened with ticker: %s" % ticker)

    def run(self):
        """
        Starts running the trading bot.
        """
        logging.info("Running the Trading Bot...")
