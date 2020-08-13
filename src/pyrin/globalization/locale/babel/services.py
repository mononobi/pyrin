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


def enable(include_pyrin=True, include_app=True):
    """
    enables locale management for the application.

    :param bool include_pyrin: specifies that it should extract pyrin localizable
                               messages. defaults to True if not provided.

    :param bool include_app: specifies that it should extract application
                             localizable messages. defaults to True if not provided.
    """

    return get_component(BabelPackage.COMPONENT_NAME).enable(include_pyrin, include_app)


def rebuild(include_pyrin=True, include_app=True, locale=None):
    """
    it will do the three complete steps needed to
    update and compile locales with new messages.

    it will do:
        1. extract
        2. update
        3. compile

    this command is defined for convenient of usage, but if you need
    to do these steps separately, you could ignore this command and
    use the relevant command for each step.

    :keyword bool include_pyrin: specifies that it must extract pyrin localizable
                                 messages as well. defaults to True if not provided.

    :keyword bool include_app: specifies that it must extract application localizable
                               messages as well. defaults to True if not provided.

    :keyword str locale: locale name of the catalog to compile.
                         it will compile all catalogs if not provided.
    """

    return get_component(BabelPackage.COMPONENT_NAME).rebuild(include_pyrin,
                                                              include_app, locale)


def check_init(locale):
    """
    checks that locale with given name does not exist.

    :param str locale: locale name for the new localized catalog.
                       for example: `en` or `fr` or ...

    :raises LocaleAlreadyExistedError: locale already existed error.
    """

    return get_component(BabelPackage.COMPONENT_NAME).check_init(locale)


def get_package_class():
    """
    gets the package class of babel manager.

    :raises PackageClassIsNotSetError: package class is not set error.

    :returns: type[BabelPackage]
    """

    return get_component(BabelPackage.COMPONENT_NAME).get_package_class()
