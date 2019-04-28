# -*- coding: utf-8 -*-
"""
packaging manager module.
"""

import os

from importlib import import_module

from bshop.core.context import CoreObject
from bshop.settings.packaging import IGNORED_MODULES, IGNORED_PACKAGES, \
    IGNORED_DIRECTORIES


class PackagingManager(CoreObject):
    """
    packaging manager class.
    """

    def __init__(self):
        """
        creates a new instance of PackagingManager.
        """

        CoreObject.__init__(self)

        # holds the absolute path of application root directory where
        # the main package is located. for example '/var/app_root/'.
        # this will be resolved automatically by packaging package.
        self._root_directory = ''

    def load_components(self, **options):
        """
        loads required packages and modules for application startup.
        """

        print('Loading application components...')

        packages, modules = self._get_loadable_components(**options)

        for package in packages:
            self.load(package, **options)
            print('[{package}] package loaded.'.format(package=package))

        for module in modules:
            self.load(module, **options)
            print('[{module}] module loaded.'.format(module=module))

        print('Total of [{count}] packages loaded.'.format(count=len(packages)))
        print('Total of [{count}] modules loaded.'.format(count=len(modules)))

    def load(self, module_name, **options):
        """
        loads the specified module.

        :param str module_name: module name.
                                example module_name = `bshop.core.application`.

        :rtype: Module
        """

        return import_module(module_name)

    def _get_loadable_components(self, **options):
        """
        gets all package and module names that should be loaded.

        :returns: tuple(package_names, module_names)

        :rtype: tuple(list[str], list[str])
        """

        self._root_directory = self._resolve_application_root_path(__name__.split('.')[0])

        package_names = []
        module_names = []
        for root, directories, filenames in os.walk(self._root_directory):

            for directory in directories:
                combined_path = os.path.join(root, directory)
                if self._is_ignored_directory(directory):
                    continue

                if not self._is_package(combined_path):
                    continue

                package_name = self._get_package_name(combined_path)
                if self._is_ignored_package(package_name):
                    continue

                package_names.append(package_name)

                files = os.listdir(combined_path)
                for file_name in files:
                    if not self._is_module(file_name):
                        continue

                    module_name = file_name.replace('.py', '')
                    if self._is_ignored_module(module_name):
                        continue

                    module_names.append(self._get_module_name(package_name, module_name))

        return package_names, module_names

    def _is_ignored_directory(self, directory):
        """
        gets a value indicating that given directory should be ignored.

        :param str directory: directory name.
                              example directory = `__pycache__`.

        :rtype: bool
        """

        return directory in IGNORED_DIRECTORIES

    def _is_ignored_package(self, package_name):
        """
        gets a value indicating that given package should be ignored.

        :param str package_name: package name.
                                 example package_name = `bshop.core.database`.

        :rtype: bool
        """

        return package_name in IGNORED_PACKAGES

    def _is_ignored_module(self, module_name):
        """
        gets a value indicating that given module should be ignored.

        :param str module_name: module name.
                                example module_name = `manager`.

        :rtype: bool
        """

        return module_name in IGNORED_MODULES

    def _get_package_name(self, path):
        """
        gets the full package name from provided path.

        :param str path: full path of package.
                         example path = `/home/src/bshop/core/database`.

        :rtype: str
        """

        return path.replace(self._root_directory, '').replace('/', '.')

    def _get_module_name(self, package_name, module_name):
        """
        gets the full module name.

        :param str package_name: package name.
                                 example package_name = `bshob.core.database`.

        :param str module_name: module name.
                                example module_name = `api`.

        :rtype: str
        """

        return '{package}.{module}'.format(package=package_name, module=module_name)

    def _is_package(self, path):
        """
        gets a value indicating that given path belongs to a python package.
        it simply checks that `__init__` module exists or not.

        :param str path: full path of package.
                         example path = `/home/src/bshop/core/database`.

        :rtype: bool
        """

        return self._has_module(path, '__init__')

    def _is_module(self, file_name):
        """
        gets a value indicating that given file is a standalone
        python module (excluding `__init__` module which belongs to package).
        it simply checks that file name ends with '.py' and not being `__init__.py`.

        :param str file_name: file name.
                              example file_name = `services.py`
        :rtype: bool
        """

        return file_name.endswith('.py') and '__init__.py' not in file_name

    def _has_module(self, path, module_name):
        """
        gets a value indicating that given module exists in specified path.

        :param str path: path to check module availability in it.
                         example path = `/home/src/bshop/core/database`.

        :param str module_name: module name.
                                example module_name = `__init__`.

        :rtype: bool
        """

        return os.path.isfile(os.path.join(path, '{module}.py'.format(module=module_name)))

    def _resolve_application_root_path(self, main_package_name):
        """
        gets the application root path which the main package is located.

        :param str main_package_name: application's main package name.
                                      example main_package_name = `bshop`.

        :rtype: str
        """

        main_package = self.load(main_package_name)
        main_package_path = os.path.abspath(main_package.__file__)

        return main_package_path.replace('{package}/__init__.py'.format(package=main_package_name), '')
