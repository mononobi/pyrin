# -*- coding: utf-8 -*-
"""
caching decorators module.
"""

from functools import update_wrapper

from werkzeug.utils import cached_property as cached_property_base

import pyrin.caching.services as caching_services
import pyrin.utils.function as function_utils

from pyrin.core.decorators import class_property


def cache(*args, **kwargs):
    """
    decorator to register a cache.

    :param object args: cache class constructor arguments.
    :param object kwargs: cache class constructor keyword arguments.

    :keyword bool replace: specifies that if there is another registered
                           cache with the same name, replace it with
                           the new one, otherwise raise an error.
                           defaults to False.

    :keyword int limit: limit count or size of cached items.
                        if not provided, it will be get
                        from `caching` config store.
                        if you want to remove count limit,
                        you could pass `caching.globals.NO_LIMIT`
                        as input. this is only used in complex
                        and some remote caches.

    :keyword int expire: default expire time of cached items in milliseconds.
                         if not provided, it will be get from `caching` config
                         store. this is only used in complex and remote caches.

    :keyword bool refreshable: specifies that cached item's expire time must be
                               extended on each hit. if not provided, will be get
                               from `caching` config store. this is only used in
                               complex caches.

    :keyword bool use_lifo: specifies that items of the cache must
                            be removed in lifo order. if not provided,
                            it will be get from `caching` config store.
                            this is only used in complex caches.

    :keyword int clear_count: number of old items to be removed from cache when
                              the cache is full. if not provided, it will be get
                              from `caching` config store.
                              note that reducing this value to extremely low values
                              will cause a performance issue when the cache becomes full.
                              this is only used in complex caches.

    :keyword bool consider_user: specifies that current user must be included in
                                 key generation. if not provided, it will be get
                                 from `caching` config store.
                                 this is only used in extended, complex and remote
                                 caches.

    :keyword bool persistent: specifies that cached items must be persisted to
                              database on application shutdown, and loaded back
                              on application startup. if not provided, will be
                              get from `caching` config store.
                              this is only used in complex caches.

    :keyword int chunk_size: chunk size to insert values for persistent caches.
                             after each chunk, store will be flushed.
                             if not provided, will be get from `caching` config store.
                             this is only used in complex caches.

    :raises InvalidCacheTypeError: invalid cache type error.
    :raises DuplicatedCacheError: duplicated cache error.

    :returns: cache class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available caches.

        :param type cls: cache class.

        :returns: cache class.
        :rtype: type
        """

        instance = cls(*args, **kwargs)
        caching_services.register_cache(instance, **kwargs)

        return cls

    return decorator


def permanent(*old_method):
    """
    decorator to convert a method or property into a lazy one.

    note that this cache type is permanent and will not consider method inputs
    in caching. the result will be calculated once and then it will be cached.
    each result will be cached using a tuple of class type and method name as
    a key in the cache. so if used on instance or class methods, all instances
    of the same class type will have access to the same shared cache. if you want
    to use a cache per each instance of a class type, you could use `cached_property`
    decorator.

    note that this decorator should only be used on instance or class methods or
    properties. otherwise the result would be inconsistent.
    for stand-alone functions use `permanent_function` decorator.

    :param function | property old_method: the original decorated method or property.

    :returns: method or property result.
    """

    def decorator(method):
        """
        decorates the given method or property and makes it a lazy one.

        :param function | property method: decorated method or property.

        :returns: method or property result.
        """

        def wrapper(self):
            """
            decorates the given method or property and makes it a lazy one.

            :returns: method or property result.
            """

            result = caching_services.try_get('permanent', method, self)
            if result is not None:
                return result

            result = method(self)
            caching_services.try_set('permanent', result, method, self)
            return result

        return update_wrapper(wrapper, method)

    if len(old_method) > 0:
        return decorator(old_method[0])

    return decorator


def permanent_function(*old_func):
    """
    decorator to convert a function into a lazy one.

    note that this cache type is permanent and will not consider function inputs
    in caching. the result will be calculated once and then it will be cached.
    each result will be cached using a tuple of function fully qualified name as
    a key in the cache.

    note that this decorator should only be used on stand-alone functions.
    otherwise the result would be inconsistent. for instance or class methods
    use `permanent` decorator.

    :param function old_func: the original decorated function.

    :returns: function result.
    """

    def decorator(func):
        """
        decorates the given function and makes it a lazy one.

        :param function func: decorated function.

        :returns: function result.
        """

        def wrapper():
            """
            decorates the given function and makes it a lazy one.

            :returns: function result.
            """

            result = caching_services.try_get('permanent', func, None)
            if result is not None:
                return result

            result = func()
            caching_services.try_set('permanent', result, func, None)
            return result

        return update_wrapper(wrapper, func)

    if len(old_func) > 0:
        return decorator(old_func[0])

    return decorator


