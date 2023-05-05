# Import all libraries - specify later.
import math
import os
import sys
import time
from datetime import datetime

import numpy as np
import pandas as pd
import pytz
import tulipy as ti
import yfinance as yf

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
                f"Can't tell if {ticker} is tradable."  # Something is breaking :(
            )
            return False

    def stop_loss(self, entry: float, direction: str) -> float:
        """
        Calculates the stop-loss price based on the entry price and the specified direction.

        Args:
            entry (float): The entry price of the asset.
            direction (str): The direction of the trade, either "long" or "short".

        Returns:
            float: The calculated stop-loss price.

        Raises:
            ValueError: If an invalid direction is provided.
        """
        stoplossMargin = 0.05

        try:
            if direction == "long":
                stop_loss = entry - (entry * stoplossMargin)
                return stop_loss
            elif direction == "short":
                stop_loss = entry + (entry * stoplossMargin)
                return stop_loss
            else:
                raise ValueError(f"Invalid direction is '{direction}'")

        except ValueError as e:
            logging.error(
                f"There is an invalid direction other than 'long' and 'short': {e}"
            )
            sys.exit()  # Figure it out when the program stops. No need to waste money.

    def take_profit(self, entry: float, direction: str) -> float:
        """
        Calculates the take-profit price based on the entry price and the specified direction.

        Args:
            entry (float): The entry price of the asset.
            direction (str): The direction of the trade, either "long" or "short".

        Returns:
            float: The calculated take-profit price.

        Raises:
            ValueError: If an invalid direction is provided.
        """
        profitMargin = 0.1  # Percent margin

        try:
            if direction == "long":
                takeProfit = entry + (entry * profitMargin)
                return takeProfit
            elif direction == "short":
                takeProfit = entry - (entry * profitMargin)
                return takeProfit
            else:
                raise ValueError(f"Invalid direction: {direction}")

        except ValueError as e:
            logging.error(
                f"There is an invalid direction other than 'long' and 'short': {e}"
            )
            sys.exit()

    def open_positions(self, asset_id: int) -> bool:
        """
        Checks if there are any open positions for the specified asset ID.

        Args:
            asset_id (int): The asset ID to check for open positions.

        Returns:
            bool: True if there is an open position for the asset ID, False otherwise.
        """
        return any(position.symbol == asset_id for position in positions)

    def check_position(self, asset) -> bool:
        """
        Checks the position of the specified asset, retrying for a limited number of attempts.

        Args:
            asset: The asset to check the position for.

        Returns:
            bool: True if the position check is successful, False otherwise.
        """
        max_attempts = 5
        attempt = 0

        while attempt <= max_attempts:
            try:
                current_price = asset.current_price
                logging.info(f"Position checked. Current price is {current_price}")
                return True
            except:
                logging.info("Position was not checked. Trying again in 5 seconds.")
                time.sleep(5)
                attempt += 1

        logging.error(f"Position was not found: {asset}")
        return False

    def run(self):
        """
        Starts running the trading bot.
        """
        logging.info("Running the Trading Bot...")
