# -*- coding: utf-8 -*-
"""
alembic decorators module.
"""

import pyrin.database.migration.alembic.services as alembic_services


def alembic_cli_handler(**options):
    """
    decorator to register an alembic cli handler.

    :keyword bool replace: specifies that if there is another registered
                           cli handler with the same name, replace it
                           with the new one, otherwise raise
                           an error. defaults to False.

    :raises InvalidCLIHandlerTypeError: invalid cli handler type error.
    :raises DuplicatedCLIHandlerError: duplicated cli handler error.

    :returns: alembic cli handler class.
    :rtype: AlembicCLIHandlerBase
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available alembic cli handlers.

        :param AlembicCLIHandlerBase cls: alembic cli handler class.

        :returns: alembic cli handler class.
        :rtype: AlembicCLIHandlerBase
        """

        instance = cls()
        alembic_services.register_cli_handler(instance, **options)

        return cls

    return decorator
