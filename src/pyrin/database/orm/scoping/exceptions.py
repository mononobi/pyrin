# -*- coding: utf-8 -*-
"""
orm scoping exceptions module.
"""

from sqlalchemy.exc import InvalidRequestError

from pyrin.core.exceptions import CoreException


class ORMScopingException(CoreException):
    """
    orm scoping exception.
    """
    pass


class InvalidRequestScopedRegistryTypeError(ORMScopingException):
    """
    invalid request scoped registry type error.
    """
    pass


class InvalidThreadScopedRegistryTypeError(ORMScopingException):
    """
    invalid thread scoped registry type error.
    """
    pass


class ScopedSessionIsAlreadyPresentError(InvalidRequestError, ORMScopingException):
    """
    scoped session is already present error.
    """
    pass
