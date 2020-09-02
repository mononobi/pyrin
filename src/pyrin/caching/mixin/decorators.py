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
    it has as few as possible overhead even on single usage.

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
