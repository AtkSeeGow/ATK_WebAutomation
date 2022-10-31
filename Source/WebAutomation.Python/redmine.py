import logging
from redmine.bot import Bot

if __name__ == "__main__":
    logging.debug("--------------------------------------開始--------------------------------------")
    bot = Bot();
    bot.execution();
    logging.debug("--------------------------------------結束--------------------------------------");