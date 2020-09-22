# -*- coding: utf-8 -*-
"""
caching services module.
"""

from pyrin.application.services import get_component
from pyrin.caching import CachingPackage
from pyrin.database.transaction.decorators import atomic


def register_cache(instance, **options):
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

    get_component(CachingPackage.COMPONENT_NAME).register_cache(instance, **options)


def get_cache(name):
    """
    gets the registered cache with given name.

    it raises an error if no cache found for given name.

    :param str name: name of cache to be get.

    :raises CacheNotFoundError: cache not found error.

    :rtype: AbstractCache
    """

    return get_component(CachingPackage.COMPONENT_NAME).get_cache(name)


def contains(name, key):
    """
    gets a value indicating that given key is existed in the cached items of given cache.

    :param str name: name of the cache.
    :param object key: key to be checked for existence.

    :raises CacheNotFoundError: cache not found error.

    :rtype: bool
    """

    return get_component(CachingPackage.COMPONENT_NAME).contains(name, key)


def pop(name, key, default=None):
    """
    pops the given key from cached items of given cache and returns its value.

    if key does not exist, it returns None or the specified default value.

    :param str name: name of the cache.
    :param object key: key to get its value.
    :param object default: value to be returned if key is not present.

    :raises CacheNotFoundError: cache not found error.

    :returns: object
    """

    return get_component(CachingPackage.COMPONENT_NAME).pop(name, key, default=default)


def remove(name, key, **options):
    """
    removes the given key from cached items of given cache.

    it does nothing if the key is not present in the cache.

    :param str name: name of the cache.
    :param object key: key to be removed.

    :raises CacheNotFoundError: cache not found error.
    """

    get_component(CachingPackage.COMPONENT_NAME).remove(name, key, **options)


def clear(name):
    """
    clears a cache with given name.

    :param str name: cache name to be cleared.

    :raises CacheNotFoundError: cache not found error.
    """

    get_component(CachingPackage.COMPONENT_NAME).clear(name)


def set(name, key, value, **options):
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

    get_component(CachingPackage.COMPONENT_NAME).set(name, key, value, **options)


def get(name, key, default=None, **options):
    """
    gets the value from given cache.

    if key does not exist, it returns None or the specified default value.

    :param str name: cache name.
    :param object key: hashable key to get its value from cache.
    :param object default: value to be returned if key is not present.

    :raises CacheNotFoundError: cache not found error.

    :returns: object
    """

    return get_component(CachingPackage.COMPONENT_NAME).get(name, key,
                                                            default=default, **options)


def try_set(name, value, func, *extra_keys, **options):
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
                         this should only passed to extended and complex caches.

    :param dict kw_inputs: function keyword arguments.
                           this should only passed to extended, complex and remote caches.

    :param object extra_keys: extra arguments to generate key from.
                              this could be used in custom caches.

    :keyword bool consider_user: specifies that current user must also be
                                 included in cache key. if not provided, will
                                 be get from `caching` config store.
                                 this value is only used in complex, extended
                                 and remote caches.

    :keyword int expire: expire time for given key in milliseconds.
                         if not provided, will be get from `caching` config store.
                         this value is only used in complex and remote caches.

    :keyword bool refreshable: specifies that cached item's expire time must be
                               extended on each hit. if not provided, will be get
                               from `caching` config store.
                               this value is only used in complex caches.

    :raises CacheNotFoundError: cache not found error.
    """

    get_component(CachingPackage.COMPONENT_NAME).try_set(name, value, func,
                                                         *extra_keys, **options)


def try_get(name, func, *extra_keys, default=None, **options):
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
                         this should only passed to extended and complex caches.

    :param dict kw_inputs: function keyword arguments.
                           this should only passed to extended, complex and remote caches.

    :param object extra_keys: extra arguments to generate key from.
                              this could be used in custom caches.

    :param object default: value to be returned if key is not present.

    :keyword bool consider_user: specifies that current user must also be
                                 included in cache key. if not provided, will
                                 be get from `caching` config store.
                                 this value is only used in complex, extended
                                 and remote caches.

    :raises CacheNotFoundError: cache not found error.

    :returns: object
    """

    return get_component(CachingPackage.COMPONENT_NAME).try_get(name, func, *extra_keys,
                                                                default=default, **options)


def generate_key(name, func, *extra_keys, **options):
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
                                 this value is only used in complex, extended
                                 and remote caches.

    :raises CacheNotFoundError: cache not found error.

    :returns: hash of generated key.
    :rtype: int
    """

    return get_component(CachingPackage.COMPONENT_NAME).generate_key(name, func,
                                                                     *extra_keys, **options)


def exists(name):
    """
    returns a value indicating that a cache with the given name existed.

    :param str name: cache name.

    :rtype: bool
    """

    return get_component(CachingPackage.COMPONENT_NAME).exists(name)


def get_cache_names():
    """
    gets all available cache names.

    :rtype: list[str]
    """

    return get_component(CachingPackage.COMPONENT_NAME).get_cache_names()


def get_stats(name):
    """
    gets statistic info of given cache.

    :param str name: cache name to get its info.

    :raises CacheNotFoundError: cache not found error.

    :rtype: dict
    """

    return get_component(CachingPackage.COMPONENT_NAME).get_stats(name)


def get_all_stats():
    """
    gets statistic info of all caches.

    :rtype: dict
    """

    return get_component(CachingPackage.COMPONENT_NAME).get_all_stats()


def persist(name, **options):
    """
    saves cached items of given cache into database.

    :param str name: cache name to be persisted.

    :keyword bool clear: clear all caches after persisting them into database.
                         defaults to False if not provided.

    :raises CacheNotFoundError: cache not found error.
    :raises CacheIsNotPersistentError: cache is not persistent error.
    """

    return get_component(CachingPackage.COMPONENT_NAME).persist(name, **options)


@atomic
def persist_all(**options):
    """
    saves cached items of all persistent caches into database.

    :keyword bool clear: clear all caches after persisting them into database.
                         defaults to False if not provided.
    """

    return get_component(CachingPackage.COMPONENT_NAME).persist_all(**options)


def load(name, **options):
    """
    loads cached items of given cache from database.

    :param str name: cache name to be loaded.

    :raises CacheNotFoundError: cache not found error.
    :raises CacheIsNotPersistentError: cache is not persistent error.
    """

    return get_component(CachingPackage.COMPONENT_NAME).load(name, **options)


@atomic
def load_all(**options):
    """
    loads cached items of all persistent caches from database.
    """

    return get_component(CachingPackage.COMPONENT_NAME).load_all(**options)


def clear_required_caches():
    """
    clears all caches that are required.

    normally, you should never call this method manually. but it is
    implemented to be used for clearing extended and complex caches after
    application has been fully loaded. to enforce that valid results are
    cached based on loaded packages.
    """

    return get_component(CachingPackage.COMPONENT_NAME).clear_required_caches()
