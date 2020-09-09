# -*- coding: utf-8 -*-
"""
caching local items permanent module.
"""

from pyrin.caching.local.items.base import LocalCacheItemBase


class PermanentLocalCacheItem(LocalCacheItemBase):
    """
    permanent local cache item class.

    this type of cache item does not support expire time.
    it also keeps the original value into the cache to gain performance.
    """
    pass
