# -*- coding: utf-8 -*-
"""
token exceptions module.
"""

from jwt.exceptions import PyJWTError

from pyrin.core.exceptions import CoreException, CoreBusinessException


class TokenManagerException(CoreException):
    """
    token manager exception.
    """
    pass


class TokenManagerBusinessException(CoreBusinessException,
                                    TokenManagerException):
    """
    token manager business exception.
    """
    pass


class TokenManagerVerificationFailedException(TokenManagerBusinessException):
    """
    token manager verification failed exception.
    """
    pass


class InvalidTokenHandlerTypeError(TokenManagerException):
    """
    invalid token handler type error.
    """
    pass


class DuplicatedTokenHandlerError(TokenManagerException):
    """
    duplicated token handler error.
    """
    pass


class TokenHandlerNotFoundError(TokenManagerVerificationFailedException):
    """
    token handler not found error.
    """
    pass


class InvalidTokenHandlerNameError(TokenManagerException):
    """
    invalid token handler name error.
    """
    pass


class TokenKidHeaderNotSpecifiedError(TokenManagerVerificationFailedException):
    """
    token kid header not specified error.
    """
    pass


class TokenKidHeaderNotFoundError(TokenManagerVerificationFailedException):
    """
    token kid header not found error.
    """
    pass


class DuplicatedTokenKidHeaderError(TokenManagerException):
    """
    duplicated token kid header error.
    """
    pass


class TokenIsBlackListedError(TokenManagerVerificationFailedException):
    """
    token is black listed error.
    """
    pass


class TokenSignatureError(TokenManagerVerificationFailedException,
                          PyJWTError):
    """
    token signature error.
    """
    pass
