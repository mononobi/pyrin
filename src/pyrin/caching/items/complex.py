# -*- coding: utf-8 -*-
"""
caching items complex module.
"""

from pyrin.caching.items.base import ComplexCacheItemBase


class ComplexCacheItem(ComplexCacheItemBase):
    """
    complex cache item class.

    this type of cache item supports timeout.
    it also keeps the deep copy of the value into the cache.
    """
    pass
