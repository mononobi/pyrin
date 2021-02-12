# -*- coding: utf-8 -*-
"""
packaging manager module.
"""

import os
import inspect

from threading import Lock
from importlib import import_module
from time import time

import pyrin.application.services as application_services
import pyrin.configuration.services as config_services
import pyrin.utils.configuration as config_utils
import pyrin.utils.path as path_utils
import pyrin.utils.environment as env_utils
import pyrin.utils.misc as misc_utils

from pyrin.core.mixin import HookMixin
from pyrin.packaging import PackagingPackage
from pyrin.core.structs import DTO, Manager
from pyrin.packaging.base import Package
from pyrin.packaging.enumerations import PackageScopeEnum
from pyrin.packaging.hooks import PackagingHookBase
from pyrin.utils.custom_print import print_info, print_default
from pyrin.packaging.exceptions import InvalidPackageNameError, \
    ComponentModuleNotFoundError, BothUnitAndIntegrationTestsCouldNotBeLoadedError, \
    InvalidPackagingHookTypeError, CircularDependencyDetectedError, PackageNotExistedError, \
    PackageIsIgnoredError, PackageIsDisabledError, SelfDependencyDetectedError, \
    SubPackageDependencyDetectedError, PackageExternalDependencyError


class PackagingManager(Manager, HookMixin):
    """
    packaging manager class.
    """

    _lock = Lock()
    hook_type = PackagingHookBase
    invalid_hook_type_error = InvalidPackagingHookTypeError
    package_class = PackagingPackage
    REQUIRED_PACKAGES = ('application', 'packaging')

    def __init__(self):
        """
        creates a new instance of PackagingManager.
        """

        super().__init__()

        # this flag indicates that application has been loaded.
        # it is required for environments in which server starts
        # multiple threads before application gets loaded.
        self._is_loaded = False

        self._pyrin_package_name = None
        self._required_packages = []

        # holds the names of all application packages that should be loaded.
        self._all_packages = []

        # holds the name of loaded packages.
        self._loaded_packages = []

        # holds the name of disabled packages.
        self._disabled_packages = []

        # a dict containing each package name and all of its dependency package names.
        # in the form of:
        # {str package_name: list[str dependency_package_name]}
        self._dependency_map = DTO()

        # holds the full path of directories that are not a package (not having __init__.py)
        self._not_packages = []

        # configs will be filled from packaging config file.
        self._configs = DTO()

        # holds the root package names in which all test packages are resided.
        self._test_roots = []

        # holds the base roots for different test root packages.
        self._test_roots_bases = []

        # these will keep all loaded components for different
        # categories inside them. extended components in each
        # category are those that extending the exact component
        # of their parent.
        # in the form of: dict[str package_name: list[str] modules]
        self._pyrin_components = DTO()
        self._application_components = DTO()
        self._custom_components = DTO()
        self._test_components = DTO()
        self._unit_test_components = DTO()
        self._integration_test_components = DTO()
        self._extended_application_components = DTO()
        self._other_application_components = DTO()
        self._extended_unit_test_components = DTO()
        self._other_unit_test_components = DTO()
        self._extended_integration_test_components = DTO()
        self._other_integration_test_components = DTO()

    def _create_config_file(self):
        """
        creates packaging config file in application settings path if not available.
        """

        config_services.create_config_file(self.package_class.CONFIG_STORE_NAMES[0],
                                           ignore_on_existed=True)

    def _load_configs(self):
        """
        loads packaging configs from application's settings directory.
        """

        self._configs.clear()
        configs = config_utils.load(self._get_config_file_path())
        self._configs = configs.get('general')
        self._extract_test_roots()

    def _get_config_file_path(self):
        """
        gets packaging config file path.

        it looks for file in top level application settings, but
        if not found it, it uses the file from default settings.
        we have to re-implement this here, because configuration
        services is not present yet to be used.

        :rtype: str
        """

        app_settings_directory = application_services.get_settings_path()
        pyrin_settings_directory = application_services.get_default_settings_path()
        config_file_name = '{store}.ini'.format(store=self.package_class.
                                                CONFIG_STORE_NAMES[0])
        config_path = path_utils.get_first_available_file(app_settings_directory,
                                                          pyrin_settings_directory,
                                                          file_name=config_file_name)

        return config_path

    def _initialize(self):
        """
        initializes required data.
        """

        self._disabled_packages.clear()
        self._not_packages.clear()
        self._dependency_map.clear()
        self._all_packages.clear()
        self._loaded_packages.clear()
        self._required_packages.clear()
        self._pyrin_components.clear()
        self._application_components.clear()
        self._custom_components.clear()
        self._test_components.clear()
        self._unit_test_components.clear()
        self._integration_test_components.clear()
        self._extended_application_components.clear()
        self._other_application_components.clear()
        self._extended_unit_test_components.clear()
        self._other_unit_test_components.clear()
        self._extended_integration_test_components.clear()
        self._other_integration_test_components.clear()

        self._pyrin_package_name = path_utils.get_pyrin_main_package_name()
        self._load_required_packages(self._pyrin_package_name)
        self._load_configs()
        self._resolve_python_path()

    def _load_required_packages(self, pyrin_package):
        """
        loads all required package names.

        these packages are always loaded before any other package and
        they do not need to be handled by packaging package itself.

        :param str pyrin_package: the name of pyrin package.
                                  it would always be `pyrin` in normal cases.
        """

        for item in self.REQUIRED_PACKAGES:
            full_name = '{pyrin}.{package}'.format(pyrin=pyrin_package,
                                                   package=item)
            self._required_packages.append(full_name)
            self._loaded_packages.append(full_name)
            self._all_packages.append(full_name)

    def _extract_test_roots(self):
        """
        extracts the root package names in which all test packages are resided.
        """

        self._test_roots.clear()
        self._test_roots_bases.clear()

        unit = self._configs.unit_test_package
        integration = self._configs.integration_test_package

        if unit not in (None, '') and not unit.isspace():
            unit_root = unit.split('.')
            if len(unit_root) > 1:
                unit_root.pop()

            self._test_roots.append('.'.join(unit_root))
            self._test_roots_bases.append(unit_root[0])

        if integration not in (None, '') and not integration.isspace():
            integration_root = integration.split('.')
            if len(integration_root) > 1:
                integration_root.pop()

            value = '.'.join(integration_root)
            if value not in self._test_roots:
                self._test_roots.append(value)

            if integration_root[0] not in self._test_roots_bases:
                self._test_roots_bases.append(integration_root[0])

    def load_components(self, **options):
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

        if self._is_loaded is True:
            return

        with self._lock:
            if self._is_loaded is True:
                return

            start_time = time()
            self._initialize()

            print_info('Loading application components...')

            self._find_pyrin_loadable_components()
            self._find_other_loadable_components()

            self._load_components(self._pyrin_components, **options)
            self._load_components(self._extended_application_components, **options)
            self._load_components(self._other_application_components, **options)
            self._load_components(self._custom_components, **options)
            self._load_tests(**options)

            self._after_packages_loaded()

            print_info('Total of [{count}] packages loaded.'
                       .format(count=len(self._loaded_packages)))

            self._create_config_file()
            self._is_loaded = True
            end_time = time()
            duration = '{:0.1f}'.format((end_time - start_time) * 1000)
            print_info('Application loaded in [{duration}] milliseconds.'
                       .format(duration=duration))

            pyrin_version = application_services.get_pyrin_version()
            print_info('Pyrin version: [{version}].'.format(version=pyrin_version))

    def _load_tests(self, **options):
        """
        loads test packages if needed.

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

        if self._configs.load_unit_test is True and \
                self._configs.load_integration_test is True:
            raise BothUnitAndIntegrationTestsCouldNotBeLoadedError('Both unit and '
                                                                   'integration tests '
                                                                   'could not be loaded '
                                                                   'at the same time.')

        if self._configs.load_unit_test is True or \
                self._configs.load_integration_test is True:
            self._load_components(self._test_components, **options)

            if self._configs.load_unit_test is True:
                self._load_components(self._extended_unit_test_components, **options)
                self._load_components(self._other_unit_test_components, **options)

            elif self._configs.load_integration_test is True:
                self._load_components(self._extended_integration_test_components, **options)
                self._load_components(self._other_integration_test_components, **options)

    def _after_packages_loaded(self):
        """
        this method will call `after_packages_loaded` method of all registered hooks.
        """

        for hook in self._get_hooks():
            hook.after_packages_loaded()

    def _package_loaded(self, package_name, **options):
        """
        this method will call `package_loaded` method of all registered hooks.

        :param str package_name: name of the loaded package.
        """

        for hook in self._get_hooks():
            hook.package_loaded(package_name, **options)

    def load(self, module_name, **options):
        """
        loads the specified module.

        :param str module_name: full module name.
                                example module_name = `pyrin.application.decorators`.

        :rtype: Module
        """

        module = import_module(module_name)
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
        self._package_loaded(package_name, **options)

        print_default('[{package}] package loaded. including [{module_count}] modules.'
                      .format(package=package_name,
                              module_count=len(module_names)))

        if package_name == self._pyrin_package_name:
            for item in self._required_packages:
                print_default('[{package}] package loaded.'
                              .format(package=item))

    def _load_components(self, components, **options):
        """
        loads the given components considering their dependency on each other.

        :param dict components: full package names and their
                                modules to be loaded.

        :note components: dict[str package_name: list[str] modules]

        :raises PackageIsIgnoredError: package is ignored error.
        :raises PackageIsDisabledError: package is disabled error.
        :raises PackageNotExistedError: package not existed error.
        :raises SelfDependencyDetectedError: self dependency detected error.
        :raises SubPackageDependencyDetectedError: sub-package dependency detected error.
        :raises CircularDependencyDetectedError: circular dependency detected error.
        :raises PackageExternalDependencyError: package external dependency error.
        """

        # a dictionary containing all dependent package names and their respective modules.
        # in the form of {str package_name: [str module]}.
        dependent_components = DTO()

        for package in components:
            dependencies = []
            package_class = self._get_package_class(package)
            if package_class is not None:
                dependencies = package_class.DEPENDS

            self._validate_dependencies(package, dependencies)

            # checking whether this package has any dependencies.
            # if so, check those dependencies have been loaded or not.
            # if not, then put this package into dependent_packages and
            # load it later. otherwise load it now.
            if (len(dependencies) <= 0 or
                self._is_dependencies_loaded(dependencies) is True) and \
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

    def _validate_dependencies(self, package_name, dependencies):
        """
        validates that given package's dependencies have no problem.

        it checks for different problems such as self and circular
        dependencies, unavailable dependencies, external dependencies and more.

        it raises an error if a problem has been detected.
        for example, if `pyrin.database` has a dependency on `pyrin.logging`
        and `pyrin.logging` also has a dependency on `pyrin.database`, this
        method raises an error.

        :param str package_name: package name.
        :param list[str] dependencies: list of given package's dependencies.

        :raises PackageIsIgnoredError: package is ignored error.
        :raises PackageIsDisabledError: package is disabled error.
        :raises PackageNotExistedError: package not existed error.
        :raises SelfDependencyDetectedError: self dependency detected error.
        :raises SubPackageDependencyDetectedError: sub-package dependency detected error.
        :raises CircularDependencyDetectedError: circular dependency detected error.
        :raises PackageExternalDependencyError: package external dependency error.
        """

        dependencies = misc_utils.make_iterable(dependencies, list)
        self._check_dependencies_exist(package_name, dependencies)

        self._dependency_map[package_name] = dependencies
        if len(dependencies) <= 0:
            return

        if package_name in dependencies:
            raise SelfDependencyDetectedError('Package [{source}] has a dependency on itself. '
                                              'it is a mistake to depend a package on itself.'
                                              .format(source=package_name))

        for item in dependencies:
            if self._contains(package_name, item) is True:
                raise SubPackageDependencyDetectedError('Package [{root}] has a dependency on '
                                                        'its sub-package [{child}]. it is a '
                                                        'mistake to depend a package on its '
                                                        'own sub-packages.'
                                                        .format(root=package_name, child=item))

            reverse_dependencies = self._dependency_map.get(item)
            if reverse_dependencies is not None:
                if package_name in reverse_dependencies:
                    raise CircularDependencyDetectedError('There is a circular dependency '
                                                          'between [{source}] and [{reverse}] '
                                                          'packages.'
                                                          .format(source=package_name,
                                                                  reverse=item))

            if self._is_valid_external_dependency(package_name, item) is False:
                raise PackageExternalDependencyError('Package [{source}] has a dependency '
                                                     'on package [{other}] which is from '
                                                     'an outer scope. a package could not be '
                                                     'dependent on outer scope packages.'
                                                     .format(source=package_name,
                                                             other=item))

    def _check_dependencies_exist(self, package_name, dependencies):
        """
        checks that given dependency packages are available in the application scope.

        :param str package_name: package name.
        :param list[str] dependencies: list of given package's dependencies.

        :raises PackageIsIgnoredError: package is ignored error.
        :raises PackageIsDisabledError: package is disabled error.
        :raises PackageNotExistedError: package not existed error.
        """

        if dependencies is None:
            return

        for item in dependencies:
            if item not in self._all_packages:
                base_message = 'Provided dependency package [{name}] ' \
                               'specified in [{source}] package,' \
                    .format(name=item, source=package_name)

                if self._is_ignored_package(item):
                    raise PackageIsIgnoredError('{base_message} is ignored in '
                                                'packaging config store.'
                                                .format(base_message=base_message))
                if self._is_disabled_package(item):
                    raise PackageIsDisabledError('{base_message} is disabled.'
                                                 .format(base_message=base_message))

                raise PackageNotExistedError('{base_message} does not exist.'
                                             .format(base_message=base_message))

    def _is_valid_external_dependency(self, package_name, dependency):
        """
        gets a value indicating that given dependency package is a valid external dependency.

        a package could not be dependent on external scope packages.
        for example `pyrin.database` package could not be dependent on
        `my_app.database` package which is from outer scope.

        note that a package could be dependent on another package from inner
        scopes, although it is nonsense. so a package like `my_app.database`
        could be dependent on `pyrin.database` but it is not required to put this
        dependency in package info because the `pyrin.database` package is always
        gets loaded before any package of outer scope application gets loaded.

        :param str package_name: package name to check its dependency.
        :param str dependency: dependency package name to be checked.

        :rtype: bool
        """

        package_scope = self._get_package_scope(package_name)
        dependency_scope = self._get_package_scope(dependency)

        if package_scope == PackageScopeEnum.UNKNOWN or \
                dependency_scope == PackageScopeEnum.UNKNOWN:
            return False

        if (self._is_unit_test_scope(package_scope) and
            self._is_integration_test_scope(dependency_scope)) or \
                (self._is_integration_test_scope(package_scope) and
                 self._is_unit_test_scope(dependency_scope)):
            return False

        return dependency_scope <= package_scope

    def _is_integration_test_scope(self, scope):
        """
        gets a value indicating that given value belongs to any of integration test scopes.

        :param int scope: the scope to be checked.
        :enum scope:
            PYRIN = 0
            EXTENDED_APPLICATION = 1
            OTHER_APPLICATION = 2
            CUSTOM_APPLICATION = 3
            TEST = 4
            EXTENDED_UNIT_TEST = 5
            OTHER_UNIT_TEST = 6
            EXTENDED_INTEGRATION_TEST = 7
            OTHER_INTEGRATION_TEST = 8
            UNKNOWN = 100

        :rtype: bool
        """

        return scope in (PackageScopeEnum.OTHER_INTEGRATION_TEST,
                         PackageScopeEnum.EXTENDED_INTEGRATION_TEST)

    def _is_unit_test_scope(self, scope):
        """
        gets a value indicating that given value belongs to any of unit test scopes.

        :param int scope: the scope to be checked.
        :enum scope:
            PYRIN = 0
            EXTENDED_APPLICATION = 1
            OTHER_APPLICATION = 2
            CUSTOM_APPLICATION = 3
            TEST = 4
            EXTENDED_UNIT_TEST = 5
            OTHER_UNIT_TEST = 6
            EXTENDED_INTEGRATION_TEST = 7
            OTHER_INTEGRATION_TEST = 8
            UNKNOWN = 100

        :rtype: bool
        """

        return scope in (PackageScopeEnum.OTHER_UNIT_TEST,
                         PackageScopeEnum.EXTENDED_UNIT_TEST)

    def _get_package_scope(self, package_name):
        """
        gets the scope of given package.

        :param str package_name: package name to get its scope.

        :returns: the scope of given package.
        :enum scope:
            PYRIN = 0
            EXTENDED_APPLICATION = 1
            OTHER_APPLICATION = 2
            CUSTOM_APPLICATION = 3
            TEST = 4
            EXTENDED_UNIT_TEST = 5
            OTHER_UNIT_TEST = 6
            EXTENDED_INTEGRATION_TEST = 7
            OTHER_INTEGRATION_TEST = 8
            UNKNOWN = 100

        :rtype: int
        """

        if self._is_pyrin_package(package_name) is True:
            return PackageScopeEnum.PYRIN

        if self._is_extended_application_package(package_name) is True:
            return PackageScopeEnum.EXTENDED_APPLICATION

        if self._is_other_application_package(package_name) is True:
            return PackageScopeEnum.OTHER_APPLICATION

        if self._is_custom_package(package_name) is True:
            return PackageScopeEnum.CUSTOM_APPLICATION

        if self._is_test_package(package_name) is True:
            return PackageScopeEnum.TEST

        if self._is_extended_unit_test_package(package_name) is True:
            return PackageScopeEnum.EXTENDED_UNIT_TEST

        if self._is_other_unit_test_package(package_name) is True:
            return PackageScopeEnum.OTHER_UNIT_TEST

        if self._is_extended_integration_test_package(package_name) is True:
            return PackageScopeEnum.EXTENDED_INTEGRATION_TEST

        if self._is_other_integration_test_package(package_name) is True:
            return PackageScopeEnum.OTHER_INTEGRATION_TEST

        return PackageScopeEnum.UNKNOWN

    def _find_pyrin_loadable_components(self):
        """
        finds all package and module names that should be loaded from pyrin package.
        """

        pyrin_root_path = application_services.get_pyrin_root_path()
        pyrin_path = application_services.get_pyrin_main_package_path()
        self._find_loadable_components(pyrin_root_path, include=pyrin_path)

    def _find_other_loadable_components(self):
        """
        finds all package and module names that should be loaded from other packages.

        for example application and tests.
        """

        application_root_path = application_services.get_application_root_path()
        working_directory = self.get_working_directory(application_root_path)
        pyrin_path = application_services.get_pyrin_main_package_path()
        self._find_loadable_components(working_directory, exclude=pyrin_path)

    def get_working_directory(self, root_path):
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

        roots = tuple(item.replace('.', os.path.sep) for item in self._test_roots)
        if len(roots) > 0:
            for item in roots:
                if root_path.endswith(item):
                    return root_path.replace(item, '').rstrip(os.path.sep)

        return root_path

    def _resolve_python_path(self):
        """
        resolves python path to put in `PYTHONPATH` variable.
        """

        application_root_path = application_services.get_application_root_path()
        env_utils.set_python_path(self.get_working_directory(application_root_path))

    def _find_loadable_components(self, root_path, include=None,
                                  exclude=None, **options):
        """
        finds all package and module names that should be loaded included in given root path.

        :param str root_path: root path to look for components inside it.

        :param str | list[str] include: specify full directory names inside the
                                        root path to just loop inside those.
                                        otherwise it loops in all available
                                        directories.

        :param str | list[str] exclude: specify full directory names inside the
                                        root path to ignore them. otherwise
                                        it loops in all available directories.
        """

        include = misc_utils.make_iterable(include, list)
        exclude = misc_utils.make_iterable(exclude, list)

        for root, directories, file_names in os.walk(root_path, followlinks=True):
            temp_dirs = list(directories)
            for single_dir in temp_dirs:
                visiting_path = os.path.abspath(os.path.join(root, single_dir))
                if self._should_visit(include, exclude, visiting_path) is False:
                    directories.remove(single_dir)

            for directory in directories:
                combined_path = os.path.join(root, directory)

                if not self._is_package(combined_path):
                    continue

                package_name = self._get_package_name(combined_path, root_path)
                if self._is_ignored_package(package_name):
                    continue

                package_class = self._get_package_class(package_name)
                if package_class is not None and package_class.ENABLED is False:
                    self._disabled_packages.append(package_name)
                    continue

                if self._is_disabled_package(package_name):
                    continue

                self._all_packages.append(package_name)

                if self._is_pyrin_package(package_name):
                    self._pyrin_components[package_name] = []
                elif self._is_custom_package(package_name):
                    self._custom_components[package_name] = []
                elif self._is_unit_test_package(package_name):
                    self._unit_test_components[package_name] = []
                elif self._is_integration_test_package(package_name):
                    self._integration_test_components[package_name] = []
                elif self._is_test_package(package_name):
                    self._test_components[package_name] = []
                else:
                    self._application_components[package_name] = []

                files = os.listdir(combined_path)
                for file_name in files:
                    if not self._is_module(file_name):
                        continue

                    module_name = file_name.replace('.py', '')
                    full_module_name = self._get_module_name(package_name, module_name)
                    if self._is_ignored_module(full_module_name):
                        continue

                    if self._is_pyrin_module(full_module_name):
                        self._pyrin_components[package_name].append(full_module_name)
                    elif self._is_custom_module(full_module_name):
                        self._custom_components[package_name].append(full_module_name)
                    elif self._is_unit_test_module(full_module_name):
                        self._unit_test_components[package_name].append(full_module_name)
                    elif self._is_integration_test_module(full_module_name):
                        self._integration_test_components[package_name].append(full_module_name)
                    elif self._is_test_module(full_module_name):
                        self._test_components[package_name].append(full_module_name)
                    else:
                        self._application_components[package_name].append(full_module_name)

        self._detach_all()

    def _detach_all(self):
        """
        detaches all founded components into extended and other components.
        """

        self._extended_application_components, \
            self._other_application_components = self._detach_extended_packages(
                list(self._pyrin_components.keys()), self._application_components)

        unit_test_base_components = self._application_components
        integration_test_base_components = self._application_components
        if len(self._application_components) <= 0:
            unit_test_base_components = self._pyrin_components
            integration_test_base_components = self._pyrin_components

        self._extended_unit_test_components, \
            self._other_unit_test_components = self._detach_extended_packages(
                list(unit_test_base_components.keys()),
                self._unit_test_components,
                main_package_name=self._configs.unit_test_package)

        self._extended_integration_test_components, \
            self._other_integration_test_components = self._detach_extended_packages(
                list(integration_test_base_components.keys()),
                self._integration_test_components,
                main_package_name=self._configs.integration_test_package)

    def _detach_extended_packages(self, base_components, components, **options):
        """
        detaches components which extend existing base components from new components.

        :param list[str] base_components: base component names.

        :param dict components: components which some of
                                them extend base components.

        :note components: dict[str package_name: list[str] modules]

        :keyword str main_package_name: main package name of given components.
                                        if not provided, it will be assumed equal
                                        to the first part of component name.
                                        for example: if component is `pyrin.api.schema`
                                        then, it will be assumed equal to `pyrin`.
                                        if the package structure has a root with more
                                        than one part, it should be provided manually.

        :returns: tuple[dict extended_components, dict other_components]

        :note extended_components: dict[str package_name: list[str] modules]
        :note other_components: dict[str package_name: list[str] modules]

        :rtype: tuple[dict, dict]
        """

        extended_components = DTO()
        other_components = DTO()
        if len(components) > 0:
            component_keys = list(components.keys())
            root_name = options.get('main_package_name', None)
            if root_name is None:
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

        return path_utils.get_main_package_name(component_name)

    def _is_included(self, include, visiting_path):
        """
        returns a value indicating that the given visiting path is under include path.

        :param list[str] include: full directory names inside the
                                  root path to just loop inside those.
                                  otherwise it loops in all available
                                  directories.

        :param str visiting_path: full path which must be checked for inclusion.

        :rtype: bool
        """

        if include is None or len(include) <= 0:
            return True

        for path in include:
            if visiting_path.startswith(path):
                return True

        return False

    def _is_excluded(self, exclude, visiting_path):
        """
        returns a value indicating that the given visiting path is under exclude path.

        :param list[str] exclude: full directory names inside the
                                  root path to ignore them. otherwise
                                  it loops in all available directories.

        :param str visiting_path: full path which must be checked for exclusion.

        :rtype: bool
        """

        if exclude is None or len(exclude) <= 0:
            return False

        for path in exclude:
            if visiting_path.startswith(path):
                return True

        return False

    def _should_visit(self, include, exclude, visiting_path):
        """
        gets a value indicating that given path should be visited.

        :param list[str] include: full directory names inside the
                                  root path to just loop inside those.
                                  otherwise it loops in all available
                                  directories.

        :param list[str] exclude: full directory names inside the
                                  root path to ignore them. otherwise
                                  it loops in all available directories.

        :param str visiting_path: full path which must be checked for exclusion.

        :rtype: bool
        """

        return self._is_included(include, visiting_path) is True and \
            self._is_excluded(exclude, visiting_path) is False

    def _is_equal(self, condition, full_module_or_package):
        """
        gets a value indicating that given name is equal with given condition.

        :param str condition: condition to compare with name.
                              for example: `*.database`, then all values
                              that have database in their second part
                              and their parts count are equal to or greater
                              than condition parts count will be recognized as equal.

        :param str full_module_or_package: module or package name to be compared.
                                           for example: `pyrin.database`.

        :rtype: bool
        """

        condition_parts = condition.split('.')
        full_module_or_package_parts = full_module_or_package.split('.')

        if len(condition_parts) > len(full_module_or_package_parts):
            return False

        for index, item in enumerate(condition_parts):
            if item != '*' and item != full_module_or_package_parts[index]:
                return False

        return True

    def _is_disabled_package(self, package_name):
        """
        gets a value indicating that given package should be considered as disabled.

        it will be detected based on parent packages of this package.

        :param str package_name: full package name.
                                 example package_name = `pyrin.database`.

        :rtype: bool
        """

        for disabled in self._disabled_packages:
            if package_name.startswith(disabled) or self._is_equal(disabled, package_name):
                return True

        return False

    def _is_ignored_package(self, package_name):
        """
        gets a value indicating that given package should be ignored.

        :param str package_name: full package name.
                                 example package_name = `pyrin.database`.

        :rtype: bool
        """

        if package_name in self._required_packages:
            return True

        for ignored in self._configs.ignored_packages:
            if package_name.startswith(ignored) or self._is_equal(ignored, package_name):
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
            if module_name.endswith(ignored) or self._is_equal(ignored, module_name):
                return True

        return False

    def _is_pyrin_component(self, component_name):
        """
        gets a value indicating that given component is a pyrin component.

        :param str component_name: full package or module name.

        :rtype: bool
        """

        return self._contains(self._pyrin_package_name, component_name)

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

    def _is_other_application_package(self, package_name):
        """
        gets a value indicating that given package is from other application packages.

        :param str package_name: full package name.

        :rtype: bool
        """

        return package_name in self._other_application_components

    def _is_extended_application_package(self, package_name):
        """
        gets a value indicating that given package is an extended application package.

        :param str package_name: full package name.

        :rtype: bool
        """

        return package_name in self._extended_application_components

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

    def _is_unit_test_component(self, component_name):
        """
        gets a value indicating that given component is a unit test component.

        :param str component_name: full package or module name.

        :rtype: bool
        """

        return self._contains(self._configs.unit_test_package, component_name)

    def _is_unit_test_package(self, package_name):
        """
        gets a value indicating that given package is a unit test package.

        :param str package_name: full package name.
                                 example package_name = 'test.api'

        :rtype: bool
        """

        return self._is_unit_test_component(package_name)

    def _is_unit_test_module(self, module_name):
        """
        gets a value indicating that given module is a unit test module.

        :param str module_name: full module name.
                                example module_name = 'test.api.error_handlers'

        :rtype: bool
        """

        return self._is_unit_test_component(module_name)

    def _is_other_unit_test_package(self, package_name):
        """
        gets a value indicating that given package is from other unit packages.

        :param str package_name: full package name.

        :rtype: bool
        """

        return package_name in self._other_unit_test_components

    def _is_extended_unit_test_package(self, package_name):
        """
        gets a value indicating that given package is an extended unit test package.

        :param str package_name: full package name.

        :rtype: bool
        """

        return package_name in self._extended_unit_test_components

    def _is_integration_test_component(self, component_name):
        """
        gets a value indicating that given component is an integration test component.

        :param str component_name: full package or module name.

        :rtype: bool
        """

        return self._contains(self._configs.integration_test_package, component_name)

    def _is_integration_test_package(self, package_name):
        """
        gets a value indicating that given package is an integration test package.

        :param str package_name: full package name.
                                 example package_name = 'test.api'

        :rtype: bool
        """

        return self._is_integration_test_component(package_name)

    def _is_integration_test_module(self, module_name):
        """
        gets a value indicating that given module is an integration test module.

        :param str module_name: full module name.
                                example module_name = 'test.api.error_handlers'

        :rtype: bool
        """

        return self._is_integration_test_component(module_name)

    def _is_other_integration_test_package(self, package_name):
        """
        gets a value indicating that given package is from other integration test packages.

        :param str package_name: full package name.

        :rtype: bool
        """

        return package_name in self._other_integration_test_components

    def _is_extended_integration_test_package(self, package_name):
        """
        gets a value indicating that given package is an extended integration test package.

        :param str package_name: full package name.

        :rtype: bool
        """

        return package_name in self._extended_integration_test_components

    def _is_test_component(self, component_name):
        """
        gets a value indicating that given component is a test component.

        this method specifies those components that are test components but
        won't be included neither in unit nor integration test components.

        :param str component_name: full package or module name.

        :rtype: bool
        """

        if not self._is_integration_test_component(component_name) and \
                not self._is_unit_test_component(component_name):
            for root in self._test_roots_bases:
                is_test = self._contains(root, component_name)
                if is_test is True:
                    return True

        return False

    def _is_test_package(self, package_name):
        """
        gets a value indicating that given package is a test package.

        this method specifies those packages that are test packages but
        won't be included neither in unit nor integration test packages.

        :param str package_name: full package name.
                                 example package_name = 'test.api'

        :rtype: bool
        """

        return self._is_test_component(package_name)

    def _is_test_module(self, module_name):
        """
        gets a value indicating that given module is a test module.

        this method specifies those modules that are test modules but
        won't be included neither in unit nor integration test modules.

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

    def _get_package_name(self, path, root_path):
        """
        gets the full package name for provided path.

        :param str path: full path of package.
                         example path = `/home/src/pyrin/database`.

        :param str root_path: root path in which this path is located.
                              example root_path = `/home/src`

        :rtype: str
        """

        return path_utils.get_package_name(path, root_path)

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

        is_package = self._has_module(path, '__init__')
        if is_package is False:
            self._not_packages.append(path)

        return is_package and self._parent_is_package(path)

    def _parent_is_package(self, path):
        """
        gets a value indicating that the parent of given path is a python package.

        :param str path: full path of package.
                         example path = `/home/src/pyrin/database`.

        :rtype: bool
        """

        for not_package in self._not_packages:
            if path.startswith(not_package):
                return False

        return True

    def _is_module(self, file_name):
        """
        gets a value indicating that given file is a standalone python module.

        excluding `__init__` module which belongs to package.
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

    def get_loaded_packages(self):
        """
        gets the name of all loaded packages.

        :rtype: list[str]
        """

        return list(self._loaded_packages)

    def is_package_loaded(self, name):
        """
        gets a value indicating that given package is loaded.

        :param str name: package fully qualified name.

        :rtype: bool
        """

        return name in self._loaded_packages
