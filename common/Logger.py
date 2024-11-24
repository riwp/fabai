import os
import logging
from flask import Flask

class Logger:
    def __init__(self, app=None, log_path=None, log_level=logging.INFO):
        self.log_path = os.path.join(os.getcwd(), log_path)
        self.log_level = log_level

        # Configure logging for file and console output
        self.configure_logging()

        if app:
            self.init_app(app)

    def configure_logging(self):
        """
        Configures the logging setup with both file and console handlers.
        """
        # Create log directory if it doesn't exist
        log_dir = os.path.dirname(self.log_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Get the root logger
        logger = logging.getLogger()

        # File handler for logging
        file_handler = logging.FileHandler(self.log_path)
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        
        # Console handler for live output in terminal (for Flask)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        # Add handlers if they are not already added
        if not any(isinstance(handler, logging.FileHandler) for handler in logger.handlers):
            logger.addHandler(file_handler)

        if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
            logger.addHandler(console_handler)

        # Set log level
        logger.setLevel(self.log_level)

    def init_app(self, app: Flask):
        """
        Initializes the logger with a Flask app, attaching to app.logger.
        Prevents duplicate handlers from being added.
        """
        # Prevent duplicate log handlers
        if not any(isinstance(handler, logging.StreamHandler) for handler in app.logger.handlers):
            app.logger.addHandler(logging.StreamHandler())
        
        if not any(isinstance(handler, logging.FileHandler) for handler in app.logger.handlers):
            app.logger.addHandler(logging.FileHandler(self.log_path))
        
        app.logger.setLevel(self.log_level)

    def log_info(self, message: str):
        """
        Logs an info level message.
        """
        logging.info(message)

    def log_warning(self, message: str):
        """
        Logs a warning level message.
        """
        logging.warning(message)

    def log_error(self, message: str):
        """
        Logs an error level message.
        """
        logging.error(message)

    def log_exception(self, exception: Exception):
        """
        Logs an exception message.
        """
        logging.exception(exception)
