import logging
import sys
from logging import config as logging_config

from pythonjsonlogger import jsonlogger


def configure_logging() -> None:
    """
    Configures logging for the application to output structured JSON logs.
    """
    logging_config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": jsonlogger.JsonFormatter,
                    "format": "%(asctime)s %(name)s %(levelname)s %(message)s %(context)s",
                },
            },
            "handlers": {
                "stdout": {
                    "class": "logging.StreamHandler",
                    "stream": sys.stdout,
                    "formatter": "json",
                },
            },
            "loggers": {
                "app": {
                    "handlers": ["stdout"],
                    "level": "INFO",
                    "propagate": False,
                },
                "": {
                    "handlers": ["stdout"],
                    "level": "WARNING",
                },
            },
        }
    )
