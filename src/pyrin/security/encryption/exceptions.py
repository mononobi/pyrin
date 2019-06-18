# -*- coding: utf-8 -*-
"""
encryption exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class EncryptionManagerException(CoreException):
    """
    encryption manager exception.
    """
    pass


class EncryptionManagerBusinessException(CoreBusinessException,
                                         EncryptionManagerException):
    """
    encryption manager business exception.
    """
    pass


class DecryptionError(EncryptionManagerBusinessException):
    """
    decryption error.
    """
    pass


class InvalidEncryptionHandlerTypeError(EncryptionManagerException):
    """
    invalid encryption handler type error.
    """
    pass


class DuplicatedEncryptionHandlerError(EncryptionManagerException):
    """
    duplicated encryption handler error.
    """
    pass


class EncryptionHandlerNotFoundError(EncryptionManagerException):
    """
    encryption handler not found error.
    """
    pass


class InvalidEncryptionHandlerNameError(EncryptionManagerException):
    """
    invalid encryption handler name error.
    """
    pass


class InvalidEncryptedValueError(EncryptionManagerBusinessException):
    """
    invalid encrypted value error.
    """
    pass
