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


class EntitiesAreNotCollectedError(DatabaseModelException):
    """
    entities are not collected error.
    """
    pass


class InvalidModelHookTypeError(DatabaseModelException):
    """
    invalid model hook type error.
    """
    pass


class InvalidOrderingColumnTypeError(DatabaseModelException):
    """
    invalid ordering column type error.
    """
    pass
