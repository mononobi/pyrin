# -*- coding: utf-8 -*-
"""
caching services module.
"""

from pyrin.application.services import get_component
from pyrin.caching import CachingPackage
from pyrin.database.transaction.decorators import atomic


def register_caching_handler(instance, **options):
    """
    registers a new caching handler or replaces the existing one.

    if `replace=True` is provided. otherwise, it raises an error
    on adding a caching handler which is already registered.

    :keyword bool replace: specifies that if there is another registered
                           caching handler with the same name, replace it
                           with the new one, otherwise raise an error.
                           defaults to False.

    :param AbstractCachingHandler instance: caching handler instance to be registered.

    :raises InvalidCachingHandlerTypeError: invalid caching handler type error.
    :raises DuplicatedCachingHandlerError: duplicated caching handler error.
    """

    get_component(CachingPackage.COMPONENT_NAME).register_caching_handler(instance, **options)


def get_caching_handler(name):
    """
    gets the registered caching handler with given name.

    it raise an error if no handler found for given name.

    :param str name: name of caching handler to be get.

    :raises CachingHandlerNotFoundError: caching handler not found error.

    :rtype: AbstractCachingHandler
    """

    return get_component(CachingPackage.COMPONENT_NAME).get_caching_handler(name)


def contains(name, key):
    """
    gets a value indicating that given key is existed in the cached items of given handler.

    :param str name: name of caching handler.
    :param object key: key to be checked for existence.

    :raises CachingHandlerNotFoundError: caching handler not found error.

    :rtype: bool
    """

    return get_component(CachingPackage.COMPONENT_NAME).contains(name, key)


def pop(name, key, default=None):
    """
    pops the given key from cached items of given handler and returns its value.

    if key does not exist, it returns None or the specified default value.

    :param str name: name of caching handler.
    :param object key: key to get its value.
    :param object default: value to be returned if key is not present.

    :raises CachingHandlerNotFoundError: caching handler not found error.

    :returns: object
    """

    return get_component(CachingPackage.COMPONENT_NAME).pop(name, key, default=default)


def remove(name, key):
    """
    removes the given key from cached items of given handler.

    it does nothing if the key is not present in the cache.

    :param str name: name of caching handler.
    :param object key: key to be removed.

    :raises CachingHandlerNotFoundError: caching handler not found error.
    """

    get_component(CachingPackage.COMPONENT_NAME).remove(name, key)


def clear(name):
    """
    clears a cache with given name.

    :param str name: caching handler name to be cleared.

    :raises CachingHandlerNotFoundError: caching handler not found error.
    """

    get_component(CachingPackage.COMPONENT_NAME).clear(name)


def set(name, key, value, **options):
    """
    sets a new value into given cache.

    :param str name: caching handler name.
    :param object key: hashable key of the cache to be registered.
    :param object value: value to be cached.

    :keyword int timeout: timeout for given key in milliseconds.
                          if not provided, will be get from caching config store.
                          this value is only used in complex handlers.

    :raises CachingHandlerNotFoundError: caching handler not found error.
    """

    get_component(CachingPackage.COMPONENT_NAME).set(name, key, value, **options)


