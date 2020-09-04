# -*- coding: utf-8 -*-
"""
caching interface module.
"""

from abc import abstractmethod

from pyrin.caching.exceptions import KeyIsNotPresentInCacheError
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.core.structs import CoreObject


class AbstractCachingHandler(CoreObject):
    """
    abstract caching handler class.

    all application caching handlers must be subclassed from this.

    this type of caching handlers does not consider method inputs, current
    user and component key in key generation. it only considers the class type
    of function and function name itself. this is useful for caching items
    that never change after application startup and are independent
    from different scoped or global variables.

    it also does not support timeout and size limit for cached values.
    its values are permanent unless manually removed if required.

    it also keeps the real value in the cache, not a deep copy of it to gain
    performance.

    it also does not provide statistic info about hit or missed
    caches, to gain performance.
    """

    def __setitem__(self, key, value):
        """
        sets the given key with given value into this caching handler.

        :param object key: key to set value with it.
        :param object value: value to be cached.
        """

        return self.set(key, value)

    def __getitem__(self, key):
        """
        gets the value of given key.

        it raises an error if key does not exist.

        :param object key: key to get its value.

        :raises KeyIsNotPresentInCacheError: key is not present in cache error.

        :returns: object
        """

        result = self.get(key, default=KeyIsNotPresentInCacheError)
        if result is KeyIsNotPresentInCacheError:
            raise KeyIsNotPresentInCacheError('Key [{key}] is not present in '
                                              'the cache.'.format(key=key))

        return result

    def __contains__(self, key):
        """
        gets a value indicating that given key exists in cache.

        :param object key: key to be checked for existence.

        :rtype: bool
        """

        return self.contains(key)

    def __len__(self):
        """
        gets the count of items of this handler.

        :rtype: int
        """

        return self.count

    @abstractmethod
    def set(self, key, value, *args, **options):
        """
        sets a new value into cached items.

        :param object key: hashable key of the cache to be registered.
        :param object value: value to be cached.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def get(self, key, default=None, **options):
        """
        gets the value from cache.

        if key does not exist, it returns None or the specified default value.

        :param object key: hashable key to get its value from cache.
        :param object default: value to be returned if key is not present.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: object
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def try_set(self, value, *keys, **options):
        """
        sets a new value into cached items.

        this method will generate cache key from given type and function.
        if the provided values are not hashable, this method won't raise
        an error and logs it silently.

        :param object value: value to be cached.
        :param object keys: value to be used for key generation.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def try_get(self, *keys, default=None, **options):
        """
        gets the value from cache.

        this method will generate cache key from given type and function.
        if key does not exist, it returns None or the specified default value.
        if the provided values are not hashable, this method won't raise
        an error and logs it silently.

        :param object keys: value to be used for key generation.
        :param object default: value to be returned if key is not present.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: object
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def contains(self, key):
        """
        gets a value indicating that given key is existed in the cached items.

        :param object key: key to be checked for existence.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def pop(self, key, default=None):
        """
        pops the given key from cache and returns its value.

        if key does not exist, it returns None or the specified default value.

        :param object key: key to get its value.
        :param object default: value to be returned if key is not present.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: object
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def remove(self, key):
        """
        removes the given key from cache.

        it does nothing if the key is not present in the cache.

        :param object key: key to be removed.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def clear(self):
        """
        clears all items from cache.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def items(self):
        """
        gets an iterable of all keys and their values in the cache.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: iterable[tuple[object, object]]
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def keys(self):
        """
        gets all keys of current cache.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: iterable[object]
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def values(self):
        """
        gets all values of current cache.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: iterable[object]
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def generate_key(self, *keys, **options):
        """
        generates a cache key from given inputs.

        :param object keys: value to be used for key generation.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: hash of generated key.
        :rtype: int
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def persist(self, version, **options):
        """
        saves cached items of this handler into database.

        :param str version: version to be saved with cached items in database.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def load(self, version, **options):
        """
        loads cached items of this handler from database.

        :param str version: version of cached items to be loaded from database.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def count(self):
        """
        gets the count of items of this handler.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: int
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def last_cleared_time(self):
        """
        gets the last time in which this handler has been cleared.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: datetime.datetime
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def stats(self):
        """
        get the statistic info about cached items.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: dict
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def persistent(self):
        """
        gets a value indicating that cached items must be persisted to database on shutdown.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def chunk_size(self):
        """
        gets the chunk size for this handler.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: int
        """

        raise CoreNotImplementedError()


class AbstractExtendedCachingHandler(AbstractCachingHandler):
    """
    abstract extended caching handler class.

    all application extended caching handlers must be subclassed from this.

    this type of caching handlers are same as `AbstractCachingHandler` type
    but it also considers method inputs, current user and component key.
    """

    @property
    @abstractmethod
    def consider_user(self):
        """
        gets the consider user value for this handler.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()


class AbstractComplexCachingHandler(AbstractExtendedCachingHandler):
    """
    abstract complex caching handler class.

    all application complex caching handlers must be subclassed from this.

    this type of caching handlers will also consider method inputs, current user
    and component key in key generation. this is useful for caching items that
    change during application runtime based on different inputs and variables.

    it also supports timeout and size limit for cached items.
    it also keeps a deep copy of the value in the cache.
    it also provides statistic info about hit or missed caches.
    it also supports persistent mode to save cached values into
    database on application shutdown and load them back on next startup.
    """

    @property
    @abstractmethod
    def is_full(self):
        """
        gets a value indicating the cache is full.

        it returns a tuple, first item is a boolean indicating the fullness of cache.
        the second item is the number of excess items in the cache.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: tuple[bool, int]
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def timeout(self):
        """
        gets default timeout value for this handler's items in milliseconds.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: int
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def limit(self):
        """
        gets the count limit of this handler.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: int
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def hit_count(self):
        """
        gets the hit count for this handler.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: int
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def miss_count(self):
        """
        gets the miss count for this handler.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: int
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def use_lifo(self):
        """
        gets the use lifo for this handler.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def clear_count(self):
        """
        gets the clear count for this handler.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: int
        """

        raise CoreNotImplementedError()
