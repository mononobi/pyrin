# -*- coding: utf-8 -*-
"""
logging adapters module.
"""

from logging import Logger, raiseExceptions

import pyrin.security.session.services as session_services
import pyrin.logging.services as logging_services
import pyrin.utils.string as string_utils

from pyrin.logging.enumerations import LogLevelIntEnum


class BaseLoggerAdapter(Logger):
    """
    base logger adapter class.

    all logger adapters should be subclassed from this.

    this class is intended to be an adapter for `Logger`, but it is implemented
    this way because of two different issues:

    1. if we implement it as an stand-alone adapter and not subclassing it from
    `Logger`, then logging package will raise an error on wrapped loggers where
    it checks the type of logger against `Logger`. for example in fixup methods.

    2. if we fully subclass this from `Logger` and removing the adapter behavior,
    another issue arises and in different situations the generated logs will not
    be emitted correctly. because the original logger with the same name exists
    before instantiating the adapter.

    so we have to implement this class this way, subclass it from `Logger`, but in
    fact use it as an adapter and proxying all accesses to `Logger` attributes to the
    underlying actual `Logger` instance.

    also note that we *DO NOT* call `super().__init()` when initializing the adapter.
    because the actual logger is the `_logger` attribute and all operations will be
    proxied to it.
    """

    def __init__(self, logger):
        """
        initializes an instance of BaseLoggerAdapter.

        :param Logger logger: logger instance to be wrapped.
        """

        self.extra = {}
        self._logger = logger

    def __str__(self):
        """
        gets string representation of this logger.

        :rtype: str
        """

        return str(self._logger)

    def __repr__(self):
        """
        gets string representation of this logger.

        :rtype: str
        """

        return repr(self._logger)

    def __reduce__(self):
        """
        gets the reduced version of this logger.

        :rtype: tuple
        """

        return self._logger.__reduce__()

    def log(self, level, msg, *args, **kwargs):
        """
        delegates a log call to the underlying logger.

        this method is overridden to execute before and after emit hooks.
        and also performing interpolation data preparation if required.

        :param int level: log level.
        :param str msg: log message.
        :param dict kwargs: keyword arguments passed to logging call.

        :keyword dict interpolation_data: data to be used for interpolation.

        :raises TypeError: type error.
        """

        if not isinstance(level, int):
            if raiseExceptions:
                raise TypeError('log level must be an integer.')
            else:
                return

        if self.isEnabledFor(level):
            self._log(level, msg, args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """
        log message with `DEBUG` severity.

        to pass exception information, use the keyword argument `exc_info` with
        a true value.

        :param str msg: log message.

        :keyword dict interpolation_data: data to be used for interpolation.
        """

        if self.isEnabledFor(LogLevelIntEnum.DEBUG):
            self._log(LogLevelIntEnum.DEBUG, msg, args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        log message with `INFO` severity.

        to pass exception information, use the keyword argument `exc_info` with
        a true value.

        :param str msg: log message.

        :keyword dict interpolation_data: data to be used for interpolation.
        """

        if self.isEnabledFor(LogLevelIntEnum.INFO):
            self._log(LogLevelIntEnum.INFO, msg, args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        log message with `WARNING` severity.

        to pass exception information, use the keyword argument `exc_info` with
        a true value.

        :param str msg: log message.

        :keyword dict interpolation_data: data to be used for interpolation.
        """

        if self.isEnabledFor(LogLevelIntEnum.WARNING):
            self._log(LogLevelIntEnum.WARNING, msg, args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        """
        log message with `WARNING` severity.

        to pass exception information, use the keyword argument `exc_info` with
        a true value.

        :param str msg: log message.

        :keyword dict interpolation_data: data to be used for interpolation.
        """

        self.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        log message with `ERROR` severity.

        to pass exception information, use the keyword argument `exc_info` with
        a true value.

        :param str msg: log message.

        :keyword dict interpolation_data: data to be used for interpolation.
        """

        if self.isEnabledFor(LogLevelIntEnum.ERROR):
            self._log(LogLevelIntEnum.ERROR, msg, args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        """
        log exception with `ERROR` severity.

        :param str msg: log message.
        :param bool exc_info: include exception info in log message.

        :keyword dict interpolation_data: data to be used for interpolation.
        """

        self.error(msg, *args, exc_info=exc_info, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        log message with `CRITICAL` severity.

        to pass exception information, use the keyword argument `exc_info` with
        a true value.

        :param str msg: log message.

        :keyword dict interpolation_data: data to be used for interpolation.
        """

        if self.isEnabledFor(LogLevelIntEnum.CRITICAL):
            self._log(LogLevelIntEnum.CRITICAL, msg, args, **kwargs)

    def fatal(self, msg, *args, **kwargs):
        """
        log message with `CRITICAL` severity.

        to pass exception information, use the keyword argument `exc_info` with
        a true value.

        :param str msg: log message.

        :keyword dict interpolation_data: data to be used for interpolation.
        """

        self.critical(msg, *args, **kwargs)

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

    def setLevel(self, level):
        """
        sets the logging level of this logger. level must be an int or a str.

        :param int | str level: logging level to be set.
        """

        self._logger.setLevel(level)

    def findCaller(self, stack_info=False, stacklevel=1):
        """
        finds the stack frame of the caller.

        so that we can note the source file name, line number and function name.

        :param bool stack_info: include stack info.
        :param int stacklevel: stack level to be included.

        :rtype: tuple
        """

        return self._logger.findCaller(stack_info, stacklevel)

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info,
                   func=None, extra=None, sinfo=None):
        """
        a factory method which can be overridden in subclasses to create
        specialized `LogRecords`.

        :rtype: LogRecord
        """

        return self._logger.makeRecord(name, level, fn, lno, msg, args, exc_info,
                                       func=func, extra=extra, sinfo=sinfo)

    def handle(self, record):
        """
        calls the handlers for the specified record.

        this method is used for unpickled records received from a socket, as
        well as those created locally. logger-level filtering is applied.

        :param LogRecord record: log record instance.
        """

        self._logger.handle(record)

    def addHandler(self, hdlr):
        """
        adds the specified handler to this logger.
        """

        self._logger.addHandler(hdlr)

    def removeHandler(self, hdlr):
        """
        removes the specified handler from this logger.
        """

        self._logger.removeHandler(hdlr)

    def hasHandlers(self):
        """
        gets a value indicating that this logger has any configured handlers.

        loop through all handlers for this logger and its parents in the
        logger hierarchy. return true if a handler was found, else false.
        stop searching up the hierarchy whenever a logger with the `propagate`
        attribute set to zero is found - that will be the last logger which
        is checked for the existence of handlers.

        :rtype: bool
        """

        return self._logger.hasHandlers()

    def callHandlers(self, record):
        """
        passes a record to all relevant handlers.

        loop through all handlers for this logger and its parents in the
        logger hierarchy. if no handler was found, output a one-off error
        message to sys.stderr. stop searching up the hierarchy whenever a
        logger with the 'propagate' attribute set to zero is found - that
        will be the last logger whose handlers are called.

        :param LogRecord record: log record instance.
        """

        self._logger.callHandlers(record)

    def getEffectiveLevel(self):
        """
        gets the effective level for this logger.

        loop through this logger and its parents in the logger hierarchy,
        looking for a non-zero logging level. return the first one found.

        :rtype: int
        """

        return self._logger.getEffectiveLevel()

    def isEnabledFor(self, level):
        """
        gets a value indicating that this logger is enabled for given log level.

        :param int level: logging level.

        :rtype: bool
        """

        return self._logger.isEnabledFor(level)

    def getChild(self, suffix):
        """
        gets a logger which is a descendant to this one.

        this is a convenience method, such that:

        `logging.getLogger('abc').getChild('def.ghi')`

        is the same as:

        `logging.getLogger('abc.def.ghi')`

        it's useful, for example, when the parent logger is named using
        `__name__` rather than a literal string.
        """

        return self._logger.getChild(suffix)

    def _log(self, level, msg, args, exc_info=None, extra=None,
             stack_info=False, stacklevel=1, **options):
        """
        low-level logging routine which creates a `LogRecord`.

        and then calls all the handlers of this logger to handle the record.

        :param int level: logging level.
        :param str msg: log message.
        :param tuple args: logging arguments.
        :param bool exc_info: include exception info in log message.
        :param dict extra: extra keyword arguments.
        :param bool stack_info: include stack info.
        :param int stacklevel: stack level to be included.

        :keyword dict interpolation_data: data to be used for interpolation.
        """

        data = options.pop('interpolation_data', None)
        if data is not None:
            data = logging_services.prepare_data(data)
            msg = string_utils.interpolate(msg, data)

        custom_message, custom_kwargs = self.process(msg, options)
        logging_services.before_emit(custom_message, data, level, **custom_kwargs)
        self._logger._log(level, custom_message, args, exc_info=exc_info,
                          extra=extra, stack_info=stack_info, stacklevel=stacklevel)
        logging_services.after_emit(custom_message, data, level, **custom_kwargs)

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

    @property
    def name(self):
        """
        gets the name of this logger.

        :rtype: str
        """

        return self._logger.name

    @name.setter
    def name(self, value):
        """
        sets the name of this logger.

        :param str value: value to be set as name.
        """

        self._logger.name = value

    @property
    def level(self):
        """
        gets the level of this logger.

        :rtype: int
        """

        return self._logger.level

    @level.setter
    def level(self, value):
        """
        sets the level of this logger.

        :param int | str value: value to be set as level.
        """

        self._logger.level = value

    @property
    def parent(self):
        """
        gets the parent logger of this logger.

        :rtype: Logger
        """

        return self._logger.parent

    @parent.setter
    def parent(self, value):
        """
        sets the parent logger of this logger.

        :param Logger value: value to be set as parent.
        """

        self._logger.parent = value

    @property
    def propagate(self):
        """
        gets a value indicating that this logger must propagate exceptions.

        :rtype: bool
        """

        return self._logger.propagate

    @propagate.setter
    def propagate(self, value):
        """
        sets the propagate value of this logger.

        :param bool value: value to be set as propagate.
        """

        self._logger.propagate = value

    @property
    def handlers(self):
        """
        gets the handlers of this logger.

        :rtype: list
        """

        return self._logger.handlers

    @handlers.setter
    def handlers(self, value):
        """
        sets the handlers of this logger.

        :param list value: values to be set as handlers.
        """

        self._logger.handlers = value

    @property
    def disabled(self):
        """
        gets a value indicating that this logger is disabled.

        :rtype: bool
        """

        return self._logger.disabled

    @disabled.setter
    def disabled(self, value):
        """
        sets the disabled value of this logger.

        :param bool value: value to be set as disabled.
        """

        self._logger.disabled = value

    @property
    def _cache(self):
        """
        gets the cache of this logger.

        :rtype: dict
        """

        return self._logger._cache

    @_cache.setter
    def _cache(self, value):
        """
        sets the cache of this logger.

        :param dict value: value to be set as cache.
        """

        self._logger._cache = value


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
