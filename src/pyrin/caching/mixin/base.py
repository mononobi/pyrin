# -*- coding: utf-8 -*-
"""
caching mixin base module.
"""

from abc import abstractmethod

import pyrin.utils.function as func_utils
import pyrin.security.session.services as session_services

from pyrin.caching.structs import CacheableDict
from pyrin.core.exceptions import CoreNotImplementedError


class CacheMixinBase:
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


class SimpleKeyGeneratorMixin:
    """
    simple key generator mixin class.
    """

    def generate_key(self, func, parent, *args, **options):
        """
        generates a cache key from given inputs.

        :param function func: function to to be cached.
        :param type | object parent: parent class or instance of given function.

        :returns: hash of generated key
        :rtype: int
        """

        return hash(self._generate_key(func, parent, *args, **options))

    def _generate_key(self, func, parent, *args, **options):
        """
        generates a cache key from given inputs.

        :param function func: function to to be cached.
        :param type | object parent: parent class or instance of given function.

        :returns: tuple[type parent, str function_name]
        :rtype: tuple[type, str]
        """

        parent_type = None
        name = func.__name__
        if parent is None:
            name = func_utils.get_fully_qualified_name(func)
        else:
            parent_type = self._get_parent_type(parent)

        return parent_type, name

    def _get_parent_type(self, parent):
        """
        gets the parent type from given input.

        if it is a class itself, it returns the same input.

        :param type | object parent: class or instance to get its type.

        :rtype: type
        """

        parent_type = parent
        if not isinstance(parent_type, type):
            parent_type = type(parent_type)

        return parent_type


class ComplexKeyGeneratorMixin(SimpleKeyGeneratorMixin):
    """
    complex key generator mixin class.
    """

    def generate_key(self, func, inputs, kw_inputs, *args, **options):
        """
        generates a cache key from given inputs.

        :param function func: function to to be cached.
        :param tuple inputs: function positional arguments.
        :param dict kw_inputs: function keyword arguments.

        :keyword bool consider_user: specifies that current user must be included in
                                     key generation. it will be get from `caching` config
                                     store if not provided.

        :returns: hash of generated key
        :rtype: int
        """

        return hash(self._generate_key(func, inputs, kw_inputs, *args, **options))

    def _generate_key(self, func, inputs, kw_inputs, *args, **options):
        """
        generates a cache key from given inputs.

        :param function func: function to to be cached.
        :param tuple inputs: function positional arguments.
        :param dict kw_inputs: function keyword arguments.

        :keyword bool consider_user: specifies that current user must be included in
                                     key generation. it will be get from `caching` config
                                     store if not provided.

        :returns: tuple[type parent, str function_name,
                        dict inputs, object user,
                        object component key,
                        str timezone, str locale]

        :rtype: tuple[type, str, dict, object, object, str, str]
        """

        current_request = session_services.get_safe_current_request()
        timezone = None
        locale = None
        current_user = None
        component_key = None

        if current_request is not None:
            consider_user = options.get('consider_user', self.consider_user)
            if consider_user is not False:
                current_user = current_request.cacheable_user

            component_key = current_request.component_custom_key
            timezone = current_request.timezone.zone
            locale = current_request.locale

        cacheable_inputs, parent = func_utils.get_inputs(func, inputs,
                                                         kw_inputs, CacheableDict)

        parent_type, name = super()._generate_key(func, parent, *args, **options)

        return parent_type, name, cacheable_inputs, \
            current_user, component_key, timezone, locale
