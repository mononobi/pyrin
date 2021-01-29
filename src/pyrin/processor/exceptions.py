# -*- coding: utf-8 -*-
"""
processor exceptions module.
"""

from pyrin.core.exceptions import CoreException


class ProcessorException(CoreException):
    """
    processor exception.
    """
    pass


class RequestIDAlreadySetError(ProcessorException):
    """
    request id already set error.
    """
    pass


class RequestDateAlreadySetError(ProcessorException):
    """
    request date already set error.
    """
    pass


class RequestUserAlreadySetError(ProcessorException):
    """
    request user already set error.
    """
    pass
