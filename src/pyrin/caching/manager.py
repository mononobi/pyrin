# -*- coding: utf-8 -*-
"""
caching manager module.
"""

import pyrin.application.services as application_services

from pyrin.caching import CachingPackage
from pyrin.caching.interface import AbstractCache, AbstractExtendedLocalCache
from pyrin.core.structs import Manager, Context
from pyrin.utils.custom_print import print_warning
from pyrin.caching.exceptions import CacheNotFoundError, DuplicatedCacheError, \
    InvalidCacheTypeError, CacheIsNotPersistentError


class CachingManager(Manager):
    """
    caching manager class.
    """

    package_class = CachingPackage

    def __init__(self):
        """
        initializes an instance of CachingManager.
        """

        super().__init__()

        self._caches = Context()

    def register_cache(self, instance, **options):
        """
        registers a new cache or replaces the existing one.

        if `replace=True` is provided. otherwise, it raises an error
        on adding a cache which is already registered.

        :param AbstractCache instance: cache instance to be registered.

        :keyword bool replace: specifies that if there is another registered
                               cache with the same name, replace it with the
                               new one, otherwise raise an error. defaults to False.

        :raises InvalidCacheTypeError: invalid cache type error.
        :raises DuplicatedCacheError: duplicated cache error.
        """

        if not isinstance(instance, AbstractCache):
            raise InvalidCacheTypeError('Input parameter [{instance}] is '
                                        'not an instance of [{base}].'
                                        .format(instance=instance,
                                                base=AbstractCache))

        if instance.get_name() in self._caches:
            old_instance = self.get_cache(instance.get_name())
            replace = options.get('replace', False)
            if replace is not True:
                raise DuplicatedCacheError('There is another registered cache [{old}] '
                                           'with name [{name}] but "replace" option is not '
                                           'set, so cache [{instance}] could not be registered.'
                                           .format(old=old_instance,
                                                   name=instance.get_name(),
                                                   instance=instance))

            print_warning('Cache [{old_instance}] is going '
                          'to be replaced by [{new_instance}].'
                          .format(old_instance=old_instance,
                                  new_instance=instance))

        self._caches[instance.get_name()] = instance

    def get_cache(self, name):
        """
        gets the registered cache with given name.

        it raises an error if no cache found for given name.

        :param str name: name of cache to be get.

        :raises CacheNotFoundError: cache not found error.

        :rtype: AbstractCache
        """

        if name not in self._caches:
            raise CacheNotFoundError('Cache [{name}] does not exist.'
                                     .format(name=name))

        return self._caches.get(name)

    def contains(self, name, key):
        """
        gets a value indicating that given key is existed in the cached items of given cache.

        :param str name: name of the cache.
        :param object key: key to be checked for existence.

        :raises CacheNotFoundError: cache not found error.

        :rtype: bool
        """

        cache = self.get_cache(name)
        return cache.contains(key)

    def pop(self, name, key, default=None):
        """
        pops the given key from cached items of given cache and returns its value.

        if key does not exist, it returns None or the specified default value.

        :param str name: name of the cache.
        :param object key: key to get its value.
        :param object default: value to be returned if key is not present.

        :raises CacheNotFoundError: cache not found error.

        :returns: object
        """

        cache = self.get_cache(name)
        return cache.pop(key, default)

    def remove(self, name, key, **options):
        """
        removes the given key from cached items of given cache.

        it does nothing if the key is not present in the cache.

        :param str name: name of the cache.
        :param object key: key to be removed.

        :raises CacheNotFoundError: cache not found error.
        """

        cache = self.get_cache(name)
        cache.remove(key, **options)

    def clear(self, name):
        """
        clears a cache with given name.

        :param str name: cache name to be cleared.

        :raises CacheNotFoundError: cache not found error.
        """

        cache = self.get_cache(name)
        cache.clear()

    def set(self, name, key, value, **options):
        """
        sets a new value into given cache.

        :param str name: cache name.
        :param object key: hashable key of the cache to be registered.
        :param object value: value to be cached.

        :keyword int expire: expire time for given key in milliseconds.
                             if not provided, will be get from `caching` config store.
                             this value is only used in complex and remote caches.

        :keyword bool refreshable: specifies that cached item's expire time must be
                                   extended on each hit. if not provided, will be get
                                   from `caching` config store.
                                   this value is only used in complex caches.

        :raises CacheNotFoundError: cache not found error.
        """

        cache = self.get_cache(name)
        cache.set(key, value, **options)

    def get(self, name, key, default=None, **options):
        """
        gets the value from given cache.

        if key does not exist, it returns None or the specified default value.

        :param str name: cache name.
        :param object key: hashable key to get its value from cache.
        :param object default: value to be returned if key is not present.

        :raises CacheNotFoundError: cache not found error.

        :returns: object
        """

        cache = self.get_cache(name)
        return cache.get(key, default=default, **options)

    def try_set(self, name, value, func, *extra_keys, **options):
        """
        sets a new value into given cache.

        this method will generate cache key from given inputs.
        if the provided values are not hashable, this method won't raise
        an error and logs it silently.

        :param str name: cache name.
        :param object value: value to be cached.
        :param function func: function to cache its result.

        :param type | object parent: parent class or instance of given function.
                                     this should only passed to simple permanent caches.

        :param tuple inputs: function positional arguments.
                             this should only passed to extended, complex and remote caches.

        :param dict kw_inputs: function keyword arguments.
                               this should only passed to extended, complex and remote caches.

        :param object extra_keys: extra arguments to generate key from.
                                  this could be used in custom caches.

        :keyword bool consider_user: specifies that current user must also be
                                     included in cache key. if not provided, will
                                     be get from `caching` config store.
                                     this value is only used in complex,
                                     extended and remote caches.

        :keyword int expire: expire time for given key in milliseconds.
                             if not provided, will be get from `caching` config store.
                             this value is only used in complex and remote caches.

        :keyword bool refreshable: specifies that cached item's expire time must be
                                   extended on each hit. if not provided, will be get
                                   from `caching` config store.
                                   this value is only used in complex caches.

        :raises CacheNotFoundError: cache not found error.
        """

        cache = self.get_cache(name)
        cache.try_set(value, func, *extra_keys, **options)

    def try_get(self, name, func, *extra_keys, default=None, **options):
        """
        gets the value from given cache.

        this method will generate cache key from given inputs.
        if key does not exist, it returns None or the specified default value.
        if the provided values are not hashable, this method won't raise
        an error and logs it silently.

        :param str name: cache name.
        :param function func: function to to get its result.

        :param type | object parent: parent class or instance of given function.
                                     this should only passed to simple permanent caches.

        :param tuple inputs: function positional arguments.
                             this should only passed to extended, complex and remote caches.

        :param dict kw_inputs: function keyword arguments.
                               this should only passed to extended, complex and remote caches.

        :param object extra_keys: extra arguments to generate key from.
                                  this could be used in custom caches.

        :param object default: value to be returned if key is not present.

        :keyword bool consider_user: specifies that current user must also be
                                     included in cache key. if not provided, will
                                     be get from `caching` config store.
                                     this value is only used in complex,
                                     extended and remote caches.

        :raises CacheNotFoundError: cache not found error.

        :returns: object
        """

        cache = self.get_cache(name)
        return cache.try_get(func, *extra_keys, default=default, **options)

    def generate_key(self, name, func, *extra_keys, **options):
        """
        generates a cache key from given inputs for the given cache.

        :param str name: cache name.
        :param function func: function to to be cached.

        :param type | object parent: parent class or instance of given function.
                                     this should only passed to simple permanent caches.

        :param tuple inputs: function positional arguments.
                             this should only passed to extended and complex caches.

        :param dict kw_inputs: function keyword arguments.
                               this should only passed to extended, complex and remote caches.

        :param object extra_keys: extra arguments to generate key from.
                                  this could be used in custom caches.

        :keyword bool consider_user: specifies that current user must also be
                                     included in cache key. if not provided, will
                                     be get from `caching` config store.
                                     this value is only used in complex,
                                     extended and remote caches.

        :raises CacheNotFoundError: cache not found error.

        :returns: hash of generated key.
        :rtype: int
        """

        cache = self.get_cache(name)
        return cache.generate_key(func, *extra_keys, **options)

    def exists(self, name):
        """
        returns a value indicating that a cache with the given name existed.

        :param str name: cache name.

        :rtype: bool
        """

        return name is self._caches

    def get_cache_names(self):
        """
        gets all available cache names.

        :rtype: list[str]
        """

        return list(self._caches.keys())

    def get_stats(self, name):
        """
        gets statistic info of given cache.

        :param str name: cache name to get its info.

        :raises CacheNotFoundError: cache not found error.

        :rtype: dict
        """

        cache = self.get_cache(name)
        return cache.stats

    def get_all_stats(self):
        """
        gets statistic info of all caches.

        :rtype: dict
        """

        result = {}
        for name, cache in self._caches.items():
            result[name] = cache.stats

        return result

    def persist(self, name, **options):
        """
        saves cached items of given cache into database.

        :param str name: cache name to be persisted.

        :keyword bool clear: clear all caches after persisting them into database.
                             defaults to False if not provided.

        :raises CacheNotFoundError: cache not found error.
        :raises CacheIsNotPersistentError: cache is not persistent error.
        """

        cache = self.get_cache(name)
        if cache.persistent is False:
            raise CacheIsNotPersistentError('Cache [{name}] is not persistent.'
                                            .format(name=cache.get_name()))

        version = application_services.get_application_version()
        cache.persist(version, **options)

    def persist_all(self, **options):
        """
        saves cached items of all persistent caches into database.

        :keyword bool clear: clear all caches after persisting them into database.
                             defaults to False if not provided.
        """

        for name, cache in self._caches.items():
            if cache.persistent is True:
                self.persist(name, **options)

    def load(self, name, **options):
        """
        loads cached items of given cache from database.

        :param str name: cache name to be loaded.

        :raises CacheNotFoundError: cache not found error.
        :raises CacheIsNotPersistentError: cache is not persistent error.
        """

        cache = self.get_cache(name)
        if cache.persistent is False:
            raise CacheIsNotPersistentError('Cache [{name}] is not persistent.'
                                            .format(name=cache.get_name()))

        version = application_services.get_application_version()
        cache.load(version, **options)

    def load_all(self, **options):
        """
        loads cached items of all persistent caches from database.
        """

        for name, cache in self._caches.items():
            if cache.persistent is True:
                self.load(name, **options)

    def clear_required_caches(self):
        """
        clears all caches that are required.

        normally, you should never call this method manually. but it is
        implemented to be used for clearing extended and complex caches after
        application has been fully loaded. to enforce that valid results are
        cached based on loaded packages.
        """

        for name, cache in self._caches.items():
            if isinstance(cache, AbstractExtendedLocalCache):
                cache.clear()
