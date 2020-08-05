# -*- coding: utf-8 -*-
"""
caching decorators module.
"""

from functools import update_wrapper

from pyrin.caching.exceptions import NotBoundedToClassError
from pyrin.caching.structs import SharedContainer


def shared_cache(*old_method_or_property, container=None):
    """
    decorator to convert a method or property into a lazy one.

    the method or property result will be calculated once and then it will
    be cached. each result will be cached using a tuple of method or property
    class type and method or property name as a key into the provided container.
    so all instances of the same class type will have access to the same shared
    cache storage. if you want to use a cache per each instance of a class
    type, you could use `cached_property` or `cached_method` decorators.

    note that this decorator could only be used on instance or class methods and properties.
    this decorator does not handle methods that have inputs.

    :param function | property old_method_or_property: the original decorated
                                                       method or property.

    :param type[SharedContainer] container: container class type to be used
                                            as cache storage.
                                            if not provided, defaults to
                                            an application level shared
                                            container. it must be a subclass
                                            of `SharedContainer` class.

    :raises NotBoundedToClassError: not bounded to class error.

    :returns: method or property result.
    """

    def decorator(method_or_property):
        """
        decorates the given method or property and makes it a lazy one.

        :param function | property method_or_property: decorated method or property.

        :returns: method or property result.
        """

        def wrapper(self):
            """
            decorates the given method or property and makes it a lazy one.

            :param object self: the method's parent class instance or type.

            :returns: method or property result.
            """

            storage = container
            if storage is None:
                storage = SharedContainer

            if self is None:
                raise NotBoundedToClassError('"@shared_cache" decorator could only '
                                             'be used on instance or class methods '
                                             'and properties.')

            class_type = self
            method_name = method_or_property.__name__
            if not isinstance(class_type, type):
                class_type = type(class_type)

            key = (class_type, method_name)
            result = storage.get(key)
            if result is not None:
                return result

            result = method_or_property(self)
            storage.set(key, result)
            return result

        return update_wrapper(wrapper, method_or_property)

    if len(old_method_or_property) > 0:
        return decorator(old_method_or_property[0])

    return decorator
