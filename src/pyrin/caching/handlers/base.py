# -*- coding: utf-8 -*-
"""
caching handlers base module.
"""

import time

from multiprocessing import Lock
from copy import deepcopy

import pyrin.configuration.services as config_services

from pyrin.core.context import CoreObject, DTO
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.core.globals import NULL
from pyrin.utils.singleton import MultiSingletonMeta


class CacheItem(CoreObject):
    """
    cache item class.
    """

    def __init__(self, key, value, timeout):
        """
        initializes an instance of CacheItem.

        :param object key: hashable key for this cache item.
        :param value: value of the hash item.
        :param int timeout: timeout for this cache item before
                            invalidation in milliseconds.
        """

        super().__init__()

        self.key = key
        self.value = deepcopy(value)
        self.create_time = time.time()
        self.hit_count = 0
        self.miss_count = 0
        self.timeout = timeout

    def __str__(self):
        return 'CacheItem: [{key}-{value}]'.format(key=self.key, value=self.value)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.key)

    def is_expired(self):
        """
        gets a value indicating that this cache item is expired.

        :rtype: bool
        """

        return (time.time() * 1000) - self.timeout > self.create_time * 1000


class CachingHandlerSingletonMeta(MultiSingletonMeta):
    """
    caching handler singleton meta class.
    this is a thread-safe implementation of singleton.
    """

    # a dictionary containing an instance of each type.
    # in the form of: {type: instance}
    _instances = dict()
    _lock = Lock()


class CachingHandlerBase(CoreObject, metaclass=CachingHandlerSingletonMeta):
    """
    caching handler base class.
    """

    def __init__(self, name, **options):
        """
        initializes an instance of CachingHandlerBase.

        :param str name: caching handler name.
                         this name will be used to get handlers.

        :keyword int timeout: timeout for items of this caching handler
                              before invalidation in milliseconds.
                              defaults to `caching.config` file `default_timeout`
                              value if not provided.
        """

        super().__init__()

        self._set_name(name)
        self._timeout = options.get('timeout', config_services.get('caching',
                                                                   'general',
                                                                   'default_timeout'))

    def __setitem__(self, key, value):
        return self.set(key, value)

    def __getitem__(self, key):
        return self.get(key)

    def __contains__(self, key):
        return self.contains(key)

    def set(self, key, value, timeout=None):
        """
        sets a new value into cached items.

        :param object key: hashable key of the cache to be registered.
        :param object value: value to be cached.

        :param int timeout: timeout for this value. defaults
                            to value from `caching.config`
                            if not provided.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    def get(self, key):
        """
        gets the value from cache.

        :param object key: key to get its value from cache.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: object
        """

        raise CoreNotImplementedError()

    def contains(self, key):
        """
        gets a value indicating that given key is existed in the cached items.

        :param object key: key to be checked for existence.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    def get_timeout(self):
        """
        gets timeout value for this handler items in milliseconds.

        :rtype: int
        """

        return self._timeout

    def remove(self, key):
        """
        removes the key from cached items.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()


class DictCachingHandlerBase(CachingHandlerBase):
    """
    dict caching handler base class.
    """

    def __init__(self, name, **options):
        """
        initializes an instance of DictCachingHandlerBase.

        :param str name: caching handler name.
                         this name will be used to get handlers.

        :keyword int max_length: max length of this caching handler.
                                 it means how many elements this handler
                                 could cache before it starts to remove old items.
                                 defaults to `caching.config` file `default_max_length`
                                 value if not provided.

        :keyword int timeout: timeout for items of this caching handler
                              before invalidation in milliseconds.
                              defaults to `caching.config` file `default_timeout`
                              value if not provided.
        """

        super().__init__(name, **options)

        self._max_length = options.get('max_length', config_services.get('caching',
                                                                         'general',
                                                                         'default_max_length'))
        self._items = DTO()
        self._cache_lock = Lock()

    def __len__(self):
        return self.get_current_length()

    def get_max_length(self):
        """
        gets the max length of this caching handler.

        :rtype: int
        """

        return self._max_length

    def get_current_length(self):
        """
        gets the length of current items available in this caching handler.

        :rtype: int
        """

        return len(self._items)

    def clear(self):
        """
        removes all cached items.
        """

        self._items.clear()

    def set(self, key, value, timeout=None):
        """
        sets a new value into cached items.

        :param object key: hashable key of the cache to be registered.
        :param object value: value to be cached.

        :param int timeout: timeout for this value. defaults
                            to value from `caching.config`
                            if not provided.
        """

        item = CacheItem(key, value, timeout or self.get_timeout())
        try:
            self._cache_lock.acquire()
            self._set(item)
        finally:
            self._cache_lock.release()

    def _set(self, item):
        """
        puts the given item into cache.

        :param CacheItem item: item to be cached.
        """

        if self.get_current_length() > self.get_max_length():
            pass

        self._items[item.key] = item

    def get(self, key):
        """
        gets the value from cache.
        if the key does not existed, it returns `NULL` object.

        :param object key: key to get its value from cache.

        :rtype: object
        """

        item = self._items.get(key, NULL)
        if item is not NULL:
            self.remove(key)
            if item.is_expired():
                return NULL
            self._set(item)
            return item.value

        return item

    def contains(self, key):
        """
        gets a value indicating that given key is existed in the cached items.

        :param object key: key to be checked for existence.

        :rtype: bool
        """

        return key in self._items

    def remove(self, key):
        """
        removes the key from cached items.

        :param object key: key to get its value from cache.
        """

        del self._items[key]
