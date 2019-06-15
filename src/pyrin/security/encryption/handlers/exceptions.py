# -*- coding: utf-8 -*-
"""
encryption handlers exceptions module.
"""

from pyrin.core.exceptions import CoreException


class EncryptionHandlerException(CoreException):
    """
    encryption handler exception.
    """
    pass


class InvalidEncryptedValueError(EncryptionHandlerException):
    """
    invalid encrypted value error.
    """
    pass


class EncryptionHandlerMismatchError(EncryptionHandlerException):
    """
    encryption handler mismatch error.
    """
    pass
