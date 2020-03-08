# -*- coding: utf-8 -*-
"""
template exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class TemplateManagerException(CoreException):
    """
    template manager exception.
    """
    pass


class TemplateManagerBusinessException(CoreBusinessException, TemplateManagerException):
    """
    template manager business exception.
    """
    pass


class TemplateHandlerNameRequiredError(TemplateManagerException):
    """
    template handler name required error.
    """
    pass


class InvalidSourceDirectoryError(TemplateManagerException):
    """
    invalid source directory error.
    """
    pass


class InvalidTargetDirectoryError(TemplateManagerException):
    """
    invalid target directory error.
    """
    pass


class InvalidTemplateHandlerTypeError(TemplateManagerException):
    """
    invalid template handler type error.
    """
    pass


class DuplicatedTemplateHandlerError(TemplateManagerException):
    """
    duplicated template handler error.
    """
    pass


class TemplateHandlerNotFoundError(TemplateManagerBusinessException):
    """
    template handler not found error.
    """
    pass


class TemplateTargetDirectoryAlreadyExistedError(TemplateManagerException):
    """
    template target directory already existed error.
    """
    pass
