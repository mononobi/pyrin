# -*- coding: utf-8 -*-
"""
caching handlers exceptions module.
"""

from pyrin.core.exceptions import CoreException


class CachingHandlersException(CoreException):
    """
    caching handlers exception.
    """
    pass


class CacheNameIsRequiredError(CachingHandlersException):
    """
    cache name is required error.
    """
    pass


class InvalidCachingContainerTypeError(CachingHandlersException):
    """
    invalid caching container type error.
    """
    pass


class InvalidCacheItemTypeError(CachingHandlersException):
    """
    invalid cache item type error.
    """
    pass


class CacheClearanceLockTypeIsRequiredError(CachingHandlersException):
    """
    cache clearance lock type is required error.
    """
    pass


class InvalidCacheLimitError(CachingHandlersException):
    """
    invalid cache limit error.
    """
    pass


class InvalidCacheTimeoutError(CachingHandlersException):
    """
    invalid cache timeout error.
    """
    pass


class InvalidCacheClearCountError(CachingHandlersException):
    """
    invalid cache clear count error.
    """
    pass
