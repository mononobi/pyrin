# -*- coding: utf-8 -*-
"""
hashing exceptions module.
"""

from pyrin.core.exceptions import CoreTypeError, CoreKeyError, CoreValueError


class InvalidHashingHandlerTypeError(CoreTypeError):
    """
    invalid hashing handler type error.
    """
    pass


class DuplicatedHashingHandlerError(CoreKeyError):
    """
    duplicated hashing handler error.
    """
    pass


class HashingHandlerNotFoundError(CoreKeyError):
    """
    hashing handler not found error.
    """
    pass


class InvalidHashingHandlerNameError(CoreValueError):
    """
    invalid hashing handler name error.
    """
    pass


class InvalidHashError(CoreValueError):
    """
    invalid hash error.
    """
    pass
