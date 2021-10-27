# -*- coding: utf-8 -*-
"""
authorization handlers exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class AuthorizationHandlersException(CoreException):
    """
    authorization handlers exception.
    """
    pass


class AuthorizationHandlersBusinessException(CoreBusinessException,
                                             AuthorizationHandlersException):
    """
    authorization handlers business exception.
    """
    pass


class AuthorizerNameIsRequiredError(AuthorizationHandlersException):
    """
    authorizer name is required error.
    """
    pass
