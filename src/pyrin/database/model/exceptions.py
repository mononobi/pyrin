# -*- coding: utf-8 -*-
"""
model exceptions module.
"""

from pyrin.core.exceptions import CoreException
from pyrin.utils.exceptions import ColumnNotExistedError as BaseColumnNotExistedError


class DatabaseModelException(CoreException):
    """
    database model exception.
    """
    pass


class ColumnNotExistedError(BaseColumnNotExistedError, DatabaseModelException):
    """
    column not existed error.
    """
    pass


class InvalidDeclarativeBaseTypeError(DatabaseModelException):
    """
    invalid declarative base type error.
    """
    pass
