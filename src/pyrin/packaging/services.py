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
    :raises PackageIsIgnoredError: package is ignored error.
    :raises PackageIsDisabledError: package is disabled error.
    :raises PackageNotExistedError: package not existed error.
    :raises SelfDependencyDetectedError: self dependency detected error.
    :raises SubPackageDependencyDetectedError: sub-package dependency detected error.
    :raises CircularDependencyDetectedError: circular dependency detected error.
    :raises PackageExternalDependencyError: package external dependency error.
    """

    get_component(PackagingPackage.COMPONENT_NAME).load_components(**options)


def load(module_name, **options):
    """
    loads the specified module.

    :param str module_name: full module name.
                            example module_name = `pyrin.application.decorators`.

    :rtype: Module
    """

    return get_component(PackagingPackage.COMPONENT_NAME).load(module_name, **options)


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


def get_loaded_packages():
    """
    gets the name of all loaded packages.

    :rtype: list[str]
    """

    return get_component(PackagingPackage.COMPONENT_NAME).get_loaded_packages()


def is_package_loaded(name):
    """
    gets a value indicating that given package is loaded.

    :param str name: package fully qualified name.

    :rtype: bool
    """

    return get_component(PackagingPackage.COMPONENT_NAME).is_package_loaded(name)
