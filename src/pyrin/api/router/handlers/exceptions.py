# -*- coding: utf-8 -*-
"""
router handlers exceptions module.
"""

from pyrin.core.exceptions import CoreTypeError, CoreValueError


class InvalidViewFunctionTypeError(CoreTypeError):
    """
    invalid view function type error.
    """
    pass


class MaxContentLengthShouldNotBeGreaterThanGlobalLimitError(CoreValueError):
    """
    max content length should not be greater than global limit error.
    """
    pass