def get(name, key, default=None, **options):
    """
    gets the value from given cache.

    if key does not exist, it returns None or the specified default value.

    :param str name: caching handler name.
    :param object key: hashable key to get its value from cache.
    :param object default: value to be returned if key is not present.

    :raises CachingHandlerNotFoundError: caching handler not found error.

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

    :param str name: caching handler name.
    :param object value: value to be cached.
    :param function func: function to cache its result.

    :param type | object parent: parent class or instance of given function.
                                 this should only passed to simple permanent handlers.

    :param tuple inputs: function positional arguments.
                         this should only passed to extended and complex handlers.

    :param dict kw_inputs: function keyword arguments.
                           this should only passed to extended and complex handlers.

    :param object extra_keys: extra arguments to generate key from.
                              this could be used in custom handlers.

    :keyword bool consider_user: specifies that current user must also be
                                 included in cache key. if not provided, will
                                 be get from `caching` config store.
                                 this value is only used in complex and
                                 extended handlers.

    :keyword int timeout: timeout for given key in milliseconds.
                          if not provided, will be get from caching config store.
                          this value is only used in complex handlers.

    :raises CachingHandlerNotFoundError: caching handler not found error.
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

    :param str name: caching handler name.
    :param function func: function to to get its result.

    :param type | object parent: parent class or instance of given function.
                                 this should only passed to simple permanent handlers.

    :param tuple inputs: function positional arguments.
                         this should only passed to extended and complex handlers.

    :param dict kw_inputs: function keyword arguments.
                           this should only passed to extended and complex handlers.

    :param object extra_keys: extra arguments to generate key from.
                              this could be used in custom handlers.

    :param object default: value to be returned if key is not present.

    :keyword bool consider_user: specifies that current user must also be
                                 included in cache key. if not provided, will
                                 be get from `caching` config store.
                                 this value is only used in complex and
                                 extended handlers.

    :raises CachingHandlerNotFoundError: caching handler not found error.

    :returns: object
    """

    return get_component(CachingPackage.COMPONENT_NAME).try_get(name, func, *extra_keys,
                                                                default=default, **options)


def generate_key(name, func, *extra_keys, **options):
    """
    generates a cache key from given inputs for the given cache.

    :param str name: caching handler name.
    :param function func: function to to be cached.

    :param type | object parent: parent class or instance of given function.
                                 this should only passed to simple permanent handlers.

    :param tuple inputs: function positional arguments.
                         this should only passed to extended and complex handlers.

    :param dict kw_inputs: function keyword arguments.
                           this should only passed to extended and complex handlers.

    :param object extra_keys: extra arguments to generate key from.
                              this could be used in custom handlers.

    :keyword bool consider_user: specifies that current user must also be
                                 included in cache key. if not provided, will
                                 be get from `caching` config store.
                                 this value is only used in complex and
                                 extended handlers.

    :raises CachingHandlerNotFoundError: caching handler not found error.

    :returns: hash of generated key.
    :rtype: int
    """

    return get_component(CachingPackage.COMPONENT_NAME).generate_key(name, func,
                                                                     *extra_keys, **options)


def exists(name):
    """
    returns a value indicating that a caching handler with the given name existed.

    :param str name: caching handler name.

    :rtype: bool
    """

    return get_component(CachingPackage.COMPONENT_NAME).exists(name)


def get_cache_names():
    """
    gets all available caching handler names.

    :rtype: list[str]
    """

    return get_component(CachingPackage.COMPONENT_NAME).get_cache_names()


def get_stats(name):
    """
    gets statistic info of given caching handler.

    :param str name: caching handler name to get its info.

    :raises CachingHandlerNotFoundError: caching handler not found error.

    :rtype: dict
    """

    return get_component(CachingPackage.COMPONENT_NAME).get_stats(name)


def get_all_stats():
    """
    gets statistic info of all caching handlers.

    :rtype: dict
    """

    return get_component(CachingPackage.COMPONENT_NAME).get_all_stats()


def persist(name, **options):
    """
    saves cached items of given caching handler into database.

    :param str name: caching handler name to be persisted.

    :raises CachingHandlerNotFoundError: caching handler not found error.
    :raises CacheIsNotPersistentError: cache is not persistent error.
    """

    return get_component(CachingPackage.COMPONENT_NAME).persist(name, **options)


@atomic
def persist_all(**options):
    """
    saves cached items of all persistent caching handlers into database.
    """

    return get_component(CachingPackage.COMPONENT_NAME).persist_all(**options)


def load(name, **options):
    """
    loads cached items of given caching handler from database.

    :param str name: caching handler name to be loaded.

    :raises CachingHandlerNotFoundError: caching handler not found error.
    :raises CacheIsNotPersistentError: cache is not persistent error.
    """

    return get_component(CachingPackage.COMPONENT_NAME).load(name, **options)


@atomic
def load_all(**options):
    """
    loads cached items of all persistent caching handlers from database.
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
