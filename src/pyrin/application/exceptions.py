# -*- coding: utf-8 -*-
"""
application exceptions module.
"""

from pyrin.core.exceptions import CoreTypeError, CoreValueError, CoreKeyError, \
    CoreNotADirectoryError, ContextAttributeError, CoreException


class ComponentAttributeError(ContextAttributeError):
    """
    component attribute error.
    """
    pass


class InvalidComponentTypeError(CoreTypeError):
    """
    invalid component type error.
    """
    pass


class InvalidComponentIDError(CoreValueError):
    """
    invalid component id error.
    """
    pass


class InvalidComponentNameError(CoreException):
    """
    invalid component name error.
    """
    pass


class DuplicateComponentIDError(CoreKeyError):
    """
    duplicate component id error.
    """
    pass


class DuplicateContextKeyError(CoreKeyError):
    """
    duplicate context key error.
    """
    pass


class DuplicateRouteURLError(CoreKeyError):
    """
    duplicate route url error.
    """
    pass


class InvalidRouteFactoryTypeError(CoreTypeError):
    """
    invalid route factory type error.
    """
    pass


class ApplicationSettingsPathNotExistedError(CoreNotADirectoryError):
    """
    application settings path not existed error.
    """
    pass


class InvalidApplicationStatusError(CoreValueError):
    """
    invalid application status error.
    """
    pass
