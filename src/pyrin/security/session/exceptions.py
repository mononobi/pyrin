# -*- coding: utf-8 -*-
"""
session exceptions module.
"""

from pyrin.core.exceptions import CoreBusinessException, CoreException


class SessionManagerException(CoreException):
    """
    session manager exception.
    """
    pass


class SessionManagerBusinessException(CoreBusinessException,
                                      SessionManagerException):
    """
    session manager business exception.
    """
    pass


class CouldNotOverwriteCurrentUserError(SessionManagerException):
    """
    could not overwrite current user error.
    """
    pass


class InvalidUserError(SessionManagerException):
    """
    invalid user error.
    """
    pass


class InvalidComponentCustomKeyError(SessionManagerException):
    """
    invalid component custom key error.
    """
    pass
