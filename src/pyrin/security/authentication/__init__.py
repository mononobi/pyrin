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
    COMPONENT_NAME = 'security.authentication.component'
    CONFIG_STORE_NAMES = ['authentication']
    DEPENDS = ['pyrin.validator',
               'pyrin.configuration',
               'pyrin.database.model']
