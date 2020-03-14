# -*- coding: utf-8 -*-
"""
token decorators module.
"""

import pyrin.security.token.services as token_services


def token(*args, **kwargs):
    """
    decorator to register a token handler.

    :param object args: token handler class constructor arguments.
    :param object kwargs: token handler class constructor keyword arguments.

    :keyword bool replace: specifies that if there is another registered
                           handler with the same name, replace it with
                           the new one, otherwise raise an error.
                           defaults to False.

    :raises InvalidTokenHandlerTypeError: invalid token handler type error.
    :raises InvalidTokenHandlerNameError: invalid token handler name error.
    :raises DuplicatedTokenHandlerError: duplicated token handler error.
    :raises DuplicatedTokenKidHeaderError: duplicated token kid header error.

    :returns: token handler class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available token handlers.

        :param type cls: token handler class.

        :returns: token handler class.
        :rtype: type
        """

        instance = cls(*args, **kwargs)
        token_services.register_token_handler(instance, **kwargs)

        return cls

    return decorator
