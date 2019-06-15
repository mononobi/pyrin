# -*- coding: utf-8 -*-
"""
token exceptions module.
"""

from pyrin.core.exceptions import CoreException


class TokenManagerException(CoreException):
    """
    token manager exception.
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


class TokenHandlerNotFoundError(TokenManagerException):
    """
    token handler not found error.
    """
    pass


class InvalidTokenHandlerNameError(TokenManagerException):
    """
    invalid token handler name error.
    """
    pass


class TokenKidHeaderNotSpecifiedError(TokenManagerException):
    """
    token kid header not specified error.
    """
    pass


class TokenKidHeaderNotFoundError(TokenManagerException):
    """
    token kid header not found error.
    """
    pass


class DuplicatedTokenKidHeaderError(TokenManagerException):
    """
    duplicated token kid header error.
    """
    pass


class TokenIsBlackListedError(TokenManagerException):
    """
    token is black listed error.
    """
    pass