def extended_permanent(*old_func, **options):
    """
    decorator to convert a method or function into a lazy one.

    note that this cache type is permanent but will consider function inputs
    in caching. the result will be calculated once and then it will be cached.
    each result will be cached using a tuple of parent class type, function fully
    qualified name, inputs, current user and component key as a key in the cache.

    that this decorator could be used on both instance or class level methods and
    properties or stand-alone functions.

    :param function old_func: the original decorated method or function.

    :keyword bool consider_user: specifies that current user must be included in
                                 key generation. if not provided, it will be get
                                 from `caching` config store.

    :returns: function result.
    """

    def decorator(func):
        """
        decorates the given method or function and makes it a lazy one.

        :param function func: decorated method or function.

        :returns: function result.
        """

        def wrapper(*args, **kwargs):
            """
            decorates the given method or function and makes it a lazy one.

            :param object args: function positional arguments.
            :param object kwargs: function keyword arguments.

            :returns: function result.
            """

            result = caching_services.try_get('extended.permanent', func,
                                              args, kwargs, **options)
            if result is not None:
                return result

            result = func(*args, **kwargs)
            caching_services.try_set('extended.permanent', result, func,
                                     args, kwargs, **options)
            return result

        return update_wrapper(wrapper, func)

    if len(old_func) > 0:
        return decorator(old_func[0])

    return decorator


def cached(*old_method, **options):
    """
    decorator to convert a method or function into a lazy one.

    note that this cache type supports expire time and will consider method inputs
    in caching. the result will be calculated once and then it will be cached.
    each result will be cached using a tuple of class type, method name, inputs,
    current user and component key as a key in the cache.

    that this decorator could be used on both instance or class level methods and
    properties or stand-alone functions.

    :param function | property old_method: the original decorated method or function.

    :keyword bool consider_user: specifies that current user must be included in
                                 key generation. if not provided, it will be get
                                 from `caching` config store.

    :keyword int expire: expire time for given key in milliseconds.
                         if not provided, it will be get from `caching`
                         config store.

    :keyword bool refreshable: specifies that cached item's expire time must be
                               extended on each hit. if not provided, it will be
                               get from `caching` config store.

    :returns: method or function result.
    """

    def decorator(method):
        """
        decorates the given method or function and makes it a lazy one.

        :param function | property method: decorated method or function.

        :returns: method or function result.
        """

        def wrapper(*args, **kwargs):
            """
            decorates the given method or function and makes it a lazy one.

            :param object args: function positional arguments.
            :param object kwargs: function keyword arguments.

            :returns: method or function result.
            """

            result = caching_services.try_get('complex', method, args,
                                              kwargs, **options)
            if result is not None:
                return result

            result = method(*args, **kwargs)
            caching_services.try_set('complex', result, method,
                                     args, kwargs, **options)
            return result

        return update_wrapper(wrapper, method)

    if len(old_method) > 0:
        return decorator(old_method[0])

    return decorator


def custom_cached(name, *old_method, **options):
    """
    decorator to convert a method or function into a lazy one.

    note that this cache type supports expire time and will consider method inputs
    in caching. the result will be calculated once and then it will be cached.
    each result will be cached using a tuple of class type, method name, inputs,
    current user and component key as a key in the cache.

    that this decorator could be used on both instance or class level methods and
    properties or stand-alone functions.

    :param str name: the cache name to be used.
                     for example: `redis`, `memcached`, `complex` or ...

    :param function | property old_method: the original decorated method or function.

    :keyword bool consider_user: specifies that current user must be included in
                                 key generation. if not provided, it will be get
                                 from `caching` config store.

    :keyword int expire: expire time for given key in milliseconds.
                         if not provided, it will be get from `caching`
                         config store.

    :keyword bool refreshable: specifies that cached item's expire time must be
                               extended on each hit. if not provided, it will be
                               get from `caching` config store.

    :returns: method or function result.
    """

    def decorator(method):
        """
        decorates the given method or function and makes it a lazy one.

        :param function | property method: decorated method or function.

        :returns: method or function result.
        """

        def wrapper(*args, **kwargs):
            """
            decorates the given method or function and makes it a lazy one.

            :param object args: function positional arguments.
            :param object kwargs: function keyword arguments.

            :returns: method or function result.
            """

            result = caching_services.try_get(name, method, args,
                                              kwargs, **options)
            if result is not None:
                return result

            result = method(*args, **kwargs)
            caching_services.try_set(name, result, method,
                                     args, kwargs, **options)
            return result

        return update_wrapper(wrapper, method)

    if len(old_method) > 0:
        return decorator(old_method[0])

    return decorator


class cached_property(cached_property_base):
    """
    a decorator to convert a property into a cached property.

    the result of the property will be calculated once and cached.
    the cached value is per instance not per type.

    usage example:

    @cached_property
    def is_valid(self):
        return True
    """
    pass


class cached_class_property(class_property):
    """
    a decorator to convert a class property into a cached class property.

    the result of the class property will be calculated once and cached.
    the cached value is per type not per instance.
    it only supports get.

    usage example:

    @cached_class_property
    def is_valid(cls):
        return True
    """

    def __init__(self, method=None):
        """
        initializes an instance of cached_class_property.

        :param function method: decorated method.
        """

        super().__init__(method)
        self.__cache_name__ = self._get_cache_key()

    def __get__(self, instance, cls=None):
        """
        gets the result of decorated method.

        if the result is available in the cache, it will be get from there.
        otherwise the method will be called to produce result.

        :param instance: instance of parent class.
        :param type cls: class type.

        :returns: decorated method result.
        """

        if cls is None:
            cls = type(instance)

        try:
            return vars(cls)[self.__cache_name__]
        except KeyError:
            result = super().__get__(instance, cls)
            setattr(cls, self.__cache_name__, result)
            return result

    def _get_cache_key(self):
        """
        gets the cache key name for current method.

        :rtype: str
        """

        return '__CACHED__{method}__'.format(
            method=function_utils.get_fully_qualified_name(self.fget).upper())
