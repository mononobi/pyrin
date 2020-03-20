# -*- coding: utf-8 -*-
"""
database decorators module.
"""

from functools import update_wrapper

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


def atomic(func):
    """
    decorator to make a function execution atomic.

    meaning that before starting the execution of the function, a new session with a
    new transaction will be started, and after the completion of that function, if it
    was successful, the transaction will be committed or if it was not successful the
    transaction will be rolled-back without the consideration or affecting the parent
    transaction which by default is scoped to request. the corresponding new session
    will also be closed and removed after function execution.

    :param function func: function.

    :returns: function result.
    """

    def decorator(*args, **kwargs):
        """
        decorates the given function and makes its execution atomic.

        :param object args: function arguments.
        :param object kwargs: function keyword arguments.

        :returns: function result.
        """

        store = database_services.get_current_store(True)
        try:
            result = func(*args, **kwargs)
            store.commit()
            return result
        except Exception as ex:
            store.rollback()
            raise ex
        finally:
            factory = database_services.get_current_session_factory()
            factory.remove(True)

    return update_wrapper(decorator, func)
