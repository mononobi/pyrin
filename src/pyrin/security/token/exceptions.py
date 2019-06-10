# -*- coding: utf-8 -*-
"""
token exceptions module.
"""

from pyrin.core.exceptions import CoreTypeError, CoreKeyError, CoreValueError


class InvalidTokenHandlerTypeError(CoreTypeError):
    """
    invalid token handler type error.
    """
    pass


class DuplicatedTokenHandlerError(CoreKeyError):
    """
    duplicated token handler error.
    """
    pass


class TokenHandlerNotFoundError(CoreKeyError):
    """
    token handler not found error.
    """
    pass


class InvalidTokenHandlerNameError(CoreValueError):
    """
    invalid token handler name error.
    """
    pass


class TokenKidHeaderNotSpecifiedError(CoreKeyError):
    """
    token kid header not specified error.
    """
    pass


class TokenKidHeaderNotFoundError(CoreKeyError):
    """
    token kid header not found error.
    """
    pass


class DuplicatedTokenKidHeaderError(CoreKeyError):
    """
    duplicated token kid header error.
    """
    pass
