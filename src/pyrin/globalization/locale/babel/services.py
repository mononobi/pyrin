# -*- coding: utf-8 -*-
"""
babel services module.
"""

from pyrin.application.services import get_component
from pyrin.globalization.locale.babel import BabelPackage


def register_cli_handler(instance, **options):
    """
    registers a new babel cli handler or replaces the existing one
    if `replace=True` is provided. otherwise, it raises an error
    on adding a cli handler which is already registered.

    :param BabelCLIHandlerBase instance: babel cli handler to be registered.
                                         it must be an instance of
                                         BabelCLIHandlerBase.

    :keyword bool replace: specifies that if there is another registered
                           cli handler with the same name, replace it
                           with the new one, otherwise raise an error.
                           defaults to False.

    :raises InvalidCLIHandlerTypeError: invalid cli handler type error.
    :raises DuplicatedCLIHandlerError: duplicated cli handler error.
    """

    get_component(BabelPackage.COMPONENT_NAME).register_cli_handler(instance, **options)


def execute(handler_name, **options):
    """
    executes the handler with the given name with given inputs.

    :param str handler_name: handler name to be executed.

    :raises CLIHandlerNotFoundError: cli handler not found error.
    """

    return get_component(BabelPackage.COMPONENT_NAME).execute(handler_name, **options)