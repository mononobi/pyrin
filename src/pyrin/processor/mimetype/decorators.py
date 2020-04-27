# -*- coding: utf-8 -*-
"""
mimetype decorators module.
"""

import pyrin.processor.mimetype.services as mimetype_services


def mimetype_handler(*args, **kwargs):
    """
    decorator to register a mimetype handler.

    :param object args: mimetype handler class constructor arguments.
    :param object kwargs: mimetype handler class constructor keyword arguments.

    :keyword bool replace: specifies that if there is another registered
                           mimetype handler with the same name and accepted type,
                           replace it with the new one, otherwise raise
                           an error. defaults to False.

    :raises InvalidMIMETypeHandlerTypeError: invalid mimetype handler type error.
    :raises DuplicatedMIMETypeHandlerError: duplicated mimetype handler error.

    :returns: mimetype handler class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available mimetype handlers.

        :param type cls: mimetype handler class.

        :returns: mimetype handler class.
        :rtype: type
        """

        instance = cls(*args, **kwargs)
        mimetype_services.register_mimetype_handler(instance, **kwargs)

        return cls

    return decorator
