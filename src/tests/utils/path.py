# -*- coding: utf-8 -*-
"""
utils path module.
"""

import os


def resolve_application_root_path():
    """
    gets the application root path where the main package is located.

    :rtype: str
    """

    current_module_directory = os.path.dirname(__file__)
    current_module_path = os.path.join(current_module_directory, 'path')
    current_module_path = current_module_path.replace('/', '.')
    current_module_name = __name__

    root_path = current_module_path.replace('{package}'
                                            .format(package=current_module_name), '')

    return root_path.replace('.', '/')
