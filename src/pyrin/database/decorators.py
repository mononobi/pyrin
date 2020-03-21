# -*- coding: utf-8 -*-
"""
database decorators module.
"""

import pyrin.database.services as database_services


def session_factory(*args, **kwargs):
    """
    decorator to register a database session factory.

    :param object args: session factory class constructor arguments.
    :param object kwargs: session factory class constructor keyword arguments.

    :keyword bool replace: specifies that if there is another registered
                           session factory with the same name, replace it with
                           the new one, otherwise raise an error. defaults to False.

    :raises InvalidSessionFactoryTypeError: invalid session factory type error.
    :raises DuplicatedSessionFactoryError: duplicated session factory error.

    :returns: session factory class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into database session factories.

        :param type cls: session factory class.

        :returns: session factory class.
        :rtype: type
        """

        instance = cls(*args, **kwargs)
        database_services.register_session_factory(instance, **kwargs)

        return cls

    return decorator


def database_hook():
    """
    decorator to register a database hook.

    :raises InvalidDatabaseHookTypeError: invalid database hook type error.

    :returns: database hook class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available database hooks.

        :param type cls: database hook class.

        :returns: database hook class.
        :rtype: type
        """

        instance = cls()
        database_services.register_hook(instance)

        return cls

    return decorator
