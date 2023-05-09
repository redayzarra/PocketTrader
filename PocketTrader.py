# Import necessary libraries
import math
import os
import sys
from enum import Enum
import time
from datetime import datetime, timedelta

# Import fun libraries
import numpy as np
import pandas as pd
import pytz
import tulipy as ti
import yfinance as yf  # Not needed
import alpaca

from logger import *
import config


class Trader:
    def __init__(self, ticker, api):
        """
        Initialize the Trader class with the given ticker and API key.

        Args:
            ticker (str): The ticker symbol for the stock.
            api: The API key to be used for trading.
        """
        logging.info(f"Trader initialized with ticker {ticker}")
        self.ticker = ticker
        self.api = api

    def is_tradable(self, ticker):
        """
        Check if the given ticker is tradable.

        Args:
            ticker (str): The ticker symbol to check if it's tradable.

        Returns:
            bool: True if the ticker is tradable, False otherwise.
        """
        try:
            if not ticker.tradable:
                logging.info(f"{ticker} is NOT tradable!")
                return False
            else:
                logging.info(f"{ticker} is tradable!")
                return True
        except:
            logging.error(f"{ticker} is encountering some issues")
            return False

    def set_stoploss(self, entry_price, trend):
        """
        Calculate the stop loss based on the entry price and trend.

        Args:
            entry_price (float): The entry price of the stock.
            trend (str): The trade direction ("long" or "short").

        Returns:
            float: The stop loss price.

        Raises:
            ValueError: If an invalid trend is provided.
        """
        try:
            if trend == "long":
                stop_loss = entry_price - (entry_price * config.stopLossMargin)
                logging.info(f"Stop loss set for long at {stop_loss:.2f}")
                return stop_loss
            elif trend == "short":
                stop_loss = entry_price + (entry_price * config.stopLossMargin)
                logging.info(f"Stop loss set for short at {stop_loss:.2f}")
                return stop_loss
            else:
                raise ValueError
        except Exception as e:
            logging.error(f"The trend value doesn't make sense: {trend}")
            sys.exit()
