# -*- coding: utf-8 -*-
"""
model exceptions module.
"""

from pyrin.core.exceptions import CoreException


class DatabaseModelException(CoreException):
    """
    database model exception.
    """
    pass


class SequenceHasNotSetError(DatabaseModelException):
    """
    sequence has not set error.
    """
    pass


class ColumnNotExistedError(DatabaseModelException):
    """
    column not existed error.
    """
    pass
