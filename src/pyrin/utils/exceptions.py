# -*- coding: utf-8 -*-
"""
utils exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class UtilsException(CoreException):
    """
    utils exception.
    """
    pass


class UtilsBusinessException(CoreBusinessException, UtilsException):
    """
    utils business exception.
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


class DictKeyPrefixIsNotProvidedError(UtilsException):
    """
    dict key prefix is not provided error.
    """
    pass


class PathIsNotAbsoluteError(UtilsBusinessException):
    """
    path is not absolute error.
    """
    pass


class PathAlreadyExistedError(UtilsBusinessException):
    """
    path already existed error.
    """
    pass


class InvalidPathError(UtilsBusinessException):
    """
    invalid path error.
    """
    pass


class PathNotExistedError(UtilsBusinessException):
    """
    path not existed error.
    """
    pass


class IsNotDirectoryError(UtilsBusinessException):
    """
    is not directory error.
    """
    pass


class IsNotFileError(UtilsBusinessException):
    """
    is not file error.
    """
    pass


class CheckConstraintValuesRequiredError(UtilsException):
    """
    check constraint values required error.
    """
    pass


class MultipleDeclarativeClassesFoundError(UtilsException):
    """
    multiple declarative classes found error.
    """
    pass


class InvalidOrderingColumnError(UtilsBusinessException):
    """
    invalid ordering column error.
    """
    pass
