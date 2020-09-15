# -*- coding: utf-8 -*-
"""
logging enumerations module.
"""

import logging

from pyrin.core.enumerations import CoreEnum


class LogLevelEnum(CoreEnum):
    """
    log level enum.
    """

    NOTSET = 'NOTSET'
    CRITICAL = 'CRITICAL'
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    INFO = 'INFO'
    DEBUG = 'DEBUG'


class LogLevelIntEnum(CoreEnum):
    """
    log level int enum.
    """

    NOTSET = logging.NOTSET
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
