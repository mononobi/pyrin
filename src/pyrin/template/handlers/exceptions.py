# -*- coding: utf-8 -*-
"""
template handlers exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class TemplateHandlersException(CoreException):
    """
    template handlers exception.
    """
    pass


class TemplateHandlersBusinessException(CoreBusinessException, TemplateHandlersException):
    """
    template handlers business exception.
    """
    pass


class InvalidPackagePathError(TemplateHandlersBusinessException):
    """
    invalid package path error.
    """
    pass


class InvalidPackageClassNameError(TemplateHandlersBusinessException):
    """
    invalid package class name error.
    """
    pass
