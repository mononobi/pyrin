# -*- coding: utf-8 -*-
"""
router package.
"""

from pyrin.packaging.base import Package


class RouterPackage(Package):
    """
    router package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.database.paging']
    COMPONENT_NAME = 'api.router.component'
