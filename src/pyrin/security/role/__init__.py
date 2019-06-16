# -*- coding: utf-8 -*-
"""
role package.
"""

from pyrin.packaging.context import Package


class RolePackage(Package):
    """
    role package class.
    """

    NAME = __name__
    DEPENDS = []
    COMPONENT_NAME = 'pyrin.security.role.component'
