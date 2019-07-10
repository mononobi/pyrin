# -*- coding: utf-8 -*-
"""
packaging exceptions module.
"""

from pyrin.core.exceptions import CoreException


class PackagingManagerException(CoreException):
    """
    packaging manager exception.
    """
    pass


class InvalidPackageNameError(PackagingManagerException):
    """
    invalid package name error.
    """
    pass


class InvalidPackagingHookTypeError(PackagingManagerException):
    """
    invalid packaging hook type error.
    """
    pass