# -*- coding: utf-8 -*-
"""
hashing decorators module.
"""

import pyrin.security.hashing.services as hashing_services


def hashing(*args, **kwargs):
    """
    decorator to register a hashing handler.

    :param object args: hashing handler class constructor arguments.
    :param object kwargs: hashing handler class constructor keyword arguments.

    :keyword bool replace: specifies that if there is another registered
                           handler with the same name, replace it with
                           the new one, otherwise raise an error.
                           defaults to False.

    :raises InvalidHashingHandlerTypeError: invalid hashing handler type error.
    :raises InvalidHashingHandlerNameError: invalid hashing handler name error.
    :raises DuplicatedHashingHandlerError: duplicated hashing handler error.

    :returns: hashing handler class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available hashing handlers.

        :param type cls: hashing handler class.

        :returns: hashing handler class.
        :rtype: type
        """

        instance = cls(*args, **kwargs)
        hashing_services.register_hashing_handler(instance, **kwargs)

        return cls

    return decorator
