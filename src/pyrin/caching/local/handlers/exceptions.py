# -*- coding: utf-8 -*-
"""
caching local handlers exceptions module.
"""

from pyrin.core.exceptions import CoreException


class CachingLocalHandlersException(CoreException):
    """
    caching local handlers exception.
    """
    pass


class InvalidCacheContainerTypeError(CachingLocalHandlersException):
    """
    invalid cache container type error.
    """
    pass


class InvalidCacheItemTypeError(CachingLocalHandlersException):
    """
    invalid cache item type error.
    """
    pass


class CacheClearanceLockTypeIsRequiredError(CachingLocalHandlersException):
    """
    cache clearance lock type is required error.
    """
    pass


class InvalidCacheClearCountError(CachingLocalHandlersException):
    """
    invalid cache clear count error.
    """
    pass


class InvalidChunkSizeError(CachingLocalHandlersException):
    """
    invalid chunk size error.
    """
    pass


class CachePersistentLockTypeIsRequiredError(CachingLocalHandlersException):
    """
    cache persistent lock type is required error.
    """
    pass


class CacheVersionIsRequiredError(CachingLocalHandlersException):
    """
    cache version is required error.
    """
    pass
