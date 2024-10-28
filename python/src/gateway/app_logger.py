import logging
import os

from dotenv import load_dotenv

load_dotenv()


def get_logger(name: str):
    # Create a logger
    logger = logging.getLogger(name)

    # Set the log level to INFO
    logger.setLevel(os.environ.get("LOG_LEVEL"))

    # Create a handler
    handler = logging.StreamHandler()

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add the formatter to the handler
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger

# Log some messages
# logger.debug('This is a debug message')
# logger.info('This is an info message')
# logger.warning('This is a warning message')
# logger.error('This is an error message')
# logger.critical('This is a critical message')