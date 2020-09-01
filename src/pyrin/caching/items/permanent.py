# -*- coding: utf-8 -*-
"""
caching items permanent module.
"""

from pyrin.caching.items.base import CacheItemBase


class PermanentCacheItem(CacheItemBase):
    """
    permanent cache item class.

    this type of cache item does not support timeout.
    it also keeps the original value into the cache to gain performance.
    """
    pass
