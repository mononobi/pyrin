# -*- coding: utf-8 -*-
"""
authentication exceptions module.
"""

from pyrin.core.enumerations import ClientErrorResponseCodeEnum
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


class AuthenticationFailedError(AuthenticationManagerBusinessException):
    """
    authentication failed error.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of AuthenticationFailedError.

        :keyword dict data: extra data for exception.
        """

        super().__init__(*args, **kwargs)
        self._code = ClientErrorResponseCodeEnum.UNAUTHORIZED


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
