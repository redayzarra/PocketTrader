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

    def set_takeprofit(self, entry_price, trend):
        """
        Calculate the take profit based on the entry price and trend.

        Args:
            entry_price (float): The entry price of the stock.
            trend (str): The trade direction ("long" or "short").

        Returns:
            float: The take profit price.

        Raises:
            ValueError: If an invalid trend is provided.
        """
        try:
            if trend == "long":
                take_profit = entry_price + (entry_price * config.takeProfitMargin)
                logging.info(f"Take profit set for long at {take_profit:.2f}")
                return take_profit
            elif trend == "short":
                take_profit = entry_price - (entry_price * config.takeProfitMargin)
                logging.info(f"Take profit set for short at {take_profit:.2f}")
                return take_profit
            else:
                raise ValueError
        except Exception as e:
            logging.error(f"The trend value doesn't make sense: {trend}")
            sys.exit()

    def load_historical_data(self, ticker, interval, period):
        """
        Load historical stock data.

        Args:
            ticker (str): The stock ticker symbol.
            interval (str): The time interval for data aggregation (e.g. '1m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo').
            period (str): The period for which to retrieve data (e.g. '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max').

        Returns:
            DataFrame: A pandas DataFrame containing the historical stock data.

        Raises:
            Exception: If there is an error while loading historical data.
        """
        try:
            ticker_data = yf.Ticker(ticker)
            historical_data = ticker_data.history(period=period, interval=interval)
        except Exception as e:
            logging.error("There are some issues with loading historical data")
            logging.error(e)
            sys.exit()

        return historical_data
    
    
    def get_open_positions(self, asset_id):
        """
        Get open positions for a given asset ID.

        Args:
            asset_id (str): The asset's unique identifier.

        Returns:
            bool: True if there is an open position for the asset, False otherwise.
        """
        positions = self.api.list_positions()
        return any(position.symbol == asset_id for position in positions)
    
    