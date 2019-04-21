# -*- coding: utf-8 -*-
"""
Packaging settings.
"""

# packages that should be ignored from loading on server startup.
IGNORED_PACKAGES = ['bshop.core.packaging',
                    'bshop.core.application',
                    'bshop.settings']

# directories that should be ignored.
IGNORED_DIRECTORIES = ['__pycache__']

# modules that should be loaded on server startup from each package.
LOADABLE_MODULES = ['api',
                    'hooks',
                    'models']

# application root directory.
ROOT_DIRECTORY = '/home/mono/workspace/bshop_server/src/'
