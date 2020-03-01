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

    return platform.uname()[0].lower()


def is_windows():
    """
    gets a value indicating that underlying operating system is windows based.

    :rtype: bool
    """

    return 'win' in get_os_name()


def set_python_path(python_path):
    """
    adds the given path into `PYTHONPATH` variable.

    :param str python_path: python path to set.
    """

    python_path = os.path.abspath(python_path)
    os.environ['PYTHONPATH'] = python_path
    sys.path.append(python_path)
