# -*- coding: utf-8 -*-
"""
caching structs module.
"""

from pyrin.core.structs import CoreObject


class SharedContainer(CoreObject):
    """
    shared container class.

    this class saves values in its `_storage` class attribute.
    subclasses could override the `_storage` to separate it per each scope.
    """

    _storage = dict()

    @classmethod
    def get(cls, key):
        """
        gets a value from cache with the given key.

        returns None if not found.

        :param object key: key to get its cache.

        :rtype: object
        """

        return cls._storage.get(key, None)

    @classmethod
    def set(cls, key, value):
        """
        sets the given value with provided key in the cache.

        :param object key: key to save value with it.
        :param object value: value to be cached.
        """

        cls._storage[key] = value

    @classmethod
    def invalidate(cls):
        """
        invalidates the current container.

        it results to all cached values get deleted.
        """

        cls._storage.clear()
