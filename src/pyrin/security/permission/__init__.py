# -*- coding: utf-8 -*-
"""
permission package.
"""

from pyrin.packaging.base import Package


class PermissionPackage(Package):
    """
    permission package class.
    """

    NAME = __name__
    DEPENDS = []
    COMPONENT_NAME = 'security.permission.component'
