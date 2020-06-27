# -*- coding: utf-8 -*-
"""
authorization exceptions module.
"""

from pyrin.core.enumerations import ClientErrorResponseCodeEnum
from pyrin.core.exceptions import CoreBusinessException, CoreException
from pyrin.security.authentication.exceptions import AuthenticationFailedError


class AuthorizationManagerException(CoreException):
    """
    authorization manager exception.
    """
    pass


class AuthorizationManagerBusinessException(CoreBusinessException,
                                            AuthorizationManagerException):
    """
    authorization manager business exception.
    """
    pass


class AuthorizationFailedError(AuthorizationManagerBusinessException):
    """
    authorization failed error.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of AuthorizationFailedError.

        :keyword dict data: extra data for exception.
        """

        super().__init__(*args, **kwargs)
        self._code = ClientErrorResponseCodeEnum.FORBIDDEN


class UserNotAuthenticatedError(AuthenticationFailedError,
                                AuthorizationFailedError):
    """
    user not authenticated error.
    """
    pass


class UserIsNotActiveError(AuthorizationFailedError):
    """
    user is not active error.
    """
    pass
