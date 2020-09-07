# -*- coding: utf-8 -*-
"""
caching local handlers package.
"""

from pyrin.packaging.base import Package


class CachingLocalHandlersPackage(Package):
    """
    caching local handlers package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.configuration',
               'pyrin.logging']
