# -*- coding: utf-8 -*-
"""
packaging settings.
"""

# packages that should be ignored from loading on server startup.
IGNORED_PACKAGES = ('bshop.core.packaging',
                    'bshop.core.application',
                    'bshop.settings')

# modules that should be ignored from loading on server startup.
IGNORED_MODULES = ('start',)

# directories that should be ignored completely.
IGNORED_DIRECTORIES = ('__pycache__',)

# base packages of system that should be loaded before other packages.
BASE_PACKAGES = ('bshop.core',)

# owner packages that should be loaded after all other packages,
# this packages will replace default behaviour of system.
OWNER_PACKAGES = ('', )

# test packages that should be loaded after all packages and owner packages have been loaded.
# this packages are used for unit testing and should not be loaded by default.
TEST_PACKAGES = ('', )
