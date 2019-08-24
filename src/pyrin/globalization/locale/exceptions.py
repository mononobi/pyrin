# -*- coding: utf-8 -*-
"""
locale exceptions module.
"""

from pyrin.core.exceptions import CoreException


class LocaleManagerException(CoreException):
    """
    locale manager exception.
    """
    pass


class InvalidLocaleSelectorTypeError(LocaleManagerException):
    """
    invalid locale selector type error.
    """
    pass


class InvalidTimezoneSelectorTypeError(LocaleManagerException):
    """
    invalid timezone selector type error.
    """
    pass


class LocaleSelectorHasBeenAlreadySetError(LocaleManagerException):
    """
    locale selector has been already set error.
    """
    pass


class TimezoneSelectorHasBeenAlreadySetError(LocaleManagerException):
    """
    timezone selector has been already set error.
    """
    pass
