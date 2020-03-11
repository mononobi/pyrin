# -*- coding: utf-8 -*-
"""
cli core template exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class CLICoreTemplateManagerException(CoreException):
    """
    cli core template manager exception.
    """
    pass


class CLICoreTemplateManagerBusinessException(CoreBusinessException,
                                              CLICoreTemplateManagerException):
    """
    cli core template manager business exception.
    """
    pass


class InvalidProjectRootPathError(CLICoreTemplateManagerException):
    """
    invalid project root path error.
    """
    pass


class InvalidApplicationPackageNameError(CLICoreTemplateManagerException):
    """
    invalid application package name error.
    """
    pass


class InvalidApplicationClassNameError(CLICoreTemplateManagerException):
    """
    invalid application class name error.
    """
    pass


class InvalidProjectStructureTemplateHandlerType(CLICoreTemplateManagerException):
    """
    invalid project structure template handler type.
    """
    pass
