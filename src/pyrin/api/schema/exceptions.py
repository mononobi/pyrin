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


class SchemaAttributesRequiredError(SchemaException):
    """
    schema attributes required error.
    """
    pass
