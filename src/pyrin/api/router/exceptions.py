# -*- coding: utf-8 -*-
"""
router exceptions module.
"""

from pyrin.core.exceptions import CoreException


class RouterException(CoreException):
    """
    router exception.
    """
    pass


class RouteAuthenticationMismatchError(RouterException):
    """
    route authentication mismatch error.
    """
    pass


class InvalidCustomRouteTypeError(RouterException):
    """
    invalid custom route type error.
    """
    pass
