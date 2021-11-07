# -*- coding: utf-8 -*-
"""
audit security exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException
from pyrin.security.exceptions import AuthorizationFailedError


class AuditSecurityException(CoreException):
    """
    audit security exception.
    """
    pass


class AuditSecurityBusinessException(CoreBusinessException,
                                     AuditSecurityException):
    """
    audit security business exception.
    """
    pass


class AuditAccessNotAllowedError(AuthorizationFailedError,
                                 AuditSecurityBusinessException):
    """
    audit access not allowed error.
    """
    pass
