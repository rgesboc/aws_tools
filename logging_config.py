import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(LOG_DIR = 'logs', LOG_FILE = 'app.log', ERROR_LOG_FILE = 'error.log'):

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    logger = logging.getLogger('aws_tools_prod')
    logger.setLevel(logging.DEBUG)

    # File handler for all messages
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, LOG_FILE),
        maxBytes=5*1024*1024,
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # File handler for error messages
    error_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, ERROR_LOG_FILE),
        maxBytes=5*1024*1024,
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    # Adding a console handler for debugging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # For example, only log INFO and above to console
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def setup_test_logger(LOG_DIR = 'test_logs', LOG_FILE = 'test_app.log', ERROR_LOG_FILE = 'test_error.log'):

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    logger = logging.getLogger('aws_tools_test')
    logger.setLevel(logging.DEBUG)

    # File handler for all messages
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, LOG_FILE),
        maxBytes=5*1024*1024,
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # File handler for error messages
    error_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, ERROR_LOG_FILE),
        maxBytes=5*1024*1024,
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    # Adding a console handler for debugging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # For example, only log INFO and above to console
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

def cleanup_logger(logger = None):

    # Retrieve the root logger if not specified.
    if logger is None:
        logger = logging.getLogger()

    for handler in logger.handlers[:]:
        try:
            if hasattr(handler, 'acquire') and hasattr(handler, 'release'):
                handler.acquire()
            try:
                handler.flush()  # Ensure all data is written to the file
                handler.close()  # Close the handler
            except (IOError, OSError) as e:
                logger.error(f"Error while flushing or closing handler {handler}: {e}", exc_info=True)
            finally:
                if hasattr(handler, 'release'):
                    handler.release()
                logger.removeHandler(handler)
        except Exception as e:
            logger.error(f"Unexpected error during handler cleanup: {e}", exc_info=True)