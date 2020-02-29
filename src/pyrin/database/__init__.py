# -*- coding: utf-8 -*-
"""
database package.
"""

from pyrin.packaging.base import Package


class DatabasePackage(Package):
    """
    database package class.
    """

    NAME = __name__
    COMPONENT_NAME = 'database.component'

    DEPENDS = ['pyrin.configuration',
               'pyrin.logging']

    CONFIG_STORE_NAMES = ['database',
                          'database.binds']
