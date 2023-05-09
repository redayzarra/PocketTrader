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


class Trader:
    def __init__(self, ticker, api):
        """
        Initialize the Trader class with the given ticker and API.

        Args:
            ticker (str): The ticker symbol for the stock.
            api: The API to be used for trading.
        """
        logging.info(f"Trader initialized with ticker {ticker}")
        self.ticker = ticker
        self.api = api
