# -*- coding: utf-8 -*-
"""
permission exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class PermissionManagerException(CoreException):
    """
    permission manager exception.
    """
    pass


class PermissionManagerBusinessException(CoreBusinessException,
                                         PermissionManagerException):
    """
    permission manager business exception.
    """
    pass


class InvalidPermissionTypeError(PermissionManagerException):
    """
    invalid permission type error.
    """
    pass


class InvalidPermissionIDError(PermissionManagerException):
    """
    invalid permission id error.
    """
    pass


class DuplicatedPermissionError(PermissionManagerException):
    """
    duplicated permission error.
    """
    pass


class PermissionNotFoundError(PermissionManagerBusinessException):
    """
    permission not found error.
    """
    pass
