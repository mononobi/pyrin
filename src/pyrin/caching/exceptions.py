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


class InvalidCacheTypeError(CachingManagerException):
    """
    invalid cache type error.
    """
    pass


class DuplicatedCacheError(CachingManagerException):
    """
    duplicated cache error.
    """
    pass


class CacheNotFoundError(CachingManagerException):
    """
    cache not found error.
    """
    pass


class CacheIsNotPersistentError(CachingManagerException):
    """
    cache is not persistent error.
    """
    pass


class CacheNameIsRequiredError(CachingManagerException):
    """
    cache name is required error.
    """
    pass


class InvalidCacheLimitError(CachingManagerException):
    """
    invalid cache limit error.
    """
    pass


class InvalidCacheExpireTimeError(CachingManagerException):
    """
    invalid cache expire time error.
    """
    pass
