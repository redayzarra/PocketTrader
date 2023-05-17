# PocketTrader - Trading Bot

PocketTrader is a trading bot designed to automate trades on [**Alpaca**](https://alpaca.markets/docs/python-sdk/getting_started.html#), a commission-free API-first stock brokerage. It interfaces with Alpaca's API to place trades, cancel orders, and check asset status. It also supports paper trading for testing strategies without risking real money.

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Running PocketTrader](#running-pockettrader)
4. [Features](#features)
    - [Automated Trading](#automated-trading)
    - [User Interface](#user-interface)
    - [Asset Checking](#asset-checking)
    - [Order Management](#order-management)
    - [Paper Trading](#paper-trading)
    - [Trade Execution](#trade-execution)
5. [Technical Analysis and Position Management](#technical-analysis-and-position-management)
6. [Disclaimer](#disclaimer)
7. [Contributing](#contributing)
8. [License](#license)

## Installation

1. Clone the repository to your local machine.
2. Install the necessary Python packages:

```bash
pip install -r requirements.txt
```

## Configuration 

PocketTrader requires API keys, normal API and Secret API strings, to interact with Alpaca's API. The keys can be entered through the bot's graphical user interface (or through the config.json file). Other settings, such as sleep times, can only be set in the **[config.json](https://github.com/redayzarra/PocketTrader/blob/master/config.json)** file.

## Running PocketTrader

To start the bot, use the following command:

```bash
python main.py
```
The bot will launch a GUI to set API keys. After this, it will check the account status, cancel all open orders, and then ask for a ticker. It will then start trading the provided asset. If a trade fails, the bot will log the failure and sleep for a set period of time before trying again.

Please **ensure that you have valid Alpaca API keys** and a **stable internet connection** before running the bot. Always remember to carefully review the bot's configurations before live trading. While the bot provides a level of automation, it's crucial to monitor its performance and intervene manually if necessary.

## Features

### Automated Trading

PocketTrader is designed to place trades automatically based on predefined strategies. This ensures consistent execution of the trading strategy, minimizing the potential for human error.

### User Interface
PocketTrader features an intuitive graphical user interface (GUI) that allows users to easily set their API keys and configure other settings. This makes the bot user-friendly, even for those without extensive technical knowledge.

### Asset Checking
Before placing a trade, PocketTrader checks whether the asset is tradable or not. This feature ensures that the bot doesn't attempt to place trades on assets that are not currently available for trading.

### Order Management
At the start of every trading session, the bot cancels all open orders. This ensures a clean slate for the new trading session and prevents any conflicts or unexpected trades from previous sessions.

### Paper Trading
PocketTrader supports paper trading, which enables users to test their trading strategies without risking real money. This feature is particularly useful for beginners and for testing new strategies before using them in a live market.

### Trade Execution
The run function is the main trading operation function. It orchestrates the entire trading process by performing trend analysis, confirming the trend, executing the trade, managing the open position, and closing the position when necessary. PocketTrader's functionality is encapsulated in a loop that continues to evaluate and trade as long as the program runs. It includes several checks and safeguards to manage risk and ensure proper trade execution.

## Technical Analysis and Position Management

PocketTrader employs a suite of functions to perform advanced technical analysis and manage open positions.

PocketTrader performs a general trend analysis on an asset's historical data, detecting overall upward or downward trends based on the relative position of three Exponential Moving Averages (EMAs): 9-period, 26-period, and 50-period. It returns **"long"** for an upward trend, **"short"** for a downward trend, or **"no trend"** if no clear trend is detected. To confirm the general trend, the bot performs a similar EMA-based analysis but on a shorter time interval. This ensures that the asset's price movement aligns with the general trend.

The bot also incorporates popular momentum-based indicators for further trend confirmation. PocketTrader performs Relative Strength Index (RSI) analysis, which can signal potential overbought or oversold conditions, while also using Stochastic Oscillator analysis to help identify potential price reversals. PocketTrade also checks whether the Stochastic Oscillator curves have crossed, a situation often considered a trading signal.

Finally, PocketTrader manages an open position by setting take-profit and stop-loss levels and continuously checking these levels against the asset's current price. It also keeps an eye on Stochastic Oscillator crossings as a potential exit signal.

## Disclaimer

Trading involves significant risk and can result in substantial financial loss. Always conduct your own research and consider your financial situation carefully before trading. The use of this bot is at your own risk and it is recommended to test any trading algorithm thoroughly before live trading.

## Contibuting

If you find a bug or want to propose a new feature, please open an issue. I really appreciate people willing to help!

## License

This project is licensed under the MIT license. Please see the [LICENSE](https://github.com/redayzarra/PocketTrader/blob/master/LICENSE) file for details.
