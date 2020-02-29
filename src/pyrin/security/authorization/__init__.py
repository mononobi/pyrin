# -*- coding: utf-8 -*-
"""
authorization package.
"""


from pyrin.packaging.base import Package


class AuthorizationPackage(Package):
    """
    authorization package class.
    """

    NAME = __name__
    DEPENDS = []
    COMPONENT_NAME = 'security.authorization.component'
