# -*- coding: utf-8 -*-
"""
caching manager module.
"""

import pyrin.application.services as application_services

from pyrin.caching import CachingPackage
from pyrin.caching.interface import AbstractCachingHandler
from pyrin.core.structs import Manager
from pyrin.utils.custom_print import print_warning
from pyrin.caching.exceptions import CachingHandlerNotFoundError, \
    DuplicatedCachingHandlerError, InvalidCachingHandlerTypeError, CacheIsNotPersistentError


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

        self._caching_handlers = {}

    def register_caching_handler(self, instance, **options):
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

        if not isinstance(instance, AbstractCachingHandler):
            raise InvalidCachingHandlerTypeError('Input parameter [{instance}] is '
                                                 'not an instance of [{base}].'
                                                 .format(instance=instance,
                                                         base=AbstractCachingHandler))

        if instance.get_name() in self._caching_handlers:
            old_instance = self.get_caching_handler(instance.get_name())
            replace = options.get('replace', False)
            if replace is not True:
                raise DuplicatedCachingHandlerError('There is another registered caching '
                                                    'handler [{old}] with name [{name}] but '
                                                    '"replace" option is not set, so caching '
                                                    'handler [{instance}] could not be '
                                                    'registered.'
                                                    .format(old=old_instance,
                                                            name=instance.get_name(),
                                                            instance=instance))

            print_warning('Caching handler [{old_instance}] is going '
                          'to be replaced by [{new_instance}].'
                          .format(old_instance=old_instance,
                                  new_instance=instance))

        self._caching_handlers[instance.get_name()] = instance

    def get_caching_handler(self, name):
        """
        gets the registered caching handler with given name.

        it raise an error if no handler found for given name.

        :param str name: name of caching handler to be get.

        :raises CachingHandlerNotFoundError: caching handler not found error.

        :rtype: AbstractCachingHandler
        """

        if name not in self._caching_handlers:
            raise CachingHandlerNotFoundError('Caching handler [{name}] not found.'
                                              .format(name=name))

        return self._caching_handlers.get(name)

    def contains(self, name, key):
        """
        gets a value indicating that given key is existed in the cached items of given handler.

        :param str name: name of caching handler.
        :param object key: key to be checked for existence.

        :raises CachingHandlerNotFoundError: caching handler not found error.

        :rtype: bool
        """

        cache = self.get_caching_handler(name)
        return cache.contains(key)

    def pop(self, name, key, default=None):
        """
        pops the given key from cached items of given handler and returns its value.

        if key does not exist, it returns None or the specified default value.

        :param str name: name of caching handler.
        :param object key: key to get its value.
        :param object default: value to be returned if key is not present.

        :raises CachingHandlerNotFoundError: caching handler not found error.

        :returns: object
        """

        cache = self.get_caching_handler(name)
        return cache.pop(key, default)

    def remove(self, name, key):
        """
        removes the given key from cached items of given handler.

        it does nothing if the key is not present in the cache.

        :param str name: name of caching handler.
        :param object key: key to be removed.

        :raises CachingHandlerNotFoundError: caching handler not found error.
        """

        cache = self.get_caching_handler(name)
        cache.remove(key)

    def clear(self, name):
        """
        clears a cache with given name.

        :param str name: caching handler name to be cleared.

        :raises CachingHandlerNotFoundError: caching handler not found error.
        """

        cache = self.get_caching_handler(name)
        cache.clear()

    def set(self, name, key, value, **options):
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

        cache = self.get_caching_handler(name)
        cache.set(key, value, **options)

    def get(self, name, key, default=None, **options):
        """
        gets the value from given cache.

        if key does not exist, it returns None or the specified default value.

        :param str name: caching handler name.
        :param object key: hashable key to get its value from cache.
        :param object default: value to be returned if key is not present.

        :raises CachingHandlerNotFoundError: caching handler not found error.

        :returns: object
        """

        cache = self.get_caching_handler(name)
        return cache.get(key, default=default, **options)

    def try_set(self, name, value, func, *extra_keys, **options):
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

        cache = self.get_caching_handler(name)
        cache.try_set(value, func, *extra_keys, **options)

    def try_get(self, name, func, *extra_keys, default=None, **options):
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

        cache = self.get_caching_handler(name)
        return cache.try_get(func, *extra_keys, default=default, **options)

    def generate_key(self, name, func, *extra_keys, **options):
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

        cache = self.get_caching_handler(name)
        return cache.generate_key(func, *extra_keys, **options)

    def exists(self, name):
        """
        returns a value indicating that a caching handler with the given name existed.

        :param str name: caching handler name.

        :rtype: bool
        """

        return name is self._caching_handlers

    def get_cache_names(self):
        """
        gets all available caching handler names.

        :rtype: list[str]
        """

        return list(self._caching_handlers.keys())

    def get_stats(self, name):
        """
        gets statistic info of given caching handler.

        :param str name: caching handler name to get its info.

        :raises CachingHandlerNotFoundError: caching handler not found error.

        :rtype: dict
        """

        cache = self.get_caching_handler(name)
        return cache.stats

    def get_all_stats(self):
        """
        gets statistic info of all caching handlers.

        :rtype: dict
        """

        result = {}
        for name, cache in self._caching_handlers.items():
            result[name] = cache.stats

        return result

    def persist(self, name, **options):
        """
        saves cached items of given caching handler into database.

        :param str name: caching handler name to be persisted.

        :raises CachingHandlerNotFoundError: caching handler not found error.
        :raises CacheIsNotPersistentError: cache is not persistent error.
        """

        cache = self.get_caching_handler(name)
        if cache.persistent is False:
            raise CacheIsNotPersistentError('Caching handler [{name}] is not persistent.'
                                            .format(name=cache.get_name()))

        version = application_services.get_application_version()
        cache.persist(version, **options)

    def persist_all(self, **options):
        """
        saves cached items of all persistent caching handlers into database.
        """

        for name, cache in self._caching_handlers.items():
            if cache.persistent is True:
                self.persist(name, **options)

    def load(self, name, **options):
        """
        loads cached items of given caching handler from database.

        :param str name: caching handler name to be loaded.

        :raises CachingHandlerNotFoundError: caching handler not found error.
        :raises CacheIsNotPersistentError: cache is not persistent error.
        """

        cache = self.get_caching_handler(name)
        if cache.persistent is False:
            raise CacheIsNotPersistentError('Caching handler [{name}] is not persistent.'
                                            .format(name=cache.get_name()))

        version = application_services.get_application_version()
        cache.load(version, **options)

    def load_all(self, **options):
        """
        loads cached items of all persistent caching handlers from database.
        """

        for name, cache in self._caching_handlers.items():
            if cache.persistent is True:
                self.load(name, **options)
