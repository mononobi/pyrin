# -*- coding: utf-8 -*-
"""
pyrin packaging settings.
"""

# packages that should be ignored from loading on server startup.
# package names must be fully qualified.
# example: `pyrin.api.router`
# notice that if a package that has sub-packages added to ignore list,
# all of it's sub-packages will be ignored automatically even if not present in ignore list.
IGNORED_PACKAGES = ('pyrin.packaging',
                    'pyrin.application')

# modules that should be ignored from loading on server startup.
# module names could be full or just the module name itself.
# example for full name: `pyrin.api.enumerations`
# example for module name: `enumerations`
# notice that if only module name is provided, then all modules
# matching the provided name will be ignored from loading.
IGNORED_MODULES = ('start',)

# core packages of system that should be loaded before other packages.
# package names must be fully qualified.
# example: `app.core.pyrin`
CORE_PACKAGES = ('pyrin',)

# custom packages that should be loaded after core and application packages.
# this packages will replace default behavior of system.
# package names must be fully qualified.
# example: `app.custom.converters.json`
CUSTOM_PACKAGES = ('', )

# test packages that should be loaded after all other packages.
# these packages are used for unit testing and should not be loaded by default.
# package names must be fully qualified.
# example: `tests.api`
TEST_PACKAGES = ('', )

