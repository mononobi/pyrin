# -*- coding: utf-8 -*-
"""
caching handlers permanent module.
"""

from pyrin.caching.containers.local import LocalContainer
from pyrin.caching.decorators import cache
from pyrin.caching.items.permanent import PermanentCacheItem
from pyrin.caching.handlers.base import CachingHandlerBase, ExtendedCachingHandlerBase


@cache()
class PermanentCachingHandler(CachingHandlerBase):
    """
    permanent caching handler class.

    this type of caching handlers cache items permanently and they won't be expired.
    it does not consider method inputs, current user and component key for cache
    key generation.
    """

    cache_name = 'permanent'
    container_class = LocalContainer
    cache_item_class = PermanentCacheItem


@cache()
class ExtendedPermanentCachingHandler(ExtendedCachingHandlerBase):
    """
    extended permanent caching handler class.

    this type of caching handlers cache items permanently and they won't be expired.
    it does consider method inputs, current user and component key for cache key generation.
    """

    cache_name = 'extended.permanent'
    container_class = LocalContainer
    cache_item_class = PermanentCacheItem
