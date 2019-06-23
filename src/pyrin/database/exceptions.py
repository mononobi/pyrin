# -*- coding: utf-8 -*-
"""
database exceptions module.
"""

from pyrin.core.exceptions import CoreException


class DatabaseManagerException(CoreException):
    """
    database manager exception.
    """
    pass


class DatabaseOperationError(DatabaseManagerException):
    """
    database operation error.
    """
    pass
