# -*- coding: utf-8 -*-
"""
utils environment module.
"""

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
