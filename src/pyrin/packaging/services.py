# -*- coding: utf-8 -*-
"""
packaging services module.
"""

from pyrin.packaging import PackagingPackage
from pyrin.application.services import get_component


def load_components(**options):
    """
    loads required packages and modules for application startup.

    :raises BothUnitAndIntegrationTestsCouldNotBeLoadedError: both unit and integration
                                                              tests could not be loaded
                                                              error.
    """

    get_component(PackagingPackage.COMPONENT_NAME).load_components(**options)


def register_hook(instance):
    """
    registers the given instance into packaging hooks.

    :param PackagingHookBase instance: packaging hook instance to be registered.

    :raises InvalidPackagingHookTypeError: invalid packaging hook type error.
    """

    get_component(PackagingPackage.COMPONENT_NAME).register_hook(instance)


def get_working_directory(root_path):
    """
    gets working directory path according to given root path.

    working directory is where the root application and test package are resided.
    this is required when application starts from any of test applications.
    then we should move root path up, to the correct root to be able to
    include real application packages too.
    if the application has been started from real application, this method
    returns the same input.

    :param str root_path: root path to get working directory from.

    :rtype: str
    """

    return get_component(PackagingPackage.COMPONENT_NAME).get_working_directory(root_path)
