# -*- coding: utf-8 -*-
"""
cli core exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class CLICoreManagerException(CoreException):
    """
    cli core manager exception.
    """
    pass


class CLICoreManagerBusinessException(CoreBusinessException, CLICoreManagerException):
    """
    cli core manager business exception.
    """
    pass


class CLICoreTemplateHandlerNotFoundError(CLICoreManagerBusinessException):
    """
    cli core template handler not found error.
    """
    pass
