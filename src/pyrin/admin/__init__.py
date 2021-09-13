# -*- coding: utf-8 -*-
"""
admin package.
"""

from pyrin.packaging.base import Package


class AdminPackage(Package):
    """
    admin package class.
    """

    NAME = __name__
    COMPONENT_NAME = 'admin.component'
    CONFIG_STORE_NAMES = ['admin']
    DEPENDS = ['pyrin.api.router',
               'pyrin.configuration',
               'pyrin.validator.auto']
