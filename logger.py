import logging
import os

path = "./logs"
try:
    os.mkdir(path)
except OSError:
    print("Creating directory %s not successful unless already exists" % path)
else:
    print("Directory created!")

    # Creating log file to store errors
logging.basicConfig(filename="trading_bot.log",
                    format="%(asctime)s - %(levelname)s: %(message)s",
                    encoding="utf-8",
                    level=logging.DEBUG)

logging.debug("Debugger")

logging.info("Useful messages")

logging.warning("Warn me")

logging.error("Any error messages")

logging.critical("what's wrong")