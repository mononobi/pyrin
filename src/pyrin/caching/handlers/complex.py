# -*- coding: utf-8 -*-
"""
caching handlers complex module.
"""

from threading import Lock

from pyrin.caching.containers.local import LocalContainer
from pyrin.caching.decorators import cache
from pyrin.caching.handlers.base import ComplexCachingHandlerBase
from pyrin.caching.items.complex import ComplexCacheItem


@cache()
class ComplexCachingHandler(ComplexCachingHandlerBase):
    """
    complex caching handler class.

    this type of caching handlers support expire time and count limit for items.
    it does also consider method inputs, current user and component key for cache
    key generation.
    """

    cache_name = 'complex'
    container_class = LocalContainer
    cache_item_class = ComplexCacheItem
    clearance_lock_class = Lock
