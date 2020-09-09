# -*- coding: utf-8 -*-
"""
caching local items complex module.
"""

from pyrin.caching.local.items.base import ComplexLocalCacheItemBase


class ComplexLocalCacheItem(ComplexLocalCacheItemBase):
    """
    complex local cache item class.

    this type of cache item supports expire time.
    it also keeps the deep copy of the value into the cache.
    """
    pass
