# -*- coding: utf-8 -*-
"""
api exceptions module.
"""

from pyrin.core.exceptions import CoreException


class APIManagerException(CoreException):
    """
    api manager exception.
    """
    pass


class InvalidAPIHookTypeError(APIManagerException):
    """
    invalid api hook type error.
    """
    pass
