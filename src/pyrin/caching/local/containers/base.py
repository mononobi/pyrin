# -*- coding: utf-8 -*-
"""
caching local containers base module.
"""

from abc import abstractmethod

from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.core.structs import CoreObject


class LocalCacheContainerBase(CoreObject):
    """
    local cache container base class.

    it has a similar interface to a normal dict except it has an extra `set` method.
    all application local cache containers must be subclassed from this.
    """

    @abstractmethod
    def __call__(self, *args, **kwargs):
        """
        implements call on this class type.

        in the form of `LocalCacheContainerBase()`.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def __setitem__(self, key, value):
        """
        sets the given key with given value into the cache.

        :param object key: key to set value with it.
        :param object value: value to be cached.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def __getitem__(self, key):
        """
        gets the value of given key.

        in the form of `self[key]`.
        it raises an error if the key does not exist.

        :param object key: key to get its value.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: object
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def __delitem__(self, key):
        """
        deletes the given key from cache.

        in the form of `del self[key]`.
        it raises an error if the key does not exist.

        :param object key: key to be deleted.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def __iter__(self, *args, **kwargs):
        """
        iterates over current cached items.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: iterator
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def __contains__(self, key):
        """
        gets a value indicating that given key exists in cache.

        :param object key: key to be checked for existence.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def __len__(self):
        """
        gets the count of items of this cache.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: int
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def set(self, key, value, *args, **kwargs):
        """
        sets a new value into cached items.

        :param object key: hashable key of the cache to be registered.
        :param object value: value to be cached.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def get(self, key, default=None):
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
    def move_to_end(self, key, last=True):
        """
        moves the given key and its value to the end of queue.

        :param object key: key to be moved.

        :param bool last: specifies that item must be moved to end.
                          defaults to True if not provided.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def slice(self, count, last=False):
        """
        gets a slice of items of this container with the count length.

        :param int count: number of items to include in slice.

        :param bool last: specifies that slice must include items from end.
                          defaults to False if not provided.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: iterable
        """

        raise CoreNotImplementedError()
