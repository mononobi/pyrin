# -*- coding: utf-8 -*-
"""
caching local handlers complex module.
"""

from threading import Lock

from pyrin.caching.local.containers.dict import OrderedDictContainer
from pyrin.caching.decorators import cache
from pyrin.caching.local.handlers.base import ComplexLocalCacheBase
from pyrin.caching.local.items.complex import ComplexLocalCacheItem


@cache()
class ComplexLocalCache(ComplexLocalCacheBase):
    """
    complex local cache class.

    this type of caches support expire time and count limit for items.
    it does also consider method inputs, current user and component key
    for cache key generation.
    """

    cache_name = 'complex'
    container_class = OrderedDictContainer
    cache_item_class = ComplexLocalCacheItem
    clearance_lock_class = Lock
    persistent_lock_class = Lock
