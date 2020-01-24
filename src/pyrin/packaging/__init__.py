# -*- coding: utf-8 -*-
"""
packaging package.
"""

from pyrin.packaging.context import Package


class PackagingPackage(Package):
    """
    packaging package class.
    """

    NAME = __name__
    COMPONENT_NAME = 'packaging.component'
    CONFIG_STORE_NAMES = ['packaging']
