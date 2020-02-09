# -*- coding: utf-8 -*-
"""
database migration alembic services module.
"""

from pyrin.application.services import get_component
from pyrin.database.migration.alembic import DatabaseMigrationAlembicPackage


def register_cli_handler(instance, **options):
    """
    registers a new alembic cli handler or replaces the existing one
    if `replace=True` is provided. otherwise, it raises an error
    on adding a cli handler which is already registered.

    :param AlembicCLIHandlerBase instance: alembic cli handler to be registered.
                                           it must be an instance of
                                           AlembicCLIHandlerBase.

    :keyword bool replace: specifies that if there is another registered
                           cli handler with the same name, replace it
                           with the new one, otherwise raise an error.
                           defaults to False.

    :raises InvalidAlembicCLIHandlerTypeError: invalid alembic cli handler type error.
    :raises DuplicatedAlembicCLIHandlerError: duplicated alembic cli handler error.
    """

    get_component(DatabaseMigrationAlembicPackage.COMPONENT_NAME).register_cli_handler(instance,
                                                                                       **options)


def execute(name, **options):
    """
    executes the handler with the given name with given inputs.

    :param str name: handler name tobe executed.

    :raises AlembicCLIHandlerNotFoundError: alembic cli handler not found error.
    """

    get_component(DatabaseMigrationAlembicPackage.COMPONENT_NAME).execute(name, **options)
