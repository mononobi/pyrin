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


class ColumnNotExistedError(DatabaseModelException):
    """
    column not existed error.
    """
    pass


class InvalidDeclarativeBaseTypeError(DatabaseModelException):
    """
    invalid declarative base type error.
    """
    pass


class InvalidDepthProvidedError(DatabaseModelException):
    """
    invalid depth provided error.
    """
    pass
