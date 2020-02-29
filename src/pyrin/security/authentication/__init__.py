# -*- coding: utf-8 -*-
"""
authentication package.
"""

from pyrin.packaging.base import Package


class AuthenticationPackage(Package):
    """
    authentication package class.
    """

    NAME = __name__
    DEPENDS = []
    COMPONENT_NAME = 'security.authentication.component'
