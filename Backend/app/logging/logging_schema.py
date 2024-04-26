import logging
import logging.handlers
import sys

from app.constants.config_constants import LOG_FILE, LOG_LEVEL
from app.logging.logger_constants import DEBUG, INFO
from app.logging.LogPropertiesManager import LogPropertiesManager


class SpotifyElectronFormatter(logging.Formatter):
    MODULE_COLOR = "\033[4m"  # Underline
    LEVEL_DEBUG_COLOR = "\033[94m"  # Blue
    LEVEL_INFO_COLOR = "\033[92m"  # Green
    LEVEL_WARNING_COLOR = "\033[38;5;208m"  # Orange
    LEVEL_ERROR_COLOR = "\033[91m"  # Red
    LEVEL_CRITICAL_COLOR = "\033[95m"  # Magenta
    RESET_COLOR = "\033[0m"  # Reset

    FORMATS = {
        logging.DEBUG: (
            f"%(asctime)s -  {MODULE_COLOR}%(name)s{RESET_COLOR} - {LEVEL_DEBUG_COLOR}%(levelname)s{RESET_COLOR} - %(message)s"
        ),
        logging.INFO: (
            f"%(asctime)s -  {MODULE_COLOR}%(name)s{RESET_COLOR} - {LEVEL_INFO_COLOR}%(levelname)s{RESET_COLOR} - %(message)s"
        ),
        logging.WARNING: (
            f"%(asctime)s -  {MODULE_COLOR}%(name)s{RESET_COLOR} - {LEVEL_WARNING_COLOR}%(levelname)s{RESET_COLOR} - %(message)s"
        ),
        logging.ERROR: (
            f"%(asctime)s -  {MODULE_COLOR}%(name)s{RESET_COLOR} - {LEVEL_ERROR_COLOR}%(levelname)s{RESET_COLOR} - %(message)s"
        ),
        logging.CRITICAL: (
            f"%(asctime)s -  {MODULE_COLOR}%(name)s{RESET_COLOR} - {LEVEL_CRITICAL_COLOR}%(levelname)s{RESET_COLOR} - %(message)s"
        ),
    }

    def format(self, record):
        log_format = self.FORMATS.get(
            record.levelno, "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        formatter = logging.Formatter(log_format)
        return formatter.format(record)


class SpotifyElectronLogger:
    """Custom Logger that accepts the current file logger name and\
    optionally an log file to store logs
    """

    _log_properties_manager = LogPropertiesManager()

    def __init__(self, logger_name, log_file=None):
        # borg pattern shared stated
        self.log_properties_manager = SpotifyElectronLogger._log_properties_manager

        # Disable other loggers
        logging.getLogger().handlers.clear()
        logging.getLogger().propagate = False
        self._log_level_mapping = {INFO: logging.INFO, DEBUG: logging.DEBUG}

        self.logger = logging.getLogger(logger_name)

        self.logger.setLevel(self._get_log_level())
        self._manage_file_handler()
        self._manage_console_handler()

    def _manage_file_handler(self):
        """Adds logging handler depending if log file has been provided or not"""
        if not self.log_properties_manager.is_log_file_provided():
            return
        file_log_handler = logging.handlers.RotatingFileHandler(
            self.log_properties_manager.__getattribute__(LOG_FILE),
            maxBytes=50000,
            backupCount=5,
        )
        self._add_handler(file_log_handler)

    def _manage_console_handler(self):
        """Adds logging console handler"""
        stream_handler = logging.StreamHandler(sys.stdout)
        self._add_handler(stream_handler)

    def _add_handler(
        self, handler: logging.StreamHandler | logging.handlers.RotatingFileHandler
    ):
        """Add handler to logger

        Args:
        ----
            handler (Union[StreamHandler, RotatingFileHandler]): the handler to add

        """
        handler.setLevel(self._get_log_level())
        formatter = SpotifyElectronFormatter()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _get_log_level(self) -> int:
        try:
            log_level = self.log_properties_manager.__getattribute__(LOG_LEVEL)
            if log_level is None:
                return logging.INFO
            mapped_log_level = self._log_level_mapping[log_level]
        except Exception:
            return logging.INFO
        else:
            return mapped_log_level

    def getLogger(self):
        return self.logger
