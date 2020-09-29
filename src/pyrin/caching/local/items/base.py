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

    def __init__(self, key, value, *args, **options):
        """
        initializes an instance of LocalCacheItemBase.

        :param object key: hashable object for cache key.
        :param object value: value to be cached.
        """

        super().__init__()

        self._created_on = time.time() * 1000
        self._key = key
        self._value = self._prepare_cache(value)

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

    def _get_cached_value(self, value):
        """
        gets the cached value.

        it is intended to be overridden in subclasses.

        :param object value: value to be returned from cached.

        :rtype: object
        """

        return value

    def _prepare_cache(self, value):
        """
        prepares value to be cached.

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

        return self._get_cached_value(self._value)

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

    this type of cache item supports expire time.
    it also keeps the deep copy of the value into the cache.

    all application complex cache items must be subclassed from this.
    """

    def __init__(self, key, value, expire, **options):
        """
        initializes an instance of ComplexLocalCacheItemBase.

        :param object key: hashable object for cache key.
        :param object value: value to be cached.

        :keyword bool refreshable: specifies that this item's expire time must be
                                   extended on each hit. defaults to False if not
                                   provided.
        """

        super().__init__(key, value, **options)

        self._refreshed_on = self._created_on
        self._expire = expire
        self._refreshable = options.get('refreshable', False)

    def _get_cached_value(self, value):
        """
        gets the cached value.

        :param object value: value to be returned from cached.

        :rtype: object
        """

        if self._refreshable is True and self.is_expired is False:
            self.refresh()

        return deepcopy(value)

    def _prepare_cache(self, value):
        """
        prepares value to be cached.

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
        gets the expire time value of this item in milliseconds.

        :rtype: int
        """

        return self._expire
