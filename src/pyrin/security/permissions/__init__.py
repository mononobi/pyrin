# -*- coding: utf-8 -*-
"""
permissions package.
"""

from pyrin.packaging import Package


class PermissionsPackage(Package):
    """
    permissions package class.
    """

    NAME = __name__
    DEPENDS = []
    COMPONENT_NAME = 'pyrin.security.permissions.component'
