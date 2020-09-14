# -*- coding: utf-8 -*-
"""
logging manager module.
"""

import logging
import logging.config

from logging import Logger

import pyrin.configuration.services as config_services

from pyrin.core.mixin import HookMixin
from pyrin.logging import LoggingPackage
from pyrin.core.structs import Manager
from pyrin.logging.adapters import RequestInfoLoggerAdapter, BaseLoggerAdapter
from pyrin.logging.hooks import LoggingHookBase
from pyrin.logging.exceptions import InvalidLoggerAdapterTypeError, LoggerNotExistedError, \
    InvalidLoggingHookTypeError


class LoggingManager(Manager, HookMixin):
    """
    logging manager class.
    """

    # the logger adapter could be overridden in subclasses.
    logger_adapter_class = RequestInfoLoggerAdapter
    hook_type = LoggingHookBase
    invalid_hook_type_error = InvalidLoggingHookTypeError
    package_class = LoggingPackage

    def __init__(self):
        """
        initializes an instance of LoggingManager.
        """

        super().__init__()

        self._config_file_path = config_services.get_file_path(
            self.package_class.EXTRA_CONFIG_STORE_NAMES[0])
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

        :returns: dict[str name: Logger instance]
        :rtype: dict
        """

        return logging.root.manager.loggerDict

    def _wrap_logger(self, logger):
        """
        wraps the given logger into an adapter and returns it.

        :param Logger logger: logger instance to be wrapped.

        :rtype: BaseLoggerAdapter | Logger
        """

        if self.should_be_wrapped(logger) is True:
            return self.logger_adapter_class(logger)

        return logger

    def _wrap_all_loggers(self):
        """
        wraps all available loggers into an adapter to inject request info into every log.

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

        unwrapped_loggers = config_services.get_active('logging', 'unwrapped_loggers')
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
                                                'instance of [{base}].'
                                                .format(adapter=adapter,
                                                        base=BaseLoggerAdapter))

        loggers = self._get_all_loggers()
        if name not in loggers:
            raise LoggerNotExistedError('Logger [{name}] does not exist.'
                                        .format(name=name))

        loggers[name] = adapter

    def get_all_loggers(self):
        """
        gets a dictionary containing all available loggers.

        it returns a shallow copy of loggers dict.

        :returns: dict[str name: Logger instance]
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
        if self.should_be_wrapped(logger) is True:
            logger = self._wrap_logger(logger)
            self._set_logger_adapter(name, logger)

        return logger

    def debug(self, msg, *args, **kwargs):
        """
        emits a log with debug level.

        :param str msg: log message.

        :keyword dict interpolation_data: data to be used for interpolation.
        """

        logging.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        emits a log with info level.

        :param str msg: log message.

        :keyword dict interpolation_data: data to be used for interpolation.
        """

        logging.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        emits a log with warning level.

        :param str msg: log message.

        :keyword dict interpolation_data: data to be used for interpolation.
        """

        logging.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        emits a log with error level.

        :param str msg: log message.

        :keyword dict interpolation_data: data to be used for interpolation.
        """

        logging.error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        """
        emits a log with error level and exception information.

        :param str msg: log message.

        :keyword dict interpolation_data: data to be used for interpolation.
        """

        logging.exception(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        emits a log with critical level.

        :param str msg: log message.

        :keyword dict interpolation_data: data to be used for interpolation.
        """

        logging.critical(msg, *args, **kwargs)

    def prepare_data(self, data, **options):
        """
        this method will call `prepare_data` method of all registered hooks.

        :param dict | object data: data that is passed to logging method.

        :returns: modified or same input data.
        :rtype: dict | object
        """

        prepared_data = data
        for hook in self._get_hooks():
            prepared_data = hook.prepare_data(prepared_data, **options)

        return prepared_data

    def before_emit(self, message, data, level, **options):
        """
        this method will call `before_emit` method of all registered hooks.

        :param str message: the log message that must be emitted.
        :param dict | object data: data that is passed to logging method.
        :param int level: log level.
        """

        for hook in self._get_hooks():
            hook.before_emit(message, data, level, **options)

    def after_emit(self, message, data, level, **options):
        """
        this method will call `after_emit` method of all registered hooks.

        :param str message: the log message that has been emitted.
        :param dict | object data: data that is passed to logging method.
        :param int level: log level.
        """

        for hook in self._get_hooks():
            hook.after_emit(message, data, level, **options)
