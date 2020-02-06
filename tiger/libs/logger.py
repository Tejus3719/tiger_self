import logging
import sys
import time
import os
from logging.handlers import TimedRotatingFileHandler

path = os.path.dirname(os.path.abspath(__file__)) + "/log/test" + str(int(time.time()))
FORMATTER = logging.Formatter("%(asctime)s %(levelname)s %(filename)s'' %(funcName)s %(lineno)s :: %(message)s")
LOG_FILE = "{}/RUN_".format(path) + str(int(time.time())) + ".log"


def mkdir_p(path):
    """
    Method: to create log dir
    :param path: path of log dir
    :return: None
    """

    if not os.path.exists(path):
        os.makedirs(path)


def get_console_handler():
    """
    Methdd to get console handler
    :return: console handler
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    """
    Method: to get file handler
    :return: file handler
    """
    mkdir_p(path)
    file_handler = TimedRotatingFileHandler(LOG_FILE, when="H", interval=48)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    """
    Method :  to get logger
    :param logger_name: Logger name
    :return: logger
    Usage:
    logger= logger.get_logger(__name__)
    """

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger


def get_logname():
    """
    :return: log name
    Method: to get the log name  file name
    usage:
    logger.get_logname()
    """
    return LOG_FILE


def get_logpath():
    """
    :return: log path
    Method: to get the logpath
    usage:
    logger.get_logpath()
    """
    return path


if __name__ == "__main__":

    pass