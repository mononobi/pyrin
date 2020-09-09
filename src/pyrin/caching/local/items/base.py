# -*- coding: utf-8 -*-
"""
caching local items base module.
"""

from copy import deepcopy

import time

from pyrin.core.structs import CoreObject


class LocalCacheItemBase(CoreObject):
    """
    local cache item base class.

    this type of cache item does not support expire time.
    it also keeps the original value into the cache to gain performance.

    all application cache items must be subclassed from this.
    """

    def __init__(self, key, value, *args, **kwargs):
        """
        initializes an instance of LocalCacheItemBase.
        """

        super().__init__()

        self._created_on = time.time() * 1000
        self._key = key
        self._value = self._get_cacheable_value(value)

    def __str__(self):
        """
        gets the string representation of this cache item.

        :rtype: str
        """
        return 'CacheItem: [{key}-{value}]'.format(key=self._key, value=self._value)

    def __repr__(self):
        """
        gets the string representation of this cache item.

        :rtype: str
        """

        return str(self)

    def __hash__(self):
        """
        gets the hash of this cache item.

        :rtype: int
        """

        return hash(self._key)

    def _get_cacheable_value(self, value):
        """
        gets cacheable version of value.

        it is intended to be overridden in subclasses.

        :param object value: value to be cached.

        :rtype: object
        """

        return value

    @property
    def value(self):
        """
        gets the cached value of this item.

        :rtype: object
        """

        return self._get_cacheable_value(self._value)

    @property
    def key(self):
        """
        gets the key of this item.

        :rtype: object
        """

        return self._key


class ComplexLocalCacheItemBase(LocalCacheItemBase):
    """
    complex local cache item base class.

    this type of cache item supports expire.
    it also keeps the deep copy of the value into the cache.

    all application complex cache items must be subclassed from this.
    """

    def __init__(self, key, value, expire, **kwargs):
        """
        initializes an instance of ComplexLocalCacheItemBase.
        """

        super().__init__(key, value, **kwargs)

        self._refreshed_on = self._created_on
        self._expire = expire

    def _get_cacheable_value(self, value):
        """
        gets cacheable version of value.

        it is intended to be overridden in subclasses.

        :param object value: value to be cached.

        :rtype: object
        """

        return deepcopy(value)

    def refresh(self):
        """
        refreshes the current item to extend its expire time.
        """

        self._refreshed_on = time.time() * 1000

    @property
    def is_expired(self):
        """
        gets a value indicating that this item has been expired.

        :rtype: bool
        """

        return time.time() * 1000 - self._refreshed_on > self._expire

    @property
    def expire(self):
        """
        gets the expire time value of this item.
        """

        return self._expire
