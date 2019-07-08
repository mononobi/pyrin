# -*- coding: utf-8 -*-
"""
hashing handlers exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class HashingHandlerException(CoreException):
    """
    hashing handler exception.
    """
    pass


class HashingHandlerBusinessException(CoreBusinessException,
                                      HashingHandlerException):
    """
    hashing handler business exception.
    """
    pass


class BcryptMaxSizeLimitError(HashingHandlerBusinessException):
    """
    bcrypt max size limit error.
    """
    pass


class InvalidHashingRoundsCountError(HashingHandlerBusinessException):
    """
    invalid hashing rounds count error error.
    """
    pass


class InvalidPBKDF2InternalAlgorithmError(HashingHandlerBusinessException):
    """
    invalid pbkdf2 internal algorithm error.
    """
    pass


class InvalidHashingSaltLengthError(HashingHandlerBusinessException):
    """
    invalid hashing salt length error.
    """
    pass


class HashingHandlerMismatchError(HashingHandlerBusinessException):
    """
    hashing handler mismatch error.
    """
    pass


class InvalidHashedValueError(HashingHandlerBusinessException):
    """
    invalid hashed value error.
    """
    pass
