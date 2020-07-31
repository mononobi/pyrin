# -*- coding: utf-8 -*-
"""
logging exceptions module.
"""

from pyrin.core.exceptions import CoreException


class LoggingManagerException(CoreException):
    """
    logging manager exception.
    """
    pass


class InvalidLoggerAdapterTypeError(LoggingManagerException):
    """
    invalid logger adapter type error.
    """
    pass


class LoggerNotExistedError(LoggingManagerException):
    """
    logger not existed error.
    """
    pass


class InvalidLoggingHookTypeError(LoggingManagerException):
    """
    invalid logging hook type error.
    """
    pass
