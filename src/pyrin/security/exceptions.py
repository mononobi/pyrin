# -*- coding: utf-8 -*-
"""
security exceptions module.
"""

from pyrin.core.exceptions import CoreBusinessException, CoreException


class SecurityManagerException(CoreException):
    """
    security manager exception.
    """
    pass


class SecurityManagerBusinessException(CoreBusinessException,
                                       SecurityManagerException):
    """
    security manager business exception.
    """
    pass


class InvalidPasswordLengthError(SecurityManagerBusinessException):
    """
    invalid password length error.
    """
    pass


class InvalidEncryptionTextLengthError(SecurityManagerBusinessException):
    """
    invalid encryption text length error.
    """
    pass
