# -*- coding: utf-8 -*-
"""
model decorators module.
"""

import pyrin.database.services as database_services


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
