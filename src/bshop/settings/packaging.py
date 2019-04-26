# -*- coding: utf-8 -*-
"""
Packaging settings.
"""

# packages that should be ignored from loading on server startup.
IGNORED_PACKAGES = ['bshop.core.packaging',
                    'bshop.core.application',
                    'bshop.settings']

# modules that should be ignored from loading on server startup.
IGNORED_MODULES = ['models',
                   'start']

# directories that should be ignored.
IGNORED_DIRECTORIES = ['__pycache__']
