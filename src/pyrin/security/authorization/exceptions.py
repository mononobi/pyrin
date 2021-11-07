# -*- coding: utf-8 -*-
"""
authorization exceptions module.
"""

from pyrin.core.exceptions import CoreBusinessException, CoreException
from pyrin.security.exceptions import AuthenticationFailedError, AuthorizationFailedError


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


class UserNotAuthenticatedError(AuthenticationFailedError,
                                AuthorizationFailedError):
    """
    user not authenticated error.
    """
    pass


class PermissionDeniedError(AuthorizationFailedError):
    """
    permission denied error.
    """
    pass


class InvalidAuthorizerTypeError(AuthorizationManagerException):
    """
    invalid authorizer type error.
    """
    pass


class DuplicatedAuthorizerError(AuthorizationManagerException):
    """
    duplicated authorizer error.
    """
    pass


class AuthorizerNotFoundError(AuthorizationManagerException):
    """
    authorizer not found error.
    """
    pass
