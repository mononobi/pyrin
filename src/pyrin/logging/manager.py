# -*- coding: utf-8 -*-
"""
logging manager module.
"""

import logging
import logging.config

from logging import Logger

import pyrin.configuration.services as config_services

from pyrin.logging import LoggingPackage
from pyrin.core.context import Manager
from pyrin.logging.adapters import RequestInfoLoggerAdapter, BaseLoggerAdapter
from pyrin.logging.exceptions import InvalidLoggerAdapterTypeError, LoggerNotExistedError


class LoggingManager(Manager):
    """
    logging manager class.
    """

    def __init__(self):
        """
        initializes an instance of LoggingManager.
        """

        super().__init__()

        self._config_file_path = config_services.get_file_path(
            LoggingPackage.LOGGER_HANDLERS_STORE_NAME)
        self._load_configs(self._config_file_path)

    def _load_configs(self, config_file_path):
        """
        loads logging configuration and handlers from given file.

        :param str config_file_path: config file path.
        """

        logging.config.fileConfig(config_file_path, disable_existing_loggers=True)

    def _wrap_root_logger(self):
        """
        wraps the root logger into an adapter.
        """

        logging.root = self._wrap_logger(logging.root)

    def _get_all_loggers(self):
        """
        gets a dictionary containing all available loggers.

        :returns: dict(str name: Logger instance)

        :rtype: dict
        """

        return logging.root.manager.loggerDict

    def _wrap_logger(self, logger):
        """
        wraps the given logger into an adapter and returns it.

        :param Logger logger: logger instance to be wrapped.

        :rtype: Union[BaseLoggerAdapter, Logger]
        """

        if isinstance(logger, Logger):
            return RequestInfoLoggerAdapter(logger)

        return logger

    def _wrap_all_loggers(self):
        """
        wraps all available loggers into an adapter to
        inject request info into every log.

        note that we should not wrap sqlalchemy and alembic loggers,
        because it does not affect on sqlalchemy loggers and they
        never have request info in emitted logs, I don't know the reason.
        but wrapping them actually has a side effect which leads to some errors.
        so we do not wrap them in the first place.
        """

        self._wrap_root_logger()

        for name, logger in self._get_all_loggers().items():
            if self.should_be_wrapped(logger) is True:
                self._set_logger_adapter(name, self._wrap_logger(logger))

    def should_be_wrapped(self, logger):
        """
        gets a value indication that given logger should be wrapped.

        note that we should not wrap sqlalchemy and alembic loggers,
        because it does not affect on sqlalchemy loggers and they
        never have request info in emitted logs, I don't know the reason.
        but wrapping them actually has a side effect which leads to some errors.
        so we do not wrap them in the first place.

        :param Logger logger: logger to check should it be wrapped.

        :rtype: bool
        """

        if not isinstance(logger, Logger):
            return False

        unwrapped_loggers = config_services.get('logging', 'general', 'unwrapped_loggers')
        return all(item not in logger.name for item in unwrapped_loggers)

    def wrap_all_loggers(self):
        """
        wraps all available loggers into an adapter.
        normally, this method should not be called manually.
        """

        self._wrap_all_loggers()

    def _set_logger_adapter(self, name, adapter):
        """
        sets the logger adapter instance with the specified name into logging loggerDict.

        :param str name: name of the logger adapter.
        :param BaseLoggerAdapter adapter: logger adapter instance.

        :raises InvalidLoggerAdapterTypeError: invalid logger adapter type error.
        :raises LoggerNotExistedError: logger not existed error.
        """

        if not isinstance(adapter, BaseLoggerAdapter):
            raise InvalidLoggerAdapterTypeError('Input parameter [{adapter}] is not an '
                                                'instance of BaseLoggerAdapter.'
                                                .format(adapter=str(adapter)))

        loggers = self._get_all_loggers()
        if name not in loggers.keys():
            raise LoggerNotExistedError('Logger [{name}] does not exist.'
                                        .format(name=name))

        loggers[name] = adapter

    def get_all_loggers(self):
        """
        gets a dictionary containing all available loggers.
        it returns a shallow copy of loggers dict.

        :returns: dict(str name: Logger instance)

        :rtype: dict
        """

        return self._get_all_loggers().copy()

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

        :rtype: BaseLoggerAdapter
        """

        logger = logging.getLogger(name)
        adapter = logger
        if isinstance(adapter, Logger):
            adapter = self._wrap_logger(logger)
            self._set_logger_adapter(name, adapter)

        return adapter

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
