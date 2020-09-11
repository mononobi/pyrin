# -*- coding: utf-8 -*-
"""
logging enumerations module.
"""

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
