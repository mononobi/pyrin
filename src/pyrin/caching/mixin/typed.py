# -*- coding: utf-8 -*-
"""
caching mixin typed module.
"""

import pyrin.utils.function as func_utils
import pyrin.security.session.services as session_services

from pyrin.caching.structs import CacheableDict
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


class ExtendedTypedCacheMixin(CacheMixinBase):
    """
    extended typed cache mixin class.

    this type of cache mixin, is the same as `TypedCacheMixin`, but it also
    considers method inputs and component key and current user in cache key generation.
    """

    _container = {}

    @classmethod
    def generate_key(cls, func, inputs, kw_inputs, **options):
        """
        generates a cache key from given inputs.

        :param function func: function to be cached.
        :param tuple inputs: function positional arguments.
        :param dict kw_inputs: function keyword arguments.

        :keyword bool consider_user: specifies that current user must be included in
                                     key generation. defaults to True if not provided.

        :returns: hash of generated key
        :rtype: int
        """

        consider_user = options.get('consider_user', True)
        current_user = None
        if consider_user is not False:
            current_user = session_services.get_safe_cacheable_current_user()

        cacheable_inputs, parent = func_utils.get_inputs(func, inputs, kw_inputs,
                                                         CacheableDict)
        component_key = session_services.get_safe_component_custom_key()

        return hash((cls, func.__name__, cacheable_inputs, current_user, component_key))
