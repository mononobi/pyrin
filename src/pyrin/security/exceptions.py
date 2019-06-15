# -*- coding: utf-8 -*-
"""
security exceptions module.
"""

from pyrin.core.exceptions import CoreException


class SecurityManagerException(CoreException):
    """
    security manager exception.
    """
    pass


class InvalidPasswordLengthError(SecurityManagerException):
    """
    invalid password length error.
    """
    pass


class InvalidEncryptionTextLengthError(SecurityManagerException):
    """
    invalid encryption text length error.
    """
    pass
