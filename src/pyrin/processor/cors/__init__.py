# -*- coding: utf-8 -*-
"""
cors package.
"""

from pyrin.packaging.base import Package


class CORSPackage(Package):
    """
    cors package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.configuration']
    CONFIG_STORE_NAMES = ['cors']
    COMPONENT_NAME = 'processor.cors.component'
