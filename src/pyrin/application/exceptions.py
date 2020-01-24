# -*- coding: utf-8 -*-
"""
application exceptions module.
"""

from pyrin.core.exceptions import ContextAttributeError, CoreException


class ComponentAttributeError(ContextAttributeError):
    """
    component attribute error.
    """
    pass


class ApplicationException(CoreException):
    """
    application exception.
    """
    pass


class InvalidComponentTypeError(ApplicationException):
    """
    invalid component type error.
    """
    pass


class InvalidComponentIDError(ApplicationException):
    """
    invalid component id error.
    """
    pass


class InvalidComponentNameError(ApplicationException):
    """
    invalid component name error.
    """
    pass


class DuplicateComponentIDError(ApplicationException):
    """
    duplicate component id error.
    """
    pass


class DuplicateContextKeyError(ApplicationException):
    """
    duplicate context key error.
    """
    pass


class DuplicateRouteURLError(ApplicationException):
    """
    duplicate route url error.
    """
    pass


class InvalidRouteFactoryTypeError(ApplicationException):
    """
    invalid route factory type error.
    """
    pass


class ApplicationSettingsPathNotExistedError(ApplicationException):
    """
    application settings path not existed error.
    """
    pass


class InvalidApplicationStatusError(ApplicationException):
    """
    invalid application status error.
    """
    pass


class InvalidApplicationHookTypeError(ApplicationException):
    """
    invalid application hook type error.
    """
    pass


class ApplicationInMigrationModeError(ApplicationException):
    """
    application in migration mode error.
    """
    pass
