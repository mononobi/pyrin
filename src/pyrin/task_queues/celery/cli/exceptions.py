# -*- coding: utf-8 -*-
"""
celery cli exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class CeleryCLIManagerException(CoreException):
    """
    celery cli manager exception.
    """
    pass


class CeleryCLIManagerBusinessException(CoreBusinessException,
                                        CeleryCLIManagerException):
    """
    celery cli manager business exception.
    """
    pass
