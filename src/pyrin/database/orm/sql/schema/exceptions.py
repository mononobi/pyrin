# -*- coding: utf-8 -*-
"""
orm sql schema exceptions module.
"""

from pyrin.core.exceptions import CoreException


class ORMSQLSchemaException(CoreException):
    """
    orm sql schema exception.
    """
    pass


class SequenceColumnTypeIsInvalidError(ORMSQLSchemaException):
    """
    sequence column type is invalid error.
    """
    pass
