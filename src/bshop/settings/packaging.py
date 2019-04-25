# -*- coding: utf-8 -*-
"""
Packaging settings.
"""

# packages that should be ignored from loading on server startup.
IGNORED_PACKAGES = ['bshop.core.packaging',
                    'bshop.core.application',
                    'bshop.settings']

# modules that should be ignored from loading on server startup.
IGNORED_MODULES = ['services',
                   'models',
                   'start']

# directories that should be ignored.
IGNORED_DIRECTORIES = ['__pycache__']

# application root directory where the main package is there.
ROOT_DIRECTORY = '/home/mono/workspace/bshop_server/src/'
