# -*- coding: utf-8 -*-
"""
logging adapters module.
"""

from logging import Logger

import pyrin.security.session.services as session_services
import pyrin.logging.services as logging_services
import pyrin.utils.string as string_utils

from pyrin.logging.enumerations import LogLevelIntEnum


class BaseLoggerAdapter(Logger):
    """
    base logger adapter class.

    all logger adapters should be subclassed from this.
    """

    def __init__(self, logger):
        """
        initializes an instance of BaseLoggerAdapter.

        :param Logger logger: logger instance to be wrapped.
        """

        super().__init__(logger.name, logger.level)
        self.extra = {}

    def log(self, level, msg, *args, **kwargs):
        """
        delegates a log call to the underlying logger.

        this method is overridden to execute before and after emit hooks.
        and also performing interpolation data preparation if required.

        :param int level: log level.
        :param str msg: log message.
        :param dict kwargs: keyword arguments passed to logging call.

        :keyword dict interpolation_data: data to be used for interpolation.
        """

        if self.isEnabledFor(level):
            data = kwargs.pop('interpolation_data', None)
            if data is not None:
                data = logging_services.prepare_data(data)
                msg = string_utils.interpolate(msg, data)

            custom_message, custom_kwargs = self.process(msg, kwargs)
            logging_services.before_emit(custom_message, data, level, **custom_kwargs)
            super().log(level, custom_message, *args, **custom_kwargs)
            logging_services.after_emit(custom_message, data, level, **custom_kwargs)

    def debug(self, msg, *args, **kwargs):
        """
        log message with `DEBUG` severity.

        to pass exception information, use the keyword argument `exc_info` with
        a true value.

        :param str msg: log message.
        """

        self.log(LogLevelIntEnum.DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        log message with `INFO` severity.

        to pass exception information, use the keyword argument `exc_info` with
        a true value.

        :param str msg: log message.
        """

        self.log(LogLevelIntEnum.INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        log message with `WARNING` severity.

        to pass exception information, use the keyword argument `exc_info` with
        a true value.

        :param str msg: log message.
        """

        self.log(LogLevelIntEnum.WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        log message with `ERROR` severity.

        to pass exception information, use the keyword argument `exc_info` with
        a true value.

        :param str msg: log message.
        """

        self.log(LogLevelIntEnum.ERROR, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        log message with `CRITICAL` severity.

        to pass exception information, use the keyword argument `exc_info` with
        a true value.

        :param str msg: log message.
        """

        self.log(LogLevelIntEnum.CRITICAL, msg, *args, **kwargs)

    def process(self, msg, kwargs):
        """
        processes the logging message and keyword arguments passed in to a logging call.

        it's to insert contextual information. you can either manipulate
        the message itself, the keyword args or both. return the message
        and kwargs modified (or not) to suit your needs.

        :param str msg: log message.
        :param dict kwargs: keyword arguments passed to logging call.

        :returns: tuple[str message, dict kwargs]
        :rtype: tuple[str, dict]
        """

        kwargs["extra"] = self.extra
        return self._process(msg, kwargs)

    def _process(self, msg, kwargs):
        """
        processes the logging message and keyword arguments passed in to a logging call.

        it's to insert contextual information. you can either manipulate
        the message itself, the keyword args or both. return the message
        and kwargs modified (or not) to suit your needs.

        this method is intended to be overridden in subclasses.

        :param str msg: log message.
        :param dict kwargs: keyword arguments passed to logging call.

        :returns: tuple[str message, dict kwargs]
        :rtype: tuple[str, dict]
        """

        return msg, kwargs


class RequestInfoLoggerAdapter(BaseLoggerAdapter):
    """
    request info logger adapter.

    this adapter adds request info into generated logs.
    """

    def _process(self, msg, kwargs):
        """
        processes the logging message and keyword arguments passed in to a logging call.

        it's to insert contextual information. you can either manipulate
        the message itself, the keyword args or both. return the message
        and kwargs modified (or not) to suit your needs.

        :param str msg: log message.
        :param dict kwargs: keyword arguments passed to logging call.

        :returns: tuple[str message, dict kwargs]
        :rtype: tuple[str, dict]
        """

        client_request = session_services.get_safe_current_request()
        request_info = ''
        if client_request is not None:
            request_info = '[{client_request}]: '.format(client_request=client_request)

        custom_message = '{request_info}{message}'.format(request_info=request_info,
                                                          message=msg)
        return custom_message, kwargs
