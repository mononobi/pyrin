# -*- coding: utf-8 -*-
"""
request exceptions module.
"""

from pyrin.core.exceptions import CoreException


class RequestException(CoreException):
    """
    request exception.
    """
    pass


class InvalidRequestContextKeyNameError(RequestException):
    """
    invalid request context key name error.
    """
    pass


class RequestContextKeyIsAlreadyPresentError(RequestException):
    """
    request context key is already present error.
    """
    pass
