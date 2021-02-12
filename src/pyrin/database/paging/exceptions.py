# -*- coding: utf-8 -*-
"""
database paging exceptions module.
"""

from pyrin.core.exceptions import CoreException


class DatabasePagingException(CoreException):
    """
    database paging exception.
    """
    pass


class DatabasePagingBusinessException(DatabasePagingException):
    """
    database paging business exception.
    """
    pass


class PageSizeLimitError(DatabasePagingException):
    """
    page size limit error.
    """
    pass


class TotalCountIsAlreadySetError(DatabasePagingException):
    """
    total count is already set error.
    """
    pass
