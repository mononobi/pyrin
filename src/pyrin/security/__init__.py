# -*- coding: utf-8 -*-
"""
security package.
"""

from pyrin.packaging.context import Package


class SecurityPackage(Package):
    """
    security package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.configuration']
    CONFIG_STORE_NAMES = ['security']
