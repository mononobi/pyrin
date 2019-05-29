# -*- coding: utf-8 -*-
"""
logging manager module.
"""

import logging
import logging.config

import pyrin.configuration.services as config_services

from pyrin.core.context import CoreObject


class LoggingManager(CoreObject):
    """
    logging manager class.
    """

    CONFIG_STORE_NAME = 'logging'

    def __init__(self):
        """
        initializes an instance of LoggingManager.
        """

        CoreObject.__init__(self)

        self._config_file_path = config_services.get_file_path(self.CONFIG_STORE_NAME)
        self._load_configs(self._config_file_path)

    def _load_configs(self, config_file_path):
        """
        loads logging configuration and handlers from given file.

        :param str config_file_path: config file path.
        """

        logging.config.fileConfig(config_file_path)

    def reload_configs(self, **options):
        """
        reloads all logging configurations from config file.
        """

        self._load_configs(self._config_file_path)

    def get_logger(self, name, **options):
        """
        gets the logger based on input parameters.

        :param str name: logger name to get.

        :returns: specified logger.

        :rtype: Logger
        """

        return logging.getLogger(name)

    def debug(self, msg, *args, **kwargs):
        """
        emits a log with debug level.

        :param str msg: log message.
        """

        logging.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        emits a log with info level.

        :param str msg: log message.
        """

        logging.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        emits a log with warning level.

        :param str msg: log message.
        """

        logging.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        emits a log with error level.

        :param str msg: log message.
        """

        logging.error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        """
        emits a log with error level and exception information.

        :param str msg: log message.
        """

        logging.exception(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        emits a log with critical level.

        :param str msg: log message.
        """

        logging.critical(msg, *args, **kwargs)
