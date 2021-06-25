# -*- coding: utf-8 -*-
"""
filtering exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class FilteringException(CoreException):
    """
    filtering exception.
    """
    pass


class FilteringBusinessException(CoreBusinessException, FilteringException):
    """
    filtering business exception.
    """
    pass
