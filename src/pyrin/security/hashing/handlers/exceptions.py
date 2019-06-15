# -*- coding: utf-8 -*-
"""
hashing handlers exceptions module.
"""

from pyrin.core.exceptions import CoreException


class HashingHandlerException(CoreException):
    """
    hashing handler exception.
    """
    pass


class BcryptMaxSizeLimitError(HashingHandlerException):
    """
    bcrypt max size limit error.
    """
    pass


class InvalidHashingRoundsCountError(HashingHandlerException):
    """
    invalid hashing rounds count error error.
    """
    pass


class InvalidPBKDF2InternalAlgorithmError(HashingHandlerException):
    """
    invalid pbkdf2 internal algorithm error.
    """
    pass


class InvalidHashingSaltLengthError(HashingHandlerException):
    """
    invalid hashing salt length error.
    """
    pass


class HashingHandlerMismatchError(HashingHandlerException):
    """
    hashing handler mismatch error.
    """
    pass


class InvalidHashedValueError(HashingHandlerException):
    """
    invalid hashed value error.
    """
    pass
