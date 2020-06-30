# -*- coding: utf-8 -*-
"""
request wrappers exceptions module.
"""

from pyrin.core.exceptions import CoreException


class RequestWrappersException(CoreException):
    """
    request wrappers exception.
    """
    pass


class InvalidRequestContextKeyNameError(RequestWrappersException):
    """
    invalid request context key name error.
    """
    pass


class RequestContextKeyIsAlreadyPresentError(RequestWrappersException):
    """
    request context key is already present error.
    """
    pass
