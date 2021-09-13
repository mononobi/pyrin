# -*- coding: utf-8 -*-
"""
validator auto exceptions.
"""

from pyrin.core.exceptions import CoreException


class AutoValidatorException(CoreException):
    """
    auto validator exception.
    """
    pass


class InvalidAutoValidatorHookTypeError(AutoValidatorException):
    """
    invalid auto validator hook type error.
    """
    pass
