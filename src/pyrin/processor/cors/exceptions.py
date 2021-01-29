# -*- coding: utf-8 -*-
"""
cors exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class CORSException(CoreException):
    """
    cors exception.
    """
    pass


class CORSBusinessException(CoreBusinessException,
                            CORSException):
    """
    cors business exception.
    """
    pass


class CORSAllowedHeadersModificationError(CORSException):
    """
    cors allowed headers modification error.
    """
    pass
