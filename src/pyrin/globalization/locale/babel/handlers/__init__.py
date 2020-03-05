# -*- coding: utf-8 -*-
"""
babel handlers package.
"""

from pyrin.packaging.base import Package


class BabelHandlersPackage(Package):
    """
    babel handlers package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.configuration']
