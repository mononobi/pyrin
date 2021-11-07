# -*- coding: utf-8 -*-
"""
authentication handlers exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException
from pyrin.security.exceptions import AuthenticationFailedError


class AuthenticationHandlersException(CoreException):
    """
    authentication handlers exception.
    """
    pass


class AuthenticationHandlersBusinessException(CoreBusinessException,
                                              AuthenticationHandlersException):
    """
    authentication handlers business exception.
    """
    pass


class AccessAndRefreshTokensDoesNotBelongToSameUserError(AuthenticationFailedError,
                                                         AuthenticationHandlersBusinessException):
    """
    access and refresh tokens does not belong to same user error.
    """
    pass


class InvalidTokenAuthenticatorError(AuthenticationFailedError,
                                     AuthenticationHandlersBusinessException):
    """
    invalid token authenticator error.
    """
    pass


class AuthenticatorNameIsRequiredError(AuthenticationHandlersException):
    """
    authenticator name is required error.
    """
    pass


class AccessTokenRequiredError(AuthenticationFailedError,
                               AuthenticationHandlersBusinessException):
    """
    access token required error.
    """
    pass


class RefreshTokenRequiredError(AuthenticationFailedError,
                                AuthenticationHandlersBusinessException):
    """
    refresh token required error.
    """
    pass


class InvalidAccessTokenError(AuthenticationFailedError,
                              AuthenticationHandlersBusinessException):
    """
    invalid access token error.
    """
    pass


class InvalidRefreshTokenError(AuthenticationFailedError,
                               AuthenticationHandlersBusinessException):
    """
    invalid refresh token error.
    """
    pass


class UserCredentialsRevokedError(AuthenticationFailedError,
                                  AuthenticationHandlersBusinessException):
    """
    user credentials revoked error.
    """
    pass


class InvalidUserError(AuthenticationHandlersException):
    """
    invalid user error.
    """
    pass


class InvalidUserIdentityError(AuthenticationHandlersException):
    """
    invalid user identity error.
    """
    pass


class ProvidedUsernameOrPasswordAreIncorrect(AuthenticationFailedError,
                                             AuthenticationHandlersBusinessException):
    """
    provided username or password are incorrect.
    """
    pass
