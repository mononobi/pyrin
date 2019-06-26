# -*- coding: utf-8 -*-
"""
database package.
"""

from pyrin.packaging.context import Package


class DatabasePackage(Package):
    """
    database package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.configuration']

    COMPONENT_NAME = 'database.component'
    CONFIG_STORE_NAMES = ['database']
