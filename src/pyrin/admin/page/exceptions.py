# -*- coding: utf-8 -*-
"""
admin page exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class AdminPageException(CoreException):
    """
    admin page exception.
    """
    pass


class AdminPageBusinessException(CoreBusinessException,
                                 AdminPageException):
    """
    admin page business exception.
    """
    pass


class InvalidListFieldError(AdminPageException):
    """
    invalid list field error.
    """
    pass


class ListFieldRequiredError(AdminPageException):
    """
    list field required error.
    """
    pass


class InvalidMethodNameError(AdminPageException):
    """
    invalid method name error.
    """
    pass


class InvalidAdminEntityTypeError(AdminPageException):
    """
    invalid admin entity type error.
    """
    pass


class AdminRegisterNameRequiredError(AdminPageException):
    """
    admin register name required error.
    """
    pass


class AdminNameRequiredError(AdminPageException):
    """
    admin name required error.
    """
    pass
