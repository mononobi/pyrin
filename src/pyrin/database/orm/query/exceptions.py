# -*- coding: utf-8 -*-
"""
orm query exceptions module.
"""

from pyrin.core.exceptions import CoreException


class ORMQueryException(CoreException):
    """
    orm query exception.
    """
    pass


class ORMQueryBusinessException(ORMQueryException):
    """
    orm query business exception.
    """
    pass


class ColumnsOutOfScopeError(ORMQueryBusinessException):
    """
    columns out of scope error.
    """
    pass


class UnsupportedQueryStyleError(ORMQueryException):
    """
    unsupported query style error.
    """
    pass


class InjectTotalCountError(ORMQueryException):
    """
    inject total count error.
    """
    pass
