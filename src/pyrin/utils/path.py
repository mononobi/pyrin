# -*- coding: utf-8 -*-
"""
utils path module.
"""

import os
import sys


def get_module_file_path(module_name):
    """
    gets the absolute file path of module with given name.

    :param str module_name: module name to get its file path.

    :rtype: str
    """

    return os.path.abspath(sys.modules[module_name].__file__)


def get_main_package_name(module_name):
    """
    gets the main package name from given module name.
    for example for `pyrin.database.manager` module, it
    returns `pyrin` as the main package name.

    :param str module_name: module name to get its root package name.

    :rtype str
    """

    return module_name.split('.')[0]


def get_main_package_path(module_name):
    """
    gets the absolute path of the main package of module with given name.

    :param str module_name: module name to get its main package path.

    :rtype: str
    """

    relative_module_path = module_name.replace('.', '/')
    root_package = get_main_package_name(module_name)
    absolute_module_path = get_module_file_path(module_name)
    temp_absolute_module_path = absolute_module_path.replace(relative_module_path, '*')
    excess_part = temp_absolute_module_path.split('*')[-1]
    list_path = list(temp_absolute_module_path)

    for i in range(-1, -len(list_path), -1):
        if list_path[i] == '*':
            list_path[i] = root_package
            break

    main_package_path = ''.join(list_path)
    main_package_path = main_package_path.replace('*', relative_module_path)
    main_package_path = main_package_path.replace(excess_part, '').rstrip('/')

    return main_package_path


def get_pyrin_main_package_name():
    """
    gets the name of pyrin main package name.
    it would always be `pyrin` in normal cases.

    :rtype: str
    """

    return get_main_package_name(__name__)


def get_pyrin_main_package_path():
    """
    gets the absolute path of pyrin main package.

    :rtype: str
    """

    return get_main_package_path(__name__)
