# -*- coding: utf-8 -*-
"""
permissions exceptions module.
"""

from pyrin.core.exceptions import CoreTypeError, CoreValueError, CoreKeyError


class InvalidPermissionTypeError(CoreTypeError):
    """
    invalid permission type error.
    """
    pass


class InvalidPermissionIDError(CoreValueError):
    """
    invalid permission id error.
    """
    pass


class DuplicatedPermissionError(CoreKeyError):
    """
    duplicated permission error.
    """
    pass


class PermissionNotFoundError(CoreKeyError):
    """
    permission not found error.
    """
    pass
