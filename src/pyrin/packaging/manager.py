# -*- coding: utf-8 -*-
"""
packaging manager module.
"""

import os
import inspect

from importlib import import_module

import pyrin.application.services as application_services
import pyrin.configuration.services as config_services
import pyrin.utils.configuration as config_utils

from pyrin.core.mixin import HookMixin
from pyrin.packaging import PackagingPackage
from pyrin.core.context import DTO, Manager
from pyrin.packaging.context import Package
from pyrin.packaging.hooks import PackagingHookBase
from pyrin.utils.custom_print import print_info, print_default
from pyrin.utils.path import resolve_application_root_path
from pyrin.packaging.exceptions import InvalidPackageNameError, \
    ComponentModuleNotFoundError


class PackagingManager(Manager, HookMixin):
    """
    packaging manager class.
    """

    PYRIN_PACKAGE_NAME = 'pyrin'
    _hook_type = PackagingHookBase

    def __init__(self):
        """
        creates a new instance of PackagingManager.
        """

        super().__init__()

        # holds the absolute path of application root directory where
        # the main package is located. for example `/var/app_root/`.
        self._root_directory = resolve_application_root_path()

        # holds the loaded packages.
        # `pyrin.application` and `pyrin.packaging` will be loaded at
        # the beginning, so they will not included in this list.
        self._loaded_packages = []

        # holds the instance of all loaded modules.
        # in the form of: {str module_name: Module module}
        self._loaded_modules = DTO()

        # configs will be filled from packaging config file.
        self._configs = DTO()

    def _load_configs(self):
        """
        loads packaging configs from application's settings directory.
        """

        configs = config_utils.load(self._get_config_file_path())
        self._configs = configs.get('general')

    def _get_config_file_path(self):
        """
        gets packaging config file path.

        :rtype: str
        """

        settings_directory = application_services.get_settings_path()
        config_file_name = '{store}.config'.format(store=PackagingPackage.CONFIG_STORE_NAMES[0])
        config_path = os.path.join(settings_directory, config_file_name)

        return os.path.abspath(config_path)

    def _initialize_loaded_packages(self):
        """
        adds `pyrin.application` and `pyrin.packaging` into loaded packages.
        those packages will load immediately and will not be added
        to loaded packages through normal operations.
        """

        for package in self._configs.ignored_packages:
            if package in ('pyrin.application', 'pyrin.packaging'):
                if package not in self._loaded_packages:
                    self._loaded_packages.append(package)

    def load_components(self, **options):
        """
        loads required packages and modules for application startup.
        """

        self._load_configs()
        self._initialize_loaded_packages()

        print_info('Loading application components...')

        pyrin_packages, extended_application_packages, \
            other_application_packages, custom_packages, \
            extended_test_packages, other_test_packages = self._get_loadable_components(**options)

        self._load_components(pyrin_packages, **options)
        self._load_components(extended_application_packages, **options)
        self._load_components(other_application_packages, **options)
        self._load_components(custom_packages, **options)

        if self._configs.load_test_packages is True:
            self._load_components(extended_test_packages, **options)
            self._load_components(other_test_packages, **options)

        self._after_packages_loaded()

        print_info('Total of [{count}] packages loaded.'
                   .format(count=len(self._loaded_packages)))

    def _after_packages_loaded(self):
        """
        this method will call `after_packages_loaded` method of all registered hooks.
        """

        for hook in self._get_hooks():
            hook.after_packages_loaded()

    def load(self, module_name, **options):
        """
        loads the specified module.

        :param str module_name: full module name.
                                example module_name = `pyrin.application.decorators`.

        :rtype: Module
        """

        module = import_module(module_name)
        self._loaded_modules[module.__name__] = module

        return module

    def _load_component(self, package_name, module_names, component_name, **options):
        """
        loads the given component.

        :param str package_name: full package name to be loaded.
        :param list[str] module_names: full module names to be loaded.
        :param str component_name: component name of this package.

        :raises ComponentModuleNotFoundError: component module not found error.
        """

        self.load(package_name)

        # component module should be loaded first if available, in case of
        # any other module needed package services in top level objects.
        component_module = None
        if component_name is not None:
            component_module = self._merge_module_name(package_name, component_name)

        if component_module is not None and component_module in module_names:
            self.load(component_module, **options)
        elif component_module is not None and component_module not in module_names:
            raise ComponentModuleNotFoundError('Component module [{name}] not '
                                               'found in [{package}] package.'
                                               .format(name=component_module,
                                                       package=package_name))

        for module in module_names:
            if module != component_module:
                self.load(module, **options)

        self._loaded_packages.append(package_name)

        print_default('[{package}] package loaded. including [{module_count}] modules.'
                      .format(package=package_name,
                              module_count=len(module_names)))

    def _load_components(self, components, **options):
        """
        loads the given components considering their dependency on each other.

        :param dict components: full package names and their
                                modules to be loaded.

        :type components: dict(str package_name: list[str] modules)
        """

        # a dictionary containing all dependent package names and their respective modules.
        # in the form of {package_name: [modules]}.
        dependent_components = DTO()

        for package in components.keys():
            package_class = self._get_package_class(package)

            # checking whether this package has any dependencies.
            # if so, check those dependencies have been loaded or not.
            # if not, then put this package into dependent_packages and
            # load it later. otherwise load it now.
            if (package_class is None or
                len(package_class.DEPENDS) == 0 or
                self._is_dependencies_loaded(package_class.DEPENDS) is True) and \
               self._is_parent_loaded(package) is True:

                instance = None
                if package_class is not None:
                    instance = package_class()
                    instance.load_configs(config_services)

                component_name = None
                if instance is not None:
                    component_name = instance.COMPONENT_NAME
                self._load_component(package, components[package], component_name, **options)
            else:
                dependent_components[package] = components[package]

        # now, go through dependent components if any, and try to load them.
        if len(dependent_components) > 0:
            self._load_components(dependent_components, **options)

    def _get_loadable_components(self, **options):
        """
        gets all package and module names that should be loaded.

        :returns: tuple(pyrin_components,
                        extended_application_components,
                        other_application_components,
                        custom_components,
                        extended_test_components,
                        other_test_components)

        :type pyrin_components: dict(str package_name: list[str] modules)

        :type extended_application_components: dict(str package_name: list[str] modules)

        :type other_application_components: dict(str package_name: list[str] modules)

        :type custom_components: dict(str package_name: list[str] modules)

        :type extended_test_components: dict(str package_name: list[str] modules)

        :type other_test_components: dict(str package_name: list[str] modules)

        :rtype: tuple
        """

        # a dictionary containing all package names and their respective modules.
        # in the form of {package_name: [modules]}.
        pyrin_components = DTO()
        application_components = DTO()
        custom_components = DTO()
        test_components = DTO()

        for root, directories, file_names in os.walk(self._root_directory, followlinks=True):

            for directory in directories:
                combined_path = os.path.join(root, directory)
                if not self._is_package(combined_path):
                    continue

                package_name = self._get_package_name(combined_path)
                if self._is_ignored_package(package_name):
                    continue

                if self._is_pyrin_package(package_name):
                    pyrin_components[package_name] = []
                elif self._is_custom_package(package_name):
                    custom_components[package_name] = []
                elif self._is_test_package(package_name):
                    test_components[package_name] = []
                else:
                    application_components[package_name] = []

                files = os.listdir(combined_path)
                for file_name in files:
                    if not self._is_module(file_name):
                        continue

                    module_name = file_name.replace('.py', '')
                    full_module_name = self._get_module_name(package_name, module_name)
                    if self._is_ignored_module(full_module_name):
                        continue

                    if self._is_pyrin_module(full_module_name):
                        pyrin_components[package_name].append(full_module_name)
                    elif self._is_custom_module(full_module_name):
                        custom_components[package_name].append(full_module_name)
                    elif self._is_test_module(full_module_name):
                        test_components[package_name].append(full_module_name)
                    else:
                        application_components[package_name].append(full_module_name)

        return self._detach_all(pyrin_components, application_components,
                                custom_components, test_components)

    def _detach_all(self, pyrin_components, application_components,
                    custom_components, test_components):
        """
        detaches all given components into extended and other components.

        :param dict pyrin_components: pyrin components.
        :type pyrin_components: dict(str package_name: list[str] modules)

        :param dict application_components: application components.
        :type application_components: dict(str package_name: list[str] modules)

        :param dict custom_components: custom components.
        :type custom_components: dict(str package_name: list[str] modules)

        :param dict test_components: test components.
        :type test_components: dict(str package_name: list[str] modules)

        :returns: tuple(pyrin_components,
                        extended_application_components,
                        other_application_components,
                        custom_components,
                        extended_test_components,
                        other_test_components)

        :type pyrin_components: dict(str package_name: list[str] modules)

        :type extended_application_components: dict(str package_name: list[str] modules)

        :type other_application_components: dict(str package_name: list[str] modules)

        :type custom_components: dict(str package_name: list[str] modules)

        :type extended_test_components: dict(str package_name: list[str] modules)

        :type other_test_components: dict(str package_name: list[str] modules)

        :rtype: tuple
        """

        extended_application_components, \
            other_application_components = self._detach_extended_packages(
                list(pyrin_components.keys()), application_components)

        test_base_components = application_components
        if len(application_components) <= 0:
            test_base_components = pyrin_components
        extended_test_components, \
            other_test_components = self._detach_extended_packages(
                list(test_base_components.keys()), test_components)

        return pyrin_components, extended_application_components, \
            other_application_components, custom_components, \
            extended_test_components, other_test_components

    def _detach_extended_packages(self, base_components, components):
        """
        detaches components which extend existing base components
        from those which are new components.

        :param list[str] base_components: base component names.

        :param dict components: components which some of
                                them extend base components.

        :type components: dict(str package_name: list[str] modules)

        :returns: tuple(extended_components, other_components)

        :type extended_components: dict(str package_name: list[str] modules)
        :type other_components: dict(str package_name: list[str] modules)

        :rtype: tuple
        """

        extended_components = DTO()
        other_components = DTO()
        if len(components) > 0:
            component_keys = list(components.keys())
            root_name = self._get_root_package(component_keys[0])
            base_names = [self._replace_root_package(item, root_name) for item in base_components]
            for package in components:
                if package in base_names:
                    extended_components[package] = components[package]
                else:
                    other_components[package] = components[package]

        return extended_components, other_components

    def _replace_root_package(self, old_package, root_name):
        """
        replaces root package name in old package with given root name.

        :param str old_package: old package fully qualified name.
                                in the form of: `pyrin.api`

        :param str root_name: root name to be put in old package name.
                              in the form of: `my_root`
        :rtype: str
        """

        parts = old_package.split('.')
        parts.pop(0)
        parts.insert(0, root_name)

        return '.'.join(parts)

    def _get_root_package(self, component_name):
        """
        gets the root package of given component.

        :param str component_name: full package or module name.

        :rtype: str
        """

        return component_name.split('.')[0]

    def _is_ignored_package(self, package_name):
        """
        gets a value indicating that given package should be ignored.

        :param str package_name: full package name.
                                 example package_name = `pyrin.database`.

        :rtype: bool
        """

        for ignored in self._configs.ignored_packages:
            if package_name.startswith(ignored):
                return True

        return False

    def _is_ignored_module(self, module_name):
        """
        gets a value indicating that given module should be ignored.

        :param str module_name: full module name.
                                example module_name = `pyrin.api.error_handlers`.

        :rtype: bool
        """

        for ignored in self._configs.ignored_modules:
            if module_name.endswith(ignored):
                return True

        return False

    def _is_pyrin_component(self, component_name):
        """
        gets a value indicating that given component is a pyrin component.

        :param str component_name: full package or module name.

        :rtype: bool
        """

        return self._contains(self.PYRIN_PACKAGE_NAME, component_name)

    def _is_pyrin_package(self, package_name):
        """
        gets a value indicating that given package is a pyrin package.

        :param str package_name: full package name.
                                 example package_name = 'pyrin.api'

        :rtype: bool
        """

        return self._is_pyrin_component(package_name)

    def _is_pyrin_module(self, module_name):
        """
        gets a value indicating that given module is a pyrin module.

        :param str module_name: full module name.
                                example module_name = 'pyrin.api.error_handlers'

        :rtype: bool
        """

        return self._is_pyrin_component(module_name)

    def _is_custom_component(self, component_name):
        """
        gets a value indicating that given component is a custom component.

        :param str component_name: full package or module name.

        :rtype: bool
        """

        for custom in self._configs.custom_packages:
            if self._contains(custom, component_name) is True:
                return True

        return False

    def _is_custom_package(self, package_name):
        """
        gets a value indicating that given package is a custom package.

        :param str package_name: full package name.
                                 example package_name = 'custom.api'

        :rtype: bool
        """

        return self._is_custom_component(package_name)

    def _is_custom_module(self, module_name):
        """
        gets a value indicating that given module is a custom module.

        :param str module_name: full module name.
                                example module_name = 'custom.api.error_handlers'

        :rtype: bool
        """

        return self._is_custom_component(module_name)

    def _is_test_component(self, component_name):
        """
        gets a value indicating that given component is a test component.

        :param str component_name: full package or module name.

        :rtype: bool
        """

        for test in self._configs.test_packages:
            if self._contains(test, component_name) is True:
                return True

        return False

    def _is_test_package(self, package_name):
        """
        gets a value indicating that given package is a test package.

        :param str package_name: full package name.
                                 example package_name = 'test.api'

        :rtype: bool
        """

        return self._is_test_component(package_name)

    def _is_test_module(self, module_name):
        """
        gets a value indicating that given module is a test module.

        :param str module_name: full module name.
                                example module_name = 'test.api.error_handlers'

        :rtype: bool
        """

        return self._is_test_component(module_name)

    def _contains(self, root, component_name):
        """
        gets a value indicating that given component
        qualified name, is belonging to the provided root.

        :param str root: root name that should be checked for component existence.
                         example root = `application.custom`

        :param str component_name: component name that should be
                                   checked for existence in root.
                                   example component_name = `application.custom.api`

        :rtype: bool
        """

        parts_component = component_name.split('.')
        parts_root = root.split('.')
        if len(parts_component) < len(parts_root):
            return False

        component_root = '.'.join(parts_component[0:len(parts_root)])

        return component_root == root

    def _get_package_name(self, path):
        """
        gets the full package name from provided path.

        :param str path: full path of package.
                         example path = `/home/src/pyrin/database`.

        :rtype: str
        """

        return path.replace(self._root_directory, '').replace('/', '.')

    def _merge_module_name(self, package_name, component_name):
        """
        merges package and component name and gets the fully qualified module name.

        :param str package_name: package name.
                                 example package_name = `pyrin.database`.

        :param str component_name: component name.
                                   example component_name = `database.component`.

        :rtype: str
        """

        parts = component_name.split('.')
        return self._get_module_name(package_name, parts[-1])

    def _get_module_name(self, package_name, module_name):
        """
        gets the full module name.

        :param str package_name: package name.
                                 example package_name = `pyrin.database`.

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
                         example path = `/home/src/pyrin/database`.

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
                         example path = `/home/src/pyrin/database`.

        :param str module_name: module name.
                                example module_name = `__init__`.

        :rtype: bool
        """

        return os.path.isfile(os.path.join(path, '{module}.py'.format(module=module_name)))

    def _get_package_class(self, package_name):
        """
        gets the package class implemented in given package if available, otherwise returns None.

        :param str package_name: full package name.
                                 example package_name = `pyrin.api`.

        :rtype: type
        """

        module = self.load(package_name)
        package_class = None

        for cls in module.__dict__.values():
            if inspect.isclass(cls) and cls is not Package and issubclass(cls, Package):
                package_class = cls
        return package_class

    def _is_dependencies_loaded(self, dependencies):
        """
        gets a value indicating that given dependencies has been already loaded.

        :param list[str] dependencies: full dependency names.
                                       example dependencies = `pyrin.logging`

        :rtype: bool
        """

        for dependency in dependencies:
            if dependency not in self._loaded_packages:
                return False

        return True

    def _is_parent_loaded(self, package_name):
        """
        gets a value indicating that given package's parent package has been loaded.

        :param str package_name: full package name.
                                 example package_name = `pyrin.encryption.handlers`

        :raises InvalidPackageNameError: invalid package name error.

        :rtype: bool
        """

        items = package_name.split('.')
        parent_package = None

        length = len(items)
        if length == 1:
            parent_package = items[0]
        elif length > 1:
            parent_package = '.'.join(items[:-1])
        else:
            raise InvalidPackageNameError('Input package name [{package_name}] is invalid.'
                                          .format(package_name=package_name))

        # application root packages like `pyrin`, has no
        # parent so it should always return `True` for them.
        if parent_package == package_name:
            return True

        return self._is_dependencies_loaded([parent_package])
