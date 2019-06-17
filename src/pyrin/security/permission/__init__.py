# -*- coding: utf-8 -*-
"""
permission package.
"""

from pyrin.packaging import Package


class PermissionPackage(Package):
    """
    permission package class.
    """

    NAME = __name__
    DEPENDS = []
    COMPONENT_NAME = 'security.permission.component'
