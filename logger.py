import logging

# Creating log file to store errors
logging.basicConfig(filename="trading_bot.log",
                    format="%(asctime)s - %(levelname)s: %(message)s",
                    encoding="utf-8",
                    level=logging.DEBUG)

logging.debug("Testing")

logging.debug("Again, testing 2")

logging.info("Testing 3")