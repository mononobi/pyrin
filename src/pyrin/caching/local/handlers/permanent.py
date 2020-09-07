# -*- coding: utf-8 -*-
"""
caching local handlers permanent module.
"""

from pyrin.caching.local.containers.dict import OrderedDictContainer
from pyrin.caching.decorators import cache
from pyrin.caching.local.items.permanent import PermanentLocalCacheItem
from pyrin.caching.local.handlers.base import LocalCacheBase, ExtendedLocalCacheBase


@cache()
class PermanentLocalCache(LocalCacheBase):
    """
    permanent local cache class.

    this type of caches cache items permanently and they won't be expired.
    it does not consider method inputs, current user and component key for cache
    key generation.
    """

    cache_name = 'permanent'
    container_class = OrderedDictContainer
    cache_item_class = PermanentLocalCacheItem


@cache()
class ExtendedPermanentLocalCache(ExtendedLocalCacheBase):
    """
    extended permanent local cache class.

    this type of caches cache items permanently and they won't be expired.
    it does consider method inputs, current user and component key for cache key generation.
    """

    cache_name = 'extended.permanent'
    container_class = OrderedDictContainer
    cache_item_class = PermanentLocalCacheItem
