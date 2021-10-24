# -*- coding: utf-8 -*-
"""
authentication decorators module.
"""

import pyrin.security.authentication.services as authentication_services


def authenticator(*args, **kwargs):
    """
    decorator to register an authenticator.

    :param object args: authenticator class constructor arguments.
    :param object kwargs: authenticator class constructor keyword arguments.

    :keyword bool replace: specifies that if there is another registered
                           authenticator with the same name, replace it
                           with the new one, otherwise raise an error.
                           defaults to False.

    :raises InvalidAuthenticatorTypeError: invalid authenticator type error.
    :raises DuplicatedAuthenticatorError: duplicated authenticator error.

    :returns: authenticator class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available authenticators.

        :param type cls: authenticator class.

        :returns: authenticator class.
        :rtype: type
        """

        instance = cls(*args, **kwargs)
        authentication_services.register_authenticator(instance, **kwargs)

        return cls

    return decorator
