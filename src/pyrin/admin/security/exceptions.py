# -*- coding: utf-8 -*-
"""
admin security exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException
from pyrin.security.exceptions import AuthorizationFailedError


class AdminSecurityException(CoreException):
    """
    admin security exception.
    """
    pass


class AdminSecurityBusinessException(CoreBusinessException,
                                     AdminSecurityException):
    """
    admin security business exception.
    """
    pass


class AdminAccessNotAllowedError(AuthorizationFailedError,
                                 AdminSecurityBusinessException):
    """
    admin access not allowed error.
    """
    pass
