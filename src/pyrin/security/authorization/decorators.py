# -*- coding: utf-8 -*-
"""
authorization decorators module.
"""

import pyrin.security.authorization.services as authorization_services


def authorizer(*args, **kwargs):
    """
    decorator to register an authorizer.

    :param object args: authorizer class constructor arguments.
    :param object kwargs: authorizer class constructor keyword arguments.

    :keyword bool replace: specifies that if there is another registered
                           authorizer with the same name, replace it
                           with the new one, otherwise raise an error.
                           defaults to False.

    :raises InvalidAuthorizerTypeError: invalid authorizer type error.
    :raises DuplicatedAuthorizerError: duplicated authorizer error.

    :returns: authorizer class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available authorizer.

        :param type cls: authorizer class.

        :returns: authorizer class.
        :rtype: type
        """

        instance = cls(*args, **kwargs)
        authorization_services.register_authorizer(instance, **kwargs)

        return cls

    return decorator
