# -*- coding: utf-8 -*-
"""
hashing package.
"""

from pyrin.packaging.base import Package


class HashingPackage(Package):
    """
    hashing package class.
    """

    NAME = __name__
    DEPENDS = []
    COMPONENT_NAME = 'security.hashing.component'
