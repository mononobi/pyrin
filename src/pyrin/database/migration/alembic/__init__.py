# -*- coding: utf-8 -*-
"""
alembic package.
"""

from pyrin.packaging.base import Package


class AlembicPackage(Package):
    """
    alembic package class.
    """

    NAME = __name__
    COMPONENT_NAME = 'database.migration.alembic.component'
    CONFIG_STORE_NAMES = ['alembic']
    DEPENDS = ['pyrin.configuration',
               'pyrin.cli']
