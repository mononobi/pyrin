# -*- coding: utf-8 -*-
"""
security exceptions module.
"""

from pyrin.core.enumerations import ClientErrorResponseCodeEnum
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


class AuthenticationFailedError(SecurityManagerBusinessException):
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


class AuthorizationFailedError(SecurityManagerBusinessException):
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


class UserIsNotActiveError(AuthorizationFailedError):
    """
    user is not active error.
    """
    pass
