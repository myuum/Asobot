from cmath import log
import logging
from logging import getLogger, StreamHandler, Formatter
format = '%(asctime)s,%(levelname)s,%(message)s'
logging.basicConfig(filename="asobot.log",format=format)
logger = getLogger("BotLog")
logger.setLevel(logging.DEBUG)
stream_handler = StreamHandler()
stream_handler.setLevel(logging.DEBUG)
handler_format = Formatter(format)
stream_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)
def d(message:str):
    logger.debug(message)
def i(message:str):
    logger.info(message)
def e(message:str):
    logger.error(message)