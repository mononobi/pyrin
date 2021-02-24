# -*- coding: utf-8 -*-
"""
model decorators module.
"""

import pyrin.database.services as database_services
import pyrin.database.model.services as model_services


def bind(name, **options):
    """
    decorator to bind a model class to a database.

    :param str name: bind name to associate with the model.

    :raises InvalidEntityTypeError: invalid entity type error.

    :returns: model class.
    :rtype: type[BaseEntity]
    """

    def decorator(cls):
        """
        decorates the given model class and binds it with the specified database.

        :param type[BaseEntity] cls: model class.

        :returns: model class.
        :rtype: type[BaseEntity]
        """

        database_services.register_bind(cls, name, **options)

        return cls

    return decorator


def model_hook():
    """
    decorator to register a model hook.

    :raises InvalidModelHookTypeError: invalid model hook type error.

    :returns: model hook class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available model hooks.

        :param type cls: model hook class.

        :returns: model hook class.
        :rtype: type
        """

        instance = cls()
        model_services.register_hook(instance)

        return cls

    return decorator
