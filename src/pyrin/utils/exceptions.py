# -*- coding: utf-8 -*-
"""
utils exceptions module.
"""

from pyrin.core.exceptions import CoreException


class UtilsException(CoreException):
    """
    utils exception.
    """
    pass


class InputNotCallableError(UtilsException):
    """
    input not callable error.
    """
    pass


class ConfigurationFileNotFoundError(UtilsException):
    """
    configuration file not found error.
    """
    pass


class InvalidSchemaNameError(UtilsException):
    """
    invalid schema name error.
    """
    pass


class InvalidTableNameError(UtilsException):
    """
    invalid table name error.
    """
    pass


class InvalidColumnNameError(UtilsException):
    """
    invalid column name error.
    """
    pass


class InvalidRowResultFieldsAndValuesError(UtilsException):
    """
    invalid row result fields and values error.
    """
    pass


class FieldsAndValuesCountMismatchError(UtilsException):
    """
    fields and values count mismatch error.
    """
    pass