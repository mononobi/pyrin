# -*- coding: utf-8 -*-
"""
caching mixin typed module.
"""

from pyrin.caching.mixin.base import CacheMixinBase


class TypedCacheMixin(CacheMixinBase):
    """
    typed cache mixin class.

    this type of cache mixin, caches items in a dict separated by type of
    each instance. so instances of the same type, will share the same cache.
    """

    _container = {}

    @classmethod
    def generate_key(cls, func, **options):
        """
        generates a cache key from given inputs.

        :param function func: function to be cached.

        :returns: object
        """

        return cls, func.__name__
