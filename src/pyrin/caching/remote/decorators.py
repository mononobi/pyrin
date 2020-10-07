# -*- coding: utf-8 -*-
"""
caching remote decorators module.
"""

from functools import update_wrapper

import pyrin.caching.services as caching_services


def memcached(*old_method, **options):
    """
    decorator to convert a method or function into a lazy one.

    note that this cache type supports expire time and will consider method inputs
    in caching. the result will be calculated once and then it will be cached.
    each result will be cached using a tuple of class type, method name, inputs,
    current user and component key as a key in the cache.

    that this decorator could be used on both instance or class level methods and
    properties or stand-alone functions.

    to be able to use this decorator you must install memcached client dependency
    using `pip install pyrin[memcached]` and also remove
    `pyrin.caching.remote.handlers.memcached` from `ignored_modules` of
    `packaging.ini` file.

    :param function | property old_method: the original decorated method or function.

    :keyword bool consider_user: specifies that current user must be included in
                                 key generation. if not provided, it will be get
                                 from `caching` config store.

    :keyword int expire: expire time for given key in seconds.
                         if not provided, it will be get from `caching`
                         config store.

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

            result = caching_services.try_get('memcached', method, args,
                                              kwargs, **options)
            if result is not None:
                return result

            result = method(*args, **kwargs)
            caching_services.try_set('memcached', result, method,
                                     args, kwargs, **options)
            return result

        return update_wrapper(wrapper, method)

    if len(old_method) > 0:
        return decorator(old_method[0])

    return decorator


def redis(*old_method, **options):
    """
    decorator to convert a method or function into a lazy one.

    note that this cache type supports expire time and will consider method inputs
    in caching. the result will be calculated once and then it will be cached.
    each result will be cached using a tuple of class type, method name, inputs,
    current user and component key as a key in the cache.

    that this decorator could be used on both instance or class level methods and
    properties or stand-alone functions.

    to be able to use this decorator you must install redis client dependency
    using `pip install pyrin[redis]` and also remove
    `pyrin.caching.remote.handlers.redis` from `ignored_modules` of
    `packaging.ini` file.

    :param function | property old_method: the original decorated method or function.

    :keyword bool consider_user: specifies that current user must be included in
                                 key generation. if not provided, it will be get
                                 from `caching` config store.

    :keyword int expire: expire time for given key in milliseconds.
                         if not provided, it will be get from `caching`
                         config store.

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

            result = caching_services.try_get('redis', method, args,
                                              kwargs, **options)
            if result is not None:
                return result

            result = method(*args, **kwargs)
            caching_services.try_set('redis', result, method,
                                     args, kwargs, **options)
            return result

        return update_wrapper(wrapper, method)

    if len(old_method) > 0:
        return decorator(old_method[0])

    return decorator
