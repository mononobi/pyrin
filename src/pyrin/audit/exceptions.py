# -*- coding: utf-8 -*-
"""
audit exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class AuditManagerException(CoreException):
    """
    audit manager exception.
    """
    pass


class AuditManagerBusinessException(CoreBusinessException, AuditManagerException):
    """
    audit manager business exception.
    """
    pass


class InvalidAuditHookTypeError(AuditManagerException):
    """
    invalid audit hook type error.
    """
    pass


class AuditFailedError(AuditManagerException):
    """
    audit failed error.
    """
    pass
