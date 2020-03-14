# -*- coding: utf-8 -*-
"""
encryption decorators module.
"""

import pyrin.security.encryption.services as encryption_services


def encrypter(*args, **kwargs):
    """
    decorator to register an encryption handler.

    :param object args: encryption handler class constructor arguments.
    :param object kwargs: encryption handler class constructor keyword arguments.

    :keyword bool replace: specifies that if there is another registered
                           handler with the same name, replace it with
                           the new one, otherwise raise an error.
                           defaults to False.

    :raises InvalidEncryptionHandlerTypeError: invalid encryption handler type error.
    :raises InvalidEncryptionHandlerNameError: invalid encryption handler name error.
    :raises DuplicatedEncryptionHandlerError: duplicated encryption handler error.

    :returns: encryption handler class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available encryption handlers.

        :param type cls: encryption handler class.

        :returns: encryption handler class.
        :rtype: type
        """

        instance = cls(*args, **kwargs)
        encryption_services.register_encryption_handler(instance, **kwargs)

        return cls

    return decorator
