import logging
from logging.handlers import TimedRotatingFileHandler

from config import store_settings as ss

def log_init(logger_name):	
    logger_file_name = ss['log_path'] + f"/{logger_name}.log.txt"
    logger = logging.getLogger(logger_name)

    fileHandler = TimedRotatingFileHandler(logger_file_name, when='midnight', interval=1, backupCount=7, encoding = "UTF-8")

    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    # fileHandler = logging.FileHandler(logger_file_name, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

def log_info(info, logger_name="main"):
    main = logging.getLogger(logger_name)
    main.info(info)

def log_error(info, logger_name="main"):
    main = logging.getLogger(logger_name)
    main.exception(info)

def log_debug(info, logger_name="main"):
    main = logging.getLogger(logger_name)
    main.debug(info)