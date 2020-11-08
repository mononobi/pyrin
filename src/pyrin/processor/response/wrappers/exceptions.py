# -*- coding: utf-8 -*-
"""
response wrappers exceptions module.
"""

from pyrin.core.exceptions import CoreException


class ResponseWrappersException(CoreException):
    """
    response wrappers exception.
    """
    pass


class InvalidResponseContextKeyNameError(ResponseWrappersException):
    """
    invalid response context key name error.
    """
    pass


class ResponseContextKeyIsAlreadyPresentError(ResponseWrappersException):
    """
    response context key is already present error.
    """
    pass


class ResponseEnvironRequiredError(ResponseWrappersException):
    """
    response environ required error.
    """
    pass
