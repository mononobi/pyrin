# -*- coding: utf-8 -*-
"""
users package.
"""

from pyrin.packaging import Package


class TestUsersPackage(Package):
    """
    test users package class.
    """

    NAME = __name__
    DEPENDS = []
    COMPONENT_NAME = 'security.users.component'
