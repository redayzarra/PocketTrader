# Import necessary libraries
import math
import os
import sys
import time
from datetime import datetime

# Import fun libraries
import numpy as np
import pandas as pd
import pytz
import tulipy as ti
import yfinance as yf  # Not needed
import alpaca

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

    def check_tradable(self, ticker: str) -> bool:
        """
        Checks if the given ticker is tradable and logs the result.

        Args:
            ticker (str): The ticker symbol to check if it's tradable.

        Returns:
            bool: True if the ticker is tradable, False otherwise.
        """
        try:
            stock_info = self.get_stock_info()
            is_tradable = stock_info["regularMarketPrice"] is not None

            if is_tradable:
                logging.info(f"{ticker} can be traded!")
            else:
                logging.info(f"{ticker} can't be traded.")

            return is_tradable
        except Exception as e:
            logging.error(f"Error checking if {ticker} is tradable: {e}")
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

    def general_trend(self, asset):
        """
        Determines the general trend of the given asset based on EMA values.

        Args:
            asset: The asset for which to find the trend.

        Returns:
            str: The general trend of the asset, either "long", "short", or "no trend".
        """
        max_attempts = 10
        attempt = 0

        while attempt < max_attempts:
            try:
                ema9 = ti.ema(data, 9)
                ema26 = ti.ema(data, 26)
                ema50 = ti.ema(data, 50)

                logging.info(f"{asset} general trend EMAS: {ema9}, {ema26}, {ema50}")

                # Determine the trend based on EMA values
                if ema9 > ema26 and ema9 > ema50:
                    logging.info(f"Trend for {asset}: Long")
                    return "long"
                elif ema9 < ema26 and ema9 < ema50:
                    logging.info(f"Trend for {asset}: Short")
                    return "short"
                else:
                    logging.info(f"Can't find trend for {asset} just yet.")
                    time.sleep(60)
                    attempt += 1
            except Exception as e:
                logging.error("Error occurred while getting trend.")
                logging.error(e)
                sys.exit()

        logging.info(f"Trend for {asset} can't be found, not waiting any longer")
        return "no trend"

    def instant_trend(self, asset, trend):
        """
        Check if the specified trend (long or short) is currently valid for the asset.

        Args:
            asset: The asset to check the trend for.
            trend (str): The trend direction to check, either "long" or "short".

        Returns:
            bool: True if the specified trend is valid, False otherwise.
        """
        max_attempts = 10

        for attempt in range(1, max_attempts + 1):
            try:
                ema9 = ti.ema(data, 9)
                ema26 = ti.ema(data, 26)
                ema50 = ti.ema(data, 50)

                logging.info(f"{asset} instant trend EMAs: {ema9}, {ema26}, {ema50}")

                if (trend == "long") and (ema9 > ema26) and (ema26 > ema50):
                    logging.info(f"We found a long trend for {asset}")
                    return True
                elif (trend == "short") and (ema9 < ema26) and (ema26 < ema50):
                    logging.info(f"We found a short trend for {asset}")
                    return True
                else:
                    logging.info(
                        f"Can't find trend for {asset} just yet. Attempt {attempt} of {max_attempts}"
                    )
                    time.sleep(60)
            except Exception as e:
                logging.warning(
                    f"Failed to find the {trend} trend for {asset} on attempt {attempt} due to error: {e}"
                )

        logging.warning(
            f"Failed to find the {trend} trend for {asset} after {max_attempts} attempts"
        )
        return False

    def run(self):
        """
        Starts running the trading bot.
        """
        logging.info("Running the Trading Bot...")
