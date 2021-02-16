# -*- coding: utf-8 -*-
"""
orm session exceptions module.
"""

from pyrin.core.exceptions import CoreException


class ORMSessionException(CoreException):
    """
    orm session exception.
    """
    pass


class TransientSQLExpressionRequiredError(ORMSessionException):
    """
    transient sql expression required error.
    """
    pass
