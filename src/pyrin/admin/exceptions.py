# -*- coding: utf-8 -*-
"""
admin exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class AdminManagerException(CoreException):
    """
    admin manager exception.
    """
    pass


class AdminManagerBusinessException(CoreBusinessException,
                                    AdminManagerException):
    """
    admin manager business exception.
    """
    pass


class InvalidAdminPageTypeError(AdminManagerException):
    """
    invalid admin page type error.
    """
    pass
