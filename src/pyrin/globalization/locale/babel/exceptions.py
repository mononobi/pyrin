# -*- coding: utf-8 -*-
"""
babel exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class BabelHandlersException(CoreException):
    """
    babel handlers exception.
    """
    pass


class BabelHandlersBusinessException(CoreBusinessException, BabelHandlersException):
    """
    babel handlers business exception.
    """
    pass


class LocaleAlreadyExistedError(BabelHandlersBusinessException):
    """
    locale already existed error.
    """
    pass
