# -*- coding: utf-8 -*-
"""
Packaging manager module.
"""

import os
from importlib import import_module

from bshop.settings.packaging import ROOT_DIRECTORY, IGNORED_DIRECTORIES, \
    IGNORED_PACKAGES


def load_packages():
    """
    Loads required packages for application startup.
    """
    packages = _get_loadable_packages()

    for package in packages:
        import_module(package)


def _get_loadable_packages():
    """
    Gets all package names that should be loaded.

    :rtype: list(str)
    """

    packages = []
    for root, directories, filenames in os.walk(ROOT_DIRECTORY):

        for directory in directories:
            if _is_ignored_directory(directory):
                continue

            if not _is_package(os.path.join(root, directory)):
                continue

            package_name = _get_package_name(os.path.join(root, directory))
            if _is_ignored_package(package_name):
                continue

            packages.append(package_name)

    return packages


def _is_ignored_directory(directory):
    """
    Gets a value indicating that given directory should be ignored.
    
    :param str directory: directory name.
                          example directory = `__pycache__`.
    
    :rtype: bool
    """

    return directory in IGNORED_DIRECTORIES


def _is_ignored_package(package_name):
    """
    Gets a value indicating that given package should be ignored.

    :param str package_name: package name.
                             example package_name = `bshop.core.database`.

    :rtype: bool
    """

    return package_name in IGNORED_PACKAGES


def _get_package_name(path):
    """
    Gets the full package name from provided path.

    :param str path: full path of package.
                     example path = `/home/src/bshop/core/database`.

    :rtype: str
    """

    return path.replace(ROOT_DIRECTORY, '').replace('/', '.')


def _is_package(path):
    """
    Gets a value indicating that given path belongs to a python package.
    It simply checks that `__init__` module exists or not.

    :param str path: full path of package.
                     example path = `/home/src/bshop/core/database`.

    :rtype: bool
    """

    return os.path.isfile(os.path.join(path, '__init__.py'))
