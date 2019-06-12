# -*- coding: utf-8 -*-
"""
encryption exceptions module.
"""

from pyrin.core.exceptions import CoreTypeError, CoreKeyError, CoreValueError


class InvalidEncryptionHandlerTypeError(CoreTypeError):
    """
    invalid encryption handler type error.
    """
    pass


class DuplicatedEncryptionHandlerError(CoreKeyError):
    """
    duplicated encryption handler error.
    """
    pass


class EncryptionHandlerNotFoundError(CoreKeyError):
    """
    encryption handler not found error.
    """
    pass


class InvalidEncryptionHandlerNameError(CoreValueError):
    """
    invalid encryption handler name error.
    """
    pass


class InvalidEncryptedValueError(CoreValueError):
    """
    invalid encrypted value error.
    """
    pass
