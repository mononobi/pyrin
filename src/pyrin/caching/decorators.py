# -*- coding: utf-8 -*-
"""
caching decorators module.
"""

from functools import update_wrapper

from werkzeug.utils import cached_property as cached_property_base

from pyrin.caching.structs import SharedContainer
from pyrin.caching.key_providers import TypedKeyProvider


def local_cached(*old_method_or_property, container=None):
    """
    decorator to convert a method, property or function into a lazy one.

    the result will be calculated once and then it will be cached. each result
    will be cached using a tuple of class type, method or property or function
    name, inputs and current component key as a key into the provided container.
    so if used on instance or class methods, all instances of the same class type
    will have access to the same shared cache storage. if you want to use a cache per
    each instance of a class type, you could use `cached_property` or `cached_method`
    decorators.

    note that if this decorator is used for stand-alone functions, the class type
    part of the generated key will always be None.

    :param function | property old_method_or_property: the original decorated
                                                       method or property.

    :param type[SharedContainer] container: container class type to be used
                                            as cache storage.
                                            if not provided, defaults to
                                            an application level shared
                                            container. it must be a subclass
                                            of `SharedContainer` class.

    :returns: method, property or function result.
    """

    def decorator(method_or_property):
        """
        decorates the given method, property or function and makes it a lazy one.

        :param function | property method_or_property: decorated method, property or function.

        :returns: method, property or function result.
        """

        def wrapper(*args, **kwargs):
            """
            decorates the given method, property or function and makes it a lazy one.

            :param object args: positional arguments of method.
            :keyword object kwargs: keyword arguments of method.

            :returns: method, property or function result.
            """

            storage = container
            if storage is None:
                storage = SharedContainer

            key_provider = TypedKeyProvider(method_or_property, args, kwargs)
            result = storage.get(key_provider.key)
            if result is not None:
                return result

            result = method_or_property(*args, **kwargs)
            storage.set(key_provider.key, result)
            return result

        return update_wrapper(wrapper, method_or_property)

    if len(old_method_or_property) > 0:
        return decorator(old_method_or_property[0])

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
