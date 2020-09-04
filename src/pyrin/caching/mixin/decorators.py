# -*- coding: utf-8 -*-
"""
caching mixin decorators module.
"""

from functools import update_wrapper


def fast_cache(*old_method):
    """
    decorator to convert a method or property into a lazy one.

    note that this type of caches will generate cache key based on
    parent type and function name. so it could only be used on instance or class
    level methods and properties. the cached method also could not have any arguments.

    note that this decorator should only be used in classes which subclassed from
    `TypedCacheMixin` class.

    this type of caches are implemented to be used where performance is critical.
    it has as few overhead as possible even on single usage.

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

            result = self.get_cache(method)
            if result is not None:
                return result

            result = method(self)
            self.set_cache(result, method)

            return result

        return update_wrapper(wrapper, method)

    if len(old_method) > 0:
        return decorator(old_method[0])

    return decorator


def extended_fast_cache(*old_method, **options):
    """
    decorator to convert a method or property into a lazy one.

    note that this type of caches will generate cache key based on
    parent type, function name, method inputs, current user and component key.
    so it could only be used on instance or class level methods and properties.

    note that this decorator should only be used in classes which subclassed from
    `ExtendedTypedCacheMixin` class.

    this type of caches are implemented to be used where performance is critical.
    it has as few overhead as possible but it is slower than `fast_cache` because
    it processes function inputs.

    important note: if you want to use this decorator inside pyrin code, you must
    add `pyrin.security.session` into depends list of the package that uses this
    decorator. this is not required in top level application.

    :param function | property old_method: the original decorated method or property.

    :keyword bool consider_user: specifies that current user must be included in
                                 key generation. defaults to True if not provided.

    :returns: method or property result.
    """

    def decorator(method):
        """
        decorates the given method or property and makes it a lazy one.

        :param function | property method: decorated method or property.

        :returns: method or property result.
        """

        def wrapper(self, *args, **kwargs):
            """
            decorates the given method or property and makes it a lazy one.

            :param object args: function positional arguments.
            :param object kwargs: function keyword arguments.

            :returns: method or property result.
            """

            result = self.get_cache(method, args, kwargs, **options)
            if result is not None:
                return result

            result = method(self, *args, **kwargs)
            self.set_cache(result, method, args, kwargs, **options)

            return result

        return update_wrapper(wrapper, method)

    if len(old_method) > 0:
        return decorator(old_method[0])

    return decorator
