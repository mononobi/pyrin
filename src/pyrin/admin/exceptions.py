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


class InvalidAdminEntityTypeError(AdminManagerException):
    """
    invalid admin entity type error.
    """
    pass


class AdminRegisterNameRequiredError(AdminManagerException):
    """
    admin register name required error.
    """
    pass


class AdminNameRequiredError(AdminManagerException):
    """
    admin name required error.
    """
    pass
