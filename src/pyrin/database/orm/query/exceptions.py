# -*- coding: utf-8 -*-
"""
database orm query exceptions module.
"""

from pyrin.core.exceptions import CoreException


class DatabaseORMQueryException(CoreException):
    """
    database orm query exception.
    """
    pass


class DatabaseORMQueryBusinessException(DatabaseORMQueryException):
    """
    database orm query business exception.
    """
    pass


class DataCouldNotBeFetchedError(DatabaseORMQueryBusinessException):
    """
    data could not be fetched error.
    """
    pass
