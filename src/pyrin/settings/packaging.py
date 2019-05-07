# -*- coding: utf-8 -*-
"""
packaging settings.
"""

# packages that should be ignored from loading on server startup.
IGNORED_PACKAGES = ('pyrin.packaging',
                    'pyrin.application',
                    'pyrin.settings')

# modules that should be ignored from loading on server startup.
IGNORED_MODULES = ('start',)

# directories that should be ignored completely.
IGNORED_DIRECTORIES = ('__pycache__',
                       'locale')

# base packages of system that should be loaded before other packages.
CORE_PACKAGES = ('pyrin',)

# custom packages that should be loaded after all other packages,
# this packages will replace default behavior of system.
CUSTOM_PACKAGES = ('', )

# test packages that should be loaded after all packages and custom packages have been loaded.
# this packages are used for unit testing and should not be loaded by default.
TEST_PACKAGES = ('', )
