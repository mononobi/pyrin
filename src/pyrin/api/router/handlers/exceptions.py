# -*- coding: utf-8 -*-
"""
router handlers exceptions module.
"""

from pyrin.core.exceptions import CoreException


class RouterHandlerException(CoreException):
    """
    router handler exception.
    """
    pass


class InvalidViewFunctionTypeError(RouterHandlerException):
    """
    invalid view function type error.
    """
    pass


class MaxContentLengthLimitMismatchError(RouterHandlerException):
    """
    max content length limit mismatch error.
    """
    pass
