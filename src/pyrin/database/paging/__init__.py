# -*- coding: utf-8 -*-
"""
database paging package.
"""

from pyrin.packaging.base import Package


class DatabasePagingPackage(Package):
    """
    database paging package class.
    """

    NAME = __name__
    COMPONENT_NAME = 'database.paging.component'
    DEPENDS = ['pyrin.configuration']
