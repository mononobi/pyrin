# -*- coding: utf-8 -*-
"""
Packaging manager.
"""

import os

from importlib import import_module

from bshop.settings.packaging import ROOT_DIRECTORY, IGNORED_DIRECTORIES, \
    IGNORED_PACKAGES, IGNORED_MODULES


def load_components():
    """
    Loads required packages and modules for application startup.
    """

    print('Loading application components...')

    packages, modules = _get_loadable_components()

    for package in packages:
        import_module(package)
        print('Package [{package}] loaded.'.format(package=package))

    for module in modules:
        import_module(module)
        print('Module [{module}] loaded.'.format(module=module))

    print('Total of [{count}] packages loaded.'.format(count=len(packages)))
    print('Total of [{count}] modules loaded.'.format(count=len(modules)))


def _get_loadable_components():
    """
    Gets all package and module names that should be loaded.

    :return: (packages, modules)
    :rtype: (list[str], list[str])
    """

    packages = []
    modules = []
    for root, directories, filenames in os.walk(ROOT_DIRECTORY):

        for directory in directories:
            combined_path = os.path.join(root, directory)
            if _is_ignored_directory(directory):
                continue

            if not _is_package(combined_path):
                continue

            package_name = _get_package_name(combined_path)
            if _is_ignored_package(package_name):
                continue

            packages.append(package_name)

            files = os.listdir(combined_path)
            for file_name in files:
                if not _is_module(file_name):
                    continue

                module = file_name.strip('.py')
                if _is_ignored_module(module):
                    continue

                modules.append(_get_module_name(package_name, module))

    return packages, modules


def _is_ignored_directory(directory):
    """
    Gets a value indicating that given directory should be ignored.

    :param str directory: directory name.
                          example directory = `__pycache__`.

    :rtype: bool
    """

    return directory in IGNORED_DIRECTORIES


def _is_ignored_package(package):
    """
    Gets a value indicating that given package should be ignored.

    :param str package: package name.
                        example package = `bshop.core.database`.

    :rtype: bool
    """

    return package in IGNORED_PACKAGES


def _is_ignored_module(module):
    """
    Gets a value indicating that given module should be ignored.

    :param str module: module name.
                       example module = `manager`.

    :rtype: bool
    """

    return module in IGNORED_MODULES


def _get_package_name(path):
    """
    Gets the full package name from provided path.

    :param str path: full path of package.
                     example path = `/home/src/bshop/core/database`.

    :rtype: str
    """

    return path.replace(ROOT_DIRECTORY, '').replace('/', '.')


def _get_module_name(package, module):
    """
    Gets the full module name.

    :param str package: package name.
                        example package = `bshob.core.database`.
    :param str module: module name.
                       example module = `api`.

    :rtype: str
    """

    return '{package}.{module}'.format(package=package, module=module)


def _is_package(path):
    """
    Gets a value indicating that given path belongs to a python package.
    It simply checks that `__init__` module exists or not.

    :param str path: full path of package.
                     example path = `/home/src/bshop/core/database`.

    :rtype: bool
    """

    return _has_module(path, '__init__')


def _is_module(file_name):
    """
    Gets a value indicating that given file is a standalone
    python module (excluding `__init__` module which belongs to package).
    It simply checks that file name ends with '.py' and not being `__init__.py`.

    :param str file_name: file name.
                          example file_name = `services.py`
    :rtype: bool
    """

    return file_name.endswith('.py') and '__init__.py' not in file_name


def _has_module(path, module):
    """
    Gets a value indicating that given module exists in specified path.

    :param str path: path to check module availability in it.
                     example path = `/home/src/bshop/core/database`.
    :param str module: module name.
                       example module = `__init__`.

    :rtype: bool
    """

    return os.path.isfile(os.path.join(path, '{module}.py'.format(module=module)))
