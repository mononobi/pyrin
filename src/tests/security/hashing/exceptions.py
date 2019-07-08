# -*- coding: utf-8 -*-
"""
hashing exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class HashingManagerException(CoreException):
    """
    hashing manager exception.
    """
    pass


class HashingManagerBusinessException(CoreBusinessException,
                                      HashingManagerException):
    """
    hashing manager business exception.
    """
    pass


class InvalidHashingHandlerTypeError(HashingManagerException):
    """
    invalid hashing handler type error.
    """
    pass


class DuplicatedHashingHandlerError(HashingManagerException):
    """
    duplicated hashing handler error.
    """
    pass


class HashingHandlerNotFoundError(HashingManagerException):
    """
    hashing handler not found error.
    """
    pass


class InvalidHashingHandlerNameError(HashingManagerException):
    """
    invalid hashing handler name error.
    """
    pass


class InvalidHashError(HashingManagerBusinessException):
    """
    invalid hash error.
    """
    pass
