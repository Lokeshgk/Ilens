from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from scripts.utils.config import LOG_LEVEL, LOGSTASH_HOST, LOGSTASH_PORT, LOG_HANDLER_NAME, BASE_LOG_PATH
import logging
#from logstash_async.handler import AsynchronousLogstashHandler
from logging.handlers import RotatingFileHandler
from logging import WARNING,INFO,DEBUG,ERROR
import os

DEFAULT_FORMAT = '%(asctime)s %(levelname)5s %(name)s %(message)s'
DEBUG_FORMAT = '%(asctime)s %(levelname)5s %(name)s [%(threadName)5s:%(filename)5s:%(funcName)5s():%(lineno)s] %(message)s'

EXTRA = {}

FORMATTER = DEFAULT_FORMAT
if LOG_LEVEL.strip() == "DEBUG":
    FORMATTER = DEBUG_FORMAT


def get_logger(log_handler_name, extra=EXTRA):
    """
    Purpose : To create logger .
    :param log_handler_name: Name of the log handler.
    :param extra: extra args for the logger
    :return: logger object.
    """
    log_path = os.path.join(BASE_LOG_PATH, log_handler_name + ".log")
    logstash_temp = os.path.join(BASE_LOG_PATH, log_handler_name + ".db")
    logger = logging.getLogger(log_handler_name)
    logger.setLevel(LOG_LEVEL.strip().upper())
    log_handler = logging.StreamHandler()
    log_handler.setLevel(LOG_LEVEL)
    formatter = logging.Formatter(FORMATTER)
    log_handler.setFormatter(formatter)
    handler = RotatingFileHandler(log_path, maxBytes=10485760,
                                  backupCount=5)
    handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.addHandler(handler)
    if LOGSTASH_PORT is not None and LOGSTASH_HOST is not None and LOGSTASH_PORT.isdigit():
        #logger.addHandler(AsynchronousLogstashHandler(LOGSTASH_HOST, int(LOGSTASH_PORT), database_path=logstash_temp))
        pass
    logger = logging.LoggerAdapter(logger, extra)
    return logger


logger = get_logger(LOG_HANDLER_NAME)

