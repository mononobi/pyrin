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
    COMPONENT_NAME = 'security.authorization.component'
    DEPENDS = ['pyrin.caching',
               'pyrin.configuration']
