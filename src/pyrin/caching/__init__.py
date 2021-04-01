# -*- coding: utf-8 -*-
"""
caching package.
"""

from pyrin.packaging.base import Package


class CachingPackage(Package):
    """
    caching package class.
    """

    NAME = __name__
    COMPONENT_NAME = 'caching.component'
    CONFIG_STORE_NAMES = ['caching']
    DEPENDS = ['pyrin.configuration',
               'pyrin.database.model']
