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
    COMPONENT_NAME = 'api.router.component'
    DEPENDS = ['pyrin.database.paging',
               'pyrin.security.authentication']
