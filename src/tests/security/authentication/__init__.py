# -*- coding: utf-8 -*-
"""
authentication package.
"""

from pyrin.packaging.context import Package


class TestAuthenticationPackage(Package):
    """
    test authentication package class.
    """

    NAME = __name__
    DEPENDS = []
    COMPONENT_NAME = 'security.authentication.component'
