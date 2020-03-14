# -*- coding: utf-8 -*-
"""
schema exceptions module.
"""

from pyrin.core.exceptions import CoreException
from pyrin.utils.exceptions import ColumnNotExistedError as BaseColumnNotExistedError


class SchemaException(CoreException):
    """
    schema exception.
    """
    pass


class SchemaColumnsOrReplaceIsRequiredError(SchemaException):
    """
    schema columns or replace is required error.
    """
    pass


class ColumnNotExistedError(BaseColumnNotExistedError, SchemaException):
    """
    column not existed error.
    """
    pass


class InvalidReplaceKeysError(SchemaException):
    """
    invalid replace keys error.
    """
    pass
