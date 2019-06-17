# -*- coding: utf-8 -*-
"""
router package.
"""

from pyrin.packaging.context import Package


class RouterPackage(Package):
    """
    router package class.
    """

    NAME = __name__
    DEPENDS = []
    COMPONENT_NAME = 'api.router.component'
