# -*- coding: utf-8 -*-
"""
alembic services module.
"""

from pyrin.application.services import get_component
from pyrin.database.migration.alembic import AlembicPackage


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

    :raises InvalidCLIHandlerTypeError: invalid cli handler type error.
    :raises DuplicatedCLIHandlerError: duplicated cli handler error.
    """

    get_component(AlembicPackage.COMPONENT_NAME).register_cli_handler(instance, **options)


def execute(handler_name, **options):
    """
    executes the handler with the given name with given inputs.

    :param str handler_name: handler name to be executed.

    :raises CLIHandlerNotFoundError: cli handler not found error.
    """

    return get_component(AlembicPackage.COMPONENT_NAME).execute(handler_name, **options)


def enable():
    """
    enables migrations for the application.
    """

    return get_component(AlembicPackage.COMPONENT_NAME).enable()


def get_package_class():
    """
    gets the package class of alembic manager.

    :raises PackageClassIsNotSetError: package class is not set error.

    :returns: type[AlembicPackage]
    """

    return get_component(AlembicPackage.COMPONENT_NAME).get_package_class()
