# -*- coding: utf-8 -*-
"""
PACKAGE_NAME exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class PACKAGE_CLASS_NAMEException(CoreException):
    """
    PACKAGE_NAME exception.
    """
    pass


class PACKAGE_CLASS_NAMEBusinessException(CoreBusinessException, PACKAGE_CLASS_NAMEException):
    """
    PACKAGE_NAME business exception.
    """
    pass
