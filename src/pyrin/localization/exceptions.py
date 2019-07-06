# -*- coding: utf-8 -*-
"""
localization exceptions module.
"""

from pyrin.core.exceptions import CoreException


class LocalizationManagerException(CoreException):
    """
    localization manager exception.
    """
    pass


class InvalidLocaleSelectorTypeError(LocalizationManagerException):
    """
    invalid locale selector type error.
    """
    pass


class InvalidTimezoneSelectorTypeError(LocalizationManagerException):
    """
    invalid timezone selector type error.
    """
    pass


class LocaleSelectorHasBeenAlreadySetError(LocalizationManagerException):
    """
    locale selector has been already set error.
    """
    pass


class TimezoneSelectorHasBeenAlreadySetError(LocalizationManagerException):
    """
    timezone selector has been already set error.
    """
    pass
