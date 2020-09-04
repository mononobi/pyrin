# -*- coding: utf-8 -*-
"""
caching mixin base module.
"""

from abc import abstractmethod

from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.core.structs import CoreObject


class CacheMixinBase(CoreObject):
    """
    cache mixin base class.
    """

    # each subclass must set this to a dict to get its own container.
    _container = None

    @classmethod
    def set_cache(cls, value, *keys, **options):
        """
        sets given value into the cache.

        :param object value: value to be cached.
        :param object keys: arguments to be used as cache key.
                            all arguments must be hashable.
        """

        key = cls.generate_key(*keys, **options)
        cls._container[key] = value

    @classmethod
    def get_cache(cls, *keys, **options):
        """
        gets the value of given key from cache.

        :param object keys: arguments to be used as cache key.
                            all arguments must be hashable.

        :returns: object
        """

        key = cls.generate_key(*keys, **options)
        return cls._container.get(key)

    @classmethod
    def clear_cache(cls):
        """
        clears all cached values.
        """

        cls._container.clear()

    @classmethod
    @abstractmethod
    def generate_key(cls, *keys, **options):
        """
        generates a cache key from given inputs.

        :param object keys: arguments to be used as cache key.
                            all arguments must be hashable.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: object
        """

        raise CoreNotImplementedError()
