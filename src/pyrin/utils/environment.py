# -*- coding: utf-8 -*-
"""
utils environment module.
"""

import os
import sys
import platform


def get_os_name():
    """
    gets current os name.

    :rtype: str
    """

    return platform.system()


def is_linux():
    """
    gets a value indicating that underlying operating system is linux based.

    :rtype: bool
    """

    return 'linux' in get_os_name().lower()


def is_windows():
    """
    gets a value indicating that underlying operating system is windows based.

    :rtype: bool
    """

    return 'windows' in get_os_name().lower()


def is_mac():
    """
    gets a value indicating that underlying operating system is mac based.

    :rtype: bool
    """

    name = get_os_name().lower()
    return 'macos' in name or 'darwin' in name


def is_java():
    """
    gets a value indicating that underlying operating system is java based.

    :rtype: bool
    """

    return 'java' in get_os_name().lower()


def set_python_path(python_path):
    """
    adds the given path into `PYTHONPATH` variable.

    :param str python_path: python path to set.
    """

    python_path = os.path.abspath(python_path)
    os.environ['PYTHONPATH'] = python_path
    sys.path.append(python_path)
