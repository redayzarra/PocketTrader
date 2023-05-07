from config import API_KEY, SECRET_KEY
from PocketTrader import TraderBot
from Strategies import MovingAverageCrossover

if __name__ == "__main__":
    # Instantiate the trading bot
    MyTrader = TraderBot(API_KEY, SECRET_KEY)

    # Set the strategy for the trading bot
    MyTrader.set_strategy(strategy)

    # Run the trading bot
    MyTrader.run()
