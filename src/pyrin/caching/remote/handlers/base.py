# -*- coding: utf-8 -*-
"""
caching remote handlers base module.
"""

from abc import abstractmethod

import pyrin.globalization.datetime.services as datetime_services
import pyrin.configuration.services as config_services
import pyrin.logging.services as logging_services

from pyrin.caching.interface import AbstractRemoteCache
from pyrin.caching.mixin.base import ComplexKeyGeneratorMixin
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.caching.exceptions import CacheNameIsRequiredError, InvalidCacheExpireTimeError


class RemoteCacheBase(ComplexKeyGeneratorMixin, AbstractRemoteCache):
    """
    remote cache base class.

    it could be used as the base class for all remote caches, such as memcached and redis.
    """

    # cache name to be used for this cache.
    # it must be unique between all caches.
    cache_name = None

    LOGGER = logging_services.get_logger('caching.remote')

    def __init__(self, *args, **options):
        """
        initializes an instance of RemoteCacheBase.

        :keyword int expire: default expire time of cached items in milliseconds.
                             if not provided, it will be get from `caching` config
                             store.

        :keyword bool consider_user: specifies that current user must also be
                                     included in cache key. if not provided, will
                                     be get from `caching` config store.

        :raises CacheNameIsRequiredError: cache name is required error.
        :raises InvalidCacheExpireTimeError: invalid cache expire time error.
        """

        super().__init__()

        if self.cache_name in (None, '') or self.cache_name.isspace():
            raise CacheNameIsRequiredError('Cache name must be provided for '
                                           'cache [{name}].'.format(name=self))

        self._set_name(self.cache_name)

        expire = options.get('expire')
        consider_user = options.get('consider_user')

        configs = self._get_configs()
        if expire is None:
            expire = configs.pop('expire')
        configs.pop('expire', None)

        if consider_user is None:
            consider_user = configs.pop('consider_user')
        configs.pop('consider_user', None)

        if expire < 0:
            raise InvalidCacheExpireTimeError('Cache expire time for cache [{name}] '
                                              'must be a non-negative integer.'
                                              .format(name=self.get_name()))

        self._last_cleared_time = datetime_services.now()
        self._expire = expire
        self._consider_user = consider_user
        self._client = self._create_client(*args, kwargs=options, **configs)

    @abstractmethod
    def _create_client(self, *args, kwargs=None, **configs):
        """
        creates a client for connecting to remote cache server.

        :param object args: all positional arguments passed to `__init__` method.
        :param dict kwargs: all keyword arguments passed to `__init__` method.

        :keyword object configs: all configurations of this cache from `caching`
                                 config store.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: object
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def _clear(self):
        """
        clears all items from cache.

        this method is intended to be overridden in subclasses.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def _set(self, key, value, *args, **options):
        """
        sets a new value into cached items.

        this method must be overridden in subclasses.

        :param object key: hashable key of the cache to be registered.
        :param object value: value to be cached.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def _get(self, key, default=None, **options):
        """
        gets the value from cache.

        if key does not exist, it returns None or the specified default value.
        this method must be overridden in subclasses.

        :param object key: hashable key to get its value from cache.
        :param object default: value to be returned if key is not present.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: object
        """

        raise CoreNotImplementedError()

    def _prepare_key(self, key):
        """
        prepares the key to be used in cache.

        this method is intended to be overridden in subclasses.

        :param object key: key to be cached.

        :returns: prepared key.
        """

        return key

    def _prepare_for_set(self, value):
        """
        prepares the value that must be cached.

        this method is intended to be overridden in subclasses.

        :param object value: value to be cached.

        :returns: prepared value.
        """

        return value

    def _prepare_for_get(self, value):
        """
        prepares the value that must be returned from cache.

        this method is intended to be overridden in subclasses.

        :param object value: value to be returned.

        :returns: prepared value.
        """

        return value

    def _get_configs(self):
        """
        gets the configs of this cache from `caching` config store.

        :rtype: dict
        """

        return config_services.get_section('caching', self.get_name())

    def _get_hit_ratio(self):
        """
        gets hit ratio for this cache in percentage.

        :rtype: float
        """

        hit = self.hit_count
        miss = self.miss_count
        if hit == 0 and miss == 0:
            return 0

        ratio = hit / (hit + miss)
        return ratio * 100

    def _try_set(self, value, func, inputs, kw_inputs, *args, **options):
        """
        sets a new value into cached items.

        this method will generate cache key from given type and function
        and inputs. it also considers current component key in key generation.

        :param object value: value to be cached.
        :param function func: function to cache its result.
        :param tuple inputs: function positional arguments.
        :param dict kw_inputs: function keyword arguments.

        :keyword bool consider_user: specifies that current user must be included in
                                     key generation. it will be get from `consider_user`
                                     attribute store if not provided.
        """

        key = self.generate_key(func, inputs, kw_inputs, *args, **options)
        self.set(key, value, **options)

    def _try_get(self, func, inputs, kw_inputs, *args, default=None, **options):
        """
        gets the value from cache.

        this method will generate cache key from given type and function
        and inputs. it also considers current component key in key generation.
        if key does not exist, it returns None or the specified default value.

        :param function func: function to to get its result.
        :param tuple inputs: function positional arguments.
        :param dict kw_inputs: function keyword arguments.
        :param object default: value to be returned if key is not present.

        :keyword bool consider_user: specifies that current user must be included in
                                     key generation. it will be get from `consider_user`
                                     attribute store if not provided.

        :returns: object
        """

        key = self.generate_key(func, inputs, kw_inputs, *args, **options)
        return self.get(key, default, **options)

    def set(self, key, value, *args, **options):
        """
        sets a new value into cached items.

        :param object key: hashable key of the cache to be registered.
        :param object value: value to be cached.
        """

        hashed_key = hash(key)
        hashed_key = self._prepare_key(hashed_key)
        prepared_value = self._prepare_for_set(value)
        self._set(hashed_key, prepared_value, *args, **options)

    def get(self, key, default=None, **options):
        """
        gets the value from cache.

        if key does not exist, it returns None or the specified default value.

        :param object key: hashable key to get its value from cache.
        :param object default: value to be returned if key is not present.

        :returns: object
        """

        hashed_key = hash(key)
        hashed_key = self._prepare_key(hashed_key)
        result = self._get(hashed_key, default=default, **options)
        if result in (None, default):
            return result

        return self._prepare_for_get(result)

    def try_set(self, value, func, inputs, kw_inputs, *args, **options):
        """
        sets a new value into cached items.

        this method will generate cache key from given type and function
        and inputs. it also considers current component key in key generation.

        :param object value: value to be cached.
        :param function func: function to cache its result.
        :param tuple inputs: function positional arguments.
        :param dict kw_inputs: function keyword arguments.

        :keyword bool consider_user: specifies that current user must be included in
                                     key generation. it will be get from `consider_user`
                                     attribute store if not provided.
        """

        try:
            self._try_set(value, func, inputs, kw_inputs, *args, **options)
        except TypeError as error:
            self.LOGGER.exception(str(error))

    def try_get(self, func, inputs, kw_inputs, *args, default=None, **options):
        """
        gets the value from cache.

        this method will generate cache key from given type and function
        and inputs. it also considers current component key in key generation.
        if key does not exist, it returns None or the specified default value.

        :param function func: function to to get its result.
        :param tuple inputs: function positional arguments.
        :param dict kw_inputs: function keyword arguments.
        :param object default: value to be returned if key is not present.

        :keyword bool consider_user: specifies that current user must be included in
                                     key generation. it will be get from `consider_user`
                                     attribute store if not provided.

        :returns: object
        """

        try:
            return self._try_get(func, inputs, kw_inputs, *args, default=default, **options)
        except TypeError as error:
            self.LOGGER.exception(str(error))
            return None

    def clear(self):
        """
        clears all items from cache.
        """

        self._clear()
        self._last_cleared_time = datetime_services.now()

    @property
    def consider_user(self):
        """
        gets the consider user value for this cache.

        :rtype: bool
        """

        return self._consider_user

    @property
    def last_cleared_time(self):
        """
        gets the last time in which this cache has been cleared.

        :rtype: datetime.datetime
        """

        return self._last_cleared_time

    @property
    def stats(self):
        """
        get the statistic info about cached items.

        :returns: dict(datetime last_cleared_time: last cleared time,
                       bool persistent: persistent cache,
                       bool consider_user: consider user,
                       int expire: cached items expire time,
                       int hit: hit count,
                       int miss: miss count,
                       str hit_ratio: hit ratio)
        :rtype: dict
        """

        hit_ratio = self._get_hit_ratio()
        hit_ratio = '{:0.1f}%'.format(hit_ratio)

        return dict(last_cleared_time=self.last_cleared_time,
                    persistent=self.persistent,
                    consider_user=self.consider_user,
                    expire=self.expire,
                    hit=self.hit_count,
                    miss=self.miss_count,
                    hit_ratio=hit_ratio)

    @property
    def persistent(self):
        """
        gets a value indicating that cached items must be persisted to database on shutdown.

        :rtype: bool
        """

        return False

    @property
    def expire(self):
        """
        gets default expire time value for this cache's items in milliseconds.

        :rtype: int
        """

        return self._expire

    @property
    def client(self):
        """
        gets the client of this cache.

        :returns: object
        """

        return self._client
