# -*- coding: utf-8 -*-
"""
api package.
"""

from pyrin.packaging.context import Package


class APIPackage(Package):
    """
    api package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.configuration']
    CONFIG_STORE_NAMES = ['api']
