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


class InvalidRequestContextKeyNameError(SessionManagerException):
    """
    invalid request context key name error.
    """
    pass
