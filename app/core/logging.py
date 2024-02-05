import logging
import logging.config
import os

from app.core.config import Settings

settings = Settings()

# Create the logs directory if it doesn't exist
log_directory = os.path.dirname(settings.LOG_FILE_PATH)
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configuration dictionary for logging
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s",  # noqa: E501
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "level": settings.LOG_LEVEL,
        },
    },
    "loggers": {
        "": {
            "level": settings.LOG_LEVEL,
            "handlers": ["console"],
            "propagate": True,
        },
        "celery": {
            "level": settings.LOG_LEVEL,
            "handlers": ["console"],
            "propagate": True,
        },
    },
}

# Load the logging configuration
logging.config.dictConfig(LOGGING_CONFIG)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    Args:
        name (str): The name of the logger.
    Returns:
        logging.Logger: The logger instance.
    """
    return logging.getLogger(name)
