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


class CheckConstraintConflictError(ORMSQLSchemaException):
    """
    check constraint conflict error.
    """
    pass


class InvalidCheckConstraintError(ORMSQLSchemaException):
    """
    invalid check constraint error.
    """
    pass


class StringColumnTypeIsInvalidError(ORMSQLSchemaException):
    """
    string column type is invalid error.
    """
    pass


class TextColumnTypeIsInvalidError(ORMSQLSchemaException):
    """
    text column type is invalid error.
    """
    pass
