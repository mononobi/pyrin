# -*- coding: utf-8 -*-
"""
caching handlers package.
"""

from pyrin.packaging.base import Package


class CachingHandlersPackage(Package):
    """
    caching handlers package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.logging']
