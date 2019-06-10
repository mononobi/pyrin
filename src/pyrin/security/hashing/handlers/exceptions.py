# -*- coding: utf-8 -*-
"""
hashing handlers exceptions module.
"""

from pyrin.core.exceptions import CoreValueError


class BcryptMaxSizeLimitError(CoreValueError):
    """
    bcrypt max size limit error.
    """
    pass


class InvalidHashingRoundsCountError(CoreValueError):
    """
    invalid hashing rounds count error error.
    """
    pass


class InvalidPBKDF2InternalAlgorithmError(CoreValueError):
    """
    invalid pbkdf2 internal algorithm error.
    """
    pass


class InvalidHashingSaltLengthError(CoreValueError):
    """
    invalid hashing salt length error.
    """
    pass


class InvalidPBKDF2HashError(CoreValueError):
    """
    invalid pbkdf2 hash error.
    """
    pass
