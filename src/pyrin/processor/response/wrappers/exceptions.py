# -*- coding: utf-8 -*-
"""
response wrappers exceptions module.
"""

from pyrin.core.exceptions import CoreException


class ResponseException(CoreException):
    """
    response exception.
    """
    pass


class InvalidResponseContextKeyNameError(ResponseException):
    """
    invalid response context key name error.
    """
    pass


class ResponseContextKeyIsAlreadyPresentError(ResponseException):
    """
    response context key is already present error.
    """
    pass
