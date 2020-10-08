# -*- coding: utf-8 -*-
"""
schema exceptions module.
"""

from pyrin.core.exceptions import CoreException


class SchemaException(CoreException):
    """
    schema exception.
    """
    pass


class SecureBooleanIsRequiredError(SchemaException):
    """
    secure boolean is required error.
    """
    pass


class InvalidStartIndexError(SchemaException):
    """
    invalid start index error.
    """
    pass
