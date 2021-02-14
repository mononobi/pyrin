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


class SequencePKColumnTypeIsInvalidError(ORMSQLSchemaException):
    """
    sequence pk column type is invalid error.
    """
    pass


class AutoPKColumnTypeIsInvalidError(ORMSQLSchemaException):
    """
    auto pk column type is invalid error.
    """
    pass


class InvalidFKColumnReferenceTypeError(ORMSQLSchemaException):
    """
    invalid fk column reference type error.
    """
    pass
