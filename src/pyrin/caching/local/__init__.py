# -*- coding: utf-8 -*-
"""
caching local package.
"""


from pyrin.packaging.base import Package


class CachingLocalPackage(Package):
    """
    caching local package class.
    """

    NAME = __name__
