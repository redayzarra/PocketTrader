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
        try:
            position = self.api.get_open_position(asset_id)
            return True
        except Exception as e:
            logging.info(f"No open position found for {asset_id}: {e}")
            return False

    def submit_order(
        self, order_type, trend, ticker, shares_qty, current_price, exit=False
    ):
        """
        Submit an order for a given asset.

        Args:
            order_type (str): The type of order (e.g., 'limit', 'market').
            trend (str): The trade direction ('long' or 'short').
            ticker (str): The asset's ticker symbol.
            shares_qty (int): The number of shares for the order.
            current_price (float): The current price of the asset.
            exit (bool, optional): Whether the order is an exit order. Defaults to False.

        Returns:
            bool: True if the order was submitted successfully, False otherwise.
        """
        logging.info(f"Submitting {trend} order for {ticker}")

        # Determine the side and limit price based on the trend and exit status
        side = None
        limit_price = None

        if trend in ("long", "short") and not exit:
            side = "buy" if trend == "long" else "sell"
            limit_price = round(
                current_price * (1 + (1 if trend == "long" else -1) * config.maxVar), 2
            )
        elif trend in ("long", "short") and exit:
            side = "sell" if trend == "long" else "buy"

        if side is None:
            logging.error("Trend was not understood")
            sys.exit()

        try:
            order_params = {
                "symbol": ticker,
                "qty": shares_qty,
                "side": side,
                "type": order_type,
                "time_in_force": "gtc",
            }

            if order_type == "limit":
                logging.info(
                    f"Current price: {current_price:.2f} // Limit price: {limit_price:.2f}"
                )
                order_params["limit_price"] = limit_price

            order = self.api.submit_order(**order_params)
            self.order_id = order.id

            logging.info(f"{trend} order submitted correctly!")
            logging.info(f"{shares_qty} shares {side} for {ticker}")
            logging.info(f"Client order ID: {self.order_id}")
            return True

        except Exception as e:
            logging.error("Something happened when submitting order")
            logging.error(e)
            sys.exit()

    def cancel_pending_order(self, ticker):
        """
        Cancel a pending order for the given ticker, retrying if necessary.

        Args:
            ticker (str): The asset's ticker symbol.

        Returns:
            bool: True if the order was cancelled successfully, False otherwise.
        """
        logging.info(f"Cancelling order {self.order_id} for {ticker}")

        for attempt in range(1, config.maxAttemptsCPO + 1):
            try:
                self.api.cancel_order(self.order_id)
                logging.info(f"Order {self.order_id} cancelled correctly")
                return True
            except Exception as e:
                logging.warning(
                    f"Attempt {attempt}: Order could not be cancelled, retrying... ({e})"
                )
                time.sleep(config.sleepTimeCPO)

        logging.error(
            f"The order could not be cancelled after {config.maxAttemptsCPO} attempts, cancelling all orders..."
        )
        logging.info(f"Client order ID: {self.order_id}")
        self.api.cancel_all_orders()
        sys.exit()

    def check_position(self, ticker, do_not_find=False):
        """
        Check if a position exists for the given ticker.

        Args:
            ticker (str): The asset's ticker symbol.
            do_not_find (bool, optional): If True, the function returns False if the position is not found.
                                        Defaults to False.

        Returns:
            bool: True if the position is found, False otherwise.
        """
        for attempt in range(1, config.maxAttemptsCP + 1):
            try:
                position = self.api.get_position(ticker)
                current_price = float(position.current_price)
                logging.info(
                    f"The position was found. Current price is: {current_price:.2f}"
                )
                return True
            except Exception as e:
                if do_not_find:
                    logging.info("Position not found, this is good!")
                    return False

                logging.info(f"Exception: {e}")
                logging.info("Position not found, waiting for it...")
                time.sleep(config.sleepTimeME)

        logging.info(f"Position not found for {ticker}, not waiting any more")
        return False

    def get_shares_amount(self, asset_price):
        """
        Calculate the number of shares to buy/sell based on the asset price and available equity.

        Args:
            asset_price (float): The current price of the asset.

        Returns:
            int: The number of shares to buy/sell.

        Raises:
            Exception: If there is an error while calculating the number of shares.
        """
        logging.info("Calculating shares amount")

        try:
            # Get the total equity available
            account = self.api.get_account()
            equity = float(account.equity)

            # Calculate the number of shares
            shares_quantity = int(config.maxSpentEquity / asset_price)

            # Check if sufficient equity is available
            if equity - shares_quantity * asset_price > 0:
                logging.info(f"Total shares to operate with: {shares_quantity}")
                return shares_quantity
            else:
                logging.info(
                    f"Cannot spend that amount, remaining equity is {equity:.2f}"
                )
                sys.exit()

        except Exception as e:
            logging.error("An error occurred while calculating the shares amount")
            logging.error(e)
            sys.exit()

    def get_current_price(self, ticker):
        """
        Get the current price of a ticker with an open position.

        Args:
            ticker (str): The ticker symbol of the asset.

        Returns:
            float: The current price of the asset.

        Raises:
            Exception: If the position is not found after the maximum number of attempts.
        """
        for attempt in range(1, config.maxAttemptsGCP + 1):
            try:
                position = self.api.get_position(ticker)
                current_price = float(position.current_price)
                logging.info(
                    f"The position was checked. Current price is: {current_price:.2f}"
                )
                return current_price
            except Exception as e:
                logging.info(
                    "Position not found, cannot check price, waiting for it..."
                )
                time.sleep(config.sleepTimeGCP)  # wait a defined time and retry

        logging.error(f"Position not found for {ticker}, not waiting any more")
        raise Exception("Position not found after maximum attempts")

    def get_avg_entry_price(self, ticker):
        """
        Get the average entry price of a ticker with an open position.

        Args:
            ticker (str): The ticker symbol of the asset.

        Returns:
            float: The average entry price of the asset.

        Raises:
            Exception: If the position is not found after the maximum number of attempts.
        """
        for attempt in range(1, config.maxAttemptsGAEP + 1):
            try:
                position = self.api.get_position(ticker)
                avg_entry_price = float(position.avg_entry_price)
                logging.info(
                    f"The position was checked. Average entry price is: {avg_entry_price:.2f}"
                )
                return avg_entry_price
            except Exception as e:
                logging.info(
                    "Position not found, cannot check price, waiting for it..."
                )
                time.sleep(config.sleepTimeGAEP)  # wait a defined time and retry

        logging.error(f"Position not found for {ticker}, not waiting any more")
        raise Exception("Position not found after maximum attempts")
