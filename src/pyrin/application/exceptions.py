# -*- coding: utf-8 -*-
"""
application exceptions module.
"""

from pyrin.core.exceptions import ContextAttributeError, CoreException


class ApplicationException(CoreException):
    """
    application exception.
    """
    pass


class ComponentAttributeError(ApplicationException, ContextAttributeError):
    """
    component attribute error.
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


class InvalidApplicationStatusError(ApplicationException):
    """
    invalid application status error.
    """
    pass


class ApplicationInScriptingModeError(ApplicationException):
    """
    application in scripting mode error.
    """
    pass


class ApplicationInstanceAlreadySetError(ApplicationException):
    """
    application instance already set error.
    """
    pass


class ApplicationIsNotSubclassedError(ApplicationException):
    """
    application is not subclassed error.
    """
    pass


class InvalidApplicationHookTypeError(ApplicationException):
    """
    invalid application hook type error.
    """
    pass


class OverwritingEndpointIsNotAllowedError(ApplicationException):
    """
    overwriting endpoint is not allowed error.
    """
    pass


class InvalidStaticHostAndHostMatchingError(ApplicationException):
    """
    invalid static host and host matching error.
    """
    pass
