
"""Manages logging for the application."""
import logging
import os
import json

class Logger:
    """Manages logging for the application."""

    def __init__(self, name: str, level: int = logging.INFO):
        """
        Initializes the logger.

        Args:
            name (str): The name of the logger.
            level (int, optional): The logging level. Defaults to logging.INFO.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    def add_file_handler(self, filename: str):
        """Adds a file handler to the logger.

        Args:
            filename (str): The path to the log file.
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def add_console_handler(self):
        """Adds a console handler to the logger."""
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

    def log(self, level: int, message: str, **kwargs):
        """Logs a message with the specified level and optional additional data.

        Args:
            level (int): The logging level.
            message (str): The message to log.
            **kwargs: Additional data to include in the log message (will be converted to json)
        """
        if kwargs:
            message = f"{message} - {json.dumps(kwargs, default=str)}"
        self.logger.log(level, message)

    def info(self, message: str, **kwargs):
        """Logs an info message.

        Args:
            message (str): The message to log.
            **kwargs: Additional data to include in the log message (will be converted to json)
        """
        self.log(logging.INFO, message, **kwargs)

    def debug(self, message: str, **kwargs):
        """Logs a debug message.

        Args:
            message (str): The message to log.
            **kwargs: Additional data to include in the log message (will be converted to json)
        """
        self.log(logging.DEBUG, message, **kwargs)

    def error(self, message: str, **kwargs):
        """Logs an error message.

        Args:
            message (str): The message to log.
            **kwargs: Additional data to include in the log message (will be converted to json)
        """
        self.log(logging.ERROR, message, **kwargs)

    def warning(self, message: str, **kwargs):
        """Logs a warning message.

        Args:
            message (str): The message to log.
            **kwargs: Additional data to include in the log message (will be converted to json)
        """
        self.log(logging.WARNING, message, **kwargs)

# Initialize logger
logger = Logger(__name__)
logger.add_console_handler()
# If you want to log to a file as well, uncomment the following line and specify the log file path
# logger.add_file_handler('logs/storyboard.log')
