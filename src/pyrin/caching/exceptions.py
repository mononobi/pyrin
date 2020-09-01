# -*- coding: utf-8 -*-
"""
caching exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class CachingManagerException(CoreException):
    """
    caching manager exception.
    """
    pass


class CachingManagerBusinessException(CoreBusinessException, CachingManagerException):
    """
    caching manager business exception.
    """
    pass


class KeyIsNotPresentInCacheError(CachingManagerException):
    """
    key is not present in cache error.
    """
    pass


class InvalidCachingHandlerTypeError(CachingManagerException):
    """
    invalid caching handler type error.
    """
    pass


class DuplicatedCachingHandlerError(CachingManagerException):
    """
    duplicated caching handler error.
    """
    pass


class CachingHandlerNotFoundError(CachingManagerException):
    """
    caching handler not found error.
    """
    pass
