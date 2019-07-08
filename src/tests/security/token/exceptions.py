# -*- coding: utf-8 -*-
"""
token exceptions module.
"""

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


class TokenDecodingError(TokenManagerBusinessException):
    """
    token decoding error.
    """
    pass


class TokenVerificationError(TokenDecodingError):
    """
    token verification error.
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


class TokenHandlerNotFoundError(TokenVerificationError):
    """
    token handler not found error.
    """
    pass


class InvalidTokenHandlerNameError(TokenManagerException):
    """
    invalid token handler name error.
    """
    pass


class TokenKidHeaderNotSpecifiedError(TokenVerificationError):
    """
    token kid header not specified error.
    """
    pass


class TokenKidHeaderNotFoundError(TokenVerificationError):
    """
    token kid header not found error.
    """
    pass


class DuplicatedTokenKidHeaderError(TokenManagerException):
    """
    duplicated token kid header error.
    """
    pass
