# -*- coding: utf-8 -*-
"""
encryption handlers exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class EncryptionHandlerException(CoreException):
    """
    encryption handler exception.
    """
    pass


class EncryptionHandlerBusinessException(CoreBusinessException,
                                         EncryptionHandlerException):
    """
    encryption handler business exception.
    """
    pass


class InvalidEncryptedValueError(EncryptionHandlerBusinessException):
    """
    invalid encrypted value error.
    """
    pass


class EncryptionHandlerMismatchError(EncryptionHandlerBusinessException):
    """
    encryption handler mismatch error.
    """
    pass
