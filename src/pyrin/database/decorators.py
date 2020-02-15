# -*- coding: utf-8 -*-
"""
database decorators module.
"""

from functools import update_wrapper

import pyrin.database.services as database_services

from pyrin.database.services import get_current_store


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
        of it into available database session factories.

        :param type cls: session factory class.

        :returns: session factory class.

        :rtype: type
        """

        instance = cls(*args, **kwargs)
        database_services.register_session_factory(instance, **kwargs)

        return cls

    return decorator


def bind(name, **options):
    """
    decorator to bind a model class to a database.

    :param str name: bind name to associate with the model.

    :raises InvalidEntityTypeError: invalid entity type error.

    :returns: model class.

    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given model class and binds it with the specified database.

        :param type cls: model class.

        :returns: model class.

        :rtype: type
        """

        database_services.register_bind(cls, name, **options)

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
    meaning that before starting the execution of the function, a sub-transaction
    will be started, and after the completion of that function, if it was successful,
    the sub-transaction will be committed or if it was not successful the sub-transaction
    will be rolled-back without the consideration or affecting the parent transaction
    which by default is scoped to request.

    :param callable func: function.

    :returns: function result.
    """

    def decorator(*args, **kwargs):
        """
        decorates the given function and makes its execution atomic.

        :param object args: function arguments.
        :param object kwargs: function keyword arguments.

        :returns: function result.
        """

        store = get_current_store()
        transaction = store.begin_nested()
        try:
            result = func(*args, **kwargs)
            transaction.commit()
            return result
        except Exception as ex:
            if transaction is not None:
                transaction.rollback()
            raise ex

    return update_wrapper(decorator, func)
