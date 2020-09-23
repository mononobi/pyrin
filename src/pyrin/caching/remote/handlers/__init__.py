# -*- coding: utf-8 -*-
"""
caching remote handlers package.
"""

from pyrin.packaging.base import Package


class CachingRemoteHandlersPackage(Package):
    """
    caching remote handlers package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.configuration',
               'pyrin.globalization.datetime',
               'pyrin.logging']
