# -*- coding: utf-8 -*-
"""
authentication exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class AuthenticationManagerException(CoreException):
    """
    authentication manager exception.
    """
    pass


class AuthenticationManagerBusinessException(CoreBusinessException,
                                             AuthenticationManagerException):
    """
    authentication manager business exception.
    """
    pass


class InvalidAuthenticatorTypeError(AuthenticationManagerException):
    """
    invalid authenticator type error.
    """
    pass


class DuplicatedAuthenticatorError(AuthenticationManagerException):
    """
    duplicated authenticator error.
    """
    pass


class AuthenticatorNotFoundError(AuthenticationManagerException):
    """
    authenticator not found error.
    """
    pass
